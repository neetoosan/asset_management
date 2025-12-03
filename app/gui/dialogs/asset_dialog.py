from PySide6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox
from PySide6.QtCore import Slot, Qt, QDate
from decimal import Decimal
from ..ui.asset_dialog_ui import Ui_AssetDialog
from ...services.asset_service import AssetService
from ...services.session_service import SessionService
from ...core.models import AssetStatus, DepreciationMethod

class AssetDialog(QDialog):
    def __init__(self, session_service: SessionService, asset=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_AssetDialog()
        self.ui.setupUi(self)
        self.asset_service = AssetService()
        self.session_service = session_service
        self.asset = None  # Will hold primitive dict when editing

        # Normalize the incoming asset parameter to a primitive dict if possible.
        # Acceptable forms: None, int/str asset id, primitive dict, or ORM instance.
        try:
            if asset is None:
                self.asset = None
            elif isinstance(asset, dict):
                self.asset = asset
            elif isinstance(asset, (int, str)):
                try:
                    self.asset = self.asset_service.get_asset_by_id(int(asset))
                except Exception:
                    self.asset = None
            else:
                # ORM instance or other object: try to extract id then fetch fresh
                aid = getattr(asset, 'id', None)
                if aid:
                    try:
                        fresh = self.asset_service.get_asset_by_id(aid)
                        if fresh:
                            self.asset = fresh
                        else:
                            self.asset = None
                    except Exception:
                        self.asset = None
                else:
                    # Unknown object, keep None
                    self.asset = None
        except Exception:
            self.asset = None
        
        # Set current user context for audit logging
        if self.session_service.is_authenticated():
            user_id = self.session_service.get_user_id()
            user_name = self.session_service.get_username()
            self.asset_service.set_current_user(user_id, user_name)
        
        self.setup_connections()
        self.load_categories()
        # Populate known locations
        self.populate_locations()
        self.load_depreciation_methods()
        self.setup_calculations()
        
        # Load asset data if editing
        if self.asset:
            self.load_asset_data()
            self.setWindowTitle("Edit Asset")
        else:
            self.setWindowTitle("Add New Asset")
        
    def setup_connections(self):
        # Note: the UI `setupUi` already connects the buttonBox accepted/rejected
        # signals to the dialog's accept/reject. Avoid reconnecting here which
        # caused the accept handler to run twice and create duplicate records.
        self.ui.categoryCombo.currentIndexChanged.connect(self.update_subcategories)
        self.ui.quantitySpinBox.valueChanged.connect(self.calculate_total_cost)
        self.ui.unitCostSpinBox.valueChanged.connect(self.calculate_total_cost)
        # Depreciation calculation triggers: percentage change, useful life change, total cost change
        self.ui.depreciationPercentageSpinBox.valueChanged.connect(self.calculate_depreciation)
        self.ui.usefulLifeSpinBox.valueChanged.connect(self.calculate_depreciation)
        # Display expiry date based on useful life (year-end accounting logic)
        self.ui.acquisitionDateEdit.dateChanged.connect(self.display_expiry_date)
        self.ui.usefulLifeSpinBox.valueChanged.connect(self.display_expiry_date)
        
    def load_categories(self):
        """Load categories from database"""
        try:
            # Open a session and load categories while session is active to avoid DetachedInstanceError
            with self.asset_service.get_session() as session:
                categories = self.asset_service.get_all_categories(session)
                self.ui.categoryCombo.clear()
                # Store category data as primitives while session is open
                for category in categories:
                    # category is now a dict with 'id' and 'name'
                    self.ui.categoryCombo.addItem(str(category.get('name', '')), category.get('id'))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load categories: {str(e)}")
        
    def load_depreciation_methods(self):
        """Load depreciation methods from enum"""
        methods = [method.value for method in DepreciationMethod]
        self.ui.depreciationMethodCombo.addItems(methods)
        
    def setup_calculations(self):
        # Set current date as default
        self.ui.acquisitionDateEdit.setDate(QDate.currentDate())
        
        # Setup unit cost spinbox
        self.ui.unitCostSpinBox.setRange(0.00, 999999999.99)
        self.ui.unitCostSpinBox.setSingleStep(100.00)
        self.ui.unitCostSpinBox.setDecimals(2)
        self.ui.unitCostSpinBox.setAccelerated(True)  # Faster increment when holding button
        self.ui.unitCostSpinBox.setValue(0.00)  # Set initial value
        
        # Setup depreciation percentage spinbox
        self.ui.depreciationPercentageSpinBox.setRange(0.00, 100.00)
        self.ui.depreciationPercentageSpinBox.setSingleStep(0.50)
        self.ui.depreciationPercentageSpinBox.setDecimals(2)
        self.ui.depreciationPercentageSpinBox.setAccelerated(True)  # Faster increment when holding button
        self.ui.depreciationPercentageSpinBox.setValue(0.00)  # Set initial value to 0%
        
        # Initialize calculation fields
        self.ui.totalCostInput.setText("0.00")
        self.ui.annualDepreciationInput.setText("0.00")
        
        # Initialize depreciation data
        self._depreciation_data = {
            'annual_depreciation': 0.00,
            'accumulated_depreciation': 0.00,
            'net_book_value': 0.00,
            'salvage_value': 0.00
        }
        
    def load_asset_data(self):
        """Load existing asset data for editing"""
        if not self.asset:
            return
        
        try:
            # Support asset being a dict (service) or ORM object
            if isinstance(self.asset, dict):
                aid = self.asset.get('asset_id', '')
                desc = self.asset.get('description', '')
                supplier = self.asset.get('supplier', '')
                location = self.asset.get('location', '')
                custodian = self.asset.get('custodian', '')
                remarks = self.asset.get('remarks', '')
                quantity = int(self.asset.get('quantity') or 1)
                unit_cost = float(self.asset.get('unit_cost') or 0)
                useful_life = int(self.asset.get('useful_life') or 5)
                acq = self.asset.get('acquisition_date')
                category_id = self.asset.get('category_id')
                subcategory_id = self.asset.get('subcategory_id')
                dep_method = self.asset.get('depreciation_method')
                dep_percentage = float(self.asset.get('depreciation_percentage') or 0)
            else:
                aid = getattr(self.asset, 'asset_id', '')
                desc = getattr(self.asset, 'description', '')
                supplier = getattr(self.asset, 'supplier', '')
                location = getattr(self.asset, 'location', '')
                custodian = getattr(self.asset, 'custodian', '')
                remarks = getattr(self.asset, 'remarks', '')
                quantity = getattr(self.asset, 'quantity', 1)
                unit_cost = float(getattr(self.asset, 'unit_cost', 0) or 0)
                useful_life = getattr(self.asset, 'useful_life', 5)
                acq = getattr(self.asset, 'acquisition_date', None)
                category_id = getattr(self.asset, 'category_id', None)
                subcategory_id = getattr(self.asset, 'subcategory_id', None)
                dep_method = getattr(self.asset, 'depreciation_method', None)
                dep_percentage = float(getattr(self.asset, 'depreciation_percentage', 0) or 0)

            # Load basic info
            self.ui.assetIdInput.setText(aid or "")
            self.ui.descriptionInput.setPlainText(desc or "")
            self.ui.supplierInput.setText(supplier or "")
            # Set location combo to saved value if present
            try:
                if location:
                    idx = self.ui.locationCombo.findText(str(location))
                    if idx >= 0:
                        self.ui.locationCombo.setCurrentIndex(idx)
                    else:
                        # if location not in list, add it and select
                        self.ui.locationCombo.addItem(str(location))
                        self.ui.locationCombo.setCurrentIndex(self.ui.locationCombo.count() - 1)
                else:
                    self.ui.locationCombo.setCurrentIndex(0)
            except Exception:
                pass
            
            # model / serial
            try:
                self.ui.modelNumberInput.setText(self.asset.get('model_number', '') if isinstance(self.asset, dict) else getattr(self.asset, 'model_number', '') or '')
            except Exception:
                pass
            try:
                self.ui.serialNumberInput.setText(self.asset.get('serial_number', '') if isinstance(self.asset, dict) else getattr(self.asset, 'serial_number', '') or '')
            except Exception:
                pass
            
            self.ui.custodianInput.setText(custodian or "")
            self.ui.remarksText.setPlainText(remarks or "")

            # Load financial info
            self.ui.quantitySpinBox.setValue(quantity or 1)
            self.ui.unitCostSpinBox.setValue(unit_cost)
            self.ui.usefulLifeSpinBox.setValue(useful_life or 5)

            # Load dates
            if acq:
                try:
                    if isinstance(acq, str):
                        qdate = QDate.fromString(acq.split('T')[0], "yyyy-MM-dd")
                    else:
                        qdate = QDate.fromString(acq.strftime("%Y-%m-%d"), "yyyy-MM-dd")
                    self.ui.acquisitionDateEdit.setDate(qdate)
                except Exception:
                    pass

            # Load category and subcategory
            if category_id:
                for i in range(self.ui.categoryCombo.count()):
                    if self.ui.categoryCombo.itemData(i) == category_id:
                        self.ui.categoryCombo.setCurrentIndex(i)
                        self.update_subcategories()  # Load subcategories
                        break

            if subcategory_id:
                for i in range(self.ui.subCategoryCombo.count()):
                    if self.ui.subCategoryCombo.itemData(i) == subcategory_id:
                        self.ui.subCategoryCombo.setCurrentIndex(i)
                        break

            # Load depreciation method
            method_text = None
            if dep_method:
                if isinstance(dep_method, str):
                    method_text = dep_method
                else:
                    method_text = dep_method.value if hasattr(dep_method, 'value') else str(dep_method)

            if method_text:
                for i in range(self.ui.depreciationMethodCombo.count()):
                    if self.ui.depreciationMethodCombo.itemText(i) == method_text:
                        self.ui.depreciationMethodCombo.setCurrentIndex(i)
                        break
            
            # Load depreciation percentage
            self.ui.depreciationPercentageSpinBox.setValue(dep_percentage or 0)

            # Trigger calculations
            self.calculate_total_cost()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load asset data: {str(e)}")
    
    def accept(self):
        if self.validate():
            if self.save_asset():
                super().accept()
        
    def update_subcategories(self):
        """Load subcategories from database based on selected category"""
        try:
            category_id = self.ui.categoryCombo.currentData()
            if category_id:
                with self.asset_service.get_session() as session:
                    subcategories = self.asset_service.get_subcategories_by_category_id(session, category_id)
                    self.ui.subCategoryCombo.clear()
                    # Store subcategory data directly rather than ORM objects
                    for subcategory in subcategories:
                        # subcategory is a dict with 'id' and 'name'
                        self.ui.subCategoryCombo.addItem(str(subcategory.get('name', '')), subcategory.get('id'))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load subcategories: {str(e)}")
        
    def populate_locations(self):
        """Populate the location combo box with the predefined list."""
        LOCATIONS = [
            "OUTDOOR",
            "KITCHEN",
            "OUTDOOR AC (ON TOP OF ROOF)",
            "HEAD CHEF OFFICE",
            "NUTRITION & DIATETICS",
            "KITCHEN (BIG)",
            "OFFICE BASENO 34",
            "BOARD ROOM",
            "DAVID PRESIDENTIAL WING WELLNESS",
            "ELECTRICAL OFFICE",
            "IT EQUIPMENT",
            "SERVER RM (2)",
            "SERVER RM(1) MAIN SERVER",
            "MDS OFFICE",
            "WALKWAY (FIRST FLOOR)",
            "SERVER ROOM 3",
            "BACK TO WALKWAY",
            "SERVER ROOM 4",
            "IT OFFICE",
            "IT EQUIPMENT STORE",
            "HEAD OF ENGINEERING OFFICE",
            "SECURITY POST",
            "BUSINESS DEVELOPMENT OFFICE",
            "FACILTY/CSO OFFICE",
            "WAITING AREA: HMO/BUSINESS DEVELOPMENT RECEPTION",
            "OPERATION MEETING: GROUND FLOOR",
            "CCO OFFICE P.A / E.A",
            "CCO OFFICE",
            "ACCOUNTS",
            "UPS ROOM",
            "ULTRA SOUND ROOM",
            "MAMMO ROOM",
            "HOD's ROOM",
            "CHANGING ROOM",
            "MIR TECHNICAL ROOM",
            "CT / MIR SUITE",
            "MIR ROOM",
            "RADIOLOGY LOUNGE",
            "CENTRAL PHARMACY STORE",
            "PHARMACY HOD OFFICE",
            "STAFF LOUNGE",
            "COMPOUNDING ROOM",
            "PHARMACY SELLING ROOM",
            "RADIOLOGY X-RAY ROOM",
            "PHARMACY REFRIGERATOR ROOM",
            "RADIOLOGY FRONT DESK",
            "ROOM ADJACENT FRONT DESK RADIOLOGY",
            "RADIOGRAPHER OFFICE",
            "ICT OFFICE",
            "PATIENCE EXPERIENCE ROOM",
            "REST ROOM (MALE) GROUND FLOOR",
            "REST ROOM (FEMALE) GROUND FLOOR",
            "OPTHALMOLOGY RECEPTION",
            "OPTHALMOLOGY CONSULTING ROOM 1",
            "OPTHALMOLOGY HOD OFFICE",
            "INSTRUMENTATION ROOM (OPTHAL)",
            "OPHTICAL WORKSHOP",
            "EAR, NOSE & THROAT OPHTAL",
            "PROCEDURE ROOM (OPTHAL)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (1)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (2)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (3)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (4)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (5)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (6)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (7)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (8)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (9)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (10)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (11)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (12)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (13)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (14)",
            "CARDIOLOGY CLINIC: CONSULTING ROOM (15)",
            "REST ROOM (MALE) FIRST FLOOR",
            "REST ROOM (FEMALE) FIRST FLOOR",
            "GROUND FLOOR MALE TOILET",
            "GROUND FLOOR FEMALE TOILET",
            "WATER TREATMENT AREA",
            "ENGINEERING OFFICE",
            "ENGINEERING STORE",
            "CMD & CCO's OFFICE",
            "EA's OFFICE",
            "CMD/CCO'S OFFICE (MAIN)",
            "CONSUMABLE STORE",
            "CONSUMABLE STORE 2",
            "CLEANER'S POTTER",
            "KITCHEN (SMALL)",
            "FACILITY MGR OFFICE",
            "GOPD RECEPTION 2",
            "PROCEDURE ROOM",
            "STAFF LOUNGE (GOPD)",
            "CONSULTING ROOM 7",
            "CONSULTING ROOM 11 (GOPD)",
            "ROOM AL 116",
            "CONSULTING ROOM 10",
            "CONSULTING ROOM 8",
            "ROOM AL 111",
            "CONSULTING ROOM 6",
            "CONSULTING ROOM 3",
            "CONSULTING ROOM (GOPD RECEPTION)",
            "GOPD FRONT OFFICE",
            "THE ARK CHAPEL",
            "PHYSIOTHERAPY (RECEPTION DESK)",
            "PHYSIOTHERAPY CONSULTING OFFICES",
            "GYM FLOOR",
            "CONSULTING ROOM",
            "PRIVTA WARD 04 (ROOM 07)",
            "PRIVTAE WARD ROOM 06",
            "PRIVTAE WARD ROOM 05",
            "PRIVTAE WARD ROOM 03",
            "PRIVTAE WARD ROOM 02",
            "PRIVTAE WARD ROOM 01",
            "PRIVTAE WARD STORE",
            "PRIVTAE WARD FRONT DESK (REMAINING)",
            "MAIN ACIDENT AND EMERGENCY",
            "ACIDENT AND EMERGENCY RECEPTION",
            "AR 115 TRUMA",
            "GF 36",
            "GF 37",
            "GF 38",
            "GF 39",
            "AR 112",
            "AR 113",
            "GF 44",
            "AR 114",
            "AR 110",
            "PRIVATE WARD 4",
            "PRIVATE WARD 10",
            "010 53",
            "PRIVATE WARD 9",
            "PRIVATE WARD 8",
            "CEO OFFICE (CEO SECRETARY)",
            "ENTRANCE BEFORE SECRETARY (CLINIC MANAGER)",
            "INTERNAL AUDITOR",
            "CEO MAIN OFFICE",
            "CEO OFFICE"
        ]
        try:
            self.ui.locationCombo.clear()
            for loc in LOCATIONS:
                self.ui.locationCombo.addItem(loc)
        except Exception:
            pass
    
    def display_expiry_date(self):
        """Display expiry date using Dec 31 depreciation logic - aligned to year end"""
        try:
            from ...services.expiry_calculator import ExpiryCalculator
            acquisition_date = self.ui.acquisitionDateEdit.date().toPython()
            useful_life = self.ui.usefulLifeSpinBox.value()
            
            # Use year-end aligned calculation for accounting compliance
            expiry_date = ExpiryCalculator.calculate_expiry_date_aligned_to_year_end(
                acquisition_date, useful_life
            )
            
            if hasattr(self.ui, 'expiryDateDisplay'):
                self.ui.expiryDateDisplay.setText(expiry_date.strftime('%Y-%m-%d'))
        except Exception as e:
            print(f"Error displaying expiry date: {e}")
    
    def calculate_total_cost(self):
        quantity = self.ui.quantitySpinBox.value()
        unit_cost = self.ui.unitCostSpinBox.value()
        total_cost = quantity * unit_cost
        self.ui.totalCostInput.setText(f"{total_cost:,.2f}")
        self.calculate_depreciation()
        
    def calculate_depreciation(self):
        """Calculate depreciation based on percentage and year-end accounting (Dec 31)"""
        try:
            # Get total cost, handling empty or invalid input
            total_cost_text = self.ui.totalCostInput.text().strip().replace(",", "")
            if not total_cost_text:
                # If no total cost yet, initialize with zeros
                self.ui.annualDepreciationInput.setText("0.00")
                self._depreciation_data = {
                    'annual_depreciation': 0.00,
                    'accumulated_depreciation': 0.00,
                    'net_book_value': 0.00,
                    'salvage_value': 0.00
                }
                return
                
            total_cost = float(total_cost_text)
            if total_cost <= 0:
                return
            
            # Get depreciation percentage (0-100)
            depreciation_percent = self.ui.depreciationPercentageSpinBox.value()
            
            # Calculate annual depreciation amount based on percentage
            annual_depreciation = total_cost * (depreciation_percent / 100.0)
            
            # For a new asset, accumulated depreciation = 0 until end of first year (Dec 31)
            accumulated_depreciation = 0.00
            
            # Net book value = total cost - accumulated depreciation
            net_book_value = total_cost - accumulated_depreciation
            
            # 10% salvage value assumption
            salvage_value = total_cost * 0.10
            
            # Update UI with annual depreciation
            self.ui.annualDepreciationInput.setText(f"{annual_depreciation:,.2f}")
            
            # Save these values for later database storage
            # Year-end accounting: accumulated depreciation is 0 for new assets,
            # will be updated on Dec 31 each year
            self._depreciation_data = {
                'annual_depreciation': annual_depreciation,
                'accumulated_depreciation': accumulated_depreciation,
                'net_book_value': net_book_value,
                'salvage_value': salvage_value,
                'depreciation_percentage': depreciation_percent
            }
            
        except Exception as e:
            QMessageBox.warning(self, "Calculation Error", 
                              f"Error calculating depreciation: {str(e)}\n\n"
                              "Please check your input values.")
        
    def validate(self):
        if not self.ui.assetIdInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Asset ID is required")
            self.ui.assetIdInput.setFocus()
            return False
            
        if not self.ui.descriptionInput.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Asset description is required")
            self.ui.descriptionInput.setFocus()
            return False
            
        if not self.ui.supplierInput.text().strip():
            QMessageBox.warning(self, "Validation Error", "Supplier/Vendor is required")
            self.ui.supplierInput.setFocus()
            return False
            
        if not self.ui.locationCombo.currentText().strip():
            QMessageBox.warning(self, "Validation Error", "Location is required")
            self.ui.locationCombo.setFocus()
            return False
        
        if self.ui.depreciationPercentageSpinBox.value() <= 0:
            QMessageBox.warning(self, "Validation Error", "Annual Depreciation percentage must be greater than 0%")
            self.ui.depreciationPercentageSpinBox.setFocus()
            return False
            
        return True
    
    def save_asset(self) -> bool:
        """Save the asset (create new or update existing)"""
        try:
            asset_data = self.get_data()
            
            if self.asset:  # Editing existing asset
                asset_id = self.asset.get('id') if isinstance(self.asset, dict) else getattr(self.asset, 'id', None)
                result = self.asset_service.update_asset(asset_id, asset_data)
            else:  # Creating new asset
                result = self.asset_service.create_asset(asset_data)
            
            if result["success"]:
                QMessageBox.information(
                    self, 
                    "Success", 
                    result["message"]
                )
                return True
            else:
                QMessageBox.warning(
                    self, 
                    "Error", 
                    result["message"]
                )
                return False
                
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"An error occurred while saving the asset: {str(e)}"
            )
            return False
        
    def get_data(self):
        """Return asset data formatted for database insertion"""
        from ...services.expiry_calculator import ExpiryCalculator
        description = self.ui.descriptionInput.toPlainText().strip()
        
        # Ensure depreciation was calculated
        if not hasattr(self, '_depreciation_data'):
            self.calculate_depreciation()
        
        # Calculate expiry date using Dec 31 depreciation logic - aligned to year end
        acquisition_date = self.ui.acquisitionDateEdit.date().toPython()
        useful_life = self.ui.usefulLifeSpinBox.value()
        expiry_date = ExpiryCalculator.calculate_expiry_date_aligned_to_year_end(
            acquisition_date, useful_life
        )
        
        return {
            "asset_id": self.ui.assetIdInput.text().strip(),
            "description": description,
            "name": description[:100] if description else "",  # Use first 100 chars as name
            "category_id": self.ui.categoryCombo.currentData(),
            "subcategory_id": self.ui.subCategoryCombo.currentData(),
            "acquisition_date": acquisition_date,
            "expiry_date": expiry_date,  # Year-end accounting logic
            "supplier": self.ui.supplierInput.text().strip(),
            "quantity": self.ui.quantitySpinBox.value(),
            "unit_cost": self.ui.unitCostSpinBox.value(),
            "total_cost": float(self.ui.totalCostInput.text().replace(",", "") or "0"),
            "useful_life": self.ui.usefulLifeSpinBox.value(),
            "depreciation_method": self.ui.depreciationMethodCombo.currentText(),
            "depreciation_percentage": self.ui.depreciationPercentageSpinBox.value(),
            "accumulated_depreciation": self._depreciation_data['accumulated_depreciation'],
            "annual_depreciation": self._depreciation_data['annual_depreciation'],
            "salvage_value": self._depreciation_data['salvage_value'],
            "net_book_value": self._depreciation_data['net_book_value'],
            "depreciation_years_applied": 0,  # New assets have not had any depreciation applied yet
            "location": self.ui.locationCombo.currentText().strip(),
            "model_number": self.ui.modelNumberInput.text().strip(),
            "serial_number": self.ui.serialNumberInput.text().strip(),
            "custodian": self.ui.custodianInput.text().strip(),
            "remarks": self.ui.remarksText.toPlainText().strip(),
            "status": AssetStatus.AVAILABLE.value,  # Default status for new assets
            "department": "General"  # Default department - could be made configurable
        }
