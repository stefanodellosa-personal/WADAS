# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_web_interface.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_DialogConfigureWebInterface(object):
    def setupUi(self, DialogConfigureWebInterface):
        if not DialogConfigureWebInterface.objectName():
            DialogConfigureWebInterface.setObjectName(u"DialogConfigureWebInterface")
        DialogConfigureWebInterface.resize(421, 448)
        self.buttonBox = QDialogButtonBox(DialogConfigureWebInterface)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 410, 401, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(True)
        self.verticalLayoutWidget = QWidget(DialogConfigureWebInterface)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 401, 341))
        self.verticalLayout_users = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_users.setObjectName(u"verticalLayout_users")
        self.verticalLayout_users.setContentsMargins(0, 0, 0, 0)
        self.label_errorMessage = QLabel(DialogConfigureWebInterface)
        self.label_errorMessage.setObjectName(u"label_errorMessage")
        self.label_errorMessage.setGeometry(QRect(20, 390, 381, 16))
        self.pushButton_add_user = QPushButton(DialogConfigureWebInterface)
        self.pushButton_add_user.setObjectName(u"pushButton_add_user")
        self.pushButton_add_user.setGeometry(QRect(10, 360, 151, 24))
        self.pushButton_remove_user = QPushButton(DialogConfigureWebInterface)
        self.pushButton_remove_user.setObjectName(u"pushButton_remove_user")
        self.pushButton_remove_user.setGeometry(QRect(160, 360, 121, 24))
        self.pushButton_reset_password = QPushButton(DialogConfigureWebInterface)
        self.pushButton_reset_password.setObjectName(u"pushButton_reset_password")
        self.pushButton_reset_password.setGeometry(QRect(280, 360, 131, 24))

        self.retranslateUi(DialogConfigureWebInterface)
        self.buttonBox.accepted.connect(DialogConfigureWebInterface.accept)
        self.buttonBox.rejected.connect(DialogConfigureWebInterface.reject)

        QMetaObject.connectSlotsByName(DialogConfigureWebInterface)
    # setupUi

    def retranslateUi(self, DialogConfigureWebInterface):
        DialogConfigureWebInterface.setWindowTitle(QCoreApplication.translate("DialogConfigureWebInterface", u"Configure web interface", None))
        self.label_errorMessage.setText("")
        self.pushButton_add_user.setText(QCoreApplication.translate("DialogConfigureWebInterface", u"Add user", None))
        self.pushButton_remove_user.setText(QCoreApplication.translate("DialogConfigureWebInterface", u"Remove user", None))
        self.pushButton_reset_password.setText(QCoreApplication.translate("DialogConfigureWebInterface", u"Reset user password", None))
    # retranslateUi

