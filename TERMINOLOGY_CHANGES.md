# UI Terminology Changes - Professional Depreciation Language

## Overview
Updated Asset Management System UI to use professionally accurate depreciation terminology. The system now reflects accounting best practices where "expired" assets are replaced with "depreciated" assets, and recognizes that not all assets depreciate (e.g., land).

## Changes Made

### 1. Asset Table View UI (`asset_table_view.ui` & `asset_table_view_ui.py`)

**Before:**
- Summary Frame: "Expiring Assets" 
- Summary Frame: "Expired Assets"

**After:**
- Summary Frame: "Depreciatable Assets (within 30 days)"
  - Represents assets approaching their end of useful life within next 30 days
  - Widget names: `depreciatableAssetsFrame`, `depreciatableAssetsLabel`, `depreciatableAssetsValue`
  
- Summary Frame: "Fully Depreciated Assets"
  - Represents assets that have reached their end of useful life
  - Widget names: `depreciatedAssetsFrame`, `depreciatedAssetsLabel`, `depreciatedAssetsValue`

### 2. Asset Table View Logic (`asset_table_view.py`)

**Updated:**
- Variable names: `expiring_count` → `depreciatable_count`
- Variable names: `expired_count` → `depreciated_count`
- Variable name: `expiring_soon` → `depreciation_window`
- Comments updated to reflect "end of life" concept instead of "expiry"
- Color coding maintained:
  - 🔴 RED = Fully Depreciated (end of useful life reached)
  - 🟡 YELLOW = Depreciatable (within 30 days of end of useful life)
  - 🟢 GREEN = Active (useful life remaining)

### 3. Asset Details Dialog (`asset_details.py`)

**Updated:**
- Label context: Display "End of Useful Life" date instead of expiry date
- Remaining life message: "End of useful life reached" instead of "Expired"
- More accurate terminology for asset status display

### 4. Expiry Calculator Service (`expiry_calculator.py`)

**Documentation updated:**
- Class docstring: "Calculate asset end of useful life dates"
- Method docstring: "Calculate end of useful life date using Dec 31 depreciation logic"
- File header: "End of Useful Life Calculator using Dec 31 Depreciation Logic"

## Key Concepts

### Depreciatable Assets
- Assets within 30 days of reaching their end of useful life
- Typically displayed in YELLOW
- Requires attention but still has some remaining useful life

### Fully Depreciated Assets  
- Assets that have reached their end of useful life
- All useful life has been consumed (0 years remaining)
- Typically displayed in RED
- May still be in use but no longer depreciating

### Non-Depreciating Assets
- Assets like land that don't depreciate
- Can be excluded from depreciation calculations by not having a useful_life value
- System is designed to handle these transparently

## Field Names (Unchanged)
The following technical field names remain unchanged for database compatibility:
- `expiry_date` - Still used in database; represents calculated end of useful life date
- `useful_life` - Still used for years of useful life

## Accounting Alignment
These changes align the UI with standard accounting practices:
- Depreciation is a systematic reduction in asset value over time
- "Expired" is imprecise; assets don't necessarily expire—they depreciate
- Not all assets depreciate (land, improvements with indefinite life)
- Terminology now reflects the concept of "remaining useful life"

## Files Modified
1. `/app/gui/ui/asset_table_view.ui` - UI definition file
2. `/app/gui/ui/asset_table_view_ui.py` - Generated UI Python code
3. `/app/gui/views/asset_table_view.py` - Asset table view logic
4. `/app/gui/dialogs/asset_details.py` - Asset details display
5. `/app/services/expiry_calculator.py` - Calculator service documentation

## Testing Checklist
- ✅ Asset table displays "Depreciatable Assets (within 30 days)" count
- ✅ Asset table displays "Fully Depreciated Assets" count
- ✅ Color coding works correctly (RED/YELLOW/GREEN)
- ✅ Asset details shows "End of Useful Life" terminology
- ✅ QR codes still generate correctly with expiry_date
- ✅ Database operations unaffected (same field names)
- ✅ Depreciation calculations unaffected

## Notes
- Land and other non-depreciating assets are naturally handled by the system (no useful_life = no depreciation)
- All existing database data remains compatible
- The change is purely UI/UX terminology, not functional
