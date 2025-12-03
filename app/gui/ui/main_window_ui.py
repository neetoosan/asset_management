# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.navFrame = QFrame(self.centralwidget)
        self.navFrame.setObjectName(u"navFrame")
        self.navFrame.setFrameShape(QFrame.StyledPanel)
        self.verticalLayout = QVBoxLayout(self.navFrame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.logoFrame = QFrame(self.navFrame)
        self.logoFrame.setObjectName(u"logoFrame")
        self.logoFrame.setMinimumSize(QSize(200, 60))
        self.logoFrame.setMaximumSize(QSize(200, 60))
        self.logoFrame.setFrameShape(QFrame.NoFrame)
        self.logoFrame.setFrameShadow(QFrame.Plain)
        self.logoLayout = QHBoxLayout(self.logoFrame)
        self.logoLayout.setSpacing(0)
        self.logoLayout.setObjectName(u"logoLayout")
        self.logoLayout.setContentsMargins(10, 5, 10, 5)
        self.logoLabel = QLabel(self.logoFrame)
        self.logoLabel.setObjectName(u"logoLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logoLabel.sizePolicy().hasHeightForWidth())
        self.logoLabel.setSizePolicy(sizePolicy)
        self.logoLabel.setMinimumSize(QSize(140, 30))
        self.logoLabel.setMaximumSize(QSize(180, 40))
        self.logoLabel.setAlignment(Qt.AlignCenter)
        self.logoLabel.setScaledContents(False)

        self.logoLayout.addWidget(self.logoLabel)


        self.verticalLayout.addWidget(self.logoFrame)

        self.dashboardBtn = QPushButton(self.navFrame)
        self.dashboardBtn.setObjectName(u"dashboardBtn")
        icon = QIcon()
        icon.addFile(u":/icons/dashboard", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dashboardBtn.setIcon(icon)

        self.verticalLayout.addWidget(self.dashboardBtn)

        self.assetsBtn = QPushButton(self.navFrame)
        self.assetsBtn.setObjectName(u"assetsBtn")

        self.verticalLayout.addWidget(self.assetsBtn)

        self.assetScrollArea = QScrollArea(self.navFrame)
        self.assetScrollArea.setObjectName(u"assetScrollArea")
        self.assetScrollArea.setWidgetResizable(True)
        self.assetSubMenu = QWidget()
        self.assetSubMenu.setObjectName(u"assetSubMenu")
        self.assetSubMenuLayout = QVBoxLayout(self.assetSubMenu)
        self.assetSubMenuLayout.setSpacing(1)
        self.assetSubMenuLayout.setObjectName(u"assetSubMenuLayout")
        self.assetSubMenuLayout.setContentsMargins(10, 2, 5, 2)
        self.allAssetsBtn = QPushButton(self.assetSubMenu)
        self.allAssetsBtn.setObjectName(u"allAssetsBtn")
        self.allAssetsBtn.setStyleSheet(u"color: white; text-align: left; padding: 8px;")

        self.assetSubMenuLayout.addWidget(self.allAssetsBtn)

        self.assetScrollArea.setWidget(self.assetSubMenu)

        self.verticalLayout.addWidget(self.assetScrollArea)

        self.addAssetBtn = QPushButton(self.navFrame)
        self.addAssetBtn.setObjectName(u"addAssetBtn")
        self.addAssetBtn.setStyleSheet(u"color: white; text-align: left; padding: 10px; margin-left: 20px;")
        icon1 = QIcon()
        icon1.addFile(u":/icons/plus", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addAssetBtn.setIcon(icon1)

        self.verticalLayout.addWidget(self.addAssetBtn)

        self.reportsBtn = QPushButton(self.navFrame)
        self.reportsBtn.setObjectName(u"reportsBtn")
        self.reportsBtn.setStyleSheet(u"color: white; text-align: left; padding: 10px;")

        self.verticalLayout.addWidget(self.reportsBtn)

        self.notificationsBtn = QPushButton(self.navFrame)
        self.notificationsBtn.setObjectName(u"notificationsBtn")
        self.notificationsBtn.setStyleSheet(u"color: white; text-align: left; padding: 10px;")

        self.verticalLayout.addWidget(self.notificationsBtn)

        self.adminBtn = QPushButton(self.navFrame)
        self.adminBtn.setObjectName(u"adminBtn")
        self.adminBtn.setStyleSheet(u"color: white; text-align: left; padding: 10px;")

        self.verticalLayout.addWidget(self.adminBtn)

        self.settingsBtn = QPushButton(self.navFrame)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setStyleSheet(u"color: white; text-align: left; padding: 10px;")

        self.verticalLayout.addWidget(self.settingsBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.logoutBtn = QPushButton(self.navFrame)
        self.logoutBtn.setObjectName(u"logoutBtn")
        self.logoutBtn.setStyleSheet(u"color: white; text-align: left; padding: 10px;")

        self.verticalLayout.addWidget(self.logoutBtn)


        self.horizontalLayout.addWidget(self.navFrame)

        self.contentStack = QStackedWidget(self.centralwidget)
        self.contentStack.setObjectName(u"contentStack")
        self.dashboardPage = QWidget()
        self.dashboardPage.setObjectName(u"dashboardPage")
        self.contentStack.addWidget(self.dashboardPage)
        self.assetsPage = QWidget()
        self.assetsPage.setObjectName(u"assetsPage")
        self.contentStack.addWidget(self.assetsPage)
        self.notificationsPage = QWidget()
        self.notificationsPage.setObjectName(u"notificationsPage")
        self.contentStack.addWidget(self.notificationsPage)
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.contentStack.addWidget(self.settingsPage)
        self.reportsPage = QWidget()
        self.reportsPage.setObjectName(u"reportsPage")
        self.contentStack.addWidget(self.reportsPage)
        self.adminPage = QWidget()
        self.adminPage.setObjectName(u"adminPage")
        self.contentStack.addWidget(self.adminPage)

        self.horizontalLayout.addWidget(self.contentStack)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Asset Management System", None))
        self.logoLabel.setText("")
        self.dashboardBtn.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.assetsBtn.setText(QCoreApplication.translate("MainWindow", u"Assets \u25bc", None))
        self.allAssetsBtn.setText(QCoreApplication.translate("MainWindow", u"All Assets", None))
        self.addAssetBtn.setText(QCoreApplication.translate("MainWindow", u"Add Asset", None))
        self.reportsBtn.setText(QCoreApplication.translate("MainWindow", u"Reports", None))
        self.notificationsBtn.setText(QCoreApplication.translate("MainWindow", u"Notifications", None))
        self.adminBtn.setText(QCoreApplication.translate("MainWindow", u"Admin", None))
        self.settingsBtn.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.logoutBtn.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
    # retranslateUi

