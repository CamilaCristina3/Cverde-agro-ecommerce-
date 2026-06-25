import os, django, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','cverde.settings')
import django
django.setup()
from django.db import connection

def run():
    cur = connection.cursor()
    db = None
    cur.execute('SELECT DATABASE()')
    db = cur.fetchone()[0]
    print(f"Connected to database: {db}")

    # find FK constraints referencing products_product
    cur.execute("""
        SELECT CONSTRAINT_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'orders_orderitem'
          AND REFERENCED_TABLE_NAME = 'products_product'
    """)
    rows = cur.fetchall()
    if not rows:
        print('No foreign keys found referencing products_product on orders_orderitem')
    else:
        for (constraint_name,) in rows:
            print(f"Dropping foreign key: {constraint_name}")
            cur.execute(f"ALTER TABLE orders_orderitem DROP FOREIGN KEY `{constraint_name}`")
            print('Dropped')

    # ensure no existing FK to users_product with same name
    # drop if exists
    try:
        cur.execute("SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='orders_orderitem' AND REFERENCED_TABLE_NAME='users_product'")
        existing = cur.fetchall()
        if existing:
            print('Existing FK(s) to users_product found:', existing)
            # don't drop them; assume OK
    except Exception as e:
        print('Error checking existing user_product FKs:', e)

    # add new FK
    try:
        print('Adding new FK orders_orderitem_product_id_fk -> users_product(id)')
        cur.execute("ALTER TABLE orders_orderitem ADD CONSTRAINT orders_orderitem_product_id_fk FOREIGN KEY (product_id) REFERENCES users_product(id) ON DELETE CASCADE")
        print('Added new FK')
    except Exception as e:
        print('Error adding FK:', e)

if __name__ == '__main__':
    run()
