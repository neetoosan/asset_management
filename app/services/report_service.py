import os
import csv
import json
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Tuple
from decimal import Decimal
import io
import tempfile

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import xlsxwriter
    XLSXWRITER_AVAILABLE = True
except ImportError:
    XLSXWRITER_AVAILABLE = False

from sqlalchemy import func, and_, or_, desc
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.models import (
    Asset, AssetCategory, AssetSubCategory, User, ReportLog,
    AssetStatus, ReportFormat, ReportStatus, DepreciationMethod
)
from .audit_service import AuditService


class ReportService:
    def __init__(self):
        self.audit_service = AuditService()
    
    def get_db_session(self):
        """Get database session (legacy method for compatibility)"""
        from ..core.database import get_db_session
        return get_db_session()
    
    def generate_asset_summary_report(self, filters: Dict[str, Any] = None, 
                                    format_type: str = "dict") -> Dict[str, Any]:
        """Generate comprehensive asset summary report."""
        try:
            with get_db() as session:
                query = session.query(Asset)
                
                # Apply filters
                if filters:
                    if filters.get('category_id'):
                        query = query.filter(Asset.category_id == filters['category_id'])
                    
                    if filters.get('status'):
                        query = query.filter(Asset.status == filters['status'])
                    
                    if filters.get('date_from'):
                        query = query.filter(Asset.acquisition_date >= filters['date_from'])
                    
                    if filters.get('date_to'):
                        query = query.filter(Asset.acquisition_date <= filters['date_to'])
                    
                    if filters.get('department'):
                        query = query.filter(Asset.department == filters['department'])
                    
                    if filters.get('location'):
                        query = query.filter(Asset.location.like(f"%{filters['location']}%"))

                assets = query.all()
                
                # Calculate summary statistics
                total_assets = len(assets)
                total_value = sum(float(asset.total_cost or 0) for asset in assets)
                total_depreciated_value = sum(float(asset.accumulated_depreciation or 0) for asset in assets)
                net_book_value = total_value - total_depreciated_value
                
                # Status breakdown
                status_counts = {}
                for status in AssetStatus:
                    count = len([a for a in assets if a.status == status])
                    status_counts[status.value] = count
                
                # Category breakdown
                category_summary = {}
                categories = session.query(AssetCategory).all()
                for category in categories:
                    category_assets = [a for a in assets if a.category_id == category.id]
                    category_value = sum(float(asset.total_cost or 0) for asset in category_assets)
                    category_summary[category.name] = {
                        'count': len(category_assets),
                        'value': category_value,
                        'percentage': (category_value / total_value * 100) if total_value > 0 else 0
                    }
                
                # Department breakdown
                department_summary = {}
                departments = set(asset.department for asset in assets if asset.department)
                for dept in departments:
                    dept_assets = [a for a in assets if a.department == dept]
                    dept_value = sum(float(asset.total_cost or 0) for asset in dept_assets)
                    department_summary[dept] = {
                        'count': len(dept_assets),
                        'value': dept_value,
                        'percentage': (dept_value / total_value * 100) if total_value > 0 else 0
                    }
                
                # Age analysis
                today = date.today()
                age_ranges = {
                    '0-1 years': 0,
                    '1-3 years': 0,
                    '3-5 years': 0,
                    '5+ years': 0
                }
                
                for asset in assets:
                    if asset.acquisition_date:
                        age_years = (today - asset.acquisition_date).days / 365.25
                        if age_years <= 1:
                            age_ranges['0-1 years'] += 1
                        elif age_years <= 3:
                            age_ranges['1-3 years'] += 1
                        elif age_years <= 5:
                            age_ranges['3-5 years'] += 1
                        else:
                            age_ranges['5+ years'] += 1

                report_data = {
                    'report_type': 'Asset Summary Report',
                    'generated_at': datetime.utcnow().isoformat(),
                    'filters_applied': filters or {},
                    'summary': {
                        'total_assets': total_assets,
                        'total_value': total_value,
                        'total_depreciated_value': total_depreciated_value,
                        'net_book_value': net_book_value,
                        'average_asset_value': total_value / total_assets if total_assets > 0 else 0
                    },
                    'status_breakdown': status_counts,
                    'category_breakdown': category_summary,
                    'department_breakdown': department_summary,
                    'age_analysis': age_ranges
                }
                
                if format_type == "dict":
                    return {
                        "success": True,
                        "data": report_data,
                        "record_count": total_assets
                    }
                
                return report_data
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    def generate_depreciation_report(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate depreciation analysis report."""
        try:
            with get_db() as session:
                query = session.query(Asset).filter(
                    Asset.depreciation_method.isnot(None),
                    Asset.useful_life.isnot(None)
                )
                
                if filters:
                    if filters.get('category_id'):
                        query = query.filter(Asset.category_id == filters['category_id'])
                    
                    if filters.get('date_from'):
                        query = query.filter(Asset.acquisition_date >= filters['date_from'])
                    
                    if filters.get('date_to'):
                        query = query.filter(Asset.acquisition_date <= filters['date_to'])

                assets = query.all()
                
                # Calculate current depreciation for each asset
                current_year = datetime.now().year
                depreciation_data = []
                
                total_original_value = 0
                total_accumulated_depreciation = 0
                total_current_book_value = 0
                
                for asset in assets:
                    if asset.acquisition_date and asset.useful_life and asset.total_cost:
                        years_owned = (datetime.now().date() - asset.acquisition_date).days / 365.25
                        current_year_depreciation = min(int(years_owned) + 1, asset.useful_life)
                        
                        try:
                            annual_dep, accumulated_dep, book_value = DepreciationMethod.calculate_depreciation(
                                method=asset.depreciation_method.value,
                                total_cost=float(asset.total_cost),
                                useful_life=asset.useful_life,
                                current_year=current_year_depreciation
                            )
                            
                            asset_data = {
                                'asset_id': asset.asset_id,
                                'name': asset.name,
                                'category': asset.category.name if asset.category else 'Unknown',
                                'original_value': float(asset.total_cost),
                                'depreciation_method': asset.depreciation_method.value,
                                'useful_life': asset.useful_life,
                                'years_owned': round(years_owned, 1),
                                'annual_depreciation': annual_dep,
                                'accumulated_depreciation': accumulated_dep,
                                'current_book_value': book_value,
                                'depreciation_percentage': (accumulated_dep / float(asset.total_cost) * 100) if asset.total_cost > 0 else 0
                            }
                            
                            depreciation_data.append(asset_data)
                            total_original_value += float(asset.total_cost)
                            total_accumulated_depreciation += accumulated_dep
                            total_current_book_value += book_value
                            
                        except Exception as e:
                            print(f"Error calculating depreciation for asset {asset.asset_id}: {e}")
                
                # Method breakdown
                method_summary = {}
                for method in DepreciationMethod:
                    method_assets = [a for a in depreciation_data if a['depreciation_method'] == method.value]
                    if method_assets:
                        method_value = sum(a['original_value'] for a in method_assets)
                        method_summary[method.value] = {
                            'count': len(method_assets),
                            'original_value': method_value,
                            'accumulated_depreciation': sum(a['accumulated_depreciation'] for a in method_assets),
                            'current_book_value': sum(a['current_book_value'] for a in method_assets)
                        }

                report_data = {
                    'report_type': 'Depreciation Analysis Report',
                    'generated_at': datetime.utcnow().isoformat(),
                    'filters_applied': filters or {},
                    'summary': {
                        'total_depreciable_assets': len(depreciation_data),
                        'total_original_value': total_original_value,
                        'total_accumulated_depreciation': total_accumulated_depreciation,
                        'total_current_book_value': total_current_book_value,
                        'overall_depreciation_percentage': (total_accumulated_depreciation / total_original_value * 100) if total_original_value > 0 else 0
                    },
                    'method_breakdown': method_summary,
                    'asset_details': depreciation_data
                }
                
                return {
                    "success": True,
                    "data": report_data,
                    "record_count": len(depreciation_data)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def create_report_log(self, report_data: dict, user_id: Optional[int] = None) -> ReportLog:
        """Create a new report log entry"""
        db = self.get_db_session()
        try:
            # Map format string to enum
            format_mapping = {
                "PDF Document": ReportFormat.PDF,
                "Excel Spreadsheet (.xlsx)": ReportFormat.EXCEL,
                "CSV File": ReportFormat.CSV,
                "Word Document (.docx)": ReportFormat.WORD
            }
            
            report_log = ReportLog(
                report_type=report_data.get('report_type'),
                report_format=format_mapping.get(report_data.get('export_format'), ReportFormat.CSV),
                file_name=report_data.get('file_name'),
                file_path=report_data.get('file_path'),
                date_range_start=report_data.get('start_date'),
                date_range_end=report_data.get('end_date'),
                records_count=report_data.get('records_count', 0),
                generated_by_id=user_id,
                status=ReportStatus.IN_PROGRESS
            )
            
            db.add(report_log)
            db.commit()
            db.refresh(report_log)
            return report_log
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def update_report_log_status(self, report_log_id: int, status: ReportStatus, 
                                records_count: int = None, error_message: str = None):
        """Update report log status and completion details"""
        db = self.get_db_session()
        try:
            report_log = db.query(ReportLog).filter(ReportLog.id == report_log_id).first()
            if report_log:
                report_log.status = status
                report_log.completed_at = datetime.utcnow()
                
                if records_count is not None:
                    report_log.records_count = records_count
                
                if error_message:
                    report_log.error_message = error_message
                
                db.commit()
                db.refresh(report_log)
                return report_log
            return None
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_all_report_logs(self) -> List[ReportLog]:
        """Get all report logs with user information"""
        db = self.get_db_session()
        try:
            return db.query(ReportLog).order_by(ReportLog.generated_at.desc()).all()
        finally:
            db.close()
    
    def get_report_logs_by_date_range(self, start_date: date, end_date: date) -> List[ReportLog]:
        """Get report logs filtered by date range"""
        db = self.get_db_session()
        try:
            return db.query(ReportLog).filter(
                ReportLog.generated_at >= datetime.combine(start_date, datetime.min.time()),
                ReportLog.generated_at <= datetime.combine(end_date, datetime.max.time())
            ).order_by(ReportLog.generated_at.desc()).all()
        finally:
            db.close()
    
    def get_report_logs_by_type(self, report_type: str) -> List[ReportLog]:
        """Get report logs filtered by report type"""
        db = self.get_db_session()
        try:
            return db.query(ReportLog).filter(
                ReportLog.report_type == report_type
            ).order_by(ReportLog.generated_at.desc()).all()
        finally:
            db.close()
    
    def get_report_logs_by_user(self, user_id: int) -> List[ReportLog]:
        """Get report logs for a specific user"""
        db = self.get_db_session()
        try:
            return db.query(ReportLog).filter(
                ReportLog.generated_by_id == user_id
            ).order_by(ReportLog.generated_at.desc()).all()
        finally:
            db.close()
    
    def get_report_logs_filtered(self, start_date: Optional[date] = None, 
                                end_date: Optional[date] = None, 
                                report_type: Optional[str] = None,
                                status: Optional[ReportStatus] = None) -> List[ReportLog]:
        """Get report logs with multiple filters"""
        db = self.get_db_session()
        try:
            query = db.query(ReportLog)
            
            if start_date:
                query = query.filter(
                    ReportLog.generated_at >= datetime.combine(start_date, datetime.min.time())
                )
            
            if end_date:
                query = query.filter(
                    ReportLog.generated_at <= datetime.combine(end_date, datetime.max.time())
                )
            
            if report_type:
                query = query.filter(ReportLog.report_type == report_type)
            
            if status:
                query = query.filter(ReportLog.status == status)
            
            return query.order_by(ReportLog.generated_at.desc()).all()
        finally:
            db.close()
    
    def delete_report_log(self, report_log_id: int) -> bool:
        """Delete a report log entry"""
        db = self.get_db_session()
        try:
            report_log = db.query(ReportLog).filter(ReportLog.id == report_log_id).first()
            if report_log:
                db.delete(report_log)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_report_statistics(self) -> dict:
        """Get report generation statistics"""
        db = self.get_db_session()
        try:
            total_reports = db.query(ReportLog).count()
            successful_reports = db.query(ReportLog).filter(
                ReportLog.status == ReportStatus.SUCCESS
            ).count()
            failed_reports = db.query(ReportLog).filter(
                ReportLog.status == ReportStatus.FAILED
            ).count()
            in_progress_reports = db.query(ReportLog).filter(
                ReportLog.status == ReportStatus.IN_PROGRESS
            ).count()
            
            return {
                'total': total_reports,
                'successful': successful_reports,
                'failed': failed_reports,
                'in_progress': in_progress_reports,
                'success_rate': (successful_reports / total_reports * 100) if total_reports > 0 else 0
            }
        finally:
            db.close()
    
    def export_report_to_csv(self, report_data: Dict[str, Any], filename: str = None) -> Dict[str, Any]:
        """Export report data to CSV format."""
        try:
            if not filename:
                filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Create temp file
            temp_dir = tempfile.gettempdir()
            filepath = os.path.join(temp_dir, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                if 'asset_details' in report_data.get('data', {}):
                    # Detailed asset report
                    assets = report_data['data']['asset_details']
                    if assets:
                        writer = csv.DictWriter(csvfile, fieldnames=assets[0].keys())
                        writer.writeheader()
                        writer.writerows(assets)
                else:
                    # Summary report
                    writer = csv.writer(csvfile)
                    writer.writerow(['Report Type', report_data.get('data', {}).get('report_type', 'Unknown')])
                    writer.writerow(['Generated At', report_data.get('data', {}).get('generated_at', '')])
                    writer.writerow([])
                    
                    # Summary data
                    summary = report_data.get('data', {}).get('summary', {})
                    writer.writerow(['Summary'])
                    for key, value in summary.items():
                        writer.writerow([key.replace('_', ' ').title(), value])
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def export_report_to_excel(self, report_data: Dict[str, Any], filename: str = None) -> Dict[str, Any]:
        """Export report data to Excel format."""
        if not XLSXWRITER_AVAILABLE:
            return {"success": False, "error": "xlsxwriter not available"}
            
        try:
            if not filename:
                filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            temp_dir = tempfile.gettempdir()
            filepath = os.path.join(temp_dir, filename)
            
            workbook = xlsxwriter.Workbook(filepath)
            
            # Header format
            header_format = workbook.add_format({
                'bold': True,
                'font_size': 14,
                'bg_color': '#4472C4',
                'font_color': 'white'
            })
            
            # Subheader format
            subheader_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D9E2F3'
            })
            
            # Summary worksheet
            summary_ws = workbook.add_worksheet('Summary')
            row = 0
            
            summary_ws.write(row, 0, report_data.get('data', {}).get('report_type', 'Report'), header_format)
            row += 2
            
            summary_ws.write(row, 0, 'Generated At:', subheader_format)
            summary_ws.write(row, 1, report_data.get('data', {}).get('generated_at', ''))
            row += 2
            
            # Summary statistics
            summary = report_data.get('data', {}).get('summary', {})
            if summary:
                summary_ws.write(row, 0, 'Summary Statistics', subheader_format)
                row += 1
                for key, value in summary.items():
                    summary_ws.write(row, 0, key.replace('_', ' ').title())
                    summary_ws.write(row, 1, value)
                    row += 1
            
            # If detailed data exists, create separate worksheet
            if 'asset_details' in report_data.get('data', {}):
                details_ws = workbook.add_worksheet('Asset Details')
                assets = report_data['data']['asset_details']
                
                if assets:
                    headers = list(assets[0].keys())
                    for col, header in enumerate(headers):
                        details_ws.write(0, col, header.replace('_', ' ').title(), subheader_format)
                    
                    for row, asset in enumerate(assets, 1):
                        for col, header in enumerate(headers):
                            details_ws.write(row, col, asset.get(header, ''))
            
            workbook.close()
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def log_report_generation(self, report_type: str, format_type: str, 
                            filename: str, record_count: int, 
                            generated_by_id: int, filters: Dict = None) -> bool:
        """Log report generation to database."""
        try:
            with get_db() as session:
                report_log = ReportLog(
                    report_type=report_type,
                    report_format=ReportFormat(format_type.upper()),
                    file_name=filename,
                    records_count=record_count,
                    status=ReportStatus.SUCCESS,
                    generated_by_id=generated_by_id,
                    completed_at=datetime.utcnow()
                )
                
                if filters:
                    report_log.date_range_start = filters.get('date_from')
                    report_log.date_range_end = filters.get('date_to')
                
                session.add(report_log)
                session.commit()
                
                # Log audit trail
                user = session.query(User).filter(User.id == generated_by_id).first()
                self.audit_service.log_action(
                    action="REPORT_GENERATED",
                    description=f"Generated {report_type} report in {format_type} format",
                    user_id=generated_by_id,
                    username=user.name if user else None,
                    new_values={
                        'report_type': report_type,
                        'format': format_type,
                        'records': record_count,
                        'filename': filename
                    }
                )
                
                return True
                
        except Exception as e:
            print(f"Error logging report generation: {e}")
            return False

    def get_report_history(self, user_id: int = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get report generation history."""
        try:
            with get_db() as session:
                query = session.query(ReportLog)
                
                if user_id:
                    query = query.filter(ReportLog.generated_by_id == user_id)
                
                reports = query.order_by(desc(ReportLog.generated_at))\
                              .limit(limit).all()
                
                history = []
                for report in reports:
                    history.append({
                        'id': report.id,
                        'report_type': report.report_type,
                        'format': report.report_format.value,
                        'filename': report.file_name,
                        'records_count': report.records_count,
                        'status': report.status.value,
                        'generated_at': report.generated_at.isoformat(),
                        'generated_by': report.generated_by.name if report.generated_by else 'Unknown'
                    })
                
                return history
                
        except Exception as e:
            print(f"Error getting report history: {e}")
            return []
