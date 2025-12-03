# Import Failure - Troubleshooting Guide

## Issue
All 72 rows from the Excel file failed to import with the same error message.

## Root Cause
**CRUD Restrictions are disabled in the database settings**

The system has a security setting that controls whether users can create/edit/delete assets. When `allow_asset_creation` is set to `false` (or missing from the database), all import attempts will fail because the import process calls `asset_service.create_asset()` which checks `settings_service.can_create_asset()`.

## Solution

### Option 1: Use the Fix Script (Recommended)
Run the provided fix script to automatically enable CRUD restrictions:

```bash
python fix_crud_restrictions.py
```

This script will:
1. Initialize the database connection
2. Check for `CRUD_RESTRICTIONS.allow_asset_creation` setting
3. Create or update it to `'true'`
4. Enable `CRUD_RESTRICTIONS.allow_asset_editing` as well

Then restart the application and try the import again.

### Option 2: Manual Database Update
If you have database access, run this SQL directly:

```sql
-- PostgreSQL
INSERT INTO system_configuration (category, key, value, data_type, description, is_system)
VALUES ('CRUD_RESTRICTIONS', 'allow_asset_creation', 'true', 'boolean', 'Allow users to create assets', 'true')
ON CONFLICT (category, key) DO UPDATE SET value = 'true';

-- SQLite
INSERT OR REPLACE INTO system_configuration (category, key, value, data_type, description, is_system)
VALUES ('CRUD_RESTRICTIONS', 'allow_asset_creation', 'true', 'boolean', 'Allow users to create assets', 'true');
```

### Option 3: Via GUI Settings
1. Close the application
2. Reopen the application
3. Navigate to **Settings** → **General** or **Admin** tab (if available)
4. Look for "Allow Asset Creation" or similar setting
5. Enable it
6. Restart application
7. Try import again

## After Enabling

1. **Close the application completely**
2. **Restart the application**
3. Go to **Settings** → **Import** tab
4. Click **Browse**
5. Select `tests/RHV TEST.xlsx`
6. Ensure "First row contains headers" is checked
7. Click **Import Data**

Expected result: 72 assets should import successfully.

## Error Message Explanation

The error message "Asset creation is currently disabled by system settings" comes from:
- **File**: `app/services/asset_service.py`, line 319
- **Function**: `can_create_asset()`
- **Check**: `if not self.settings_service.can_create_asset():`

When this returns `False`, the entire import fails.

## Technical Details

### Database Settings Table
```
system_configuration
├── category: 'CRUD_RESTRICTIONS'
├── key: 'allow_asset_creation'
├── value: 'true' or 'false'
└── data_type: 'boolean'
```

### Related Settings
- `allow_asset_creation` - Controls if assets can be created (needed for imports)
- `allow_asset_editing` - Controls if assets can be edited (may also block imports)
- `allow_asset_deletion` - Controls if assets can be deleted

### Code Flow for Imports
```
import_data()
  ↓
  for each row:
    ↓
    asset_service.create_asset()
      ↓
      asset_service.can_create_asset()
        ↓
        settings_service.can_create_asset()
          ↓
          database lookup: CRUD_RESTRICTIONS.allow_asset_creation
            ↓
            if False → return {success: False, message: "Asset creation is currently disabled..."}
```

## Prevention

To prevent this issue in the future:
1. Ensure database is properly initialized with default settings
2. In database initialization code, create default CRUD restrictions with `value='true'`
3. Provide admin UI to manage these settings

## Additional Notes

- The enhanced logging added to `setting_screen.py` will now print error messages for each failed row
- Check console output when import fails for detailed error messages
- The import preview table will now show all columns including the failed rows
- Export failed rows to CSV for detailed review using the "Yes" button when prompted

## Files Involved

- `app/services/asset_service.py` - `can_create_asset()` method
- `app/services/settings_service.py` - Database settings lookup
- `app/gui/views/setting_screen.py` - Import UI and logic
- `app/core/models.py` - SystemConfiguration model
- `fix_crud_restrictions.py` - Fix script to enable CRUD operations
- `diagnose_import.py` - Diagnostic script (requires app environment)

## Testing the Fix

After enabling CRUD restrictions:

```python
# This should work:
from app.services.asset_service import AssetService
asset_service = AssetService()
result = asset_service.create_asset({
    'asset_id': 'TEST-001',
    'name': 'Test Asset',
    'total_cost': 1000.0
})
print(result['success'])  # Should print: True
```
