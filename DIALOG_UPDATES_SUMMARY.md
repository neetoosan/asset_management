# Dialog Updates: Annual Depreciation and Asset Details

## Overview

The Asset Management System dialogs have been restructured with better logical separation:

✅ **Asset Dialog** - Shows Annual Depreciation (what users need when adding assets)
✅ **Asset Details Dialog** - Shows Accumulated Depreciation + other financial metrics (viewed after asset is saved)

## Changes Made

### 1. Asset Dialog (`asset_dialog.py` and `asset_dialog.ui`)

#### What Changed
- **Removed**: "Accumulated Depreciation" field (logical: not applicable for new assets)
- **Removed**: "Net Book Value" field (logical: calculated separately for existing assets)
- **Added**: "Annual Depreciation" field (displays expected Year 1 depreciation)

#### Why This Makes Sense
When adding a NEW asset, users don't care about accumulated depreciation (it's always 0). They need to know:
- How much the asset will depreciate PER YEAR
- This varies based on the depreciation method selected

#### User Experience
```
User fills in:
- Total Cost: ₦250,000
- Useful Life: 4 years
- Depreciation Method: Declining Balance

Dialog shows:
✅ Annual Depreciation: ₦109,414.67 (what they expect for Year 1)
```

### 2. Asset Details Dialog (`asset_details.py` and `asset_details.ui`)

#### What Changed
- **Added**: Expiry Date field (displays from database)
- **Added**: Useful Life field (for reference)
- **Added**: Depreciation Method field (what method was used)
- **Added**: Accumulated Depreciation field (total depreciation so far)
- **Renamed**: Value field to "Net Book Value" (for clarity)

#### User Experience
```
User clicks on existing asset in list
Asset Details Dialog opens showing:
✅ Expiry Date: 2029-11-06
✅ Useful Life: 4 years
✅ Depreciation Method: Declining Balance
✅ Accumulated Depreciation: ₦109,414.67 (already lost this value)
✅ Net Book Value: ₦140,585.33 (current worth)
```

## Implementation Details

### Asset Dialog Changes
**File**: `app/gui/dialogs/asset_dialog.py`
- Line 114: Changed from `accumulatedDepreciationInput` to `annualDepreciationInput`
- Lines 445, 476: Updated to set Annual Depreciation instead of Accumulated

**File**: `app/gui/ui/asset_dialog.ui`
- Row 11: Label changed to "Annual Depreciation (₦):"
- Row 11: Widget name changed to `annualDepreciationInput`
- Removed: Net Book Value field (row 12)
- Updated: Row numbers for subsequent fields

### Asset Details Changes
**File**: `app/gui/dialogs/asset_details.py`
- Lines 49-50: Added expiry_date display
- Lines 52-58: Added useful_life, depreciation_method, accumulated_depreciation displays
- Lines 97-102: Updated QR code payload to include depreciation fields

**File**: `app/gui/ui/asset_details.ui`
- Row 6: Changed label from "Exp. Date:" to "Expiry Date:"
- Added rows 7-10: Useful Life, Depreciation Method, Accumulated Depreciation, Net Book Value
- Updated description rows from 8-9 to 11-12

## Key Benefits

✅ **Better User Experience**
- Add dialog focuses on entry: Annual Depreciation shows expected yearly cost
- Details dialog shows complete financial picture

✅ **Logical Separation**
- New assets: Show Annual Depreciation (relevant)
- Existing assets: Show Accumulated Depreciation (history)

✅ **Complete Information**
- Details now include expiry_date
- All depreciation context visible
- QR code includes full financial details

## Testing

### Test Case 1: Add New Asset
1. Click "Add Asset"
2. Fill in values: Cost ₦250,000, Useful Life 4 years
3. Select Depreciation Method
4. Verify: Annual Depreciation shows (e.g., ₦109,414.67)

### Test Case 2: View Asset Details
1. Click on asset in list
2. Asset Details opens
3. Verify displays:
   - Expiry Date: YYYY-MM-DD
   - Accumulated Depreciation: ₦X,XXX.XX
   - Net Book Value: ₦X,XXX.XX

## Compilation Status

✅ Both modules import successfully
✅ No syntax errors
✅ Ready for testing