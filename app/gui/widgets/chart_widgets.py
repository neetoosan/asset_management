"""
Chart Widgets for Asset Management System
Reimplemented to use QtCharts (2D pie/bar/donut) and QtDataVisualization (3D bars when available).
This removes the matplotlib dependency and uses PySide6 native charting where possible.
"""

from typing import Dict, List, Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QWidget as QtWidget, QSizePolicy
from PySide6.QtCore import Signal, Qt, QMargins
from PySide6.QtGui import QFont, QPainter, QColor

# Optional matplotlib/numpy fallback for legacy chart classes
try:
    import matplotlib
    matplotlib.use('Qt5Agg')
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    import numpy as np
    HAS_MATPLOTLIB = True
except Exception:
    HAS_MATPLOTLIB = False

# QtCharts imports (2D charts)
try:
    from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
    HAS_QTCHARTS = True
except Exception:
    HAS_QTCHARTS = False

# Qt Data Visualization (3D) - optional
try:
    from PySide6.QtDataVisualization import Q3DBars, QBar3DSeries, QBarDataArray, QBarDataItem, QValue3DAxis, QCategory3DAxis
    from PySide6.QtWidgets import QWidget
    HAS_3D = True
except Exception:
    HAS_3D = False


class BaseChartWidget(QWidget):
    """Base class for all chart widgets (uses QtCharts when available).

    This class provides a compatibility layer: if matplotlib is available it
    creates a Figure and FigureCanvas (accessible as `self.figure` and
    `self.canvas`) so legacy matplotlib-based subclasses continue to work.
    Otherwise the widget exposes `self.canvas` which points to the active
    chart widget (e.g. QChartView).
    """
    dataUpdated = Signal()

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.title = title
        # Use a private layout attribute to avoid shadowing QWidget.layout()
        self._v_layout = QVBoxLayout(self)

        # Title
        if title:
            title_label = QLabel(title)
            title_font = QFont()
            title_font.setPointSize(12)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setAlignment(Qt.AlignCenter)
            self._v_layout.addWidget(title_label)

        # Default placeholder chart widget
        self.chart_widget = QtWidget()
        self._v_layout.addWidget(self.chart_widget)

        # Matplotlib compatibility: create a Figure + Canvas if available
        if HAS_MATPLOTLIB:
            try:
                self.figure = Figure(figsize=(8, 6), dpi=100)
                self.canvas = FigureCanvas(self.figure)
                # Add matplotlib canvas to layout so legacy classes can use it
                self._v_layout.addWidget(self.canvas)
                # Provide a convenience alias for older code that expected .ax
            except Exception:
                # If matplotlib exists but fails to initialize, provide placeholders
                self.figure = None
                self.canvas = self.chart_widget
        else:
            # No matplotlib: canvas points to the generic chart widget
            self.figure = None
            self.canvas = self.chart_widget

    def clear(self):
        # Subclasses should implement
        pass

    def refresh(self):
        # If matplotlib canvas exists, trigger a redraw
        if HAS_MATPLOTLIB and getattr(self, 'canvas', None) is not None and hasattr(self.canvas, 'draw'):
            try:
                self.canvas.draw()
            except Exception:
                pass

    def save_chart(self, filename: str):
        # Try to save using matplotlib if present
        if HAS_MATPLOTLIB and getattr(self, 'figure', None) is not None:
            try:
                self.figure.savefig(filename, dpi=300, bbox_inches='tight')
                return True
            except Exception:
                return False
        return False


