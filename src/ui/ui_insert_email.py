# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'insert_email.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_DialogInsertEmail(object):
    def setupUi(self, DialogInsertEmail):
        if not DialogInsertEmail.objectName():
            DialogInsertEmail.setObjectName(u"DialogInsertEmail")
        DialogInsertEmail.resize(522, 303)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogInsertEmail.sizePolicy().hasHeightForWidth())
        DialogInsertEmail.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(DialogInsertEmail)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(DialogInsertEmail)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayoutWidget = QWidget(self.tab_3)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 461, 186))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)

        self.lineEdit_port = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_port.setObjectName(u"lineEdit_port")

        self.gridLayout.addWidget(self.lineEdit_port, 3, 3, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.lineEdit_smtpServer = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_smtpServer.setObjectName(u"lineEdit_smtpServer")

        self.gridLayout.addWidget(self.lineEdit_smtpServer, 2, 3, 1, 2)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 4, 1, 1)

        self.pushButton_testEmail = QPushButton(self.gridLayoutWidget)
        self.pushButton_testEmail.setObjectName(u"pushButton_testEmail")

        self.gridLayout.addWidget(self.pushButton_testEmail, 4, 3, 1, 2)

        self.lineEdit_senderEmail = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_senderEmail.setObjectName(u"lineEdit_senderEmail")

        self.gridLayout.addWidget(self.lineEdit_senderEmail, 0, 3, 1, 2)

        self.lineEdit_password = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 3, 1, 2)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.scrollArea = QScrollArea(self.tab_4)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(0, 0, 491, 201))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 472, 199))
        self.gridLayoutWidget_2 = QWidget(self.scrollAreaWidgetContents_2)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 461, 331))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_rec_email7 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email7.setObjectName(u"lineEdit_rec_email7")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email7, 6, 2, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)

        self.lineEdit_rec_email9 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email9.setObjectName(u"lineEdit_rec_email9")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email9, 8, 2, 1, 1)

        self.lineEdit_rec_email6 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email6.setObjectName(u"lineEdit_rec_email6")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email6, 5, 2, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_12 = QLabel(self.gridLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 7, 0, 1, 1)

        self.lineEdit_rec_email8 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email8.setObjectName(u"lineEdit_rec_email8")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email8, 7, 2, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 6, 0, 1, 1)

        self.lineEdit_rec_email5 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email5.setObjectName(u"lineEdit_rec_email5")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email5, 4, 2, 1, 1)

        self.lineEdit_rec_email1 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email1.setObjectName(u"lineEdit_rec_email1")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email1, 0, 2, 1, 1)

        self.lineEdit_rec_email2 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email2.setObjectName(u"lineEdit_rec_email2")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email2, 1, 2, 1, 1)

        self.lineEdit_rec_email4 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email4.setObjectName(u"lineEdit_rec_email4")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email4, 3, 2, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 5, 0, 1, 1)

        self.lineEdit_rec_email3 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email3.setObjectName(u"lineEdit_rec_email3")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email3, 2, 2, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 4, 0, 1, 1)

        self.lineEdit_rec_email10 = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_rec_email10.setObjectName(u"lineEdit_rec_email10")

        self.gridLayout_2.addWidget(self.lineEdit_rec_email10, 9, 2, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 8, 0, 1, 1)

        self.label_14 = QLabel(self.gridLayoutWidget_2)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_2.addWidget(self.label_14, 9, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.label_status = QLabel(DialogInsertEmail)
        self.label_status.setObjectName(u"label_status")

        self.verticalLayout.addWidget(self.label_status)

        self.buttonBox = QDialogButtonBox(DialogInsertEmail)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lineEdit_senderEmail, self.lineEdit_password)
        QWidget.setTabOrder(self.lineEdit_password, self.lineEdit_smtpServer)
        QWidget.setTabOrder(self.lineEdit_smtpServer, self.lineEdit_port)
        QWidget.setTabOrder(self.lineEdit_port, self.pushButton_testEmail)

        self.retranslateUi(DialogInsertEmail)
        self.buttonBox.accepted.connect(DialogInsertEmail.accept)
        self.buttonBox.rejected.connect(DialogInsertEmail.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DialogInsertEmail)
    # setupUi

    def retranslateUi(self, DialogInsertEmail):
        DialogInsertEmail.setWindowTitle(QCoreApplication.translate("DialogInsertEmail", u"Insert Email configuration parameters", None))
        self.label_4.setText(QCoreApplication.translate("DialogInsertEmail", u"Port", None))
        self.label_3.setText(QCoreApplication.translate("DialogInsertEmail", u"SMTP server", None))
        self.label.setText(QCoreApplication.translate("DialogInsertEmail", u"Sender email", None))
        self.pushButton_testEmail.setText(QCoreApplication.translate("DialogInsertEmail", u"Test email", None))
        self.label_2.setText(QCoreApplication.translate("DialogInsertEmail", u"password", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("DialogInsertEmail", u"Sender", None))
        self.label_6.setText(QCoreApplication.translate("DialogInsertEmail", u"Email2", None))
        self.label_5.setText(QCoreApplication.translate("DialogInsertEmail", u"Email1", None))
        self.label_12.setText(QCoreApplication.translate("DialogInsertEmail", u"Email8", None))
        self.label_8.setText(QCoreApplication.translate("DialogInsertEmail", u"Email4", None))
        self.label_11.setText(QCoreApplication.translate("DialogInsertEmail", u"Email7", None))
        self.label_10.setText(QCoreApplication.translate("DialogInsertEmail", u"Email6", None))
        self.label_7.setText(QCoreApplication.translate("DialogInsertEmail", u"Email3", None))
        self.label_9.setText(QCoreApplication.translate("DialogInsertEmail", u"Email5", None))
        self.label_13.setText(QCoreApplication.translate("DialogInsertEmail", u"Email9", None))
        self.label_14.setText(QCoreApplication.translate("DialogInsertEmail", u"Email10", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("DialogInsertEmail", u"Receivers", None))
        self.label_status.setText("")
    # retranslateUi

