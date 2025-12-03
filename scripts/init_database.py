#!/usr/bin/env python3
"""
Database initialization script for Asset Management System
Creates all tables, initializes default data, and creates sample records
"""

import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import init_db
from app.core.config import Config
from app.core.models import (
    Base, Asset, AssetCategory, AssetSubCategory, User, Role, Permission, 
    RolePermission, UserRole, PermissionType, AssetStatus, DepreciationMethod,
    SystemConfiguration, AuditLog
)
from app.services.auth_service import AuthService
from app.services.settings_service import SettingsService


def initialize_database():
    """Initialize the database with all tables"""
    print("[*] Initializing database...")
    config = Config()
    init_db(config.DATABASE_URL)
    print("[OK] Database tables created successfully")


def create_default_roles_and_permissions():
    """Create default roles and permissions"""
    print("[*] Creating default roles and permissions...")
    
    from app.core.database import get_db
    
    try:
        with get_db() as session:
            # Create default roles
            default_roles = [
                (UserRole.ADMIN, "System administrator with full access"),
                (UserRole.USER, "Regular user with limited permissions"), 
                (UserRole.VIEWER, "View-only access to system")
            ]
            
            for role_enum, description in default_roles:
                existing_role = session.query(Role).filter(Role.name == role_enum).first()
                if not existing_role:
                    role = Role(name=role_enum, description=description)
                    session.add(role)
                    print(f"  [+] Created role: {role_enum.value}")
            
            # Create default permissions
            for perm_enum in PermissionType:
                existing_perm = session.query(Permission).filter(
                    Permission.name == perm_enum
                ).first()
                if not existing_perm:
                    permission = Permission(
                        name=perm_enum,
                        description=f"Permission to {perm_enum.value.lower()}"
                    )
                    session.add(permission)
                    print(f"  [+] Created permission: {perm_enum.value}")
            
            session.commit()
            session.flush()  # Flush to get ID
            
            # Set up default role-permission mappings
            admin_role = session.query(Role).filter(Role.name == UserRole.ADMIN).first()
            user_role = session.query(Role).filter(Role.name == UserRole.USER).first()
            viewer_role = session.query(Role).filter(Role.name == UserRole.VIEWER).first()
            
            # Admin gets all permissions
            if admin_role:
                for perm_enum in PermissionType:
                    permission = session.query(Permission).filter(
                        Permission.name == perm_enum
                    ).first()
                    if permission:
                        existing_rp = session.query(RolePermission).filter(
                            RolePermission.role_id == admin_role.id,
                            RolePermission.permission_id == permission.id
                        ).first()
                        if not existing_rp:
                            role_perm = RolePermission(
                                role_id=admin_role.id,
                                permission_id=permission.id,
                                granted="true"
                            )
                            session.add(role_perm)
            
            # User gets limited permissions
            if user_role:
                user_permissions = [
                    PermissionType.VIEW_ASSET,
                    PermissionType.CREATE_ASSET,
                    PermissionType.EDIT_ASSET,
                    PermissionType.VIEW_REPORTS
                ]
                for perm_enum in user_permissions:
                    permission = session.query(Permission).filter(
                        Permission.name == perm_enum
                    ).first()
                    if permission:
                        existing_rp = session.query(RolePermission).filter(
                            RolePermission.role_id == user_role.id,
                            RolePermission.permission_id == permission.id
                        ).first()
                        if not existing_rp:
                            role_perm = RolePermission(
                                role_id=user_role.id,
                                permission_id=permission.id,
                                granted="true"
                            )
                            session.add(role_perm)
            
            # Viewer gets view-only permissions
            if viewer_role:
                viewer_permissions = [
                    PermissionType.VIEW_ASSET,
                    PermissionType.VIEW_REPORTS
                ]
                for perm_enum in viewer_permissions:
                    permission = session.query(Permission).filter(
                        Permission.name == perm_enum
                    ).first()
                    if permission:
                        existing_rp = session.query(RolePermission).filter(
                            RolePermission.role_id == viewer_role.id,
                            RolePermission.permission_id == permission.id
                        ).first()
                        if not existing_rp:
                            role_perm = RolePermission(
                                role_id=viewer_role.id,
                                permission_id=permission.id,
                                granted="true"
                            )
                            session.add(role_perm)
            
            session.commit()
            print(" Roles and permissions created successfully")
            
    except Exception as e:
        print(f" Error creating roles and permissions: {e}")
        raise


