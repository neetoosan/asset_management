# Expiry Date Workflow - Visual Guide

## Flowchart 1: Asset Creation/Editing

```
┌─────────────────────────────────────┐
│  User Opens Asset Creation Dialog   │
│  OR Edits Existing Asset            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  User Enters/Modifies:              │
│  - Acquisition Date                 │
│  - Useful Life (Years)              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  System Triggers:                   │
│  calculate_expiry_date()            │
│  (Lines 422-439)                    │
└──────────────┬──────────────────────┘
               │
               ▼
     ┌─────────────────────┐
     │  FORMULA:           │
     │  Expiry Date =      │
     │  Acq Date +         │
     │  Useful Life × 365  │
     └─────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Display Updated Expiry Date        │
│  in Expiry Date Field               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  User Clicks "Save"                 │
└──────────────┬──────────────────────┘
               │
               ▼
        get_data() Method
        (Lines 575-578)
        Recalculates ONE MORE TIME
               │
               ▼
┌─────────────────────────────────────┐
│  Save to Database:                  │
│  - expiry_date column               │
│  - useful_life column               │
│  - acquisition_date column          │
└──────────────┬──────────────────────┘
               │
               ▼
       ✅ Asset Saved
```

---

## Flowchart 2: Year-End Processing (December 31st)

```
┌──────────────────────────────────────────┐
│  System Clock Reaches 12/31 Midnight    │
│  (UTC Time)                              │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  YearEndService.process_year_end_        │
│  depreciation() triggered                │
│  (Lines 30-154)                          │
└────────────────┬─────────────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ is_year_end()?  │
        │ Check: month==12│
        │ & day==31       │
        └────────┬────────┘
                 │
         ┌───────┴────────┐
         │                │
      YES│                │NO
         │                │
         ▼                ▼
    Continue        Return Error
    Processing      "Not Dec 31st"
         │
         ▼
┌──────────────────────────────────────────┐
│  Get All Active Assets From Database:   │
│  - Available                             │
│  - In Use                                │
│  - Under Maintenance                     │
└────────────────┬─────────────────────────┘
                 │
                 ▼
         FOR EACH ASSET:
      ┌────────────────────┐
      │  Step 1: Reduce    │
      │  useful_life -= 1  │
      │                    │
      │  Step 2: Recalculate
      │  expiry_date =     │
      │  acq_date +        │
      │  (new_useful_life  │
      │   × 365 days)      │
      │                    │
      │  Step 3: Apply     │
      │  annual deprec.    │
      │  amount            │
      │                    │
      │  Step 4: Update    │
      │  net_book_value    │
      │                    │
      │  Step 5: Log audit │
      │  trail             │
      └────────────────────┘
                 │
         (Repeat for all assets)
                 │
                 ▼
┌──────────────────────────────────────────┐
│  Commit All Changes to Database          │
│  session.commit()                        │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  Return Summary:                         │
│  - Number of assets processed            │
│  - Details of each asset updated         │
│  - Depreciation amounts applied          │
└────────────────┬─────────────────────────┘
                 │
                 ▼
       ✅ Year-End Processing Complete
```

---

## Example: Year-End Updates Timeline

