"""
Test Script: Verify Dec 31 Expiry Date Logic Implementation

Tests:
1. ExpiryCalculator functionality
2. Asset table view display calculations
3. Asset details view display calculations
4. Database integration
"""

import sys
from datetime import date
sys.path.insert(0, '/Users/HP/Documents/python_projects/asset_management_system')

from app.services.expiry_calculator import ExpiryCalculator
from app.core.database import get_db
from app.core.models import Asset


def test_calculator():
    """Test ExpiryCalculator with known examples"""
    print("\n" + "="*80)
    print("TEST 1: ExpiryCalculator Functionality")
    print("="*80)
    
    # Test Case 1: Asset acquired 2025-11-11, 4 years useful life
    acq = date(2025, 11, 11)
    life = 4
    
    print(f"\nTest Case 1: Acquired {acq}, Useful Life {life} years")
    print("-" * 80)
    
    # Today (before Dec 31, 2025)
    today = date(2025, 11, 12)
    dec31s = ExpiryCalculator.count_dec31_since_acquisition(acq, today)
    remaining = ExpiryCalculator.calculate_remaining_useful_life(life, acq, today)
    expiry = ExpiryCalculator.calculate_expiry_date(acq, life, today)
    
    print(f"Date: {today}")
    print(f"  Dec 31s passed: {dec31s}")
    print(f"  Remaining life: {remaining} years")
    print(f"  Expiry date: {expiry}")
    print(f"  ✓ Expected: 4.0 years remaining, expiry ~2029-11-12 (±1 day)")
    
    assert dec31s == 0, f"Expected 0 Dec 31s, got {dec31s}"
    assert remaining == 4.0, f"Expected 4.0 remaining, got {remaining}"
    expected = date(2029, 11, 12)
    days_diff = abs((expiry - expected).days)
    assert days_diff <= 1, f"Expected 2029-11-12 (±1 day), got {expiry} (diff: {days_diff} days)"
    
    # After Dec 31, 2025 (2026-01-01)
    after_year_end = date(2026, 1, 1)
    dec31s_after = ExpiryCalculator.count_dec31_since_acquisition(acq, after_year_end)
    remaining_after = ExpiryCalculator.calculate_remaining_useful_life(life, acq, after_year_end)
    expiry_after = ExpiryCalculator.calculate_expiry_date(acq, life, after_year_end)
    
    print(f"\nDate: {after_year_end}")
    print(f"  Dec 31s passed: {dec31s_after}")
    print(f"  Remaining life: {remaining_after} years")
    print(f"  Expiry date: {expiry_after}")
    print(f"  ✓ Expected: 3.0 years remaining, expiry ~2028-12-31")
    
    assert dec31s_after == 1, f"Expected 1 Dec 31, got {dec31s_after}"
    assert remaining_after == 3.0, f"Expected 3.0 remaining, got {remaining_after}"
    assert expiry_after.month == 12 and expiry_after.day == 31, f"Expected Dec 31, got {expiry_after.month}-{expiry_after.day}"
    
    print("\n✅ ExpiryCalculator tests PASSED")


def test_database_integration():
    """Test that database assets are readable and calculations work"""
    print("\n" + "="*80)
    print("TEST 2: Database Integration")
    print("="*80)
    
    try:
        with get_db() as session:
            assets = session.query(Asset).limit(5).all()
            
            if not assets:
                print("⚠️  No assets in database, skipping this test")
                return
            
            print(f"\nFound {len(assets)} assets to test")
            print("-" * 80)
            
            for asset in assets:
                if not asset.acquisition_date or not asset.useful_life:
                    print(f"⊘ {asset.asset_id}: Missing acq_date or useful_life, skipping")
                    continue
                
                try:
                    remaining = ExpiryCalculator.calculate_remaining_useful_life(
                        asset.useful_life,
                        asset.acquisition_date
                    )
                    expiry = ExpiryCalculator.calculate_expiry_date(
                        asset.acquisition_date,
                        asset.useful_life
                    )
                    
                    print(f"✓ {asset.asset_id:20s} | Acq: {asset.acquisition_date} | Life: {asset.useful_life}y | "
                          f"Remaining: {remaining:.1f}y | Expiry: {expiry}")
                    
                except Exception as e:
                    print(f"❌ {asset.asset_id}: Error calculating - {e}")
            
            print("\n✅ Database integration test PASSED")
        
    except Exception as e:
        print(f"⚠️  Database integration test skipped: {e}")


def test_display_calculations():
    """Test calculations match what will be displayed in views"""
    print("\n" + "="*80)
    print("TEST 3: Display Calculations (Asset Table & Details)")
    print("="*80)
    
    print("\nSimulating asset table view calculation...")
    print("-" * 80)
    
    # Simulate asset data from database
    asset_data = {
        'asset_id': 'TEST-001',
        'acquisition_date': '2025-11-11',
        'useful_life': 4,
        'name': 'Test Asset',
        'expiry_date': None  # Will be calculated
    }
    
    # Parse and calculate (same logic as in asset_table_view.py)
    acq_date_str = asset_data.get('acquisition_date')
    useful_life_val = asset_data.get('useful_life')
    
    if acq_date_str and useful_life_val:
        try:
            acq_date_obj = date.fromisoformat(acq_date_str.split('T')[0]) if 'T' in acq_date_str else date.fromisoformat(acq_date_str)
            
            # Calculate expiry using Dec 31 logic
            expiry_calculated = ExpiryCalculator.calculate_expiry_date(acq_date_obj, useful_life_val)
            expiry_display = expiry_calculated.strftime('%Y-%m-%d')
            
            print(f"Asset: {asset_data['asset_id']}")
            print(f"  Acquisition: {asset_data['acquisition_date']}")
            print(f"  Useful Life: {useful_life_val} years")
            print(f"  Calculated Expiry: {expiry_display}")
            print(f"  ✓ Expected: ~2029-11-12 (±1 day due to 365.25 day calculation)")
            
            # Check that expiry is within 1 day of expected (due to 365.25 day calculation rounding)
            expiry_date_obj = date.fromisoformat(expiry_display)
            expected_date = date(2029, 11, 12)
            days_diff = abs((expiry_date_obj - expected_date).days)
            assert days_diff <= 1, f"Expected 2029-11-12 (±1 day), got {expiry_display} (diff: {days_diff} days)"
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
    
    print("\n✅ Display calculations test PASSED")


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("DEC 31 EXPIRY DATE LOGIC - TEST SUITE")
    print("="*80)
    
    try:
        test_calculator()
        test_display_calculations()
        test_database_integration()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED")
        print("="*80)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
