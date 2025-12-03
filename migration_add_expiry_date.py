#!/usr/bin/env python
"""
Database Migration Script - Add expiry_date column to assets table

This script adds the missing expiry_date column to the assets table in PostgreSQL.
Run this before starting the application.

Usage:
    python migration_add_expiry_date.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_migration():
    """Run the migration to add expiry_date column"""
    try:
        from app.core.config import Config
        from sqlalchemy import create_engine, text
        
        print("🔄 Starting migration: Adding expiry_date column to assets table...")
        print("-" * 70)
        
        # Initialize database URL from config
        config = Config()
        engine = create_engine(config.DATABASE_URL, echo=False)
        
        # Get a connection
        connection = engine.connect()
        
        try:
            # Check if column already exists
            result = connection.execute(
                text("""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.columns 
                        WHERE table_name='assets' 
                        AND column_name='expiry_date'
                    )
                """)
            )
            
            column_exists = result.scalar()
            
            if column_exists:
                print("✅ Column 'expiry_date' already exists. No migration needed.")
                connection.close()
                return True
            
            # Add the column
            print("📝 Adding expiry_date column to assets table...")
            connection.execute(
                text("""
                    ALTER TABLE assets 
                    ADD COLUMN expiry_date DATE DEFAULT NULL
                """)
            )
            connection.commit()
            print("✅ Column added successfully!")
            
            # Optionally populate expiry_date for existing assets
            print("\n📋 Populating expiry_date for existing assets...")
            result = connection.execute(
                text("""
                    SELECT COUNT(*) as count 
                    FROM assets 
                    WHERE acquisition_date IS NOT NULL 
                    AND useful_life IS NOT NULL 
                    AND expiry_date IS NULL
                """)
            )
            
            count = result.scalar()
            
            if count > 0:
                print(f"   Found {count} assets without expiry_date")
                print("   Calculating and updating...")
                
                connection.execute(
                    text("""
                        UPDATE assets 
                        SET expiry_date = acquisition_date + (useful_life || ' years')::interval
                        WHERE acquisition_date IS NOT NULL 
                        AND useful_life IS NOT NULL 
                        AND expiry_date IS NULL
                    """)
                )
                connection.commit()
                print(f"✅ Updated {count} assets with calculated expiry dates!")
            else:
                print("   No existing assets to update (or all already have expiry_date)")
            
            print("\n" + "-" * 70)
            print("✅ Migration completed successfully!")
            print("\nYou can now start the application:")
            print("   python -m app.main")
            return True
        
        finally:
            connection.close()
            engine.dispose()
            
    except Exception as e:
        print(f"\n❌ Migration failed with error:")
        print(f"   {type(e).__name__}: {str(e)}")
        print("\n📌 Manual Migration SQL (if needed):")
        print("""
        -- Add the column
        ALTER TABLE assets ADD COLUMN expiry_date DATE DEFAULT NULL;
        
        -- Populate existing assets with expiry_date
        UPDATE assets 
        SET expiry_date = acquisition_date + (useful_life || ' years')::interval
        WHERE acquisition_date IS NOT NULL 
        AND useful_life IS NOT NULL 
        AND expiry_date IS NULL;
        
        -- Verify the update
        SELECT asset_id, acquisition_date, useful_life, expiry_date 
        FROM assets 
        WHERE acquisition_date IS NOT NULL 
        LIMIT 5;
        """)
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
