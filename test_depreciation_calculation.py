#!/usr/bin/env python
"""
Test depreciation calculation to verify it matches user expectations.

For a NEW asset with:
- Total Cost: ₦250,000
- Useful Life: 4 years
- Depreciation Method: Declining Balance
- Current Year: 1 (new asset)
- Salvage Value: 10% = ₦25,000

Expected for Year 1:
- Annual Depreciation: calculated based on declining balance method
- Accumulated Depreciation: 0 (brand new)
- Net Book Value: ₦250,000 (at acquisition, full value)
"""

from app.core.models import DepreciationMethod

def test_declining_balance():
    """Test Declining Balance depreciation"""
    print("\n" + "="*70)
    print("TEST: Declining Balance Depreciation")
    print("="*70)
    
    total_cost = 250000
    useful_life = 4
    salvage_value = total_cost * 0.10  # 10% = 25,000
    
    # For new asset, current_year = 1
    annual_dep, accum_dep, book_value = DepreciationMethod.calculate_depreciation(
        method="Declining Balance",
        total_cost=total_cost,
        useful_life=useful_life,
        current_year=1,
        salvage_value=salvage_value
    )
    
    print(f"\nInput Parameters:")
    print(f"  Total Cost: ₦{total_cost:,.2f}")
    print(f"  Useful Life: {useful_life} years")
    print(f"  Salvage Value (10%): ₦{salvage_value:,.2f}")
    print(f"  Current Year: 1 (New Asset)")
    
    print(f"\nYear 1 Calculations (Declining Balance):")
    print(f"  Annual Depreciation: ₦{annual_dep:,.2f}")
    print(f"  Accumulated Depreciation: ₦{accum_dep:,.2f}")
    print(f"  Net Book Value: ₦{book_value:,.2f}")
    
    # Verify the values are correct for a new asset
    assert accum_dep == 0, f"❌ Accumulated depreciation should be 0 for new asset, got {accum_dep}"
    assert book_value == total_cost, f"❌ Book value should be {total_cost}, got {book_value}"
    assert annual_dep > 0, f"❌ Annual depreciation should be > 0, got {annual_dep}"
    
    print(f"\n✅ Year 1 values correct for new asset")
    
    # Now test Year 2
    annual_dep_y2, accum_dep_y2, book_value_y2 = DepreciationMethod.calculate_depreciation(
        method="Declining Balance",
        total_cost=total_cost,
        useful_life=useful_life,
        current_year=2,
        salvage_value=salvage_value
    )
    
    print(f"\nYear 2 Calculations (Declining Balance):")
    print(f"  Annual Depreciation: ₦{annual_dep_y2:,.2f}")
    print(f"  Accumulated Depreciation: ₦{accum_dep_y2:,.2f}")
    print(f"  Net Book Value: ₦{book_value_y2:,.2f}")
    
    # Accumulated should be Year 1's annual depreciation
    assert accum_dep_y2 == annual_dep, f"❌ Accumulated should equal Year 1 annual depreciation"
    assert book_value_y2 < total_cost, f"❌ Year 2 book value should be less than original"
    
    print(f"\n✅ Year 2 values correct")

def test_straight_line():
    """Test Straight Line depreciation"""
    print("\n" + "="*70)
    print("TEST: Straight Line Depreciation")
    print("="*70)
    
    total_cost = 250000
    useful_life = 4
    salvage_value = total_cost * 0.10  # 10% = 25,000
    
    annual_dep, accum_dep, book_value = DepreciationMethod.calculate_depreciation(
        method="Straight Line",
        total_cost=total_cost,
        useful_life=useful_life,
        current_year=1,
        salvage_value=salvage_value
    )
    
    print(f"\nYear 1 Calculations (Straight Line):")
    print(f"  Annual Depreciation: ₦{annual_dep:,.2f}")
    print(f"  Accumulated Depreciation: ₦{accum_dep:,.2f}")
    print(f"  Net Book Value: ₦{book_value:,.2f}")
    
    # For straight line: annual = (total - salvage) / useful_life
    expected_annual = (total_cost - salvage_value) / useful_life
    assert abs(annual_dep - expected_annual) < 0.01, f"Annual depreciation mismatch"
    assert accum_dep == 0, f"Accumulated depreciation should be 0 for new asset"
    assert book_value == total_cost, f"Book value should equal total cost for new asset"
    
    print(f"\n✅ Straight Line Year 1 correct")

