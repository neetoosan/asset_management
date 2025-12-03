"""
Migration: Update all existing assets with expiry dates calculated using Dec 31 logic

This script:
1. Reads all assets from the database
2. Calculates new expiry_date using: expiry = acq_date + (remaining_life × 365.25 days)
   where remaining_life = original_useful_life - (number of Dec 31s since acquisition)
3. Updates the expiry_date column for each asset
4. Logs all changes
"""

import sys
import os
from datetime import datetime, date
sys.path.insert(0, '/Users/HP/Documents/python_projects/asset_management_system')

from app.core.database import get_db, init_db
from app.core.models import Asset
from app.services.expiry_calculator import ExpiryCalculator

# Initialize database
from app.core.config import Config
config = Config()
print(f"Initializing database: {config.DATABASE_URL}")
init_db(config.DATABASE_URL)

def migrate_expiry_dates():
    """Update all assets with new expiry date calculation using Dec 31 logic"""
    
    try:
        with get_db() as session:
            # Get all assets
            assets = session.query(Asset).filter(Asset.acquisition_date.isnot(None), Asset.useful_life.isnot(None)).all()
            
            updated_count = 0
            errors = []
            
            print(f"\nStarting migration: Processing {len(assets)} assets...")
            print("=" * 80)
            
            for idx, asset in enumerate(assets, 1):
                try:
                    old_expiry = asset.expiry_date
                    
                    # Calculate new expiry using Dec 31 logic
                    new_expiry = ExpiryCalculator.calculate_expiry_date(asset.acquisition_date, asset.useful_life)
                    
                    # Update asset
                    asset.expiry_date = new_expiry
                    
                    # Print progress
                    print(f"[{idx}/{len(assets)}] {asset.asset_id:20s} | Acq: {asset.acquisition_date} | "
                          f"Life: {asset.useful_life:2d}y | Old Expiry: {old_expiry} → New: {new_expiry}")
                    
                    updated_count += 1
                    
                except Exception as e:
                    error_msg = f"Asset {asset.asset_id}: {str(e)}"
                    errors.append(error_msg)
                    print(f"[{idx}/{len(assets)}] ❌ ERROR: {error_msg}")
            
            # Session will auto-commit when exiting the context manager
            print("=" * 80)
            print(f"\n✅ Migration completed!")
            print(f"   - Updated: {updated_count} assets")
            print(f"   - Errors: {len(errors)} assets")
            
            if errors:
                print(f"\n⚠️  Errors encountered:")
                for error in errors:
                    print(f"   - {error}")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise


if __name__ == "__main__":
    migrate_expiry_dates()
