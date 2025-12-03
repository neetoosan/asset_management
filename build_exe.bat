@echo off
REM Asset Management System - PyInstaller Build Script for Windows
REM This script builds a debug executable for company testing

echo.
echo ========================================================================
echo Asset Management System - EXE Build Script
echo ========================================================================
echo.
echo Building debug version with PyInstaller...
echo.

REM Check if virtual environment exists
if not exist .Rhv\Scripts\activate.bat (
    echo ERROR: Virtual environment not found at .Rhv\Scripts\activate.bat
    echo Please create the virtual environment first
    pause
    exit /b 1
)

REM Activate virtual environment
call .Rhv\Scripts\activate.bat

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
)

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

REM Run PyInstaller with spec file
echo.
echo Running PyInstaller with AssetManagement.spec...
echo.
pyinstaller AssetManagement.spec

REM Check if build was successful
if errorlevel 1 (
    echo.
    echo ERROR: PyInstaller build failed!
    echo Check the error messages above for details.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo BUILD SUCCESSFUL!
echo ========================================================================
echo.
echo Output file: dist\AssetManagement.exe
echo.
echo Next steps:
echo 1. Create a .env file in the same directory as AssetManagement.exe
echo 2. Set DATABASE_URL in .env to your PostgreSQL connection string
echo 3. Run AssetManagement.exe
echo.
echo Example .env file:
echo DATABASE_URL=postgresql://username:password@localhost:5432/asset_management
echo.
pause
