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
    QSizePolicy, QSpacerItem, QWidget)

class Ui_DialogInsertEmail(object):
    def setupUi(self, DialogInsertEmail):
        if not DialogInsertEmail.objectName():
            DialogInsertEmail.setObjectName(u"DialogInsertEmail")
        DialogInsertEmail.resize(483, 240)
        self.buttonBox = QDialogButtonBox(DialogInsertEmail)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 200, 461, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.gridLayoutWidget = QWidget(DialogInsertEmail)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 461, 151))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.lineEdit_port = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_port.setObjectName(u"lineEdit_port")

        self.gridLayout.addWidget(self.lineEdit_port, 3, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 4, 1, 1)

        self.lineEdit_smtpServer = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_smtpServer.setObjectName(u"lineEdit_smtpServer")

        self.gridLayout.addWidget(self.lineEdit_smtpServer, 2, 3, 1, 2)

        self.lineEdit_password = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 3, 1, 2)

        self.lineEdit_senderEmail = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_senderEmail.setObjectName(u"lineEdit_senderEmail")

        self.gridLayout.addWidget(self.lineEdit_senderEmail, 0, 3, 1, 2)

        self.pushButton_testEmail = QPushButton(self.gridLayoutWidget)
        self.pushButton_testEmail.setObjectName(u"pushButton_testEmail")

        self.gridLayout.addWidget(self.pushButton_testEmail, 4, 3, 1, 2)

        self.label_status = QLabel(DialogInsertEmail)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setGeometry(QRect(8, 170, 461, 20))
        QWidget.setTabOrder(self.lineEdit_senderEmail, self.lineEdit_password)
        QWidget.setTabOrder(self.lineEdit_password, self.lineEdit_smtpServer)
        QWidget.setTabOrder(self.lineEdit_smtpServer, self.lineEdit_port)
        QWidget.setTabOrder(self.lineEdit_port, self.pushButton_testEmail)

        self.retranslateUi(DialogInsertEmail)
        self.buttonBox.accepted.connect(DialogInsertEmail.accept)
        self.buttonBox.rejected.connect(DialogInsertEmail.reject)

        QMetaObject.connectSlotsByName(DialogInsertEmail)
    # setupUi

    def retranslateUi(self, DialogInsertEmail):
        DialogInsertEmail.setWindowTitle(QCoreApplication.translate("DialogInsertEmail", u"Insert Email configuration parameters", None))
        self.label_3.setText(QCoreApplication.translate("DialogInsertEmail", u"SMTP server", None))
        self.label.setText(QCoreApplication.translate("DialogInsertEmail", u"Sender email", None))
        self.label_4.setText(QCoreApplication.translate("DialogInsertEmail", u"Port", None))
        self.label_2.setText(QCoreApplication.translate("DialogInsertEmail", u"password", None))
        self.pushButton_testEmail.setText(QCoreApplication.translate("DialogInsertEmail", u"Test email", None))
        self.label_status.setText("")
    # retranslateUi

