# patients/utils.py
import hashlib


def compute_record_hash(record, previous_hash=''):
    """SHA-256 of the record data plus the hash of the previous record of the same patient."""
    payload = (
        f'{record.patient_id}{record.diagnosis}{record.visit_date}'
        f'{record.analysis_results}{record.complaint}{record.treatment}{previous_hash}'
    )
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()
