"""
Migration: Add salvage_value and depreciation_years_applied fields

This migration adds:
1. salvage_value column to assets table (defaults to 10% of total_cost)
2. depreciation_years_applied column to track number of Dec 31 depreciations applied
"""

import sys
import os
from datetime import datetime
from sqlalchemy import create_engine, inspect, text

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import Config

# Initialize engine
config = Config()
engine = create_engine(config.DATABASE_URL, echo=False)


def add_columns():
    """Add new columns to assets table"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('assets')]
    
    print("=" * 80)
    print("MIGRATION: Add Prorated Depreciation Fields")
    print("=" * 80)
    print()
    
    salvage_exists = 'salvage_value' in columns
    years_applied_exists = 'depreciation_years_applied' in columns
    
    if salvage_exists and years_applied_exists:
        print("✓ Columns already exist. No migration needed.")
        return
    
    with engine.connect() as conn:
        # Add salvage_value column if it doesn't exist
        if not salvage_exists:
            print("Adding salvage_value column...")
            conn.execute(text("""
                ALTER TABLE assets 
                ADD COLUMN salvage_value REAL DEFAULT 0.0
            """))
            conn.commit()
            print("✓ Added salvage_value column")
        else:
            print("✓ salvage_value column already exists")
        
        # Add depreciation_years_applied column if it doesn't exist
        if not years_applied_exists:
            print("\nAdding depreciation_years_applied column...")
            conn.execute(text("""
                ALTER TABLE assets 
                ADD COLUMN depreciation_years_applied INTEGER DEFAULT 0
            """))
            conn.commit()
            print("✓ Added depreciation_years_applied column")
        else:
            print("✓ depreciation_years_applied column already exists")
        
        # Update existing assets with salvage_value (10% of total_cost)
        print("\nUpdating existing assets with default salvage values (10% of total_cost)...")
        result = conn.execute(text("""
            UPDATE assets 
            SET salvage_value = total_cost * 0.10 
            WHERE salvage_value IS NULL OR salvage_value = 0
        """))
        conn.commit()
        print(f"✓ Updated {result.rowcount} assets with salvage values")
        
        # Update existing assets with depreciation_years_applied
        # Set to 0 for all assets (will be incremented on next Dec 31)
        print("\nInitializing depreciation_years_applied to 0 for existing assets...")
        result = conn.execute(text("""
            UPDATE assets 
            SET depreciation_years_applied = 0 
            WHERE depreciation_years_applied IS NULL
        """))
        conn.commit()
        print(f"✓ Initialized {result.rowcount} assets with depreciation_years_applied = 0")
    
    print()
    print("=" * 80)
    print("MIGRATION COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. New assets will automatically get salvage_value = 10% of total_cost")
    print("2. On December 31st, depreciation will be prorated for first year")
    print("3. Depreciation will stop when NBV reaches salvage_value")
    print()


def verify_migration():
    """Verify the migration was successful"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('assets')]
    
    print("\nVerifying migration...")
    print("-" * 80)
    
    # Check salvage_value
    if 'salvage_value' in columns:
        print("✓ salvage_value column exists")
    else:
        print("❌ salvage_value column NOT found")
        return False
    
    # Check depreciation_years_applied
    if 'depreciation_years_applied' in columns:
        print("✓ depreciation_years_applied column exists")
    else:
        print("❌ depreciation_years_applied column NOT found")
        return False
    
    # Check sample data
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total_assets,
                COUNT(salvage_value) as has_salvage,
                COUNT(depreciation_years_applied) as has_years_applied,
                AVG(salvage_value) as avg_salvage
            FROM assets
        """))
        
        row = result.fetchone()
        if row:
            print(f"\nAsset Statistics:")
            print(f"  Total assets: {row[0]}")
            print(f"  Assets with salvage_value: {row[1]}")
            print(f"  Assets with depreciation_years_applied: {row[2]}")
            print(f"  Average salvage value: ₦{row[3]:,.2f}" if row[3] else "  Average salvage value: N/A")
    
    print("\n✓ Migration verification successful")
    return True


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "PRORATED DEPRECIATION MIGRATION" + " " * 31 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    try:
        add_columns()
        verify_migration()
        
        print("\n✅ All migration steps completed successfully!\n")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}\n")
        sys.exit(1)
