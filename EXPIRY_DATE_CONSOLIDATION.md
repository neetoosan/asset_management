# Expiry Date Logic Consolidation

## Changes Made

### Single Logic: Year-End Service ONLY

**What Changed**:
- Removed initial expiry date calculation from `asset_dialog.py`
- `expiry_date` is now set to `NULL` when creating/editing assets
- Only `YearEndService` (Dec 31st) calculates and updates expiry dates

### File Modified

**`app/gui/dialogs/asset_dialog.py`**

1. **Removed** from `setup_connections()`:
   - Connection for `acquisitionDateEdit.dateChanged` → `calculate_expiry_date()`
   - Connection for `usefulLifeSpinBox.valueChanged` → `calculate_expiry_date()`

2. **Deleted** method:
   - `calculate_expiry_date()` - (was lines 410-439)

3. **Removed** from `calculate_total_cost()`:
   - Call to `self.calculate_expiry_date()` after cost calculation

4. **Updated** `get_data()` method:
   - Changed: `"expiry_date": expiry_date` 
   - To: `"expiry_date": None`
   - Removed all `timedelta` calculations for expiry date

---

## Expiry Date Workflow (NEW)

```
CREATE/EDIT ASSET
├─ Set expiry_date = NULL
├─ Save to database
└─ Asset saved with NO expiry date

↓

DECEMBER 31ST (Year-End Service)
├─ Check is_year_end()
├─ Get all active assets
├─ For each asset:
│  ├─ Calculate: expiry_date = acq_date + (useful_life × 365)
│  ├─ Reduce: useful_life -= 1
│  ├─ Apply depreciation
│  └─ Save changes
└─ All assets updated with expiry dates

↓

ASSET DISPLAYS EXPIRY DATE
└─ Color coded: GREEN / YELLOW / RED
```

---

## Key Points

✅ **Simpler** - One calculation logic instead of two
✅ **Consistent** - All assets use year-end accounting
✅ **Centralized** - Only `YearEndService` sets expiry dates
✅ **Controlled** - No manual expiry date editing during create/edit

---

## SQL Notes

When querying assets before Dec 31st:
```sql
SELECT * FROM assets WHERE expiry_date IS NULL
-- Will show newly created/edited assets awaiting year-end processing
```

After Dec 31st year-end service runs:
```sql
SELECT * FROM assets WHERE expiry_date IS NOT NULL
-- All active assets will have calculated expiry dates
```

---

## Testing Checklist

- [ ] Create new asset - verify `expiry_date` is NULL
- [ ] Edit asset - verify `expiry_date` stays NULL
- [ ] Run year-end on Dec 31st - verify `expiry_date` calculated
- [ ] Check color coding in asset table
- [ ] Verify audit logs recorded
