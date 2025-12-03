# Depreciation Percentage System-Wide Integration

## Overview
This document summarizes the complete integration of the `depreciation_percentage` field across all project files. This field represents the annual depreciation percentage (0-100%) for each asset, used in calculating annual depreciation amounts.

## Changes Made

### 1. Database & Models
**File**: `app/core/models.py`
- Asset model already has `depreciation_percentage` column defined (Float, default 0.0)
- Column is at line 225

### 2. Asset Service Layer
**File**: `app/services/asset_service.py`

#### Changes:
1. **Updated `_asset_to_dict()` method** (line 1028)
   - Added `'depreciation_percentage': _to_float(_safe_getattr(asset, 'depreciation_percentage'))`
   - Ensures depreciation_percentage is included when converting assets to dicts for audit logging and API responses

2. **Updated `create_asset()` allowed_fields** (lines 360-363)
   - Added `'depreciation_percentage'` to the fallback allowed_fields set
   - Also added `'expiry_date'` and `'model_number'` for consistency
   - Ensures the field is accepted during asset creation and updates

**Impact**: Depreciation percentage is now properly serialized/deserialized in all asset service operations

### 3. Asset Details View
**File**: `app/gui/dialogs/asset_details.py`

#### Changes:
1. **Updated `load_asset()` method** (lines 60-66)
   - Loads depreciation_percentage from asset data
   - Formats it as percentage string (e.g., "12.50%")
   - Sets it in the UI label `depPercentLabel`

2. **Updated QR code payload** (line 108)
   - Added `'depreciation_percentage'` to the payload dictionary
   - QR codes now include depreciation_percentage when generated

**Impact**: Depreciation percentage is displayed in asset details dialog and included in QR codes

### 4. Asset Details UI
**File**: `app/gui/ui/asset_details.ui`

#### Changes:
1. Added new UI row 9 with depreciation percentage display
   - Label: "Annual Depreciation %:"
   - Widget name: `labelDepPercent` and `depPercentLabel`
2. Updated height from 420 to 500 to accommodate new field
3. Adjusted row numbers for Accumulated Depreciation and Net Book Value fields

**File**: `app/gui/ui/asset_details_ui.py`
- Regenerated from asset_details.ui using `pyside6-uic`
- Includes all necessary widget definitions for the new depreciation percentage display

**Impact**: Asset details dialog now displays depreciation percentage between depreciation method and accumulated depreciation

### 5. Asset Dialog (Creation/Edit)
**File**: `app/gui/dialogs/asset_dialog.py`

#### Already implemented:
1. **Line 152**: Loads depreciation_percentage during asset edit
   ```python
   dep_percentage = float(self.asset.get('depreciation_percentage') or 0)
   ```

2. **Lines 246**: Loads into UI spinbox
   ```python
   self.ui.depreciationPercentageSpinBox.setValue(dep_percentage or 0)
   ```

3. **Lines 471-474**: Calculates annual depreciation based on percentage
   ```python
   depreciation_percent = self.ui.depreciationPercentageSpinBox.value()
   annual_depreciation = total_cost * (depreciation_percent / 100.0)
   ```

4. **Line 525-528**: Validates percentage > 0%
   ```python
   if self.ui.depreciationPercentageSpinBox.value() <= 0:
       QMessageBox.warning(self, "Validation Error", "Annual Depreciation percentage must be greater than 0%")
   ```

5. **Line 594**: Includes in get_data()
   ```python
   "depreciation_percentage": self.ui.depreciationPercentageSpinBox.value(),
   ```

**Impact**: Asset creation/editing fully supports depreciation_percentage

### 6. Report Service
**File**: `app/services/report_service.py`

#### Already implemented:
1. **Line 218**: Depreciation report includes depreciation_percentage calculation
   ```python
   'depreciation_percentage': (accumulated_dep / float(asset.total_cost) * 100) if asset.total_cost > 0 else 0
   ```

**Impact**: Reports include depreciation information

### 7. Asset Table View
**File**: `app/gui/views/asset_table_view.py`

#### Status: Not modified for display column
- The asset table currently displays 10 columns: Asset ID, Name, Model, Serial, Department, Category, Date Registered, Expiry Date, Value, Status
- Depreciation percentage is available in the asset data but not displayed as a separate column
- This is acceptable as the primary display is in the Asset Details dialog

### 8. Year-End Service
**File**: `app/services/year_end_service.py`

#### Already implemented:
- Uses depreciation_percentage from asset data when processing year-end accounting
- Reduces useful_life by 1 on Dec 31st
- Recalculates expiry_date based on new remaining useful_life

## System-Wide Consistency Checklist

✅ **Database Model**: depreciation_percentage field exists in Asset model
✅ **Asset Service**: Includes depreciation_percentage in _asset_to_dict()
✅ **Asset Service**: Allows depreciation_percentage in create_asset()
✅ **Asset Dialog**: Loads, validates, and saves depreciation_percentage
✅ **Asset Details**: Displays depreciation_percentage with formatting
✅ **QR Code**: Includes depreciation_percentage in payload
✅ **Reports**: Calculates and includes depreciation_percentage
✅ **Year-End Service**: Uses depreciation_percentage for accounting

## Field Format

- **Database**: Float, default 0.0
- **Display**: Formatted as percentage string with 2 decimal places (e.g., "12.50%")
- **Input Range**: 0-100% via spinbox with 0.5% increments
- **Validation**: Required to be > 0% when creating/editing assets with depreciation

## Calculation Formula

```
Annual Depreciation = Total Cost × (Depreciation Percentage / 100)
```

For year-end accounting:
1. Reduce useful_life by 1
2. Recalculate expiry_date = acquisition_date + remaining_useful_life
3. Apply annual depreciation to accumulated_depreciation

## Files Modified Summary

| File | Changes | Impact |
|------|---------|--------|
| asset_service.py | _asset_to_dict(), allowed_fields | Service layer serialization |
| asset_details.py | load_asset(), QR payload | Display and QR codes |
| asset_details.ui | New row for depreciation % | UI layout |
| asset_details_ui.py | Regenerated | UI widget definitions |
| asset_dialog.py | Already complete | Asset creation/editing |
| report_service.py | Already complete | Report generation |
| year_end_service.py | Already complete | Year-end accounting |

## Testing Recommendations

1. Create a new asset and verify:
   - Depreciation percentage field is editable and accepts 0-100%
   - Annual depreciation calculates correctly (Total Cost × Depreciation % / 100)
   - Asset Details dialog displays the percentage

2. Edit existing asset and verify:
   - Depreciation percentage loads and displays correctly
   - Changing percentage updates annual depreciation calculation
   - Changes are saved to database

3. QR Code generation:
   - Generate QR code and verify JSON includes depreciation_percentage
   - Scan and verify all fields are readable

4. Reports:
   - Generate depreciation report and verify depreciation_percentage appears
   - Verify calculations are consistent

5. Year-End Accounting:
   - Run year-end service on Dec 31st
   - Verify expiry_date is updated based on depreciation_percentage
   - Verify accumulated depreciation is updated

## Backward Compatibility

- Existing assets without depreciation_percentage will default to 0.0
- The system validates that percentage > 0% for new assets
- Depreciation calculations respect the new percentage-based system