def create_sample_users():
    """Create sample users including admin user"""
    print(" Creating sample users...")
    
    auth_service = AuthService()
    
    from app.core.database import get_db
    
    try:
        with get_db() as session:
            # Get roles
            admin_role = session.query(Role).filter(Role.name == UserRole.ADMIN).first()
            user_role = session.query(Role).filter(Role.name == UserRole.USER).first()
            viewer_role = session.query(Role).filter(Role.name == UserRole.VIEWER).first()
            
            sample_users = [
                {
                    "name": "System Administrator",
                    "email": "admin@company.com", 
                    "password": "admin123",
                    "department": "IT",
                    "position": "System Administrator",
                    "role": admin_role,
                    "is_active": "Active"
                },
                {
                    "name": "John Smith",
                    "email": "john.smith@company.com",
                    "password": "password123",
                    "department": "Finance",
                    "position": "Asset Manager", 
                    "role": user_role,
                    "is_active": "Active"
                },
                {
                    "name": "Sarah Johnson",
                    "email": "sarah.johnson@company.com",
                    "password": "password123",
                    "department": "HR",
                    "position": "HR Manager",
                    "role": user_role,
                    "is_active": "Active"
                },
                {
                    "name": "Mike Davis",
                    "email": "mike.davis@company.com",
                    "password": "password123",
                    "department": "Operations",
                    "position": "Operations Supervisor",
                    "role": user_role,
                    "is_active": "Active"
                },
                {
                    "name": "Lisa Chen",
                    "email": "lisa.chen@company.com",
                    "password": "password123",
                    "department": "Finance",
                    "position": "Financial Analyst",
                    "role": viewer_role,
                    "is_active": "Active"
                }
            ]
            
            for user_data in sample_users:
                # Check if user already exists
                existing_user = session.query(User).filter(
                    User.email == user_data["email"]
                ).first()
                
                if not existing_user:
                    # Hash password
                    password_hash = auth_service.hash_password(user_data["password"])
                    
                    user = User(
                        name=user_data["name"],
                        email=user_data["email"],
                        password_hash=password_hash,
                        department=user_data["department"],
                        position=user_data["position"],
                        role_id=user_data["role"].id if user_data["role"] else None,
                        is_active=user_data["is_active"]
                    )
                    
                    session.add(user)
                    print(f"   Created user: {user_data['name']} ({user_data['email']})")
            
            session.commit()
            print(" Sample users created successfully")
            
    except Exception as e:
        print(f" Error creating sample users: {e}")
        raise


def create_asset_categories():
    """Create asset categories and subcategories"""
    print(" Creating asset categories...")
    
    from app.core.database import get_db
    
    try:
        with get_db() as session:
            # Skip if categories already exist
            if session.query(AssetCategory).count() > 0:
                print("  ℹ  Categories already exist, skipping...")
                return
            
            categories_data = {
                "Imported Assets": [
                    "Bulk Import", "Excel Import", "CSV Import", "Data Migration"
                ],
                "Land and Buildings": [
                    "Land", "Buildings", "Leasehold Improvements", "Building Improvements"
                ],
                "Plant and Machinery": [
                    "Production Equipment", "Heavy Machinery", "Tools", "Industrial Equipment"
                ],
                "Vehicles": [
                    "Cars", "Trucks", "Heavy Vehicles", "Delivery Vehicles"
                ],
                "Office Equipment": [
                    "Printers", "Copiers", "Communication Equipment", "Office Appliances"
                ],
                "IT Equipment": [
                    "Computers", "Servers", "Network Equipment", "Mobile Devices"
                ],
                "Furniture and Fixtures": [
                    "Office Furniture", "Storage Units", "Fixtures", "Decorative Items"
                ],
                "Hospital Equipment": [
                    "Medical Devices", "Radiology Equipment", "Theatre Equipment/Surgical", "Laboratory Equipment"
                ],
                "Software and Applications": [
                    "Operating Systems", "Business Applications", "Licenses", "Development Tools"
                ]
            }
            
            for category_name, subcategories in categories_data.items():
                # Create category
                category = AssetCategory(
                    name=category_name,
                    description=f"Assets in the {category_name} category"
                )
                session.add(category)
                session.flush()  # Get the ID
                
                print(f"   Created category: {category_name}")
                
                # Create subcategories
                for subcategory_name in subcategories:
                    subcategory = AssetSubCategory(
                        name=subcategory_name,
                        category_id=category.id,
                        description=f"{subcategory_name} under {category_name}"
                    )
                    session.add(subcategory)
                    print(f"     Created subcategory: {subcategory_name}")
            
            session.commit()
            print(" Asset categories created successfully")
            
    except Exception as e:
        print(f" Error creating asset categories: {e}")
        raise


