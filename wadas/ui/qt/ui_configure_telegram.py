# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_telegram.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QWidget)

class Ui_DialogConfigureTelegram(object):
    def setupUi(self, DialogConfigureTelegram):
        if not DialogConfigureTelegram.objectName():
            DialogConfigureTelegram.setObjectName(u"DialogConfigureTelegram")
        DialogConfigureTelegram.resize(519, 434)
        self.buttonBox = QDialogButtonBox(DialogConfigureTelegram)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 400, 501, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.tabWidget = QTabWidget(DialogConfigureTelegram)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 30, 521, 311))
        self.tab_sender = QWidget()
        self.tab_sender.setObjectName(u"tab_sender")
        self.gridLayoutWidget = QWidget(self.tab_sender)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 10, 511, 261))
        self.gridLayout_sender = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_sender.setObjectName(u"gridLayout_sender")
        self.gridLayout_sender.setContentsMargins(0, 0, 0, 0)
        self.checkBox_enable_images = QCheckBox(self.gridLayoutWidget)
        self.checkBox_enable_images.setObjectName(u"checkBox_enable_images")

        self.gridLayout_sender.addWidget(self.checkBox_enable_images, 2, 0, 1, 2)

        self.plainTextEdit = QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setReadOnly(True)

        self.gridLayout_sender.addWidget(self.plainTextEdit, 4, 1, 1, 1)

        self.pushButton_test_message = QPushButton(self.gridLayoutWidget)
        self.pushButton_test_message.setObjectName(u"pushButton_test_message")

        self.gridLayout_sender.addWidget(self.pushButton_test_message, 3, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_sender.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.lineEdit_org_code = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_org_code.setObjectName(u"lineEdit_org_code")
        self.lineEdit_org_code.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout_sender.addWidget(self.lineEdit_org_code, 1, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout_sender.addWidget(self.label, 1, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_sender.addWidget(self.label_3, 0, 0, 1, 2)

        self.tabWidget.addTab(self.tab_sender, "")
        self.tab_receivers = QWidget()
        self.tab_receivers.setObjectName(u"tab_receivers")
        self.gridLayoutWidget_2 = QWidget(self.tab_receivers)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 501, 241))
        self.gridLayout_receivers = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_receivers.setObjectName(u"gridLayout_receivers")
        self.gridLayout_receivers.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.tab_receivers)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 250, 241, 24))
        self.pushButton_2 = QPushButton(self.tab_receivers)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(260, 250, 251, 24))
        self.tabWidget.addTab(self.tab_receivers, "")
        self.label_errorMessage = QLabel(DialogConfigureTelegram)
        self.label_errorMessage.setObjectName(u"label_errorMessage")
        self.label_errorMessage.setGeometry(QRect(0, 350, 521, 20))
        self.checkBox_enable_telegram_notifications = QCheckBox(DialogConfigureTelegram)
        self.checkBox_enable_telegram_notifications.setObjectName(u"checkBox_enable_telegram_notifications")
        self.checkBox_enable_telegram_notifications.setGeometry(QRect(10, 10, 621, 20))
        self.label_2 = QLabel(DialogConfigureTelegram)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 370, 511, 16))

        self.retranslateUi(DialogConfigureTelegram)
        self.buttonBox.accepted.connect(DialogConfigureTelegram.accept)
        self.buttonBox.rejected.connect(DialogConfigureTelegram.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DialogConfigureTelegram)
    # setupUi

    def retranslateUi(self, DialogConfigureTelegram):
        DialogConfigureTelegram.setWindowTitle(QCoreApplication.translate("DialogConfigureTelegram", u"Configure Telegram", None))
        self.checkBox_enable_images.setText(QCoreApplication.translate("DialogConfigureTelegram", u"Enable images in Telegram notification messages", None))
        self.pushButton_test_message.setText(QCoreApplication.translate("DialogConfigureTelegram", u"Test Message", None))
        self.label.setText(QCoreApplication.translate("DialogConfigureTelegram", u"Organization code:", None))
        self.label_3.setText(QCoreApplication.translate("DialogConfigureTelegram", u"To get your organization code please request it at info@wadas.it", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_sender), QCoreApplication.translate("DialogConfigureTelegram", u"Sender", None))
        self.pushButton.setText(QCoreApplication.translate("DialogConfigureTelegram", u"Add Receiver", None))
        self.pushButton_2.setText(QCoreApplication.translate("DialogConfigureTelegram", u"Remove Receiver", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_receivers), QCoreApplication.translate("DialogConfigureTelegram", u"Receivers", None))
        self.label_errorMessage.setText("")
        self.checkBox_enable_telegram_notifications.setText(QCoreApplication.translate("DialogConfigureTelegram", u"Enable Telegram notifications", None))
        self.label_2.setText(QCoreApplication.translate("DialogConfigureTelegram", u"NOTE: Telegram name and logo are copyright of Telegram LLC.", None))
    # retranslateUi

