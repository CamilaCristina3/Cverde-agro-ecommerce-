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

2. Prepare the database and load demo data (two options):

Option A — run the management command (recommended):

```powershell
python manage.py migrate
# Create a superuser and demo accounts + products
python manage.py create_demo_data
```

Option B — load the fixture JSON (useful if you prefer `loaddata`):

```powershell
python manage.py migrate
python manage.py loaddata fixtures/demo_seed.json
```

Demo accounts (available in both options):

- Superuser: `demoadmin` / `demoadminpass` (Django admin)
- Consumer: `alice` / `alicepass`
- Producer: `bobfarm` / `bobpass`

Both options are provided so the evaluator can choose the preferred setup method.

Note about demo accounts and evaluator steps:

- The demo users can be (re)created at any time by running:

```powershell
python manage.py create_demo_data
```

- If a `demoadmin` account already exists in the local database, its password may differ from the one documented above (it might have been changed after creation). To reset the `demoadmin` password, run:

```powershell
python manage.py changepassword demoadmin
```

- Note for evaluators: If `demoadmin` exists in your local database, either reset its password with `changepassword` or recreate the demo data with `create_demo_data` before starting your evaluation.

3. Run the development server:

```powershell
python manage.py runserver
```

Notes:
- If you need the schema-only SQL, `coverde_db_sanitized.sql` is included.
- The real `coverde_db.sql` and `db.sqlite3` were intentionally removed from this branch to avoid exposing sensitive data.
