"""Module containing MainWindows class and methods."""

import logging
import os
from logging.handlers import RotatingFileHandler

import keyring
import yaml
from PySide6 import QtGui
from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QComboBox,
    QErrorMessage,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
)

from domain.ai_model import AiModel
from domain.animal_detection_mode import AnimalDetectionAndClassificationMode
from domain.camera import Camera, cameras
from domain.configure_ai_model import ConfigureAiModel
from domain.configure_ftp_cameras import DialogFTPCameras
from domain.email_notifier import EmailNotifier
from domain.ftp_camera import FTPCamera
from domain.ftps_server import FTPsServer
from domain.insert_email import DialogInsertEmail
from domain.insert_url import InsertUrlDialog
from domain.notifier import Notifier
from domain.operation_mode import OperationMode
from domain.qtextedit_logger import QTextEditLogger
from domain.select_local_cameras import DialogSelectLocalCameras
from domain.select_mode import DialogSelectMode
from domain.test_model_mode import TestModelMode
from domain.usb_camera import USBCamera
from ui.ui_mainwindow import Ui_MainWindow

logger = logging.getLogger()

level_mapping = {
    0: logging.DEBUG,
    1: logging.INFO,
    2: logging.WARNING,
    3: logging.ERROR,
    4: logging.CRITICAL,
}


