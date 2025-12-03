# Expiry Date Logic - Complete Guide

## Overview
The expiry date represents when an asset's useful life ends. It's calculated and updated through two main mechanisms:
1. **Initial Calculation** - When the asset is created or edited
2. **Year-End Adjustment** - Every December 31st, the system recalculates based on remaining useful life

---

## 1. Initial Expiry Date Calculation

### When Does It Happen?
- When creating a NEW asset
- When EDITING an existing asset
- When the **Acquisition Date** or **Useful Life** changes

### The Formula

```
Expiry Date = Acquisition Date + (Useful Life × 365 days)
```

### Example

**Scenario**: You acquire an asset on January 15, 2024, with a useful life of 5 years

```
Acquisition Date: 2024-01-15
Useful Life: 5 years
Expiry Date: 2024-01-15 + (5 × 365 days)
          = 2024-01-15 + 1,825 days
          = 2029-01-15
```

### Code Location
- **File**: `app/gui/dialogs/asset_dialog.py`
- **Method**: `calculate_expiry_date()` (lines 422-439)
- **Also in**: `get_data()` method (lines 575-578)

```python
acquisition_date = self.ui.acquisitionDateEdit.date().toPython()
useful_life = self.ui.usefulLifeSpinBox.value()
expiry_date = acquisition_date + timedelta(days=useful_life * 365)
```

### How It's Triggered

The expiry date recalculates automatically when:
1. User changes **Acquisition Date** - triggers `calculate_expiry_date()`
2. User changes **Useful Life (Years)** - triggers `calculate_expiry_date()`
3. User saves the asset - calculates in `get_data()` before saving

---

## 2. Year-End Expiry Date Update (December 31st)

### When Does It Happen?
**Every December 31st at midnight**, the system automatically processes all active assets and updates their expiry dates.

### The Process (Year-End Service)

**File**: `app/services/year_end_service.py`

#### Step 1: Check if Today is December 31st
```python
def is_year_end(self, target_date: datetime = None) -> bool:
    check_date = target_date or datetime.utcnow()
    return check_date.month == 12 and check_date.day == 31
```

#### Step 2: For Each Active Asset, Apply These Changes

1. **Reduce Useful Life by 1 year**
   ```python
   asset.useful_life -= 1
   ```

2. **Recalculate Expiry Date**
   ```python
   # Using NEW remaining useful life
   new_expiry = asset.acquisition_date + timedelta(days=asset.useful_life * 365)
   asset.expiry_date = new_expiry
   ```

3. **Apply Annual Depreciation** (based on depreciation_percentage)
   ```python
   annual_depreciation = asset.total_cost * (asset.depreciation_percentage / 100.0)
   asset.accumulated_depreciation += annual_depreciation
   ```

4. **Update Net Book Value**
   ```python
   asset.net_book_value = asset.total_cost - asset.accumulated_depreciation
   ```

### Year-End Example

**Scenario**: An asset acquired on 2024-01-15 with original useful life of 5 years

**Before Year-End (December 30, 2024)**:
```
Useful Life: 5 years
Expiry Date: 2029-01-15
Accumulated Depreciation: ₦0
```

**After Year-End (December 31, 2024 - after processing)**:
```
Useful Life: 4 years (reduced by 1)
Expiry Date: 2028-01-15 (recalculated)
Accumulated Depreciation: ₦100,000 (if depreciation_percentage is 10% of ₦1M)
Net Book Value: ₦900,000
```

**After Next Year-End (December 31, 2025)**:
```
Useful Life: 3 years (reduced by 1 more)
Expiry Date: 2027-01-15 (recalculated again)
Accumulated Depreciation: ₦200,000 (adds another year's depreciation)
Net Book Value: ₦800,000
```

---

## 3. Expiry Date Status Indicators

### How It's Displayed in Asset Table View

The system uses color-coding to show asset status:

**File**: `app/gui/views/asset_table_view.py` (lines 204-217)

```python
expiry_item = QTableWidgetItem(str(expiry) if expiry else '')

if expiry:
    try:
        exp_dt = datetime.strptime(str(expiry), '%Y-%m-%d')
        today = datetime.now()
        
        if exp_dt < today:
            expiry_item.setForeground(QColor('#F44336'))  # RED - Expired
        elif exp_dt < today + timedelta(days=30):
            expiry_item.setForeground(QColor('#FFC107'))  # YELLOW - Expiring Soon
        else:
            expiry_item.setForeground(QColor('#4CAF50'))  # GREEN - Valid
    except:
        pass
```

### Color Legend:
- 🟢 **GREEN** - Expiry date is more than 30 days away (Valid)
- 🟡 **YELLOW** - Expiry date is within 30 days (Expiring Soon)
- 🔴 **RED** - Expiry date has passed (Expired)

---

## 4. Fully Depreciated Assets

### When Useful Life Reaches Zero

If an asset's useful life becomes 0 or less during year-end processing:

```python
elif asset.useful_life and asset.useful_life <= 0:
    # Asset is fully depreciated
    asset.expiry_date = today  # Set to today's date
```

