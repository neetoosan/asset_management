from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QTableWidgetItem, QAbstractItemView
from PySide6.QtCore import QDate, Slot, Qt
from ..ui.report_screen_ui import Ui_ReportScreen
from ...services.asset_service import AssetService
from ...services.report_service import ReportService
from ...core.models import ReportStatus, ReportFormat
from datetime import datetime
import os
from ...services.export_method import export_csv, export_xlsx, export_pdf, export_docx


class ReportScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ReportScreen()
        self.ui.setupUi(self)
        self.asset_service = AssetService()
        self.report_service = ReportService()
        
        # Set current date as end date
        self.ui.endDateEdit.setDate(QDate.currentDate())
        
        # Set current date as filter end date
        self.ui.filterEndDateEdit.setDate(QDate.currentDate())
        
        # Connect buttons
        self.ui.exportButton.clicked.connect(self.export_report)
        self.ui.filterButton.clicked.connect(self.filter_report_logs)
        self.ui.clearFilterButton.clicked.connect(self.clear_filter_and_reload)
        
        # Initialize and load report logs
        self.setup_report_logs_table()
        self.load_report_logs()
    
    @Slot()
    def export_report(self):
        """Handle export button click - show file save dialog and generate report"""
        try:
            # Get selected report type and format
            report_type = self.ui.reportTypeComboBox.currentText()
            export_format = self.ui.formatComboBox.currentText()
            start_date = self.ui.startDateEdit.date().toPython()
            end_date = self.ui.endDateEdit.date().toPython()
            
            # Determine file extension based on format
            format_extensions = {
                "PDF Document": "pdf",
                "Excel Spreadsheet (.xlsx)": "xlsx", 
                "CSV File": "csv",
                "Word Document (.docx)": "docx"
            }
            
            extension = format_extensions.get(export_format, "pdf")
            
            # Show file save dialog
            suggested_filename = f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Report",
                suggested_filename,
                f"{export_format} (*.{extension});;All Files (*.*)"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Generate and export the report
            self.generate_report(report_type, export_format, start_date, end_date, file_path)
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export report: {str(e)}")
    
    def generate_report(self, report_type, export_format, start_date, end_date, file_path):
        """Generate the actual report based on parameters"""
        records_count = 0
        try:
            # Get assets data based on report type
            if report_type == "All Assets Report":
                assets = self.asset_service.get_all_assets()
                data = self.prepare_all_assets_data(assets)
            elif report_type == "Assets by Category":
                assets = self.asset_service.get_all_assets()
                data = self.prepare_assets_by_category_data(assets)
            elif report_type == "Assets by Department":
                assets = self.asset_service.get_all_assets()
                data = self.prepare_assets_by_department_data(assets)
            elif report_type == "Depreciation Report":
                assets = self.asset_service.get_all_assets()
                data = self.prepare_depreciation_data(assets)
            elif report_type == "Asset Valuation Report":
                assets = self.asset_service.get_all_assets()
                data = self.prepare_valuation_data(assets)
            elif report_type == "Maintenance Schedule":
                assets = self.asset_service.get_all_assets()
                data = self.prepare_maintenance_data(assets)
            else:
                assets = self.asset_service.get_all_assets()
                data = self.prepare_all_assets_data(assets)
            
            # Filter by date range if applicable
            filtered_data = self.filter_by_date_range(data, start_date, end_date)
            
            # Calculate records count
            if isinstance(filtered_data, dict):
                records_count = sum(len(group) for group in filtered_data.values())
            else:
                records_count = len(filtered_data)
            
            # Export based on format
            if export_format == "CSV File":
                self.export_to_csv(filtered_data, file_path, report_type)
            elif export_format == "Excel Spreadsheet (.xlsx)":
                self.export_to_excel(filtered_data, file_path, report_type)
            elif export_format == "PDF Document":
                self.export_to_pdf(filtered_data, file_path, report_type)
            elif export_format == "Word Document (.docx)":
                self.export_to_docx(filtered_data, file_path, report_type)
            
            # Log successful report generation
            self.log_report_generation(
                report_type, export_format, start_date, end_date,
                file_path, file_path, records_count, ReportStatus.SUCCESS
            )
            
            QMessageBox.information(self, "Export Successful", 
                                  f"Report exported successfully to:\n{file_path}")
            
        except Exception as e:
            # Log failed report generation
            self.log_report_generation(
                report_type, export_format, start_date, end_date,
                file_path, file_path, records_count, ReportStatus.FAILED
            )
            raise Exception(f"Report generation failed: {str(e)}")
    
    def prepare_all_assets_data(self, assets):
        """Prepare data for all assets report with depreciation fields"""
        from ...services.expiry_calculator import ExpiryCalculator
        data = []
        for asset in assets:
            # support both dicts (service) and ORM objects (legacy callers)
            aid = asset.get('asset_id') if isinstance(asset, dict) else getattr(asset, 'asset_id', '')
            name = asset.get('name') if isinstance(asset, dict) else getattr(asset, 'name', '')
            category = asset.get('category_name') or asset.get('category') if isinstance(asset, dict) else (asset.category.name if getattr(asset, 'category', None) else 'Unknown')
            department = asset.get('department') if isinstance(asset, dict) else getattr(asset, 'department', None)
            acq = asset.get('acquisition_date') if isinstance(asset, dict) else getattr(asset, 'acquisition_date', None)
            # normalize date
            acq_str = ''
            acq_date = None
            if acq:
                try:
                    if isinstance(acq, str):
                        acq_dt = datetime.fromisoformat(acq)
                    else:
                        acq_dt = acq
                    acq_date = acq_dt.date() if isinstance(acq_dt, datetime) else acq_dt
                    acq_str = acq_date.strftime('%Y-%m-%d')
                except Exception:
                    acq_str = str(acq)

            total_cost = float(asset.get('total_cost') or 0) if isinstance(asset, dict) else float(getattr(asset, 'total_cost', 0) or 0)
            useful_life = asset.get('useful_life') if isinstance(asset, dict) else getattr(asset, 'useful_life', 0)
            depreciation_pct = asset.get('depreciation_percentage') if isinstance(asset, dict) else getattr(asset, 'depreciation_percentage', 0) or 0
            status = asset.get('status') if isinstance(asset, dict) else (getattr(asset, 'status').value if getattr(asset, 'status', None) else 'Unknown')
            model = asset.get('model_number') if isinstance(asset, dict) else getattr(asset, 'model_number', '')
            serial = asset.get('serial_number') if isinstance(asset, dict) else getattr(asset, 'serial_number', '')
            
            # Calculate remaining useful life using Dec 31 logic
            remaining_life = useful_life
            if acq_date and useful_life:
                try:
                    remaining_life = ExpiryCalculator.calculate_remaining_useful_life(useful_life, acq_date)
                except Exception:
                    remaining_life = useful_life

            data.append({
                'Asset ID': aid,
                'Name': name,
                'Model Number': model or '',
                'Serial Number': serial or '',
                'Category': category or 'Unknown',
                'Department': department or 'Not Assigned',
                'Acquisition Date': acq_str,
                'Total Cost': total_cost,
                'Useful Life (Years)': useful_life or 0,
                'Remaining Life (Years)': remaining_life or 0,
                'Depreciation %': float(depreciation_pct) or 0,
                'Status': status or 'Unknown'
            })
        return data
    
    def prepare_assets_by_category_data(self, assets):
        """Prepare data grouped by category"""
        category_data = {}
        for asset in assets:
            if isinstance(asset, dict):
                category = asset.get('category_name') or asset.get('category') or 'Unknown'
                acq = asset.get('acquisition_date')
                try:
                    if acq:
                        acq_str = datetime.fromisoformat(acq).strftime('%Y-%m-%d') if isinstance(acq, str) else acq.strftime('%Y-%m-%d')
                    else:
                        acq_str = ''
                except Exception:
                    acq_str = str(acq) if acq else ''

                entry = {
                    'Asset ID': asset.get('asset_id'),
                    'Name': asset.get('name'),
                    'Model Number': asset.get('model_number') or '',
                    'Serial Number': asset.get('serial_number') or '',
                    'Department': asset.get('department') or 'Not Assigned',
                    'Acquisition Date': acq_str,
                    'Total Cost': float(asset.get('total_cost') or 0),
                    'Status': asset.get('status') or 'Unknown'
                }
            else:
                category = asset.category.name if asset.category else 'Unknown'
                entry = {
                    'Asset ID': asset.asset_id,
                    'Name': asset.name,
                    'Model Number': getattr(asset, 'model_number', '') or '',
                    'Serial Number': getattr(asset, 'serial_number', '') or '',
                    'Department': asset.department or 'Not Assigned',
                    'Acquisition Date': asset.acquisition_date.strftime('%Y-%m-%d') if asset.acquisition_date else '',
                    'Total Cost': float(asset.total_cost or 0),
                    'Status': asset.status.value if asset.status else 'Unknown'
                }

            if category not in category_data:
                category_data[category] = []
            category_data[category].append(entry)
        return category_data
    
    def prepare_assets_by_department_data(self, assets):
        """Prepare data grouped by department"""
        dept_data = {}
        for asset in assets:
            if isinstance(asset, dict):
                dept = asset.get('department') or 'Not Assigned'
                category = asset.get('category_name') or asset.get('category') or 'Unknown'
                acq = asset.get('acquisition_date')
                try:
                    if acq:
                        acq_str = datetime.fromisoformat(acq).strftime('%Y-%m-%d') if isinstance(acq, str) else acq.strftime('%Y-%m-%d')
                    else:
                        acq_str = ''
                except Exception:
                    acq_str = str(acq) if acq else ''

                entry = {
                    'Asset ID': asset.get('asset_id'),
                    'Name': asset.get('name'),
                    'Model Number': asset.get('model_number') or '',
                    'Serial Number': asset.get('serial_number') or '',
                    'Category': category,
                    'Acquisition Date': acq_str,
                    'Total Cost': float(asset.get('total_cost') or 0),
                    'Status': asset.get('status') or 'Unknown'
                }
            else:
                dept = asset.department or 'Not Assigned'
                entry = {
                    'Asset ID': asset.asset_id,
                    'Name': asset.name,
                    'Model Number': getattr(asset, 'model_number', '') or '',
                    'Serial Number': getattr(asset, 'serial_number', '') or '',
                    'Category': asset.category.name if asset.category else 'Unknown',
                    'Acquisition Date': asset.acquisition_date.strftime('%Y-%m-%d') if asset.acquisition_date else '',
                    'Total Cost': float(asset.total_cost or 0),
                    'Status': asset.status.value if asset.status else 'Unknown'
                }

            if dept not in dept_data:
                dept_data[dept] = []
            dept_data[dept].append(entry)
        return dept_data
    
    def prepare_depreciation_data(self, assets):
        """Prepare depreciation report data"""
        data = []
        for asset in assets:
            # Support dict or ORM
            total_cost = asset.get('total_cost') if isinstance(asset, dict) else getattr(asset, 'total_cost', None)
            useful_life = asset.get('useful_life') if isinstance(asset, dict) else getattr(asset, 'useful_life', None)
            acq = asset.get('acquisition_date') if isinstance(asset, dict) else getattr(asset, 'acquisition_date', None)

            if acq and total_cost and useful_life:
                try:
                    # normalize acquisition date
                    if isinstance(acq, str):
                        acq_date = datetime.fromisoformat(acq).date()
                    else:
                        acq_date = acq if isinstance(acq, datetime) else acq
                        acq_date = acq_date.date() if isinstance(acq_date, datetime) else acq_date

                    annual_depreciation = float(total_cost) / float(useful_life)
                    years_owned = (datetime.now().date() - acq_date).days / 365.25
                    accumulated_depreciation = min(annual_depreciation * years_owned, float(total_cost))
                    book_value = float(total_cost) - accumulated_depreciation

                    data.append({
                        'Asset ID': asset.get('asset_id') if isinstance(asset, dict) else getattr(asset, 'asset_id', ''),
                        'Name': asset.get('name') if isinstance(asset, dict) else getattr(asset, 'name', ''),
                        'Model Number': asset.get('model_number') if isinstance(asset, dict) else getattr(asset, 'model_number', '') or '',
                        'Serial Number': asset.get('serial_number') if isinstance(asset, dict) else getattr(asset, 'serial_number', '') or '',
                        'Original Cost': float(total_cost),
                        'Useful Life': useful_life,
                        'Annual Depreciation': round(annual_depreciation, 2),
                        'Accumulated Depreciation': round(accumulated_depreciation, 2),
                        'Book Value': round(book_value, 2),
                        'Years Owned': round(years_owned, 2)
                    })
                except Exception:
                    # skip problematic records
                    continue
        return data
    
    def prepare_valuation_data(self, assets):
        """Prepare asset valuation report data"""
        data = []
        total_original_cost = 0
        total_book_value = 0
        
        for asset in assets:
            # Support dict or ORM asset
            original_cost = float(asset.get('total_cost') or 0) if isinstance(asset, dict) else float(getattr(asset, 'total_cost', 0) or 0)
            acq = asset.get('acquisition_date') if isinstance(asset, dict) else getattr(asset, 'acquisition_date', None)
            useful_life = asset.get('useful_life') if isinstance(asset, dict) else getattr(asset, 'useful_life', None)
            book_value = original_cost

            if acq and useful_life and original_cost > 0:
                try:
                    if isinstance(acq, str):
                        acq_date = datetime.fromisoformat(acq).date()
                    else:
                        acq_date = acq if isinstance(acq, datetime) else acq
                        acq_date = acq_date.date() if isinstance(acq_date, datetime) else acq_date

                    years_owned = (datetime.now().date() - acq_date).days / 365.25
                    annual_depreciation = original_cost / float(useful_life)
                    accumulated_depreciation = min(annual_depreciation * years_owned, original_cost)
                    book_value = original_cost - accumulated_depreciation
                except Exception:
                    book_value = original_cost

            total_original_cost += original_cost
            total_book_value += book_value

            category = asset.get('category_name') or asset.get('category') if isinstance(asset, dict) else (asset.category.name if getattr(asset, 'category', None) else 'Unknown')
            data.append({
                'Asset ID': asset.get('asset_id') if isinstance(asset, dict) else getattr(asset, 'asset_id', ''),
                'Name': asset.get('name') if isinstance(asset, dict) else getattr(asset, 'name', ''),
                'Model Number': asset.get('model_number') if isinstance(asset, dict) else getattr(asset, 'model_number', '') or '',
                'Serial Number': asset.get('serial_number') if isinstance(asset, dict) else getattr(asset, 'serial_number', '') or '',
                'Category': category or 'Unknown',
                'Original Cost': original_cost,
                'Current Book Value': round(book_value, 2),
                'Depreciation': round(original_cost - book_value, 2)
            })
        
        # Add summary
        data.append({
            'Asset ID': 'TOTAL',
            'Name': 'Summary',
            'Category': '',
            'Original Cost': round(total_original_cost, 2),
            'Current Book Value': round(total_book_value, 2),
            'Depreciation': round(total_original_cost - total_book_value, 2)
        })
        
        return data
    
    def prepare_maintenance_data(self, assets):
        """Prepare maintenance schedule data"""
        # This is a placeholder - in a real system, you'd have maintenance records
        data = []
        for asset in assets:
            if isinstance(asset, dict):
                category = asset.get('category_name') or asset.get('category') or 'Unknown'
                status = asset.get('status') or 'Unknown'
                aid = asset.get('asset_id')
                name = asset.get('name')
            else:
                category = asset.category.name if asset.category else 'Unknown'
                status = asset.status.value if asset.status else 'Unknown'
                aid = getattr(asset, 'asset_id', '')
                name = getattr(asset, 'name', '')
            # Model and Serial may come from dict or ORM
            model = asset.get('model_number') if isinstance(asset, dict) else getattr(asset, 'model_number', '')
            serial = asset.get('serial_number') if isinstance(asset, dict) else getattr(asset, 'serial_number', '')

            data.append({
                'Asset ID': aid,
                'Name': name,
                'Model Number': model or '',
                'Serial Number': serial or '',
                'Category': category,
                'Last Maintenance': 'N/A',  # Would come from maintenance records
                'Next Maintenance Due': 'N/A',  # Would be calculated
                'Maintenance Type': 'Routine',
                'Status': status
            })
        return data
    
    def filter_by_date_range(self, data, start_date, end_date):
        """Filter data by date range (simplified implementation)"""
        # For this implementation, we'll return the data as-is
        # In a real scenario, you'd filter based on relevant date fields
        return data
    
    def export_to_csv(self, data, file_path, report_type):
        """Delegate CSV export to export_method.export_csv"""
        export_csv(data, file_path, report_type)
    
    def export_to_excel(self, data, file_path, report_type):
        """Delegate Excel export to export_method.export_xlsx"""
        try:
            export_xlsx(data, file_path, report_type)
        except Exception as e:
            QMessageBox.warning(self, "Excel Export", f"Excel export failed: {e}")
    
    def export_to_pdf(self, data, file_path, report_type):
        """Delegate PDF export to export_method.export_pdf"""
        try:
            export_pdf(data, file_path, report_type)
        except Exception as e:
            QMessageBox.warning(self, "PDF Export", f"PDF export failed: {e}")
    
    def export_to_docx(self, data, file_path, report_type):
        """Delegate DOCX export to export_method.export_docx"""
        try:
            export_docx(data, file_path, report_type)
        except Exception as e:
            QMessageBox.warning(self, "Word Export", f"Word export failed: {e}")
    
    def setup_report_logs_table(self):
        """Set up the report logs table columns and properties"""
        # Set column widths
        self.ui.reportLogsTable.setColumnWidth(0, 150)  # Date & Time
        self.ui.reportLogsTable.setColumnWidth(1, 180)  # Report Type
        self.ui.reportLogsTable.setColumnWidth(2, 100)  # Format
        self.ui.reportLogsTable.setColumnWidth(3, 200)  # File Name
        self.ui.reportLogsTable.setColumnWidth(4, 100)  # Status
        self.ui.reportLogsTable.setColumnWidth(5, 100)  # Records Count
        
        # Enable sorting
        self.ui.reportLogsTable.setSortingEnabled(True)
        
        # Set selection behavior
        self.ui.reportLogsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
    
    def load_report_logs(self, logs=None):
        """Load report logs into the table"""
        try:
            if logs is None:
                logs = self.report_service.get_all_report_logs()
            
            self.ui.reportLogsTable.setRowCount(len(logs))
            
            for row, log in enumerate(logs):
                # Date & Time
                date_time = log.generated_at.strftime('%Y-%m-%d %H:%M:%S') if log.generated_at else 'N/A'
                self.ui.reportLogsTable.setItem(row, 0, QTableWidgetItem(date_time))
                
                # Report Type
                self.ui.reportLogsTable.setItem(row, 1, QTableWidgetItem(log.report_type or 'Unknown'))
                
                # Format
                format_text = log.report_format.value if log.report_format else 'Unknown'
                self.ui.reportLogsTable.setItem(row, 2, QTableWidgetItem(format_text))
                
                # File Name
                self.ui.reportLogsTable.setItem(row, 3, QTableWidgetItem(log.file_name or 'N/A'))
                
                # Status
                status_text = log.status.value if log.status else 'Unknown'
                status_item = QTableWidgetItem(status_text)
                
                # Color code status
                if log.status == ReportStatus.SUCCESS:
                    status_item.setForeground(Qt.darkGreen)
                elif log.status == ReportStatus.FAILED:
                    status_item.setForeground(Qt.red)
                elif log.status == ReportStatus.IN_PROGRESS:
                    status_item.setForeground(Qt.blue)
                
                self.ui.reportLogsTable.setItem(row, 4, status_item)
                
                # Records Count
                self.ui.reportLogsTable.setItem(row, 5, QTableWidgetItem(str(log.records_count or 0)))
            
            # Sort by date (newest first)
            self.ui.reportLogsTable.sortItems(0, Qt.DescendingOrder)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load report logs: {str(e)}")
    
    @Slot()
    def filter_report_logs(self):
        """Filter report logs based on date range"""
        try:
            start_date = self.ui.filterStartDateEdit.date().toPython()
            end_date = self.ui.filterEndDateEdit.date().toPython()
            
            # Get filtered logs
            filtered_logs = self.report_service.get_report_logs_filtered(
                start_date=start_date,
                end_date=end_date
            )
            
            # Load filtered logs into table
            self.load_report_logs(filtered_logs)
            
        except Exception as e:
            QMessageBox.warning(self, "Filter Error", f"Failed to filter report logs: {str(e)}")
    
    @Slot()
    def clear_filter_and_reload(self):
        """Clear filters and reload all report logs"""
        # Reset filter dates
        self.ui.filterStartDateEdit.setDate(QDate(2024, 1, 1))
        self.ui.filterEndDateEdit.setDate(QDate.currentDate())
        
        # Reload all logs
        self.load_report_logs()
    
    def log_report_generation(self, report_type, export_format, start_date, end_date, 
                            file_name, file_path, records_count, status=ReportStatus.SUCCESS):
        """Log a report generation event"""
        try:
            report_data = {
                'report_type': report_type,
                'export_format': export_format,
                'file_name': os.path.basename(file_name),
                'file_path': file_path,
                'start_date': start_date,
                'end_date': end_date,
                'records_count': records_count
            }
            
            # Create report log
            report_log = self.report_service.create_report_log(report_data, user_id=1)  # TODO: Get actual user ID
            
            # Update status
            self.report_service.update_report_log_status(report_log.id, status, records_count)
            
            # Refresh the logs table
            self.load_report_logs()
            
        except Exception as e:
            print(f"Failed to log report generation: {str(e)}")
