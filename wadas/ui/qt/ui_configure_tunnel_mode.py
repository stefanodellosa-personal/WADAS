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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_DialogConfigureTunnelMode(object):
    def setupUi(self, DialogConfigureTunnelMode):
        if not DialogConfigureTunnelMode.objectName():
            DialogConfigureTunnelMode.setObjectName(u"DialogConfigureTunnelMode")
        DialogConfigureTunnelMode.resize(652, 183)
        self.gridLayout = QGridLayout(DialogConfigureTunnelMode)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_entrance_direction = QGridLayout()
        self.gridLayout_entrance_direction.setObjectName(u"gridLayout_entrance_direction")
        self.gridLayout_entrance_direction.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label_8 = QLabel(DialogConfigureTunnelMode)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_entrance_direction.addWidget(self.label_8, 2, 0, 1, 1)

        self.comboBox_camera_2 = QComboBox(DialogConfigureTunnelMode)
        self.comboBox_camera_2.setObjectName(u"comboBox_camera_2")

        self.gridLayout_entrance_direction.addWidget(self.comboBox_camera_2, 3, 1, 1, 1)

        self.label_error = QLabel(DialogConfigureTunnelMode)
        self.label_error.setObjectName(u"label_error")

        self.gridLayout_entrance_direction.addWidget(self.label_error, 4, 0, 1, 2)

        self.label_7 = QLabel(DialogConfigureTunnelMode)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_entrance_direction.addWidget(self.label_7, 1, 0, 1, 1)

        self.pushButton_add_new_tunnel = QPushButton(DialogConfigureTunnelMode)
        self.pushButton_add_new_tunnel.setObjectName(u"pushButton_add_new_tunnel")

        self.gridLayout_entrance_direction.addWidget(self.pushButton_add_new_tunnel, 0, 1, 1, 1)

        self.lineEdit_new_tunnel_name = QLineEdit(DialogConfigureTunnelMode)
        self.lineEdit_new_tunnel_name.setObjectName(u"lineEdit_new_tunnel_name")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_new_tunnel_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_new_tunnel_name.setSizePolicy(sizePolicy)

        self.gridLayout_entrance_direction.addWidget(self.lineEdit_new_tunnel_name, 0, 0, 1, 1)

        self.label = QLabel(DialogConfigureTunnelMode)
        self.label.setObjectName(u"label")

        self.gridLayout_entrance_direction.addWidget(self.label, 3, 0, 1, 1)

        self.comboBox_tunnel = QComboBox(DialogConfigureTunnelMode)
        self.comboBox_tunnel.setObjectName(u"comboBox_tunnel")

        self.gridLayout_entrance_direction.addWidget(self.comboBox_tunnel, 1, 1, 1, 1)

        self.comboBox_camera_1 = QComboBox(DialogConfigureTunnelMode)
        self.comboBox_camera_1.setObjectName(u"comboBox_camera_1")

        self.gridLayout_entrance_direction.addWidget(self.comboBox_camera_1, 2, 1, 1, 1)

        self.pushButton_direction_camera_2 = QPushButton(DialogConfigureTunnelMode)
        self.pushButton_direction_camera_2.setObjectName(u"pushButton_direction_camera_2")

        self.gridLayout_entrance_direction.addWidget(self.pushButton_direction_camera_2, 3, 3, 1, 1)

        self.label_direction_camera_2 = QLabel(DialogConfigureTunnelMode)
        self.label_direction_camera_2.setObjectName(u"label_direction_camera_2")

        self.gridLayout_entrance_direction.addWidget(self.label_direction_camera_2, 3, 2, 1, 1)

        self.label_direction_camera_1 = QLabel(DialogConfigureTunnelMode)
        self.label_direction_camera_1.setObjectName(u"label_direction_camera_1")

        self.gridLayout_entrance_direction.addWidget(self.label_direction_camera_1, 2, 2, 1, 1)

        self.pushButton_direction_camera_1 = QPushButton(DialogConfigureTunnelMode)
        self.pushButton_direction_camera_1.setObjectName(u"pushButton_direction_camera_1")

        self.gridLayout_entrance_direction.addWidget(self.pushButton_direction_camera_1, 2, 3, 1, 1)


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
        self.label_8.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"Select camera for tunnel entrance 1", None))
        self.label_error.setText("")
        self.label_7.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"Select tunnel", None))
        self.pushButton_add_new_tunnel.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"add new tunnel", None))
        self.label.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"Select camera for tunnel entrance 2", None))
        self.pushButton_direction_camera_2.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"select entrance direction", None))
        self.label_direction_camera_2.setText("")
        self.label_direction_camera_1.setText("")
        self.pushButton_direction_camera_1.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"select entrance direction", None))
    # retranslateUi

