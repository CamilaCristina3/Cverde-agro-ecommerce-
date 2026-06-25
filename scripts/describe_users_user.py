import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cverde.settings')
import django
django.setup()
from django.db import connection
cur = connection.cursor()
cur.execute('SHOW COLUMNS FROM users_user')
for row in cur.fetchall():
    print(row)
