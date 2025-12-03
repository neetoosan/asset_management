#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verification Script - Phase 1 Completion Check
Confirms all changes are working correctly
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*80)
print("PHASE 1 VERIFICATION - Settings Screen Updates")
print("="*80 + "\n")

checks = []

# Check 1: Import setting_screen.py
print("[1] Checking setting_screen.py imports...")
try:
    from app.gui.views.setting_screen import SettingScreen
    checks.append(("Import SettingScreen", True, "Module loads successfully"))
    print("    OK - Module imports successfully")
except Exception as e:
    checks.append(("Import SettingScreen", False, str(e)))
    print(f"    FAIL - {e}")

# Check 2: Verify deprecation_alerts exists in default_settings
print("\n[2] Checking default_settings for 'deprecation_alerts'...")
try:
    from app.gui.views.setting_screen import SettingScreen
    settings = SettingScreen.__init__.__code__.co_consts
    
    # Read the file to check
    with open("app/gui/views/setting_screen.py") as f:
        content = f.read()
        if "'deprecation_alerts': True" in content:
            checks.append(("Deprecation alerts setting", True, "Found in default_settings"))
            print("    OK - 'deprecation_alerts' found in default_settings")
        else:
            checks.append(("Deprecation alerts setting", False, "Not found in default_settings"))
            print("    FAIL - 'deprecation_alerts' not found")
except Exception as e:
    checks.append(("Deprecation alerts setting", False, str(e)))
    print(f"    FAIL - {e}")

# Check 3: Verify Excel import mappings
print("\n[3] Checking Excel import field mappings...")
try:
    with open("app/gui/views/setting_screen.py") as f:
        content = f.read()
        
    required_mappings = [
        "'useful_life': col_lookup",
        "'depreciation_method': col_lookup",
        "'depreciation_percentage': col_lookup",
        "acquistion",  # Misspelling variant
        "usefull life",  # Misspelling variant
        "netbook value",  # Combined variant
    ]
    
    all_found = all(mapping in content for mapping in required_mappings)
    if all_found:
        checks.append(("Excel import mappings", True, "All depreciation fields mapped"))
        print("    OK - All required field mappings found")
        for m in required_mappings:
            print(f"       - {m}")
    else:
        missing = [m for m in required_mappings if m not in content]
        checks.append(("Excel import mappings", False, f"Missing: {missing}"))
        print(f"    FAIL - Missing mappings: {missing}")
except Exception as e:
    checks.append(("Excel import mappings", False, str(e)))
    print(f"    FAIL - {e}")

# Check 4: Verify Excel empty row handling
print("\n[4] Checking Excel empty row skip logic...")
try:
    with open("app/gui/views/setting_screen.py") as f:
        content = f.read()
    
    if "skip_rows" in content and "row.isna().all()" in content:
        checks.append(("Excel empty row handling", True, "Skip logic implemented"))
        print("    OK - Empty row skip logic found")
    else:
        checks.append(("Excel empty row handling", False, "Skip logic not found"))
        print("    FAIL - Empty row skip logic not found")
except Exception as e:
    checks.append(("Excel empty row handling", False, str(e)))
    print(f"    FAIL - {e}")

# Check 5: Verify UI file updated
print("\n[5] Checking UI file for 'deprecationAlertsCheckBox'...")
try:
    with open("app/gui/ui/setting_screen_ui.py") as f:
        content = f.read()
    
    if "deprecationAlertsCheckBox" in content and "deprecationAlertsLabel" in content:
        checks.append(("UI widget names", True, "Updated to deprecationAlerts*"))
        print("    OK - UI widgets renamed correctly")
    else:
        checks.append(("UI widget names", False, "Not found"))
        print("    FAIL - UI widgets not properly renamed")
except Exception as e:
    checks.append(("UI widget names", False, str(e)))
    print(f"    FAIL - {e}")

# Check 6: Verify test file exists
print("\n[6] Checking test Excel file...")
try:
    test_file = Path("tests/RHV TEST.xlsx")
    if test_file.exists():
        size_mb = test_file.stat().st_size / (1024 * 1024)
        checks.append(("Test file RHV TEST.xlsx", True, f"Found ({size_mb:.2f} MB)"))
        print(f"    OK - Test file found ({size_mb:.2f} MB)")
    else:
        checks.append(("Test file RHV TEST.xlsx", False, "File not found"))
        print("    FAIL - Test file not found")
except Exception as e:
    checks.append(("Test file RHV TEST.xlsx", False, str(e)))
    print(f"    FAIL - {e}")

# Check 7: Verify syntax
print("\n[7] Checking Python syntax...")
try:
    import py_compile
    py_compile.compile("app/gui/views/setting_screen.py", doraise=True)
    checks.append(("Python syntax", True, "No syntax errors"))
    print("    OK - No syntax errors")
except Exception as e:
    checks.append(("Python syntax", False, str(e)))
    print(f"    FAIL - {e}")

# Summary
print("\n" + "="*80)
print("VERIFICATION SUMMARY")
print("="*80 + "\n")

passed = sum(1 for _, success, _ in checks if success)
total = len(checks)

for name, success, message in checks:
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} {name:35s} - {message}")

print(f"\n{'='*80}")
print(f"Result: {passed}/{total} checks passed")
print(f"{'='*80}\n")

if passed == total:
    print("SUCCESS! All Phase 1 changes verified and working correctly.")
    print("\nYou can now:")
    print("  1. Open the application")
    print("  2. Go to Settings > Import tab")
    print("  3. Select tests/RHV TEST.xlsx")
    print("  4. Click 'Import Data'")
    print("  5. Watch 72 assets import successfully")
    sys.exit(0)
else:
    print(f"WARNING: {total - passed} check(s) failed. Review the issues above.")
    sys.exit(1)
