#!/usr/bin/env python
"""
Migration: Add depreciation_percentage column to assets table

This migration adds support for storing the annual depreciation percentage
for each asset. The percentage will be used for year-end accounting calculations.
"""

import os
import sys
from sqlalchemy import create_engine, inspect, text

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.config import Config
from app.core.models import Asset

# Initialize engine with database URL from config
config = Config()
engine = create_engine(config.DATABASE_URL, echo=False)


def migrate_up():
    """Add depreciation_percentage column"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('assets')]
    
    if 'depreciation_percentage' not in columns:
        with engine.connect() as conn:
            # Use raw SQL to add column (compatible with SQLite and PostgreSQL)
            conn.execute(text(
                'ALTER TABLE assets ADD COLUMN depreciation_percentage REAL DEFAULT 0.0'
            ))
            conn.commit()
        print("✓ Added depreciation_percentage column to assets table")
    else:
        print("✓ depreciation_percentage column already exists")


def migrate_down():
    """Rollback: Remove depreciation_percentage column"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('assets')]
    
    if 'depreciation_percentage' in columns:
        with engine.connect() as conn:
            try:
                # SQLite doesn't support DROP COLUMN directly
                conn.execute(text('ALTER TABLE assets DROP COLUMN depreciation_percentage'))
                conn.commit()
                print("✓ Removed depreciation_percentage column from assets table")
            except Exception as e:
                print(f"⚠ Could not drop column: {e}")
                print("  For SQLite, manual migration would be needed")
    else:
        print("✓ depreciation_percentage column does not exist")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "up"
    
    if action == "up":
        print("Running migration: Add depreciation_percentage column")
        migrate_up()
    elif action == "down":
        print("Running migration rollback: Remove depreciation_percentage column")
        migrate_down()
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
