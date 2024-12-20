# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_mode.ui'
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
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_DialogSelectMode(object):
    def setupUi(self, DialogSelectMode):
        if not DialogSelectMode.objectName():
            DialogSelectMode.setObjectName("DialogSelectMode")
        DialogSelectMode.resize(400, 194)
        self.buttonBox = QDialogButtonBox(DialogSelectMode)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(30, 160, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        self.verticalLayoutWidget = QWidget(DialogSelectMode)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 20, 351, 132))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButton_test_model_mode = QRadioButton(self.verticalLayoutWidget)
        self.buttonGroup = QButtonGroup(DialogSelectMode)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioButton_test_model_mode)
        self.radioButton_test_model_mode.setObjectName("radioButton_test_model_mode")
        self.radioButton_test_model_mode.setChecked(True)
        self.radioButton_test_model_mode.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.radioButton_test_model_mode)

        self.radioButton_animal_det_mode = QRadioButton(self.verticalLayoutWidget)
        self.buttonGroup.addButton(self.radioButton_animal_det_mode)
        self.radioButton_animal_det_mode.setObjectName("radioButton_animal_det_mode")
        self.radioButton_animal_det_mode.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.radioButton_animal_det_mode)

        self.radioButton_animal_det_and_class_mode = QRadioButton(
            self.verticalLayoutWidget
        )
        self.buttonGroup.addButton(self.radioButton_animal_det_and_class_mode)
        self.radioButton_animal_det_and_class_mode.setObjectName(
            "radioButton_animal_det_and_class_mode"
        )
        self.radioButton_animal_det_and_class_mode.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.radioButton_animal_det_and_class_mode)

        self.radioButton_tunnel_mode = QRadioButton(self.verticalLayoutWidget)
        self.buttonGroup.addButton(self.radioButton_tunnel_mode)
        self.radioButton_tunnel_mode.setObjectName("radioButton_tunnel_mode")
        self.radioButton_tunnel_mode.setEnabled(False)
        self.radioButton_tunnel_mode.setCheckable(False)
        self.radioButton_tunnel_mode.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.radioButton_tunnel_mode)

        self.radioButton_bear_det_mode = QRadioButton(self.verticalLayoutWidget)
        self.buttonGroup.addButton(self.radioButton_bear_det_mode)
        self.radioButton_bear_det_mode.setObjectName("radioButton_bear_det_mode")
        self.radioButton_bear_det_mode.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.radioButton_bear_det_mode)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(DialogSelectMode)
        self.buttonBox.accepted.connect(DialogSelectMode.accept)
        self.buttonBox.rejected.connect(DialogSelectMode.reject)

        QMetaObject.connectSlotsByName(DialogSelectMode)

    # setupUi

    def retranslateUi(self, DialogSelectMode):
        DialogSelectMode.setWindowTitle(
            QCoreApplication.translate(
                "DialogSelectMode", "Select operation mode", None
            )
        )
        self.radioButton_test_model_mode.setText(
            QCoreApplication.translate("DialogSelectMode", "Test model mode", None)
        )
        self.radioButton_animal_det_mode.setText(
            QCoreApplication.translate(
                "DialogSelectMode", "Animal detection mode", None
            )
        )
        self.radioButton_animal_det_and_class_mode.setText(
            QCoreApplication.translate(
                "DialogSelectMode", "Animal detection and classification mode", None
            )
        )
        self.radioButton_tunnel_mode.setText(
            QCoreApplication.translate("DialogSelectMode", "Tunnel mode", None)
        )
        self.radioButton_bear_det_mode.setText(
            QCoreApplication.translate("DialogSelectMode", "Bear detection mode", None)
        )

    # retranslateUi
