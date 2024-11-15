"""FTP server and cameras UI Module"""

import logging
import os

import keyring
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QScrollArea,
    QWidget, QMessageBox,
)
from prompt_toolkit.key_binding.bindings.named_commands import end_of_file
from validators import ipv4

from wadas.domain.camera import Camera, cameras
from wadas.domain.ftp_camera import FTPCamera
from wadas.domain.ftps_server import FTPsServer
from wadas.domain.qtextedit_logger import QTextEditLogger
from wadas.ui.qt.ui_configure_ftp_cameras import Ui_DialogFTPCameras

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class DialogFTPCameras(QDialog, Ui_DialogFTPCameras):
    """Class to configure FTP server and cameras"""

    def __init__(self):
        super(DialogFTPCameras, self).__init__()
        self.ui = Ui_DialogFTPCameras()
        self.ui_camera_idx = 0
        self.ftp_thread = None
        self.removed_cameras = []
        self.removed_rows = set()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.pushButton_testFTPServer.setEnabled(False)
        self.ui.pushButton_stopFTPServer.setEnabled(False)
        self.ui.pushButton_removeFTPCamera.setEnabled(False)
        self.ui.label_errorMessage.setStyleSheet("color: red")

        # Create scrollable area for ftp camera list in FTPCamera tab
        scroll_area = QScrollArea(self.ui.tab_FTPcameras)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        cameras_grid_layout = QGridLayout(scroll_widget)
        cameras_grid_layout.setObjectName("gridLayout_cameras")
        self.ui.verticalLayout_FTPCameraTab.addWidget(scroll_area)
        # Adding first row of camera form
        self.add_ftp_camera()

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.pushButton_selectKeyFile.clicked.connect(self.select_key_file)
        self.ui.pushButton_sekectCertificateKey.clicked.connect(self.select_certificate_file)
        self.ui.lineEdit_ip.textChanged.connect(self.validate)
        self.ui.lineEdit_port.textChanged.connect(self.validate)
        self.ui.lineEdit_passive_port_range_start.textChanged.connect(self.validate)
        self.ui.lineEdit_passive_port_range_end.textChanged.connect(self.validate)
        self.ui.lineEdit_max_conn.textChanged.connect(self.validate)
        self.ui.lineEdit_max_conn_ip.textChanged.connect(self.validate)
        self.ui.pushButton_addFTPCamera.clicked.connect(self.add_ftp_camera)
        self.ui.pushButton_removeFTPCamera.clicked.connect(self.remove_ftp_camera)
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
            self.ui.lineEdit_passive_port_range_start.setText(str(min(FTPsServer.ftps_server.passive_ports)))
            self.ui.lineEdit_passive_port_range_end.setText(str(max(FTPsServer.ftps_server.passive_ports)))
        else:
            self.ui.lineEdit_ip.setText("0.0.0.0")
            self.ui.lineEdit_port.setText("21")
            self.ui.lineEdit_max_conn.setText("50")
            self.ui.lineEdit_max_conn_ip.setText("5")
            self.ui.lineEdit_passive_port_range_start.setText("65522")
            self.ui.lineEdit_passive_port_range_end.setText("65523")

        self.list_ftp_cameras_in_tab()

    def list_ftp_cameras_in_tab(self):
        """Method to list cameras in FTPCameras tab."""
        if cameras:
            i = 0
            for camera in cameras:
                if camera.type == Camera.CameraTypes.FTP_CAMERA:
                    if i > 0:
                        self.add_ftp_camera()
                    camera_id_ln = self.findChild(QLineEdit, f"lineEdit_camera_id_{i}")
                    camera_id_ln.setText(camera.id)
                    credentials = keyring.get_credential(f"WADAS_FTP_camera_{camera.id}", "")
                    if credentials:
                        camera_user_ln = self.findChild(QLineEdit, f"lineEdit_username_{i}")
                        camera_user_ln.setText(credentials.username)
                        camera_pass_ln = self.findChild(QLineEdit, f"lineEdit_password_{i}")
                        camera_pass_ln.setText(credentials.password)
                    i += 1

    def accept_and_close(self):
        """When Ok is clicked, save FTP config info before closing."""

        # If server object exists needs to be closed
        # in order to be edited (otherwise socket editing fails)
        if FTPsServer.ftps_server and FTPsServer.ftps_server.server:
            FTPsServer.ftps_server.server.close_all()

        FTPsServer.ftps_server = FTPsServer(
            self.ui.lineEdit_ip.text(),
            int(self.ui.lineEdit_port.text()),
            list(range(int(self.ui.lineEdit_passive_port_range_start.text()),
                       int(self.ui.lineEdit_passive_port_range_end.text()) + 1)),
            int(self.ui.lineEdit_max_conn.text()),
            int(self.ui.lineEdit_max_conn_ip.text()),
            self.ui.label_certificate_file_path.text(),
            self.ui.label_key_file_path.text(),
            self.ui.label_FTPServer_path.text(),
        )
        if cameras:
            # Check for need of updating cameras credentials.
            # If camera ID changes it is seen as new camera.
            ui_camera_id = []
            for i in range(0, self.ui_camera_idx):
                if i in self.removed_rows:
                    continue

                cur_ui_id = self.get_camera_id(i)
                if cur_ui_id:
                    ui_camera_id.append(cur_ui_id)
                    found = False
                    for camera in cameras:
                        if camera.type == Camera.CameraTypes.FTP_CAMERA:
                            if cur_ui_id == camera.id:
                                found = True
                                cur_user = self.get_camera_user(i)
                                cur_pass = self.get_camera_pass(i)
                                if cur_user and cur_pass:
                                    credentials = keyring.get_credential(
                                        f"WADAS_FTP_camera_{camera.id}", ""
                                    )
                                    if credentials and (
                                            credentials.username != cur_user
                                            or credentials.password != cur_pass
                                    ):
                                        keyring.set_password(
                                            f"WADAS_FTP_camera_{cur_ui_id}",
                                            cur_user,
                                            cur_pass,
                                        )
                                        break
                    if not found:
                        # If camera id is not in cameras list, then is new or modified
                        camera = FTPCamera(
                            cur_ui_id,
                            os.path.join(FTPsServer.ftps_server.ftp_dir, cur_ui_id),
                        )
                        cameras.append(camera)
                        # Store credentials in keyring
                        keyring.set_password(
                            f"WADAS_FTP_camera_{cur_ui_id}",
                            self.get_camera_user(i),
                            self.get_camera_pass(i),
                        )

            # Check for cameras old id (prior to modification) and remove them
            orphan_cameras = (
                camera
                for camera in cameras
                if camera.id not in ui_camera_id and camera.type == Camera.CameraTypes.FTP_CAMERA
            )
            for camera in orphan_cameras:
                cameras.remove(camera)
            for camera in tuple(cameras):
                if camera.id in self.removed_cameras:
                    if camera.type == Camera.CameraTypes.FTP_CAMERA:
                        cameras.remove(camera)
        else:
            # Insert new camera(s) in list (including the ones with modified id)
            for i in range(0, self.ui_camera_idx):
                cur_camera_id = self.get_camera_id(i)
                if cur_camera_id:
                    cur_cam_ftp_dir = os.path.join(FTPsServer.ftps_server.ftp_dir, cur_camera_id)
                    camera = FTPCamera(cur_camera_id, cur_cam_ftp_dir)
                    cameras.append(camera)
                    # Store credentials in keyring
                    keyring.set_password(
                        f"WADAS_FTP_camera_{cur_camera_id}",
                        self.get_camera_user(i),
                        self.get_camera_pass(i),
                    )
                    # Add camera user to FTPS server
                    if not FTPsServer.ftps_server.has_user(cur_camera_id):
                        if not os.path.isdir(cur_cam_ftp_dir):
                            os.makedirs(cur_cam_ftp_dir, exist_ok=True)
                        FTPsServer.ftps_server.add_user(
                            self.get_camera_user(i),
                            self.get_camera_pass(i),
                            cur_cam_ftp_dir,
                        )
        self.accept()

    def get_camera_id(self, row):
        """Method to get camera id text from UI programmatically by row number"""
        camera_id_ln = self.findChild(QLineEdit, f"lineEdit_camera_id_{row}")
        return camera_id_ln.text() if camera_id_ln else None

    def get_camera_user(self, row):
        """Method to get camera username text from UI programmatically by row number"""
        camera_user_ln = self.findChild(QLineEdit, f"lineEdit_username_{row}")
        return camera_user_ln.text() if camera_user_ln else None

    def get_camera_pass(self, row):
        """Method to get camera password text from UI programmatically by row number"""
        camera_pass_ln = self.findChild(QLineEdit, f"lineEdit_password_{row}")
        return camera_pass_ln.text() if camera_pass_ln else None

    def select_key_file(self):
        """Method to select SSL key file"""

        file_name = QFileDialog.getOpenFileName(
            self, "Open SSL key file", os.getcwd(), "Pem File (*.pem)"
        )
        self.ui.label_key_file_path.setText(str(file_name[0]))
        self.validate()

    def select_certificate_file(self):
        """Method to select SSL certificate file"""

        file_name = QFileDialog.getOpenFileName(
            self, "Open SSL certificate file", os.getcwd(), "Pem File (*.pem)"
        )
        self.ui.label_certificate_file_path.setText(str(file_name[0]))
        self.validate()

    def select_ftp_folder(self):
        """Method to select FTP Server folder."""

        dir = QFileDialog.getExistingDirectory(self, "Select FTP Server folder", os.getcwd())
        self.ui.label_FTPServer_path.setText(dir)
        self.validate()

    def validate_port(self, port, port_name):
        """Validate port method"""

        try:
            port_to_int = int(port)
        except  ValueError:
            self.ui.label_errorMessage.setText(f"Invalid {port_name} port type. Shall be an integer value!")
            return False

        if port_to_int < 1 or port_to_int > 65535:
            self.ui.label_errorMessage.setText(f"Invalid {port_name} port provided!")
            return False
        else:
            return True

    def validate_passive_port_range(self, start_passive_port, end_passive_port):
        """Method to validate passive ports range."""

        try:
            int_start_passive_port = int(start_passive_port)
        except ValueError:
            self.ui.label_errorMessage.setText(f"Invalid start passive port type. Shall be an integer value!")
            return False
        try:
            int_end_passive_port = int(end_passive_port)
        except ValueError:
            self.ui.label_errorMessage.setText(f"Invalid end passive port type. Shall be an integer value!")
            return False

        if start_passive_port and end_passive_port:
            if int_start_passive_port > int_end_passive_port:
                self.ui.label_errorMessage.setText("Start passive port cannot be greater than end passive port!")
                return False
            elif int_end_passive_port < int_start_passive_port:
                self.ui.label_errorMessage.setText("End passive port cannot be lower than start passive port!")
                return False
        return True

    def validate(self):
        """Method to validate data prior to accept and close dialog."""

        # IP
        valid = True
        if not ipv4(self.ui.lineEdit_ip.text()):
            self.ui.label_errorMessage.setText("Invalid server IP address provided!")
            valid = False
        # Port
        if port := self.ui.lineEdit_port.text():
            if not self.validate_port(port, "server"):
                valid = False
        else:
            self.ui.label_errorMessage.setText("No server port provided!")
            valid = False
        # Passive ports
        start_passive_port = self.ui.lineEdit_passive_port_range_start.text()
        end_passive_port = self.ui.lineEdit_passive_port_range_end.text()
        if not start_passive_port:
            self.ui.label_errorMessage.setText("Start passive port not provided!")
            valid = False
        elif self.validate_port(start_passive_port, "start passive port") == False:
            valid = False
        if not end_passive_port:
            self.ui.label_errorMessage.setText("End passive port not provided!")
            valid = False
        elif self.validate_port(end_passive_port, "end passive port") == False:
            valid = False
        if not self.validate_passive_port_range(start_passive_port, end_passive_port):
            valid = False
        # SSL key file
        if not os.path.isfile(self.ui.label_key_file_path.text()):
            self.ui.label_errorMessage.setText("Invalid SSL key file provided!")
            valid = False
        # SSL certificate file
        if not os.path.isfile(self.ui.label_certificate_file_path.text()):
            self.ui.label_errorMessage.setText("Invalid SSL certificate file provided!")
            valid = False
        # FTP dir
        if not os.path.isdir(self.ui.label_FTPServer_path.text()):
            self.ui.label_errorMessage.setText("Invalid FTP server directory provided!")
            valid = False
        # Max conn
        max_conn = self.ui.lineEdit_max_conn.text()
        if not max_conn or int(max_conn) < 0:
            self.ui.label_errorMessage.setText("No or Invalid maximum connection value provided!")
            valid = False
        max_conn_per_ip = self.ui.lineEdit_max_conn_ip.text()
        if not max_conn_per_ip or int(max_conn_per_ip) < 0:
            self.ui.label_errorMessage.setText(
                "No or Invalid maximum connection per IP value provided!"
            )
            valid = False
        # Camera IDs, users and passwords
        for i in range(0, self.ui_camera_idx):
            if i in self.removed_rows:
                continue

            if not self.get_camera_id(i):
                self.ui.label_errorMessage.setText("Missing Camera ID!")
                valid = False
            elif self.is_duplicated_id(i):
                self.ui.label_errorMessage.setText(f"Duplicated Camera ID {self.get_camera_id(i)}!")
                valid = False
            if not self.get_camera_pass(i):
                self.ui.label_errorMessage.setText("Missing Camera password!")
                valid = False
            if not self.get_camera_user(i):
                self.ui.label_errorMessage.setText("Missing Camera user!")
                valid = False
            elif self.is_duplicated_username(i):
                self.ui.label_errorMessage.setText(
                    f"Duplicated Camera Username {self.get_camera_user(i)}!"
                )
                valid = False

        if valid:
            self.ui.label_errorMessage.setText("")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)
        self.ui.pushButton_testFTPServer.setEnabled(valid)

    def is_duplicated_id(self, idx):
        """Method to check whether cameras have unique id."""

        cameras_id = set()
        for i in range(0, self.ui_camera_idx):
            cur_id = self.get_camera_id(i)
            if cur_id not in cameras_id:
                cameras_id.add(cur_id)
            elif i == idx:
                return True
        return False

    def is_duplicated_username(self, idx):
        """Method to check whether cameras have duplicated username."""

        cameras_username = set()
        for i in range(0, self.ui_camera_idx):
            cur_username = self.get_camera_user(i)
            if cur_username and cur_username not in cameras_username:
                cameras_username.add(cur_username)
            elif i == idx:
                return True
        return False

    def add_ftp_camera(self):
        """Method to add new FTP camera line edits."""

        grid_layout_cameras = self.findChild(QGridLayout, "gridLayout_cameras")
        if grid_layout_cameras:
            row = self.ui_camera_idx
            # Camera selection check box
            radio_button = QRadioButton()
            radio_button.setObjectName(f"radioButton_camera_{row}")
            radio_button.setChecked(False)
            radio_button.clicked.connect(self.update_remove_ftp_camera_btn)
            grid_layout_cameras.addWidget(radio_button, row, 0)
            # Camera id
            label = QLabel("ID:")
            label.setObjectName(f"label_cameraId_{row}")
            grid_layout_cameras.addWidget(label, row, 1)
            id_line_edit = QLineEdit()
            id_line_edit.setObjectName(f"lineEdit_camera_id_{row}")
            id_line_edit.textChanged.connect(self.validate)
            grid_layout_cameras.addWidget(id_line_edit, row, 2)
            # Camera FTP user
            label = QLabel("user:")
            label.setObjectName(f"label_cameraUser_{row}")
            label.setToolTip("FTP user name")
            grid_layout_cameras.addWidget(label, row, 3)
            user_line_edit = QLineEdit()
            user_line_edit.setObjectName(f"lineEdit_username_{row}")
            user_line_edit.textChanged.connect(self.validate)
            grid_layout_cameras.addWidget(user_line_edit, row, 4)
            # Camera password
            label = QLabel("password:")
            label.setObjectName(f"label_cameraPass_{row}")
            grid_layout_cameras.addWidget(label, row, 5)
            pass_line_edit = QLineEdit()
            pass_line_edit.setObjectName(f"lineEdit_password_{row}")
            pass_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            pass_line_edit.textChanged.connect(self.validate)
            grid_layout_cameras.addWidget(pass_line_edit, row, 6)

            grid_layout_cameras.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.ui_camera_idx += 1

            self.validate()

    def remove_ftp_camera(self):
        """Method to remove FTP camera from list."""

        for i in range(0, self.ui_camera_idx):
            radiobtn = self.findChild(QRadioButton, f"radioButton_camera_{i}")
            if radiobtn:
                camera_id_ln = self.findChild(QLineEdit, f"lineEdit_camera_id_{i}")
                if radiobtn.isChecked() and camera_id_ln:
                    self.removed_cameras.append(camera_id_ln.text())
                    self.removed_rows.add(i)
                    grid_layout_cameras = self.findChild(QGridLayout, "gridLayout_cameras")
                    if grid_layout_cameras:
                        for j in range(0, 7):
                            grid_layout_cameras.itemAtPosition(i, j).widget().setParent(None)
        self.ui.pushButton_removeFTPCamera.setEnabled(False)

    def update_remove_ftp_camera_btn(self):
        """Method to update remove FTP Camera button enablement logic."""

        self.ui.pushButton_removeFTPCamera.setEnabled(True)

    def test_ftp_server(self):
        """Method to test out FTP server configuration options by running a FTP server instance."""

        if not FTPsServer.ftps_server:
            FTPsServer.ftps_server = FTPsServer(
                self.ui.lineEdit_ip.text(),
                int(self.ui.lineEdit_port.text()),
                range(int(self.ui.lineEdit_passive_port_range_start.text()),
                      int(self.ui.lineEdit_passive_port_range_end.text())),
                int(self.ui.lineEdit_max_conn.text()),
                int(self.ui.lineEdit_max_conn_ip.text()),
                self.ui.label_certificate_file_path.text(),
                self.ui.label_key_file_path.text(),
                self.ui.label_FTPServer_path.text(),
            )
        for i in range(0, self.ui_camera_idx):
            FTPsServer.ftps_server.add_user(
                self.get_camera_user(i),
                self.get_camera_pass(i),
                self.ui.label_FTPServer_path.text(),
            )

        self.ui.pushButton_testFTPServer.setEnabled(False)
        self.ui.pushButton_stopFTPServer.setEnabled(True)
        self.ui.buttonBox.setEnabled(False)
        # Start the thread
        self.ftp_thread = FTPsServer.ftps_server.run()

    def _stop_ftp_server(self):
        """Method to stop FTP server thread"""
        if self.ftp_thread and FTPsServer.ftps_server:
            FTPsServer.ftps_server.server.close_all()
            FTPsServer.ftps_server.server.close()
            self.ftp_thread.join()

    def stop_ftp_server(self):
        """Method to stop FTP server thread and to show the appropriate buttons on the UI"""
        self._stop_ftp_server()
        self.ui.pushButton_stopFTPServer.setEnabled(False)
        self.ui.buttonBox.setEnabled(True)
        self.ui.pushButton_testFTPServer.setEnabled(True)

    def _setup_logger(self):
        """Initialize logger for UI logging."""

        logger = logging.getLogger("pyftpdlib")
        log_textbox = QTextEditLogger(self.ui.plainTextEdit_FTPserver_log)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_textbox)

    def closeEvent(self, event):
        self._stop_ftp_server()
