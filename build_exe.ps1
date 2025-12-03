# PowerShell Build Script for Asset Management System
# This script builds a debug executable using PyInstaller

# Enable error handling
$ErrorActionPreference = "Stop"

# Color functions for output
function Write-Header {
    param([string]$Message)
    Write-Host "`n========================================================================" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "========================================================================`n" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Yellow
}

# Main build process
try {
    Write-Header "Asset Management System - EXE Build Script"
    
    # Check if virtual environment exists
    Write-Info "Checking for virtual environment..."
    if (-not (Test-Path ".Rhv\Scripts\Activate.ps1")) {
        Write-Error "Virtual environment not found at .Rhv\Scripts\Activate.ps1"
        Write-Info "Please create the virtual environment first"
        exit 1
    }
    Write-Success "Virtual environment found"
    
    # Activate virtual environment
    Write-Info "Activating virtual environment..."
    & ".Rhv\Scripts\Activate.ps1"
    Write-Success "Virtual environment activated"
    
    # Check if PyInstaller is installed
    Write-Info "Checking for PyInstaller..."
    $pyinstallerCheck = python -m pip show pyinstaller 2>$null
    if (-not $pyinstallerCheck) {
        Write-Info "PyInstaller not found. Installing..."
        python -m pip install pyinstaller
        Write-Success "PyInstaller installed"
    } else {
        Write-Success "PyInstaller found"
    }
    
    # Clean previous builds
    Write-Header "Cleaning Previous Builds"
    $dirsToClean = @("build", "dist", "__pycache__")
    foreach ($dir in $dirsToClean) {
        if (Test-Path $dir) {
            Write-Info "Removing $dir..."
            Remove-Item -Path $dir -Recurse -Force
            Write-Success "Removed $dir"
        }
    }
    
    # Run PyInstaller
    Write-Header "Running PyInstaller"
    Write-Info "Building with AssetManagement.spec..."
    Write-Info "This may take 2-5 minutes depending on system performance..."
    Write-Host ""
    
    pyinstaller AssetManagement.spec
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "PyInstaller build failed with exit code $LASTEXITCODE"
        exit 1
    }
    
    # Verify build output
    Write-Header "Verifying Build Output"
    if (Test-Path "dist\AssetManagement.exe") {
        Write-Success "Executable created successfully"
        $exeSize = (Get-Item "dist\AssetManagement.exe").Length / 1MB
        Write-Success "File size: $([Math]::Round($exeSize, 2)) MB"
    } else {
        Write-Error "Executable not found at dist\AssetManagement.exe"
        exit 1
    }
    
    # Display next steps
    Write-Header "Build Complete - Next Steps"
    Write-Host ""
    Write-Host "1. Create a .env file in the dist folder:" -ForegroundColor White
    Write-Host "   dist\.env" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Configure database connection:" -ForegroundColor White
    Write-Host "   DATABASE_URL=postgresql://user:password@localhost/asset_management" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Run the executable:" -ForegroundColor White
    Write-Host "   dist\AssetManagement.exe" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Built executable location:" -ForegroundColor White
    Write-Host "   $(Resolve-Path 'dist\AssetManagement.exe')" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Success "Build process completed successfully!"
    
} catch {
    Write-Error "Build failed: $($_.Exception.Message)"
    exit 1
}
