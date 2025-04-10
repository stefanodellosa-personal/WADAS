# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_camera_for_tunnel_mode.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLayout,
    QRadioButton, QSizePolicy, QWidget)

class Ui_DialogConfigureCameraForTunnelMode(object):
    def setupUi(self, DialogConfigureCameraForTunnelMode):
        if not DialogConfigureCameraForTunnelMode.objectName():
            DialogConfigureCameraForTunnelMode.setObjectName(u"DialogConfigureCameraForTunnelMode")
        DialogConfigureCameraForTunnelMode.resize(581, 513)
        self.gridLayout = QGridLayout(DialogConfigureCameraForTunnelMode)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_entrance_direction = QGridLayout()
        self.gridLayout_entrance_direction.setObjectName(u"gridLayout_entrance_direction")
        self.gridLayout_entrance_direction.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.label = QLabel(DialogConfigureCameraForTunnelMode)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setPixmap(QPixmap(u"wadas/img/in_up.png"))
        self.label.setScaledContents(True)

        self.gridLayout_entrance_direction.addWidget(self.label, 2, 1, 1, 1)

        self.label_4 = QLabel(DialogConfigureCameraForTunnelMode)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setPixmap(QPixmap(u"wadas/img/in_right.png"))
        self.label_4.setScaledContents(True)

        self.gridLayout_entrance_direction.addWidget(self.label_4, 4, 2, 1, 1)

        self.radioButton_bottom_frame = QRadioButton(DialogConfigureCameraForTunnelMode)
        self.buttonGroup = QButtonGroup(DialogConfigureCameraForTunnelMode)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_bottom_frame)
        self.radioButton_bottom_frame.setObjectName(u"radioButton_bottom_frame")

        self.gridLayout_entrance_direction.addWidget(self.radioButton_bottom_frame, 7, 1, 1, 1)

        self.radioButton_top_frame = QRadioButton(DialogConfigureCameraForTunnelMode)
        self.buttonGroup.addButton(self.radioButton_top_frame)
        self.radioButton_top_frame.setObjectName(u"radioButton_top_frame")

        self.gridLayout_entrance_direction.addWidget(self.radioButton_top_frame, 3, 1, 1, 1)

        self.label_6 = QLabel(DialogConfigureCameraForTunnelMode)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_entrance_direction.addWidget(self.label_6, 1, 0, 1, 3)

        self.radioButton_right_frame = QRadioButton(DialogConfigureCameraForTunnelMode)
        self.buttonGroup.addButton(self.radioButton_right_frame)
        self.radioButton_right_frame.setObjectName(u"radioButton_right_frame")

        self.gridLayout_entrance_direction.addWidget(self.radioButton_right_frame, 5, 2, 1, 1)

        self.label_3 = QLabel(DialogConfigureCameraForTunnelMode)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setPixmap(QPixmap(u"wadas/img/in_left.png"))
        self.label_3.setScaledContents(True)

        self.gridLayout_entrance_direction.addWidget(self.label_3, 4, 0, 1, 1)

        self.radioButton_left_frame = QRadioButton(DialogConfigureCameraForTunnelMode)
        self.buttonGroup.addButton(self.radioButton_left_frame)
        self.radioButton_left_frame.setObjectName(u"radioButton_left_frame")

        self.gridLayout_entrance_direction.addWidget(self.radioButton_left_frame, 5, 0, 1, 1)

        self.label_2 = QLabel(DialogConfigureCameraForTunnelMode)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap(u"wadas/img/in_down.png"))
        self.label_2.setScaledContents(True)

        self.gridLayout_entrance_direction.addWidget(self.label_2, 6, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_entrance_direction, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(DialogConfigureCameraForTunnelMode)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(DialogConfigureCameraForTunnelMode)
        self.buttonBox.accepted.connect(DialogConfigureCameraForTunnelMode.accept)
        self.buttonBox.rejected.connect(DialogConfigureCameraForTunnelMode.reject)

        QMetaObject.connectSlotsByName(DialogConfigureCameraForTunnelMode)
    # setupUi

    def retranslateUi(self, DialogConfigureCameraForTunnelMode):
        DialogConfigureCameraForTunnelMode.setWindowTitle(QCoreApplication.translate("DialogConfigureCameraForTunnelMode", u"Configure camera for  Tunnel Mode", None))
        self.label.setText("")
        self.label_4.setText("")
        self.radioButton_bottom_frame.setText(QCoreApplication.translate("DialogConfigureCameraForTunnelMode", u"At the bottom of the frame", None))
        self.radioButton_top_frame.setText(QCoreApplication.translate("DialogConfigureCameraForTunnelMode", u"At the top of the frame", None))
        self.label_6.setText(QCoreApplication.translate("DialogConfigureCameraForTunnelMode", u"Select tunnel entrance direction with respect to the camera framing:", None))
        self.radioButton_right_frame.setText(QCoreApplication.translate("DialogConfigureCameraForTunnelMode", u"On the right of the frame", None))
        self.label_3.setText("")
        self.radioButton_left_frame.setText(QCoreApplication.translate("DialogConfigureCameraForTunnelMode", u"On the left of the frame", None))
        self.label_2.setText("")
    # retranslateUi

