# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'recently_deleted.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_RecentlyDeleted(object):
    def setupUi(self, RecentlyDeleted):
        if not RecentlyDeleted.objectName():
            RecentlyDeleted.setObjectName(u"RecentlyDeleted")
        RecentlyDeleted.resize(700, 500)
        self.verticalLayout = QVBoxLayout(RecentlyDeleted)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(RecentlyDeleted)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabUsers = QWidget()
        self.tabUsers.setObjectName(u"tabUsers")
        self.verticalLayout_users = QVBoxLayout(self.tabUsers)
        self.verticalLayout_users.setObjectName(u"verticalLayout_users")
        self.usersTable = QTableWidget(self.tabUsers)
        if (self.usersTable.columnCount() < 4):
            self.usersTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.usersTable.setObjectName(u"usersTable")

        self.verticalLayout_users.addWidget(self.usersTable)

        self.tabWidget.addTab(self.tabUsers, "")
        self.tabAssets = QWidget()
        self.tabAssets.setObjectName(u"tabAssets")
        self.verticalLayout_assets = QVBoxLayout(self.tabAssets)
        self.verticalLayout_assets.setObjectName(u"verticalLayout_assets")
        self.assetsTable = QTableWidget(self.tabAssets)
        if (self.assetsTable.columnCount() < 4):
            self.assetsTable.setColumnCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.assetsTable.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.assetsTable.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.assetsTable.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.assetsTable.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        self.assetsTable.setObjectName(u"assetsTable")

        self.verticalLayout_assets.addWidget(self.assetsTable)

        self.tabWidget.addTab(self.tabAssets, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer)

        self.restoreBtn = QPushButton(RecentlyDeleted)
        self.restoreBtn.setObjectName(u"restoreBtn")

        self.horizontalLayout_buttons.addWidget(self.restoreBtn)

        self.deleteBtn = QPushButton(RecentlyDeleted)
        self.deleteBtn.setObjectName(u"deleteBtn")

        self.horizontalLayout_buttons.addWidget(self.deleteBtn)

        self.closeBtn = QPushButton(RecentlyDeleted)
        self.closeBtn.setObjectName(u"closeBtn")

        self.horizontalLayout_buttons.addWidget(self.closeBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_buttons)


        self.retranslateUi(RecentlyDeleted)

        QMetaObject.connectSlotsByName(RecentlyDeleted)
    # setupUi

    def retranslateUi(self, RecentlyDeleted):
        RecentlyDeleted.setWindowTitle(QCoreApplication.translate("RecentlyDeleted", u"Recently Deleted", None))
        ___qtablewidgetitem = self.usersTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("RecentlyDeleted", u"Email", None));
        ___qtablewidgetitem1 = self.usersTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("RecentlyDeleted", u"Full Name", None));
        ___qtablewidgetitem2 = self.usersTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("RecentlyDeleted", u"Role", None));
        ___qtablewidgetitem3 = self.usersTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("RecentlyDeleted", u"Deleted At", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabUsers), QCoreApplication.translate("RecentlyDeleted", u"Users", None))
        ___qtablewidgetitem4 = self.assetsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("RecentlyDeleted", u"Asset ID", None));
        ___qtablewidgetitem5 = self.assetsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("RecentlyDeleted", u"Name", None));
        ___qtablewidgetitem6 = self.assetsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("RecentlyDeleted", u"Status", None));
        ___qtablewidgetitem7 = self.assetsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("RecentlyDeleted", u"Updated At", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAssets), QCoreApplication.translate("RecentlyDeleted", u"Assets", None))
        self.restoreBtn.setText(QCoreApplication.translate("RecentlyDeleted", u"Restore", None))
        self.deleteBtn.setText(QCoreApplication.translate("RecentlyDeleted", u"Clear", None))
        self.closeBtn.setText(QCoreApplication.translate("RecentlyDeleted", u"Close", None))
    # retranslateUi

