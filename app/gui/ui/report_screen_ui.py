# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'report_screen.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDateEdit,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_ReportScreen(object):
    def setupUi(self, ReportScreen):
        if not ReportScreen.objectName():
            ReportScreen.setObjectName(u"ReportScreen")
        ReportScreen.resize(800, 600)
        self.mainLayout = QVBoxLayout(ReportScreen)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.reportsTitle = QLabel(ReportScreen)
        self.reportsTitle.setObjectName(u"reportsTitle")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.reportsTitle.setFont(font)
        self.reportsTitle.setAlignment(Qt.AlignLeft|Qt.AlignTop)

        self.mainLayout.addWidget(self.reportsTitle)

        self.reportFrame = QFrame(ReportScreen)
        self.reportFrame.setObjectName(u"reportFrame")
        self.reportFrame.setFrameShape(QFrame.StyledPanel)
        self.reportFrame.setFrameShadow(QFrame.Raised)
        self.frameLayout = QVBoxLayout(self.reportFrame)
        self.frameLayout.setSpacing(15)
        self.frameLayout.setObjectName(u"frameLayout")
        self.frameLayout.setContentsMargins(20, 20, 20, 20)
        self.generateLabel = QLabel(self.reportFrame)
        self.generateLabel.setObjectName(u"generateLabel")
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.generateLabel.setFont(font1)
        self.generateLabel.setAlignment(Qt.AlignCenter)

        self.frameLayout.addWidget(self.generateLabel)

        self.filtersGroupBox = QGroupBox(self.reportFrame)
        self.filtersGroupBox.setObjectName(u"filtersGroupBox")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.filtersGroupBox.setFont(font2)
        self.filtersLayout = QGridLayout(self.filtersGroupBox)
        self.filtersLayout.setSpacing(15)
        self.filtersLayout.setObjectName(u"filtersLayout")
        self.reportTypeLabel = QLabel(self.filtersGroupBox)
        self.reportTypeLabel.setObjectName(u"reportTypeLabel")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(False)
        self.reportTypeLabel.setFont(font3)

        self.filtersLayout.addWidget(self.reportTypeLabel, 0, 0, 1, 1)

        self.reportTypeComboBox = QComboBox(self.filtersGroupBox)
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.setObjectName(u"reportTypeComboBox")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(False)
        self.reportTypeComboBox.setFont(font4)

        self.filtersLayout.addWidget(self.reportTypeComboBox, 0, 1, 1, 1)

        self.formatLabel = QLabel(self.filtersGroupBox)
        self.formatLabel.setObjectName(u"formatLabel")
        self.formatLabel.setFont(font3)

        self.filtersLayout.addWidget(self.formatLabel, 1, 0, 1, 1)

        self.formatComboBox = QComboBox(self.filtersGroupBox)
        self.formatComboBox.addItem("")
        self.formatComboBox.addItem("")
        self.formatComboBox.addItem("")
        self.formatComboBox.addItem("")
        self.formatComboBox.setObjectName(u"formatComboBox")
        self.formatComboBox.setFont(font4)

        self.filtersLayout.addWidget(self.formatComboBox, 1, 1, 1, 1)

        self.dateRangeLabel = QLabel(self.filtersGroupBox)
        self.dateRangeLabel.setObjectName(u"dateRangeLabel")
        self.dateRangeLabel.setFont(font3)

        self.filtersLayout.addWidget(self.dateRangeLabel, 2, 0, 1, 1)

        self.dateRangeLayout = QHBoxLayout()
        self.dateRangeLayout.setObjectName(u"dateRangeLayout")
        self.startDateEdit = QDateEdit(self.filtersGroupBox)
        self.startDateEdit.setObjectName(u"startDateEdit")
        self.startDateEdit.setFont(font4)
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.setDate(QDate(2024, 1, 1))

        self.dateRangeLayout.addWidget(self.startDateEdit)

        self.toLabel = QLabel(self.filtersGroupBox)
        self.toLabel.setObjectName(u"toLabel")
        self.toLabel.setAlignment(Qt.AlignCenter)

        self.dateRangeLayout.addWidget(self.toLabel)

        self.endDateEdit = QDateEdit(self.filtersGroupBox)
        self.endDateEdit.setObjectName(u"endDateEdit")
        self.endDateEdit.setFont(font4)
        self.endDateEdit.setCalendarPopup(True)

        self.dateRangeLayout.addWidget(self.endDateEdit)


        self.filtersLayout.addLayout(self.dateRangeLayout, 2, 1, 1, 1)


        self.frameLayout.addWidget(self.filtersGroupBox)

        self.exportLayout = QHBoxLayout()
        self.exportLayout.setObjectName(u"exportLayout")
        self.leftSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.exportLayout.addItem(self.leftSpacer)

        self.exportButton = QPushButton(self.reportFrame)
        self.exportButton.setObjectName(u"exportButton")
        self.exportButton.setFont(font2)
        icon = QIcon()
        icon.addFile(u"../../static/images/file_logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportButton.setIcon(icon)
        self.exportButton.setIconSize(QSize(20, 20))

        self.exportLayout.addWidget(self.exportButton)

        self.rightSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.exportLayout.addItem(self.rightSpacer)


        self.frameLayout.addLayout(self.exportLayout)

        self.smallVerticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.frameLayout.addItem(self.smallVerticalSpacer)


        self.mainLayout.addWidget(self.reportFrame)

        self.reportLogsFrame = QFrame(ReportScreen)
        self.reportLogsFrame.setObjectName(u"reportLogsFrame")
        self.reportLogsFrame.setFrameShape(QFrame.StyledPanel)
        self.reportLogsFrame.setFrameShadow(QFrame.Raised)
        self.logsFrameLayout = QVBoxLayout(self.reportLogsFrame)
        self.logsFrameLayout.setSpacing(15)
        self.logsFrameLayout.setObjectName(u"logsFrameLayout")
        self.logsFrameLayout.setContentsMargins(20, 20, 20, 20)
        self.reportLogsLabel = QLabel(self.reportLogsFrame)
        self.reportLogsLabel.setObjectName(u"reportLogsLabel")
        self.reportLogsLabel.setFont(font1)
        self.reportLogsLabel.setAlignment(Qt.AlignCenter)

        self.logsFrameLayout.addWidget(self.reportLogsLabel)

        self.logsFilterLayout = QHBoxLayout()
        self.logsFilterLayout.setObjectName(u"logsFilterLayout")
        self.filterLabel = QLabel(self.reportLogsFrame)
        self.filterLabel.setObjectName(u"filterLabel")
        self.filterLabel.setFont(font3)

        self.logsFilterLayout.addWidget(self.filterLabel)

        self.filterStartDateEdit = QDateEdit(self.reportLogsFrame)
        self.filterStartDateEdit.setObjectName(u"filterStartDateEdit")
        self.filterStartDateEdit.setFont(font4)
        self.filterStartDateEdit.setCalendarPopup(True)
        self.filterStartDateEdit.setDate(QDate(2024, 1, 1))

        self.logsFilterLayout.addWidget(self.filterStartDateEdit)

        self.filterToLabel = QLabel(self.reportLogsFrame)
        self.filterToLabel.setObjectName(u"filterToLabel")
        self.filterToLabel.setAlignment(Qt.AlignCenter)

        self.logsFilterLayout.addWidget(self.filterToLabel)

        self.filterEndDateEdit = QDateEdit(self.reportLogsFrame)
        self.filterEndDateEdit.setObjectName(u"filterEndDateEdit")
        self.filterEndDateEdit.setFont(font4)
        self.filterEndDateEdit.setCalendarPopup(True)

        self.logsFilterLayout.addWidget(self.filterEndDateEdit)

        self.filterButton = QPushButton(self.reportLogsFrame)
        self.filterButton.setObjectName(u"filterButton")
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(True)
        self.filterButton.setFont(font5)

        self.logsFilterLayout.addWidget(self.filterButton)

        self.clearFilterButton = QPushButton(self.reportLogsFrame)
        self.clearFilterButton.setObjectName(u"clearFilterButton")
        self.clearFilterButton.setFont(font5)

        self.logsFilterLayout.addWidget(self.clearFilterButton)

        self.filterSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logsFilterLayout.addItem(self.filterSpacer)


        self.logsFrameLayout.addLayout(self.logsFilterLayout)

        self.reportLogsTable = QTableWidget(self.reportLogsFrame)
        if (self.reportLogsTable.columnCount() < 6):
            self.reportLogsTable.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.reportLogsTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.reportLogsTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.reportLogsTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.reportLogsTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.reportLogsTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.reportLogsTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.reportLogsTable.setObjectName(u"reportLogsTable")
        self.reportLogsTable.setAlternatingRowColors(True)
        self.reportLogsTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.reportLogsTable.setSortingEnabled(True)

        self.logsFrameLayout.addWidget(self.reportLogsTable)


        self.mainLayout.addWidget(self.reportLogsFrame)

        self.bottomSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.bottomSpacer)


        self.retranslateUi(ReportScreen)

        QMetaObject.connectSlotsByName(ReportScreen)
    # setupUi

    def retranslateUi(self, ReportScreen):
        ReportScreen.setWindowTitle(QCoreApplication.translate("ReportScreen", u"Reports", None))
        self.reportsTitle.setText(QCoreApplication.translate("ReportScreen", u"Reports", None))
        self.generateLabel.setText(QCoreApplication.translate("ReportScreen", u"Generate Reports", None))
        self.filtersGroupBox.setTitle(QCoreApplication.translate("ReportScreen", u"Filter Options", None))
        self.reportTypeLabel.setText(QCoreApplication.translate("ReportScreen", u"Report Type:", None))
        self.reportTypeComboBox.setItemText(0, QCoreApplication.translate("ReportScreen", u"All Assets Report", None))
        self.reportTypeComboBox.setItemText(1, QCoreApplication.translate("ReportScreen", u"Assets by Category", None))
        self.reportTypeComboBox.setItemText(2, QCoreApplication.translate("ReportScreen", u"Assets by Department", None))
        self.reportTypeComboBox.setItemText(3, QCoreApplication.translate("ReportScreen", u"Depreciation Report", None))
        self.reportTypeComboBox.setItemText(4, QCoreApplication.translate("ReportScreen", u"Asset Valuation Report", None))
        self.reportTypeComboBox.setItemText(5, QCoreApplication.translate("ReportScreen", u"Maintenance Schedule", None))

        self.formatLabel.setText(QCoreApplication.translate("ReportScreen", u"Export Format:", None))
        self.formatComboBox.setItemText(0, QCoreApplication.translate("ReportScreen", u"PDF Document", None))
        self.formatComboBox.setItemText(1, QCoreApplication.translate("ReportScreen", u"Excel Spreadsheet (.xlsx)", None))
        self.formatComboBox.setItemText(2, QCoreApplication.translate("ReportScreen", u"CSV File", None))
        self.formatComboBox.setItemText(3, QCoreApplication.translate("ReportScreen", u"Word Document (.docx)", None))

        self.dateRangeLabel.setText(QCoreApplication.translate("ReportScreen", u"Date Range:", None))
        self.toLabel.setText(QCoreApplication.translate("ReportScreen", u"to", None))
        self.exportButton.setText(QCoreApplication.translate("ReportScreen", u"Export Report", None))
        self.reportLogsLabel.setText(QCoreApplication.translate("ReportScreen", u"Report Logs", None))
        self.filterLabel.setText(QCoreApplication.translate("ReportScreen", u"Filter by Date:", None))
        self.filterToLabel.setText(QCoreApplication.translate("ReportScreen", u"to", None))
        self.filterButton.setText(QCoreApplication.translate("ReportScreen", u"Filter", None))
        self.clearFilterButton.setText(QCoreApplication.translate("ReportScreen", u"Clear Filter", None))
        ___qtablewidgetitem = self.reportLogsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ReportScreen", u"Date & Time", None));
        ___qtablewidgetitem1 = self.reportLogsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ReportScreen", u"Report Type", None));
        ___qtablewidgetitem2 = self.reportLogsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ReportScreen", u"Format", None));
        ___qtablewidgetitem3 = self.reportLogsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ReportScreen", u"File Name", None));
        ___qtablewidgetitem4 = self.reportLogsTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ReportScreen", u"Status", None));
        ___qtablewidgetitem5 = self.reportLogsTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ReportScreen", u"Records Count", None));
    # retranslateUi

