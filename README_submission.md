# Academic Submission — Coverde

This branch (`academic-submission`) contains a sanitized version of the project prepared for academic evaluation.

What I changed for submission:
- Removed production/local database files (sensitive data removed).
- Added `coverde_db_sanitized.sql` — schema-only sanitized dump (no personal data).
- Added this `README_submission.md` with run instructions.

Run instructions (recommended):

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Prepare the database and load sample fixtures:

```powershell
python manage.py migrate
python manage.py loaddata fixtures/seed_data.json
```

3. Run the development server:

```powershell
python manage.py runserver
```

Notes:
- If you need the schema-only SQL, `coverde_db_sanitized.sql` is included.
- The real `coverde_db.sql` and `db.sqlite3` were intentionally removed from this branch to avoid exposing sensitive data.
