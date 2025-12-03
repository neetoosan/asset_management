import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import Config
from sqlalchemy import create_engine, text

cfg = Config()
engine = create_engine(cfg.DATABASE_URL)

sql = "ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;"
print('Running SQL to add column `deleted_at` if missing...')
with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()
print('Done.')
