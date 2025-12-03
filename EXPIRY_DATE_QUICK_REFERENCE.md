# Expiry Date - Quick Reference Card

## The Basics (60 seconds)

| Question | Answer |
|----------|--------|
| **What is expiry date?** | When an asset's useful life ends |
| **How is it calculated?** | `Expiry Date = Acquisition Date + (Useful Life × 365 days)` |
| **When is it calculated?** | When asset is created/edited AND every Dec 31st |
| **Does it change?** | YES - Every December 31st, useful_life reduces by 1 year |
| **Can I edit it manually?** | NO - It's auto-calculated from acquisition_date + useful_life |

---

## Three Key Formulas

### 1. Initial Calculation (Asset Creation)
```
expiry_date = acquisition_date + (useful_life × 365 days)
```

### 2. Year-End Recalculation (December 31st)
```
REDUCE: useful_life = useful_life - 1
RECALCULATE: expiry_date = acquisition_date + (useful_life × 365 days)
```

### 3. Color Status Display
```
IF expiry_date < today
    color = RED (expired)
ELSE IF expiry_date < today + 30 days
    color = YELLOW (expiring soon)
ELSE
    color = GREEN (valid)
```

---

## Example

```
Asset: Server-001
Acquired: 2024-01-15
Useful Life: 5 years
Depreciation: 10% yearly

Initial Expiry:
  2024-01-15 + (5 × 365) = 2029-01-15

Dec 31, 2024 - Year-End Update:
  Useful Life: 5 - 1 = 4 years
  New Expiry: 2024-01-15 + (4 × 365) = 2028-01-15
  
Dec 31, 2025 - Year-End Update:
  Useful Life: 4 - 1 = 3 years
  New Expiry: 2024-01-15 + (3 × 365) = 2027-01-15
```

---

## Where to Find Code

| What | Where |
|-----|-------|
| **Initial calc** | `app/gui/dialogs/asset_dialog.py:422-439` |
| **Save calc** | `app/gui/dialogs/asset_dialog.py:575-578` |
| **Year-end update** | `app/services/year_end_service.py:30-154` |
| **Display status** | `app/gui/views/asset_table_view.py:204-217` |
| **Database field** | `app/core/models.py:230` |

---

## Year-End Processing

**When**: December 31st at midnight (UTC)
**Triggers**: Automatically via YearEndService
**What happens**:
1. ✅ Useful life reduced by 1
2. ✅ Expiry date recalculated
3. ✅ Annual depreciation applied
4. ✅ Net book value updated
5. ✅ Audit trail logged

---

## Status Colors

🟢 **GREEN**
- More than 30 days until expiry
- Asset is valid
- No action needed

🟡 **YELLOW**
- Less than 30 days until expiry
- Asset expiring soon
- Consider planning replacement

🔴 **RED**
- Expiry date has passed
- Asset is expired
- May need retirement/disposal

---

## Related Fields

| Field | Effect on Expiry |
|-------|------------------|
| `acquisition_date` | Changes expiry (base calculation) |
| `useful_life` | Changes expiry (duration factor) |
| `depreciation_percentage` | Doesn't affect expiry date, only depreciation amount |
| `depreciation_method` | Doesn't affect expiry date |

---

## Edge Cases

### Asset expires today
```
Expiry: 2024-11-12
Today: 2024-11-12
Status: RED (expired)
Display: Red text
```

### Asset fully depreciated
```
Useful Life: 0 years
Expiry: Set to today
Status: RED (expired)
Next update: Stays expired
```

### Negative useful life
```
Useful Life: -2 years (overdue)
Expiry: Today
Status: RED (expired)
Note: Should retire asset
```

---

## Key Points to Remember

✅ **DO**:
- Set useful_life when creating asset
- Check asset status via color codes
- Run year-end processing on Dec 31st
- Review expired assets for retirement

❌ **DON'T**:
- Manually edit expiry_date (it's calculated)
- Expect expiry_date to stay same (updates Dec 31st)
- Forget to set depreciation percentage
- Ignore YELLOW status (expiring soon)

---

## FAQ

**Q: Can I change the expiry date directly?**
A: No, it's auto-calculated. Change acquisition_date or useful_life instead.

**Q: What happens on Dec 31st?**
A: System reduces useful_life by 1 and recalculates expiry_date automatically.

**Q: When does depreciation apply?**
A: Based on depreciation_percentage (not expiry_date). Applied each Dec 31st.

**Q: Can I disable year-end processing?**
A: It's automatic on Dec 31st. Can manually trigger via YearEndService.manually_trigger_year_end().

**Q: What if I create an asset on Dec 31st?**
A: It gets created with initial expiry date, then immediately processed in year-end (expiry reduced by 1 year).

---

## Quick Calculation

**How many years until asset expires?**
```
years_remaining = (expiry_date - today) / 365
```

**Is asset expiring soon?**
```
IF (expiry_date - today) < 30 days → YES (YELLOW)
```

**Is asset expired?**
```
IF expiry_date < today → YES (RED)
```

---

## Timeline Example

```
2024-01-15: Asset created
            Useful Life: 5 years
            Expiry: 2029-01-15 (GREEN)

2024-12-30: Before year-end
            Useful Life: 5 years (still)
            Expiry: 2029-01-15 (GREEN)

2024-12-31: YEAR-END PROCESSING
            Useful Life: 4 years (✓ reduced)
            Expiry: 2028-01-15 (✓ updated)

2025-12-31: YEAR-END PROCESSING
            Useful Life: 3 years (✓ reduced)
            Expiry: 2027-01-15 (✓ updated)

2028-12-30: Before final year-end
            Useful Life: 1 year (still)
            Expiry: 2029-01-15 (GREEN)

2028-12-31: FINAL YEAR-END
            Useful Life: 0 years (✓ fully depreciated)
            Expiry: 2028-12-31 (✓ today)
            Status: RED (EXPIRED)
```

---

## Files Created

📄 **EXPIRY_DATE_LOGIC.md** - Complete detailed guide
📄 **EXPIRY_DATE_WORKFLOW.md** - Visual flowcharts and diagrams
📄 **EXPIRY_DATE_QUICK_REFERENCE.md** - This quick reference (you are here)