def test_double_declining():
    """Test Double Declining Balance depreciation"""
    print("\n" + "="*70)
    print("TEST: Double Declining Balance Depreciation")
    print("="*70)
    
    total_cost = 250000
    useful_life = 4
    salvage_value = total_cost * 0.10  # 10% = 25,000
    
    annual_dep, accum_dep, book_value = DepreciationMethod.calculate_depreciation(
        method="Double Declining Balance",
        total_cost=total_cost,
        useful_life=useful_life,
        current_year=1,
        salvage_value=salvage_value
    )
    
    print(f"\nYear 1 Calculations (Double Declining):")
    print(f"  Annual Depreciation: ₦{annual_dep:,.2f}")
    print(f"  Accumulated Depreciation: ₦{accum_dep:,.2f}")
    print(f"  Net Book Value: ₦{book_value:,.2f}")
    
    # For double declining: rate = 2/useful_life, annual = total_cost * rate
    rate = 2.0 / useful_life
    expected_annual = total_cost * rate
    assert abs(annual_dep - expected_annual) < 0.01, f"Annual depreciation should be {expected_annual}, got {annual_dep}"
    assert accum_dep == 0, f"Accumulated depreciation should be 0 for new asset"
    assert book_value == total_cost, f"Book value should equal total cost for new asset"
    
    print(f"\n✅ Double Declining Year 1 correct")

def test_sum_of_years():
    """Test Sum of Years Digits depreciation"""
    print("\n" + "="*70)
    print("TEST: Sum of Years Digits Depreciation")
    print("="*70)
    
    total_cost = 250000
    useful_life = 4
    salvage_value = total_cost * 0.10  # 10% = 25,000
    
    annual_dep, accum_dep, book_value = DepreciationMethod.calculate_depreciation(
        method="Sum of Years Digits",
        total_cost=total_cost,
        useful_life=useful_life,
        current_year=1,
        salvage_value=salvage_value
    )
    
    print(f"\nYear 1 Calculations (Sum of Years Digits):")
    print(f"  Annual Depreciation: ₦{annual_dep:,.2f}")
    print(f"  Accumulated Depreciation: ₦{accum_dep:,.2f}")
    print(f"  Net Book Value: ₦{book_value:,.2f}")
    
    # For sum of years: sum = n(n+1)/2, year 1 fraction = 4/10
    sum_of_years = (useful_life * (useful_life + 1)) / 2.0
    depreciable_amount = total_cost - salvage_value
    expected_annual = (depreciable_amount * useful_life) / sum_of_years
    assert abs(annual_dep - expected_annual) < 0.01, f"Annual depreciation mismatch"
    assert accum_dep == 0, f"Accumulated depreciation should be 0 for new asset"
    assert book_value == total_cost, f"Book value should equal total cost for new asset"
    
    print(f"\n✅ Sum of Years Year 1 correct")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("DEPRECIATION CALCULATION TEST SUITE")
    print("Testing with: Total Cost = ₦250,000, Useful Life = 4 years")
    print("="*70)
    
    try:
        test_straight_line()
        test_declining_balance()
        test_double_declining()
        test_sum_of_years()
        
        print("\n" + "="*70)
        print("✅ ALL DEPRECIATION TESTS PASSED")
        print("="*70)
        print("\nKey Findings:")
        print("- For NEW assets (Year 1), Accumulated Depreciation = ₦0")
        print("- For NEW assets (Year 1), Net Book Value = Total Cost")
        print("- Each method calculates different Annual Depreciation amounts")
        print("- The dialog should display these values correctly")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
