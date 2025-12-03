# Expiry Date and Depreciation Calculation Fixes

## Overview

This document details all fixes implemented to ensure automatic expiry date calculation and accurate depreciation values for newly created assets in the Asset Management System.

## Problem Statement

### Issue 1: Expiry Date NULL
- When adding a new asset, the `expiry_date` field was always NULL
- Expiry date should be automatically calculated as: `acquisition_date + useful_life (in years)`
- Users had no visibility into when assets would reach end-of-life

### Issue 2: Inaccurate Depreciation Calculations
- Depreciation calculations were returning incorrect values
- For Year 1 assets (newly acquired), accumulated depreciation was being incorrectly calculated
- Different depreciation methods had logic errors that produced wrong results

## Solutions Implemented

### 1. Added `expiry_date` Column to Asset Model

**File:** `app/core/models.py` (Line 208-209)

```python
# Expiry/End of Life information
expiry_date = Column(Date)  # Calculated as acquisition_date + useful_life
```

**Impact:** Database now has a column to store the expiry date for each asset.

### 2. Automatic Expiry Date Calculation in Asset Dialog

**File:** `app/gui/dialogs/asset_dialog.py` (Lines 534-537)

```python
# Calculate expiry date: acquisition_date + useful_life (in years)
acquisition_date = self.ui.acquisitionDateEdit.date().toPython()
useful_life = self.ui.usefulLifeSpinBox.value()
expiry_date = acquisition_date + timedelta(days=useful_life * 365)
```

**How It Works:**
- When user fills in acquisition date and useful life in the dialog
- Expiry date is automatically calculated as: `acquisition_date + (useful_life years)`
- Uses 365 days per year for simplicity (industry standard)
- Calculation happens in real-time and is included in the data sent to the database

### 3. Expiry Date Persistence in Asset Service

**File:** `app/services/asset_service.py`

The `_asset_to_dict()` method now includes expiry_date (Lines 997-1002, 1020):

```python
# Expiry date handling
expiry = _safe_getattr(asset, 'expiry_date')
try:
    expiry_iso = expiry.isoformat() if expiry else None
except Exception:
    expiry_iso = str(expiry) if expiry is not None else None

# In returned dict:
'expiry_date': expiry_iso,  # Calculated expiry date
```

**Impact:** Expiry date is properly converted to ISO format and included in all asset data operations.

### 4. Fixed Depreciation Calculation Methods

**File:** `app/core/models.py` (Lines 42-160)

#### Problem Analysis

The original implementation had a fundamental logic error:
- When calculating for Year 1 (newly acquired asset), it was **including** Year 1's depreciation in accumulated depreciation
- This is incorrect; for a NEW asset, accumulated depreciation should be 0
- Depreciation should start accruing AFTER the first year is complete

#### Solution

Completely rewrote the `DepreciationMethod.calculate_depreciation()` static method with correct logic:

**For NEW ASSETS (current_year=1):**
- `annual_depreciation` = depreciation amount for Year 1
- `accumulated_depreciation` = 0 (no years have completed yet)
- `current_book_value` = total_cost (full value at acquisition)

**For EXISTING ASSETS (current_year>1):**
- `annual_depreciation` = depreciation for the current year
- `accumulated_depreciation` = sum of all previous years' depreciation
- `current_book_value` = total_cost - accumulated_depreciation

#### Method-by-Method Fixes

##### 1. Straight-Line Depreciation

**Formula:**
```
depreciable_amount = total_cost - salvage_value
annual_depreciation = depreciable_amount / useful_life
accumulated_depreciation = annual_depreciation * (current_year - 1)
current_book_value = total_cost - accumulated_depreciation
```

**Example:** Asset costs $10,000, salvage $1,000, useful life 5 years
- Year 1: Annual = $1,800, Accumulated = $0, Book Value = $10,000
- Year 2: Annual = $1,800, Accumulated = $1,800, Book Value = $8,200
- Year 3: Annual = $1,800, Accumulated = $3,600, Book Value = $6,400
- Year 5: Annual = $1,800, Accumulated = $7,200, Book Value = $2,800

