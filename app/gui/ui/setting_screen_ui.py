# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_screen.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_SettingScreen(object):
    def setupUi(self, SettingScreen):
        if not SettingScreen.objectName():
            SettingScreen.setObjectName(u"SettingScreen")
        SettingScreen.resize(800, 600)
        self.mainLayout = QVBoxLayout(SettingScreen)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.titleLabel = QLabel(SettingScreen)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.mainLayout.addWidget(self.titleLabel)

        self.centralFrame = QFrame(SettingScreen)
        self.centralFrame.setObjectName(u"centralFrame")
        self.centralFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.centralFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.frameLayout = QVBoxLayout(self.centralFrame)
        self.frameLayout.setObjectName(u"frameLayout")
        self.frameLayout.setContentsMargins(10, 10, 10, 10)
        self.settingTabs = QTabWidget(self.centralFrame)
        self.settingTabs.setObjectName(u"settingTabs")
        self.generalTab = QWidget()
        self.generalTab.setObjectName(u"generalTab")
        self.generalLayout = QVBoxLayout(self.generalTab)
        self.generalLayout.setObjectName(u"generalLayout")
        self.generalScrollArea = QScrollArea(self.generalTab)
        self.generalScrollArea.setObjectName(u"generalScrollArea")
        self.generalScrollArea.setWidgetResizable(True)
        self.generalScrollContent = QWidget()
        self.generalScrollContent.setObjectName(u"generalScrollContent")
        self.generalScrollContent.setGeometry(QRect(0, 0, 712, 417))
        self.generalContentLayout = QVBoxLayout(self.generalScrollContent)
        self.generalContentLayout.setObjectName(u"generalContentLayout")
        self.applicationGroup = QGroupBox(self.generalScrollContent)
        self.applicationGroup.setObjectName(u"applicationGroup")
        self.applicationFormLayout = QFormLayout(self.applicationGroup)
        self.applicationFormLayout.setObjectName(u"applicationFormLayout")
        self.autoStartLabel = QLabel(self.applicationGroup)
        self.autoStartLabel.setObjectName(u"autoStartLabel")

        self.applicationFormLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.autoStartLabel)

        self.autoStartCheckBox = QCheckBox(self.applicationGroup)
        self.autoStartCheckBox.setObjectName(u"autoStartCheckBox")

        self.applicationFormLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.autoStartCheckBox)

        self.minimizeToTrayLabel = QLabel(self.applicationGroup)
        self.minimizeToTrayLabel.setObjectName(u"minimizeToTrayLabel")

        self.applicationFormLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.minimizeToTrayLabel)

        self.minimizeToTrayCheckBox = QCheckBox(self.applicationGroup)
        self.minimizeToTrayCheckBox.setObjectName(u"minimizeToTrayCheckBox")

        self.applicationFormLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.minimizeToTrayCheckBox)

        self.confirmExitLabel = QLabel(self.applicationGroup)
        self.confirmExitLabel.setObjectName(u"confirmExitLabel")

        self.applicationFormLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.confirmExitLabel)

        self.confirmExitCheckBox = QCheckBox(self.applicationGroup)
        self.confirmExitCheckBox.setObjectName(u"confirmExitCheckBox")
        self.confirmExitCheckBox.setChecked(True)

        self.applicationFormLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.confirmExitCheckBox)


        self.generalContentLayout.addWidget(self.applicationGroup)

        self.languageGroup = QGroupBox(self.generalScrollContent)
        self.languageGroup.setObjectName(u"languageGroup")
        self.languageFormLayout = QFormLayout(self.languageGroup)
        self.languageFormLayout.setObjectName(u"languageFormLayout")
        self.languageLabel = QLabel(self.languageGroup)
        self.languageLabel.setObjectName(u"languageLabel")

        self.languageFormLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.languageLabel)

        self.languageComboBox = QComboBox(self.languageGroup)
        self.languageComboBox.addItem("")
        self.languageComboBox.addItem("")
        self.languageComboBox.addItem("")
        self.languageComboBox.setObjectName(u"languageComboBox")

        self.languageFormLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.languageComboBox)

        self.dateFormatLabel = QLabel(self.languageGroup)
        self.dateFormatLabel.setObjectName(u"dateFormatLabel")

        self.languageFormLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.dateFormatLabel)

        self.dateFormatComboBox = QComboBox(self.languageGroup)
        self.dateFormatComboBox.addItem("")
        self.dateFormatComboBox.addItem("")
        self.dateFormatComboBox.addItem("")
        self.dateFormatComboBox.setObjectName(u"dateFormatComboBox")

        self.languageFormLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.dateFormatComboBox)

        self.currencyLabel = QLabel(self.languageGroup)
        self.currencyLabel.setObjectName(u"currencyLabel")

        self.languageFormLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.currencyLabel)

        self.currencyComboBox = QComboBox(self.languageGroup)
        self.currencyComboBox.addItem("")
        self.currencyComboBox.addItem("")
        self.currencyComboBox.addItem("")
        self.currencyComboBox.setObjectName(u"currencyComboBox")

        self.languageFormLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.currencyComboBox)


        self.generalContentLayout.addWidget(self.languageGroup)

        self.generalScrollArea.setWidget(self.generalScrollContent)

        self.generalLayout.addWidget(self.generalScrollArea)

        self.settingTabs.addTab(self.generalTab, "")
        self.appearanceTab = QWidget()
        self.appearanceTab.setObjectName(u"appearanceTab")
        self.appearanceLayout = QVBoxLayout(self.appearanceTab)
        self.appearanceLayout.setObjectName(u"appearanceLayout")
        self.appearanceScrollArea = QScrollArea(self.appearanceTab)
        self.appearanceScrollArea.setObjectName(u"appearanceScrollArea")
        self.appearanceScrollArea.setWidgetResizable(True)
        self.appearanceScrollContent = QWidget()
        self.appearanceScrollContent.setObjectName(u"appearanceScrollContent")
        self.appearanceScrollContent.setGeometry(QRect(0, 0, 712, 417))
        self.appearanceContentLayout = QVBoxLayout(self.appearanceScrollContent)
        self.appearanceContentLayout.setObjectName(u"appearanceContentLayout")
        self.themeGroup = QGroupBox(self.appearanceScrollContent)
        self.themeGroup.setObjectName(u"themeGroup")
        self.themeFormLayout = QFormLayout(self.themeGroup)
        self.themeFormLayout.setObjectName(u"themeFormLayout")
        self.themeLabel = QLabel(self.themeGroup)
        self.themeLabel.setObjectName(u"themeLabel")

        self.themeFormLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.themeLabel)

        self.themeComboBox = QComboBox(self.themeGroup)
        self.themeComboBox.addItem("")
        self.themeComboBox.addItem("")
        self.themeComboBox.addItem("")
        self.themeComboBox.setObjectName(u"themeComboBox")

        self.themeFormLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.themeComboBox)

        self.fontSizeLabel = QLabel(self.themeGroup)
        self.fontSizeLabel.setObjectName(u"fontSizeLabel")

        self.themeFormLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.fontSizeLabel)

        self.fontSizeSpinBox = QSpinBox(self.themeGroup)
        self.fontSizeSpinBox.setObjectName(u"fontSizeSpinBox")
        self.fontSizeSpinBox.setMinimum(8)
        self.fontSizeSpinBox.setMaximum(24)
        self.fontSizeSpinBox.setValue(10)

        self.themeFormLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.fontSizeSpinBox)


        self.appearanceContentLayout.addWidget(self.themeGroup)

        self.displayGroup = QGroupBox(self.appearanceScrollContent)
        self.displayGroup.setObjectName(u"displayGroup")
        self.displayFormLayout = QFormLayout(self.displayGroup)
        self.displayFormLayout.setObjectName(u"displayFormLayout")
        self.showToolTipsLabel = QLabel(self.displayGroup)
        self.showToolTipsLabel.setObjectName(u"showToolTipsLabel")

        self.displayFormLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.showToolTipsLabel)

        self.showToolTipsCheckBox = QCheckBox(self.displayGroup)
        self.showToolTipsCheckBox.setObjectName(u"showToolTipsCheckBox")
        self.showToolTipsCheckBox.setChecked(True)

        self.displayFormLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.showToolTipsCheckBox)

        self.showIconsLabel = QLabel(self.displayGroup)
        self.showIconsLabel.setObjectName(u"showIconsLabel")

        self.displayFormLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.showIconsLabel)

        self.showIconsCheckBox = QCheckBox(self.displayGroup)
        self.showIconsCheckBox.setObjectName(u"showIconsCheckBox")
        self.showIconsCheckBox.setChecked(True)

        self.displayFormLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.showIconsCheckBox)


        self.appearanceContentLayout.addWidget(self.displayGroup)

        self.appearanceScrollArea.setWidget(self.appearanceScrollContent)

        self.appearanceLayout.addWidget(self.appearanceScrollArea)

        self.settingTabs.addTab(self.appearanceTab, "")
        self.notificationsTab = QWidget()
        self.notificationsTab.setObjectName(u"notificationsTab")
        self.notificationsLayout = QVBoxLayout(self.notificationsTab)
        self.notificationsLayout.setObjectName(u"notificationsLayout")
        self.notificationsScrollArea = QScrollArea(self.notificationsTab)
        self.notificationsScrollArea.setObjectName(u"notificationsScrollArea")
        self.notificationsScrollArea.setWidgetResizable(True)
        self.notificationsScrollContent = QWidget()
        self.notificationsScrollContent.setObjectName(u"notificationsScrollContent")
        self.notificationsScrollContent.setGeometry(QRect(0, 0, 712, 417))
        self.notificationsContentLayout = QVBoxLayout(self.notificationsScrollContent)
        self.notificationsContentLayout.setObjectName(u"notificationsContentLayout")
        self.alertsGroup = QGroupBox(self.notificationsScrollContent)
        self.alertsGroup.setObjectName(u"alertsGroup")
        self.alertsFormLayout = QFormLayout(self.alertsGroup)
        self.alertsFormLayout.setObjectName(u"alertsFormLayout")
        self.enableAlertsLabel = QLabel(self.alertsGroup)
        self.enableAlertsLabel.setObjectName(u"enableAlertsLabel")

        self.alertsFormLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.enableAlertsLabel)

        self.enableAlertsCheckBox = QCheckBox(self.alertsGroup)
        self.enableAlertsCheckBox.setObjectName(u"enableAlertsCheckBox")
        self.enableAlertsCheckBox.setChecked(True)

        self.alertsFormLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.enableAlertsCheckBox)

        self.maintenanceAlertsLabel = QLabel(self.alertsGroup)
        self.maintenanceAlertsLabel.setObjectName(u"maintenanceAlertsLabel")

        self.alertsFormLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.maintenanceAlertsLabel)

        self.maintenanceAlertsCheckBox = QCheckBox(self.alertsGroup)
        self.maintenanceAlertsCheckBox.setObjectName(u"maintenanceAlertsCheckBox")
        self.maintenanceAlertsCheckBox.setChecked(True)

        self.alertsFormLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.maintenanceAlertsCheckBox)

        self.deprecationAlertsLabel = QLabel(self.alertsGroup)
        self.deprecationAlertsLabel.setObjectName(u"deprecationAlertsLabel")

        self.alertsFormLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.deprecationAlertsLabel)

        self.deprecationAlertsCheckBox = QCheckBox(self.alertsGroup)
        self.deprecationAlertsCheckBox.setObjectName(u"deprecationAlertsCheckBox")
        self.deprecationAlertsCheckBox.setChecked(True)

        self.alertsFormLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.deprecationAlertsCheckBox)

        self.alertDaysLabel = QLabel(self.alertsGroup)
        self.alertDaysLabel.setObjectName(u"alertDaysLabel")

        self.alertsFormLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.alertDaysLabel)

        self.alertDaysSpinBox = QSpinBox(self.alertsGroup)
        self.alertDaysSpinBox.setObjectName(u"alertDaysSpinBox")
        self.alertDaysSpinBox.setMinimum(1)
        self.alertDaysSpinBox.setMaximum(365)
        self.alertDaysSpinBox.setValue(30)

        self.alertsFormLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.alertDaysSpinBox)


        self.notificationsContentLayout.addWidget(self.alertsGroup)

        self.emailGroup = QGroupBox(self.notificationsScrollContent)
        self.emailGroup.setObjectName(u"emailGroup")
        self.emailFormLayout = QFormLayout(self.emailGroup)
        self.emailFormLayout.setObjectName(u"emailFormLayout")
        self.enableEmailLabel = QLabel(self.emailGroup)
        self.enableEmailLabel.setObjectName(u"enableEmailLabel")

        self.emailFormLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.enableEmailLabel)

        self.enableEmailCheckBox = QCheckBox(self.emailGroup)
        self.enableEmailCheckBox.setObjectName(u"enableEmailCheckBox")

        self.emailFormLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.enableEmailCheckBox)

        self.emailAddressLabel = QLabel(self.emailGroup)
        self.emailAddressLabel.setObjectName(u"emailAddressLabel")

        self.emailFormLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.emailAddressLabel)

        self.emailAddressLineEdit = QLineEdit(self.emailGroup)
        self.emailAddressLineEdit.setObjectName(u"emailAddressLineEdit")

        self.emailFormLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.emailAddressLineEdit)


        self.notificationsContentLayout.addWidget(self.emailGroup)

        self.notificationsScrollArea.setWidget(self.notificationsScrollContent)

        self.notificationsLayout.addWidget(self.notificationsScrollArea)

        self.settingTabs.addTab(self.notificationsTab, "")
        self.importTab = QWidget()
        self.importTab.setObjectName(u"importTab")
        self.importLayout = QVBoxLayout(self.importTab)
        self.importLayout.setObjectName(u"importLayout")
        self.importScrollArea = QScrollArea(self.importTab)
        self.importScrollArea.setObjectName(u"importScrollArea")
        self.importScrollArea.setWidgetResizable(True)
        self.importScrollContent = QWidget()
        self.importScrollContent.setObjectName(u"importScrollContent")
        self.importScrollContent.setGeometry(QRect(0, 0, 712, 417))
        self.importContentLayout = QVBoxLayout(self.importScrollContent)
        self.importContentLayout.setObjectName(u"importContentLayout")
        self.importGroup = QGroupBox(self.importScrollContent)
        self.importGroup.setObjectName(u"importGroup")
        self.importFormLayout = QVBoxLayout(self.importGroup)
        self.importFormLayout.setObjectName(u"importFormLayout")
        self.importInstructionsLabel = QLabel(self.importGroup)
        self.importInstructionsLabel.setObjectName(u"importInstructionsLabel")
        self.importInstructionsLabel.setMaximumSize(QSize(16777215, 16777215))
        self.importInstructionsLabel.setWordWrap(True)

        self.importFormLayout.addWidget(self.importInstructionsLabel)

        self.fileSelectLayout = QHBoxLayout()
        self.fileSelectLayout.setObjectName(u"fileSelectLayout")
        self.importFilePathInput = QLineEdit(self.importGroup)
        self.importFilePathInput.setObjectName(u"importFilePathInput")
        self.importFilePathInput.setReadOnly(True)

        self.fileSelectLayout.addWidget(self.importFilePathInput)

        self.browseImportBtn = QPushButton(self.importGroup)
        self.browseImportBtn.setObjectName(u"browseImportBtn")

        self.fileSelectLayout.addWidget(self.browseImportBtn)


        self.importFormLayout.addLayout(self.fileSelectLayout)

        self.headerRowCheckBox = QCheckBox(self.importGroup)
        self.headerRowCheckBox.setObjectName(u"headerRowCheckBox")
        self.headerRowCheckBox.setChecked(True)

        self.importFormLayout.addWidget(self.headerRowCheckBox)

        self.importDataBtn = QPushButton(self.importGroup)
        self.importDataBtn.setObjectName(u"importDataBtn")

        self.importFormLayout.addWidget(self.importDataBtn)

        self.importProgressBar = QProgressBar(self.importGroup)
        self.importProgressBar.setObjectName(u"importProgressBar")
        self.importProgressBar.setMinimum(0)
        self.importProgressBar.setMaximum(100)
        self.importProgressBar.setValue(0)

        self.importFormLayout.addWidget(self.importProgressBar)

        self.importPreviewTable = QTableWidget(self.importGroup)
        self.importPreviewTable.setObjectName(u"importPreviewTable")
        self.importPreviewTable.setMinimumSize(QSize(600, 180))
        self.importPreviewTable.setRowCount(0)
        self.importPreviewTable.setColumnCount(0)

        self.importFormLayout.addWidget(self.importPreviewTable)

        self.importSummaryFrame = QFrame(self.importGroup)
        self.importSummaryFrame.setObjectName(u"importSummaryFrame")
        self.importSummaryFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.importSummaryLayout = QHBoxLayout(self.importSummaryFrame)
        self.importSummaryLayout.setObjectName(u"importSummaryLayout")
        self.importSuccessLabel = QLabel(self.importSummaryFrame)
        self.importSuccessLabel.setObjectName(u"importSuccessLabel")

        self.importSummaryLayout.addWidget(self.importSuccessLabel)

        self.importFailedLabel = QLabel(self.importSummaryFrame)
        self.importFailedLabel.setObjectName(u"importFailedLabel")

        self.importSummaryLayout.addWidget(self.importFailedLabel)

        self.importSummarySpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.importSummaryLayout.addItem(self.importSummarySpacer)

        self.importPercentLabel = QLabel(self.importSummaryFrame)
        self.importPercentLabel.setObjectName(u"importPercentLabel")

        self.importSummaryLayout.addWidget(self.importPercentLabel)


        self.importFormLayout.addWidget(self.importSummaryFrame)

        self.importStatusLabel = QLabel(self.importGroup)
        self.importStatusLabel.setObjectName(u"importStatusLabel")
        self.importStatusLabel.setWordWrap(True)

        self.importFormLayout.addWidget(self.importStatusLabel)


        self.importContentLayout.addWidget(self.importGroup)

        self.importScrollArea.setWidget(self.importScrollContent)

        self.importLayout.addWidget(self.importScrollArea)

        self.settingTabs.addTab(self.importTab, "")

        self.frameLayout.addWidget(self.settingTabs)

        self.buttonFrame = QFrame(self.centralFrame)
        self.buttonFrame.setObjectName(u"buttonFrame")
        self.buttonFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.buttonLayout = QHBoxLayout(self.buttonFrame)
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.buttonSpacer)

        self.saveBtn = QPushButton(self.buttonFrame)
        self.saveBtn.setObjectName(u"saveBtn")

        self.buttonLayout.addWidget(self.saveBtn)

        self.resetBtn = QPushButton(self.buttonFrame)
        self.resetBtn.setObjectName(u"resetBtn")

        self.buttonLayout.addWidget(self.resetBtn)


        self.frameLayout.addWidget(self.buttonFrame)


        self.mainLayout.addWidget(self.centralFrame)


        self.retranslateUi(SettingScreen)

        self.settingTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SettingScreen)
    # setupUi

    def retranslateUi(self, SettingScreen):
        SettingScreen.setWindowTitle(QCoreApplication.translate("SettingScreen", u"Settings", None))
        self.titleLabel.setText(QCoreApplication.translate("SettingScreen", u"Settings", None))
        self.applicationGroup.setTitle(QCoreApplication.translate("SettingScreen", u"Application Settings", None))
        self.autoStartLabel.setText(QCoreApplication.translate("SettingScreen", u"Start with Windows:", None))
        self.autoStartCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.minimizeToTrayLabel.setText(QCoreApplication.translate("SettingScreen", u"Minimize to System Tray:", None))
        self.minimizeToTrayCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.confirmExitLabel.setText(QCoreApplication.translate("SettingScreen", u"Confirm on Exit:", None))
        self.confirmExitCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.languageGroup.setTitle(QCoreApplication.translate("SettingScreen", u"Language and Region", None))
        self.languageLabel.setText(QCoreApplication.translate("SettingScreen", u"Language:", None))
        self.languageComboBox.setItemText(0, QCoreApplication.translate("SettingScreen", u"English", None))
        self.languageComboBox.setItemText(1, QCoreApplication.translate("SettingScreen", u"Spanish", None))
        self.languageComboBox.setItemText(2, QCoreApplication.translate("SettingScreen", u"French", None))

        self.dateFormatLabel.setText(QCoreApplication.translate("SettingScreen", u"Date Format:", None))
        self.dateFormatComboBox.setItemText(0, QCoreApplication.translate("SettingScreen", u"DD/MM/YYYY", None))
        self.dateFormatComboBox.setItemText(1, QCoreApplication.translate("SettingScreen", u"MM/DD/YYYY", None))
        self.dateFormatComboBox.setItemText(2, QCoreApplication.translate("SettingScreen", u"YYYY-MM-DD", None))

        self.currencyLabel.setText(QCoreApplication.translate("SettingScreen", u"Currency:", None))
        self.currencyComboBox.setItemText(0, QCoreApplication.translate("SettingScreen", u"USD ($)", None))
        self.currencyComboBox.setItemText(1, QCoreApplication.translate("SettingScreen", u"EUR (\u20ac)", None))
        self.currencyComboBox.setItemText(2, QCoreApplication.translate("SettingScreen", u"GBP (\u00a3)", None))

        self.settingTabs.setTabText(self.settingTabs.indexOf(self.generalTab), QCoreApplication.translate("SettingScreen", u"General", None))
        self.themeGroup.setTitle(QCoreApplication.translate("SettingScreen", u"Theme Settings", None))
        self.themeLabel.setText(QCoreApplication.translate("SettingScreen", u"Theme:", None))
        self.themeComboBox.setItemText(0, QCoreApplication.translate("SettingScreen", u"Default", None))
        self.themeComboBox.setItemText(1, QCoreApplication.translate("SettingScreen", u"Dark", None))
        self.themeComboBox.setItemText(2, QCoreApplication.translate("SettingScreen", u"Light", None))

        self.fontSizeLabel.setText(QCoreApplication.translate("SettingScreen", u"Font Size:", None))
        self.displayGroup.setTitle(QCoreApplication.translate("SettingScreen", u"Display Settings", None))
        self.showToolTipsLabel.setText(QCoreApplication.translate("SettingScreen", u"Show Tooltips:", None))
        self.showToolTipsCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.showIconsLabel.setText(QCoreApplication.translate("SettingScreen", u"Show Icons in Menus:", None))
        self.showIconsCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.settingTabs.setTabText(self.settingTabs.indexOf(self.appearanceTab), QCoreApplication.translate("SettingScreen", u"Appearance", None))
        self.alertsGroup.setTitle(QCoreApplication.translate("SettingScreen", u"Alert Settings", None))
        self.enableAlertsLabel.setText(QCoreApplication.translate("SettingScreen", u"Enable Alerts:", None))
        self.enableAlertsCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.maintenanceAlertsLabel.setText(QCoreApplication.translate("SettingScreen", u"Maintenance Alerts:", None))
        self.maintenanceAlertsCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.deprecationAlertsLabel.setText(QCoreApplication.translate("SettingScreen", u"End of Useful Life Alerts:", None))
        self.deprecationAlertsCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.alertDaysLabel.setText(QCoreApplication.translate("SettingScreen", u"Alert Days Before:", None))
        self.emailGroup.setTitle(QCoreApplication.translate("SettingScreen", u"Email Notifications", None))
        self.enableEmailLabel.setText(QCoreApplication.translate("SettingScreen", u"Enable Email Notifications:", None))
        self.enableEmailCheckBox.setText(QCoreApplication.translate("SettingScreen", u"Enable", None))
        self.emailAddressLabel.setText(QCoreApplication.translate("SettingScreen", u"Email Address:", None))
        self.emailAddressLineEdit.setPlaceholderText(QCoreApplication.translate("SettingScreen", u"Enter email address", None))
        self.settingTabs.setTabText(self.settingTabs.indexOf(self.notificationsTab), QCoreApplication.translate("SettingScreen", u"Notifications", None))
        self.importGroup.setTitle(QCoreApplication.translate("SettingScreen", u"Import Data", None))
        self.importInstructionsLabel.setText(QCoreApplication.translate("SettingScreen", u"Import data from CSV or Excel (XLSX) files.", None))
        self.importFilePathInput.setPlaceholderText(QCoreApplication.translate("SettingScreen", u"Select a file to import...", None))
        self.browseImportBtn.setText(QCoreApplication.translate("SettingScreen", u"Browse", None))
        self.headerRowCheckBox.setText(QCoreApplication.translate("SettingScreen", u"First row contains headers", None))
        self.importDataBtn.setText(QCoreApplication.translate("SettingScreen", u"Import Data", None))
        self.importSuccessLabel.setText(QCoreApplication.translate("SettingScreen", u"Success: 0", None))
        self.importFailedLabel.setText(QCoreApplication.translate("SettingScreen", u"Failed: 0", None))
        self.importPercentLabel.setText(QCoreApplication.translate("SettingScreen", u"0%", None))
        self.importStatusLabel.setText("")
        self.settingTabs.setTabText(self.settingTabs.indexOf(self.importTab), QCoreApplication.translate("SettingScreen", u"Import", None))
        self.saveBtn.setText(QCoreApplication.translate("SettingScreen", u"Save Settings", None))
        self.resetBtn.setText(QCoreApplication.translate("SettingScreen", u"Reset to Defaults", None))
    # retranslateUi

