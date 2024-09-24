"""FTP server and cameras UI Module"""

import os
import keyring
from validators import ipv4

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog
from PySide6.QtGui import QIcon

from src.ui.ui_configure_ftp_cameras import Ui_DialogFTPCameras
from src.domain.ftps_server import FTPsServer


class DialogFTPCameras(QDialog, Ui_DialogFTPCameras):
    """Class to configure FTP server and cameras"""
    def __init__(self, ftp_server: FTPsServer, cameras):
        super(DialogFTPCameras, self).__init__()
        self.ui = Ui_DialogFTPCameras()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(
            os.getcwd(), "src", "img","mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.pushButton_testFTPServer.setEnabled(False)
        self.ui.label_errorMessage.setStyleSheet("color: red")

        # FTP Server and Cameras
        self.ftp_server = ftp_server
        self.cameras = cameras

        # Slots
        self.ui.pushButton_selectKeyFile.clicked.connect(self.select_key_file)
        self.ui.pushButton_sekectCertificateKey.clicked.connect(self.select_certificate_file)
        self.ui.lineEdit_ip.textChanged.connect(self.validate)
        self.ui.lineEdit_ip.textChanged.connect(self.validate)
        self.ui.lineEdit_max_conn.textChanged.connect(self.validate)
        self.ui.lineEdit_max_conn_ip.textChanged.connect(self.validate)

        # Init dialog
        self.initialize_dialog()

    def initialize_dialog(self):
        """Method to initialize dialog with existing values (if any)."""

        if self.ftp_server:
            self.ui.label_certificate_file_path.setText(self.ftp_server.handler.certfile)
            self.ui.label_key_file_path.setText(self.ftp_server.handler.keyfile)
            self.ui.lineEdit_ip.setText(self.ftp_server.server.address()[0])
            self.ui.lineEdit_port.setText(self.ftp_server.server.address()[1])
            self.ui.lineEdit_max_conn.setText(self.ftp_server.server.max_cons)
            self.ui.lineEdit_max_conn_ip.setText(self.ftp_server.server.max_cons_per_ip)
        else:
            self.ui.lineEdit_ip.setText("0.0.0.0")
            self.ui.lineEdit_port.setText("21")
            self.ui.lineEdit_max_conn.setText("50")
            self.ui.lineEdit_max_conn_ip.setText("5")

            #TODO: add cameras init
            for camera in self.cameras:
                credentials = keyring.get_credential(r"WADAS_FTP_Cam_{camera.id}", "")
                self.ui.lineEdit_username_1.setText(credentials.username)
                self.ui.lineEdit_password_1.setText(credentials.password)

    def select_key_file(self):
        """Method to select SSL key file"""

        file_name = QFileDialog.getOpenFileName(self, "Open SSL key file",
                                                os.getcwd(), "Pem File (*.pem)")
        self.ui.label_key_file_path.setText(str(file_name[0]))

    def select_certificate_file(self):
        """Method to select SSL certificate file"""

        file_name = QFileDialog.getOpenFileName(self, "Open SSL certificate file",
                                                os.getcwd(), "Pem File (*.pem)")
        self.ui.label_certificate_file_path.setText(str(file_name[0]))

    def validate(self):
        """Method to validate data prior to accept and close dialog."""

        #TODO: add cameras list validation
        valid = True
        if not ipv4(self.ui.lineEdit_ip.text()):
            self.ui.label_errorMessage.setText("Invalid server IP address provided!")
            valid = False
        if port := int(self.ui.lineEdit_port.text()) < 1 or port > 65535:
            self.ui.label_errorMessage.setText("Invalid server port provided!")
            valid = False
        if not os.path.isfile(self.ui.label_key_file_path.text()):
            self.ui.label_errorMessage.setText("Invalid SSL key file provided!")
            valid = False
        if not os.path.isfile(self.ui.label_certificate_file_path.text()):
            self.ui.label_errorMessage.setText("Invalid SSL key file provided!")
            valid = False
        if not self.ui.lineEdit_max_conn > 0:
            self.ui.label_errorMessage.setText("Invalid maximum connection value provided!")
            valid = False
        if not self.ui.lineEdit_max_conn_ip > 0:
            self.ui.label_errorMessage.setText("Invalid maximum connection per IP value provided!")
            valid = False

        if valid:
            self.ui.label_errorMessage.setText("")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

    def accept_and_close(self):
        """When Ok is clicked, save FTP config info before closing."""

        if self.ftp_server:
            self.ftp_server.handler.certfile = self.ui.label_certificate_file_path.text()
            self.ftp_server.handler.keyfile = self.ui.label_key_file_path.text()
            self.ftp_server.server.address()[0] = self.ui.lineEdit_ip.text()
            self.ftp_server.server.address()[1] = self.ui.lineEdit_port.text()
            self.ftp_server.server.max_cons = self.ui.lineEdit_max_conn.text()
            self.ftp_server.server.max_cons_per_ip = self.ui.lineEdit_max_conn_ip.text()
        else:
            self.ftp_server = FTPsServer(self.ui.lineEdit_ip.text(),
                                         int(self.ui.lineEdit_port.text()),
                                         int(self.ui.lineEdit_max_conn.text()),
                                         int(self.ui.lineEdit_max_conn_ip.text()),
                                         self.ui.label_certificate_file_path.text(),
                                         self.ui.label_key_file_path.text())

            #TODO: add cameras save
        self.accept()