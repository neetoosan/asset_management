# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audit_entry_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_AuditEntryDialog(object):
    def setupUi(self, AuditEntryDialog):
        if not AuditEntryDialog.objectName():
            AuditEntryDialog.setObjectName(u"AuditEntryDialog")
        AuditEntryDialog.resize(480, 320)
        self.verticalLayout = QVBoxLayout(AuditEntryDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainHBox = QHBoxLayout()
        self.mainHBox.setObjectName(u"mainHBox")
        self.auditList = QListWidget(AuditEntryDialog)
        self.auditList.setObjectName(u"auditList")
        self.auditList.setMinimumWidth(160)

        self.mainHBox.addWidget(self.auditList)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelWho = QLabel(AuditEntryDialog)
        self.labelWho.setObjectName(u"labelWho")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelWho)

        self.whoValue = QLabel(AuditEntryDialog)
        self.whoValue.setObjectName(u"whoValue")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.whoValue)

        self.labelWhen = QLabel(AuditEntryDialog)
        self.labelWhen.setObjectName(u"labelWhen")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelWhen)

        self.whenValue = QLabel(AuditEntryDialog)
        self.whenValue.setObjectName(u"whenValue")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.whenValue)

        self.labelAction = QLabel(AuditEntryDialog)
        self.labelAction.setObjectName(u"labelAction")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelAction)

        self.actionValue = QLabel(AuditEntryDialog)
        self.actionValue.setObjectName(u"actionValue")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.actionValue)

        self.labelDescription = QLabel(AuditEntryDialog)
        self.labelDescription.setObjectName(u"labelDescription")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelDescription)

        self.descriptionValue = QTextEdit(AuditEntryDialog)
        self.descriptionValue.setObjectName(u"descriptionValue")
        self.descriptionValue.setReadOnly(True)
        self.descriptionValue.setMinimumHeight(120)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.descriptionValue)


        self.mainHBox.addLayout(self.formLayout)


        self.verticalLayout.addLayout(self.mainHBox)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer)

        self.restoreBtn = QPushButton(AuditEntryDialog)
        self.restoreBtn.setObjectName(u"restoreBtn")

        self.buttonLayout.addWidget(self.restoreBtn)

        self.deleteBtn = QPushButton(AuditEntryDialog)
        self.deleteBtn.setObjectName(u"deleteBtn")

        self.buttonLayout.addWidget(self.deleteBtn)

        self.closeBtn = QPushButton(AuditEntryDialog)
        self.closeBtn.setObjectName(u"closeBtn")

        self.buttonLayout.addWidget(self.closeBtn)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(AuditEntryDialog)

        QMetaObject.connectSlotsByName(AuditEntryDialog)
    # setupUi

    def retranslateUi(self, AuditEntryDialog):
        AuditEntryDialog.setWindowTitle(QCoreApplication.translate("AuditEntryDialog", u"Audit Entry Details", None))
        self.restoreBtn.setText(QCoreApplication.translate("AuditEntryDialog", u"Restore", None))
        self.deleteBtn.setText(QCoreApplication.translate("AuditEntryDialog", u"Delete", None))
        self.closeBtn.setText(QCoreApplication.translate("AuditEntryDialog", u"Close", None))
    # retranslateUi

