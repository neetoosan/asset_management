# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard_screen.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_DashboardScreen(object):
    def setupUi(self, DashboardScreen):
        if not DashboardScreen.objectName():
            DashboardScreen.setObjectName(u"DashboardScreen")
        DashboardScreen.resize(1200, 800)
        self.mainVerticalLayout = QVBoxLayout(DashboardScreen)
        self.mainVerticalLayout.setObjectName(u"mainVerticalLayout")
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName(u"headerLayout")
        self.assetsLabel = QLabel(DashboardScreen)
        self.assetsLabel.setObjectName(u"assetsLabel")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.assetsLabel.setFont(font)
        self.assetsLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.headerLayout.addWidget(self.assetsLabel)

        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)


        self.mainVerticalLayout.addLayout(self.headerLayout)

        self.summaryCardsLayout = QHBoxLayout()
        self.summaryCardsLayout.setObjectName(u"summaryCardsLayout")
        self.rightColumnLayout = QVBoxLayout()
        self.rightColumnLayout.setObjectName(u"rightColumnLayout")
        self.recentActivitiesFrame = QFrame(DashboardScreen)
        self.recentActivitiesFrame.setObjectName(u"recentActivitiesFrame")
        self.recentActivitiesFrame.setMaximumSize(QSize(16777215, 300))
        self.recentActivitiesFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.recentActivitiesLayout = QVBoxLayout(self.recentActivitiesFrame)
        self.recentActivitiesLayout.setObjectName(u"recentActivitiesLayout")
        self.recentActivitiesLabel = QLabel(self.recentActivitiesFrame)
        self.recentActivitiesLabel.setObjectName(u"recentActivitiesLabel")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.recentActivitiesLabel.setFont(font1)

        self.recentActivitiesLayout.addWidget(self.recentActivitiesLabel)

        self.recentActivitiesList = QListWidget(self.recentActivitiesFrame)
        self.recentActivitiesList.setObjectName(u"recentActivitiesList")

        self.recentActivitiesLayout.addWidget(self.recentActivitiesList)


        self.rightColumnLayout.addWidget(self.recentActivitiesFrame)


        self.summaryCardsLayout.addLayout(self.rightColumnLayout)

        self.totalAssetsFrame = QFrame(DashboardScreen)
        self.totalAssetsFrame.setObjectName(u"totalAssetsFrame")
        self.totalAssetsFrame.setMinimumSize(QSize(200, 100))
        self.totalAssetsFrame.setMaximumSize(QSize(16777215, 100))
        self.totalAssetsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.totalAssetsLayout = QVBoxLayout(self.totalAssetsFrame)
        self.totalAssetsLayout.setObjectName(u"totalAssetsLayout")
        self.totalAssetsTitle = QLabel(self.totalAssetsFrame)
        self.totalAssetsTitle.setObjectName(u"totalAssetsTitle")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.totalAssetsTitle.setFont(font2)
        self.totalAssetsTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.totalAssetsLayout.addWidget(self.totalAssetsTitle)

        self.totalAssetsLabel = QLabel(self.totalAssetsFrame)
        self.totalAssetsLabel.setObjectName(u"totalAssetsLabel")
        font3 = QFont()
        font3.setPointSize(16)
        font3.setBold(True)
        self.totalAssetsLabel.setFont(font3)
        self.totalAssetsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.totalAssetsLayout.addWidget(self.totalAssetsLabel)


        self.summaryCardsLayout.addWidget(self.totalAssetsFrame)

        self.totalValueFrame = QFrame(DashboardScreen)
        self.totalValueFrame.setObjectName(u"totalValueFrame")
        self.totalValueFrame.setMinimumSize(QSize(200, 100))
        self.totalValueFrame.setMaximumSize(QSize(16777215, 100))
        self.totalValueFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.totalValueLayout = QVBoxLayout(self.totalValueFrame)
        self.totalValueLayout.setObjectName(u"totalValueLayout")
        self.totalValueTitle = QLabel(self.totalValueFrame)
        self.totalValueTitle.setObjectName(u"totalValueTitle")
        self.totalValueTitle.setFont(font2)
        self.totalValueTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.totalValueLayout.addWidget(self.totalValueTitle)

        self.totalValueLabel = QLabel(self.totalValueFrame)
        self.totalValueLabel.setObjectName(u"totalValueLabel")
        self.totalValueLabel.setFont(font3)
        self.totalValueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.totalValueLayout.addWidget(self.totalValueLabel)


        self.summaryCardsLayout.addWidget(self.totalValueFrame)

        self.totalCategoriesFrame = QFrame(DashboardScreen)
        self.totalCategoriesFrame.setObjectName(u"totalCategoriesFrame")
        self.totalCategoriesFrame.setMinimumSize(QSize(200, 100))
        self.totalCategoriesFrame.setMaximumSize(QSize(16777215, 100))
        self.totalCategoriesFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.totalCategoriesLayout = QVBoxLayout(self.totalCategoriesFrame)
        self.totalCategoriesLayout.setObjectName(u"totalCategoriesLayout")
        self.totalCategoriesTitle = QLabel(self.totalCategoriesFrame)
        self.totalCategoriesTitle.setObjectName(u"totalCategoriesTitle")
        self.totalCategoriesTitle.setFont(font2)
        self.totalCategoriesTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.totalCategoriesLayout.addWidget(self.totalCategoriesTitle)

        self.totalCategoriesLabel = QLabel(self.totalCategoriesFrame)
        self.totalCategoriesLabel.setObjectName(u"totalCategoriesLabel")
        self.totalCategoriesLabel.setFont(font3)
        self.totalCategoriesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.totalCategoriesLayout.addWidget(self.totalCategoriesLabel)


        self.summaryCardsLayout.addWidget(self.totalCategoriesFrame)


        self.mainVerticalLayout.addLayout(self.summaryCardsLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.mainVerticalLayout.addItem(self.horizontalSpacer)

        self.contentLayout = QHBoxLayout()
        self.contentLayout.setObjectName(u"contentLayout")
        self.leftColumnLayout = QVBoxLayout()
        self.leftColumnLayout.setObjectName(u"leftColumnLayout")
        self.valuationFrame = QFrame(DashboardScreen)
        self.valuationFrame.setObjectName(u"valuationFrame")
        self.valuationFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.valuationLayout = QVBoxLayout(self.valuationFrame)
        self.valuationLayout.setObjectName(u"valuationLayout")
        self.valuationLabel = QLabel(self.valuationFrame)
        self.valuationLabel.setObjectName(u"valuationLabel")
        self.valuationLabel.setMaximumSize(QSize(16777215, 100))
        self.valuationLabel.setFont(font1)

        self.valuationLayout.addWidget(self.valuationLabel)

        self.valuationChartWidget = QWidget(self.valuationFrame)
        self.valuationChartWidget.setObjectName(u"valuationChartWidget")

        self.valuationLayout.addWidget(self.valuationChartWidget)


        self.leftColumnLayout.addWidget(self.valuationFrame)


        self.contentLayout.addLayout(self.leftColumnLayout)

        self.chartsRowLayout = QHBoxLayout()
        self.chartsRowLayout.setObjectName(u"chartsRowLayout")
        self.assetCategoryFrame = QFrame(DashboardScreen)
        self.assetCategoryFrame.setObjectName(u"assetCategoryFrame")
        self.assetCategoryFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.assetCategoryLayout = QVBoxLayout(self.assetCategoryFrame)
        self.assetCategoryLayout.setObjectName(u"assetCategoryLayout")
        self.assetCategoryLabel = QLabel(self.assetCategoryFrame)
        self.assetCategoryLabel.setObjectName(u"assetCategoryLabel")
        self.assetCategoryLabel.setMaximumSize(QSize(16777215, 100))
        self.assetCategoryLabel.setFont(font1)

        self.assetCategoryLayout.addWidget(self.assetCategoryLabel)

        self.assetCategoryPieWidget = QWidget(self.assetCategoryFrame)
        self.assetCategoryPieWidget.setObjectName(u"assetCategoryPieWidget")

        self.assetCategoryLayout.addWidget(self.assetCategoryPieWidget)


        self.chartsRowLayout.addWidget(self.assetCategoryFrame)


        self.contentLayout.addLayout(self.chartsRowLayout)


        self.mainVerticalLayout.addLayout(self.contentLayout)


        self.retranslateUi(DashboardScreen)

        QMetaObject.connectSlotsByName(DashboardScreen)
    # setupUi

    def retranslateUi(self, DashboardScreen):
        self.assetsLabel.setText(QCoreApplication.translate("DashboardScreen", u"ASSETS", None))
        self.recentActivitiesLabel.setText(QCoreApplication.translate("DashboardScreen", u"Recent Activities", None))
        self.totalAssetsTitle.setText(QCoreApplication.translate("DashboardScreen", u"Total Assets", None))
        self.totalAssetsLabel.setText(QCoreApplication.translate("DashboardScreen", u"0", None))
        self.totalValueTitle.setText(QCoreApplication.translate("DashboardScreen", u"Total Value", None))
        self.totalValueLabel.setText(QCoreApplication.translate("DashboardScreen", u"\u20a60.00", None))
        self.totalCategoriesTitle.setText(QCoreApplication.translate("DashboardScreen", u"Total Categories", None))
        self.totalCategoriesLabel.setText(QCoreApplication.translate("DashboardScreen", u"0", None))
        self.valuationLabel.setText(QCoreApplication.translate("DashboardScreen", u"Valuation", None))
        self.assetCategoryLabel.setText(QCoreApplication.translate("DashboardScreen", u"Asset Category", None))
        pass
    # retranslateUi

