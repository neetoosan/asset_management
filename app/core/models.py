from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Float, Text, Enum
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import enum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(enum.Enum):
    ADMIN = "Admin"
    USER = "User"
    VIEWER = "Viewer"


class PermissionType(enum.Enum):
    CREATE_ASSET = "Create Asset"
    VIEW_ASSET = "View Asset"
    EDIT_ASSET = "Edit Asset"
    DELETE_ASSET = "Delete Asset"
    MANAGE_USERS = "Manage Users"
    VIEW_REPORTS = "View Reports"
    SYSTEM_CONFIG = "System Configuration"


class AssetStatus(enum.Enum):
    AVAILABLE = "Available"
    IN_USE = "In Use"
    MAINTENANCE = "Under Maintenance"
    RETIRED = "Retired"
    DAMAGED = "Damaged"
    DISPOSED = "Disposed"


class DepreciationMethod(enum.Enum):
    STRAIGHT_LINE = "Straight Line"
    DECLINING_BALANCE = "Declining Balance"
    DOUBLE_DECLINING = "Double Declining Balance"
    SUM_OF_YEARS = "Sum of Years Digits"
    
    @staticmethod
    def calculate_depreciation(method, total_cost, useful_life, current_year=1, salvage_value=0):
        """
        Calculate depreciation based on the specified method.
        
        For NEW ASSETS (current_year=1):
        - annual_depreciation = depreciation for year 1
        - accumulated_depreciation = 0 (no depreciation has been applied yet)
        - current_book_value = total_cost (full value at acquisition)
        
        For EXISTING ASSETS (current_year>1):
        - annual_depreciation = depreciation for the current year
        - accumulated_depreciation = sum of depreciation from year 1 to year (current_year-1)
        - current_book_value = total_cost - accumulated_depreciation
        
        Args:
            method: DepreciationMethod enum value or string
            total_cost: Initial cost of the asset
            useful_life: Expected useful life in years
            current_year: Current year of depreciation (1-based). Year 1 = newly acquired asset
            salvage_value: Expected salvage value at end of useful life
        
        Returns:
            tuple: (annual_depreciation, accumulated_depreciation, current_book_value)
        """
        if useful_life <= 0 or total_cost <= 0:
            return 0.0, 0.0, float(total_cost)
            
        if current_year > useful_life:
            return 0.0, float(total_cost - salvage_value), float(salvage_value)
        
        # Normalize method to DepreciationMethod enum if a value/string is passed
        if isinstance(method, DepreciationMethod):
            m = method
        else:
            try:
                m = DepreciationMethod(method)
            except Exception:
                # Try matching by value
                m = None
                for member in DepreciationMethod:
                    if member.value == method:
                        m = member
                        break
        if m is None:
            raise ValueError(f"Unsupported depreciation method: {method}")

        if m == DepreciationMethod.STRAIGHT_LINE:
            # Straight-line: constant depreciation each year
            depreciable_amount = total_cost - salvage_value
            annual_depreciation = depreciable_amount / useful_life
            accumulated_depreciation = annual_depreciation * (current_year - 1)
            current_book_value = total_cost - accumulated_depreciation
            
        elif m == DepreciationMethod.DECLINING_BALANCE:
            # Declining balance: fixed rate applied to book value each year
            # Rate is calculated to reach salvage value over useful life
            if salvage_value > 0:
                rate = 1 - (salvage_value / total_cost) ** (1 / useful_life)
            else:
                rate = 1 - (0.1 / total_cost) ** (1 / useful_life)  # Assume 10% salvage if not specified
            
            book_value = total_cost
            accumulated_depreciation = 0.0
            
            # Calculate accumulated depreciation through previous years
            for year in range(1, current_year):
                annual_dep = book_value * rate
                accumulated_depreciation += annual_dep
                book_value -= annual_dep
            
            # Current year's depreciation
            annual_depreciation = book_value * rate
            # Don't let book value go below salvage value
            if book_value - annual_depreciation < salvage_value:
                annual_depreciation = max(0, book_value - salvage_value)
            current_book_value = book_value  # Book value BEFORE this year's depreciation
            
        elif m == DepreciationMethod.DOUBLE_DECLINING:
            # Double declining balance: rate = 2/useful_life, applied to book value
            rate = 2.0 / useful_life
            book_value = total_cost
            accumulated_depreciation = 0.0
            
            # Calculate accumulated depreciation through previous years
            for year in range(1, current_year):
                annual_dep = book_value * rate
                # Don't depreciate below salvage value
                if book_value - annual_dep < salvage_value:
                    annual_dep = max(0, book_value - salvage_value)
                accumulated_depreciation += annual_dep
                book_value -= annual_dep
            
            # Current year's depreciation
            annual_depreciation = book_value * rate
            if book_value - annual_depreciation < salvage_value:
                annual_depreciation = max(0, book_value - salvage_value)
            current_book_value = book_value  # Book value BEFORE this year's depreciation
            
        elif m == DepreciationMethod.SUM_OF_YEARS:
            # Sum of years digits: depreciation decreases each year
            # Year 1 gets the largest fraction, year N gets the smallest
            sum_of_years = (useful_life * (useful_life + 1)) / 2.0
            depreciable_amount = total_cost - salvage_value
            
            accumulated_depreciation = 0.0
            
            # Calculate accumulated depreciation through previous years
            for year in range(1, current_year):
                remaining_years = useful_life - (year - 1)
                annual_dep = (depreciable_amount * remaining_years) / sum_of_years
                accumulated_depreciation += annual_dep
            
            # Current year's depreciation
            remaining_years_current = useful_life - (current_year - 1)
            annual_depreciation = (depreciable_amount * remaining_years_current) / sum_of_years
            current_book_value = total_cost - accumulated_depreciation
        
        return float(annual_depreciation), float(accumulated_depreciation), float(current_book_value)


