# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_model_download.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_AiModelDownloadDialog(object):
    def setupUi(self, AiModelDownloadDialog):
        if not AiModelDownloadDialog.objectName():
            AiModelDownloadDialog.setObjectName(u"AiModelDownloadDialog")
        AiModelDownloadDialog.resize(399, 197)
        self.gridLayoutWidget = QWidget(AiModelDownloadDialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 381, 181))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.progressBar = QProgressBar(self.gridLayoutWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)

        self.pushButton_cancel = QPushButton(self.gridLayoutWidget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.gridLayout.addWidget(self.pushButton_cancel, 6, 0, 1, 1)

        self.pushButton_download = QPushButton(self.gridLayoutWidget)
        self.pushButton_download.setObjectName(u"pushButton_download")

        self.gridLayout.addWidget(self.pushButton_download, 6, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 2)

        self.lineEdit_token = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_token.setObjectName(u"lineEdit_token")
        self.lineEdit_token.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.lineEdit_token, 3, 0, 1, 2)


        self.retranslateUi(AiModelDownloadDialog)

        QMetaObject.connectSlotsByName(AiModelDownloadDialog)
    # setupUi

    def retranslateUi(self, AiModelDownloadDialog):
        AiModelDownloadDialog.setWindowTitle(QCoreApplication.translate("AiModelDownloadDialog", u"Download AI Models", None))
        self.label.setText(QCoreApplication.translate("AiModelDownloadDialog", u"Insert your Hugging Face access token:", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("AiModelDownloadDialog", u"Cancel", None))
        self.pushButton_download.setText(QCoreApplication.translate("AiModelDownloadDialog", u"Download Models", None))
        self.label_2.setText(QCoreApplication.translate("AiModelDownloadDialog", u"Ai Model files not found. Download is required to let WADAS work.", None))
    # retranslateUi