def create_sample_assets():
    """Create sample assets for demonstration"""
    print(" Creating sample assets...")
    
    from app.core.database import get_db
    
    try:
        with get_db() as session:
            # Skip if assets already exist
            if session.query(Asset).count() > 0:
                print("  ℹ  Assets already exist, skipping...")
                return
            
            # Get categories and users
            categories = session.query(AssetCategory).all()
            users = session.query(User).all()
            
            if not categories:
                print("    No categories found, skipping asset creation")
                return
            
            # Extended sample assets data by category
            assets_by_category = {
                "IT Equipment": [
                    {"name": "Dell OptiPlex 7090", "description": "Desktop computer with Intel i7 processor", 
                     "unit_cost": 1299.99, "location": "IT Department", "supplier": "Dell Inc."},
                    {"name": "HP LaserJet Pro", "description": "Color laser printer for office use", 
                     "unit_cost": 449.99, "location": "Main Office", "supplier": "HP Inc."},
                    {"name": "MacBook Pro 16", "description": "Laptop for design and development work", 
                     "unit_cost": 2499.99, "location": "Development Team", "supplier": "Apple Inc."},
                    {"name": "Cisco Catalyst 2960", "description": "24-port managed network switch", 
                     "unit_cost": 599.99, "location": "Server Room", "supplier": "Cisco Systems"},
                    {"name": "Dell PowerEdge R740", "description": "Rack server for applications", 
                     "unit_cost": 4999.99, "location": "Data Center", "supplier": "Dell Technologies"},
                    {"name": "Lenovo ThinkPad E14", "description": "14-inch business laptop", 
                     "unit_cost": 899.99, "location": "Sales Department", "supplier": "Lenovo Inc."},
                    {"name": "HP ProDesk 400", "description": "Desktop workstation for CAD", 
                     "unit_cost": 1599.99, "location": "Engineering", "supplier": "HP Inc."},
                    {"name": "Fortinet FortiGate 200D", "description": "Network security firewall", 
                     "unit_cost": 2899.99, "location": "Server Room", "supplier": "Fortinet Inc."},
                    {"name": "Apple iPad Pro 12.9", "description": "Tablet for presentations", 
                     "unit_cost": 1199.99, "location": "Executive Suite", "supplier": "Apple Inc."},
                    {"name": "Samsung Galaxy S24 Ultra", "description": "Enterprise smartphone", 
                     "unit_cost": 1299.99, "location": "Mobile Pool", "supplier": "Samsung Electronics"}
                ],
                "Office Equipment": [
                    {"name": "Xerox WorkCentre 6515", "description": "Multifunction color printer", 
                     "unit_cost": 699.99, "location": "Copy Center", "supplier": "Xerox Corporation"},
                    {"name": "Canon imageCLASS", "description": "Document scanner and copier", 
                     "unit_cost": 399.99, "location": "Administrative Office", "supplier": "Canon Inc."},
                    {"name": "Polycom VVX 601", "description": "IP business phone", 
                     "unit_cost": 249.99, "location": "Reception", "supplier": "Polycom Inc."},
                    {"name": "Epson PowerLite", "description": "Conference room projector", 
                     "unit_cost": 899.99, "location": "Conference Room A", "supplier": "Epson America"},
                    {"name": "Brother HL-L8360", "description": "Monochrome laser printer", 
                     "unit_cost": 349.99, "location": "Finance Department", "supplier": "Brother Industries"},
                    {"name": "Ricoh MP C5504", "description": "Color multifunction printer", 
                     "unit_cost": 2499.99, "location": "Marketing Department", "supplier": "Ricoh Company"}
                ],
                "Furniture and Fixtures": [
                    {"name": "Herman Miller Aeron", "description": "Ergonomic office chair", 
                     "unit_cost": 1395.00, "location": "Executive Office", "supplier": "Herman Miller"},
                    {"name": "Steelcase Think", "description": "Office chair with lumbar support", 
                     "unit_cost": 415.00, "location": "Open Office Area", "supplier": "Steelcase Inc."},
                    {"name": "IKEA Bekant", "description": "Office desk with adjustable legs", 
                     "unit_cost": 149.99, "location": "Workstation Area", "supplier": "IKEA"},
                    {"name": "Hon Filing Cabinet", "description": "4-drawer vertical filing cabinet", 
                     "unit_cost": 299.99, "location": "Records Room", "supplier": "HNI Corporation"},
                    {"name": "Vitra Lounge Chair", "description": "Premium lounge seating", 
                     "unit_cost": 2800.00, "location": "Executive Lounge", "supplier": "Vitra AG"},
                    {"name": "Knoll Saarinen Table", "description": "Conference table", 
                     "unit_cost": 3500.00, "location": "Conference Room B", "supplier": "Knoll Inc."},
                    {"name": "USM Haller Shelving", "description": "Modular storage system", 
                     "unit_cost": 1299.00, "location": "Library", "supplier": "USM Furniture"},
                    {"name": "Steelcase Mobile Pedestal", "description": "Under-desk storage unit", 
                     "unit_cost": 299.00, "location": "Workstations", "supplier": "Steelcase Inc."}
                ],
                "Vehicles": [
                    {"name": "Toyota Camry 2023", "description": "Mid-size sedan for executive use", 
                     "unit_cost": 28500.00, "location": "Parking Garage Level 2", "supplier": "Toyota Motors"},
                    {"name": "Ford Transit Connect", "description": "Cargo van for deliveries", 
                     "unit_cost": 24000.00, "location": "Loading Dock", "supplier": "Ford Motor Company"},
                    {"name": "Honda Accord 2022", "description": "Sedan for sales team", 
                     "unit_cost": 25900.00, "location": "Parking Garage Level 1", "supplier": "Honda Motor Co."},
                    {"name": "Tesla Model 3", "description": "Electric sedan for executives", 
                     "unit_cost": 45000.00, "location": "Executive Parking", "supplier": "Tesla Inc."},
                    {"name": "Hyundai Tucson 2024", "description": "SUV for operations team", 
                     "unit_cost": 26500.00, "location": "Fleet Lot", "supplier": "Hyundai Motors"},
                    {"name": "Chevrolet Silverado", "description": "Heavy-duty truck for equipment", 
                     "unit_cost": 52000.00, "location": "Warehouse Area", "supplier": "General Motors"}
                ],
                "Hospital Equipment": [
                    {"name": "GE LightSpeed CT Scanner", "description": "Multi-detector CT imaging system", 
                     "unit_cost": 75000.00, "location": "Radiology Department", "supplier": "GE Healthcare"},
                    {"name": "Philips X-Ray System", "description": "Digital radiography system", 
                     "unit_cost": 45000.00, "location": "Radiology Department", "supplier": "Philips Healthcare"},
                    {"name": "Siemens SPECT Camera", "description": "Nuclear medicine imaging", 
                     "unit_cost": 55000.00, "location": "Nuclear Medicine", "supplier": "Siemens Healthcare"},
                    {"name": "Stryker Surgical Suite", "description": "Integrated operating room system", 
                     "unit_cost": 125000.00, "location": "Theatre 1", "supplier": "Stryker Corporation"},
                    {"name": "Abbott Laboratory Analyzer", "description": "Automated chemistry analyzer", 
                     "unit_cost": 35000.00, "location": "Laboratory", "supplier": "Abbott Diagnostics"},
                    {"name": "Roche Molecular System", "description": "PCR and molecular testing system", 
                     "unit_cost": 28000.00, "location": "Laboratory", "supplier": "Roche Diagnostics"}
                ],
                "Plant and Machinery": [
                    {"name": "Caterpillar Excavator 320", "description": "Heavy excavator for construction", 
                     "unit_cost": 95000.00, "location": "Equipment Yard", "supplier": "Caterpillar Inc."},
                    {"name": "Komatsu Bulldozer D65PX", "description": "Diesel bulldozer for earthwork", 
                     "unit_cost": 125000.00, "location": "Equipment Yard", "supplier": "Komatsu Ltd."},
                    {"name": "Bosch Industrial Drill", "description": "Industrial drilling machine", 
                     "unit_cost": 8500.00, "location": "Workshop", "supplier": "Bosch Power Tools"},
                    {"name": "Atlas Copco Compressor", "description": "Rotary screw air compressor", 
                     "unit_cost": 12000.00, "location": "Maintenance", "supplier": "Atlas Copco"}
                ],
                "Land and Buildings": [
                    {"name": "Main Office Building", "description": "Corporate headquarters building", 
                     "unit_cost": 1500000.00, "location": "Downtown", "supplier": "Real Estate Inc."},
                    {"name": "Warehouse Extension", "description": "Storage building addition", 
                     "unit_cost": 250000.00, "location": "Industrial District", "supplier": "Construction Co."}
                ],
                "Software and Applications": [
                    {"name": "Microsoft Windows Server 2022", "description": "Enterprise server operating system", 
                     "unit_cost": 6000.00, "location": "IT Infrastructure", "supplier": "Microsoft"},
                    {"name": "Oracle Database Enterprise", "description": "Database management system", 
                     "unit_cost": 40000.00, "location": "Data Center", "supplier": "Oracle Corporation"}
                ]
            }
            
            asset_counter = 1
            
            for category in categories:  # Process all categories
                if category.name in assets_by_category:
                    category_assets = assets_by_category[category.name]
                    
                    for asset_data in category_assets:
                        # Generate asset ID
                        asset_id = f"{category.name[:3].upper().replace(' ', '')}-{asset_counter:04d}"
                        
                        # Random status (80% available, remainder distributed among other statuses)
                        statuses = list(AssetStatus)
                        num_statuses = len(statuses)
                        # Primary weight for AVAILABLE, distribute remaining weight equally
                        primary_weight = 0.8
                        if num_statuses > 1:
                            remaining = 1.0 - primary_weight
                            other_weight = remaining / (num_statuses - 1)
                            status_weights = [primary_weight] + [other_weight] * (num_statuses - 1)
                        else:
                            status_weights = [1.0]
                        status = random.choices(statuses, weights=status_weights)[0]
                        
                        # Random purchase date (last 3 years)
                        days_ago = random.randint(1, 1095)  # 3 years
                        acquisition_date = date.today() - timedelta(days=days_ago)
                        
                        # Random assignment (60% chance of being assigned)
                        assigned_to = None
                        if users and random.random() < 0.6:
                            assigned_to = random.choice(users)
                        
                        # Calculate depreciation info (updated for new changes)
                        useful_life = random.randint(3, 10)  # 3-10 years
                        depreciation_method = random.choice(list(DepreciationMethod))
                        depreciation_percentage = round(random.uniform(0.05, 0.25), 3)  # 5-25% annual
                        total_cost = asset_data["unit_cost"]
                        
                        # Calculate current depreciation
                        years_owned = (date.today() - acquisition_date).days / 365.25
                        current_year = min(int(years_owned) + 1, useful_life)
                        
                        try:
                            annual_dep, accumulated_dep, book_value = DepreciationMethod.calculate_depreciation(
                                method=depreciation_method.value,
                                total_cost=total_cost,
                                useful_life=useful_life,
                                current_year=current_year
                            )
                        except:
                            accumulated_dep = total_cost * 0.1  # Fallback
                            book_value = total_cost - accumulated_dep
                        
                        # Calculate expiry date using Dec 31 depreciation logic
                        try:
                            from app.services.expiry_calculator import ExpiryCalculator
                            expiry_date = ExpiryCalculator.calculate_expiry_date(useful_life, acquisition_date)
                        except:
                            # Fallback: simple calculation (acquisition_date + useful_life years)
                            from dateutil.relativedelta import relativedelta
                            expiry_date = acquisition_date + relativedelta(years=useful_life)
                        
                        # Create asset with all new fields
                        asset = Asset(
                            asset_id=asset_id,
                            name=asset_data["name"],
                            description=asset_data["description"],  # Now properly handled
                            category_id=category.id,
                            acquisition_date=acquisition_date,
                            supplier=asset_data["supplier"],
                            quantity=1,
                            unit_cost=asset_data["unit_cost"],
                            total_cost=total_cost,
                            useful_life=useful_life,
                            depreciation_method=depreciation_method,
                            depreciation_percentage=depreciation_percentage,  # New field
                            accumulated_depreciation=accumulated_dep,
                            net_book_value=book_value,
                            location=asset_data["location"],
                            department=assigned_to.department if assigned_to else "Unassigned",
                            assigned_to_id=assigned_to.id if assigned_to else None,
                            status=status,
                            asset_tag=f"TAG-{asset_counter:06d}",
                            serial_number=f"SN{random.randint(100000, 999999)}",
                            custodian=assigned_to.name if assigned_to else None,
                            model_number=f"MODEL-{random.randint(1000, 9999)}",  # Added model number
                            expiry_date=expiry_date  # Using Dec 31 depreciation logic
                        )
                        
                        session.add(asset)
                        print(f"   Created asset: {asset_data['name']} ({asset_id})")
                        asset_counter += 1
            
            session.commit()
            total_assets_created = asset_counter - 1
            print(f" Created {total_assets_created} sample assets successfully")
            
    except Exception as e:
        import traceback
        print(f" Error creating sample assets: {e}")
        traceback.print_exc()
        raise


