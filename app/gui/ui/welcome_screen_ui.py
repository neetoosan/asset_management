# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcome_screen.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_WelcomeScreen(object):
    def setupUi(self, WelcomeScreen):
        if not WelcomeScreen.objectName():
            WelcomeScreen.setObjectName(u"WelcomeScreen")
        WelcomeScreen.resize(800, 480)
        self.verticalLayout = QVBoxLayout(WelcomeScreen)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.contentLayout = QVBoxLayout()
        self.contentLayout.setObjectName(u"contentLayout")
        self.verticalSpacerTop = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.contentLayout.addItem(self.verticalSpacerTop)

        self.centerHBox = QHBoxLayout()
        self.centerHBox.setObjectName(u"centerHBox")
        self.imageFrame = QFrame(WelcomeScreen)
        self.imageFrame.setObjectName(u"imageFrame")
        self.imageFrame.setMinimumSize(QSize(480, 320))
        self.frameLayout = QVBoxLayout(self.imageFrame)
        self.frameLayout.setObjectName(u"frameLayout")
        self.imageLabel = QLabel(self.imageFrame)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.frameLayout.addWidget(self.imageLabel)


        self.centerHBox.addWidget(self.imageFrame)


        self.contentLayout.addLayout(self.centerHBox)

        self.verticalSpacerBottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.contentLayout.addItem(self.verticalSpacerBottom)


        self.verticalLayout.addLayout(self.contentLayout)

        self.buttonHBox = QHBoxLayout()
        self.buttonHBox.setObjectName(u"buttonHBox")
        self.buttonSpacerLeft = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonHBox.addItem(self.buttonSpacerLeft)

        self.buttonCenterSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonHBox.addItem(self.buttonCenterSpacer)

        self.loginBtn = QPushButton(WelcomeScreen)
        self.loginBtn.setObjectName(u"loginBtn")

        self.buttonHBox.addWidget(self.loginBtn)


        self.verticalLayout.addLayout(self.buttonHBox)


        self.retranslateUi(WelcomeScreen)

        QMetaObject.connectSlotsByName(WelcomeScreen)
    # setupUi

    def retranslateUi(self, WelcomeScreen):
        WelcomeScreen.setWindowTitle(QCoreApplication.translate("WelcomeScreen", u"Welcome", None))
        self.loginBtn.setText(QCoreApplication.translate("WelcomeScreen", u"Login", None))
    # retranslateUi

