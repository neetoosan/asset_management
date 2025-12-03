# PyInstaller Build Guide - Asset Management System

## Overview

This guide explains how to build a standalone Windows executable (.exe) for the Asset Management System using PyInstaller.

## Project Structure Analysis

```
asset_management_system/
├── app/                          # Main application package
│   ├── main.py                   # Entry point
│   ├── core/                     # Core functionality
│   │   ├── models.py             # Database models
│   │   ├── database.py           # Database configuration
│   │   └── config.py             # Application configuration
│   ├── gui/                      # GUI components (PySide6)
│   │   ├── main_window.py        # Main window
│   │   ├── dialogs/              # Dialog windows
│   │   ├── views/                # View components
│   │   └── ui/                   # UI definition files
│   ├── services/                 # Business logic services
│   ├── static/                   # Static assets (CSS, images)
│   │   ├── css/                  # QSS theme files
│   │   ├── images/               # Images and icons
│   │   └── images/splash/        # Splash screen images
│   ├── api/                      # FastAPI endpoints
│   └── utils/                    # Utility functions
├── AssetManagement.spec          # PyInstaller spec file
├── build_exe.bat                 # Build script
└── requirements.txt              # Python dependencies
```

## Key Dependencies

### GUI Framework
- **PySide6** - Qt6 bindings for Python (primary UI framework)

### Database
- **SQLAlchemy** - ORM framework
- **psycopg2** - PostgreSQL adapter

### Security
- **cryptography** - Encryption library
- **passlib** - Password hashing
- **python-jose** - JWT tokens

### Additional
- **qrcode** - QR code generation
- **PIL/Pillow** - Image processing
- **matplotlib** - Charts
- **numpy** - Numerical computing

## Build Process

### Prerequisites

1. **Python 3.11+** installed
2. **Virtual environment** (.Rhv folder exists)
3. **All dependencies** installed via pip
4. **PyInstaller** installed

### Step 1: Verify Dependencies

```bash
# Activate virtual environment
.Rhv\Scripts\activate.bat

# Verify PyInstaller is installed
pip show pyinstaller

# If not installed, install it
pip install pyinstaller
```

### Step 2: Build the EXE

**Option A: Using the Batch Script**
```bash
# Simply run the build script
build_exe.bat
```

**Option B: Using PyInstaller Directly**
```bash
pyinstaller AssetManagement.spec
```

### Step 3: Output

Build generates:
- **dist/AssetManagement.exe** - Main executable
- **build/** - Temporary build artifacts (can be deleted)

## Configuration (.env File)

Create a `.env` file in the same directory as the executable:

```env
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/asset_management

# Optional: Application Settings
DEBUG=true
ADMIN_TOKEN=your-admin-token-here
```

## Debug Version Features (Current Build)

The spec file is configured for **debug testing**:

```python
debug=True              # Debug mode enabled
console=True           # Console window visible
upx=True               # UPX compression enabled
```

### Advantages
✅ Console shows all debug output and errors
✅ Easier to troubleshoot issues  
✅ Full error tracebacks displayed
✅ Ideal for testing and development

## Production Build (When Ready)

To create a production version, modify `AssetManagement.spec`:

```python
debug=False            # Disable debug mode
console=False          # Hide console window
upx=True               # Keep UPX compression
```

Then rebuild:
```bash
pyinstaller AssetManagement.spec
```

Expected size: ~130 MB (release) vs ~200 MB (debug)

## First Run Setup

When running the executable for the first time:

1. **Database Initialization**
   ```
   Database initialized successfully
   ```

2. **Role and Permission Setup**
   - Admin role created
   - All permissions granted

3. **Welcome Screen Appears**
   - User logs in or registers

## Distribution Checklist

Before sending to company for testing:

- [ ] Built with `build_exe.bat` or `pyinstaller AssetManagement.spec`
- [ ] `.env` file created with DATABASE_URL
- [ ] PostgreSQL database accessible
- [ ] All dependencies included
- [ ] Tested on Windows 10/11
- [ ] Console output verified (debug mode)

## Success Indicators

Successful build shows:
```
Built successfully
dist/AssetManagement.exe created
```

File size: 150-200 MB (debug)

Ready for distribution! ✓