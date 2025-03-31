# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_tunnel_mode.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QLabel,
    QLayout, QPushButton, QSizePolicy, QWidget)

class Ui_DialogConfigureTunnelMode(object):
    def setupUi(self, DialogConfigureTunnelMode):
        if not DialogConfigureTunnelMode.objectName():
            DialogConfigureTunnelMode.setObjectName(u"DialogConfigureTunnelMode")
        DialogConfigureTunnelMode.resize(652, 418)
        self.gridLayout = QGridLayout(DialogConfigureTunnelMode)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_entrance_direction = QGridLayout()
        self.gridLayout_entrance_direction.setObjectName(u"gridLayout_entrance_direction")
        self.gridLayout_entrance_direction.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.pushButton_new_tunnel = QPushButton(DialogConfigureTunnelMode)
        self.pushButton_new_tunnel.setObjectName(u"pushButton_new_tunnel")

        self.gridLayout_entrance_direction.addWidget(self.pushButton_new_tunnel, 0, 1, 1, 1)

        self.label = QLabel(DialogConfigureTunnelMode)
        self.label.setObjectName(u"label")

        self.gridLayout_entrance_direction.addWidget(self.label, 0, 0, 1, 1)

        self.label_8 = QLabel(DialogConfigureTunnelMode)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_entrance_direction.addWidget(self.label_8, 2, 0, 1, 1)

        self.comboBox_tunnel = QComboBox(DialogConfigureTunnelMode)
        self.comboBox_tunnel.setObjectName(u"comboBox_tunnel")

        self.gridLayout_entrance_direction.addWidget(self.comboBox_tunnel, 1, 1, 1, 1)

        self.label_7 = QLabel(DialogConfigureTunnelMode)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_entrance_direction.addWidget(self.label_7, 1, 0, 1, 1)

        self.comboBox_camera = QComboBox(DialogConfigureTunnelMode)
        self.comboBox_camera.setObjectName(u"comboBox_camera")

        self.gridLayout_entrance_direction.addWidget(self.comboBox_camera, 2, 1, 1, 1)

        self.label_2 = QLabel(DialogConfigureTunnelMode)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_entrance_direction.addWidget(self.label_2, 3, 0, 1, 2)


        self.gridLayout.addLayout(self.gridLayout_entrance_direction, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DialogConfigureTunnelMode)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(DialogConfigureTunnelMode)
        self.buttonBox.accepted.connect(DialogConfigureTunnelMode.accept)
        self.buttonBox.rejected.connect(DialogConfigureTunnelMode.reject)

        QMetaObject.connectSlotsByName(DialogConfigureTunnelMode)
    # setupUi

    def retranslateUi(self, DialogConfigureTunnelMode):
        DialogConfigureTunnelMode.setWindowTitle(QCoreApplication.translate("DialogConfigureTunnelMode", u"Configure Tunnel Mode", None))
        self.pushButton_new_tunnel.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"new tunnel", None))
        self.label.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"TextLabel", None))
        self.label_8.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"Select camera", None))
        self.label_7.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"Select tunnel", None))
        self.label_2.setText("")
    # retranslateUi

