# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_table_view.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_AssetTableView(object):
    def setupUi(self, AssetTableView):
        if not AssetTableView.objectName():
            AssetTableView.setObjectName(u"AssetTableView")
        AssetTableView.resize(800, 600)
        self.verticalLayout = QVBoxLayout(AssetTableView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName(u"headerLayout")
        self.categoryLabel = QLabel(AssetTableView)
        self.categoryLabel.setObjectName(u"categoryLabel")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.categoryLabel.setFont(font)

        self.headerLayout.addWidget(self.categoryLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.horizontalSpacer)

        self.searchInput = QLineEdit(AssetTableView)
        self.searchInput.setObjectName(u"searchInput")

        self.headerLayout.addWidget(self.searchInput)


        self.verticalLayout.addLayout(self.headerLayout)

        self.summaryLayout = QHBoxLayout()
        self.summaryLayout.setObjectName(u"summaryLayout")
        self.summaryFramesLayout = QVBoxLayout()
        self.summaryFramesLayout.setObjectName(u"summaryFramesLayout")
        self.categoryAssetsFrame = QFrame(AssetTableView)
        self.categoryAssetsFrame.setObjectName(u"categoryAssetsFrame")
        self.categoryAssetsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.categoryAssetsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.categoryAssetsLayout = QHBoxLayout(self.categoryAssetsFrame)
        self.categoryAssetsLayout.setObjectName(u"categoryAssetsLayout")
        self.categoryAssetsLabel = QLabel(self.categoryAssetsFrame)
        self.categoryAssetsLabel.setObjectName(u"categoryAssetsLabel")

        self.categoryAssetsLayout.addWidget(self.categoryAssetsLabel)

        self.categoryAssetsValue = QLabel(self.categoryAssetsFrame)
        self.categoryAssetsValue.setObjectName(u"categoryAssetsValue")
        self.categoryAssetsValue.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.categoryAssetsLayout.addWidget(self.categoryAssetsValue)


        self.summaryFramesLayout.addWidget(self.categoryAssetsFrame)


        self.summaryLayout.addLayout(self.summaryFramesLayout)

        self.totalAssetsFrame = QFrame(AssetTableView)
        self.totalAssetsFrame.setObjectName(u"totalAssetsFrame")
        self.totalAssetsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.totalAssetsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.totalAssetsLayout = QHBoxLayout(self.totalAssetsFrame)
        self.totalAssetsLayout.setObjectName(u"totalAssetsLayout")
        self.totalAssetsLabel = QLabel(self.totalAssetsFrame)
        self.totalAssetsLabel.setObjectName(u"totalAssetsLabel")

        self.totalAssetsLayout.addWidget(self.totalAssetsLabel)

        self.totalAssetsValue = QLabel(self.totalAssetsFrame)
        self.totalAssetsValue.setObjectName(u"totalAssetsValue")
        self.totalAssetsValue.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.totalAssetsLayout.addWidget(self.totalAssetsValue)


        self.summaryLayout.addWidget(self.totalAssetsFrame)

        self.categoryValueFrame = QFrame(AssetTableView)
        self.categoryValueFrame.setObjectName(u"categoryValueFrame")
        self.categoryValueFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.categoryValueFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.categoryValueLayout = QHBoxLayout(self.categoryValueFrame)
        self.categoryValueLayout.setObjectName(u"categoryValueLayout")
        self.categoryValueLabel = QLabel(self.categoryValueFrame)
        self.categoryValueLabel.setObjectName(u"categoryValueLabel")

        self.categoryValueLayout.addWidget(self.categoryValueLabel)

        self.categoryValueAmount = QLabel(self.categoryValueFrame)
        self.categoryValueAmount.setObjectName(u"categoryValueAmount")
        self.categoryValueAmount.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.categoryValueLayout.addWidget(self.categoryValueAmount)


        self.summaryLayout.addWidget(self.categoryValueFrame)

        self.depreciatableAssetsFrame = QFrame(AssetTableView)
        self.depreciatableAssetsFrame.setObjectName(u"depreciatableAssetsFrame")
        self.depreciatableAssetsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.depreciatableAssetsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.depreciatableAssetsLayout = QHBoxLayout(self.depreciatableAssetsFrame)
        self.depreciatableAssetsLayout.setObjectName(u"depreciatableAssetsLayout")
        self.depreciatableAssetsLabel = QLabel(self.depreciatableAssetsFrame)
        self.depreciatableAssetsLabel.setObjectName(u"depreciatableAssetsLabel")

        self.depreciatableAssetsLayout.addWidget(self.depreciatableAssetsLabel)

        self.depreciatableAssetsValue = QLabel(self.depreciatableAssetsFrame)
        self.depreciatableAssetsValue.setObjectName(u"depreciatableAssetsValue")
        self.depreciatableAssetsValue.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.depreciatableAssetsLayout.addWidget(self.depreciatableAssetsValue)


        self.summaryLayout.addWidget(self.depreciatableAssetsFrame)

        self.depreciatedAssetsFrame = QFrame(AssetTableView)
        self.depreciatedAssetsFrame.setObjectName(u"depreciatedAssetsFrame")
        self.depreciatedAssetsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.depreciatedAssetsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.depreciatedAssetsLayout = QHBoxLayout(self.depreciatedAssetsFrame)
        self.depreciatedAssetsLayout.setObjectName(u"depreciatedAssetsLayout")
        self.depreciatedAssetsLabel = QLabel(self.depreciatedAssetsFrame)
        self.depreciatedAssetsLabel.setObjectName(u"depreciatedAssetsLabel")

        self.depreciatedAssetsLayout.addWidget(self.depreciatedAssetsLabel)

        self.depreciatedAssetsValue = QLabel(self.depreciatedAssetsFrame)
        self.depreciatedAssetsValue.setObjectName(u"depreciatedAssetsValue")
        self.depreciatedAssetsValue.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.depreciatedAssetsLayout.addWidget(self.depreciatedAssetsValue)


        self.summaryLayout.addWidget(self.depreciatedAssetsFrame)

        self.highestValueFrame = QFrame(AssetTableView)
        self.highestValueFrame.setObjectName(u"highestValueFrame")
        self.highestValueFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.highestValueFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.highestValueLayout = QVBoxLayout(self.highestValueFrame)
        self.highestValueLayout.setObjectName(u"highestValueLayout")
        self.highestValueLabel = QLabel(self.highestValueFrame)
        self.highestValueLabel.setObjectName(u"highestValueLabel")

        self.highestValueLayout.addWidget(self.highestValueLabel)

        self.highestValueDetailsLayout = QHBoxLayout()
        self.highestValueDetailsLayout.setObjectName(u"highestValueDetailsLayout")
        self.highestValueName = QLabel(self.highestValueFrame)
        self.highestValueName.setObjectName(u"highestValueName")

        self.highestValueDetailsLayout.addWidget(self.highestValueName)

        self.highestValueAmount = QLabel(self.highestValueFrame)
        self.highestValueAmount.setObjectName(u"highestValueAmount")
        self.highestValueAmount.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.highestValueDetailsLayout.addWidget(self.highestValueAmount)


        self.highestValueLayout.addLayout(self.highestValueDetailsLayout)


        self.summaryLayout.addWidget(self.highestValueFrame)


        self.verticalLayout.addLayout(self.summaryLayout)

        self.assetTable = QTableWidget(AssetTableView)
        if (self.assetTable.columnCount() < 10):
            self.assetTable.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.assetTable.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        self.assetTable.setObjectName(u"assetTable")
        self.assetTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.assetTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.assetTable.setSortingEnabled(True)
        self.assetTable.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.assetTable)


        self.retranslateUi(AssetTableView)

        QMetaObject.connectSlotsByName(AssetTableView)
    # setupUi

    def retranslateUi(self, AssetTableView):
        self.categoryLabel.setText(QCoreApplication.translate("AssetTableView", u"Category Name", None))
        self.searchInput.setPlaceholderText(QCoreApplication.translate("AssetTableView", u"Search assets...", None))
        self.categoryAssetsLabel.setText(QCoreApplication.translate("AssetTableView", u"Category Assets", None))
        self.categoryAssetsValue.setText(QCoreApplication.translate("AssetTableView", u"0", None))
        self.totalAssetsLabel.setText(QCoreApplication.translate("AssetTableView", u"Total Assets", None))
        self.totalAssetsValue.setText(QCoreApplication.translate("AssetTableView", u"0", None))
        self.categoryValueLabel.setText(QCoreApplication.translate("AssetTableView", u"Category Value", None))
        self.categoryValueAmount.setText(QCoreApplication.translate("AssetTableView", u"\u20a60.00", None))
        self.depreciatableAssetsLabel.setText(QCoreApplication.translate("AssetTableView", u"Depreciatable Assets (within 30 days)", None))
        self.depreciatableAssetsValue.setText(QCoreApplication.translate("AssetTableView", u"0", None))
        self.depreciatedAssetsLabel.setText(QCoreApplication.translate("AssetTableView", u"Fully Depreciated Assets", None))
        self.depreciatedAssetsValue.setText(QCoreApplication.translate("AssetTableView", u"0", None))
        self.highestValueLabel.setText(QCoreApplication.translate("AssetTableView", u"Highest Value Asset", None))
        self.highestValueName.setText(QCoreApplication.translate("AssetTableView", u"N/A", None))
        self.highestValueAmount.setText(QCoreApplication.translate("AssetTableView", u"\u20a60.00", None))
        ___qtablewidgetitem = self.assetTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("AssetTableView", u"Asset ID", None));
        ___qtablewidgetitem1 = self.assetTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("AssetTableView", u"Name", None));
        ___qtablewidgetitem2 = self.assetTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("AssetTableView", u"Model Number", None));
        ___qtablewidgetitem3 = self.assetTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("AssetTableView", u"Serial Number", None));
        ___qtablewidgetitem4 = self.assetTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("AssetTableView", u"Department", None));
        ___qtablewidgetitem5 = self.assetTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("AssetTableView", u"Category", None));
        ___qtablewidgetitem6 = self.assetTable.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("AssetTableView", u"Date Registered", None));
        ___qtablewidgetitem7 = self.assetTable.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("AssetTableView", u"Exp. Date", None));
        ___qtablewidgetitem8 = self.assetTable.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("AssetTableView", u"Value", None));
        ___qtablewidgetitem9 = self.assetTable.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("AssetTableView", u"Status", None));
        pass
    # retranslateUi

