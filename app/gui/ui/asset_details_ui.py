# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_details.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_AssetDetails(object):
    def setupUi(self, AssetDetails):
        if not AssetDetails.objectName():
            AssetDetails.setObjectName(u"AssetDetails")
        AssetDetails.resize(480, 500)
        self.verticalLayout = QVBoxLayout(AssetDetails)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelName = QLabel(AssetDetails)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout.addWidget(self.labelName, 0, 0, 1, 1)

        self.nameLabel = QLabel(AssetDetails)
        self.nameLabel.setObjectName(u"nameLabel")

        self.gridLayout.addWidget(self.nameLabel, 0, 1, 1, 1)

        self.labelAssetId = QLabel(AssetDetails)
        self.labelAssetId.setObjectName(u"labelAssetId")

        self.gridLayout.addWidget(self.labelAssetId, 1, 0, 1, 1)

        self.assetIdLabel = QLabel(AssetDetails)
        self.assetIdLabel.setObjectName(u"assetIdLabel")

        self.gridLayout.addWidget(self.assetIdLabel, 1, 1, 1, 1)

        self.labelCategory = QLabel(AssetDetails)
        self.labelCategory.setObjectName(u"labelCategory")

        self.gridLayout.addWidget(self.labelCategory, 2, 0, 1, 1)

        self.categoryLabel = QLabel(AssetDetails)
        self.categoryLabel.setObjectName(u"categoryLabel")

        self.gridLayout.addWidget(self.categoryLabel, 2, 1, 1, 1)

        self.labelDepartment = QLabel(AssetDetails)
        self.labelDepartment.setObjectName(u"labelDepartment")

        self.gridLayout.addWidget(self.labelDepartment, 3, 0, 1, 1)

        self.departmentLabel = QLabel(AssetDetails)
        self.departmentLabel.setObjectName(u"departmentLabel")

        self.gridLayout.addWidget(self.departmentLabel, 3, 1, 1, 1)

        self.labelStatus = QLabel(AssetDetails)
        self.labelStatus.setObjectName(u"labelStatus")

        self.gridLayout.addWidget(self.labelStatus, 4, 0, 1, 1)

        self.statusLabel = QLabel(AssetDetails)
        self.statusLabel.setObjectName(u"statusLabel")

        self.gridLayout.addWidget(self.statusLabel, 4, 1, 1, 1)

        self.labelAcq = QLabel(AssetDetails)
        self.labelAcq.setObjectName(u"labelAcq")

        self.gridLayout.addWidget(self.labelAcq, 5, 0, 1, 1)

        self.acqDateLabel = QLabel(AssetDetails)
        self.acqDateLabel.setObjectName(u"acqDateLabel")

        self.gridLayout.addWidget(self.acqDateLabel, 5, 1, 1, 1)

        self.labelExp = QLabel(AssetDetails)
        self.labelExp.setObjectName(u"labelExp")

        self.gridLayout.addWidget(self.labelExp, 6, 0, 1, 1)

        self.expDateLabel = QLabel(AssetDetails)
        self.expDateLabel.setObjectName(u"expDateLabel")

        self.gridLayout.addWidget(self.expDateLabel, 6, 1, 1, 1)

        self.labelUsefulLife = QLabel(AssetDetails)
        self.labelUsefulLife.setObjectName(u"labelUsefulLife")

        self.gridLayout.addWidget(self.labelUsefulLife, 7, 0, 1, 1)

        self.usefulLifeLabel = QLabel(AssetDetails)
        self.usefulLifeLabel.setObjectName(u"usefulLifeLabel")

        self.gridLayout.addWidget(self.usefulLifeLabel, 7, 1, 1, 1)

        self.labelDepMethod = QLabel(AssetDetails)
        self.labelDepMethod.setObjectName(u"labelDepMethod")

        self.gridLayout.addWidget(self.labelDepMethod, 8, 0, 1, 1)

        self.depMethodLabel = QLabel(AssetDetails)
        self.depMethodLabel.setObjectName(u"depMethodLabel")

        self.gridLayout.addWidget(self.depMethodLabel, 8, 1, 1, 1)

        self.labelDepPercent = QLabel(AssetDetails)
        self.labelDepPercent.setObjectName(u"labelDepPercent")

        self.gridLayout.addWidget(self.labelDepPercent, 9, 0, 1, 1)

        self.depPercentLabel = QLabel(AssetDetails)
        self.depPercentLabel.setObjectName(u"depPercentLabel")

        self.gridLayout.addWidget(self.depPercentLabel, 9, 1, 1, 1)

        self.labelAccumDep = QLabel(AssetDetails)
        self.labelAccumDep.setObjectName(u"labelAccumDep")

        self.gridLayout.addWidget(self.labelAccumDep, 10, 0, 1, 1)

        self.accumDepLabel = QLabel(AssetDetails)
        self.accumDepLabel.setObjectName(u"accumDepLabel")

        self.gridLayout.addWidget(self.accumDepLabel, 10, 1, 1, 1)

        self.labelValue = QLabel(AssetDetails)
        self.labelValue.setObjectName(u"labelValue")

        self.gridLayout.addWidget(self.labelValue, 11, 0, 1, 1)

        self.valueLabel = QLabel(AssetDetails)
        self.valueLabel.setObjectName(u"valueLabel")

        self.gridLayout.addWidget(self.valueLabel, 11, 1, 1, 1)

        self.labelDescription = QLabel(AssetDetails)
        self.labelDescription.setObjectName(u"labelDescription")

        self.gridLayout.addWidget(self.labelDescription, 12, 0, 1, 2)

        self.descriptionText = QTextEdit(AssetDetails)
        self.descriptionText.setObjectName(u"descriptionText")
        self.descriptionText.setReadOnly(True)

        self.gridLayout.addWidget(self.descriptionText, 13, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer)

        self.qrButton = QPushButton(AssetDetails)
        self.qrButton.setObjectName(u"qrButton")

        self.buttonLayout.addWidget(self.qrButton)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(AssetDetails)

        QMetaObject.connectSlotsByName(AssetDetails)
    # setupUi

    def retranslateUi(self, AssetDetails):
        AssetDetails.setWindowTitle(QCoreApplication.translate("AssetDetails", u"Asset Details", None))
        self.labelName.setText(QCoreApplication.translate("AssetDetails", u"Name:", None))
        self.nameLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelAssetId.setText(QCoreApplication.translate("AssetDetails", u"Asset ID:", None))
        self.assetIdLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelCategory.setText(QCoreApplication.translate("AssetDetails", u"Category:", None))
        self.categoryLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelDepartment.setText(QCoreApplication.translate("AssetDetails", u"Department:", None))
        self.departmentLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelStatus.setText(QCoreApplication.translate("AssetDetails", u"Status:", None))
        self.statusLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelAcq.setText(QCoreApplication.translate("AssetDetails", u"Acquisition Date:", None))
        self.acqDateLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelExp.setText(QCoreApplication.translate("AssetDetails", u"Expiry Date:", None))
        self.expDateLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelUsefulLife.setText(QCoreApplication.translate("AssetDetails", u"Useful Life (Years):", None))
        self.usefulLifeLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelDepMethod.setText(QCoreApplication.translate("AssetDetails", u"Depreciation Method:", None))
        self.depMethodLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelDepPercent.setText(QCoreApplication.translate("AssetDetails", u"Annual Depreciation %:", None))
        self.depPercentLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelAccumDep.setText(QCoreApplication.translate("AssetDetails", u"Accumulated Depreciation (\u20a6):", None))
        self.accumDepLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelValue.setText(QCoreApplication.translate("AssetDetails", u"Net Book Value (\u20a6):", None))
        self.valueLabel.setText(QCoreApplication.translate("AssetDetails", u"-", None))
        self.labelDescription.setText(QCoreApplication.translate("AssetDetails", u"Description:", None))
        self.qrButton.setText(QCoreApplication.translate("AssetDetails", u"QR", None))
    # retranslateUi

