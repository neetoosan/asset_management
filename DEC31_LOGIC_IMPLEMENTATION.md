# Dec 31 Depreciation Logic - Implementation Complete

## Formula Applied
```
D = Number of Dec 31s between acquisition_date and evaluation_date (inclusive)
L_r = max(0, original_useful_life - D)
expiry_date = evaluation_date + (L_r × 365.25 days)
```

## Example: Asset acquired 2025-11-11, useful life 4 years

**Today (2025-11-12)**:
- Dec 31s passed: 0
- Remaining: 4 - 0 = 4 years  
- Expiry: 2025-11-12 + 4y = **2029-11-12**

**After Dec 31, 2025 (2026-01-01)**:
- Dec 31s passed: 1 (2025-12-31)
- Remaining: 4 - 1 = 3 years
- Expiry: 2026-01-01 + 3y = **2028-12-31** ✓

---

## Files Modified

### 1. **NEW**: `app/services/expiry_calculator.py`
- `count_dec31_since_acquisition()` - Counts Dec 31s
- `calculate_remaining_useful_life()` - Calculates L_r
- `calculate_expiry_date()` - Calculates final expiry

### 2. `app/gui/dialogs/asset_dialog.py`
- `display_expiry_date()` - Uses ExpiryCalculator
- `get_data()` - Uses ExpiryCalculator for DB save

### 3. `app/services/year_end_service.py`
- `process_year_end_depreciation()` - Uses ExpiryCalculator
- No manual date math, auto-calculated

---

## Works Everywhere

✅ Asset creation/edit (calculates & saves)
✅ Asset table view (displays from DB)
✅ Asset details (displays from DB)
✅ QR code (includes from DB)
✅ Year-end service (recalculates on Dec 31)
✅ Previously created assets (same logic)

---

## Testing

Run: `python app/services/expiry_calculator.py`

Output shows:
- 2025-11-11 + 4 years → 2029-11-12 ✓
- After Dec 31 → 2028-12-31 ✓
