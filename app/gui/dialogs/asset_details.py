from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
import json
import os
from datetime import date

from ..ui.asset_details_ui import Ui_AssetDetails
from ...services.asset_service import AssetService
from ...services.expiry_calculator import ExpiryCalculator

try:
    import qrcode
except Exception:
    qrcode = None


class AssetDetailsDialog(QDialog):
    """Dialog that shows full asset details and allows saving a QR code containing asset info."""
    def __init__(self, asset_id: int, parent=None):
        super().__init__(parent)
        self.ui = Ui_AssetDetails()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.asset_id = asset_id
        self.asset_service = AssetService()

        # Load asset
        self.asset = None
        self.load_asset()

        # Connect QR button
        self.ui.qrButton.clicked.connect(self.on_qr_clicked)

    def load_asset(self):
        try:
            data = self.asset_service.get_asset_by_id(self.asset_id)
            if not data:
                QMessageBox.warning(self, "Not found", "Asset not found")
                self.reject()
                return
            self.asset = data
            # Populate fields
            self.ui.nameLabel.setText(str(data.get('name') or '-'))
            self.ui.assetIdLabel.setText(str(data.get('asset_id') or '-'))
            self.ui.categoryLabel.setText(str(data.get('category_name') or '-'))
            self.ui.departmentLabel.setText(str(data.get('department') or '-'))
            self.ui.statusLabel.setText(str(data.get('status') or '-'))
            self.ui.acqDateLabel.setText(str(data.get('acquisition_date') or '-'))
            
            # Display expiry_date calculated using Dec 31 logic
            acq_date = data.get('acquisition_date')
            useful_life = data.get('useful_life')
            if acq_date and useful_life:
                try:
                    # Parse acquisition_date if string
                    if isinstance(acq_date, str):
                        acq_date_obj = date.fromisoformat(acq_date.split('T')[0]) if 'T' in acq_date else date.fromisoformat(acq_date)
                    else:
                        acq_date_obj = acq_date
                    
                    # Calculate expiry using Dec 31 logic
                    expiry_calculated = ExpiryCalculator.calculate_expiry_date(acq_date_obj, useful_life)
                    expiry_date_display = expiry_calculated.strftime('%Y-%m-%d')
                except Exception:
                    expiry_date_display = data.get('expiry_date') or data.get('exp_date') or '-'
            else:
                expiry_date_display = data.get('expiry_date') or data.get('exp_date') or '-'
            
            # Display "End of Useful Life" date instead of expiry date
            self.ui.expDateLabel.setText(str(expiry_date_display))
            
            # Display useful life
            useful_life = data.get('useful_life')
            self.ui.usefulLifeLabel.setText(str(useful_life or '-'))
            
            # Display remaining useful life (using Dec 31 logic)
            acq_date = data.get('acquisition_date')
            if acq_date and useful_life:
                try:
                    # Parse acquisition_date if it's a string
                    if isinstance(acq_date, str):
                        acq_date_obj = date.fromisoformat(acq_date.split('T')[0]) if 'T' in acq_date else date.fromisoformat(acq_date)
                    else:
                        acq_date_obj = acq_date
                    
                    remaining = ExpiryCalculator.calculate_remaining_useful_life(useful_life, acq_date_obj)
                    remaining_str = f"{remaining:.1f} years" if remaining > 0 else "End of useful life reached"
                except Exception:
                    remaining_str = '-'
            else:
                remaining_str = '-'
            
            if hasattr(self.ui, 'remainingLifeLabel'):
                self.ui.remainingLifeLabel.setText(remaining_str)
            
            # Display depreciation method
            dep_method = data.get('depreciation_method')
            self.ui.depMethodLabel.setText(str(dep_method or '-'))
            
            # Display depreciation percentage
            dep_percent = data.get('depreciation_percentage')
            try:
                dep_percent_str = f"{float(dep_percent):.2f}%" if dep_percent is not None else '-'
            except Exception:
                dep_percent_str = str(dep_percent or '-')
            self.ui.depPercentLabel.setText(dep_percent_str)
            
            # Display accumulated depreciation
            accum_dep = data.get('accumulated_depreciation')
            try:
                accum_dep_str = f"₦{float(accum_dep):,.2f}" if accum_dep is not None else '-'
            except Exception:
                accum_dep_str = str(accum_dep or '-')
            self.ui.accumDepLabel.setText(accum_dep_str)
            
            # Display net book value
            value = data.get('net_book_value') if data.get('net_book_value') is not None else data.get('total_cost')
            try:
                value_str = f"₦{float(value):,.2f}" if value is not None else '-'
            except Exception:
                value_str = str(value)
            self.ui.valueLabel.setText(value_str)
            
            desc = data.get('description') or ''
            self.ui.descriptionText.setPlainText(desc)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load asset: {e}")
            self.reject()

    def on_qr_clicked(self):
        if not self.asset:
            QMessageBox.warning(self, "No asset", "No asset loaded")
            return

        payload = {
                'id': self.asset.get('id') if isinstance(self.asset, dict) else getattr(self.asset, 'id', None),
                'asset_id': self.asset.get('asset_id') if isinstance(self.asset, dict) else getattr(self.asset, 'asset_id', None),
                'name': self.asset.get('name') if isinstance(self.asset, dict) else getattr(self.asset, 'name', None),
                'model_number': self.asset.get('model_number') if isinstance(self.asset, dict) else getattr(self.asset, 'model_number', None),
                'serial_number': self.asset.get('serial_number') if isinstance(self.asset, dict) else getattr(self.asset, 'serial_number', None),
                'category': self.asset.get('category_name') if isinstance(self.asset, dict) else getattr(self.asset, 'category_name', None),
                'department': self.asset.get('department') if isinstance(self.asset, dict) else getattr(self.asset, 'department', None),
                'status': self.asset.get('status') if isinstance(self.asset, dict) else getattr(self.asset, 'status', None),
                'acquisition_date': self.asset.get('acquisition_date') if isinstance(self.asset, dict) else getattr(self.asset, 'acquisition_date', None),
                'expiry_date': self.asset.get('expiry_date') if isinstance(self.asset, dict) else getattr(self.asset, 'expiry_date', None),
                'useful_life': self.asset.get('useful_life') if isinstance(self.asset, dict) else getattr(self.asset, 'useful_life', None),
                'depreciation_method': self.asset.get('depreciation_method') if isinstance(self.asset, dict) else getattr(self.asset, 'depreciation_method', None),
                'depreciation_percentage': self.asset.get('depreciation_percentage') if isinstance(self.asset, dict) else getattr(self.asset, 'depreciation_percentage', None),
                'accumulated_depreciation': self.asset.get('accumulated_depreciation') if isinstance(self.asset, dict) else getattr(self.asset, 'accumulated_depreciation', None),
                'net_book_value': self.asset.get('net_book_value') if isinstance(self.asset, dict) else getattr(self.asset, 'net_book_value', None),
                'value': self.asset.get('total_cost') if isinstance(self.asset, dict) else getattr(self.asset, 'total_cost', None),
        }

        # Create JSON representation
        try:
            data_json = json.dumps(payload, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to prepare QR payload: {e}")
            return

        # Ask where to save
        default_name = f"asset_{self.asset.get('asset_id') or self.asset.get('id')}.png"
        path, _ = QFileDialog.getSaveFileName(self, "Save QR code", default_name, "PNG Files (*.png);;All Files (*)")
        if not path:
            return

        # If qrcode is available, generate an image
        if qrcode is not None:
            try:
                img = qrcode.make(data_json)
                # Ensure filename has .png
                if not os.path.splitext(path)[1]:
                    path = path + '.png'
                img.save(path)
                QMessageBox.information(self, "Saved", f"QR code saved to {path}")
                return
            except Exception as e:
                QMessageBox.warning(self, "QR generation failed", f"Failed to generate QR image: {e}\nFalling back to saving JSON.")

        # Fallback: save JSON text file
        try:
            if not os.path.splitext(path)[1]:
                path = path + '.json'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data_json)
            QMessageBox.information(self, "Saved", f"Asset JSON saved to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Save failed", f"Failed to save QR/JSON: {e}")