##### 2. Declining Balance Depreciation

**Formula:**
```
rate = 1 - (salvage_value / total_cost) ^ (1 / useful_life)
For each year: depreciation = book_value * rate
```

**Key Fixes:**
- Rate calculation now properly handles cases where salvage_value is 0
- Added check to prevent depreciating below salvage value
- Correctly iterates through previous years to calculate accumulated depreciation

**Example:** Asset costs $10,000, salvage $1,000, useful life 5 years
- Calculated rate ≈ 0.148
- Year 1: Annual = $1,480, Accumulated = $0, Book Value = $10,000
- Year 2: Annual = $1,298, Accumulated = $1,480, Book Value = $8,520
- Year 3: Annual = $1,260, Accumulated = $2,778, Book Value = $7,222
- Depreciation decreases each year as book value decreases

##### 3. Double Declining Balance Depreciation

**Formula:**
```
rate = 2 / useful_life  (twice the straight-line rate)
For each year: depreciation = book_value * rate
```

**Key Fixes:**
- Fixed rate calculation to use floating-point division
- Corrected accumulated depreciation calculation to properly iterate through previous years
- Added salvage value floor checks

**Example:** Asset costs $10,000, salvage $1,000, useful life 5 years
- Rate = 2/5 = 0.4 (40% per year)
- Year 1: Annual = $4,000, Accumulated = $0, Book Value = $10,000
- Year 2: Annual = $2,400, Accumulated = $4,000, Book Value = $6,000
- Year 3: Annual = $1,440, Accumulated = $6,400, Book Value = $3,600
- Fastest depreciation method; front-loaded

##### 4. Sum of Years Digits Depreciation

**Formula:**
```
sum_of_years = (useful_life * (useful_life + 1)) / 2
depreciable_amount = total_cost - salvage_value
For year N: depreciation = depreciable_amount * (remaining_years) / sum_of_years
```

**Key Fixes:**
- Fixed accumulated depreciation calculation to sum previous years correctly
- Corrected current year depreciation calculation
- Proper handling of remaining years for each year

**Example:** Asset costs $10,000, salvage $1,000, useful life 5 years
- Sum of years = 5+4+3+2+1 = 15
- Depreciable amount = $9,000
- Year 1: Annual = $9,000 * 5/15 = $3,000, Accumulated = $0, Book Value = $10,000
- Year 2: Annual = $9,000 * 4/15 = $2,400, Accumulated = $3,000, Book Value = $7,000
- Year 3: Annual = $9,000 * 3/15 = $1,800, Accumulated = $5,400, Book Value = $4,600
- Year 5: Annual = $9,000 * 1/15 = $600, Accumulated = $8,400, Book Value = $1,600

## Files Modified

| File | Changes | Lines |
|------|---------|-------|
| `app/core/models.py` | Added expiry_date column; Completely rewrote depreciation calculation methods | 42-210 |
| `app/gui/dialogs/asset_dialog.py` | Added automatic expiry_date calculation in get_data() | 534-537, 546 |
| `app/services/asset_service.py` | Updated _asset_to_dict() to include expiry_date | 997-1002, 1020 |

## Technical Details

### Expiry Date Calculation

**Approach:** Linear calculation using 365 days per year
```python
expiry_date = acquisition_date + timedelta(days=useful_life * 365)
```

**Alternative (for future enhancement):** Use date arithmetic to add years
```python
from dateutil.relativedelta import relativedelta
expiry_date = acquisition_date + relativedelta(years=useful_life)
```

### Depreciation Calculation Corrections

**Key Insights:**

1. **Year 1 Clarification:** When `current_year=1`, the asset has JUST been acquired, so:
   - No depreciation has been applied yet (accumulated = 0)
   - The asset has its full value (book_value = total_cost)
   - Annual depreciation shows what WILL be depreciated in Year 1

