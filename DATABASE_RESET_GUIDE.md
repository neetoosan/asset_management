# Database Reset Guide

## Why You Need to Reset

The `init_database.py` script has checks to prevent duplicate data:
- If categories already exist → skips category creation
- If assets already exist → skips asset creation

Since your database already had 7 old sample assets, the new initialization script skipped creating the 44 new sample assets with the updated expiry calculation logic.

## Solution: Use the Reset Script

### Quick Start

```bash
python scripts/reset_database.py
```

### What It Does

1. **Confirms deletion** - Asks for explicit confirmation (type "yes")
2. **Drops all tables** - Removes all existing data from the database
3. **Reinitializes schema** - Creates all database tables fresh
4. **Creates new sample data** including:
   - 5 sample users with different roles
   - 8 asset categories with 33 subcategories
   - 44 sample assets with proper depreciation fields
   - All expiry dates calculated using Dec 31 depreciation logic
   - CRUD restrictions enabled
   - System settings initialized

### Step-by-Step

1. **Open terminal** in your project directory:
   ```bash
   cd C:\Users\HP\Documents\python_projects\asset_management_system
   ```

2. **Run the reset script**:
   ```bash
   python scripts/reset_database.py
   ```

3. **Confirm the reset** when prompted:
   ```
   Are you sure you want to reset the database? (yes/no): yes
   ```

4. **Wait for completion**:
   ```
   ============================================================
   ✅ DATABASE RESET COMPLETE!
   ============================================================
   
   🎉 Database has been reset and reinitialized with new sample data.
   All sample assets now use the Dec 31 depreciation logic for expiry dates.
   ```

5. **Start the application**:
   ```bash
   python app/main.py
   ```

## What You'll Get

After reset, your database will contain:

### Users (5 total)
- Admin: admin@company.com / admin123
- Asset Manager (John Smith)
- HR Manager (Sarah Johnson)
- Operations Supervisor (Mike Davis)
- Viewer (Lisa Chen)

### Assets (44 total)
- **IT Equipment** (10): Computers, servers, network equipment, mobile devices
- **Office Equipment** (6): Printers, copiers, phones, projectors
- **Furniture & Fixtures** (8): Chairs, tables, storage, shelving
- **Vehicles** (6): Cars, vans, trucks, SUVs
- **Categories ready for imports**: Imported Assets, Land and Buildings, Plant and Machinery, Hospital Equipment, Software

### Asset Features

✅ All assets have:
- Proper descriptions
- Correct category assignments
- Depreciation method (random: Straight Line, Declining Balance, etc.)
- Depreciation percentage (5-25% annual)
- Acquisition dates (random within last 3 years)
- **Expiry dates calculated with Dec 31 logic**
- Random status (mostly Available with some In Use/Maintenance)
- Model numbers and serial numbers
- Proper locations and departments

## Troubleshooting

### Error: "Database connection failed"
- Ensure your PostgreSQL database is running
- Check DATABASE_URL in `.env` file
- Verify credentials are correct

### Error: "relation already exists"
- This shouldn't happen with the reset script
- If it does, manually drop the database and recreate it

### The script hangs
- Press Ctrl+C to cancel
- Check if the database is responsive
- Try resetting in smaller steps

## Important Notes

⚠️ **This will delete everything**:
- All user accounts (except you'll need to recreate login)
- All assets and asset history
- All audit logs
- All reports

📝 **After reset**:
- Always use new admin credentials: admin@company.com / admin123
- **Change the password immediately after first login**
- All sample data is fresh and ready for testing

## Files Involved

- `scripts/reset_database.py` - The reset script (new)
- `scripts/init_database.py` - Initialization logic (updated)
- `app/core/database.py` - Database connection
- `app/core/models.py` - Database schema

## Alternative: Manual Database Deletion

If you prefer not to use the script:

### PostgreSQL (via psql)
```sql
-- Connect to PostgreSQL
psql -U your_user -d your_database

-- Drop all tables
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Exit
\q
```

Then run the original init script:
```bash
python scripts/init_database.py
```

## Verification

After reset, verify by starting the app and checking:

1. **Login**: admin@company.com / admin123
2. **View Assets**: Should see 44 sample assets
3. **Check Expiry Dates**: Should be calculated using Dec 31 logic
4. **Check Categories**: Should see all 8 categories with correct subcategories

---

**Need help?** Check the database logs or run the script with verbose output for debugging.
