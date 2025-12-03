# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_user_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_AddUserDialog(object):
    def setupUi(self, AddUserDialog):
        if not AddUserDialog.objectName():
            AddUserDialog.setObjectName(u"AddUserDialog")
        AddUserDialog.resize(400, 500)
        AddUserDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(AddUserDialog)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(AddUserDialog)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.titleLabel.setFont(font)

        self.verticalLayout.addWidget(self.titleLabel)

        self.formFrame = QFrame(AddUserDialog)
        self.formFrame.setObjectName(u"formFrame")
        self.formFrame.setFrameShape(QFrame.StyledPanel)
        self.formLayout = QFormLayout(self.formFrame)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(15)
        self.nameLabel = QLabel(self.formFrame)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.nameLabel)

        self.nameLineEdit = QLineEdit(self.formFrame)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.nameLineEdit)

        self.emailLabel = QLabel(self.formFrame)
        self.emailLabel.setObjectName(u"emailLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.emailLabel)

        self.emailLineEdit = QLineEdit(self.formFrame)
        self.emailLineEdit.setObjectName(u"emailLineEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.emailLineEdit)

        self.departmentLabel = QLabel(self.formFrame)
        self.departmentLabel.setObjectName(u"departmentLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.departmentLabel)

        self.departmentLineEdit = QLineEdit(self.formFrame)
        self.departmentLineEdit.setObjectName(u"departmentLineEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.departmentLineEdit)

        self.positionLabel = QLabel(self.formFrame)
        self.positionLabel.setObjectName(u"positionLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.positionLabel)

        self.positionLineEdit = QLineEdit(self.formFrame)
        self.positionLineEdit.setObjectName(u"positionLineEdit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.positionLineEdit)

        self.roleLabel = QLabel(self.formFrame)
        self.roleLabel.setObjectName(u"roleLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.roleLabel)

        self.roleComboBox = QComboBox(self.formFrame)
        self.roleComboBox.addItem("")
        self.roleComboBox.addItem("")
        self.roleComboBox.addItem("")
        self.roleComboBox.setObjectName(u"roleComboBox")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.roleComboBox)

        self.passwordLabel = QLabel(self.formFrame)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.passwordLabel)

        self.passwordLineEdit = QLineEdit(self.formFrame)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.passwordLineEdit)

        self.confirmPasswordLabel = QLabel(self.formFrame)
        self.confirmPasswordLabel.setObjectName(u"confirmPasswordLabel")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.confirmPasswordLabel)

        self.confirmPasswordLineEdit = QLineEdit(self.formFrame)
        self.confirmPasswordLineEdit.setObjectName(u"confirmPasswordLineEdit")
        self.confirmPasswordLineEdit.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.confirmPasswordLineEdit)

        self.statusLabel = QLabel(self.formFrame)
        self.statusLabel.setObjectName(u"statusLabel")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.statusLabel)

        self.statusComboBox = QComboBox(self.formFrame)
        self.statusComboBox.addItem("")
        self.statusComboBox.addItem("")
        self.statusComboBox.addItem("")
        self.statusComboBox.setObjectName(u"statusComboBox")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.statusComboBox)


        self.verticalLayout.addWidget(self.formFrame)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer)

        self.saveButton = QPushButton(AddUserDialog)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMinimumSize(QSize(80, 30))

        self.buttonLayout.addWidget(self.saveButton)

        self.cancelButton = QPushButton(AddUserDialog)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setMinimumSize(QSize(80, 30))

        self.buttonLayout.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(AddUserDialog)
        self.cancelButton.clicked.connect(AddUserDialog.reject)
        self.saveButton.clicked.connect(AddUserDialog.accept)

        QMetaObject.connectSlotsByName(AddUserDialog)
    # setupUi

    def retranslateUi(self, AddUserDialog):
        AddUserDialog.setWindowTitle(QCoreApplication.translate("AddUserDialog", u"Add User", None))
        self.titleLabel.setText(QCoreApplication.translate("AddUserDialog", u"Add New User", None))
        self.nameLabel.setText(QCoreApplication.translate("AddUserDialog", u"Full Name:", None))
        self.nameLineEdit.setPlaceholderText(QCoreApplication.translate("AddUserDialog", u"Enter full name", None))
        self.emailLabel.setText(QCoreApplication.translate("AddUserDialog", u"Email:", None))
        self.emailLineEdit.setPlaceholderText(QCoreApplication.translate("AddUserDialog", u"Enter email address", None))
        self.departmentLabel.setText(QCoreApplication.translate("AddUserDialog", u"Department:", None))
        self.departmentLineEdit.setPlaceholderText(QCoreApplication.translate("AddUserDialog", u"Enter department", None))
        self.positionLabel.setText(QCoreApplication.translate("AddUserDialog", u"Position:", None))
        self.positionLineEdit.setPlaceholderText(QCoreApplication.translate("AddUserDialog", u"Enter position/title", None))
        self.roleLabel.setText(QCoreApplication.translate("AddUserDialog", u"Role:", None))
        self.roleComboBox.setItemText(0, QCoreApplication.translate("AddUserDialog", u"User", None))
        self.roleComboBox.setItemText(1, QCoreApplication.translate("AddUserDialog", u"Admin", None))
        self.roleComboBox.setItemText(2, QCoreApplication.translate("AddUserDialog", u"Viewer", None))

        self.passwordLabel.setText(QCoreApplication.translate("AddUserDialog", u"Password:", None))
        self.passwordLineEdit.setPlaceholderText(QCoreApplication.translate("AddUserDialog", u"Enter password", None))
        self.confirmPasswordLabel.setText(QCoreApplication.translate("AddUserDialog", u"Confirm Password:", None))
        self.confirmPasswordLineEdit.setPlaceholderText(QCoreApplication.translate("AddUserDialog", u"Confirm password", None))
        self.statusLabel.setText(QCoreApplication.translate("AddUserDialog", u"Status:", None))
        self.statusComboBox.setItemText(0, QCoreApplication.translate("AddUserDialog", u"Active", None))
        self.statusComboBox.setItemText(1, QCoreApplication.translate("AddUserDialog", u"Inactive", None))
        self.statusComboBox.setItemText(2, QCoreApplication.translate("AddUserDialog", u"Suspended", None))

        self.saveButton.setText(QCoreApplication.translate("AddUserDialog", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("AddUserDialog", u"Cancel", None))
    # retranslateUi

