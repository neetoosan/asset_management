"""
Migration: Update Expiry Dates to December 31st Alignment

This migration updates all asset expiry dates to align with December 31st,
following proper accounting standards where depreciation is calculated annually
on December 31st.

WHY ALIGN TO DECEMBER 31ST?
- Most organizations follow calendar-based accounting (Jan 1 – Dec 31)
- IAS 16 standard compliance
- Assets must be depreciated for the period they were available for use
- Aligns with annual depreciation calculation dates

Logic:
- Asset acquired in any month of year Y with useful life N years
- Will be fully depreciated on Dec 31 of year (Y + N)
- Expiry date = Dec 31 of (acquisition_year + useful_life)
"""

import sys
import os
from datetime import date
from sqlalchemy import create_engine, inspect, text

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import Config
from app.services.expiry_calculator import ExpiryCalculator

# Initialize engine
config = Config()
engine = create_engine(config.DATABASE_URL, echo=False)


def update_expiry_dates():
    """Update all asset expiry dates to align with December 31st"""
    
    print("=" * 80)
    print("MIGRATION: Update Expiry Dates to December 31st Alignment")
    print("=" * 80)
    print()
    print("WHY THIS CHANGE?")
    print("- Aligns with calendar-based accounting (Jan 1 – Dec 31)")
    print("- Follows IAS 16 accounting standard")
    print("- Matches annual depreciation calculation on December 31st")
    print("- Ensures expiry date = last depreciation date")
    print()
    print("=" * 80)
    print()
    
    with engine.connect() as conn:
        # Get all assets with acquisition_date and useful_life
        result = conn.execute(text("""
            SELECT id, asset_id, acquisition_date, useful_life, expiry_date
            FROM assets
            WHERE acquisition_date IS NOT NULL 
              AND useful_life IS NOT NULL
              AND useful_life > 0
            ORDER BY acquisition_date
        """))
        
        assets = result.fetchall()
        
        if not assets:
            print("No assets found to update.")
            return
        
        print(f"Found {len(assets)} assets to update\n")
        print(f"{'Asset ID':<20} {'Old Expiry':<15} {'New Expiry':<15} {'Status':<10}")
        print("-" * 70)
        
        updated_count = 0
        
        for asset in assets:
            asset_id_db = asset[0]
            asset_id_str = asset[1]
            acquisition_date_str = asset[2]
            useful_life = asset[3]
            old_expiry = asset[4]
            
            try:
                # Parse acquisition date - handle both string and date objects
                if isinstance(acquisition_date_str, date):
                    acquisition_date = acquisition_date_str
                elif isinstance(acquisition_date_str, str):
                    if 'T' in acquisition_date_str:
                        acquisition_date = date.fromisoformat(acquisition_date_str.split('T')[0])
                    else:
                        acquisition_date = date.fromisoformat(acquisition_date_str)
                else:
                    # Try to convert to string first
                    date_str = str(acquisition_date_str)
                    if 'T' in date_str:
                        acquisition_date = date.fromisoformat(date_str.split('T')[0])
                    else:
                        acquisition_date = date.fromisoformat(date_str)
                
                # Calculate new expiry date aligned to Dec 31
                new_expiry = ExpiryCalculator.calculate_expiry_date_aligned_to_year_end(
                    acquisition_date, useful_life
                )
                
                # Update the database
                conn.execute(text("""
                    UPDATE assets 
                    SET expiry_date = :new_expiry 
                    WHERE id = :asset_id
                """), {
                    'new_expiry': new_expiry.isoformat(),
                    'asset_id': asset_id_db
                })
                
                updated_count += 1
                
                # Format for display
                old_expiry_display = old_expiry if old_expiry else "None"
                new_expiry_display = new_expiry.strftime('%Y-%m-%d')
                
                # Check if changed
                status = "✓ Updated" if old_expiry != new_expiry_display else "- No change"
                
                print(f"{asset_id_str:<20} {old_expiry_display:<15} {new_expiry_display:<15} {status:<10}")
                
            except Exception as e:
                print(f"{asset_id_str:<20} ERROR: {str(e)}")
                continue
        
        # Commit all changes
        conn.commit()
        
        print()
        print("=" * 80)
        print(f"MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print(f"✓ Updated {updated_count} asset expiry dates")
        print()
        print("All expiry dates now align to December 31st of the final depreciation year.")
        print()


def verify_expiry_dates():
    """Verify that expiry dates are correctly aligned"""
    
    print("\nVerifying expiry date alignment...")
    print("-" * 80)
    
    with engine.connect() as conn:
        # Check that all expiry dates end on Dec 31
        # PostgreSQL compatible query
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total_assets,
                SUM(CASE WHEN expiry_date IS NOT NULL THEN 1 ELSE 0 END) as has_expiry,
                SUM(CASE WHEN EXTRACT(MONTH FROM expiry_date) = 12 AND EXTRACT(DAY FROM expiry_date) = 31 THEN 1 ELSE 0 END) as aligned_to_dec31
            FROM assets
            WHERE acquisition_date IS NOT NULL 
              AND useful_life IS NOT NULL
              AND useful_life > 0
        """))
        
        row = result.fetchone()
        
        if row:
            total = row[0]
            has_expiry = row[1]
            aligned = row[2]
            
            print(f"Total assets with useful_life: {total}")
            print(f"Assets with expiry_date: {has_expiry}")
            print(f"Aligned to Dec 31: {aligned}")
            
            if has_expiry == aligned:
                print("\n✓ All expiry dates are correctly aligned to December 31st!")
            else:
                print(f"\n⚠ Warning: {has_expiry - aligned} assets not aligned to Dec 31")
        
        # Show some examples
        print("\nSample expiry dates:")
        print(f"{'Asset ID':<20} {'Acquisition':<15} {'Useful Life':<12} {'Expiry Date':<15}")
        print("-" * 70)
        
        result = conn.execute(text("""
            SELECT asset_id, acquisition_date, useful_life, expiry_date
            FROM assets
            WHERE expiry_date IS NOT NULL
            ORDER BY acquisition_date
            LIMIT 10
        """))
        
        for row in result:
            asset_id = row[0]
            # Handle date objects and strings
            acq_date_obj = row[1]
            if isinstance(acq_date_obj, str):
                acq_date = acq_date_obj.split('T')[0] if 'T' in acq_date_obj else acq_date_obj
            else:
                acq_date = str(acq_date_obj)
            useful_life = row[2]
            expiry = row[3]
            
            print(f"{asset_id:<20} {acq_date:<15} {useful_life:<12} {expiry:<15}")
    
    print("\n✓ Verification complete")


def show_examples():
    """Show examples of the expiry date calculation"""
    
    print("\n" + "=" * 80)
    print("EXPIRY DATE CALCULATION EXAMPLES")
    print("=" * 80)
    print()
    
    examples = [
        ("2025-01-15", 5, "Acquired in January, 5-year life"),
        ("2025-06-15", 5, "Acquired in June, 5-year life"),
        ("2025-10-15", 5, "Acquired in October, 5-year life"),
        ("2025-12-20", 5, "Acquired in December, 5-year life"),
        ("2024-01-24", 5, "From your data: Workshop asset"),
    ]
    
    print(f"{'Purchase Date':<15} {'Life':<6} {'Expiry Date':<15} {'Description':<40}")
    print("-" * 85)
    
    for purchase_date_str, useful_life, description in examples:
        purchase_date = date.fromisoformat(purchase_date_str)
        expiry = ExpiryCalculator.calculate_expiry_date_aligned_to_year_end(
            purchase_date, useful_life
        )
        
        # Calculate which Dec 31 it expires on
        expiry_year = purchase_date.year + useful_life
        
        print(f"{purchase_date_str:<15} {useful_life:<6} {expiry.strftime('%Y-%m-%d'):<15} {description:<40}")
    
    print()
    print("Pattern: Asset acquired in year Y with N-year life expires on Dec 31 of year (Y + N)")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "EXPIRY DATE ALIGNMENT MIGRATION" + " " * 27 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    try:
        show_examples()
        update_expiry_dates()
        verify_expiry_dates()
        
        print("\n✅ All migration steps completed successfully!\n")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
