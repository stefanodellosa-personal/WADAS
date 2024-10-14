# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_ai_model.ui'
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
    QSizePolicy,
    QSpacerItem,
    QWidget,
)


class Ui_DialogConfigureAi(object):
    def setupUi(self, DialogConfigureAi):
        if not DialogConfigureAi.objectName():
            DialogConfigureAi.setObjectName("DialogConfigureAi")
        DialogConfigureAi.resize(400, 179)
        self.buttonBox = QDialogButtonBox(DialogConfigureAi)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(10, 140, 381, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        self.gridLayoutWidget = QWidget(DialogConfigureAi)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 381, 101))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_detectionTreshold = QLabel(self.gridLayoutWidget)
        self.label_detectionTreshold.setObjectName("label_detectionTreshold")

        self.gridLayout.addWidget(self.label_detectionTreshold, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.lineEdit_classificationTreshold = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_classificationTreshold.setObjectName(
            "lineEdit_classificationTreshold"
        )

        self.gridLayout.addWidget(self.lineEdit_classificationTreshold, 1, 1, 1, 1)

        self.label_classificationTreshold = QLabel(self.gridLayoutWidget)
        self.label_classificationTreshold.setObjectName("label_classificationTreshold")

        self.gridLayout.addWidget(self.label_classificationTreshold, 1, 0, 1, 1)

        self.lineEdit_detectionTreshold = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_detectionTreshold.setObjectName("lineEdit_detectionTreshold")

        self.gridLayout.addWidget(self.lineEdit_detectionTreshold, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.label_errorMEssage = QLabel(DialogConfigureAi)
        self.label_errorMEssage.setObjectName("label_errorMEssage")
        self.label_errorMEssage.setGeometry(QRect(8, 120, 381, 20))

        self.retranslateUi(DialogConfigureAi)
        self.buttonBox.accepted.connect(DialogConfigureAi.accept)
        self.buttonBox.rejected.connect(DialogConfigureAi.reject)

        QMetaObject.connectSlotsByName(DialogConfigureAi)

    # setupUi

    def retranslateUi(self, DialogConfigureAi):
        DialogConfigureAi.setWindowTitle(
            QCoreApplication.translate("DialogConfigureAi", "Configure Ai model", None)
        )
        # if QT_CONFIG(tooltip)
        self.label_detectionTreshold.setToolTip(
            QCoreApplication.translate(
                "DialogConfigureAi",
                "Min detection probability to trigger notification.",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_detectionTreshold.setText(
            QCoreApplication.translate(
                "DialogConfigureAi", "Detection accurancy treshold (probablility)", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.lineEdit_classificationTreshold.setToolTip(
            QCoreApplication.translate(
                "DialogConfigureAi",
                "Min classification probability to trigger notification.",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_classificationTreshold.setToolTip(
            QCoreApplication.translate(
                "DialogConfigureAi",
                "Min classification probability to trigger notification.",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_classificationTreshold.setText(
            QCoreApplication.translate(
                "DialogConfigureAi",
                "Classification accurancy treshold (probablility)",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.lineEdit_detectionTreshold.setToolTip(
            QCoreApplication.translate(
                "DialogConfigureAi",
                "Min detection probability to trigger notification.",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_errorMEssage.setText("")

    # retranslateUi
