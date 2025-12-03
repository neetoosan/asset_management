# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loading_screen.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_LoadingScreen(object):
    def setupUi(self, LoadingScreen):
        if not LoadingScreen.objectName():
            LoadingScreen.setObjectName(u"LoadingScreen")
        LoadingScreen.resize(600, 400)
        self.verticalLayout = QVBoxLayout(LoadingScreen)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splashLabel = QLabel(LoadingScreen)
        self.splashLabel.setObjectName(u"splashLabel")
        self.splashLabel.setMinimumSize(QSize(400, 250))
        self.splashLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.splashLabel)

        self.statusLabel = QLabel(LoadingScreen)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout.addWidget(self.statusLabel)


        self.retranslateUi(LoadingScreen)

        QMetaObject.connectSlotsByName(LoadingScreen)
    # setupUi

    def retranslateUi(self, LoadingScreen):
        LoadingScreen.setWindowTitle(QCoreApplication.translate("LoadingScreen", u"Loading", None))
        self.splashLabel.setText("")
        self.statusLabel.setText(QCoreApplication.translate("LoadingScreen", u"Loading...", None))
    # retranslateUi

