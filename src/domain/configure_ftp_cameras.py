"""FTP server and cameras UI Module"""

import os
import keyring
import logging
from validators import ipv4

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QLineEdit, QRadioButton, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtCore import QThread

from src.domain.camera import Camera
from src.domain.camera import cameras
from src.domain.ftp_camera import FTPCamera
from src.ui.ui_configure_ftp_cameras import Ui_DialogFTPCameras
from src.domain.ftps_server import FTPsServer
from src.domain.qtextedit_logger import QTextEditLogger


class DialogFTPCameras(QDialog, Ui_DialogFTPCameras):
    """Class to configure FTP server and cameras"""
    def __init__(self):
        super(DialogFTPCameras, self).__init__()
        self.ui = Ui_DialogFTPCameras()
        self.num_of_cameras = 1
        self.ftp_thread = None

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(
            os.getcwd(), "src", "img","mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.pushButton_testFTPServer.setEnabled(False)
        self.ui.pushButton_stopFTPServer.setEnabled(False)
        self.ui.pushButton_removeFTPCamera.setEnabled(False)
        self.ui.label_errorMessage.setStyleSheet("color: red")

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
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
        self.ui.pushButton_stopFTPServer.clicked.connect(self.stop_ftp_server)

        # Init dialog
        self.initialize_dialog()
        self._setup_logger()

    def initialize_dialog(self):
        """Method to initialize dialog with existing values (if any)."""

        if FTPsServer.ftps_server:
            self.ui.label_certificate_file_path.setText(FTPsServer.ftps_server.certificate)
            self.ui.label_key_file_path.setText(FTPsServer.ftps_server.key)
            self.ui.label_FTPServer_path.setText(FTPsServer.ftps_server.ftp_dir)
            self.ui.lineEdit_ip.setText(FTPsServer.ftps_server.ip)
            self.ui.lineEdit_port.setText(str(FTPsServer.ftps_server.port))
            self.ui.lineEdit_max_conn.setText(str(FTPsServer.ftps_server.max_conn))
            self.ui.lineEdit_max_conn_ip.setText(str(FTPsServer.ftps_server.max_conn_per_ip))
        else:
            self.ui.lineEdit_ip.setText("0.0.0.0")
            self.ui.lineEdit_port.setText("21")
            self.ui.lineEdit_max_conn.setText("50")
            self.ui.lineEdit_max_conn_ip.setText("5")

        if cameras:
            for camera in cameras:
                i = 1
                if camera.type == Camera.CameraTypes.FTPCamera:
                    if i > 1:
                        self.add_ftp_camera()
                    camera_id_ui = f"lineEdit_camera_id_{i}"
                    camera_id_ln = self.findChild(QLineEdit, camera_id_ui)
                    camera_id_ln.setText(camera.id)
                    credentials = keyring.get_credential(f"WADAS_FTPcamera_{camera.id}", "")
                    if credentials:
                        camera_user_ui = f"lineEdit_username_{i}"
                        camera_user_ln = self.findChild(QLineEdit, camera_user_ui)
                        camera_user_ln.setText(credentials.username)
                        camera_pass_ui = f"lineEdit_password_{i}"
                        camera_pass_ln = self.findChild(QLineEdit, camera_pass_ui)
                        camera_pass_ln.setText(credentials.password)

    def accept_and_close(self):
        """When Ok is clicked, save FTP config info before closing."""

        if FTPsServer.ftps_server:
            FTPsServer.ftps_server.handler.certfile = self.ui.label_certificate_file_path.text()
            FTPsServer.ftps_server.handler.keyfile = self.ui.label_key_file_path.text()
            FTPsServer.ftps_server.ftp_dir = self.ui.label_FTPServer_path.text()
            #TODO: fix server address value update
            #FTPsServer.ftps_server.server.address()[0] = self.ui.lineEdit_ip.text()
            #FTPsServer.ftps_server.server.address()[1] = self.ui.lineEdit_port.text()
            FTPsServer.ftps_server.server.max_cons = self.ui.lineEdit_max_conn.text()
            FTPsServer.ftps_server.server.max_cons_per_ip = self.ui.lineEdit_max_conn_ip.text()
        else:
            FTPsServer.ftps_server = FTPsServer(self.ui.lineEdit_ip.text(),
                                     int(self.ui.lineEdit_port.text()),
                                     int(self.ui.lineEdit_max_conn.text()),
                                     int(self.ui.lineEdit_max_conn_ip.text()),
                                     self.ui.label_certificate_file_path.text(),
                                     self.ui.label_key_file_path.text(),
                                     self.ui.label_FTPServer_path.text())
        if cameras:
            # Check for need of updating cameras credentials. If camera ID changes it is seen as new camera.
            i = 1
            ui_camera_id = []
            while i <= self.num_of_cameras:
                cur_ui_id = self.get_camera_id(i)
                ui_camera_id.append(cur_ui_id)
                for camera in cameras:
                    if camera.type == Camera.CameraTypes.FTPCamera:
                        if cur_ui_id == camera.id:
                            cur_user = self.get_camera_user(i)
                            cur_pass = self.get_camera_pass(i)
                            credentials = keyring.get_credential(f"WADAS_FTPcamera_{camera.id}", "")
                            if credentials and (credentials.username != cur_user or credentials.password != cur_pass):
                                keyring.set_password(f"WADAS_FTPcamera_{cur_ui_id}", cur_user, cur_pass)
                                break
                # If camera id is not in cameras list, then is new or modified
                camera = FTPCamera(cur_ui_id, os.path.join(FTPsServer.ftps_server.ftp_dir, cur_ui_id))
                cameras.append(camera)
                # Store credentials in keyring
                keyring.set_password(f"WADAS_FTPcamera_{cur_ui_id}", self.get_camera_user(i),
                                     self.get_camera_pass(i))
                i = i + 1

            # Check for cameras old id (prior to modification) and remove them
            orphan_cameras = [camera for camera in cameras if camera.id not in ui_camera_id]
            for camera in orphan_cameras:
                cameras.remove(camera)
        else:
            # Insert new camera(s) in list (including the ones with modified id)
            i=1
            while i <= self.num_of_cameras:
                cur_camera_id = self.get_camera_id(i)
                camera = FTPCamera(cur_camera_id, os.path.join(FTPsServer.ftps_server.ftp_dir, cur_camera_id))
                cameras.append(camera)
                # Store credentials in keyring
                keyring.set_password(f"WADAS_FTPcamera_{cur_camera_id}", self.get_camera_user(i),
                                     self.get_camera_pass(i))
                i = i+1
        self.accept()

    def get_camera_id(self, row):
        """Method to get camera id text from UI programmatically by row number"""
        camera_id_ui = f"lineEdit_camera_id_{row}"
        camera_id_ln = self.findChild(QLineEdit, camera_id_ui)
        return camera_id_ln.text()

    def get_camera_user(self, row):
        """Method to get camera username text from UI programmatically by row number"""
        camera_user_ui = f"lineEdit_username_{row}"
        camera_user_ln = self.findChild(QLineEdit, camera_user_ui)
        return camera_user_ln.text()

    def get_camera_pass(self, row):
        """Method to get camera password text from UI programmatically by row number"""
        camera_pass_ui = f"lineEdit_password_{row}"
        camera_pass_ln = self.findChild(QLineEdit, camera_pass_ui)
        return camera_pass_ln.text()

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
            if not self.get_camera_id(i):
                self.ui.label_errorMessage.setText("No Camera ID provided!")
                valid = False
            i = i+1

        if valid:
            self.ui.label_errorMessage.setText("")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)
        self.ui.pushButton_testFTPServer.setEnabled(valid)

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

        if not FTPsServer.ftps_server:
            FTPsServer.ftps_server = FTPsServer(self.ui.lineEdit_ip.text(),
                                                int(self.ui.lineEdit_port.text()),
                                                int(self.ui.lineEdit_max_conn.text()),
                                                int(self.ui.lineEdit_max_conn_ip.text()),
                                                self.ui.label_certificate_file_path.text(),
                                                self.ui.label_key_file_path.text())
        i = 1
        while i <= self.num_of_cameras:
            if not FTPsServer.ftps_server.has_user(self.get_camera_id(i)):
                FTPsServer.ftps_server.add_user(self.get_camera_user(i),
                                               self.get_camera_pass(i),
                                               self.ui.label_FTPServer_path.text())
            i = i+1

        self.ftp_thread = QThread()
        # Move operation mode in dedicated thread
        FTPsServer.ftps_server.moveToThread(self.ftp_thread)

        # Connect thread related signals and slots
        self.ftp_thread.started.connect(FTPsServer.ftps_server.run)
        FTPsServer.ftps_server.run_finished.connect(self.ftp_thread.quit)
        FTPsServer.ftps_server.run_finished.connect(FTPsServer.ftps_server.deleteLater)
        self.ftp_thread.finished.connect(self.ftp_thread.deleteLater)

        self.ui.pushButton_stopFTPServer.setEnabled(True)
        # Start the thread
        self.ftp_thread.start()

    def stop_ftp_server(self):
        """Method to stop FTP server thread"""

        if self.ftp_thread and FTPsServer.ftps_server:
            FTPsServer.ftps_server.server.close_all()
            FTPsServer.ftps_server.server.close()
            self.ftp_thread.requestInterruption()
            self.ui.pushButton_stopFTPServer.setEnabled(False)

    def _setup_logger(self):
        """Initialize logger for UI logging."""

        logger = logging.getLogger("pyftpdlib")
        log_textbox = QTextEditLogger(self.ui.plainTextEdit_FTPserver_log)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_textbox)