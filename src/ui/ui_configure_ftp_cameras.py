# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configure_ftp_cameras.ui'
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
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_DialogFTPCameras(object):
    def setupUi(self, DialogFTPCameras):
        if not DialogFTPCameras.objectName():
            DialogFTPCameras.setObjectName(u"DialogFTPCameras")
        DialogFTPCameras.resize(639, 533)
        self.buttonBox = QDialogButtonBox(DialogFTPCameras)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 490, 621, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.label_errorMessage = QLabel(DialogFTPCameras)
        self.label_errorMessage.setObjectName(u"label_errorMessage")
        self.label_errorMessage.setGeometry(QRect(10, 470, 611, 16))
        self.gridLayoutWidget_5 = QWidget(DialogFTPCameras)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(0, 10, 631, 451))
        self.gridLayout_main = QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_main.setObjectName(u"gridLayout_main")
        self.gridLayout_main.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.gridLayoutWidget_5)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_FTPcameras = QWidget()
        self.tab_FTPcameras.setObjectName(u"tab_FTPcameras")
        self.gridLayoutWidget = QWidget(self.tab_FTPcameras)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 39, 611, 381))
        self.gridLayout_cameras = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_cameras.setObjectName(u"gridLayout_cameras")
        self.gridLayout_cameras.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_cameras.addWidget(self.label_9, 0, 4, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_cameras.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.lineEdit_username_1 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_username_1.setObjectName(u"lineEdit_username_1")

        self.gridLayout_cameras.addWidget(self.lineEdit_username_1, 0, 3, 1, 1)

        self.lineEdit_camera_id_1 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_camera_id_1.setObjectName(u"lineEdit_camera_id_1")

        self.gridLayout_cameras.addWidget(self.lineEdit_camera_id_1, 0, 1, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_cameras.addWidget(self.label_8, 0, 2, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_cameras.addWidget(self.label_7, 0, 0, 1, 1)

        self.lineEdit_password_1 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_password_1.setObjectName(u"lineEdit_password_1")
        self.lineEdit_password_1.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout_cameras.addWidget(self.lineEdit_password_1, 0, 5, 1, 1)

        self.pushButton = QPushButton(self.tab_FTPcameras)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 10, 131, 24))
        self.tabWidget.addTab(self.tab_FTPcameras, "")
        self.tab_FTPServer = QWidget()
        self.tab_FTPServer.setObjectName(u"tab_FTPServer")
        self.gridLayoutWidget_2 = QWidget(self.tab_FTPServer)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 611, 476))
        self.gridLayout = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_FTPServer = QGroupBox(self.gridLayoutWidget_2)
        self.groupBox_FTPServer.setObjectName(u"groupBox_FTPServer")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_FTPServer.sizePolicy().hasHeightForWidth())
        self.groupBox_FTPServer.setSizePolicy(sizePolicy)
        self.groupBox_FTPServer.setMinimumSize(QSize(0, 167))
        self.gridLayoutWidget_4 = QWidget(self.groupBox_FTPServer)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 20, 561, 141))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.gridLayoutWidget_4)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)

        self.lineEdit_port = QLineEdit(self.gridLayoutWidget_4)
        self.lineEdit_port.setObjectName(u"lineEdit_port")

        self.gridLayout_3.addWidget(self.lineEdit_port, 1, 1, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)

        self.lineEdit_ip = QLineEdit(self.gridLayoutWidget_4)
        self.lineEdit_ip.setObjectName(u"lineEdit_ip")

        self.gridLayout_3.addWidget(self.lineEdit_ip, 0, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget_4)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEdit_max_conn = QLineEdit(self.gridLayoutWidget_4)
        self.lineEdit_max_conn.setObjectName(u"lineEdit_max_conn")

        self.gridLayout_3.addWidget(self.lineEdit_max_conn, 2, 1, 1, 1)

        self.lineEdit_max_conn_ip = QLineEdit(self.gridLayoutWidget_4)
        self.lineEdit_max_conn_ip.setObjectName(u"lineEdit_max_conn_ip")

        self.gridLayout_3.addWidget(self.lineEdit_max_conn_ip, 3, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget_4)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 3, 2, 1, 1)


        self.gridLayout.addWidget(self.groupBox_FTPServer, 0, 0, 1, 1)

        self.groupBox_SSL = QGroupBox(self.gridLayoutWidget_2)
        self.groupBox_SSL.setObjectName(u"groupBox_SSL")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_SSL.sizePolicy().hasHeightForWidth())
        self.groupBox_SSL.setSizePolicy(sizePolicy1)
        self.groupBox_SSL.setMinimumSize(QSize(0, 92))
        self.gridLayoutWidget_3 = QWidget(self.groupBox_SSL)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(9, 29, 561, 84))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_sekectCertificateKey = QPushButton(self.gridLayoutWidget_3)
        self.pushButton_sekectCertificateKey.setObjectName(u"pushButton_sekectCertificateKey")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_sekectCertificateKey.sizePolicy().hasHeightForWidth())
        self.pushButton_sekectCertificateKey.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.pushButton_sekectCertificateKey, 1, 2, 1, 1)

        self.label_key_file_path = QLabel(self.gridLayoutWidget_3)
        self.label_key_file_path.setObjectName(u"label_key_file_path")

        self.gridLayout_2.addWidget(self.label_key_file_path, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.label_certificate_file_path = QLabel(self.gridLayoutWidget_3)
        self.label_certificate_file_path.setObjectName(u"label_certificate_file_path")

        self.gridLayout_2.addWidget(self.label_certificate_file_path, 1, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget_3)
        self.label.setObjectName(u"label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.pushButton_selectKeyFile = QPushButton(self.gridLayoutWidget_3)
        self.pushButton_selectKeyFile.setObjectName(u"pushButton_selectKeyFile")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_selectKeyFile.sizePolicy().hasHeightForWidth())
        self.pushButton_selectKeyFile.setSizePolicy(sizePolicy4)

        self.gridLayout_2.addWidget(self.pushButton_selectKeyFile, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.groupBox_SSL, 1, 0, 1, 1)

        self.groupBox_TestFTPServer = QGroupBox(self.gridLayoutWidget_2)
        self.groupBox_TestFTPServer.setObjectName(u"groupBox_TestFTPServer")
        self.groupBox_TestFTPServer.setMinimumSize(QSize(0, 190))
        self.verticalLayoutWidget = QWidget(self.groupBox_TestFTPServer)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 591, 151))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_testFTPServer = QPushButton(self.verticalLayoutWidget)
        self.pushButton_testFTPServer.setObjectName(u"pushButton_testFTPServer")

        self.verticalLayout.addWidget(self.pushButton_testFTPServer)

        self.scrollArea = QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 71))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 587, 69))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea, 0, Qt.AlignmentFlag.AlignTop)


        self.gridLayout.addWidget(self.groupBox_TestFTPServer, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tab_FTPServer, "")

        self.gridLayout_main.addWidget(self.tabWidget, 1, 0, 1, 1)


        self.retranslateUi(DialogFTPCameras)
        self.buttonBox.accepted.connect(DialogFTPCameras.accept)
        self.buttonBox.rejected.connect(DialogFTPCameras.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DialogFTPCameras)
    # setupUi

    def retranslateUi(self, DialogFTPCameras):
        DialogFTPCameras.setWindowTitle(QCoreApplication.translate("DialogFTPCameras", u"Configure FTP Server and Cameras", None))
        self.label_errorMessage.setText("")
