# Expiry Date Display Fix - Asset Table

## Issue
The expiry_date was not displaying in the asset_table_view.py despite the database having the column.

## Root Cause
The code was attempting to create 11 columns and add an actions column, which didn't match the UI definition. The UI file (asset_table_view.ui) already had exactly 10 columns with column 7 reserved for "Exp. Date".

## Solution

### 1. UI File Structure (asset_table_view.ui)
The UI already defines 10 columns (0-9):
```
0: Asset ID
1: Name
2: Model Number
3: Serial Number
4: Department
5: Category
6: Date Registered
7: Exp. Date        ← Expiry date display column
8: Value
9: Status
```

### 2. Fixed asset_table_view.py Changes

**File:** `app/gui/views/asset_table_view.py`

#### setup_table() method (lines 35-87)
- ✅ Removed incorrect column count logic that tried to create 11 columns
- ✅ Now correctly sets widths for 10 columns only
- ✅ No longer attempts to create "Actions" column

#### load_assets() method (lines 171-237)
- ✅ Properly extracts `expiry_date` from database:
  - For dicts: `asset.get('expiry_date', '')`
  - For ORM objects: `getattr(asset, 'expiry_date', None)`
- ✅ Correctly populates 10 columns (0-9):
  - Column 0: Asset ID
  - Column 1: Name
  - Column 2: Model
  - Column 3: Serial
  - Column 4: Department
  - Column 5: Category
  - Column 6: Date Registered
  - **Column 7: Expiry Date** (with color coding)
  - Column 8: Value
  - Column 9: Status
- ✅ Color coding for expiry dates:
  - 🔴 **RED (#F44336):** Expired
  - 🟡 **YELLOW (#FFC107):** Expiring soon (< 30 days)
  - 🟢 **GREEN (#4CAF50):** Valid (> 30 days)
- ✅ Removed incorrect "Actions" column (column 10)

### 3. Key Differences from Previous Implementation

**BEFORE (Incorrect):**
```python
# Tried to create 11 columns
if self.ui.assetTable.columnCount() != 11:
    self.ui.assetTable.setColumnCount(11)
    # Added custom headers including "Actions"
    
# Tried to populate column 10 with actions
self.ui.assetTable.setItem(row, 10, QTableWidgetItem('---'))
```

**AFTER (Correct):**
```python
# Works with existing 10 columns from UI
# Only sets column widths, doesn't modify column count

# Properly populates column 7 with expiry_date
expiry_item = QTableWidgetItem(str(expiry) if expiry else '')
if expiry:
    # Apply color coding
    exp_dt = datetime.strptime(str(expiry), '%Y-%m-%d')
    # Color based on expiration status
self.ui.assetTable.setItem(row, 7, expiry_item)
```

## Implementation Details

### Column 7 Population Logic
```python
# Extract expiry_date
expiry = asset.get('expiry_date', '')  # for dicts
expiry = getattr(asset, 'expiry_date', None)  # for ORM objects

# Format as string and create item
expiry_item = QTableWidgetItem(str(expiry) if expiry else '')

# Apply color coding based on expiration
if expiry:
    exp_dt = datetime.strptime(str(expiry), '%Y-%m-%d')
    today = datetime.now()
    
    if exp_dt < today:
        expiry_item.setForeground(QColor('#F44336'))  # Red - EXPIRED
    elif exp_dt < today + timedelta(days=30):
        expiry_item.setForeground(QColor('#FFC107'))  # Yellow - EXPIRING SOON
    else:
        expiry_item.setForeground(QColor('#4CAF50'))  # Green - VALID

# Set in table at column 7
self.ui.assetTable.setItem(row, 7, expiry_item)
```

## Testing Checklist

- [ ] Launch application
- [ ] Navigate to asset list view
- [ ] Verify "Exp. Date" column displays dates
- [ ] Check color coding:
  - [ ] Expired dates show RED
  - [ ] Expiring soon dates show YELLOW
  - [ ] Valid dates show GREEN
- [ ] Verify Actions column is NOT displayed
- [ ] Check that all 10 columns align with UI file
- [ ] Test with multiple assets

## Files Modified

| File | Changes |
|------|---------|
| `app/gui/views/asset_table_view.py` | Fixed setup_table() and load_assets() to use 10 columns correctly |

## Notes

- Always use the .ui files as the source of truth for UI structure
- The UI file defines exactly what columns exist and their order
- Python code should adapt to the UI, not modify it programmatically
- When making GUI changes, edit the .ui file and regenerate, don't modify generated code

## Result

✅ Expiry date now displays in the asset table with proper color coding
✅ No unnecessary "Actions" column
✅ All 10 columns properly aligned with UI definition
✅ Dates color-coded based on expiration status
