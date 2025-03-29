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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QRadioButton,
    QScrollArea, QSizePolicy, QWidget)

class Ui_DialogConfigureTunnelMode(object):
    def setupUi(self, DialogConfigureTunnelMode):
        if not DialogConfigureTunnelMode.objectName():
            DialogConfigureTunnelMode.setObjectName(u"DialogConfigureTunnelMode")
        DialogConfigureTunnelMode.resize(626, 418)
        self.buttonBox = QDialogButtonBox(DialogConfigureTunnelMode)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 380, 611, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.gridLayoutWidget = QWidget(DialogConfigureTunnelMode)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 40, 341, 331))
        self.gridLayout_entrance_direction = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_entrance_direction.setObjectName(u"gridLayout_entrance_direction")
        self.gridLayout_entrance_direction.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap(u"../../img/in_down.png"))
        self.label_2.setScaledContents(True)

        self.gridLayout_entrance_direction.addWidget(self.label_2, 3, 1, 1, 1)

        self.radioButton_bottom_frame = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup = QButtonGroup(DialogConfigureTunnelMode)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_bottom_frame)
        self.radioButton_bottom_frame.setObjectName(u"radioButton_bottom_frame")

        self.gridLayout_entrance_direction.addWidget(self.radioButton_bottom_frame, 3, 0, 1, 1)

        self.radioButton_left_frame = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup.addButton(self.radioButton_left_frame)
        self.radioButton_left_frame.setObjectName(u"radioButton_left_frame")

        self.gridLayout_entrance_direction.addWidget(self.radioButton_left_frame, 5, 0, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setPixmap(QPixmap(u"../../img/in_right.png"))
        self.label_4.setScaledContents(True)

        self.gridLayout_entrance_direction.addWidget(self.label_4, 5, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setPixmap(QPixmap(u"../../img/in_left.png"))
        self.label_3.setScaledContents(True)

        self.gridLayout_entrance_direction.addWidget(self.label_3, 4, 1, 1, 1)

        self.radioButton_top_frame = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup.addButton(self.radioButton_top_frame)
        self.radioButton_top_frame.setObjectName(u"radioButton_top_frame")

        self.gridLayout_entrance_direction.addWidget(self.radioButton_top_frame, 2, 0, 1, 1)

        self.radioButton_right_frame = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup.addButton(self.radioButton_right_frame)
        self.radioButton_right_frame.setObjectName(u"radioButton_right_frame")

        self.gridLayout_entrance_direction.addWidget(self.radioButton_right_frame, 4, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u"../../img/in_up.png"))
        self.label.setScaledContents(True)

        self.gridLayout_entrance_direction.addWidget(self.label, 2, 1, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_entrance_direction.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_6 = QLabel(DialogConfigureTunnelMode)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 10, 611, 16))
        self.scrollArea_cameras = QScrollArea(DialogConfigureTunnelMode)
        self.scrollArea_cameras.setObjectName(u"scrollArea_cameras")
        self.scrollArea_cameras.setGeometry(QRect(360, 40, 251, 331))
        self.scrollArea_cameras.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 249, 329))
        self.scrollArea_cameras.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(DialogConfigureTunnelMode)
        self.buttonBox.accepted.connect(DialogConfigureTunnelMode.accept)
        self.buttonBox.rejected.connect(DialogConfigureTunnelMode.reject)

        QMetaObject.connectSlotsByName(DialogConfigureTunnelMode)
    # setupUi

    def retranslateUi(self, DialogConfigureTunnelMode):
        DialogConfigureTunnelMode.setWindowTitle(QCoreApplication.translate("DialogConfigureTunnelMode", u"Dialog", None))
        self.label_2.setText("")
        self.radioButton_bottom_frame.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"At the bottom of the frame", None))
        self.radioButton_left_frame.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"On the left of the frame", None))
        self.label_4.setText("")
        self.label_3.setText("")
        self.radioButton_top_frame.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"At the top of the frame", None))
        self.radioButton_right_frame.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"On the right of the frame", None))
        self.label.setText("")
        self.label_5.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"Tunnel entrance:", None))
        self.label_6.setText(QCoreApplication.translate("DialogConfigureTunnelMode", u"Select tunnel entrance direction with respect to the camera framing:", None))
    # retranslateUi

