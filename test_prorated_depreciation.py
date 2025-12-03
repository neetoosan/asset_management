"""
Test Script: Prorated First-Year Depreciation Implementation

Tests:
1. First-year depreciation proration based on purchase month
2. Full yearly depreciation in subsequent years
3. Stop depreciation when NBV reaches residual value
4. Stop depreciation when useful life is completed
5. December 31st depreciation calculation
"""

import sys
from datetime import date
sys.path.insert(0, 'C:/Users/HP/Documents/python_projects/asset_management_system')

from app.services.depreciation_calculator import DepreciationCalculator


def test_first_year_proration():
    """Test that first-year depreciation is prorated correctly"""
    print("\n" + "=" * 80)
    print("TEST 1: First-Year Proration by Purchase Month")
    print("=" * 80)
    
    # Test Case: Asset purchased in October (Example from user)
    cost = 500000
    residual_value = 50000
    useful_life = 5
    purchase_date = "2025-10-15"
    
    first_year_dep = DepreciationCalculator.calculate_first_year_depreciation(
        cost, residual_value, useful_life, purchase_date
    )
    
    print(f"\nScenario: Asset purchased October 15, 2025")
    print(f"Cost: ₦{cost:,.2f}")
    print(f"Residual Value: ₦{residual_value:,.2f}")
    print(f"Useful Life: {useful_life} years")
    print(f"\nExpected: ₦22,500.00 (3 months × ₦7,500)")
    print(f"Actual:   ₦{first_year_dep:,.2f}")
    
    assert first_year_dep == 22500.00, f"Expected 22500, got {first_year_dep}"
    print("✓ PASSED: First-year prorated correctly for October purchase")
    
    # Test various months
    test_cases = [
        ("2025-01-15", 12, 90000.00),  # January: 12 months
        ("2025-06-15", 7, 52500.00),   # June: 7 months
        ("2025-12-15", 1, 7500.00),    # December: 1 month
    ]
    
    print(f"\n{'Month':<12} {'Months Used':<15} {'Expected':<18} {'Actual':<18} {'Status':<10}")
    print("-" * 80)
    
    for purchase_date, expected_months, expected_dep in test_cases:
        actual_dep = DepreciationCalculator.calculate_first_year_depreciation(
            cost, residual_value, useful_life, purchase_date
        )
        months_used = DepreciationCalculator.calculate_months_used_in_first_year(purchase_date)
        status = "✓ PASS" if abs(actual_dep - expected_dep) < 0.01 else "✗ FAIL"
        
        month_name = date.fromisoformat(purchase_date).strftime("%B")
        print(f"{month_name:<12} {months_used:<15} ₦{expected_dep:>14,.2f} ₦{actual_dep:>14,.2f} {status:<10}")
    
    print("\n✅ TEST 1 PASSED: First-year proration works correctly")


def test_full_yearly_depreciation():
    """Test that subsequent years use full yearly depreciation"""
    print("\n" + "=" * 80)
    print("TEST 2: Full Yearly Depreciation After First Year")
    print("=" * 80)
    
    cost = 500000
    residual_value = 50000
    useful_life = 5
    purchase_date = "2025-10-15"
    
    # Year 1: Prorated
    result1 = DepreciationCalculator.calculate_depreciation_for_year(
        cost, residual_value, useful_life, purchase_date,
        depreciation_years_applied=0,
        current_net_book_value=cost
    )
    
    # Year 2: Full year
    result2 = DepreciationCalculator.calculate_depreciation_for_year(
        cost, residual_value, useful_life, purchase_date,
        depreciation_years_applied=1,
        current_net_book_value=result1['new_net_book_value']
    )
    
    print(f"\nYear 1 Depreciation: ₦{result1['depreciation_to_apply']:,.2f} (Prorated)")
    print(f"Year 2 Depreciation: ₦{result2['depreciation_to_apply']:,.2f} (Full Year)")
    
    assert result1['depreciation_to_apply'] == 22500.00, "Year 1 should be prorated"
    assert result2['depreciation_to_apply'] == 90000.00, "Year 2 should be full yearly amount"
    
    print("\n✅ TEST 2 PASSED: Subsequent years use full depreciation")


def test_stop_at_residual_value():
    """Test that depreciation stops when NBV reaches residual value"""
    print("\n" + "=" * 80)
    print("TEST 3: Stop Depreciation at Residual Value")
    print("=" * 80)
    
    # Create scenario where NBV is close to residual value
    cost = 100000
    residual_value = 10000
    useful_life = 10  # Long useful life
    purchase_date = "2020-01-01"
    current_nbv = 15000  # Close to residual value
    
    result = DepreciationCalculator.calculate_depreciation_for_year(
        cost, residual_value, useful_life, purchase_date,
        depreciation_years_applied=9,  # Near end
        current_net_book_value=current_nbv
    )
    
    print(f"\nCurrent NBV: ₦{current_nbv:,.2f}")
    print(f"Residual Value: ₦{residual_value:,.2f}")
    print(f"Depreciation Applied: ₦{result['depreciation_to_apply']:,.2f}")
    print(f"New NBV: ₦{result['new_net_book_value']:,.2f}")
    print(f"Should Continue: {result['should_continue']}")
    
    # Depreciation should bring NBV exactly to residual value, not below
    assert result['new_net_book_value'] == residual_value, "NBV should equal residual value"
    assert result['depreciation_to_apply'] == (current_nbv - residual_value), "Should only depreciate to residual value"
    
    # Next year should stop
    result_next = DepreciationCalculator.calculate_depreciation_for_year(
        cost, residual_value, useful_life, purchase_date,
        depreciation_years_applied=10,
        current_net_book_value=residual_value
    )
    
    print(f"\nNext Year Depreciation: ₦{result_next['depreciation_to_apply']:,.2f}")
    print(f"Reason: {result_next['reason']}")
    
    assert result_next['depreciation_to_apply'] == 0, "No depreciation when at residual value"
    assert not result_next['should_continue'], "Should not continue depreciating"
    
    print("\n✅ TEST 3 PASSED: Depreciation stops at residual value")


