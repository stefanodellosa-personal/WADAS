# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_tunnels.ui'
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
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DialogTunnels(object):
    def setupUi(self, DialogTunnels):
        if not DialogTunnels.objectName():
            DialogTunnels.setObjectName(u"DialogTunnels")
        DialogTunnels.resize(418, 308)
        self.buttonBox = QDialogButtonBox(DialogTunnels)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 270, 401, 41))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.listWidget = QListWidget(DialogTunnels)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 10, 271, 251))
        self.verticalLayoutWidget = QWidget(DialogTunnels)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(290, 20, 121, 241))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add_tunnel = QPushButton(self.verticalLayoutWidget)
        self.pushButton_add_tunnel.setObjectName(u"pushButton_add_tunnel")

        self.verticalLayout.addWidget(self.pushButton_add_tunnel)

        self.pushButton_remove_tunnel = QPushButton(self.verticalLayoutWidget)
        self.pushButton_remove_tunnel.setObjectName(u"pushButton_remove_tunnel")

        self.verticalLayout.addWidget(self.pushButton_remove_tunnel)

        self.pushButton_edit_tunnel = QPushButton(self.verticalLayoutWidget)
        self.pushButton_edit_tunnel.setObjectName(u"pushButton_edit_tunnel")

        self.verticalLayout.addWidget(self.pushButton_edit_tunnel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(DialogTunnels)
        self.buttonBox.accepted.connect(DialogTunnels.accept)
        self.buttonBox.rejected.connect(DialogTunnels.reject)

        QMetaObject.connectSlotsByName(DialogTunnels)
    # setupUi

    def retranslateUi(self, DialogTunnels):
        DialogTunnels.setWindowTitle(QCoreApplication.translate("DialogTunnels", u"Tunnels", None))
        self.pushButton_add_tunnel.setText(QCoreApplication.translate("DialogTunnels", u"Add tunnel", None))
        self.pushButton_remove_tunnel.setText(QCoreApplication.translate("DialogTunnels", u"Remove Tunnel", None))
        self.pushButton_edit_tunnel.setText(QCoreApplication.translate("DialogTunnels", u"Edit tunnel", None))
    # retranslateUi

