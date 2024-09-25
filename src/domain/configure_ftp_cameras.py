"""FTP server and cameras UI Module"""

import os
import keyring
from validators import ipv4

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QLineEdit, QRadioButton, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from src.domain.camera import Camera
from src.domain.camera import cameras
from src.domain.ftp_camera import FTPCamera
from src.ui.ui_configure_ftp_cameras import Ui_DialogFTPCameras
from src.domain.ftps_server import FTPsServer


class DialogFTPCameras(QDialog, Ui_DialogFTPCameras):
    """Class to configure FTP server and cameras"""
    def __init__(self, ftp_server: FTPsServer):
        super(DialogFTPCameras, self).__init__()
        self.ui = Ui_DialogFTPCameras()
        self.num_of_cameras = 1

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(
            os.getcwd(), "src", "img","mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.pushButton_testFTPServer.setEnabled(False)
        self.ui.pushButton_stopFTPServer.setEnabled(False)
        self.ui.pushButton_removeFTPCamera.setEnabled(False)
        self.ui.label_errorMessage.setStyleSheet("color: red")

        # FTP Server and Cameras
        self.ftp_server = ftp_server

        # Slots
        self.ui.pushButton_selectKeyFile.clicked.connect(self.select_key_file)
        self.ui.pushButton_sekectCertificateKey.clicked.connect(self.select_certificate_file)
        self.ui.lineEdit_ip.textChanged.connect(self.validate)
        self.ui.lineEdit_ip.textChanged.connect(self.validate)
        self.ui.lineEdit_max_conn.textChanged.connect(self.validate)
        self.ui.lineEdit_max_conn_ip.textChanged.connect(self.validate)
        self.ui.lineEdit_camera_id_1.textChanged.connect(self.validate)
        self.ui.lineEdit_username_1.textChanged.connect(self.validate)
        self.ui.lineEdit_password_1.textChanged.connect(self.validate)
        self.ui.pushButton_addFTPCamera.clicked.connect(self.add_ftp_camera)
        self.ui.pushButton_testFTPServer.clicked.connect(self.test_ftp_server)
        self.ui.pushButton_select_FTPserver_folder.clicked.connect(self.select_ftp_folder)

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
        if cameras:
            for camera in cameras:
                if camera.type == Camera.CameraTypes.FTPCamera:
                    credentials = keyring.get_credential(r"WADAS_FTPCamera_{camera.id}", "")
                    if credentials:
                        self.ui.lineEdit_username_1.setText(credentials.username)
                        self.ui.lineEdit_password_1.setText(credentials.password)

    def select_key_file(self):
        """Method to select SSL key file"""

        file_name = QFileDialog.getOpenFileName(self, "Open SSL key file",
                                                os.getcwd(), "Pem File (*.pem)")
        self.ui.label_key_file_path.setText(str(file_name[0]))
        self.validate()

    def select_certificate_file(self):
        """Method to select SSL certificate file"""

        file_name = QFileDialog.getOpenFileName(self, "Open SSL certificate file",
                                                os.getcwd(), "Pem File (*.pem)")
        self.ui.label_certificate_file_path.setText(str(file_name[0]))
        self.validate()

    def select_ftp_folder(self):
        """Method to select FTP Server folder."""

        dir = QFileDialog.getExistingDirectory(self, "Select FTP Server folder", os.getcwd())
        self.ui.label_FTPServer_path.setText(dir)
        self.validate()

    def validate(self):
        """Method to validate data prior to accept and close dialog."""

        #TODO: add cameras list validation
        valid = True
        if not ipv4(self.ui.lineEdit_ip.text()):
            self.ui.label_errorMessage.setText("Invalid server IP address provided!")
            valid = False
        if port := self.ui.lineEdit_port.text():
            if int(port) < 1 or int(port) > 65535:
                self.ui.label_errorMessage.setText("Invalid server port provided!")
                valid = False
        else:
            self.ui.label_errorMessage.setText("No server port provided!")
            valid = False
        if not os.path.isfile(self.ui.label_key_file_path.text()):
            self.ui.label_errorMessage.setText("Invalid SSL key file provided!")
            valid = False
        if not os.path.isfile(self.ui.label_certificate_file_path.text()):
            self.ui.label_errorMessage.setText("Invalid SSL key file provided!")
            valid = False
        if not os.path.isdir(self.ui.label_FTPServer_path.text()):
            self.ui.label_errorMessage.setText("Invalid FTP server directory provided!")
            valid = False
        max_conn = self.ui.lineEdit_max_conn.text()
        if not max_conn or int(max_conn) < 0:
            self.ui.label_errorMessage.setText("No or Invalid maximum connection value provided!")
            valid = False
        max_conn_per_ip = self.ui.lineEdit_max_conn_ip.text()
        if not max_conn_per_ip or int(max_conn_per_ip) < 0:
            self.ui.label_errorMessage.setText("No or Invalid maximum connection per IP value provided!")
            valid = False

        i = 1
        while i <= self.num_of_cameras:
            camera_id_ui = f"lineEdit_camera_id_{i}"
            camera_id_ln = self.findChild(QLineEdit, camera_id_ui)
            if camera_id_ln and not camera_id_ln.text():
                self.ui.label_errorMessage.setText("No Camera ID provided!")
                valid = False
            i = i+1

        if valid:
            self.ui.label_errorMessage.setText("")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)
        self.ui.pushButton_testFTPServer.setEnabled(valid)

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

        if cameras:
            for camera in cameras:
                if camera.type == Camera.CameraTypes.FTPCamera:
                    #TODO: check for previously configured FTP camera to update
                    pass
        else:
            # Insert brand new Camera in list
            for i in range(self.num_of_cameras):
                camera_id_ui = f"lineEdit_camera_id_{i}"
                camera_id_ln = self.findChild(QLineEdit, camera_id_ui)
                camera = FTPCamera(camera_id_ln.text(), True, camera_id_ln.text())
                cameras.append(camera)
                # Store credentials in keyring
                camera_user_ui = f"lineEdit_username_{i}"
                camera_user_ln = self.findChild(QLineEdit, camera_user_ui)
                camera_pass_ui = f"lineEdit_password_{i}"
                camera_pass_ln = self.findChild(QLineEdit, camera_pass_ui)
                keyring.set_password(f"WADAS_FTPCamera_{camera_id_ln.text()}",
                                     camera_user_ln.text(),
                                     camera_pass_ln.text())

        self.accept()

    def add_ftp_camera(self):
        """Method to add new FTP camera line edits."""

        row = self.num_of_cameras+1
        # Camera selection check box
        radio_button = QRadioButton()
        radiob_obj_name = f"checkBox_camera_{row}"
        radio_button.setObjectName(radiob_obj_name)
        radio_button.setChecked(False)
        self.ui.gridLayout_cameras.addWidget(radio_button, row, 0)

        # Camera id
        label = QLabel("ID:")
        label.setObjectName(f"label_cameraId_{row}")
        self.ui.gridLayout_cameras.addWidget(label, row, 1)
        id_line_edit = QLineEdit()
        lnedit_obj_name = f"lineEdit_camera_id_{row}"
        id_line_edit.setObjectName(lnedit_obj_name)
        id_line_edit.textChanged.connect(self.validate)
        self.ui.gridLayout_cameras.addWidget(id_line_edit, row, 2)
        # Camera FTP user
        label = QLabel("user:")
        label.setObjectName(f"label_cameraUser_{row}")
        label.setToolTip("FTP user name")
        self.ui.gridLayout_cameras.addWidget(label, row, 3)
        user_line_edit = QLineEdit()
        lnedit_obj_name = f"lineEdit_username_{row}"
        user_line_edit.setObjectName(lnedit_obj_name)
        user_line_edit.textChanged.connect(self.validate)
        self.ui.gridLayout_cameras.addWidget(user_line_edit, row, 4)
        # Camera password
        label = QLabel("password:")
        label.setObjectName(f"label_cameraPass_{row}")
        self.ui.gridLayout_cameras.addWidget(label, row, 5)
        pass_line_edit = QLineEdit()
        lnedit_obj_name = f"lineEdit_password_{row}"
        pass_line_edit.setObjectName(lnedit_obj_name)
        pass_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        pass_line_edit.textChanged.connect(self.validate)
        self.ui.gridLayout_cameras.addWidget(pass_line_edit, row, 6)

        self.ui.gridLayout_cameras.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.num_of_cameras = self.num_of_cameras+1

    def test_ftp_server(self):
        """Method to test out FTP server configuration options by running a FTP server instance."""

        ftps_server = FTPsServer(self.ui.lineEdit_ip.text(),
                                         int(self.ui.lineEdit_port.text()),
                                         int(self.ui.lineEdit_max_conn.text()),
                                         int(self.ui.lineEdit_max_conn_ip.text()),
                                         self.ui.label_certificate_file_path.text(),
                                         self.ui.label_key_file_path.text())
        ftps_server.add_user(self.ui.lineEdit_username_1.text(),
                             self.ui.lineEdit_password_1.text(),
                             self.ui.label_FTPServer_path.text())
        ftps_server.run()