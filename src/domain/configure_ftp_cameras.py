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
from src.domain.ftps_server import ftps_server
from src.domain.qtextedit_logger import QTextEditLogger

logger = logging.getLogger(__name__)


class DialogFTPCameras(QDialog, Ui_DialogFTPCameras):
    """Class to configure FTP server and cameras"""
    def __init__(self):
        super(DialogFTPCameras, self).__init__()
        self.ui = Ui_DialogFTPCameras()
        self.num_of_cameras = 1
        self.ftp_thread = None
        self.test_ftps_server = None

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

        if ftps_server:
            self.ui.label_certificate_file_path.setText(ftps_server.certificate)
            self.ui.label_key_file_path.setText(ftps_server.key)
            self.ui.label_FTPServer_path.setText(ftps_server.ftp_dir)
            self.ui.lineEdit_ip.setText(ftps_server.ip)
            self.ui.lineEdit_port.setText(str(ftps_server.port))
            self.ui.lineEdit_max_conn.setText(str(ftps_server.max_conn))
            self.ui.lineEdit_max_conn_ip.setText(str(ftps_server.max_conn_per_ip))
        else:
            self.ui.lineEdit_ip.setText("0.0.0.0")
            self.ui.lineEdit_port.setText("21")
            self.ui.lineEdit_max_conn.setText("50")
            self.ui.lineEdit_max_conn_ip.setText("5")

            #TODO: add cameras init
        if cameras:
            for camera in cameras:
                if camera.type == Camera.CameraTypes.FTPCamera:
                    self.ui.lineEdit_camera_id_1.setText(camera.id)
                    credentials = keyring.get_credential(f"WADAS_FTPcamera_{camera.id}", "")
                    if credentials:
                        self.ui.lineEdit_username_1.setText(credentials.username)
                        self.ui.lineEdit_password_1.setText(credentials.password)

    def accept_and_close(self):
        """When Ok is clicked, save FTP config info before closing."""

        if ftps_server:
            ftps_server.handler.certfile = self.ui.label_certificate_file_path.text()
            ftps_server.handler.keyfile = self.ui.label_key_file_path.text()
            ftps_server.ftp_dir = self.ui.label_FTPServer_path.text()
            ftps_server.server.address()[0] = self.ui.lineEdit_ip.text()
            ftps_server.server.address()[1] = self.ui.lineEdit_port.text()
            ftps_server.server.max_cons = self.ui.lineEdit_max_conn.text()
            ftps_server.server.max_cons_per_ip = self.ui.lineEdit_max_conn_ip.text()
        else:
            ftps_server = FTPsServer(self.ui.lineEdit_ip.text(),
                                     int(self.ui.lineEdit_port.text()),
                                     int(self.ui.lineEdit_max_conn.text()),
                                     int(self.ui.lineEdit_max_conn_ip.text()),
                                     self.ui.label_certificate_file_path.text(),
                                     self.ui.label_key_file_path.text(),
                                     self.ui.label_FTPServer_path.text())
        if cameras:
            i = 1
            ui_camera_id = []
            while i <= self.num_of_cameras:
                camera_id_ui = f"lineEdit_camera_id_{i}"
                camera_id_ln = self.findChild(QLineEdit, camera_id_ui)
                ui_camera_id.append(camera_id_ln.text())
                for camera in cameras:
                    if camera.type == Camera.CameraTypes.FTPCamera:
                        if camera_id_ln.text() == camera.id:
                            credentials = keyring.get_credential(f"WADAS_FTPcamera_{camera.id}", "")
                            if credentials and (credentials.username != self.ui.lineEdit_username_1 or
                            credentials.password != self.ui.lineEdit_password_1):
                                keyring.set_password(f"WADAS_FTPcamera_{camera_id_ln.text()}",
                                                     camera_user_ln.text(),
                                                     camera_pass_ln.text())
                                break
                i = i + 1
            orphan_cameras = [camera for camera in cameras if camera not in ui_camera_id]
            for camera in orphan_cameras:
                cameras.delete(camera)
        else:
            # Insert brand new Camera in list
            i=1
            while i <= self.num_of_cameras:
                camera_id_ui = f"lineEdit_camera_id_{i}"
                camera_id_ln = self.findChild(QLineEdit, camera_id_ui)
                camera = FTPCamera(camera_id_ln.text(), True, camera_id_ln.text())
                cameras.append(camera)
                # Store credentials in keyring
                camera_user_ui = f"lineEdit_username_{i}"
                camera_user_ln = self.findChild(QLineEdit, camera_user_ui)
                camera_pass_ui = f"lineEdit_password_{i}"
                camera_pass_ln = self.findChild(QLineEdit, camera_pass_ui)
                keyring.set_password(f"WADAS_FTPcamera_{camera_id_ln.text()}",
                                     camera_user_ln.text(),
                                     camera_pass_ln.text())
                i = i+1
        self.accept()

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

        logger.info("Starting test FTP server...")
        self.test_ftps_server = FTPsServer(self.ui.lineEdit_ip.text(),
                                           int(self.ui.lineEdit_port.text()),
                                           int(self.ui.lineEdit_max_conn.text()),
                                           int(self.ui.lineEdit_max_conn_ip.text()),
                                           self.ui.label_certificate_file_path.text(),
                                           self.ui.label_key_file_path.text(),
                                           self.ui.label_FTPServer_path.text())
        self.test_ftps_server.add_user(self.ui.lineEdit_username_1.text(),
                                       self.ui.lineEdit_password_1.text(),
                                       self.ui.label_FTPServer_path.text())

        self.ui.pushButton_stopFTPServer.setEnabled(True)

        self.ftp_thread = QThread()
        # Move operation mode in dedicated thread
        self.test_ftps_server.moveToThread(self.ftp_thread)

        # Connect thread related signals and slots
        self.ftp_thread.started.connect(self.test_ftps_server.run)
        self.test_ftps_server.run_finished.connect(self.ftp_thread.quit)
        self.test_ftps_server.run_finished.connect(self.test_ftps_server.deleteLater)
        self.ftp_thread.finished.connect(self.ftp_thread.deleteLater)

        # Start the thread
        self.ftp_thread.start()

    def stop_ftp_server(self):
        """Method to stop FTP server thread"""

        if self.ftp_thread and ftps_server:
            self.test_ftps_server.close_all()
            self.ui.pushButton_stopFTPServer.setEnabled(False)

    def _setup_logger(self):
        """Initialize logger for UI logging."""

        log_textbox = QTextEditLogger(self.ui.plainTextEdit_FTPserver_log)
        log_textbox.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_textbox)
        logger.propagate = False