import os, django, json, sys
from pathlib import Path
# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cverde.settings')
django.setup()
from django.db import connection
tables=['users_producer','users_product','users_category','users_order','users_orderitem','orders_order','orders_orderitem']
all_tables = connection.introspection.table_names()
print('All tables in DB:', all_tables)
out={}
cur=connection.cursor()
for t in tables:
    try:
        cur.execute(f"SHOW COLUMNS FROM {t}")
        out[t]=[list(row) for row in cur.fetchall()]
    except Exception as e:
        out[t]=str(e)
print(json.dumps(out, indent=2, ensure_ascii=False))
# Now list foreign key constraints for these tables
fk_query = '''
SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = DATABASE() AND REFERENCED_TABLE_NAME IS NOT NULL
AND TABLE_NAME IN (%s)
'''
table_list = ','.join([f"'{t}'" for t in tables])
try:
    cur.execute(fk_query % table_list)
    fks = [list(r) for r in cur.fetchall()]
except Exception as e:
    fks = str(e)
print('\nForeign keys:')
print(json.dumps(fks, indent=2, ensure_ascii=False))
