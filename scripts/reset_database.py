#!/usr/bin/env python3
"""
Database reset script for Asset Management System
Clears all existing data and reinitializes with sample data
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db, init_db, Base
from app.core.config import Config
from sqlalchemy import text


def drop_all_tables():
    """Drop all tables from the database"""
    print("[*] Dropping all existing tables...")
    config = Config()
    
    try:
        # Initialize database connection first
        init_db(config.DATABASE_URL)
        
        with get_db() as session:
            # Get all table names
            inspector_query = text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            """)
            
            result = session.execute(inspector_query)
            tables = [row[0] for row in result]
            
            if tables:
                # Drop all tables
                for table in tables:
                    session.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                    print(f"  [OK] Dropped table: {table}")
                
                session.commit()
                print("[SUCCESS] All tables dropped successfully")
            else:
                print("  [INFO] No tables found to drop")
                
    except Exception as e:
        print(f"[ERROR] Error dropping tables: {e}")
        raise


def reinitialize_database():
    """Reinitialize database schema and sample data"""
    print("\n[*] Reinitializing database...")
    
    # Import the init_database function
    from scripts.init_database import (
        initialize_database,
        create_default_roles_and_permissions,
        create_sample_users,
        create_asset_categories,
        create_sample_assets,
        initialize_system_settings,
        create_sample_audit_log,
        print_summary
    )
    
    try:
        # Initialize database tables
        initialize_database()
        
        # Create roles and permissions
        create_default_roles_and_permissions()
        
        # Create sample users
        create_sample_users()
        
        # Create asset categories
        create_asset_categories()
        
        # Create sample assets (with new expiry calculation)
        create_sample_assets()
        
        # Initialize system settings
        initialize_system_settings()
        
        # Create audit log
        create_sample_audit_log()
        
        # Print summary
        print_summary()
        
    except Exception as e:
        print(f"[ERROR] Error during reinitialization: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Main reset function"""
    print("[*] Asset Management System - Database Reset")
    print("=" * 60)
    print("\n[WARNING] This will delete ALL data in the database!")
    print("This includes all users, assets, categories, and other records.\n")
    
    # Ask for confirmation
    confirm = input("Are you sure you want to reset the database? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("\n[CANCELLED] Reset cancelled.")
        sys.exit(0)
    
    try:
        # Drop all tables
        drop_all_tables()
        
        # Reinitialize with new data
        reinitialize_database()
        
        print("\n" + "=" * 60)
        print("[SUCCESS] DATABASE RESET COMPLETE!")
        print("=" * 60)
        print("\n[INFO] Database has been reset and reinitialized with new sample data.")
        print("All sample assets now use the Dec 31 depreciation logic for expiry dates.")
        
    except Exception as e:
        print(f"\n[FAILED] RESET FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
