# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'notification_screen.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)
class Ui_NotificationScreen(object):
    def setupUi(self, NotificationScreen):
        if not NotificationScreen.objectName():
            NotificationScreen.setObjectName(u"NotificationScreen")
        NotificationScreen.resize(800, 600)
        self.mainLayout = QVBoxLayout(NotificationScreen)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.titleLabel = QLabel(NotificationScreen)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignLeft|Qt.AlignTop)

        self.mainLayout.addWidget(self.titleLabel)

        self.centralFrame = QFrame(NotificationScreen)
        self.centralFrame.setObjectName(u"centralFrame")
        self.centralFrame.setFrameShape(QFrame.StyledPanel)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.frameLayout = QVBoxLayout(self.centralFrame)
        self.frameLayout.setObjectName(u"frameLayout")
        self.frameLayout.setContentsMargins(10, 10, 10, 10)
        self.notificationTabs = QTabWidget(self.centralFrame)
        self.notificationTabs.setObjectName(u"notificationTabs")
        self.todayTab = QWidget()
        self.todayTab.setObjectName(u"todayTab")
        self.todayLayout = QVBoxLayout(self.todayTab)
        self.todayLayout.setObjectName(u"todayLayout")
        self.todayScrollArea = QScrollArea(self.todayTab)
        self.todayScrollArea.setObjectName(u"todayScrollArea")
        self.todayScrollArea.setWidgetResizable(True)
        self.todayScrollContent = QWidget()
        self.todayScrollContent.setObjectName(u"todayScrollContent")
        self.todayScrollContent.setGeometry(QRect(0, 0, 742, 485))
        self.todayContentLayout = QVBoxLayout(self.todayScrollContent)
        self.todayContentLayout.setObjectName(u"todayContentLayout")
        self.todayPlaceholder = QLabel(self.todayScrollContent)
        self.todayPlaceholder.setObjectName(u"todayPlaceholder")
        self.todayPlaceholder.setAlignment(Qt.AlignCenter)

        self.todayContentLayout.addWidget(self.todayPlaceholder)

        self.todayVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.todayContentLayout.addItem(self.todayVerticalSpacer)

        self.todayScrollArea.setWidget(self.todayScrollContent)

        self.todayLayout.addWidget(self.todayScrollArea)

        self.notificationTabs.addTab(self.todayTab, "")
        self.yesterdayTab = QWidget()
        self.yesterdayTab.setObjectName(u"yesterdayTab")
        self.yesterdayLayout = QVBoxLayout(self.yesterdayTab)
        self.yesterdayLayout.setObjectName(u"yesterdayLayout")
        self.yesterdayScrollArea = QScrollArea(self.yesterdayTab)
        self.yesterdayScrollArea.setObjectName(u"yesterdayScrollArea")
        self.yesterdayScrollArea.setWidgetResizable(True)
        self.yesterdayScrollContent = QWidget()
        self.yesterdayScrollContent.setObjectName(u"yesterdayScrollContent")
        self.yesterdayScrollContent.setGeometry(QRect(0, 0, 742, 485))
        self.yesterdayContentLayout = QVBoxLayout(self.yesterdayScrollContent)
        self.yesterdayContentLayout.setObjectName(u"yesterdayContentLayout")
        self.yesterdayPlaceholder = QLabel(self.yesterdayScrollContent)
        self.yesterdayPlaceholder.setObjectName(u"yesterdayPlaceholder")
        self.yesterdayPlaceholder.setAlignment(Qt.AlignCenter)

        self.yesterdayContentLayout.addWidget(self.yesterdayPlaceholder)

        self.yesterdayVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.yesterdayContentLayout.addItem(self.yesterdayVerticalSpacer)

        self.yesterdayScrollArea.setWidget(self.yesterdayScrollContent)

        self.yesterdayLayout.addWidget(self.yesterdayScrollArea)

        self.notificationTabs.addTab(self.yesterdayTab, "")
        self.lastWeekTab = QWidget()
        self.lastWeekTab.setObjectName(u"lastWeekTab")
        self.lastWeekLayout = QVBoxLayout(self.lastWeekTab)
        self.lastWeekLayout.setObjectName(u"lastWeekLayout")
        self.lastWeekScrollArea = QScrollArea(self.lastWeekTab)
        self.lastWeekScrollArea.setObjectName(u"lastWeekScrollArea")
        self.lastWeekScrollArea.setWidgetResizable(True)
        self.lastWeekScrollContent = QWidget()
        self.lastWeekScrollContent.setObjectName(u"lastWeekScrollContent")
        self.lastWeekScrollContent.setGeometry(QRect(0, 0, 742, 485))
        self.lastWeekContentLayout = QVBoxLayout(self.lastWeekScrollContent)
        self.lastWeekContentLayout.setObjectName(u"lastWeekContentLayout")
        self.lastWeekPlaceholder = QLabel(self.lastWeekScrollContent)
        self.lastWeekPlaceholder.setObjectName(u"lastWeekPlaceholder")
        self.lastWeekPlaceholder.setAlignment(Qt.AlignCenter)

        self.lastWeekContentLayout.addWidget(self.lastWeekPlaceholder)

        self.lastWeekVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.lastWeekContentLayout.addItem(self.lastWeekVerticalSpacer)

        self.lastWeekScrollArea.setWidget(self.lastWeekScrollContent)

        self.lastWeekLayout.addWidget(self.lastWeekScrollArea)

        self.notificationTabs.addTab(self.lastWeekTab, "")
        self.allTab = QWidget()
        self.allTab.setObjectName(u"allTab")
        self.allLayout = QVBoxLayout(self.allTab)
        self.allLayout.setObjectName(u"allLayout")
        self.allScrollArea = QScrollArea(self.allTab)
        self.allScrollArea.setObjectName(u"allScrollArea")
        self.allScrollArea.setWidgetResizable(True)
        self.allScrollContent = QWidget()
        self.allScrollContent.setObjectName(u"allScrollContent")
        self.allScrollContent.setGeometry(QRect(0, 0, 742, 485))
        self.allContentLayout = QVBoxLayout(self.allScrollContent)
        self.allContentLayout.setObjectName(u"allContentLayout")
        self.allPlaceholder = QLabel(self.allScrollContent)
        self.allPlaceholder.setObjectName(u"allPlaceholder")
        self.allPlaceholder.setAlignment(Qt.AlignCenter)

        self.allContentLayout.addWidget(self.allPlaceholder)

        self.allVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.allContentLayout.addItem(self.allVerticalSpacer)

        self.allScrollArea.setWidget(self.allScrollContent)

        self.allLayout.addWidget(self.allScrollArea)

        self.notificationTabs.addTab(self.allTab, "")

        self.frameLayout.addWidget(self.notificationTabs)


        self.mainLayout.addWidget(self.centralFrame)


        self.retranslateUi(NotificationScreen)

        self.notificationTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(NotificationScreen)
    # setupUi

    def retranslateUi(self, NotificationScreen):
        NotificationScreen.setWindowTitle(QCoreApplication.translate("NotificationScreen", u"Notifications", None))
        self.titleLabel.setText(QCoreApplication.translate("NotificationScreen", u"Notifications", None))
        self.todayPlaceholder.setText(QCoreApplication.translate("NotificationScreen", u"No notifications for today", None))
        self.notificationTabs.setTabText(self.notificationTabs.indexOf(self.todayTab), QCoreApplication.translate("NotificationScreen", u"Today", None))
        self.yesterdayPlaceholder.setText(QCoreApplication.translate("NotificationScreen", u"No notifications for yesterday", None))
        self.notificationTabs.setTabText(self.notificationTabs.indexOf(self.yesterdayTab), QCoreApplication.translate("NotificationScreen", u"Yesterday", None))
        self.lastWeekPlaceholder.setText(QCoreApplication.translate("NotificationScreen", u"No notifications for last week", None))
        self.notificationTabs.setTabText(self.notificationTabs.indexOf(self.lastWeekTab), QCoreApplication.translate("NotificationScreen", u"Last Week", None))
        self.allPlaceholder.setText(QCoreApplication.translate("NotificationScreen", u"No notifications available", None))
        self.notificationTabs.setTabText(self.notificationTabs.indexOf(self.allTab), QCoreApplication.translate("NotificationScreen", u"All", None))
    # retranslateUi

