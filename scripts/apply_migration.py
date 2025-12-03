"""
Small helper to run the SQL migration file using SQLAlchemy engine configured in the project.
This script attempts to import the project's DB URL or uses sqlite fallback.
Run from project root in your virtualenv:
    python scripts\apply_migration.py
"""
import os
import sqlalchemy
from sqlalchemy import text

SQL_FILE = os.path.join(os.path.dirname(__file__), '001_add_model_number.sql')

# Try to grab DB URL from environment or fallback
DB_URL = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_URI')

if not DB_URL:
    print("DATABASE_URL not set in environment. Please set it to your DB connection string.")
    print("Example (Windows PowerShell): $env:DATABASE_URL='postgresql://user:pass@localhost/dbname'")
    raise SystemExit(1)

engine = sqlalchemy.create_engine(DB_URL)

with open(SQL_FILE, 'r', encoding='utf-8') as f:
    sql = f.read()

with engine.connect() as conn:
    for stmt in sql.split(';'):
        stmt = stmt.strip()
        if not stmt:
            continue

        # Skip statements that are only SQL comments (lines starting with -- or /* ... */)
        lines = [ln.strip() for ln in stmt.splitlines()]
        if all((not ln or ln.startswith('--') or ln.startswith('/*') or ln.startswith('*/')) for ln in lines):
            # Nothing to execute (only comments)
            continue

        print('Executing:', stmt[:80])
        try:
            conn.execute(text(stmt))
            conn.commit()
        except Exception as e:
            print('Statement failed:', e)

print('Migration file executed (or attempted). Check output above for errors.')
