# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_mode.ui'
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
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_DialogSelectMode(object):
    def setupUi(self, DialogSelectMode):
        if not DialogSelectMode.objectName():
            DialogSelectMode.setObjectName(u"DialogSelectMode")
        DialogSelectMode.resize(400, 174)
        self.buttonBox = QDialogButtonBox(DialogSelectMode)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 130, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.verticalLayoutWidget = QWidget(DialogSelectMode)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 20, 351, 101))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButton_test_model_mode = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_test_model_mode.setObjectName(u"radioButton_test_model_mode")
        self.radioButton_test_model_mode.setChecked(True)

        self.verticalLayout.addWidget(self.radioButton_test_model_mode)

        self.radioButton_tunnel_mode = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_tunnel_mode.setObjectName(u"radioButton_tunnel_mode")
        self.radioButton_tunnel_mode.setEnabled(False)
        self.radioButton_tunnel_mode.setCheckable(False)

        self.verticalLayout.addWidget(self.radioButton_tunnel_mode)

        self.radioButton_bear_det_mode = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_bear_det_mode.setObjectName(u"radioButton_bear_det_mode")
        self.radioButton_bear_det_mode.setEnabled(False)
        self.radioButton_bear_det_mode.setCheckable(False)

        self.verticalLayout.addWidget(self.radioButton_bear_det_mode)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(DialogSelectMode)
        self.buttonBox.accepted.connect(DialogSelectMode.accept)
        self.buttonBox.rejected.connect(DialogSelectMode.reject)

        QMetaObject.connectSlotsByName(DialogSelectMode)
    # setupUi

    def retranslateUi(self, DialogSelectMode):
        DialogSelectMode.setWindowTitle(QCoreApplication.translate("DialogSelectMode", u"Dialog", None))
        self.radioButton_test_model_mode.setText(QCoreApplication.translate("DialogSelectMode", u"Test Model", None))
        self.radioButton_tunnel_mode.setText(QCoreApplication.translate("DialogSelectMode", u"Tunnel mode", None))
        self.radioButton_bear_det_mode.setText(QCoreApplication.translate("DialogSelectMode", u"Bear detection mode", None))
    # retranslateUi

