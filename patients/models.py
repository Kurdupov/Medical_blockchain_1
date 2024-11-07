import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=255)
    complaint = models.TextField(default='No complaint')  # Скарга пацієнта
    treatment = models.TextField(default='No treatment')  # Лікування
    visit_date = models.DateField()
    analysis_results = models.TextField()
    blockchain_hash = models.CharField(max_length=64, blank=True, null=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    checksum = models.CharField(max_length=64, blank=True, editable=False)

    def __str__(self):
        return f'{self.patient} - {self.diagnosis}'

    def save(self, *args, **kwargs):
        # При створенні запису встановлюємо контрольну суму
        if not self.pk:  # Це означає, що об'єкт створюється, а не оновлюється
            self.checksum = self.calculate_checksum()
        super().save(*args, **kwargs)

    def calculate_checksum(self):
        """
        Calculate SHA-256 checksum based on the data fields.
        """
        sha = hashlib.sha256()
        sha.update(f'{self.patient.id}{self.diagnosis}{self.complaint}{self.treatment}{self.visit_date}{self.analysis_results}'.encode('utf-8'))
        return sha.hexdigest()

    def has_data_changed(self):
        """
        Verify if the current data matches the stored checksum.
        """
        return self.calculate_checksum() != self.checksum

    def data_status(self):
        """
        Return if data has been modified.
        """
        return "Змінено" if self.has_data_changed() else "Не змінено"

class MedicalRecordHashHistory(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    blockchain_hash = models.CharField(max_length=64)

    def __str__(self):
        return f'Хеш історії для {self.medical_record} від {self.timestamp}'
