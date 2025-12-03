# Expiry Date Implementation - Final

## Single Formula Everywhere

**Formula**: `expiry_date = acquisition_date + (useful_life × 365 days)`

---

## Where It's Used

### 1. Asset Creation/Edit
**File**: `app/gui/dialogs/asset_dialog.py`
- Display expiry in UI: `display_expiry_date()` (lines 422-434)
- Save to DB: `get_data()` calculates expiry (lines 574-578)
- Both use SAME year-end formula

### 2. Asset Table View
**File**: `app/gui/views/asset_table_view.py`
- Loads from database (line 174)
- Color-codes: RED (expired) | YELLOW (< 30 days) | GREEN (valid)

### 3. Asset Details
**File**: `app/gui/dialogs/asset_details.py`
- Displays expiry from DB (lines 48-50)
- Included in QR code payload (line 105)

### 4. Year-End Service
**File**: `app/services/year_end_service.py`
- Reduces useful_life by 1 (line 78)
- Recalculates expiry using same formula (line 82)
- Sets to today if fully depreciated (line 86)

---

## Data Flow

```
CREATE ASSET
├─ User enters: acquisition_date, useful_life
├─ System calculates: expiry = acq_date + (useful_life × 365)
├─ Display shows calculated date
└─ Save to DB with calculated expiry

DISPLAY EVERYWHERE
├─ Asset Table: Shows expiry with color coding
├─ Asset Details: Shows expiry as info
├─ QR Code: Includes expiry in JSON
└─ Reports: Includes expiry

DEC 31 YEAR-END
├─ Reduce useful_life: life - 1
├─ Recalculate expiry: acq_date + (new_life × 365)
├─ Update all assets
└─ Next day: All displays show updated expiry
```

---

## Example

```
CREATE: 2024-01-15, Useful Life: 5 years
Expiry: 2024-01-15 + (5 × 365) = 2029-01-15
Saved & Displayed: 2029-01-15 (GREEN)

DEC 31, 2024:
Useful Life: 5 - 1 = 4 years
New Expiry: 2024-01-15 + (4 × 365) = 2028-01-15
Updated & Displayed: 2028-01-15 (GREEN)
```

---

## Status

✅ Created with year-end formula
✅ Saved to database
✅ Displayed in all screens
✅ Updated Dec 31 annually
✅ Shown in QR codes
✅ Color-coded status
