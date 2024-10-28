# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_camera_to_actuator_associations.ui'
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
    QHeaderView, QSizePolicy, QTreeView, QWidget)

class Ui_DialogCameraActuatorAssociation(object):
    def setupUi(self, DialogCameraActuatorAssociation):
        if not DialogCameraActuatorAssociation.objectName():
            DialogCameraActuatorAssociation.setObjectName(u"DialogCameraActuatorAssociation")
        DialogCameraActuatorAssociation.resize(640, 480)
        self.buttonBox = QDialogButtonBox(DialogCameraActuatorAssociation)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 440, 621, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.treeView = QTreeView(DialogCameraActuatorAssociation)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setGeometry(QRect(10, 10, 621, 421))

        self.retranslateUi(DialogCameraActuatorAssociation)
        self.buttonBox.accepted.connect(DialogCameraActuatorAssociation.accept)
        self.buttonBox.rejected.connect(DialogCameraActuatorAssociation.reject)

        QMetaObject.connectSlotsByName(DialogCameraActuatorAssociation)
    # setupUi

    def retranslateUi(self, DialogCameraActuatorAssociation):
        DialogCameraActuatorAssociation.setWindowTitle(QCoreApplication.translate("DialogCameraActuatorAssociation", u"Camera to Actuator associations", None))
    # retranslateUi

