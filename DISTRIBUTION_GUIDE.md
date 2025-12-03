# Distribution and Testing Guide

## For Company Testing (Debug Version)

This guide explains how to distribute and test the Asset Management System EXE with companies.

## Build Information

- **Executable**: AssetManagement.exe
- **Size**: ~200 MB (debug version with console)
- **Type**: Standalone - no installation required
- **Python**: Bundled - no Python installation needed on target
- **Debug Mode**: Enabled - console shows all output

## Distribution Package Contents

When delivering to a company, include:

```
AssetManagement/
├── AssetManagement.exe          # Main executable
├── README.txt                   # Quick start guide
├── .env.example                 # Configuration template
├── DATABASE_SETUP.md            # Database setup instructions
└── TROUBLESHOOTING.md           # Common issues and solutions
```

## Step 1: Prepare Distribution Files

### Create README.txt
```
Asset Management System - Debug Version
========================================

Quick Start:
1. Create a .env file with your database URL
2. Run AssetManagement.exe
3. Log in with admin credentials (setup on first run)

Requirements:
- Windows 10 or Windows 11
- PostgreSQL database (local or remote)
- Internet connection for database access

For detailed instructions, see DATABASE_SETUP.md
```

### Create .env.example
```
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/asset_management

# Optional Settings
DEBUG=true
ADMIN_TOKEN=your-admin-token-here
```

### Create DATABASE_SETUP.md
```
# Database Setup Instructions

## Prerequisites
- PostgreSQL server installed and running
- Database server accessible from your machine
- Database credentials (username/password)

## Setup Steps

1. Create a new database:
   ```sql
   CREATE DATABASE asset_management;
   ```

2. Create a database user:
   ```sql
   CREATE USER asset_user WITH PASSWORD 'your_password';
   ALTER ROLE asset_user SET client_encoding TO 'utf8';
   ALTER ROLE asset_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE asset_user SET default_transaction_deferrable TO on;
   ALTER ROLE asset_user SET timezone TO 'UTC';
   ```

3. Grant privileges:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE asset_management TO asset_user;
   ```

4. Create .env file in same folder as AssetManagement.exe:
   ```
   DATABASE_URL=postgresql://asset_user:your_password@localhost:5432/asset_management
   ```

5. Run AssetManagement.exe

## First Run

The application will automatically:
- Create all required tables
- Initialize admin role
- Set up permissions
- Display login screen

Default Admin Account:
- Username: admin
- Password: admin (change on first login)

## Verification

Check console output for:
```
Database initialized successfully
```

If you see this message, setup is complete!
```
```

## Pre-Delivery Checklist

Before sending to company:

- [ ] Build completed successfully with `build_exe.bat` or `build_exe.ps1`
- [ ] dist/AssetManagement.exe exists and is ~200 MB
- [ ] All distribution files created
- [ ] Tested on Windows 10 or 11
- [ ] Created sample .env file with test database URL
- [ ] Console output verified (shows debug messages)
- [ ] Database initialization tested
- [ ] Login functionality verified

## Testing Procedure

### Phase 1: Basic Startup
1. Run AssetManagement.exe
2. Verify console window appears
3. Check console for "Database initialized successfully"
4. Welcome screen should appear
5. No errors in console output

### Phase 2: Database Connection
1. Click "Login" button
2. Verify login form appears
3. Enter test credentials (admin/admin)
4. Verify main window opens
5. Check console for successful database queries

### Phase 3: Core Features
1. **Asset Management**
   - Add new asset with depreciation values
   - Verify annual depreciation calculation
   - Check depreciation methods work
   - Edit existing asset
   - Delete asset

2. **Asset Details**
   - Click on asset in list
   - Verify details dialog shows:
     - Expiry date
     - Accumulated depreciation
     - Net book value
     - All financial information

3. **Asset Table**
   - Verify expiry_date column displays
   - Check color coding (Red/Yellow/Green)
   - Try search and filter

4. **QR Code Generation**
   - Open asset details
   - Click QR button
   - Save and verify QR code includes asset data

### Phase 4: Error Handling
1. Disconnect database and try to use application
2. Verify error messages appear in console
3. Check error handling is graceful
4. Application should not crash

## Company Feedback Template

Provide feedback on:

```
Feedback Form - Asset Management System Debug Build
===================================================

1. Installation & Startup
   ☐ Easy to install
   ☐ Application started without issues
   ☐ Console output clear and helpful
   Issue: _______________

2. Performance
   ☐ Application responsive
   ☐ No crashes or freezes
   ☐ Database queries fast
   Issue: _______________

3. Depreciation Calculations
   ☐ Annual depreciation calculated correctly
   ☐ All 4 depreciation methods work
   ☐ Accumulated depreciation displays correctly
   Issue: _______________

4. Asset Management
   ☐ Easy to add assets
   ☐ Easy to edit assets
   ☐ Asset deletion works
   ☐ Search and filtering work
   Issue: _______________

5. UI/UX
   ☐ Interface intuitive
   ☐ Dialogs clear and organized
   ☐ Visual feedback clear
   ☐ No UI glitches
   Issue: _______________

6. Overall Assessment
   Rating (1-5): ___
   Ready for Production: ☐ Yes  ☐ No  ☐ With Changes

Additional Comments:
_________________________________
```

## Support During Testing

### Common Issues

**Issue**: "Database connection failed"
**Solution**: Check DATABASE_URL in .env file, verify PostgreSQL is running

**Issue**: "No module named 'X'"
**Solution**: Check console for missing imports, this shouldn't happen in release build

**Issue**: "Console freezes"
**Solution**: This is debug mode - console shows all database activity. Normal behavior.

**Issue**: "Depreciation values not updating"
**Solution**: Try changing depreciation method dropdown, values update automatically

### Debug Console Tips

- All SQL queries logged
- All errors printed to console
- Copy console output for bug reports
- Press Ctrl+C to close application gracefully

## Post-Testing Actions

1. **Collect Feedback**
   - Review feedback forms
   - Note any issues or suggestions
   - Prioritize fixes based on severity

2. **Bug Fixes**
   - Create GitHub issues for reported bugs
   - Prioritize critical issues
   - Test fixes with company feedback

3. **Production Release**
   - Disable debug mode
   - Remove console window
   - Rebuild with `debug=False, console=False`
   - Conduct internal QA testing
   - Deploy production version

## Version Tracking

Current Build:
- **Version**: Debug 1.0
- **Release Date**: [Date]
- **Build Command**: `pyinstaller AssetManagement.spec`
- **File**: dist/AssetManagement.exe
- **Size**: ~200 MB
- **Status**: Ready for company testing

Next Release:
- Production version (no console, optimized)
- Size: ~130 MB
- Status: After company feedback integration