# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_screen.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_LoginScreen(object):
    def setupUi(self, LoginScreen):
        if not LoginScreen.objectName():
            LoginScreen.setObjectName(u"LoginScreen")
        LoginScreen.resize(800, 500)
        self.horizontalLayout = QHBoxLayout(LoginScreen)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.leftFrame = QFrame(LoginScreen)
        self.leftFrame.setObjectName(u"leftFrame")
        self.leftFrame.setMinimumSize(QSize(400, 0))
        self.leftFrame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout = QVBoxLayout(self.leftFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(40, 40, 40, 40)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.titleLabel = QLabel(self.leftFrame)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setStyleSheet(u"font-size: 24px;\n"
"color: #0066cc;\n"
"font-weight: bold;")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(self.leftFrame)
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.subtitleLabel.setStyleSheet(u"color: #666666;\n"
"font-size: 14px;\n"
"margin-bottom: 20px;")
        self.subtitleLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.subtitleLabel)

        self.usernameInput = QLineEdit(self.leftFrame)
        self.usernameInput.setObjectName(u"usernameInput")
        self.usernameInput.setMinimumSize(QSize(0, 40))
        self.usernameInput.setStyleSheet(u"#usernameInput {\n"
"    border: 1px ;\n"
"    border-radius: 4px;\n"
"    padding: 8px;\n"
"    margin-bottom: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"#usernameInput:focus {\n"
"    border: 2px solid #0066cc;\n"
"}")

        self.verticalLayout.addWidget(self.usernameInput)

        self.passwordInput = QLineEdit(self.leftFrame)
        self.passwordInput.setObjectName(u"passwordInput")
        self.passwordInput.setMinimumSize(QSize(0, 40))
        self.passwordInput.setStyleSheet(u"#passwordInput {\n"
"    border: 1px ;\n"
"    border-radius: 4px;\n"
"    padding: 8px;\n"
"    margin-bottom: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"#passwordInput:focus {\n"
"    border: 2px solid #0066cc;\n"
"}")
        self.passwordInput.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.passwordInput)

        self.loginButton = QPushButton(self.leftFrame)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMinimumSize(QSize(0, 40))
        self.loginButton.setStyleSheet(u"#loginButton {\n"
"    background-color: #0066cc;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"}\n"
"#loginButton:hover {\n"
"    background-color: #0055aa;\n"
"}\n"
"#loginButton:pressed {\n"
"    background-color: #004488;\n"
"}")

        self.verticalLayout.addWidget(self.loginButton)

        self.errorLabel = QLabel(self.leftFrame)
        self.errorLabel.setObjectName(u"errorLabel")
        self.errorLabel.setStyleSheet(u"color: #ff0000;\n"
"font-size: 12px;\n"
"margin-top: 10px;")
        self.errorLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.errorLabel)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.leftFrame)

        self.rightFrame = QFrame(LoginScreen)
        self.rightFrame.setObjectName(u"rightFrame")
        self.rightFrame.setMinimumSize(QSize(400, 0))
        self.rightFrame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(self.rightFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.backgroundLabel = QLabel(self.rightFrame)
        self.backgroundLabel.setObjectName(u"backgroundLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backgroundLabel.sizePolicy().hasHeightForWidth())
        self.backgroundLabel.setSizePolicy(sizePolicy)
        self.backgroundLabel.setStyleSheet(u"background-position: center;")
        self.backgroundLabel.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.backgroundLabel)


        self.horizontalLayout.addWidget(self.rightFrame)


        self.retranslateUi(LoginScreen)

        QMetaObject.connectSlotsByName(LoginScreen)
    # setupUi

    def retranslateUi(self, LoginScreen):
        LoginScreen.setWindowTitle(QCoreApplication.translate("LoginScreen", u"Asset Management System - Login", None))
        self.titleLabel.setText(QCoreApplication.translate("LoginScreen", u"Welcome Back", None))
        self.subtitleLabel.setText(QCoreApplication.translate("LoginScreen", u"Please login to your account", None))
        self.usernameInput.setPlaceholderText(QCoreApplication.translate("LoginScreen", u"Username", None))
        self.passwordInput.setPlaceholderText(QCoreApplication.translate("LoginScreen", u"Password", None))
        self.loginButton.setText(QCoreApplication.translate("LoginScreen", u"Login", None))
        self.errorLabel.setText("")
        self.backgroundLabel.setText("")
    # retranslateUi