class PieChartWidget(BaseChartWidget):
    """Pie chart widget using QtCharts QPieSeries. Expects data as list of tuples [(label, value), ...]."""

    def __init__(self, title: str = "", parent=None):
        super().__init__(title=title, parent=parent)

        if not HAS_QTCHARTS:
            # Show placeholder
            placeholder = QLabel("QtCharts is not available in this environment.")
            placeholder.setAlignment(Qt.AlignCenter)
            self._v_layout.addWidget(placeholder)
            self.chart_widget = placeholder
            return

        # Build chart
        self.series = QPieSeries()
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(self.title)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        # Make the chart view expand to available space and give a reasonable minimum height
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view.setMinimumHeight(220)
        # Title styling
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        try:
            self.chart.setTitleFont(title_font)
            self.chart.setAnimationOptions(QChart.SeriesAnimations)
        except Exception:
            pass

        # Replace placeholder. Also remove any existing matplotlib canvas if present
        try:
            # remove old chart_widget
            self._v_layout.removeWidget(self.chart_widget)
            self.chart_widget.deleteLater()
        except Exception:
            pass
        try:
            # If a matplotlib canvas was created by BaseChartWidget, remove it
            if HAS_MATPLOTLIB and getattr(self, 'canvas', None) is not None:
                # FigureCanvas has 'figure' attribute; do a duck-typing check
                canvas_obj = getattr(self, 'canvas')
                if getattr(canvas_obj, 'figure', None) is not None:
                    try:
                        self._v_layout.removeWidget(canvas_obj)
                        canvas_obj.setParent(None)
                    except Exception:
                        pass
        except Exception:
            pass

        self.chart_widget = self.view
        # make canvas point to the chart view for compatibility
        self.canvas = self.chart_widget
        self._v_layout.addWidget(self.chart_widget)

    def set_data(self, data: List[Any]):
        """Set data for pie chart. data -> list of (label, value)."""
        if not HAS_QTCHARTS:
            return
        self.series.clear()
        total = 0
        for label, value in data:
            total += float(value or 0)
            slice_ = QPieSlice(label, float(value or 0))
            # Label formatting: show count and percent
            slice_.setLabelVisible(True)
            try:
                slice_.setLabel(f"{label}: {int(float(value or 0))}")
                slice_.setLabelPosition(QPieSlice.LabelOutside)
            except Exception:
                pass
            # Give slices distinct colors using a simple hue variation
            try:
                idx = self.series.count()
                hue = (idx * 47) % 360
                slice_.setBrush(QColor.fromHsv(hue, 200, 200))
            except Exception:
                pass
            self.series.append(slice_)

        # Optionally highlight largest slice
        if self.series.count() > 0:
            max_slice = max(self.series.slices(), key=lambda s: s.value())
            max_slice.setExploded(True)
            max_slice.setLabelVisible(True)

        self.dataUpdated.emit()