class ReportStatus(enum.Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    IN_PROGRESS = "In Progress"


class ReportFormat(enum.Enum):
    PDF = "PDF Document"
    EXCEL = "Excel Spreadsheet (.xlsx)"
    CSV = "CSV File"
    WORD = "Word Document (.docx)"


class AssetCategory(Base):
    __tablename__ = "asset_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assets = relationship("Asset", back_populates="category")
    subcategories = relationship("AssetSubCategory", back_populates="category")


class AssetSubCategory(Base):
    __tablename__ = "asset_subcategories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('asset_categories.id'), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category = relationship("AssetCategory", back_populates="subcategories")
    assets = relationship("Asset", back_populates="subcategory")


class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, nullable=False, unique=True)  # User-defined asset ID
    description = Column(Text, nullable=False)  # Asset description
    name = Column(String, nullable=False)  # Asset name (derived from description if needed)
    
    # Category information
    category_id = Column(Integer, ForeignKey('asset_categories.id'), nullable=False)
    subcategory_id = Column(Integer, ForeignKey('asset_subcategories.id'))
    
    # Acquisition information
    acquisition_date = Column(Date, nullable=False)
    supplier = Column(String, nullable=False)  # Supplier/Vendor
    
    # Financial information
    quantity = Column(Integer, default=1)
    unit_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    
    # Depreciation information
    useful_life = Column(Integer)  # In years
    depreciation_method = Column(Enum(DepreciationMethod))
    depreciation_percentage = Column(Float, default=0.0)  # Annual depreciation percentage (0-100)
    accumulated_depreciation = Column(Float, default=0.0)
    net_book_value = Column(Float, nullable=False)
    salvage_value = Column(Float, default=0.0)  # Residual value at end of useful life
    depreciation_years_applied = Column(Integer, default=0)  # Track number of Dec 31 depreciations applied
    
    # Expiry/End of Life information
    expiry_date = Column(Date)  # Calculated as acquisition_date + useful_life
    
    # Location and assignment
    location = Column(String, nullable=False)
    custodian = Column(String)  # Person responsible for the asset
    department = Column(String)  # Department the asset belongs to
    assigned_to_id = Column(Integer, ForeignKey('users.id'))
    
    # Status and tracking
    status = Column(Enum(AssetStatus), default=AssetStatus.AVAILABLE)
    asset_tag = Column(String, unique=True)  # Physical tag/barcode
    model_number = Column(String)  # Manufacturer model number
    serial_number = Column(String)  # Manufacturer serial number
    
    # Additional information
    remarks = Column(Text)  # Additional notes/remarks
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("AssetCategory", back_populates="assets")
    subcategory = relationship("AssetSubCategory", back_populates="assets")
    assigned_to = relationship("User", back_populates="assets")
    
    def get_remaining_useful_life(self):
        """Calculate remaining useful life using Dec 31 depreciation logic"""
        if not self.acquisition_date or not self.useful_life:
            return self.useful_life or 0
        
        from app.services.expiry_calculator import ExpiryCalculator
        return ExpiryCalculator.calculate_remaining_useful_life(
            self.useful_life,
            self.acquisition_date
        )


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(UserRole), nullable=False, unique=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(PermissionType), nullable=False, unique=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    roles = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False)
    granted = Column(String, default="true")  # "true", "false", "conditional"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)  # Hashed password
    department = Column(String)
    position = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    is_active = Column(String, default="Active")  # "Active", "Inactive", "Suspended"
    last_login = Column(DateTime)  # Track last login time
    password_changed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    assets = relationship("Asset", back_populates="assigned_to")
    role = relationship("Role", back_populates="users")
    report_logs = relationship("ReportLog", back_populates="generated_by")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Set a hashed password"""
        self.password_hash = pwd_context.hash(password)
        self.password_changed_at = datetime.utcnow()
        
    def verify_password(self, password):
        """Verify a password against the hash"""
        return pwd_context.verify(password, self.password_hash)


class ReportLog(Base):
    __tablename__ = "report_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String, nullable=False)  # Type of report generated
    report_format = Column(Enum(ReportFormat), nullable=False)  # Export format
    file_name = Column(String, nullable=False)  # Generated file name
    file_path = Column(String)  # Path where file was saved (optional)
    
    # Report parameters
    date_range_start = Column(Date)  # Start date for report filtering
    date_range_end = Column(Date)    # End date for report filtering
    
    # Report metadata
    records_count = Column(Integer, default=0)  # Number of records in report
    status = Column(Enum(ReportStatus), default=ReportStatus.IN_PROGRESS)
    error_message = Column(Text)  # Error details if failed
    
    # Audit fields
    generated_by_id = Column(Integer, ForeignKey('users.id'))  # User who generated the report
    generated_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)  # When report generation was completed
    
    # Relationships
    generated_by = relationship("User", back_populates="report_logs")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT, etc.
    table_name = Column(String)  # Table affected (if applicable)
    record_id = Column(String)   # ID of the record affected (if applicable)
    
    # Action details
    description = Column(Text, nullable=False)  # Human-readable description
    old_values = Column(Text)    # JSON string of old values (for updates/deletes)
    new_values = Column(Text)    # JSON string of new values (for creates/updates)
    
    # User and session info
    user_id = Column(Integer, ForeignKey('users.id'))  # User who performed the action
    username = Column(String)    # Username (in case user is deleted later)
    ip_address = Column(String)  # IP address (for web requests)
    user_agent = Column(String)  # User agent (for web requests)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User")


class SystemConfiguration(Base):
    __tablename__ = "system_configuration"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)  # CRUD_RESTRICTIONS, SYSTEM_SETTINGS, etc.
    key = Column(String, nullable=False)       # Specific setting key
    value = Column(Text, nullable=False)       # Setting value (JSON string for complex values)
    data_type = Column(String, default="string")  # string, boolean, integer, json
    
    # Metadata
    description = Column(Text)  # Description of what this setting does
    default_value = Column(Text)  # Default value
    is_system = Column(String, default="false")  # System settings vs user-configurable
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    updated_by = relationship("User")


class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_token = Column(String, unique=True, nullable=False)
    
    # Session timing
    login_time = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    logout_time = Column(DateTime)
    
    # Session status - using consistent string values
    is_active = Column(String, default="Active")  # "Active", "Expired", "Revoked"
    
    # Client information
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
