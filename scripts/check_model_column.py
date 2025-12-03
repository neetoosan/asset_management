import os
import sqlalchemy

DB_URL = os.environ.get('DATABASE_URL')
if not DB_URL:
    print('DATABASE_URL not set')
    raise SystemExit(1)

engine = sqlalchemy.create_engine(DB_URL)
with engine.connect() as conn:
    res = conn.execute(sqlalchemy.text("SELECT column_name FROM information_schema.columns WHERE table_name='assets' AND column_name='model_number'"))
    rows = res.fetchall()
    if rows:
        print('model_number column exists')
        for r in rows:
            print(r)
    else:
        print('model_number column NOT found')