class MainWindow(QMainWindow):
    """Main Window class listing code customization. All code to manipulate
    the mainwindow class shall be defined here.
    ui/mainwindow.py represents auto generated code from Qt Creator, it is
    overwritten every time a new modification is done on Qt Creator side."""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.configuration_file_name = ""
        self.selected_operation_mode = None
        self.operation_mode = None
        self.key_ring = None
        self.ftp_server = None

        # Connect Actions
        self._connect_actions()

        # Setup UI logger
        self._setup_logger()

        # Initialize startup image
        self.set_image(os.path.join(os.getcwd(), "img", "WADAS_logo_big.jpg"))
        # Set mainwindow icon
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), "img", "mainwindow_icon.jpg")))

        # Update mainwindow UI methods
        self._init_logging_dropdown()
        self.update_toolbar_status()
        logger.info("Welcome to WADAS!")

        # Create required folders
        os.makedirs("log", exist_ok=True)

    def _connect_actions(self):
        """List all actions to connect to MainWindow"""
        self.ui.actionSelect_Mode.triggered.connect(self.select_mode)
        self.ui.actionRun.triggered.connect(self.run)
        self.ui.actionStop.triggered.connect(self.interrupt_thread)
        self.ui.actionActionConfigureEmail.triggered.connect(self.configure_email)
        self.ui.actionSelectLocalCameras.triggered.connect(self.select_local_cameras)
        self.ui.actionConfigure_Ai_model.triggered.connect(self.configure_ai_model)
        self.ui.actionSave_configuration_as.triggered.connect(self.save_as_to_config_file)
        self.ui.actionSave_configuration_as_menu.triggered.connect(self.save_as_to_config_file)
        self.ui.actionOpen_configuration_file.triggered.connect(self.load_config_from_file)
        self.ui.actionOpen_configuration_file_menu.triggered.connect(self.load_config_from_file)
        self.ui.actionSave_configuration.triggered.connect(self.save_config_to_file)
        self.ui.actionSave_configuration_menu.triggered.connect(self.save_config_to_file)
        self.ui.actionConfigure_FTP_Cameras.triggered.connect(self.configure_ftp_cameras)

    def __connect_mode_ui_slots(self):
        """Function to connect UI slot with operation_mode signals."""

        # Connect Signal to update image in widget.
        self.operation_mode.update_image.connect(self.set_image)
        self.operation_mode.run_finished.connect(self.on_run_completion)
        self.operation_mode.update_image.connect(self.update_info_widget)

    def _setup_logger(self):
        """Initialize MainWindow logger for UI logging."""

        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
        logging_level = logging.DEBUG
        # Line edit logging in mainwindow
        self.log_txtedt_handler = QTextEditLogger(self.ui.plainTextEdit_log)
        self.log_txtedt_handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(self.log_txtedt_handler)

        # WADAS log file
        file_handler = RotatingFileHandler(
            os.path.join(os.getcwd(), "log", "WADAS.log"),
            maxBytes=10 * 1024 * 1024,
            backupCount=3,
        )
        file_handler.setLevel(logging_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def set_image(self, img):
        """Set image to show in WADAS. This is used for startup, detected and
        classified images."""

        if os.path.isfile(img):
            image_widget = self.ui.label_image
            image_widget.setPixmap(QtGui.QPixmap(img))
            image_widget.setMinimumSize(1, 1)
            image_widget.setScaledContents(True)
            image_widget.show()
        else:
            logger.error("Provided image path is not valid. %s", img)

    def select_mode(self):
        """Slot for mode selection (toolbar button)"""

        dialog = DialogSelectMode(self.selected_operation_mode)
        if dialog.exec_():
            logger.debug("Selected mode from dialog: %s", dialog.selected_mode.value)
            if dialog.selected_mode in OperationMode.OperationModeTypes:
                self.selected_operation_mode = dialog.selected_mode
                self.setWindowModified(True)
            else:
                # Default, we should never be here.
                logger.error("No valid model selected. Resetting to test model mode.")

        self.update_toolbar_status()
        self.update_info_widget()

    def run(self):
        """Slot to run selected mode once run button is clicked.
        Since image processing is heavy task, new thread is created."""

        # Check if notifications have been configured
        proceed = self.check_notification_enablement()
        if not proceed:
            return

        self.instantiate_selected_model()
        if self.operation_mode:
            # Satisfy preconditions and required inputs for the selected operation mode
            if self.selected_operation_mode == OperationMode.OperationModeTypes.TestModelMode:
                if not self.check_models():
                    logger.error("Cannot run this mode without AI models. Aborting.")
                    return
                self.operation_mode.url = self.url_input_dialog()
                if not self.operation_mode.url:
                    logger.error("Cannot proceed without a valid URL. Please run again.")
                    return
            elif not cameras:
                logger.error("No camera configured. Please configure input cameras and run again.")
                return
            else:
                # Passing cameras list to the selected operation mode
                self.operation_mode.cameras = cameras

            # Connect slots to update UI from operation mode
            self.__connect_mode_ui_slots()

            # Initialize thread where to run the inference
            self.thread = QThread()

            # Move operation mode in dedicated thread
            self.operation_mode.moveToThread(self.thread)

            # Connect thread related signals and slots
            self.thread.started.connect(self.operation_mode.run)
            self.operation_mode.run_finished.connect(self.thread.quit)
            self.operation_mode.run_finished.connect(self.operation_mode.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            # Start the thread
            self.thread.start()

            # Enable Stop button in toolbar
            self.update_toolbar_status_on_run(True)
        else:
            logger.error("Unable to run the selected model.")

    def on_run_completion(self):
        """Actions performed after a run is completed."""

        self.update_toolbar_status_on_run(False)
        self.update_info_widget()

    def interrupt_thread(self):
        """Method to interrupt a running thread."""

        self.thread.requestInterruption()

    def update_toolbar_status(self):
        """Update status of toolbar and related buttons (actions)."""

        if not self.selected_operation_mode:
            self.ui.actionConfigure_Ai_model.setEnabled(False)
            self.ui.actionRun.setEnabled(False)
        elif (
            self.selected_operation_mode == OperationMode.OperationModeTypes.AnimalDetectionMode
            and not cameras
        ):
            self.ui.actionConfigure_Ai_model.setEnabled(True)
            self.ui.actionRun.setEnabled(False)
        else:
            self.ui.actionConfigure_Ai_model.setEnabled(True)
            self.ui.actionRun.setEnabled(True)
        self.ui.actionStop.setEnabled(False)
        self.ui.actionSave_configuration_as.setEnabled(self.isWindowModified())
        self.ui.actionSave_configuration_as_menu.setEnabled(self.isWindowModified())
        self.ui.actionSave_configuration.setEnabled(
            self.isWindowModified() and bool(self.configuration_file_name)
        )
        self.ui.actionSave_configuration_menu.setEnabled(
            self.isWindowModified() and bool(self.configuration_file_name)
        )

    def update_toolbar_status_on_run(self, running):
        """Update toolbar status while running model."""

        self.ui.actionStop.setEnabled(running)
        self.ui.actionRun.setEnabled(not running)
        self.ui.actionActionConfigureEmail.setEnabled(not running)
        self.ui.actionSelect_Mode.setEnabled(not running)
        self.ui.actionConfigure_Ai_model.setEnabled(not running)
        self.ui.actionSelectLocalCameras.setEnabled(not running)
        self.ui.actionConfigure_FTP_Cameras.setEnabled(not running)
        self.ui.actionOpen_configuration_file.setEnabled(not running)
        self.ui.actionSave_configuration_as.setEnabled(not running)
        self.ui.actionSave_configuration.setEnabled(not running)

    def update_info_widget(self):
        """Update information widget."""

        if self.selected_operation_mode:
            self.ui.label_op_mode.setText(self.selected_operation_mode.value)
        if self.operation_mode:
            self.ui.label_last_detection.setText(
                os.path.basename(self.operation_mode.last_detection)
            )
            self.ui.label_last_classification.setText(
                os.path.basename(self.operation_mode.last_classification)
            )
            self.ui.label_classified_animal.setText(
                str(self.operation_mode.last_classified_animals)
            )

    def url_input_dialog(self):
        """Method to run dialog for insertion of a URL to fetch image from."""

        inserturl_dialog = InsertUrlDialog()
        if inserturl_dialog.exec_():
            logger.debug("Provided URL from dialog: %s", inserturl_dialog.url)
            return inserturl_dialog.url
        else:
            logger.warning("URL insertion aborted.")
            return ""

    def instantiate_selected_model(self):
        """Given the selected model from dedicated UI Dialog, instantiate
        the corresponding object."""

        if not self.selected_operation_mode:
            logger.error("No operation mode selected.")
            return
        else:
            if self.selected_operation_mode == OperationMode.OperationModeTypes.TestModelMode:
                logger.info("Running test model mode....")
                self.operation_mode = TestModelMode()
            elif (
                self.selected_operation_mode == OperationMode.OperationModeTypes.AnimalDetectionMode
            ):
                self.operation_mode = AnimalDetectionAndClassificationMode(classification=False)
            elif (
                self.selected_operation_mode
                == OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode
            ):
                self.operation_mode = AnimalDetectionAndClassificationMode()
            # TODO: add elif with other operation modes

    def configure_email(self):
        """Method to run dialog for insertion of email parameters to enable notifications."""

        insert_email_dialog = DialogInsertEmail()
        if insert_email_dialog.exec_():
            logger.info("Email configuration added.")

            credentials = keyring.get_credential("WADAS_email", "")
            logger.info("Saved credentials for %s", credentials.username)
            self.setWindowModified(True)
            self.update_toolbar_status()
        else:
            logger.debug("Email configuration aborted.")
            return

    def check_notification_enablement(self):
        """Method to check whether a notification protocol has been set in WADAS.
        If not, ask the user whether to proceed without."""

        notification = False
        for notifier in Notifier.notifiers:
            if (
                Notifier.notifiers[notifier]
                and Notifier.notifiers[notifier].type == Notifier.NotifierTypes.Email
            ):
                credentials = keyring.get_credential("WADAS_email", "")
                if notifier and credentials.username:
                    notification = True
        if not notification:
            logger.warning("No notification protocol set.")

            message_box = QMessageBox
            message = "No notification protocol set. Do you wish to continue anyway?"
            answer = message_box.question(self, "", message, message_box.Yes | message_box.No)

            if answer == message_box.No:
                return False
            else:
                return True
        else:
            return True

    def select_local_cameras(self):
        """Method to trigger UI dialog for local cameras configuration."""

        select_local_cameras = DialogSelectLocalCameras()
        if select_local_cameras.exec_():
            logger.info("Camera(s) configured.")
            self.setWindowModified(True)
            self.update_toolbar_status()
            self.update_en_camera_list()

    def configure_ai_model(self):
        """Method to trigger UI dialog to configure Ai model."""

        configure_ai_model = ConfigureAiModel()
        if configure_ai_model.exec():
            logger.info("Ai model configured.")
            logger.debug(
                "Detection treshold: %s. Classification threshold: %s",
                AiModel.detection_treshold,
                AiModel.classification_treshold,
            )
            self.setWindowModified(True)

    def check_models(self):
        """Method to initialize classification model."""
        if not AiModel.check_model():
            logger.error("AI module not found. Downloading...")
            AiModel.download_models()
            return self.check_models()
        logger.info("AI module found!")
        return True

    def save_config_to_file(self):
        """Method to save configuration to file."""

        logger.info("Saving configuration to file...")
        # Serializing cameras per class type
        cameras_to_dict = []
        for camera in cameras:
            if (
                camera.type == Camera.CameraTypes.USBCamera
                or camera.type == Camera.CameraTypes.FTPCamera
            ):
                cameras_to_dict.append(camera.serialize())
        # Serialize configured notification methods
        notification = {}
        for key in Notifier.notifiers:
            notification[key] = Notifier.notifiers[key].serialize()

        data = {
            "notification": notification or "",
            "cameras": cameras_to_dict,
            "camera_detection_params": Camera.detection_params,
            "ai_model": {
                "ai_detect_treshold": AiModel.detection_treshold,
                "ai_class_treshold": AiModel.classification_treshold,
            },
            "operation_mode": self.selected_operation_mode.value
            if self.selected_operation_mode
            else "",
            "ftps_server": (FTPsServer.ftps_server.serialize() if FTPsServer.ftps_server else ""),
        }

        if not self.configuration_file_name:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                "No configuration file provided. Please specify file name and path."
            )
            logger.error("No configuration file provided. Aborting save.")
            return

        with open(self.configuration_file_name, "w") as yamlfile:
            yaml.safe_dump(data, yamlfile)

        logger.info("Configuration saved to file %s.", self.configuration_file_name)
        self.setWindowModified(False)
        self.update_toolbar_status()

    def save_as_to_config_file(self):
        """Method to save configuration file as"""

        file_name = QFileDialog.getSaveFileName(
            self,
            "Select WADAS configuration file to save",
            os.getcwd(),
            "YAML File (*.yaml)",
        )
        if file_name[0]:
            self.configuration_file_name = str(file_name[0])
        else:
            # Empty file name (or dialog Cancel button)
            return

        self.save_config_to_file()

    def load_config_from_file(self):
        """Method to load config from file."""

        file_name = QFileDialog.getOpenFileName(
            self, "Open WADAS configuration file", os.getcwd(), "YAML File (*.yaml)"
        )

        if file_name[0]:
            with (open(str(file_name[0]), "r") as file):

                logging.info("Loading configuration from file...")
                wadas_config = yaml.safe_load(file)

                # Applying configuration to WADAS from config file values
                notification = wadas_config["notification"]
                for key in notification:
                    if key in Notifier.notifiers:
                        if key == Notifier.NotifierTypes.Email.value:
                            Notifier.notifiers[key] = EmailNotifier(**notification[key])
                if FTPsServer.ftps_server:
                    FTPsServer.ftps_server.server.close_all()
                FTPsServer.ftps_server = (
                    FTPsServer.deserialize(wadas_config["ftps_server"])
                    if wadas_config["ftps_server"]
                    else None
                )
                cameras.clear()
                for data in wadas_config["cameras"]:
                    if data["type"] == Camera.CameraTypes.USBCamera.value:
                        usb_camera = USBCamera.deserialize(data)
                        cameras.append(usb_camera)
                    elif data["type"] == Camera.CameraTypes.FTPCamera.value:
                        ftp_camera = FTPCamera.deserialize(data)
                        cameras.append(ftp_camera)
                        if FTPsServer.ftps_server:
                            if not os.path.isdir(ftp_camera.ftp_folder):
                                os.makedirs(ftp_camera.ftp_folder, exist_ok=True)
                            credentials = keyring.get_credential(
                                f"WADAS_FTPcamera_{ftp_camera.id}", ""
                            )
                            if credentials:
                                FTPsServer.ftps_server.add_user(
                                    credentials.username,
                                    credentials.password,
                                    ftp_camera.ftp_folder,
                                )
                Camera.detection_params = wadas_config["camera_detection_params"]
                AiModel.detection_treshold = wadas_config["ai_model"]["ai_detect_treshold"]
                AiModel.classification_treshold = wadas_config["ai_model"]["ai_class_treshold"]
                self.selected_operation_mode = (
                    OperationMode.OperationModeTypes(wadas_config["operation_mode"])
                    if wadas_config["operation_mode"]
                    else None
                )

                logging.info("Configuration loaded from file %s.", file_name[0])
                self.configuration_file_name = file_name[0]
                self.setWindowModified(False)
                self.update_toolbar_status()
                self.update_en_camera_list()

    def configure_ftp_cameras(self):
        """Method to trigger ftp cameras configuration dialog"""

        configure_ftp_cameras_dlg = DialogFTPCameras()
        if configure_ftp_cameras_dlg.exec():
            logger.info("FTP Server and Cameras configured.")
            self.setWindowModified(True)
            self.update_toolbar_status()
            self.update_en_camera_list()

    def update_en_camera_list(self):
        """Method to list enabled camera(s) in UI"""

        self.ui.listWidget_en_cameras.clear()
        for camera in cameras:
            if camera.enabled:
                text = f"({camera.type.value}) {camera.id}"
                self.ui.listWidget_en_cameras.addItem(text)

    def _init_logging_dropdown(self):
        """Method to initialize logging levels in tooldbar dropdown"""

        label = QLabel("Log level: ")
        self.ui.toolBar.addWidget(label)

        comboBox = QComboBox(self)
        comboBox.setObjectName("logLevelComboBox")
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        comboBox.addItems(levels)
        comboBox.setToolTip("Select logging level")
        comboBox.setCurrentText("INFO")
        comboBox.currentIndexChanged.connect(self.change_logging_level)
        self.ui.toolBar.addWidget(comboBox)

    def change_logging_level(self, index):
        """Method to modify UI logging level"""

        new_level = level_mapping.get(index, logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        self.log_txtedt_handler.setLevel(logging.DEBUG)
        logger.log(new_level, "Logging level changed to %s:", logging.getLevelName(new_level))
        self.log_txtedt_handler.setLevel(new_level)