class Bar3DChartWidget(BaseChartWidget):
    """3D Bar chart using QtDataVisualization when available. Falls back to 2D QChart bar series.

    Expects data as a dict: {category_label: [v1, v2, ...], ...} or a list of (category, value) pairs.
    For simple usage pass a list of (label, value) and it will render a single series.
    """

    def __init__(self, title: str = "", parent=None):
        super().__init__(title=title, parent=parent)

        if HAS_3D:
            try:
                # Create 3D bars window and container
                self.graph = Q3DBars()
                self.container = QWidget.createWindowContainer(self.graph)
                layout = QVBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(self.container)

                # Replace placeholder
                self.layout.removeWidget(self.chart_widget)
                self.chart_widget.deleteLater()
                self.chart_widget = self.container
                # Ensure container expands
                try:
                    self.container.setMinimumHeight(260)
                    self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                except Exception:
                    pass
                self._v_layout.addLayout(layout)
            except Exception:
                # Fallback to 2D
                self._init_2d()
        else:
            self._init_2d()

    def _init_2d(self):
        if not HAS_QTCHARTS:
            placeholder = QLabel("QtCharts / QtDataVisualization not available.")
            placeholder.setAlignment(Qt.AlignCenter)
            try:
                self._v_layout.removeWidget(self.chart_widget)
                self.chart_widget.deleteLater()
            except Exception:
                pass
            try:
                if HAS_MATPLOTLIB and getattr(self, 'canvas', None) is not None:
                    canvas_obj = getattr(self, 'canvas')
                    if getattr(canvas_obj, 'figure', None) is not None:
                        try:
                            self._v_layout.removeWidget(canvas_obj)
                            canvas_obj.setParent(None)
                        except Exception:
                            pass
            except Exception:
                pass
            self.chart_widget = placeholder
            self.canvas = self.chart_widget
            self._v_layout.addWidget(self.chart_widget)
            return

        # 2D bar chart setup
        self.series = QBarSeries()
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(self.title)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.axisX = QBarCategoryAxis()
        self.axisY = QValueAxis()

        self.chart.createDefaultAxes()
        self.chart.setAxisX(self.axisX, self.series)
        self.chart.setAxisY(self.axisY, self.series)

        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view.setMinimumHeight(240)
        try:
            self._v_layout.removeWidget(self.chart_widget)
            self.chart_widget.deleteLater()
        except Exception:
            pass
        try:
            if HAS_MATPLOTLIB and getattr(self, 'canvas', None) is not None:
                canvas_obj = getattr(self, 'canvas')
                if getattr(canvas_obj, 'figure', None) is not None:
                    try:
                        self._v_layout.removeWidget(canvas_obj)
                        canvas_obj.setParent(None)
                    except Exception:
                        pass
        except Exception:
            pass
        self.chart_widget = self.view
        self.canvas = self.chart_widget
        self._v_layout.addWidget(self.chart_widget)

    def set_data(self, data: Any):
        """Set data for the 3D/2D bar chart. Accepts list of (label, value) or dict of label->[values]."""
        if HAS_3D:
            # Provide a simple 3D rendering for list of pairs
            try:
                if isinstance(data, dict):
                    categories = list(data.keys())
                    # Build a single row per category with first value
                    data_array = QBarDataArray()
                    for label in categories:
                        row = []
                        vals = data[label]
                        # take first value or 0
                        row.append(QBarDataItem(float(vals[0]) if vals else 0.0))
                        data_array.append(row)

                    series = QBar3DSeries()
                    series.dataProxy().resetArray(data_array)
                    self.graph.addSeries(series)
                elif isinstance(data, list):
                    data_array = QBarDataArray()
                    row = []
                    categories = []
                    for label, value in data:
                        categories.append(label)
                        row.append(QBarDataItem(float(value or 0)))
                    data_array.append(row)
                    series = QBar3DSeries()
                    series.dataProxy().resetArray(data_array)
                    self.graph.addSeries(series)
                self.dataUpdated.emit()
                return
            except Exception:
                # Fall through to 2D
                pass

        # Fallback: 2D bar chart
        if not HAS_QTCHARTS:
            return

        # Normalize data to simple series
        pairs = []
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (list, tuple)):
                    val = v[0] if v else 0
                else:
                    val = v
                pairs.append((k, val))
        elif isinstance(data, list):
            pairs = data

        # Clear series
        for s in list(self.series.barSets()):
            self.series.remove(s)

        set0 = QBarSet(self.title or "")
        categories = []
        for label, value in pairs:
            categories.append(str(label))
            set0.append(float(value or 0))

        self.series.append(set0)
        self.axisX.clear()
        self.axisX.append(categories)
        try:
            upper = max([float(v or 0) for _, v in pairs] + [1])
            self.axisY.setRange(0, upper * 1.15)
        except Exception:
            try:
                self.axisY.setRange(0, 1)
            except Exception:
                pass

        self.dataUpdated.emit()


class AssetCategoryPieChart(PieChartWidget):
    """Pie chart showing asset distribution by category using QtCharts."""

    def __init__(self, title: str = "Asset Distribution by Category", parent=None):
        super().__init__(title=title, parent=parent)

    def update_data(self, category_data: Dict[str, int]):
        """Update pie chart with category data (dict -> list)"""
        if not category_data:
            # Clear existing series
            try:
                if hasattr(self, 'series'):
                    self.series.clear()
            except Exception:
                pass
            return

        data = [(k, float(v or 0)) for k, v in category_data.items()]
        self.set_data(data)


class AssetValueBarChart(Bar3DChartWidget):
    """Bar chart showing asset values by category using Bar3DChartWidget (3D if available)."""

    def __init__(self, title: str = "Asset Values by Category", parent=None):
        super().__init__(title=title, parent=parent)

    def update_data(self, value_data: Dict[str, float]):
        """Update bar chart with value_data dict or list of pairs"""
        if not value_data:
            # clear
            try:
                if hasattr(self, 'series'):
                    for s in list(self.series.barSets()):
                        self.series.remove(s)
            except Exception:
                pass
            return

        # Provide dict -> list format for Bar3DChartWidget
        if isinstance(value_data, dict):
            pairs = [(k, float(v or 0)) for k, v in value_data.items()]
        else:
            pairs = value_data

        self.set_data(pairs)


