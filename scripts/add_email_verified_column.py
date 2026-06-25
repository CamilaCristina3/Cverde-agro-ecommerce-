import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cverde.settings')
import django
django.setup()
from django.db import connection
cur = connection.cursor()
cur.execute("SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users_user' AND COLUMN_NAME = 'email_verified_at'")
exists = cur.fetchone()[0]
if exists:
    print('Column email_verified_at already exists')
else:
    print('Adding column email_verified_at')
    cur.execute("ALTER TABLE users_user ADD COLUMN email_verified_at DATETIME NULL")
    print('Column added')