```
ASSET ACQUIRED: 2024-01-15
USEFUL LIFE: 5 years
DEPRECIATION %: 10%
TOTAL COST: ₦1,000,000

═════════════════════════════════════════════════════════════

DATE: 2024-01-15 (Asset Created)
  Acquisition Date: 2024-01-15
  Useful Life: 5 years
  Expiry Date: 2024-01-15 + (5 × 365) = 2029-01-15
  Accumulated Depreciation: ₦0
  Net Book Value: ₦1,000,000
  Status: 🟢 VALID

═════════════════════════════════════════════════════════════

DATE: 2024-12-30 (Day Before Year-End)
  Useful Life: 5 years (unchanged)
  Expiry Date: 2029-01-15 (unchanged)
  Accumulated Depreciation: ₦0
  Status: 🟢 VALID

═════════════════════════════════════════════════════════════

DATE: 2024-12-31 (YEAR-END PROCESSING)
┌─────────────────────────────────────────────────────────┐
│ BEFORE Processing          │ AFTER Processing           │
├────────────────────────────┼────────────────────────────┤
│ Useful Life: 5 years       │ Useful Life: 4 years ✓     │
│ Expiry: 2029-01-15         │ Expiry: 2028-01-15 ✓       │
│ Accum Deprec: ₦0           │ Accum Deprec: ₦100,000 ✓   │
│ Net Book Value: ₦1,000,000 │ Net Book Value: ₦900,000 ✓ │
└────────────────────────────┴────────────────────────────┘

Processing Steps:
  1. useful_life: 5 - 1 = 4
  2. expiry_date: 2024-01-15 + (4 × 365) = 2028-01-15
  3. annual_depreciation: ₦1,000,000 × 10% = ₦100,000
     accumulated_depreciation: ₦0 + ₦100,000 = ₦100,000
  4. net_book_value: ₦1,000,000 - ₦100,000 = ₦900,000
  5. Audit logged ✓

═════════════════════════════════════════════════════════════

DATE: 2025-12-31 (NEXT YEAR-END)
┌─────────────────────────────────────────────────────────┐
│ BEFORE Processing          │ AFTER Processing           │
├────────────────────────────┼────────────────────────────┤
│ Useful Life: 4 years       │ Useful Life: 3 years ✓     │
│ Expiry: 2028-01-15         │ Expiry: 2027-01-15 ✓       │
│ Accum Deprec: ₦100,000     │ Accum Deprec: ₦200,000 ✓   │
│ Net Book Value: ₦900,000   │ Net Book Value: ₦800,000 ✓ │
└────────────────────────────┴────────────────────────────┘

Processing Steps:
  1. useful_life: 4 - 1 = 3
  2. expiry_date: 2024-01-15 + (3 × 365) = 2027-01-15
  3. annual_depreciation: ₦1,000,000 × 10% = ₦100,000
     accumulated_depreciation: ₦100,000 + ₦100,000 = ₦200,000
  4. net_book_value: ₦1,000,000 - ₦200,000 = ₦800,000
  5. Audit logged ✓

═════════════════════════════════════════════════════════════

[Continues for 3 more years...]

═════════════════════════════════════════════════════════════

DATE: 2028-12-31 (FINAL YEAR-END)
┌─────────────────────────────────────────────────────────┐
│ BEFORE Processing          │ AFTER Processing           │
├────────────────────────────┼────────────────────────────┤
│ Useful Life: 1 year        │ Useful Life: 0 years ✓     │
│ Expiry: 2029-01-15         │ Expiry: 2028-12-31 ✓       │
│ Accum Deprec: ₦400,000     │ Accum Deprec: ₦500,000 ✓   │
│ Net Book Value: ₦600,000   │ Net Book Value: ₦500,000 ✓ │
└────────────────────────────┴────────────────────────────┘

Processing Steps:
  1. useful_life: 1 - 1 = 0
  2. expiry_date: Since useful_life = 0, set to today (2028-12-31)
  3. annual_depreciation: ₦1,000,000 × 10% = ₦100,000
     accumulated_depreciation: ₦400,000 + ₦100,000 = ₦500,000
  4. net_book_value: ₦1,000,000 - ₦500,000 = ₦500,000
  5. Audit logged ✓

═════════════════════════════════════════════════════════════

ASSET IS NOW FULLY DEPRECIATED
Status Changes to: 🔴 EXPIRED (Expiry Date = Today)
Remains at: ₦500,000 net book value (salvage value)
```

---

## Status Display in Asset Table

