# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_tunnel.ui'
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
    QDialogButtonBox, QGridLayout, QGroupBox, QLabel,
    QLayout, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_DialogConfigureTunnel(object):
    def setupUi(self, DialogConfigureTunnel):
        if not DialogConfigureTunnel.objectName():
            DialogConfigureTunnel.setObjectName(u"DialogConfigureTunnel")
        DialogConfigureTunnel.resize(652, 397)
        self.gridLayout = QGridLayout(DialogConfigureTunnel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_entrance_direction = QGridLayout()
        self.gridLayout_entrance_direction.setObjectName(u"gridLayout_entrance_direction")
        self.gridLayout_entrance_direction.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label_7 = QLabel(DialogConfigureTunnel)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_entrance_direction.addWidget(self.label_7, 1, 0, 1, 1)

        self.groupBox = QGroupBox(DialogConfigureTunnel)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayoutWidget = QWidget(self.groupBox)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(19, 19, 601, 111))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.comboBox_camera_1 = QComboBox(self.gridLayoutWidget)
        self.comboBox_camera_1.setObjectName(u"comboBox_camera_1")

        self.gridLayout_2.addWidget(self.comboBox_camera_1, 0, 1, 1, 1)

        self.pushButton_direction_camera_1 = QPushButton(self.gridLayoutWidget)
        self.pushButton_direction_camera_1.setObjectName(u"pushButton_direction_camera_1")

        self.gridLayout_2.addWidget(self.pushButton_direction_camera_1, 1, 2, 1, 1)

        self.label_direction_camera_1 = QLabel(self.gridLayoutWidget)
        self.label_direction_camera_1.setObjectName(u"label_direction_camera_1")

        self.gridLayout_2.addWidget(self.label_direction_camera_1, 1, 1, 1, 1)


        self.gridLayout_entrance_direction.addWidget(self.groupBox, 2, 0, 1, 2)

        self.groupBox_2 = QGroupBox(DialogConfigureTunnel)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayoutWidget_2 = QWidget(self.groupBox_2)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 20, 611, 111))
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 1, 0, 1, 1)

        self.comboBox_camera_2 = QComboBox(self.gridLayoutWidget_2)
        self.comboBox_camera_2.setObjectName(u"comboBox_camera_2")

        self.gridLayout_4.addWidget(self.comboBox_camera_2, 0, 1, 1, 1)

        self.label_direction_camera_2 = QLabel(self.gridLayoutWidget_2)
        self.label_direction_camera_2.setObjectName(u"label_direction_camera_2")

        self.gridLayout_4.addWidget(self.label_direction_camera_2, 1, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)

        self.pushButton_direction_camera_2 = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_direction_camera_2.setObjectName(u"pushButton_direction_camera_2")

        self.gridLayout_4.addWidget(self.pushButton_direction_camera_2, 1, 2, 1, 1)


        self.gridLayout_entrance_direction.addWidget(self.groupBox_2, 3, 0, 1, 2)

        self.lineEdit_tunnel_name = QLineEdit(DialogConfigureTunnel)
        self.lineEdit_tunnel_name.setObjectName(u"lineEdit_tunnel_name")

        self.gridLayout_entrance_direction.addWidget(self.lineEdit_tunnel_name, 1, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_entrance_direction, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DialogConfigureTunnel)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)


        self.retranslateUi(DialogConfigureTunnel)
        self.buttonBox.accepted.connect(DialogConfigureTunnel.accept)
        self.buttonBox.rejected.connect(DialogConfigureTunnel.reject)

        QMetaObject.connectSlotsByName(DialogConfigureTunnel)
    # setupUi

    def retranslateUi(self, DialogConfigureTunnel):
        DialogConfigureTunnel.setWindowTitle(QCoreApplication.translate("DialogConfigureTunnel", u"Configure Tunnel", None))
        self.label_7.setText(QCoreApplication.translate("DialogConfigureTunnel", u"Tunnel:", None))
        self.groupBox.setTitle(QCoreApplication.translate("DialogConfigureTunnel", u"Entrance1", None))
        self.label_8.setText(QCoreApplication.translate("DialogConfigureTunnel", u"Select camera for tunnel entrance 1", None))
        self.label_2.setText(QCoreApplication.translate("DialogConfigureTunnel", u"Direction to the entrance:", None))
        self.pushButton_direction_camera_1.setText(QCoreApplication.translate("DialogConfigureTunnel", u"select entrance direction", None))
        self.label_direction_camera_1.setText(QCoreApplication.translate("DialogConfigureTunnel", u"no direction set", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("DialogConfigureTunnel", u"Entrance2", None))
        self.label_3.setText(QCoreApplication.translate("DialogConfigureTunnel", u"Direction to the entrance:", None))
        self.label_direction_camera_2.setText(QCoreApplication.translate("DialogConfigureTunnel", u"no direction set", None))
        self.label.setText(QCoreApplication.translate("DialogConfigureTunnel", u"Select camera for tunnel entrance 2", None))
        self.pushButton_direction_camera_2.setText(QCoreApplication.translate("DialogConfigureTunnel", u"select entrance direction", None))
    # retranslateUi