def initialize_system_settings():
    """Initialize system settings and CRUD restrictions"""
    print(" Initializing system settings...")
    
    from app.core.database import get_db
    from app.core.models import SystemConfiguration
    
    try:
        settings_service = SettingsService()
        
        # Enable CRUD operations (important for imports)
        with get_db() as session:
            # Check if CRUD restrictions already exist
            crud_setting = session.query(SystemConfiguration).filter(
                SystemConfiguration.category == 'CRUD_RESTRICTIONS',
                SystemConfiguration.key == 'allow_asset_creation'
            ).first()
            
            if not crud_setting:
                crud_setting = SystemConfiguration(
                    category='CRUD_RESTRICTIONS',
                    key='allow_asset_creation',
                    value='true',
                    data_type='boolean',
                    description='Allow users to create assets',
                    is_system='true'
                )
                session.add(crud_setting)
                print("   Enabled asset creation")
            
            # Enable asset editing
            edit_setting = session.query(SystemConfiguration).filter(
                SystemConfiguration.category == 'CRUD_RESTRICTIONS',
                SystemConfiguration.key == 'allow_asset_editing'
            ).first()
            
            if not edit_setting:
                edit_setting = SystemConfiguration(
                    category='CRUD_RESTRICTIONS',
                    key='allow_asset_editing',
                    value='true',
                    data_type='boolean',
                    description='Allow users to edit assets',
                    is_system='true'
                )
                session.add(edit_setting)
                print("   Enabled asset editing")
            
            session.commit()
        
        print(" System settings initialized successfully")
        
    except Exception as e:
        print(f" Error initializing system settings: {e}")
        raise


