# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_ai_model.ui'
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
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)

class Ui_DialogConfigureAi(object):
    def setupUi(self, DialogConfigureAi):
        if not DialogConfigureAi.objectName():
            DialogConfigureAi.setObjectName(u"DialogConfigureAi")
        DialogConfigureAi.resize(400, 217)
        self.buttonBox = QDialogButtonBox(DialogConfigureAi)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 180, 381, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.gridLayoutWidget = QWidget(DialogConfigureAi)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 381, 171))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_classificationTreshold = QLabel(self.gridLayoutWidget)
        self.label_classificationTreshold.setObjectName(u"label_classificationTreshold")

        self.gridLayout.addWidget(self.label_classificationTreshold, 1, 0, 1, 1)

        self.comboBox_class_lang = QComboBox(self.gridLayoutWidget)
        self.comboBox_class_lang.setObjectName(u"comboBox_class_lang")

        self.gridLayout.addWidget(self.comboBox_class_lang, 2, 1, 1, 1)

        self.label_detectionTreshold = QLabel(self.gridLayoutWidget)
        self.label_detectionTreshold.setObjectName(u"label_detectionTreshold")

        self.gridLayout.addWidget(self.label_detectionTreshold, 0, 0, 1, 1)

        self.label_errorMEssage = QLabel(self.gridLayoutWidget)
        self.label_errorMEssage.setObjectName(u"label_errorMEssage")

        self.gridLayout.addWidget(self.label_errorMEssage, 6, 1, 1, 1)

        self.lineEdit_detectionTreshold = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_detectionTreshold.setObjectName(u"lineEdit_detectionTreshold")

        self.gridLayout.addWidget(self.lineEdit_detectionTreshold, 0, 1, 1, 1)

        self.lineEdit_classificationTreshold = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_classificationTreshold.setObjectName(u"lineEdit_classificationTreshold")

        self.gridLayout.addWidget(self.lineEdit_classificationTreshold, 1, 1, 1, 1)

        self.comboBox_detection_dev = QComboBox(self.gridLayoutWidget)
        self.comboBox_detection_dev.setObjectName(u"comboBox_detection_dev")

        self.gridLayout.addWidget(self.comboBox_detection_dev, 3, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.comboBox_class_dev = QComboBox(self.gridLayoutWidget)
        self.comboBox_class_dev.setObjectName(u"comboBox_class_dev")

        self.gridLayout.addWidget(self.comboBox_class_dev, 4, 1, 1, 1)


        self.retranslateUi(DialogConfigureAi)
        self.buttonBox.accepted.connect(DialogConfigureAi.accept)
        self.buttonBox.rejected.connect(DialogConfigureAi.reject)

        QMetaObject.connectSlotsByName(DialogConfigureAi)
    # setupUi

    def retranslateUi(self, DialogConfigureAi):
        DialogConfigureAi.setWindowTitle(QCoreApplication.translate("DialogConfigureAi", u"Configure Ai model", None))
#if QT_CONFIG(tooltip)
        self.label_classificationTreshold.setToolTip(QCoreApplication.translate("DialogConfigureAi", u"Min classification probability to trigger notification.", None))
#endif // QT_CONFIG(tooltip)
        self.label_classificationTreshold.setText(QCoreApplication.translate("DialogConfigureAi", u"Classification accurancy treshold (probablility)", None))
#if QT_CONFIG(tooltip)
        self.label_detectionTreshold.setToolTip(QCoreApplication.translate("DialogConfigureAi", u"Min detection probability to trigger notification.", None))
#endif // QT_CONFIG(tooltip)
        self.label_detectionTreshold.setText(QCoreApplication.translate("DialogConfigureAi", u"Detection accurancy treshold (probablility)", None))
        self.label_errorMEssage.setText("")
#if QT_CONFIG(tooltip)
        self.lineEdit_detectionTreshold.setToolTip(QCoreApplication.translate("DialogConfigureAi", u"Min detection probability to trigger notification.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_classificationTreshold.setToolTip(QCoreApplication.translate("DialogConfigureAi", u"Min classification probability to trigger notification.", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("DialogConfigureAi", u"Ai classification device", None))
        self.label_2.setText(QCoreApplication.translate("DialogConfigureAi", u"Ai detection device", None))
        self.label.setText(QCoreApplication.translate("DialogConfigureAi", u"Classification label language", None))
    # retranslateUi

