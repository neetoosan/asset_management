# Settings Screen - Quick Fix Guide

## What to Do Next (In Order of Priority)

### 🔴 CRITICAL - Fix Now (30 minutes)
**Issue:** Settings still use old "expiry_alerts" terminology

**Fix:**
1. In `setting_screen.py` line 45, change:
   ```python
   'expiry_alerts': True  →  'depreciation_alerts': True
   ```

2. In `setting_screen.py` line 90, change:
   ```python
   self.ui.expiryAlertsCheckBox.toggled.connect  →  self.ui.depreciation_alerts_checkbox.toggled.connect
   ```

3. Update UI file `setting_screen.ui`:
   - Find "Expiry Alerts" label
   - Change to "Depreciation Alerts" or "End of Useful Life Alerts"

4. Test: Save settings, reload app, verify "Depreciation Alerts" saves/loads

---

### 🟠 HIGH PRIORITY - Add Depreciation Fields to Import (1-2 hours)

**What:** Data import doesn't handle depreciation fields

**Add to `setting_screen.py` around line 552:**
```python
'useful_life': col_lookup(['useful life', 'useful_life', 'years', 'lifespan']),
'depreciation_method': col_lookup(['depreciation method', 'depreciation_method', 'method']),
'depreciation_percentage': col_lookup(['depreciation %', 'depreciation_percentage', 'dep %']),
```

**Add to `setting_screen.py` around line 600 (field type handling):**
```python
elif field == 'useful_life':
    try:
        asset_data[field] = int(float(val_str))
    except (ValueError, AttributeError):
        pass

elif field == 'depreciation_percentage':
    try:
        asset_data[field] = float(val_str.replace('%', ''))
    except (ValueError, AttributeError):
        pass

elif field == 'depreciation_method':
    asset_data[field] = val_str
```

**Test:** Import CSV with useful_life, depreciation_percentage, depreciation_method columns

---

### 🟡 MEDIUM PRIORITY - Implement Features or Remove (2-3 hours each)

Choose one action for each:

#### A) Email Notifications
**Current State:** UI exists but doesn't actually send emails
- **Option 1:** Fully implement SMTP settings + email sending → 4-6 hours
- **Option 2:** Remove feature from settings, mark as "Coming Soon" → 30 min

#### B) Language Support
**Current State:** English only works
- **Option 1:** Add Spanish/French/German translation files → 3-4 hours
- **Option 2:** Remove language dropdown, keep English-only → 30 min

#### C) Date Format
**Current State:** Setting saved but not applied to app
- **Option 1:** Apply format to asset table, details, reports → 3-4 hours
- **Option 2:** Remove setting, use system locale → 30 min

---

### 🟢 LOW PRIORITY - Nice-to-Have (Later Sprints)

These are good to have but not critical:
- Admin settings for depreciation policies
- Settings import/export (backup/restore)
- Alert system integration
- Theme customization
- Backup/restore database

---

## One-Command Implementation Strategy

**Quick Path (30 min - 2 hours):**
1. ✅ Fix "expiry_alerts" terminology (30 min)
2. ✅ Add depreciation field mappings (1-2 hours)
3. ✅ Verify import/export works with new fields

**Result:** Settings screen properly aligned with new depreciation terminology + import works correctly

**Extended Path (6-8 hours):**
- Above + 
- Decide on email (implement or remove)
- Decide on language (implement or remove)
- Decide on date format (implement or remove)

---

## Files to Modify

| File | Changes | Lines |
|------|---------|-------|
| `setting_screen.py` | Rename expiry_alerts, add depreciation mappings, add field handlers | 45, 90, 552-570, 600-615 |
| `setting_screen.ui` | Update label "Expiry Alerts" → "Depreciation Alerts" | Search for "Expiry" |
| `setting_screen_ui.py` | Update widget names (auto-generated from UI) | Auto |

---

## Success Criteria

✅ "Depreciation Alerts" displays instead of "Expiry Alerts"  
✅ Import CSV/Excel with useful_life column  
✅ Import CSV/Excel with depreciation_percentage column  
✅ Import CSV/Excel with depreciation_method column  
✅ Settings persist after app restart  
✅ No errors in console  

---

## Recommended Approach

**Do TODAY:**
1. Fix critical "expiry_alerts" bug (makes settings consistent with new terminology)
2. Add depreciation field mappings (enables proper asset import)

**Do NEXT SPRINT:**
1. Choose/implement email feature OR remove it
2. Choose/simplify language support
3. Choose/implement date formatting

**RESULT:** Professional, complete settings screen aligned with system architecture
