# Medical Blockchain (prototype)

Django prototype of a medical information system in which every medical record is protected by a
**hash chain**. Master's thesis project (2024).

> **Note:** the "blockchain" in this prototype is a chain of SHA-256 hashes stored in the database,
> not a distributed network. Hyperledger Fabric is described in the thesis as the target architecture.

## How it works

- Each `MedicalRecord` stores `blockchain_hash` = SHA-256 of the record data **plus the hash of the
  previous record of the same patient** (ordered by visit date).
- Changing any record changes its hash and every following hash in that patient's chain.
- Old hashes are kept in `MedicalRecordHashHistory`.
- Each record also has a `checksum`, taken on creation, so the page can show whether the data was changed
  ("Змінено / Не змінено").
- The page `patients/patient/<id>/hash_chain/` shows the chain and verifies every link.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install Django djangorestframework      # add mysqlclient if you use MySQL

# quickest start, SQLite, no MySQL needed
export DB_ENGINE=sqlite
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

For MySQL, copy `.env.example`, set the `DB_*` variables and install `mysqlclient`
(see `requirements.txt`). Secrets are read from environment variables and are not stored in the repository.

## Stack

Python, Django, Django REST framework, MySQL (or SQLite for local runs), SHA-256 (`hashlib`).