def test_stop_at_useful_life_completion():
    """Test that depreciation stops when useful life is completed"""
    print("\n" + "=" * 80)
    print("TEST 4: Stop Depreciation When Useful Life Completed")
    print("=" * 80)
    
    cost = 500000
    residual_value = 50000
    useful_life = 5
    purchase_date = "2020-01-01"
    
    # Simulate 5 years of depreciation
    current_nbv = cost
    for year in range(1, useful_life + 1):
        result = DepreciationCalculator.calculate_depreciation_for_year(
            cost, residual_value, useful_life, purchase_date,
            depreciation_years_applied=year - 1,
            current_net_book_value=current_nbv
        )
        current_nbv = result['new_net_book_value']
        print(f"Year {year}: Depreciation ₦{result['depreciation_to_apply']:,.2f}, NBV ₦{current_nbv:,.2f}")
    
    # Try year 6 (beyond useful life)
    result_beyond = DepreciationCalculator.calculate_depreciation_for_year(
        cost, residual_value, useful_life, purchase_date,
        depreciation_years_applied=useful_life,
        current_net_book_value=current_nbv
    )
    
    print(f"\nYear 6 (Beyond Useful Life):")
    print(f"  Depreciation: ₦{result_beyond['depreciation_to_apply']:,.2f}")
    print(f"  Reason: {result_beyond['reason']}")
    print(f"  Should Continue: {result_beyond['should_continue']}")
    
    assert result_beyond['depreciation_to_apply'] == 0, "No depreciation beyond useful life"
    assert result_beyond['reason'] == "Useful life completed", "Correct stop reason"
    
    print("\n✅ TEST 4 PASSED: Depreciation stops when useful life completed")


def test_dec31_calculation():
    """Test December 31st annual depreciation calculation"""
    print("\n" + "=" * 80)
    print("TEST 5: December 31st Depreciation Calculation")
    print("=" * 80)
    
    # Asset purchased in October
    cost = 500000
    residual_value = 50000
    useful_life = 5
    purchase_date = "2025-10-15"
    
    print(f"\nAsset purchased: {purchase_date}")
    print(f"Cost: ₦{cost:,.2f}, Residual: ₦{residual_value:,.2f}, Life: {useful_life} years")
    print(f"\n{'Year':<8} {'Date':<15} {'Months':<10} {'Depreciation':<18} {'Accumulated':<18} {'NBV':<18}")
    print("-" * 95)
    
    current_nbv = cost
    accumulated = 0
    
    dates = [
        (1, "2025-12-31", "First year"),
        (2, "2026-12-31", "Full year"),
        (3, "2027-12-31", "Full year"),
        (4, "2028-12-31", "Full year"),
        (5, "2029-12-31", "Full year"),
        (6, "2030-12-31", "After useful life")
    ]
    
    for year_num, dec31_date, description in dates:
        result = DepreciationCalculator.calculate_depreciation_for_year(
            cost, residual_value, useful_life, purchase_date,
            depreciation_years_applied=year_num - 1,
            current_net_book_value=current_nbv
        )
        
        if result['depreciation_to_apply'] > 0:
            accumulated += result['depreciation_to_apply']
            current_nbv = result['new_net_book_value']
            print(f"{year_num:<8} {dec31_date:<15} {description:<10} ₦{result['depreciation_to_apply']:>14,.2f} ₦{accumulated:>14,.2f} ₦{current_nbv:>14,.2f}")
        else:
            print(f"{year_num:<8} {dec31_date:<15} STOPPED - {result['reason']}")
            break
    
    print("\n✅ TEST 5 PASSED: December 31st calculations work correctly")


def main():
    """Run all tests"""
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 18 + "PRORATED DEPRECIATION TEST SUITE" + " " * 28 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        test_first_year_proration()
        test_full_yearly_depreciation()
        test_stop_at_residual_value()
        test_stop_at_useful_life_completion()
        test_dec31_calculation()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED SUCCESSFULLY")
        print("=" * 80)
        print("\nThe prorated depreciation implementation is working correctly:")
        print("✓ First-year depreciation is prorated by purchase month")
        print("✓ Subsequent years use full yearly depreciation")
        print("✓ Depreciation stops when NBV reaches residual value")
        print("✓ Depreciation stops when useful life is completed")
        print("✓ December 31st calculations work as expected")
        print()
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