class AssetStatusDonutChart(PieChartWidget):
    """Donut chart showing asset distribution by status using QtCharts (donut)."""

    def __init__(self, title: str = "Asset Distribution by Status", parent=None):
        super().__init__(title=title, parent=parent)
        # Make donut hole if supported
        try:
            if HAS_QTCHARTS and hasattr(self, 'series'):
                self.series.setHoleSize(0.5)
        except Exception:
            pass

    def update_data(self, status_data: Dict[str, int]):
        if not status_data:
            try:
                self.series.clear()
            except Exception:
                pass
            return

        # Map colors if desired via slices
        data = [(k, float(v or 0)) for k, v in status_data.items()]
        self.set_data(data)
        # Optionally set colors per slice
        try:
            color_map = {
                'Available': '#28a745',
                'In Use': '#007bff',
                'Under Maintenance': '#ffc107',
                'Retired': '#6c757d',
                'Damaged': '#dc3545',
                'Disposed': '#343a40'
            }
            for slice_ in self.series.slices():
                lbl = slice_.label()
                color = color_map.get(lbl)
                if color:
                    slice_.setBrush(color)
        except Exception:
            pass


class AssetTrendLineChart(BaseChartWidget):
    """Line chart showing asset trends over time using QtCharts."""

    def __init__(self, title: str = "Asset Trends", parent=None):
        super().__init__(title=title, parent=parent)
        # Build QLineSeries chart
        if not HAS_QTCHARTS:
            placeholder = QLabel("QtCharts not available for AssetTrendLineChart")
            placeholder.setAlignment(Qt.AlignCenter)
            try:
                self._v_layout.removeWidget(self.canvas)
                self.canvas.setParent(None)
            except Exception:
                pass
            self.canvas = placeholder
            self._v_layout.addWidget(self.canvas)
            self.series = None
            return

        from PySide6.QtCharts import QLineSeries, QValueAxis

        self.series = QLineSeries()
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(self.title)
        self.axisX = QBarCategoryAxis()
        self.axisY = QValueAxis()
        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)

        try:
            self._v_layout.removeWidget(self.chart_widget)
            self.chart_widget.deleteLater()
        except Exception:
            pass
        self.chart_widget = self.view
        self.canvas = self.chart_widget
        self._v_layout.addWidget(self.chart_widget)

    def update_data(self, trend_data: Dict[str, List[Any]]):
        if not HAS_QTCHARTS or getattr(self, 'series', None) is None:
            return

        if not trend_data or 'dates' not in trend_data or 'values' not in trend_data:
            return

        dates = trend_data['dates']
        values = trend_data['values']
        if len(dates) != len(values) or len(dates) == 0:
            return

        self.series.clear()
        categories = []
        for i, (d, v) in enumerate(zip(dates, values)):
            self.series.append(i, float(v or 0))
            categories.append(str(d))

        # Update axes
        try:
            self.axisX.clear()
            # QBarCategoryAxis append categories
            self.axisX.append(categories)
            self.axisY.setRange(0, max([float(v or 0) for v in values] + [1]))
        except Exception:
            pass

        self.dataUpdated.emit()


class AssetDepreciationChart(BaseChartWidget):
    """Chart showing asset depreciation over time using QtCharts with two series."""

    def __init__(self, title: str = "Asset Depreciation", parent=None):
        super().__init__(title=title, parent=parent)
        if not HAS_QTCHARTS:
            placeholder = QLabel("QtCharts not available for AssetDepreciationChart")
            placeholder.setAlignment(Qt.AlignCenter)
            try:
                self._v_layout.removeWidget(self.canvas)
                self.canvas.setParent(None)
            except Exception:
                pass
            self.canvas = placeholder
            self._v_layout.addWidget(self.canvas)
            self.series1 = self.series2 = None
            return

        from PySide6.QtCharts import QLineSeries, QValueAxis

        self.series1 = QLineSeries()
        self.series2 = QLineSeries()
        self.chart = QChart()
        self.chart.addSeries(self.series1)
        self.chart.addSeries(self.series2)
        self.chart.setTitle(self.title)

        self.axisX = QBarCategoryAxis()
        self.axisY_left = QValueAxis()
        self.axisY_right = QValueAxis()

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY_left, Qt.AlignLeft)
        self.chart.addAxis(self.axisY_right, Qt.AlignRight)

        self.series1.attachAxis(self.axisX)
        self.series1.attachAxis(self.axisY_left)
        self.series2.attachAxis(self.axisX)
        self.series2.attachAxis(self.axisY_right)

        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)

        try:
            self._v_layout.removeWidget(self.chart_widget)
            self.chart_widget.deleteLater()
        except Exception:
            pass
        self.chart_widget = self.view
        self.canvas = self.chart_widget
        self._v_layout.addWidget(self.chart_widget)

    def update_data(self, depreciation_data: Dict[str, Any]):
        if not HAS_QTCHARTS or getattr(self, 'series1', None) is None:
            return

        years = depreciation_data.get('years', [])
        book_values = depreciation_data.get('book_values', [])
        accumulated_dep = depreciation_data.get('accumulated_depreciation', [])

        if not years or not book_values:
            return

        self.series1.clear()
        self.series2.clear()
        categories = []
        for i, year in enumerate(years):
            val1 = float(book_values[i]) if i < len(book_values) else 0.0
            self.series1.append(i, val1)
            categories.append(str(year))
            if accumulated_dep and i < len(accumulated_dep):
                self.series2.append(i, float(accumulated_dep[i] or 0))

        # Update axes
        try:
            self.axisX.clear()
            self.axisX.append(categories)
            max_left = max([float(v or 0) for v in book_values] + [1])
            self.axisY_left.setRange(0, max_left)
            if accumulated_dep:
                max_right = max([float(v or 0) for v in accumulated_dep] + [1])
                self.axisY_right.setRange(0, max_right)
        except Exception:
            pass

        self.dataUpdated.emit()