```
Asset: Server-2024-001
Expiry: 2029-01-15
Today: 2024-11-12

Days Until Expiry: 1520 days
Status: 🟢 GREEN (More than 30 days away)

────────────────────────────────────────

Asset: Server-2024-002
Expiry: 2024-12-15
Today: 2024-11-20

Days Until Expiry: 25 days
Status: 🟡 YELLOW (Within 30 days - Expiring Soon!)

────────────────────────────────────────

Asset: Server-2019-101
Expiry: 2023-06-30
Today: 2024-11-12

Days Since Expiry: 500 days
Status: 🔴 RED (Already Expired)
```

---

## Code Execution Flow

### During Asset Save:

```
User clicks "Save"
        ↓
accept() method called
        ↓
validate() checks
  ├─ Asset ID not empty ✓
  ├─ Description not empty ✓
  ├─ Supplier not empty ✓
  ├─ Location selected ✓
  └─ Depreciation % > 0% ✓
        ↓
save_asset() called
        ↓
get_data() called
  ├─ Calculate acquisition_date
  ├─ Calculate useful_life
  ├─ RECALCULATE expiry_date = acq_date + (useful_life × 365)
  ├─ Prepare other fields
  └─ Return dict with all data
        ↓
asset_service.create_asset(data)
  OR asset_service.update_asset(id, data)
        ↓
Data saved to database
        ↓
Dialog closes ✅
```

### During Year-End (Dec 31st):

```
System Time Check: UTC datetime.now()
        ↓
is_year_end()? (month==12 && day==31)
        ↓ YES
Query active assets
        ↓
FOR EACH asset:
  ├─ Save old values (audit trail)
  ├─ useful_life -= 1
  ├─ IF useful_life > 0:
  │   expiry_date = acq_date + (useful_life × 365)
  │ ELSE:
  │   expiry_date = today
  ├─ annual_depreciation = total_cost × (deprec_percent / 100)
  ├─ accumulated_depreciation += annual_depreciation
  ├─ net_book_value = total_cost - accumulated_depreciation
  ├─ Log audit entry with old/new values
  └─ Add to updated_assets list
        ↓
Commit all changes
        ↓
Return summary ✅
```

---

## Key Decision Points

### Decision 1: When Creating Asset
```
IF (Useful Life provided)
    THEN calculate expiry_date = acq_date + (useful_life × 365)
ELSE
    error("Useful Life is required")
```

### Decision 2: During Year-End Processing
```
IF (today is December 31st)
    IF (useful_life > 0)
        THEN expiry_date = acq_date + ((useful_life - 1) × 365)
    ELSE
        THEN expiry_date = today (fully depreciated)
    THEN apply annual depreciation
ELSE
    skip processing
```

### Decision 3: Display in Table
```
IF (expiry_date < today)
    THEN color = RED (expired)
ELSE IF (expiry_date < today + 30 days)
    THEN color = YELLOW (expiring soon)
ELSE
    THEN color = GREEN (valid)
```

---

## Database Schema

```
Assets Table
┌────────────────────────────────┐
│ Column                 Type    │
├────────────────────────────────┤
│ id                    INTEGER  │ PRIMARY KEY
│ asset_id              STRING   │ (Unique user ID)
│ acquisition_date      DATE     │ (When asset was bought)
│ useful_life           INTEGER  │ (Years the asset lasts)
│ expiry_date           DATE     │ (When asset expires)
│ depreciation_percentage FLOAT  │ (% to depreciate yearly)
│ accumulated_deprec.   FLOAT    │ (Total depreciation)
│ net_book_value        FLOAT    │ (Current value)
│ total_cost            FLOAT    │ (Original cost)
└────────────────────────────────┘

Relationships:
  acquisition_date + (useful_life × 365) = expiry_date
  accumulated_depreciation changes on Dec 31st
  net_book_value = total_cost - accumulated_depreciation
```

---

## Summary

**Expiry date** is calculated as:
- **Initial**: When asset is created → Acquisition Date + (Useful Life × 365 days)
- **Updated**: Every December 31st → Acquisition Date + (New Remaining Useful Life × 365 days)

This works hand-in-hand with **depreciation percentage** which determines how much value the asset loses each year.

