# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for Asset Management System
Debug Version for Company Testing

This spec file creates a standalone Windows executable for the Asset Management System.
The application includes:
- PySide6 GUI framework
- PostgreSQL/SQLAlchemy database support
- Real-time depreciation calculations
- Asset tracking with QR codes
- User authentication and role-based access control

Build Command:
    pyinstaller AssetManagement.spec

Output:
    dist/AssetManagement.exe (single file executable)
"""

import sys
from pathlib import Path
import os

# Get project root - use spec file location
spec_dir = os.path.dirname(os.path.abspath(SPEC))
project_root = Path(spec_dir).absolute()

# Block cipher for advanced obfuscation (optional)
block_cipher = None

# ============================================================================
# Analysis Configuration
# ============================================================================
a = Analysis(
    ['app/main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Static files (CSS, images, QSS themes)
        (str(project_root / 'app' / 'static'), 'app/static'),
        # UI files (if not compiled to Python)
        (str(project_root / 'app' / 'gui' / 'ui'), 'app/gui/ui'),
    ],
    hiddenimports=[
        # Core PySide6 modules
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtSql',
        
        # Database and ORM
        'sqlalchemy',
        'sqlalchemy.orm',
        'sqlalchemy.pool',
        'psycopg2',
        
        # Security and cryptography
        'cryptography',
        'passlib',
        'passlib.context',
        'passlib.handlers',
        'passlib.handlers.bcrypt',
        'passlib.handlers.pbkdf2',
        'cryptography.fernet',
        'cryptography.hazmat',
        'cryptography.hazmat.backends',
        'cryptography.hazmat.primitives',
        
        # API and web
        'fastapi',
        'uvicorn',
        'pydantic',
        
        # Additional utilities
        'dotenv',
        'keyring',
        'qrcode',
        'PIL',
        'matplotlib',
        'numpy',
        
        # Application modules
        'app',
        'app.core',
        'app.core.models',
        'app.core.database',
        'app.core.config',
        'app.services',
        'app.gui',
        'app.gui.dialogs',
        'app.gui.views',
        'app.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        # Exclude unnecessary modules to reduce file size
        'pytest',
        'setuptools',
        'pip',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ============================================================================
# PYZ (Python Archive) Configuration
# ============================================================================
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

# ============================================================================
# EXE Configuration
# ============================================================================
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AssetManagement',
    debug=True,  # Debug mode: set to False for production
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console for debug output (set to False for production)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Optional: add icon path here, e.g., 'app/static/images/logo.ico'
)

# ============================================================================
# COLLECT Configuration (Alternative for multi-file build)
# ============================================================================
# Uncomment this section if you want to create a directory instead of a single file
# This is useful for debugging as it allows modification of Python files after build
# To use: change onefile=True to onefile=False in EXE, and uncomment below

# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='AssetManagement'
# )

# ============================================================================
# Build Notes
# ============================================================================
# 
# DEBUG VERSION FEATURES:
# - Console window enabled for debug output
# - Debug mode active (slower but more detailed errors)
# - All error messages printed to console
# - UPX compression disabled for faster builds
#
# TO BUILD:
#   pyinstaller AssetManagement.spec
#
# OUTPUT:
#   dist/AssetManagement.exe (single executable)
#
# FIRST RUN SETUP:
# When the exe first runs, it will:
# 1. Load configuration from environment (.env file)
# 2. Connect to PostgreSQL database
# 3. Initialize database with default admin role
# 4. Create necessary tables if they don't exist
#
# REQUIREMENTS FOR DISTRIBUTION:
# - .env file with DATABASE_URL set correctly
# - PostgreSQL database server accessible
# - All required Python packages installed on target system
#
# SIZE OPTIMIZATION:
# - Current size: ~150-200 MB (debug with console)
# - For production: set console=False, debug=False (~130 MB)
# - Use UPX for additional compression (upx=True, already enabled)
#
# TROUBLESHOOTING:
# - If imports fail, check hiddenimports list
# - If assets missing, verify datas paths are correct
# - If database connection fails, check DATABASE_URL in .env
# - For more verbose output, keep debug=True
#
# ============================================================================