class InteractiveChartWidget(BaseChartWidget):
    """Interactive chart widget with controls"""
    
    chartTypeChanged = Signal(str)
    
    def __init__(self, title: str = "Interactive Chart", parent=None):
        super().__init__(title, parent)
        
        # Create control panel
        self.setup_controls()
        
        # Chart types
        self.chart_types = {
            'pie': AssetCategoryPieChart("", self),
            'bar': AssetValueBarChart("", self),
            'donut': AssetStatusDonutChart("", self)
        }
        
        self.current_chart = self.chart_types['pie']
        self.current_data = {}
    
    def setup_controls(self):
        """Set up interactive controls"""
        # Insert control panel at the top
        control_layout = QHBoxLayout()
        
        # Chart type selector
        type_label = QLabel("Chart Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Pie Chart", "Bar Chart", "Donut Chart"])
        self.type_combo.currentTextChanged.connect(self.change_chart_type)
        
        # Export button
        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self.export_chart)
        
        control_layout.addWidget(type_label)
        control_layout.addWidget(self.type_combo)
        control_layout.addStretch()
        control_layout.addWidget(self.export_btn)
        
        # Insert at the beginning of the layout
        try:
            self._v_layout.insertLayout(1, control_layout)
        except Exception:
            pass
    
    def change_chart_type(self, chart_type: str):
        """Change the active chart type"""
        type_map = {
            "Pie Chart": 'pie',
            "Bar Chart": 'bar', 
            "Donut Chart": 'donut'
        }
        
        chart_key = type_map.get(chart_type, 'pie')
        
        if chart_key in self.chart_types:
            # Remove current chart widget from layout
            if hasattr(self, 'current_chart') and self.current_chart:
                try:
                    self._v_layout.removeWidget(self.current_chart.canvas)
                    self.current_chart.canvas.setParent(None)
                except Exception:
                    pass

            # Add new chart
            self.current_chart = self.chart_types[chart_key]
            try:
                self._v_layout.addWidget(self.current_chart.canvas)
            except Exception:
                pass

            # Update with current data
            if hasattr(self.current_chart, 'update_data') and self.current_data:
                try:
                    self.current_chart.update_data(self.current_data)
                except Exception:
                    pass

            self.chartTypeChanged.emit(chart_key)
    
    def update_data(self, data: Dict[str, Any]):
        """Update the current chart with new data"""
        self.current_data = data
        if hasattr(self.current_chart, 'update_data'):
            self.current_chart.update_data(data)
    
    def export_chart(self):
        """Export current chart to file"""
        from PySide6.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Chart",
            f"{self.title.replace(' ', '_').lower()}_chart.png",
            "PNG files (*.png);;PDF files (*.pdf);;SVG files (*.svg)"
        )
        
        if filename:
            success = self.current_chart.save_chart(filename)
            if success:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Success", f"Chart exported to {filename}")
            else:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Error", "Failed to export chart")