#if QT_CONFIG(accessibility)
        self.tabWidget.setAccessibleName(QCoreApplication.translate("DialogFTPCameras", u"FTP Server", None))
#endif // QT_CONFIG(accessibility)
        self.label_9.setText(QCoreApplication.translate("DialogFTPCameras", u"password:", None))
        self.label_8.setText(QCoreApplication.translate("DialogFTPCameras", u"username:", None))
        self.label_7.setText(QCoreApplication.translate("DialogFTPCameras", u"Camera ID:", None))
        self.pushButton.setText(QCoreApplication.translate("DialogFTPCameras", u"Add FTP Camera", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_FTPcameras), QCoreApplication.translate("DialogFTPCameras", u"FTP Cameras", None))
        self.groupBox_FTPServer.setTitle(QCoreApplication.translate("DialogFTPCameras", u"FTP Server", None))
        self.label_5.setText(QCoreApplication.translate("DialogFTPCameras", u"Max connections:", None))
        self.label_6.setText(QCoreApplication.translate("DialogFTPCameras", u"Max connections per IP", None))
        self.label_4.setText(QCoreApplication.translate("DialogFTPCameras", u"Port:", None))
        self.label_3.setText(QCoreApplication.translate("DialogFTPCameras", u"IP:", None))
        self.groupBox_SSL.setTitle(QCoreApplication.translate("DialogFTPCameras", u"SSL", None))
        self.pushButton_sekectCertificateKey.setText(QCoreApplication.translate("DialogFTPCameras", u"Select certificate file", None))
        self.label_key_file_path.setText("")
        self.label_certificate_file_path.setText("")
        self.label_2.setText(QCoreApplication.translate("DialogFTPCameras", u"Certificate file:", None))
        self.label.setText(QCoreApplication.translate("DialogFTPCameras", u"Key file:", None))
        self.pushButton_selectKeyFile.setText(QCoreApplication.translate("DialogFTPCameras", u"Select key file", None))
        self.groupBox_TestFTPServer.setTitle(QCoreApplication.translate("DialogFTPCameras", u"Test FTP Server", None))
        self.pushButton_testFTPServer.setText(QCoreApplication.translate("DialogFTPCameras", u"Test FTP Server", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_FTPServer), QCoreApplication.translate("DialogFTPCameras", u"FTP Server", None))
    # retranslateUi

