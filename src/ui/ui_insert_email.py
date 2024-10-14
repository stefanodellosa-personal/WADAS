# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'insert_email.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_DialogInsertEmail(object):
    def setupUi(self, DialogInsertEmail):
        if not DialogInsertEmail.objectName():
            DialogInsertEmail.setObjectName("DialogInsertEmail")
        DialogInsertEmail.resize(522, 291)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogInsertEmail.sizePolicy().hasHeightForWidth())
        DialogInsertEmail.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(DialogInsertEmail)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QTabWidget(DialogInsertEmail)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget = QWidget(self.tab_3)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 461, 186))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)

        self.lineEdit_port = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_port.setObjectName("lineEdit_port")

        self.gridLayout.addWidget(self.lineEdit_port, 3, 3, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.lineEdit_smtpServer = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_smtpServer.setObjectName("lineEdit_smtpServer")

        self.gridLayout.addWidget(self.lineEdit_smtpServer, 2, 3, 1, 2)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 3, 4, 1, 1)

        self.pushButton_testEmail = QPushButton(self.gridLayoutWidget)
        self.pushButton_testEmail.setObjectName("pushButton_testEmail")

        self.gridLayout.addWidget(self.pushButton_testEmail, 4, 3, 1, 2)

        self.lineEdit_senderEmail = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_senderEmail.setObjectName("lineEdit_senderEmail")

        self.gridLayout.addWidget(self.lineEdit_senderEmail, 0, 3, 1, 2)

        self.lineEdit_password = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 3, 1, 2)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.textEdit_recipient_email = QTextEdit(self.tab_4)
        self.textEdit_recipient_email.setObjectName("textEdit_recipient_email")
        self.textEdit_recipient_email.setGeometry(QRect(10, 50, 481, 131))
        self.label_5 = QLabel(self.tab_4)
        self.label_5.setObjectName("label_5")
        self.label_5.setGeometry(QRect(10, 10, 471, 16))
        self.label_6 = QLabel(self.tab_4)
        self.label_6.setObjectName("label_6")
        self.label_6.setGeometry(QRect(10, 30, 481, 16))
        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.label_status = QLabel(DialogInsertEmail)
        self.label_status.setObjectName("label_status")

        self.verticalLayout.addWidget(self.label_status)

        self.buttonBox = QDialogButtonBox(DialogInsertEmail)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )

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
        DialogInsertEmail.setWindowTitle(
            QCoreApplication.translate("DialogInsertEmail", "Email configuration", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("DialogInsertEmail", "Port", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("DialogInsertEmail", "SMTP server", None)
        )
        self.label.setText(
            QCoreApplication.translate("DialogInsertEmail", "Sender email", None)
        )
        self.pushButton_testEmail.setText(
            QCoreApplication.translate("DialogInsertEmail", "Test email", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("DialogInsertEmail", "password", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3),
            QCoreApplication.translate("DialogInsertEmail", "Sender", None),
        )
        self.label_5.setText(
            QCoreApplication.translate(
                "DialogInsertEmail",
                "Insert recipients email address(es) separated by comma and space. ",
                None,
            )
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "DialogInsertEmail",
                "Example: email1@domail.com, email2@domail.com, email3@domail.com",
                None,
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_4),
            QCoreApplication.translate("DialogInsertEmail", "Recipients", None),
        )
        self.label_status.setText("")

    # retranslateUi
