"""
Chart Magnifier Dialog - Displays charts in a magnified view when clicked on dashboard
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtCharts import (
    QChart, QChartView, QPieSeries, QPieSlice, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import QPainter, QColor


class ChartMagnifierDialog(QDialog):
    """Dialog to display a magnified chart with close button and details"""
    
    def __init__(self, title: str, chart_type: str, chart_data: dict, parent=None):
        super().__init__(parent)
        self.title = title
        self.chart_type = chart_type  # 'pie' or 'bar'
        self.chart_data = chart_data or {}
        
        # Set window properties
        self.setWindowTitle(f"Magnified View - {title}")
        self.setGeometry(100, 100, 1000, 700)  # Larger size for magnified view
        self.setModal(True)
        
        # Create layout
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title label
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create fresh chart from data (avoid passing an owned QChart instance)
        chart = self._create_chart()
        
        # Chart view
        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(500)
        main_layout.addWidget(self.chart_view)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def _create_chart(self) -> QChart:
        """Create a new chart from stored data"""
        chart = QChart()
        chart.setTitle(self.title)
        
        if self.chart_type == 'pie':
            # Recreate pie chart
            series = QPieSeries()
            for label, value in self.chart_data.items():
                slice_ = QPieSlice(str(label), float(value or 0))
                slice_.setLabelVisible(True)
                try:
                    slice_.setLabel(f"{label}: {int(float(value or 0))}")
                    slice_.setLabelPosition(QPieSlice.LabelOutside)
                except Exception:
                    pass
                # Color slices
                idx = series.count()
                hue = (idx * 47) % 360
                slice_.setBrush(QColor.fromHsv(hue, 200, 200))
                series.append(slice_)
            # Highlight largest
            try:
                if series.count() > 0:
                    max_slice = max(series.slices(), key=lambda s: s.value())
                    max_slice.setExploded(True)
            except Exception:
                pass
            chart.addSeries(series)
            try:
                chart.legend().setVisible(True)
                chart.legend().setAlignment(Qt.AlignBottom)
            except Exception:
                pass
        
        elif self.chart_type == 'bar':
            # Recreate bar chart
            series = QBarSeries()
            bar_set = QBarSet(self.title or "Values")
            categories = []
            for label, value in self.chart_data.items():
                categories.append(str(label))
                bar_set.append(float(value or 0))
            series.append(bar_set)
            chart.addSeries(series)
            # Axes
            axis_x = QBarCategoryAxis()
            axis_x.append(categories)
            axis_y = QValueAxis()
            try:
                max_val = max([float(v or 0) for v in self.chart_data.values()] + [1])
                axis_y.setRange(0, max_val * 1.15)
            except Exception:
                pass
            chart.addAxis(axis_x, Qt.AlignBottom)
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)
        
        try:
            chart.setAnimationOptions(QChart.SeriesAnimations)
        except Exception:
            pass
        return chart


class ClickableChartView(QChartView):
    """Custom QChartView that emits a signal when clicked"""
    
    # Signal emitted when chart is clicked
    chart_clicked = Signal(str)  # Passes chart title
    
    def __init__(self, chart: QChart, title: str = "", parent=None):
        super().__init__(chart, parent)
        self.title = title
        self.setRenderHint(QPainter.Antialiasing)
        
        # Enable mouse tracking
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
    
    def mousePressEvent(self, event):
        """Handle mouse press event on chart"""
        if event.button() == Qt.LeftButton:
            # Emit signal to indicate chart was clicked
            self.chart_clicked.emit(self.title)
        super().mousePressEvent(event)
    
    def set_title(self, title: str):
        """Update the chart title"""
        self.title = title
