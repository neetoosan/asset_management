# Asset Dialog Depreciation Implementation Guide

## Overview
The Asset Dialog in `app/gui/dialogs/asset_dialog.py` now properly calculates and displays depreciation values when adding or editing assets.

## UI Structure (from asset_dialog.ui)

The form includes the following fields:
- **Row 8**: Total Cost (read-only) - calculated from Quantity × Unit Cost
- **Row 9**: Useful Life (Years) - user input (1-50 years)
- **Row 10**: Depreciation Method - dropdown with 4 options
- **Row 11**: Accumulated Depreciation (read-only) - auto-calculated
- **Row 12**: Net Book Value (read-only) - auto-calculated

## Depreciation Calculation Flow

### When is calculation triggered?
The depreciation is automatically recalculated whenever:
1. **Unit Cost changes** → Total Cost updates → Depreciation recalculated
2. **Quantity changes** → Total Cost updates → Depreciation recalculated  
3. **Useful Life changes** → Depreciation recalculated directly
4. **Depreciation Method changes** → Depreciation recalculated with new method

### How it works
```python
# In calculate_depreciation() method (line 438)
annual_dep, accum_dep, net_book_value = DepreciationMethod.calculate_depreciation(
    method=method,              # Selected depreciation method (string)
    total_cost=total_cost,      # Total Cost from UI
    useful_life=useful_life,    # Useful Life in years
    current_year=1,             # Always 1 for NEW assets
    salvage_value=salvage_value # 10% of total cost by default
)
```

## Example: Total Cost ₦250,000, 4 Years, Declining Balance

### For NEW Asset (Year 1):
- **Annual Depreciation**: ₦109,414.67
- **Accumulated Depreciation**: ₦0.00
- **Net Book Value**: ₦250,000.00 (full value at acquisition)

### If we look at Year 2 (for reference):
- **Annual Depreciation**: ₦61,528.39
- **Accumulated Depreciation**: ₦109,414.67
- **Net Book Value**: ₦140,585.33

## Supported Depreciation Methods

### 1. Straight Line (Linear)
- **Formula**: Annual = (Total Cost - Salvage) / Useful Life
- **Example Year 1**: ₦56,250.00
- **Use Case**: Consistent depreciation for buildings, furniture

### 2. Declining Balance
- **Rate**: Calculated to reach salvage value over useful life
- **Formula**: Annual = Book Value × Rate (applied to decreasing balance)
- **Example Year 1**: ₦109,414.67
- **Use Case**: Equipment that loses value quickly initially

### 3. Double Declining Balance
- **Rate**: 2 / Useful Life (0.5 for 4-year asset)
- **Formula**: Annual = Book Value × Rate (fastest depreciation initially)
- **Example Year 1**: ₦125,000.00
- **Use Case**: Vehicles, computers with rapid obsolescence

### 4. Sum of Years Digits
- **Sum**: n(n+1)/2 where n = useful life (10 for 4-year asset)
- **Formula**: Annual = Depreciable Amount × (Remaining Years / Sum)
- **Example Year 1**: ₦90,000.00
- **Use Case**: Equipment with moderate front-loaded depreciation

## UI Display Format

All monetary values display with:
- Naira symbol: ₦
- Thousands separator: comma (,)
- 2 decimal places: .00

Example: ₦250,000.00

## Database Storage

When the asset is saved, the following values are stored in the database:
```python
"accumulated_depreciation": accumulated_depreciation,    # ₦0.00 for new asset
"annual_depreciation": annual_depreciation,              # Based on method
"net_book_value": net_book_value,                        # = Total Cost for new asset
"salvage_value": salvage_value,                          # 10% of total cost
"depreciation_method": selected_method_string            # e.g., "Declining Balance"
```

## Key Features

✅ **Real-time Calculation**: Updates display as user changes values
✅ **Multiple Methods**: All 4 standard depreciation methods supported
✅ **Year 1 Aware**: Recognizes new assets (accumulated depreciation = 0)
✅ **Fallback Salvage Value**: Defaults to 10% if not specified
✅ **Currency Formatted**: All values display with ₦ symbol and proper formatting
✅ **Read-only Fields**: Prevents manual entry of calculated fields
✅ **Audit Trail**: All depreciation data saved with asset for future calculations

## Testing Verification

Run the test suite to verify depreciation calculations:
```bash
python test_depreciation_calculation.py
```

Expected output shows all 4 methods correctly calculate:
- Accumulated Depreciation = ₦0.00 for new assets
- Net Book Value = Total Cost for new assets
- Each method's unique Annual Depreciation amount

## Important Notes

1. **New vs. Existing Assets**: Dialog always assumes new asset (current_year=1)
   - Accumulated depreciation will always be ₦0.00 in the dialog
   - This is correct for newly added assets
   - Existing assets' depreciation history is managed elsewhere

2. **Salvage Value**: Currently hardcoded to 10% of total cost
   - Can be made configurable in the future if needed
   - Affects the Declining Balance and Sum of Years calculations

3. **Rounding**: All values calculated to 2 decimal places for currency

## Future Enhancements

- Add a "Salvage Value" field for user customization
- Display depreciation schedule (Year 1, Year 2, etc.)
- Add preview of asset value over useful life
- Support partial year depreciation for mid-year purchases

## File References

- **Dialog Code**: `app/gui/dialogs/asset_dialog.py` (lines 438-491)
- **UI Definition**: `app/gui/ui/asset_dialog.ui` (rows 8-12)
- **Calculation Logic**: `app/core/models.py` (DepreciationMethod class, lines 42-160)
- **Test Suite**: `test_depreciation_calculation.py`
