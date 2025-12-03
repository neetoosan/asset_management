# -*- coding: utf-8 -*-
"""
Fix Script: Enable CRUD Restrictions for imports
This script ensures that asset creation is enabled in the database settings
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*80)
print("FIXING CRUD RESTRICTIONS FOR IMPORT")
print("="*80 + "\n")

try:
    from app.core.database import get_db, init_db
    from app.core.config import Config
    from app.core.models import SystemConfiguration
    
    # Initialize database
    config = Config()
    print(f"[1] Initializing database...")
    init_db(config.DATABASE_URL)
    print(f"    ✓ Database initialized")
    
    # Enable CRUD operations
    print(f"\n[2] Enabling CRUD operations...")
    with get_db() as session:
        # Check existing settings
        allow_creation = session.query(SystemConfiguration).filter(
            SystemConfiguration.category == 'CRUD_RESTRICTIONS',
            SystemConfiguration.key == 'allow_asset_creation'
        ).first()
        
        if allow_creation:
            print(f"    Current value: {allow_creation.value}")
            allow_creation.value = 'true'
            print(f"    Updated to: true")
        else:
            print(f"    Setting not found, creating...")
            new_setting = SystemConfiguration(
                category='CRUD_RESTRICTIONS',
                key='allow_asset_creation',
                value='true',
                data_type='boolean',
                description='Allow users to create assets',
                is_system='true'
            )
            session.add(new_setting)
            print(f"    Created setting")
        
        # Also ensure allow_asset_editing is enabled
        allow_editing = session.query(SystemConfiguration).filter(
            SystemConfiguration.category == 'CRUD_RESTRICTIONS',
            SystemConfiguration.key == 'allow_asset_editing'
        ).first()
        
        if allow_editing:
            if allow_editing.value != 'true':
                allow_editing.value = 'true'
                print(f"    Updated allow_asset_editing to: true")
        else:
            new_setting = SystemConfiguration(
                category='CRUD_RESTRICTIONS',
                key='allow_asset_editing',
                value='true',
                data_type='boolean',
                description='Allow users to edit assets',
                is_system='true'
            )
            session.add(new_setting)
            print(f"    Created allow_asset_editing setting")
        
        session.commit()
        print(f"\n✅ CRUD restrictions have been enabled")
        print(f"\nNow try importing again:")
        print(f"1. Close the application completely")
        print(f"2. Restart the application")
        print(f"3. Go to Settings > Import")
        print(f"4. Select tests/RHV TEST.xlsx")
        print(f"5. Click Import Data")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print(f"\nNote: This script must be run from within the application environment")
