# Depreciation Quick Reference Guide

## Formula Summary

```
Yearly Depreciation = (Cost - Residual Value) / Useful Life
Monthly Depreciation = Yearly Depreciation / 12
Months in First Year = 12 - Purchase Month + 1
First Year Depreciation = Monthly Depreciation × Months in First Year
```

## Example: Asset Purchased October 15, 2025

```
Cost:              ₦500,000
Residual Value:    ₦50,000 (10%)
Useful Life:       5 years
Purchase Month:    October (10)

Calculations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Yearly Depreciation:   (500,000 - 50,000) / 5 = ₦90,000
Monthly Depreciation:  90,000 / 12 = ₦7,500
Months Used:           12 - 10 + 1 = 3
First Year:            7,500 × 3 = ₦22,500

Schedule:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dec 31, 2025: ₦22,500   (NBV: ₦477,500)  ← Prorated
Dec 31, 2026: ₦90,000   (NBV: ₦387,500)  ← Full year
Dec 31, 2027: ₦90,000   (NBV: ₦297,500)  ← Full year
Dec 31, 2028: ₦90,000   (NBV: ₦207,500)  ← Full year
Dec 31, 2029: ₦90,000   (NBV: ₦117,500)  ← Full year
Dec 31, 2030: STOPPED   (Useful life completed)
```

## Month-by-Month First Year Proration

| Purchase Month | Months Used | Example Depreciation* |
|----------------|-------------|----------------------|
| January        | 12          | ₦90,000 (100%)       |
| February       | 11          | ₦82,500 (92%)        |
| March          | 10          | ₦75,000 (83%)        |
| April          | 9           | ₦67,500 (75%)        |
| May            | 8           | ₦60,000 (67%)        |
| June           | 7           | ₦52,500 (58%)        |
| July           | 6           | ₦45,000 (50%)        |
| August         | 5           | ₦37,500 (42%)        |
| September      | 4           | ₦30,000 (33%)        |
| October        | 3           | ₦22,500 (25%)        |
| November       | 2           | ₦15,000 (17%)        |
| December       | 1           | ₦7,500 (8%)          |

*Based on ₦90,000 yearly depreciation

## Stopping Conditions

### Stop When Either Condition is Met:

1. **Net Book Value ≤ Residual Value**
   ```
   if NBV ≤ Residual Value:
       STOP
   ```

2. **Useful Life Completed**
   ```
   if Years Applied ≥ Useful Life:
       STOP
   ```

## Testing Commands

```bash
# Test the depreciation calculator
python app/services/depreciation_calculator.py

# Run comprehensive tests
python test_prorated_depreciation.py

# Run database migration
python migrations/add_prorated_depreciation_fields.py
```

## Key Files

| File | Purpose |
|------|---------|
| `app/services/depreciation_calculator.py` | Core depreciation logic |
| `app/services/year_end_service.py` | December 31st processing |
| `app/core/models.py` | Database model with new fields |
| `migrations/add_prorated_depreciation_fields.py` | Database migration |
| `test_prorated_depreciation.py` | Test suite |

## Database Fields

| Field | Type | Description |
|-------|------|-------------|
| `salvage_value` | REAL | 10% of total_cost (residual value) |
| `depreciation_years_applied` | INTEGER | Number of Dec 31 depreciations applied |

## Quick Check

To verify implementation is working:

```python
from app.services.depreciation_calculator import DepreciationCalculator

# Test October purchase
result = DepreciationCalculator.calculate_first_year_depreciation(
    cost=500000,
    residual_value=50000,
    useful_life=5,
    purchase_date="2025-10-15"
)

print(f"First year depreciation: ₦{result:,.2f}")
# Should output: First year depreciation: ₦22,500.00
```

## Common Scenarios

### Scenario 1: Asset Purchased at Start of Year (January)
- Gets **full year** depreciation in first year (12 months)

### Scenario 2: Asset Purchased Mid-Year (June)
- Gets **7 months** depreciation in first year
- Full year depreciation every year after

### Scenario 3: Asset Purchased at End of Year (December)
- Gets **1 month** depreciation in first year
- Full year depreciation every year after

### Scenario 4: Asset Reaches Residual Value Before Useful Life
- Depreciation **stops** when NBV = Residual Value
- Useful life counter may still have years remaining

### Scenario 5: Asset Completes Useful Life Before Reaching Residual Value
- Depreciation **stops** after final year
- NBV will be above residual value

## Troubleshooting

### Issue: Migration fails
**Solution:** Check that database file exists and is accessible

### Issue: Tests fail
**Solution:** Ensure all dependencies installed: `pip install sqlalchemy`

### Issue: Depreciation not applying
**Solution:** Check that asset has:
- Valid acquisition_date
- useful_life > 0
- total_cost > 0
- salvage_value set (should be 10% of total_cost)

## Support Matrix

| Feature | Status | Notes |
|---------|--------|-------|
| First-year proration | ✅ Working | Based on purchase month |
| Full yearly after first | ✅ Working | Applies full amount |
| Stop at residual value | ✅ Working | NBV won't go below salvage |
| Stop at useful life end | ✅ Working | Tracks years applied |
| December 31st only | ✅ Working | Annual calculation |
| Audit logging | ✅ Working | All changes tracked |

---

**Last Updated:** November 27, 2025  
**Version:** 1.0  
**Status:** ✅ Production Ready