def create_sample_audit_log():
    """Create sample audit log entry"""
    print(" Creating sample audit log...")
    
    from app.core.database import get_db
    from app.services.audit_service import AuditService
    
    try:
        audit_service = AuditService()
        
        # Log system initialization
        audit_service.log_action(
            action="SYSTEM_INITIALIZED",
            description="Asset Management System database initialized with sample data",
            new_values={
                "initialization_date": datetime.utcnow().isoformat(),
                "sample_data": "true"
            }
        )
        
        print(" Sample audit log created successfully")
        
    except Exception as e:
        print(f" Error creating sample audit log: {e}")
        raise


def print_summary():
    """Print summary of created data"""
    print("\n" + "="*60)
    print(" DATABASE INITIALIZATION COMPLETE!")
    print("="*60)
    
    from app.core.database import get_db
    
    try:
        with get_db() as session:
            # Count records
            user_count = session.query(User).count()
            category_count = session.query(AssetCategory).count()
            asset_count = session.query(Asset).count()
            role_count = session.query(Role).count()
            permission_count = session.query(Permission).count()
            
            print(f" SUMMARY:")
            print(f"    Users created: {user_count}")
            print(f"    Roles created: {role_count}")  
            print(f"    Permissions created: {permission_count}")
            print(f"    Categories created: {category_count}")
            print(f"    Assets created: {asset_count}")
            
            print(f"\n DEFAULT ADMIN CREDENTIALS:")
            print(f"   Email: admin@company.com")
            print(f"   Password: admin123")
            print(f"     Please change the default password after first login!")
            
            print(f"\n You can now start the application:")
            print(f"   python app/main.py")
            
    except Exception as e:
        print(f" Error getting summary: {e}")


def main():
    """Main initialization function"""
    print(" Asset Management System - Database Initialization")
    print("=" * 60)
    
    try:
        # Initialize database
        initialize_database()
        
        # Create roles and permissions
        create_default_roles_and_permissions()
        
        # Create sample users
        create_sample_users()
        
        # Create asset categories
        create_asset_categories()
        
        # Create sample assets
        create_sample_assets()
        
        # Initialize system settings
        initialize_system_settings()
        
        # Create sample audit log
        create_sample_audit_log()
        
        # Print summary
        print_summary()
        
    except Exception as e:
        print(f"\n INITIALIZATION FAILED: {e}")
        print("Please check the error details and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
