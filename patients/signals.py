import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MedicalRecord, MedicalRecordHashHistory
import hashlib

logger = logging.getLogger(__name__)

@receiver(post_save, sender=MedicalRecord)
def update_blockchain_chain(sender, instance, **kwargs):
    # Отримуємо всі записи пацієнта в правильному порядку
    records = MedicalRecord.objects.filter(patient=instance.patient).order_by('visit_date', 'id')

    def create_blockchain_record(patient_id, diagnosis, visit_date, analysis_results, complaint, treatment,
                                 previous_hash):
        """
        Створює новий блокчейн-хеш для медичного запису.
        """
        sha = hashlib.sha256()
        sha.update(f'{patient_id}{diagnosis}{visit_date}{analysis_results}{complaint}{treatment}{previous_hash}'.encode(
            'utf-8'))
        return sha.hexdigest()

    previous_hash = ''
    for record in records:
        new_hash = create_blockchain_record(
            record.patient.id,
            record.diagnosis,
            record.visit_date,
            record.analysis_results,
            record.complaint,
            record.treatment,
            previous_hash
        )
        if record.blockchain_hash != new_hash:
            # Зберігаємо старий хеш в історію перед оновленням
            if record.blockchain_hash:
                MedicalRecordHashHistory.objects.create(
                    medical_record=record,
                    blockchain_hash=record.blockchain_hash
                )
            # Оновлюємо хеш запису
            logger.info(f"Updating blockchain hash for record ID {record.id}. New hash: {new_hash}")
            record.blockchain_hash = new_hash
            record.save(update_fields=['blockchain_hash'])

        previous_hash = new_hash
