# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_db_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QCheckBox,
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QWidget)

class Ui_ConfigureDBDialog(object):
    def setupUi(self, ConfigureDBDialog):
        if not ConfigureDBDialog.objectName():
            ConfigureDBDialog.setObjectName(u"ConfigureDBDialog")
        ConfigureDBDialog.resize(425, 414)
        self.buttonBox = QDialogButtonBox(ConfigureDBDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 380, 401, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.label_error = QLabel(ConfigureDBDialog)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setGeometry(QRect(8, 360, 401, 20))
        self.gridLayoutWidget_2 = QWidget(ConfigureDBDialog)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 401, 341))
        self.gridLayout_mysql = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_mysql.setObjectName(u"gridLayout_mysql")
        self.gridLayout_mysql.setContentsMargins(0, 0, 0, 0)
        self.pushButton_test_db = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_test_db.setObjectName(u"pushButton_test_db")

        self.gridLayout_mysql.addWidget(self.pushButton_test_db, 12, 0, 1, 3)

        self.radioButton_MySQL = QRadioButton(self.gridLayoutWidget_2)
        self.buttonGroup = QButtonGroup(ConfigureDBDialog)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_MySQL)
        self.radioButton_MySQL.setObjectName(u"radioButton_MySQL")

        self.gridLayout_mysql.addWidget(self.radioButton_MySQL, 2, 2, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_mysql.addWidget(self.label_4, 7, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_mysql.addWidget(self.label_3, 6, 0, 1, 1)

        self.plainTextEdit_db_test = QPlainTextEdit(self.gridLayoutWidget_2)
        self.plainTextEdit_db_test.setObjectName(u"plainTextEdit_db_test")

        self.gridLayout_mysql.addWidget(self.plainTextEdit_db_test, 13, 0, 1, 3)

        self.lineEdit_db_password = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_db_password.setObjectName(u"lineEdit_db_password")
        self.lineEdit_db_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout_mysql.addWidget(self.lineEdit_db_password, 7, 2, 1, 1)

        self.label = QLabel(self.gridLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.gridLayout_mysql.addWidget(self.label, 8, 0, 1, 1)

        self.lineEdit_db_host = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_db_host.setObjectName(u"lineEdit_db_host")

        self.gridLayout_mysql.addWidget(self.lineEdit_db_host, 5, 2, 1, 1)

        self.line = QFrame(self.gridLayoutWidget_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_mysql.addWidget(self.line, 11, 0, 1, 3)

        self.radioButton_SQLite = QRadioButton(self.gridLayoutWidget_2)
        self.buttonGroup.addButton(self.radioButton_SQLite)
        self.radioButton_SQLite.setObjectName(u"radioButton_SQLite")

        self.gridLayout_mysql.addWidget(self.radioButton_SQLite, 2, 0, 1, 1)

        self.checkBox = QCheckBox(self.gridLayoutWidget_2)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_mysql.addWidget(self.checkBox, 0, 0, 1, 3)

        self.pushButton_create_db = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_create_db.setObjectName(u"pushButton_create_db")

        self.gridLayout_mysql.addWidget(self.pushButton_create_db, 3, 2, 1, 1)

        self.lineEdit_db_username = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_db_username.setObjectName(u"lineEdit_db_username")

        self.gridLayout_mysql.addWidget(self.lineEdit_db_username, 6, 2, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_mysql.addWidget(self.label_2, 5, 0, 1, 1)

        self.lineEdit_db_name = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_db_name.setObjectName(u"lineEdit_db_name")

        self.gridLayout_mysql.addWidget(self.lineEdit_db_name, 8, 2, 1, 1)

        QWidget.setTabOrder(self.checkBox, self.radioButton_SQLite)
        QWidget.setTabOrder(self.radioButton_SQLite, self.radioButton_MySQL)
        QWidget.setTabOrder(self.radioButton_MySQL, self.pushButton_create_db)
        QWidget.setTabOrder(self.pushButton_create_db, self.lineEdit_db_host)
        QWidget.setTabOrder(self.lineEdit_db_host, self.lineEdit_db_username)
        QWidget.setTabOrder(self.lineEdit_db_username, self.lineEdit_db_password)
        QWidget.setTabOrder(self.lineEdit_db_password, self.lineEdit_db_name)
        QWidget.setTabOrder(self.lineEdit_db_name, self.pushButton_test_db)
        QWidget.setTabOrder(self.pushButton_test_db, self.plainTextEdit_db_test)

        self.retranslateUi(ConfigureDBDialog)
        self.buttonBox.accepted.connect(ConfigureDBDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDBDialog.reject)

        QMetaObject.connectSlotsByName(ConfigureDBDialog)
    # setupUi

    def retranslateUi(self, ConfigureDBDialog):
        ConfigureDBDialog.setWindowTitle(QCoreApplication.translate("ConfigureDBDialog", u"Configure Database", None))
        self.label_error.setText("")
        self.pushButton_test_db.setText(QCoreApplication.translate("ConfigureDBDialog", u"Test database connection", None))
        self.radioButton_MySQL.setText(QCoreApplication.translate("ConfigureDBDialog", u"MySQL", None))
        self.label_4.setText(QCoreApplication.translate("ConfigureDBDialog", u"Password", None))
        self.label_3.setText(QCoreApplication.translate("ConfigureDBDialog", u"Username:", None))
        self.label.setText(QCoreApplication.translate("ConfigureDBDialog", u"Database name:", None))
        self.radioButton_SQLite.setText(QCoreApplication.translate("ConfigureDBDialog", u"SQLite", None))
        self.checkBox.setText(QCoreApplication.translate("ConfigureDBDialog", u"Enable database", None))
        self.pushButton_create_db.setText(QCoreApplication.translate("ConfigureDBDialog", u"Create new DB", None))
        self.label_2.setText(QCoreApplication.translate("ConfigureDBDialog", u"Database host:", None))
    # retranslateUi

