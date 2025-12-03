# -*- coding: utf-8 -*-
"""
Diagnostic script to check why imports are failing
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*80)
print("IMPORT FAILURE DIAGNOSIS")
print("="*80 + "\n")

try:
    # Check database connection
    print("[1] Checking database connection...")
    from app.core.database import get_db, init_db
    from app.core.config import Config
    
    config = Config()
    print(f"    Database URL: {config.DATABASE_URL[:50]}...")
    init_db(config.DATABASE_URL)
    print("    ✓ Database initialized")
    
    # Check CRUD settings
    print("\n[2] Checking CRUD_RESTRICTIONS settings...")
    from app.services.settings_service import SettingsService
    
    ss = SettingsService()
    can_create = ss.can_create_asset()
    can_edit = ss.can_edit_asset()
    print(f"    Can create asset: {can_create}")
    print(f"    Can edit asset: {can_edit}")
    
    if not can_create or not can_edit:
        print("    ❌ CRUD restrictions are blocking imports!")
        print("    → Need to enable these in Settings")
    else:
        print("    ✓ CRUD operations enabled")
    
    # Check if we can create a test asset
    print("\n[3] Attempting to create a test asset...")
    from app.services.asset_service import AssetService
    
    asset_service = AssetService()
    test_asset = {
        'asset_id': 'TEST-DIAG-001',
        'name': 'Diagnostic Test Asset',
        'total_cost': 1000.0,
    }
    
    result = asset_service.create_asset(test_asset)
    print(f"    Result: {result['message']}")
    
    if result['success']:
        print("    ✓ Test asset created successfully")
        print(f"    Asset ID: {result['asset'].get('asset_id')}")
        
        # Try to delete it
        print("\n[4] Cleaning up test asset...")
        asset_id = result['asset'].get('id')
        if asset_id:
            with get_db() as session:
                from app.core.models import Asset
                asset_obj = session.query(Asset).filter(Asset.id == asset_id).first()
                if asset_obj:
                    session.delete(asset_obj)
                    print("    ✓ Test asset deleted")
    else:
        print(f"    ❌ Failed: {result['message']}")
        print("    → This is the issue blocking imports")
    
    print("\n" + "="*80)
    if result['success']:
        print("DIAGNOSIS: System is working correctly")
        print("The issue may be with the Excel data format or column mappings")
    else:
        print(f"DIAGNOSIS: {result['message']}")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"❌ Diagnostic error: {e}")
    import traceback
    traceback.print_exc()