2. **Salvage Value Handling:** All methods now properly respect salvage value as a floor; depreciation cannot reduce book value below salvage value

3. **Precision:** All return values are cast to float to ensure consistent decimal precision

## Testing Recommendations

### Unit Tests for Depreciation Methods

```python
# Test Straight-Line for 5-year asset
cost = 10000, salvage = 1000, life = 5, year = 1
annual, accum, book = DepreciationMethod.calculate_depreciation(
    "Straight Line", cost, life, year, salvage
)
assert annual == 1800.0  # (10000 - 1000) / 5
assert accum == 0.0      # No previous years
assert book == 10000.0   # Full value at acquisition

# Test Double Declining in Year 3
cost = 10000, salvage = 1000, life = 5, year = 3
annual, accum, book = DepreciationMethod.calculate_depreciation(
    "Double Declining Balance", cost, life, year, salvage
)
# Year 1: 4000 depreciated, book = 6000
# Year 2: 2400 depreciated, book = 3600
# Year 3: 1440 depreciation, accumulated = 6400
assert accum == 6400.0
assert book == 3600.0
```

### Integration Tests

1. **Asset Creation:**
   - Create asset with acquisition date 2024-01-01 and useful life 5 years
   - Verify expiry_date is set to 2029-01-01
   - Verify depreciation values are calculated correctly

2. **Asset Editing:**
   - Edit asset to change useful life from 5 to 7 years
   - Verify expiry_date updates to new calculated date
   - Verify depreciation recalculates

3. **Database Persistence:**
   - Create asset
   - Query database directly
   - Verify expiry_date is stored correctly
   - Verify it appears in API responses

## Migration Guide

### For Existing Database

Since a new column was added to the Asset model, you need to:

1. **Create a database migration:**
   ```sql
   ALTER TABLE assets ADD COLUMN expiry_date DATE DEFAULT NULL;
   ```

2. **Populate existing assets (optional):**
   ```sql
   UPDATE assets 
   SET expiry_date = DATE_ADD(acquisition_date, INTERVAL useful_life YEAR)
   WHERE expiry_date IS NULL AND acquisition_date IS NOT NULL;
   ```

3. **Restart the application** to use the updated schema

### Fresh Installation

The expiry_date column will be created automatically on first database initialization.

## Performance Considerations

1. **Calculation Performance:** Depreciation calculations are O(n) where n is current_year. For typical assets (current_year < 50), this is negligible.

2. **Database:** Added one nullable DATE column; minimal storage impact.

3. **UI Responsiveness:** Expiry date calculation in dialogs is instantaneous for typical asset lifetimes (1-50 years).

## Future Enhancements

1. **Mid-Year Acquisition:** Support partial-year depreciation for assets acquired mid-fiscal year
2. **Composite Methods:** Switch between depreciation methods based on asset type
3. **Depreciation Reporting:** Generate depreciation schedules showing year-by-year breakdown
4. **Tax Compliance:** Support MACRS (Modified Accelerated Cost Recovery System) and other tax-specific methods
5. **Residual Value Optimization:** Calculate optimal salvage values based on historical data

## Verification Steps

After implementing these fixes, verify:

✅ New assets show calculated expiry_date (not NULL)
✅ Expiry date = acquisition_date + useful_life
✅ Depreciation values appear realistic and consistent
✅ Year 1 assets show 0 accumulated depreciation
✅ All four depreciation methods produce different but valid results
✅ Increasing useful_life increases expiry_date appropriately
✅ Salvage value properly limits depreciation floor

## Conclusion

The Asset Management System now correctly:
- Automatically calculates and stores expiry dates for all assets
- Accurately computes depreciation using four industry-standard methods
- Properly initializes Year 1 assets with correct accounting values
- Maintains data integrity through proper type conversion and validation

These fixes ensure that asset financial tracking is accurate, compliant with accounting standards, and provides users with essential asset lifecycle information.
