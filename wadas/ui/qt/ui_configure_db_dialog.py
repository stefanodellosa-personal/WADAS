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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFrame, QGridLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QWidget)

class Ui_ConfigureDBDialog(object):
    def setupUi(self, ConfigureDBDialog):
        if not ConfigureDBDialog.objectName():
            ConfigureDBDialog.setObjectName(u"ConfigureDBDialog")
        ConfigureDBDialog.resize(545, 414)
        self.buttonBox = QDialogButtonBox(ConfigureDBDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 380, 531, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.label_error = QLabel(ConfigureDBDialog)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setGeometry(QRect(8, 360, 531, 20))
        self.tabWidget = QTabWidget(ConfigureDBDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 531, 341))
        self.tab_sqlite = QWidget()
        self.tab_sqlite.setObjectName(u"tab_sqlite")
        self.gridLayoutWidget = QWidget(self.tab_sqlite)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 501, 291))
        self.gridLayout_sqlite = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_sqlite.setObjectName(u"gridLayout_sqlite")
        self.gridLayout_sqlite.setContentsMargins(0, 0, 0, 0)
        self.checkBox_enable_sqlite_db = QCheckBox(self.gridLayoutWidget)
        self.checkBox_enable_sqlite_db.setObjectName(u"checkBox_enable_sqlite_db")

        self.gridLayout_sqlite.addWidget(self.checkBox_enable_sqlite_db, 0, 0, 1, 3)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_sqlite.addWidget(self.label_5, 2, 1, 1, 1)

        self.plainTextEdit = QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.gridLayout_sqlite.addWidget(self.plainTextEdit, 8, 0, 1, 3)

        self.pushButton_sqlite_create_db = QPushButton(self.gridLayoutWidget)
        self.pushButton_sqlite_create_db.setObjectName(u"pushButton_sqlite_create_db")

        self.gridLayout_sqlite.addWidget(self.pushButton_sqlite_create_db, 2, 0, 1, 1)

        self.pushButton_sqlite_open_db = QPushButton(self.gridLayoutWidget)
        self.pushButton_sqlite_open_db.setObjectName(u"pushButton_sqlite_open_db")

        self.gridLayout_sqlite.addWidget(self.pushButton_sqlite_open_db, 2, 2, 1, 1)

        self.label_db_path = QLabel(self.gridLayoutWidget)
        self.label_db_path.setObjectName(u"label_db_path")

        self.gridLayout_sqlite.addWidget(self.label_db_path, 5, 0, 1, 1)

        self.pushButton_sqlite_test = QPushButton(self.gridLayoutWidget)
        self.pushButton_sqlite_test.setObjectName(u"pushButton_sqlite_test")

        self.gridLayout_sqlite.addWidget(self.pushButton_sqlite_test, 7, 0, 1, 3)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_sqlite.addWidget(self.label, 4, 0, 1, 1)

        self.line_2 = QFrame(self.gridLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_sqlite.addWidget(self.line_2, 6, 0, 1, 3)

        self.tabWidget.addTab(self.tab_sqlite, "")
        self.tab_mysql = QWidget()
        self.tab_mysql.setObjectName(u"tab_mysql")
        self.gridLayoutWidget_2 = QWidget(self.tab_mysql)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 501, 291))
        self.gridLayout_mysql = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_mysql.setObjectName(u"gridLayout_mysql")
        self.gridLayout_mysql.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_db_password = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_db_password.setObjectName(u"lineEdit_db_password")
        self.lineEdit_db_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout_mysql.addWidget(self.lineEdit_db_password, 5, 1, 1, 1)

        self.checkBox = QCheckBox(self.gridLayoutWidget_2)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_mysql.addWidget(self.checkBox, 0, 0, 1, 2)

        self.label_4 = QLabel(self.gridLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_mysql.addWidget(self.label_4, 5, 0, 1, 1)

        self.plainTextEdit_mysql_test = QPlainTextEdit(self.gridLayoutWidget_2)
        self.plainTextEdit_mysql_test.setObjectName(u"plainTextEdit_mysql_test")

        self.gridLayout_mysql.addWidget(self.plainTextEdit_mysql_test, 10, 0, 1, 2)

        self.line = QFrame(self.gridLayoutWidget_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_mysql.addWidget(self.line, 8, 0, 1, 2)

        self.pushButton_mysql_test_connection = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_mysql_test_connection.setObjectName(u"pushButton_mysql_test_connection")

        self.gridLayout_mysql.addWidget(self.pushButton_mysql_test_connection, 9, 0, 1, 2)

        self.label_3 = QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_mysql.addWidget(self.label_3, 4, 0, 1, 1)

        self.lineEdit_db_host = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_db_host.setObjectName(u"lineEdit_db_host")

        self.gridLayout_mysql.addWidget(self.lineEdit_db_host, 3, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_mysql.addWidget(self.label_2, 3, 0, 1, 1)

        self.lineEdit_db_username = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_db_username.setObjectName(u"lineEdit_db_username")

        self.gridLayout_mysql.addWidget(self.lineEdit_db_username, 4, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_mysql.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.pushButton_mysql_create_db = QPushButton(self.gridLayoutWidget_2)
        self.pushButton_mysql_create_db.setObjectName(u"pushButton_mysql_create_db")

        self.gridLayout_mysql.addWidget(self.pushButton_mysql_create_db, 1, 1, 1, 1)

        self.tabWidget.addTab(self.tab_mysql, "")

        self.retranslateUi(ConfigureDBDialog)
        self.buttonBox.accepted.connect(ConfigureDBDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDBDialog.reject)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(ConfigureDBDialog)
    # setupUi

    def retranslateUi(self, ConfigureDBDialog):
        ConfigureDBDialog.setWindowTitle(QCoreApplication.translate("ConfigureDBDialog", u"Configure Database", None))
        self.label_error.setText("")
        self.checkBox_enable_sqlite_db.setText(QCoreApplication.translate("ConfigureDBDialog", u"Enable SQLite DB", None))
        self.label_5.setText(QCoreApplication.translate("ConfigureDBDialog", u"OR", None))
        self.pushButton_sqlite_create_db.setText(QCoreApplication.translate("ConfigureDBDialog", u"Create new DB", None))
        self.pushButton_sqlite_open_db.setText(QCoreApplication.translate("ConfigureDBDialog", u"Open existing DB file", None))
        self.label_db_path.setText("")
        self.pushButton_sqlite_test.setText(QCoreApplication.translate("ConfigureDBDialog", u"Test DB connection", None))
        self.label.setText(QCoreApplication.translate("ConfigureDBDialog", u"Database file:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_sqlite), QCoreApplication.translate("ConfigureDBDialog", u"SQLite", None))
        self.checkBox.setText(QCoreApplication.translate("ConfigureDBDialog", u"Enable MySQL SB", None))
        self.label_4.setText(QCoreApplication.translate("ConfigureDBDialog", u"Password", None))
        self.pushButton_mysql_test_connection.setText(QCoreApplication.translate("ConfigureDBDialog", u"Test DB connection", None))
        self.label_3.setText(QCoreApplication.translate("ConfigureDBDialog", u"Username:", None))
        self.label_2.setText(QCoreApplication.translate("ConfigureDBDialog", u"Database host:", None))
        self.pushButton_mysql_create_db.setText(QCoreApplication.translate("ConfigureDBDialog", u"Create new DB", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mysql), QCoreApplication.translate("ConfigureDBDialog", u"MySQL", None))
    # retranslateUi

