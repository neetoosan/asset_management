#!/usr/bin/env python
"""
Test script to verify that expiry_date is properly loaded and displayed in the asset table view.

This script:
1. Fetches assets from the database using AssetService
2. Converts them to the format expected by the table view (like main_window does)
3. Verifies that 'expiry_date' key is present in the asset_data
4. Checks that the expiry_date is properly formatted as YYYY-MM-DD
"""

from datetime import datetime, timedelta
from app.services.asset_service import AssetService
from app.core.database import get_db, init_db
from app.core.models import Asset
from app.core.config import Config

# Initialize database
try:
    config = Config()
    init_db(config.DATABASE_URL)
except Exception as e:
    print(f"Warning: Database init failed: {e}")
    pass

def test_expiry_date_in_service():
    """Test that AssetService returns expiry_date in _asset_to_dict"""
    print("\n" + "="*70)
    print("TEST 1: Check AssetService._asset_to_dict includes expiry_date")
    print("="*70)
    
    try:
        with get_db() as session:
            asset = session.query(Asset).first()
            if not asset:
                print("❌ No assets found in database")
                return False
            
            service = AssetService()
            asset_dict = service._asset_to_dict(asset)
            
            if 'expiry_date' in asset_dict:
                print(f"✅ 'expiry_date' key found in asset dict")
                print(f"   Asset: {asset_dict.get('name')}")
                print(f"   Expiry Date: {asset_dict.get('expiry_date')}")
                return True
            else:
                print(f"❌ 'expiry_date' key NOT found in asset dict")
                print(f"   Available keys: {list(asset_dict.keys())}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_expiry_date_in_asset_data_dict():
    """Test that asset_data dict (from main_window) contains expiry_date"""
    print("\n" + "="*70)
    print("TEST 2: Check main_window asset_data dict format")
    print("="*70)
    
    try:
        service = AssetService()
        assets = service.get_all_assets()
        
        if not assets:
            print("❌ No assets returned from get_all_assets()")
            return False
        
        asset = assets[0]
        print(f"✅ Retrieved {len(assets)} assets from database")
        
        # Simulate what main_window.load_assets_for_category does for dict assets
        if isinstance(asset, dict):
            acq = asset.get('acquisition_date')
            date_registered = ''
            if acq:
                try:
                    if isinstance(acq, str):
                        date_registered = datetime.fromisoformat(acq).strftime('%Y-%m-%d')
                    elif isinstance(acq, datetime):
                        date_registered = acq.strftime('%Y-%m-%d')
                except Exception:
                    pass
            
            asset_data = {
                'id': asset.get('id'),
                'asset_id': asset.get('asset_id'),
                'name': asset.get('name'),
                'expiry_date': asset.get('expiry_date'),  # This should be populated
                'date_registered': date_registered,
                'value': float(asset.get('total_cost', 0)),
                'status': asset.get('status') if asset.get('status') else 'Unknown'
            }
            
            if asset_data['expiry_date']:
                print(f"✅ 'expiry_date' is present and has value: {asset_data['expiry_date']}")
                return True
            else:
                print(f"❌ 'expiry_date' is None or empty")
                return False
        else:
            # ORM object
            expiry = getattr(asset, 'expiry_date', None)
            if expiry:
                expiry_str = expiry.strftime('%Y-%m-%d') if hasattr(expiry, 'strftime') else str(expiry)
                print(f"✅ ORM object has expiry_date: {expiry_str}")
                return True
            else:
                print(f"❌ ORM object has no expiry_date (None)")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_expiry_date_format():
    """Test that expiry_date is in YYYY-MM-DD format"""
    print("\n" + "="*70)
    print("TEST 3: Check expiry_date format (should be YYYY-MM-DD)")
    print("="*70)
    
    try:
        service = AssetService()
        assets = service.get_all_assets()
        
        if not assets:
            print("❌ No assets found")
            return False
        
        success_count = 0
        error_count = 0
        
        for asset in assets[:10]:  # Check first 10 assets
            if isinstance(asset, dict):
                expiry = asset.get('expiry_date')
            else:
                expiry = getattr(asset, 'expiry_date', None)
                if expiry and hasattr(expiry, 'strftime'):
                    expiry = expiry.strftime('%Y-%m-%d')
            
            if expiry:
                try:
                    # Try to parse as YYYY-MM-DD
                    parsed = datetime.strptime(str(expiry), '%Y-%m-%d')
                    print(f"✅ {asset.get('asset_id') if isinstance(asset, dict) else asset.asset_id}: {expiry} (valid)")
                    success_count += 1
                except ValueError:
                    print(f"❌ {asset.get('asset_id') if isinstance(asset, dict) else asset.asset_id}: {expiry} (invalid format)")
                    error_count += 1
            else:
                print(f"⚠️  {asset.get('asset_id') if isinstance(asset, dict) else asset.asset_id}: No expiry_date")
        
        if error_count == 0 and success_count > 0:
            print(f"\n✅ All {success_count} dates are in correct YYYY-MM-DD format")
            return True
        else:
            print(f"\n❌ Found {error_count} format errors out of {success_count + error_count} dates")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("EXPIRY DATE DISPLAY TEST SUITE")
    print("="*70)
    
    results = []
    
    results.append(("ServiceDict Format", test_expiry_date_in_service()))
    results.append(("Asset Data Dict", test_expiry_date_in_asset_data_dict()))
    results.append(("Date Format", test_expiry_date_format()))
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - Expiry date should display in asset table!")
    else:
        print(f"\n❌ {total - passed} test(s) failed - Check the issues above")
