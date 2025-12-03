from PySide6.QtWidgets import QWidget, QLabel, QListWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from datetime import datetime, timedelta

from app.gui.ui.dashboard_screen_ui import Ui_DashboardScreen
from app.gui.widgets.chart_widgets import AssetCategoryPieChart, AssetValueBarChart, AssetStatusDonutChart
from app.gui.dialogs.chart_magnifier_dialog import ChartMagnifierDialog
from app.services.asset_service import AssetService
from app.services.session_service import SessionService
from app.services.audit_service import AuditService

class DashboardScreen(QWidget):
    def __init__(self, session_service: SessionService, parent=None):
        super().__init__(parent)
        self.ui = Ui_DashboardScreen()
        self.ui.setupUi(self)
        
        # Initialize services
        self.session_service = session_service
        self.asset_service = AssetService()
        self.audit_service = AuditService()
        
        # Set current user context for services
        if self.session_service.is_authenticated():
            user_id = self.session_service.get_user_id()
            user_name = self.session_service.get_username()
            self.asset_service.set_current_user(user_id, user_name)
            self.audit_service.set_current_user(user_id, user_name)
        
        # Initialize charts
        self.pie_chart = None
        self.bar_chart = None
        
        self.init_dashboard()
        self.load_dashboard_data()

    def init_dashboard(self):
        """Initialize dashboard UI components"""
        # Initialize with default values
        self.ui.totalAssetsLabel.setText("Total Assets: Loading...")
        self.ui.totalValueLabel.setText("Total Value: Loading...")
        self.ui.totalCategoriesLabel.setText("Total Categories: Loading...")
        
        # Clear recent activities list
        self.ui.recentActivitiesList.clear()
        
        # Initialize charts
        self.setup_charts()
    
    def setup_charts(self):
        """Set up real chart widgets"""
        # Asset Category Pie Chart
        self.pie_chart = AssetCategoryPieChart("Asset Distribution by Category")
        pie_layout = QVBoxLayout(self.ui.assetCategoryPieWidget)
        pie_layout.addWidget(self.pie_chart)
        
        # Add click handler to pie chart if it has a view
        if hasattr(self.pie_chart, 'view') and hasattr(self.pie_chart.view, 'mousePressEvent'):
            self.pie_chart.view.mousePressEvent = lambda event: self._on_pie_chart_clicked(event)
        elif hasattr(self.pie_chart, 'canvas'):
            # For other chart types, use the canvas if available
            pass
        
        # Asset Value Bar Chart
        self.bar_chart = AssetValueBarChart("Asset Values by Category")
        bar_layout = QVBoxLayout(self.ui.valuationChartWidget)
        bar_layout.addWidget(self.bar_chart)
        
        # Add click handler to bar chart if it has a view
        if hasattr(self.bar_chart, 'view') and hasattr(self.bar_chart.view, 'mousePressEvent'):
            self.bar_chart.view.mousePressEvent = lambda event: self._on_bar_chart_clicked(event)
        elif hasattr(self.bar_chart, 'canvas'):
            # For other chart types, use the canvas if available
            pass
    
    def load_dashboard_data(self):
        """Load and display dashboard data from services"""
        try:
            # Load asset statistics
            self.load_asset_statistics()
            
            # Load category data for charts
            self.load_category_charts()
            
            # Load recent activities
            self.load_recent_activities()
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
    
    def load_asset_statistics(self):
        """Load and display asset statistics"""
        try:
            with self.asset_service.get_session() as session:
                # Get all assets
                assets = self.asset_service.get_all_assets(session)
                total_assets = len(assets)

                # Calculate total value (support dicts or ORM objects)
                def _get_total(a):
                    if isinstance(a, dict):
                        return float(a.get('total_cost', 0) or 0)
                    return float(getattr(a, 'total_cost', 0) or 0)

                total_value = sum(_get_total(asset) for asset in assets)
                
                # Get categories with the same session
                categories = self.asset_service.get_all_categories(session)
                total_categories = len(categories)
                
                # Update UI
                self.ui.totalAssetsLabel.setText(f"Total Assets: {total_assets:,}")
                self.ui.totalValueLabel.setText(f"Total Value: ₦{total_value:,.2f}")
                self.ui.totalCategoriesLabel.setText(f"Total Categories: {total_categories}")
            
        except Exception as e:
            print(f"Error loading asset statistics: {e}")
            self.ui.totalAssetsLabel.setText("Total Assets: Error")
            self.ui.totalValueLabel.setText("Total Value: Error")
            self.ui.totalCategoriesLabel.setText("Total Categories: Error")
    
    def load_category_charts(self):
        """Load data for category charts"""
        try:
            with self.asset_service.get_session() as session:
                # Get category statistics
                category_stats = self.asset_service.get_assets_by_category(session)
                
                if category_stats:
                    # Prepare data for pie chart (asset count by category)
                    pie_data = {}
                    bar_data = {}
                    
                    for category_name, stats in category_stats.items():
                        count = stats.get('count', 0)
                        total_value = stats.get('total_value', 0)
                        
                        if count > 0:
                            pie_data[category_name] = count
                            bar_data[category_name] = total_value
                
                    # Update charts
                    if self.pie_chart and pie_data:
                        self.pie_chart.update_data(pie_data)
                    
                    if self.bar_chart and bar_data:
                        self.bar_chart.update_data(bar_data)
            
        except Exception as e:
            print(f"Error loading category charts: {e}")
    
    def load_recent_activities(self):
        """Load recent activities from audit log"""
        try:
            # Get recent audit logs for the last 24 hours
            recent_logs = self.audit_service.get_recent_activity(hours=24, limit=10)

            # Clear existing items
            self.ui.recentActivitiesList.clear()

            if not recent_logs:
                self.ui.recentActivitiesList.addItem("No recent activities")
                return

            for log in recent_logs:
                timestamp = log.get('timestamp')
                description = log.get('description', '')

                # Parse timestamp
                time_str = ''
                if timestamp:
                    try:
                        ts = timestamp
                        if isinstance(ts, str) and ts.endswith('Z'):
                            ts = ts.replace('Z', '+00:00')
                        dt = datetime.fromisoformat(ts)
                        time_str = dt.strftime('%H:%M')
                    except Exception:
                        time_str = ''

                # If this is an asset-related action, try to show asset name/id
                action = (log.get('action') or '').upper()
                details = ''
                if action.startswith('ASSET') or log.get('table_name') == 'assets':
                    vals = log.get('new_values') or log.get('old_values') or {}
                    if isinstance(vals, dict):
                        name = vals.get('name') or vals.get('asset_name')
                        aid = vals.get('asset_id') or vals.get('assetId') or log.get('record_id')
                        details = f" {name or ''} (ID: {aid or ''})"

                # Fallback to generic description
                entry = f"[{time_str}] {description}{details}" if time_str else f"{description}{details}"
                self.ui.recentActivitiesList.addItem(entry)
                    
        except Exception as e:
            print(f"Error loading recent activities: {e}")
            self.ui.recentActivitiesList.addItem("Error loading activities")
    
    def _on_pie_chart_clicked(self, event):
        """Handle pie chart click event"""
        if event.button() == Qt.LeftButton and hasattr(self.pie_chart, 'series'):
            # Extract data from pie chart series
            chart_data = {}
            try:
                for slice_ in self.pie_chart.series.slices():
                    chart_data[slice_.label().split(':')[0].strip()] = slice_.value()
            except Exception as e:
                print(f"Error extracting pie chart data: {e}")
            
            if chart_data:
                # Show magnified dialog with data
                dialog = ChartMagnifierDialog(
                    "Asset Distribution by Category",
                    'pie',
                    chart_data,
                    parent=self
                )
                dialog.exec()
    
    def _on_bar_chart_clicked(self, event):
        """Handle bar chart click event"""
        if event.button() == Qt.LeftButton and hasattr(self.bar_chart, 'series'):
            # Extract data from bar chart series
            chart_data = {}
            try:
                categories = self.bar_chart.axisX.categories() if hasattr(self.bar_chart, 'axisX') else []
                if self.bar_chart.series and len(self.bar_chart.series.barSets()) > 0:
                    bar_set = self.bar_chart.series.barSets()[0]
                    # Use count() and at() to access QBarSet values
                    for i in range(bar_set.count()):
                        val = bar_set.at(i)
                        cat = categories[i] if i < len(categories) else f"Category {i+1}"
                        chart_data[cat] = val
            except Exception as e:
                print(f"Error extracting bar chart data: {e}")
            
            if chart_data:
                # Show magnified dialog with data
                dialog = ChartMagnifierDialog(
                    "Asset Values by Category",
                    'bar',
                    chart_data,
                    parent=self
                )
                dialog.exec()
