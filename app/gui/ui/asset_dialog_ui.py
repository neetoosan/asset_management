# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QComboBox,
    QDateEdit, QDialog, QDialogButtonBox, QDoubleSpinBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QSpinBox, QTextEdit, QVBoxLayout, QWidget)

class Ui_AssetDialog(object):
    def setupUi(self, AssetDialog):
        if not AssetDialog.objectName():
            AssetDialog.setObjectName(u"AssetDialog")
        AssetDialog.setMinimumWidth(800)
        AssetDialog.setMinimumHeight(600)
        self.verticalLayout = QVBoxLayout(AssetDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelId = QLabel(AssetDialog)
        self.labelId.setObjectName(u"labelId")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelId)

        self.assetIdInput = QLineEdit(AssetDialog)
        self.assetIdInput.setObjectName(u"assetIdInput")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.assetIdInput)

        self.labelDesc = QLabel(AssetDialog)
        self.labelDesc.setObjectName(u"labelDesc")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelDesc)

        self.descriptionInput = QTextEdit(AssetDialog)
        self.descriptionInput.setObjectName(u"descriptionInput")
        self.descriptionInput.setMaximumHeight(60)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.descriptionInput)

        self.labelCategory = QLabel(AssetDialog)
        self.labelCategory.setObjectName(u"labelCategory")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelCategory)

        self.categoryCombo = QComboBox(AssetDialog)
        self.categoryCombo.setObjectName(u"categoryCombo")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.categoryCombo)

        self.labelSubCategory = QLabel(AssetDialog)
        self.labelSubCategory.setObjectName(u"labelSubCategory")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelSubCategory)

        self.subCategoryCombo = QComboBox(AssetDialog)
        self.subCategoryCombo.setObjectName(u"subCategoryCombo")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.subCategoryCombo)

        self.labelAcquisition = QLabel(AssetDialog)
        self.labelAcquisition.setObjectName(u"labelAcquisition")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelAcquisition)

        self.acquisitionDateEdit = QDateEdit(AssetDialog)
        self.acquisitionDateEdit.setObjectName(u"acquisitionDateEdit")
        self.acquisitionDateEdit.setCalendarPopup(True)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.acquisitionDateEdit)

        self.labelSupplier = QLabel(AssetDialog)
        self.labelSupplier.setObjectName(u"labelSupplier")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelSupplier)

        self.supplierInput = QLineEdit(AssetDialog)
        self.supplierInput.setObjectName(u"supplierInput")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.supplierInput)

        self.labelQuantity = QLabel(AssetDialog)
        self.labelQuantity.setObjectName(u"labelQuantity")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.labelQuantity)

        self.quantitySpinBox = QSpinBox(AssetDialog)
        self.quantitySpinBox.setObjectName(u"quantitySpinBox")
        self.quantitySpinBox.setMinimum(1)
        self.quantitySpinBox.setMaximum(999999)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.quantitySpinBox)

        self.labelUnitCost = QLabel(AssetDialog)
        self.labelUnitCost.setObjectName(u"labelUnitCost")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.labelUnitCost)

        self.unitCostSpinBox = QDoubleSpinBox(AssetDialog)
        self.unitCostSpinBox.setObjectName(u"unitCostSpinBox")
        self.unitCostSpinBox.setDecimals(2)
        self.unitCostSpinBox.setMinimum(0)
        self.unitCostSpinBox.setMaximum(0)
        self.unitCostSpinBox.setSingleStep(0)
        self.unitCostSpinBox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.unitCostSpinBox.setAccelerated(True)

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.unitCostSpinBox)

        self.labelTotalCost = QLabel(AssetDialog)
        self.labelTotalCost.setObjectName(u"labelTotalCost")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.labelTotalCost)

        self.totalCostInput = QLineEdit(AssetDialog)
        self.totalCostInput.setObjectName(u"totalCostInput")
        self.totalCostInput.setReadOnly(True)

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.totalCostInput)

        self.labelUsefulLife = QLabel(AssetDialog)
        self.labelUsefulLife.setObjectName(u"labelUsefulLife")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.labelUsefulLife)

        self.usefulLifeSpinBox = QSpinBox(AssetDialog)
        self.usefulLifeSpinBox.setObjectName(u"usefulLifeSpinBox")
        self.usefulLifeSpinBox.setMinimum(1)
        self.usefulLifeSpinBox.setMaximum(50)

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.usefulLifeSpinBox)

        self.labelDepMethod = QLabel(AssetDialog)
        self.labelDepMethod.setObjectName(u"labelDepMethod")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.labelDepMethod)

        self.depreciationMethodCombo = QComboBox(AssetDialog)
        self.depreciationMethodCombo.setObjectName(u"depreciationMethodCombo")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.depreciationMethodCombo)

        self.labelDepPercentage = QLabel(AssetDialog)
        self.labelDepPercentage.setObjectName(u"labelDepPercentage")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.labelDepPercentage)

        self.depreciationPercentageSpinBox = QDoubleSpinBox(AssetDialog)
        self.depreciationPercentageSpinBox.setObjectName(u"depreciationPercentageSpinBox")
        self.depreciationPercentageSpinBox.setDecimals(2)
        self.depreciationPercentageSpinBox.setMinimum(0)
        self.depreciationPercentageSpinBox.setMaximum(0)
        self.depreciationPercentageSpinBox.setSingleStep(0)

        self.formLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.depreciationPercentageSpinBox)

        self.labelAnnualDep = QLabel(AssetDialog)
        self.labelAnnualDep.setObjectName(u"labelAnnualDep")

        self.formLayout.setWidget(12, QFormLayout.ItemRole.LabelRole, self.labelAnnualDep)

        self.annualDepreciationInput = QLineEdit(AssetDialog)
        self.annualDepreciationInput.setObjectName(u"annualDepreciationInput")
        self.annualDepreciationInput.setReadOnly(True)

        self.formLayout.setWidget(12, QFormLayout.ItemRole.FieldRole, self.annualDepreciationInput)

        self.labelLocation = QLabel(AssetDialog)
        self.labelLocation.setObjectName(u"labelLocation")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.LabelRole, self.labelLocation)

        self.locationCombo = QComboBox(AssetDialog)
        self.locationCombo.setObjectName(u"locationCombo")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.FieldRole, self.locationCombo)

        self.labelModelNumber = QLabel(AssetDialog)
        self.labelModelNumber.setObjectName(u"labelModelNumber")

        self.formLayout.setWidget(14, QFormLayout.ItemRole.LabelRole, self.labelModelNumber)

        self.modelNumberInput = QLineEdit(AssetDialog)
        self.modelNumberInput.setObjectName(u"modelNumberInput")

        self.formLayout.setWidget(14, QFormLayout.ItemRole.FieldRole, self.modelNumberInput)

        self.labelSerialNumber = QLabel(AssetDialog)
        self.labelSerialNumber.setObjectName(u"labelSerialNumber")

        self.formLayout.setWidget(15, QFormLayout.ItemRole.LabelRole, self.labelSerialNumber)

        self.serialNumberInput = QLineEdit(AssetDialog)
        self.serialNumberInput.setObjectName(u"serialNumberInput")

        self.formLayout.setWidget(15, QFormLayout.ItemRole.FieldRole, self.serialNumberInput)

        self.labelCustodian = QLabel(AssetDialog)
        self.labelCustodian.setObjectName(u"labelCustodian")

        self.formLayout.setWidget(16, QFormLayout.ItemRole.LabelRole, self.labelCustodian)

        self.custodianInput = QLineEdit(AssetDialog)
        self.custodianInput.setObjectName(u"custodianInput")

        self.formLayout.setWidget(16, QFormLayout.ItemRole.FieldRole, self.custodianInput)

        self.labelRemarks = QLabel(AssetDialog)
        self.labelRemarks.setObjectName(u"labelRemarks")

        self.formLayout.setWidget(17, QFormLayout.ItemRole.LabelRole, self.labelRemarks)

        self.remarksText = QTextEdit(AssetDialog)
        self.remarksText.setObjectName(u"remarksText")

        self.formLayout.setWidget(17, QFormLayout.ItemRole.FieldRole, self.remarksText)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(AssetDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AssetDialog)
        self.buttonBox.accepted.connect(AssetDialog.accept)
        self.buttonBox.rejected.connect(AssetDialog.reject)

        QMetaObject.connectSlotsByName(AssetDialog)
    # setupUi

    def retranslateUi(self, AssetDialog):
        AssetDialog.setWindowTitle(QCoreApplication.translate("AssetDialog", u"Add/Edit Asset", None))
        self.labelId.setText(QCoreApplication.translate("AssetDialog", u"Asset ID:", None))
        self.labelDesc.setText(QCoreApplication.translate("AssetDialog", u"Asset Description:", None))
        self.labelCategory.setText(QCoreApplication.translate("AssetDialog", u"Category:", None))
        self.labelSubCategory.setText(QCoreApplication.translate("AssetDialog", u"Sub-Category:", None))
        self.labelAcquisition.setText(QCoreApplication.translate("AssetDialog", u"Acquisition Date:", None))
        self.labelSupplier.setText(QCoreApplication.translate("AssetDialog", u"Supplier / Vendor:", None))
        self.labelQuantity.setText(QCoreApplication.translate("AssetDialog", u"Quantity:", None))
        self.labelUnitCost.setText(QCoreApplication.translate("AssetDialog", u"Unit Cost (\u20a6):", None))
        self.unitCostSpinBox.setPrefix(QCoreApplication.translate("AssetDialog", u"\u20a6 ", None))
        self.labelTotalCost.setText(QCoreApplication.translate("AssetDialog", u"Total Cost (\u20a6):", None))
        self.labelUsefulLife.setText(QCoreApplication.translate("AssetDialog", u"Useful Life (Years):", None))
        self.labelDepMethod.setText(QCoreApplication.translate("AssetDialog", u"Depreciation Method:", None))
        self.labelDepPercentage.setText(QCoreApplication.translate("AssetDialog", u"Annual Depreciation %:", None))
        self.depreciationPercentageSpinBox.setSuffix(QCoreApplication.translate("AssetDialog", u" %", None))
        self.labelAnnualDep.setText(QCoreApplication.translate("AssetDialog", u"Annual Depreciation (\u20a6):", None))
        self.labelLocation.setText(QCoreApplication.translate("AssetDialog", u"Location:", None))
        self.labelModelNumber.setText(QCoreApplication.translate("AssetDialog", u"Model Number:", None))
        self.labelSerialNumber.setText(QCoreApplication.translate("AssetDialog", u"Serial Number:", None))
        self.labelCustodian.setText(QCoreApplication.translate("AssetDialog", u"Custodian / User:", None))
        self.labelRemarks.setText(QCoreApplication.translate("AssetDialog", u"Remarks:", None))
    # retranslateUi