**What happens**:
- Expiry date is set to TODAY (the processing date)
- The asset is considered fully depreciated
- Accumulated depreciation stops increasing
- Net book value reaches salvage value

---

## 5. Database Storage

### Asset Model
**File**: `app/core/models.py` (line 230)

```python
expiry_date = Column(Date)  # Calculated as acquisition_date + useful_life
```

### Database Persistence
- Expiry date is **stored in the database** as a DATE field
- Recalculated on Dec 31st each year
- Automatically updated when useful_life decreases
- Displayed in Asset Details and asset tables

---

## 6. Key Scenarios

### Scenario A: New Asset Created
**Input**:
- Acquisition Date: 2024-11-12
- Useful Life: 3 years

**Calculation**:
```
Expiry = 2024-11-12 + (3 × 365) = 2027-11-12
```

**Result**: Asset expires on November 12, 2027

---

### Scenario B: Asset Near Expiration
**Current**: November 1, 2024
**Asset**: Expires December 15, 2024

**Status**: 🟡 YELLOW - Expiring Soon (within 30 days)

**What happens on Dec 31, 2024?**
```
Before:  Useful Life = 1 year, Expiry = 2025-11-12
After:   Useful Life = 0 years, Expiry = 2024-12-31 (today)
Result:  Asset is now EXPIRED (shown in RED)
```

---

### Scenario C: Asset Already Past Useful Life
**Scenario**: Asset acquired 10 years ago with 5-year useful life

**Current Status**: 🔴 RED - Expired

**On Dec 31st Year-End**:
- Useful Life: -5 years → becomes -6 years (reduced by 1)
- Expiry Date: Set to today (2024-12-31)
- The asset remains expired

---

## 7. Audit Trail

All year-end updates are logged:

**File**: `app/services/year_end_service.py` (lines 107-115)

```python
self.audit_service.log_action(
    action='YEAR_END_DEPRECIATION',
    table_name='assets',
    record_id=str(asset.id),
    description=f'Year-end depreciation update for asset {asset.asset_id}',
    old_values=str(old_values),
    new_values=str(new_values)
)
```

**What's tracked**:
- Old useful_life → New useful_life
- Old expiry_date → New expiry_date
- Old accumulated_depreciation → New accumulated_depreciation
- Old net_book_value → New net_book_value
- Depreciation amount applied

---

## 8. Relationship with Depreciation Percentage

The expiry date and depreciation percentage work together:

1. **Expiry Date** = How long the asset will last (useful life)
2. **Depreciation Percentage** = How much value it loses per year

### Example:
```
Asset Cost: ₦1,000,000
Useful Life: 5 years (Expiry: 2029-01-15)
Depreciation Percentage: 10% per year

Year 1 (Dec 31, 2024):
  - Expiry moves to: 2028-01-15 (4 years remaining)
  - Annual Depreciation: ₦100,000
  - New Net Book Value: ₦900,000

Year 2 (Dec 31, 2025):
  - Expiry moves to: 2027-01-15 (3 years remaining)
  - Annual Depreciation: ₦100,000
  - New Net Book Value: ₦800,000
```

---

## 9. API/Service Methods

### In Asset Service (`asset_service.py`):
- `get_asset_by_id()` - Returns asset with current expiry_date
- `_asset_to_dict()` - Includes expiry_date in dictionary (line 1021)

### In Year-End Service (`year_end_service.py`):
- `is_year_end()` - Checks if today is Dec 31
- `process_year_end_depreciation()` - Applies all updates
- `calculate_new_expiry_date()` - Calculates expiry given useful life
- `get_asset_year_end_summary()` - Shows what will be updated
- `manually_trigger_year_end()` - For testing/admin purposes

---

## 10. Important Notes

### Calculation Note:
- Uses **365 days per year** (not accounting for leap years precisely)
- This is acceptable for accounting purposes
- Date arithmetic handles leap years correctly at the database level

### Timezone Note:
- Year-end processing checks `datetime.utcnow()`
- Runs in UTC time
- Consider your server timezone if scheduling automated processes

### Edge Cases:
- **Useful Life = 0**: Asset is fully depreciated, expiry_date = today
- **Negative Useful Life**: Asset is overdue, expiry_date = today, net_book_value = 0
- **No Acquisition Date**: Expiry cannot be calculated, stays NULL
- **Leap Years**: Handled automatically by Python's timedelta

---

## Summary Table

| Aspect | Details |
|--------|---------|
| **Initial Expiry** | Acquisition Date + (Useful Life × 365 days) |
| **Annual Update** | December 31st - Useful Life reduced by 1, Expiry recalculated |
| **Color Coding** | RED (expired), YELLOW (< 30 days), GREEN (valid) |
| **Database** | Stored as DATE field in assets table |
| **Auditing** | All changes logged via audit_service |
| **Related Field** | depreciation_percentage (controls depreciation amount) |
| **Service** | YearEndService handles automatic updates |

