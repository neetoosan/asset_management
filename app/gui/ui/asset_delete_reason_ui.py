# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_delete_reason.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_AssetDeleteReason(object):
    def setupUi(self, AssetDeleteReason):
        if not AssetDeleteReason.objectName():
            AssetDeleteReason.setObjectName(u"AssetDeleteReason")
        AssetDeleteReason.resize(400, 220)
        self.verticalLayout = QVBoxLayout(AssetDeleteReason)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(AssetDeleteReason)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.reasonEdit = QTextEdit(AssetDeleteReason)
        self.reasonEdit.setObjectName(u"reasonEdit")

        self.verticalLayout.addWidget(self.reasonEdit)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer)

        self.cancelBtn = QPushButton(AssetDeleteReason)
        self.cancelBtn.setObjectName(u"cancelBtn")

        self.buttonLayout.addWidget(self.cancelBtn)

        self.okBtn = QPushButton(AssetDeleteReason)
        self.okBtn.setObjectName(u"okBtn")

        self.buttonLayout.addWidget(self.okBtn)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(AssetDeleteReason)

        QMetaObject.connectSlotsByName(AssetDeleteReason)
    # setupUi

    def retranslateUi(self, AssetDeleteReason):
        AssetDeleteReason.setWindowTitle(QCoreApplication.translate("AssetDeleteReason", u"Asset Deletion Reason", None))
        self.label.setText(QCoreApplication.translate("AssetDeleteReason", u"Please provide a reason for deleting this asset:", None))
        self.cancelBtn.setText(QCoreApplication.translate("AssetDeleteReason", u"Cancel", None))
        self.okBtn.setText(QCoreApplication.translate("AssetDeleteReason", u"OK", None))
    # retranslateUi

