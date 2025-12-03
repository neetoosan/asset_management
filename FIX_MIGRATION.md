# 🔧 Quick Fix: Missing expiry_date Column

## Problem
```
Error: column assets.expiry_date does not exist
```

The code was updated to use `expiry_date`, but your PostgreSQL database doesn't have this column yet.

## Solution

### Option 1: Automated Migration (Recommended) ⭐

Run the migration script we created:

```bash
# From the project root directory
python migration_add_expiry_date.py
```

This script will:
1. ✅ Check if column exists (won't fail if already there)
2. ✅ Add the `expiry_date` column to your assets table
3. ✅ Populate existing assets with calculated expiry dates
4. ✅ Show you the results

**Expected output:**
```
🔄 Starting migration: Adding expiry_date column to assets table...
----------------------------------------------------------------------
📝 Adding expiry_date column to assets table...
✅ Column added successfully!

📋 Populating expiry_date for existing assets...
   Found X assets without expiry_date
   Calculating and updating...
✅ Updated X assets with calculated expiry dates!

----------------------------------------------------------------------
✅ Migration completed successfully!

You can now start the application:
   python -m app.main
```

### Option 2: Manual Migration (If script fails)

Connect to your PostgreSQL database and run:

```sql
-- Add the column
ALTER TABLE assets ADD COLUMN expiry_date DATE DEFAULT NULL;

-- Populate existing assets with calculated expiry dates
UPDATE assets 
SET expiry_date = acquisition_date + (useful_life || ' years')::interval
WHERE acquisition_date IS NOT NULL 
AND useful_life IS NOT NULL 
AND expiry_date IS NULL;

-- Verify the update
SELECT asset_id, acquisition_date, useful_life, expiry_date 
FROM assets 
WHERE acquisition_date IS NOT NULL 
LIMIT 5;
```

**Using psql command line:**
```bash
psql -U your_user -d your_database -c "ALTER TABLE assets ADD COLUMN expiry_date DATE DEFAULT NULL;"
psql -U your_user -d your_database -c "UPDATE assets SET expiry_date = acquisition_date + (useful_life || ' years')::interval WHERE acquisition_date IS NOT NULL AND useful_life IS NOT NULL AND expiry_date IS NULL;"
```

### Option 3: Using pgAdmin (GUI)

1. Open pgAdmin
2. Connect to your database
3. Navigate to: Tables → assets
4. Right-click → View/Edit Data → Tools → Query Tool
5. Paste and run the SQL from Option 2

## After Migration

Once the column is added:

1. ✅ **Stop the application** (if running)
2. ✅ **Run the migration** (Option 1, 2, or 3)
3. ✅ **Start the application** again:
   ```bash
   python -m app.main
   ```

## Verification

Check that the migration worked:

```sql
-- Should show the new column
\d assets

-- Or check specific columns:
SELECT asset_id, acquisition_date, useful_life, expiry_date 
FROM assets 
WHERE acquisition_date IS NOT NULL 
LIMIT 5;
```

You should see `expiry_date` populated with dates like: `2024-11-07` (for assets with acquisition_date and useful_life)

## Troubleshooting

### "Column already exists" error
This is fine - it means the column is already there. Just start your application.

### "Transaction is aborted" error
This happens after the first error. Just rerun the migration script - it will handle cleanup.

### "Permission denied" error
Your database user doesn't have ALTER TABLE permissions. Contact your DBA or use a superuser account.

### Still getting the error after migration?
1. Verify the column was created: `\d assets` (in psql)
2. Restart your Python application completely
3. Check that you're connected to the right database

## What the Migration Does

1. **Checks** if `expiry_date` column exists
2. **Adds** the column with DATE type (nullable)
3. **Populates** all existing assets with: `acquisition_date + (useful_life years)`
4. **Commits** all changes

For example:
- Asset acquired: 2022-01-01, useful_life: 5 years
- → expiry_date becomes: 2027-01-01

## Next Steps

After successful migration:

1. ✅ Run: `python -m app.main`
2. ✅ Create a new asset in the UI
3. ✅ Verify the expiry_date is automatically calculated
4. ✅ Edit an asset and confirm depreciation values look correct

That's it! You're done. 🎉
