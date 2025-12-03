# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'admin_screen.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QScrollArea, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_AdminScreen(object):
    def setupUi(self, AdminScreen):
        if not AdminScreen.objectName():
            AdminScreen.setObjectName(u"AdminScreen")
        AdminScreen.resize(1000, 600)
        self.horizontalLayout = QHBoxLayout(AdminScreen)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftPanelLayout = QVBoxLayout()
        self.leftPanelLayout.setSpacing(10)
        self.leftPanelLayout.setObjectName(u"leftPanelLayout")
        self.adminHeaderLabel = QLabel(AdminScreen)
        self.adminHeaderLabel.setObjectName(u"adminHeaderLabel")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.adminHeaderLabel.setFont(font)
        self.adminHeaderLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.leftPanelLayout.addWidget(self.adminHeaderLabel)

        self.notificationsFrame = QFrame(AdminScreen)
        self.notificationsFrame.setObjectName(u"notificationsFrame")
        self.notificationsFrame.setMinimumSize(QSize(300, 250))
        self.notificationsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout = QVBoxLayout(self.notificationsFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.notificationsLabel = QLabel(self.notificationsFrame)
        self.notificationsLabel.setObjectName(u"notificationsLabel")
        self.notificationsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.notificationsLabel)

        self.notificationsList = QListWidget(self.notificationsFrame)
        self.notificationsList.setObjectName(u"notificationsList")

        self.verticalLayout.addWidget(self.notificationsList)

        self.recycleBtn = QPushButton(self.notificationsFrame)
        self.recycleBtn.setObjectName(u"recycleBtn")
        self.recycleBtn.setMaximumSize(QSize(120, 40))

        self.verticalLayout.addWidget(self.recycleBtn)


        self.leftPanelLayout.addWidget(self.notificationsFrame)

        self.auditLogsFrame = QFrame(AdminScreen)
        self.auditLogsFrame.setObjectName(u"auditLogsFrame")
        self.auditLogsFrame.setMinimumSize(QSize(300, 250))
        self.auditLogsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_2 = QVBoxLayout(self.auditLogsFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.auditLogsLabel = QLabel(self.auditLogsFrame)
        self.auditLogsLabel.setObjectName(u"auditLogsLabel")
        self.auditLogsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.auditLogsLabel)

        self.auditLogsTable = QTableWidget(self.auditLogsFrame)
        if (self.auditLogsTable.columnCount() < 3):
            self.auditLogsTable.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.auditLogsTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.auditLogsTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.auditLogsTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.auditLogsTable.setObjectName(u"auditLogsTable")

        self.verticalLayout_2.addWidget(self.auditLogsTable)


        self.leftPanelLayout.addWidget(self.auditLogsFrame)


        self.horizontalLayout.addLayout(self.leftPanelLayout)

        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName(u"headerLayout")

        self.horizontalLayout.addLayout(self.headerLayout)

        self.rightPanelLayout = QVBoxLayout()
        self.rightPanelLayout.setSpacing(10)
        self.rightPanelLayout.setObjectName(u"rightPanelLayout")
        self.userManagementFrame = QFrame(AdminScreen)
        self.userManagementFrame.setObjectName(u"userManagementFrame")
        self.userManagementFrame.setMaximumSize(QSize(16777215, 300))
        self.userManagementFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_3 = QVBoxLayout(self.userManagementFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.userManagementLabel = QLabel(self.userManagementFrame)
        self.userManagementLabel.setObjectName(u"userManagementLabel")
        self.userManagementLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.userManagementLabel)

        self.addUserBtn = QPushButton(self.userManagementFrame)
        self.addUserBtn.setObjectName(u"addUserBtn")

        self.horizontalLayout_2.addWidget(self.addUserBtn)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.usersTable = QTableWidget(self.userManagementFrame)
        if (self.usersTable.columnCount() < 5):
            self.usersTable.setColumnCount(5)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(3, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.usersTable.setHorizontalHeaderItem(4, __qtablewidgetitem7)
        self.usersTable.setObjectName(u"usersTable")
        self.usersTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_3.addWidget(self.usersTable)


        self.rightPanelLayout.addWidget(self.userManagementFrame)

        self.userPermissionsFrame = QFrame(AdminScreen)
        self.userPermissionsFrame.setObjectName(u"userPermissionsFrame")
        self.userPermissionsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.verticalLayout_4 = QVBoxLayout(self.userPermissionsFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.permissionsHeaderLayout = QHBoxLayout()
        self.permissionsHeaderLayout.setObjectName(u"permissionsHeaderLayout")
        self.userPermissionsLabel = QLabel(self.userPermissionsFrame)
        self.userPermissionsLabel.setObjectName(u"userPermissionsLabel")
        self.userPermissionsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.permissionsHeaderLayout.addWidget(self.userPermissionsLabel)

        self.savePermissionsBtn = QPushButton(self.userPermissionsFrame)
        self.savePermissionsBtn.setObjectName(u"savePermissionsBtn")

        self.permissionsHeaderLayout.addWidget(self.savePermissionsBtn)


        self.verticalLayout_4.addLayout(self.permissionsHeaderLayout)

        self.selectedUserLabel = QLabel(self.userPermissionsFrame)
        self.selectedUserLabel.setObjectName(u"selectedUserLabel")
        self.selectedUserLabel.setAlignment(Qt.AlignmentFlag.AlignLeading)

        self.verticalLayout_4.addWidget(self.selectedUserLabel)

        self.permissionsScrollArea = QScrollArea(self.userPermissionsFrame)
        self.permissionsScrollArea.setObjectName(u"permissionsScrollArea")
        self.permissionsScrollArea.setWidgetResizable(True)
        self.permissionsWidget = QWidget()
        self.permissionsWidget.setObjectName(u"permissionsWidget")
        self.permissionsWidget.setGeometry(QRect(0, 0, 455, 208))
        self.permissionsLayout = QVBoxLayout(self.permissionsWidget)
        self.permissionsLayout.setObjectName(u"permissionsLayout")
        self.roleGroupBox = QGroupBox(self.permissionsWidget)
        self.roleGroupBox.setObjectName(u"roleGroupBox")
        self.roleLayout = QVBoxLayout(self.roleGroupBox)
        self.roleLayout.setObjectName(u"roleLayout")

        self.permissionsLayout.addWidget(self.roleGroupBox)

        self.permissionsGroupBox = QGroupBox(self.permissionsWidget)
        self.permissionsGroupBox.setObjectName(u"permissionsGroupBox")
        self.permissionsCheckboxLayout = QVBoxLayout(self.permissionsGroupBox)
        self.permissionsCheckboxLayout.setObjectName(u"permissionsCheckboxLayout")

        self.permissionsLayout.addWidget(self.permissionsGroupBox)

        self.permissionsScrollArea.setWidget(self.permissionsWidget)

        self.verticalLayout_4.addWidget(self.permissionsScrollArea)


        self.rightPanelLayout.addWidget(self.userPermissionsFrame)


        self.horizontalLayout.addLayout(self.rightPanelLayout)


        self.retranslateUi(AdminScreen)

        QMetaObject.connectSlotsByName(AdminScreen)
    # setupUi

    def retranslateUi(self, AdminScreen):
        self.adminHeaderLabel.setText(QCoreApplication.translate("AdminScreen", u"ADMIN", None))
        self.notificationsLabel.setText(QCoreApplication.translate("AdminScreen", u"System Notifications", None))
        self.recycleBtn.setText(QCoreApplication.translate("AdminScreen", u"RECYCLE", None))
        self.auditLogsLabel.setText(QCoreApplication.translate("AdminScreen", u"Audit Logs", None))
        ___qtablewidgetitem = self.auditLogsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("AdminScreen", u"Date", None));
        ___qtablewidgetitem1 = self.auditLogsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("AdminScreen", u"User", None));
        ___qtablewidgetitem2 = self.auditLogsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("AdminScreen", u"Action", None));
        self.userManagementLabel.setText(QCoreApplication.translate("AdminScreen", u"User Management", None))
        self.addUserBtn.setText(QCoreApplication.translate("AdminScreen", u"Add User", None))
        ___qtablewidgetitem3 = self.usersTable.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("AdminScreen", u"Username", None));
        ___qtablewidgetitem4 = self.usersTable.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("AdminScreen", u"Full Name", None));
        ___qtablewidgetitem5 = self.usersTable.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("AdminScreen", u"Role", None));
        ___qtablewidgetitem6 = self.usersTable.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("AdminScreen", u"Status", None));
        ___qtablewidgetitem7 = self.usersTable.horizontalHeaderItem(4)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("AdminScreen", u"E-D-R", None));
        self.userPermissionsLabel.setText(QCoreApplication.translate("AdminScreen", u"User Permissions", None))
        self.savePermissionsBtn.setText(QCoreApplication.translate("AdminScreen", u"Save Permissions", None))
        self.selectedUserLabel.setText(QCoreApplication.translate("AdminScreen", u"Select a user to edit permissions", None))
        self.roleGroupBox.setTitle(QCoreApplication.translate("AdminScreen", u"User Role", None))
        self.permissionsGroupBox.setTitle(QCoreApplication.translate("AdminScreen", u"Permissions", None))
        pass
    # retranslateUi

