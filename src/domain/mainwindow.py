"""Module containing MainWindows class and methods."""

import logging
import os

import keyring
from PySide6 import QtGui
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QMessageBox

from domain.insert_email import DialogInsertEmail
from domain.insert_url import InsertUrlDialog
from domain.operation_mode import OperationMode
from domain.qtextedit_logger import QTextEditLogger
from domain.select_mode import DialogSelectMode
from domain.test_model_mode import TestModelMode
from domain.animal_detection_mode import AnimalDetectionMode
from domain.select_local_cameras import DialogSelectLocalCameras
from domain.camera import Camera
from ui.ui_mainwindow import Ui_MainWindow

logger = logging.getLogger()

class MainWindow(QMainWindow):
    """Main Window class listing code customization. All code to manipulate
    the mainwindow class shall be defined here.
    ui/mainwindow.py represents auto generated code from Qt Creator, it is
    overwritten every time a new modification is done on Qt Creator side."""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.operation_mode_name = ""
        self.ai_model = None
        self.operation_mode = None
        self.operation_mode_name = ""
        self.ai_model = None
        self.operation_mode = None
        self.key_ring = None
        self.email_config = dict.fromkeys(
            ['smtp_hostname',
             'smtp_port', 
             'recipients_email']
             )
        self.cameras_list = []

        # Connect Actions
        self._connect_actions()

        # Setup UI logger
        self.setup_logger()

        # Initialize startup image
        self.set_image(os.path.join(os.getcwd(), "src", "img","WADAS_logo_big.jpg"))
        # Set mainwindow icon
        self.setWindowIcon(QtGui.QIcon(os.path.join(
            os.getcwd(), "src", "img","mainwindow_icon.jpg")))

        # Update mainwindow UI methods
        self.update_toolbar_status()
        logger.info('Welcome to WADAS!')

    def _connect_actions(self):
        """List all actions to connect to MainWindow"""
        self.ui.actionSelect_Mode.triggered.connect(self.select_mode)
        self.ui.actionRun.triggered.connect(self.run)
        self.ui.actionStop.triggered.connect(self.interrupt_thread)
        self.ui.actionActionConfigureEmail.triggered.connect(self.configure_email)
        self.ui.actionSelectLocalCameras.triggered.connect(self.select_local_cameras)

    def connect_mode_ui_slots(self):
        """Function to connect UI slot with operation_mode signals."""

        # Connect Signal to update image in widget.
        self.operation_mode.update_image.connect(self.set_image)
        self.operation_mode.run_finished.connect(self.on_run_completion)

    def setup_logger(self):
        """Initialize MainWindow logger for UI logging."""

        log_textbox = QTextEditLogger(self.ui.plainTextEdit_log)
        log_textbox.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_textbox)
        logger.propagate = False


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

        dialog = DialogSelectMode()
        if dialog.exec_():
            logger.debug("Selected mode from dialog: %s", dialog.selected_mode)
            if dialog.selected_mode in OperationMode.operation_modes:
                self.operation_mode_name = dialog.selected_mode
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
            if self.operation_mode_name == "test_model_mode":
                self.operation_mode.url = self.url_input_dialog()
                if not self.operation_mode.url:
                    logger.error("Cannot proceed without a valid URL. Please run again.")
                    return
            elif not self.cameras_list:
                logger.error("No camera configured. Please configure input cameras and run again.")
                return
            else:
                # Passing cameras list to the selected operation mode
                self.operation_mode.cameras_list = self.cameras_list

            self.operation_mode.email_configuration = self.email_config

            # Connect slots to update UI from operation mode
            self.connect_mode_ui_slots()

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

        if (not self.operation_mode_name or
            (self.operation_mode_name == "animal_detection_mode" and not self.cameras_list)):
            self.ui.actionRun.setEnabled(False)
        else:
            self.ui.actionRun.setEnabled(True)
        self.ui.actionStop.setEnabled(False)

    def update_toolbar_status_on_run(self, running):
        """Update toolbar status while running model."""

        self.ui.actionStop.setEnabled(running)
        self.ui.actionRun.setEnabled(not running)
        self.ui.actionActionConfigureEmail.setEnabled(not running)
        self.ui.actionSelect_Mode.setEnabled(not running)

    def update_info_widget(self):
        """Update information widget."""

        self.ui.label_op_mode.setText(self.operation_mode_name)
        if self.operation_mode:
            self.ui.label_last_detection.setText(
                os.path.basename(self.operation_mode.last_detection))
            self.ui.label_last_classification.setText(
                 os.path.basename(self.operation_mode.last_classification))
            self.ui.label_classified_animal.setText(
                str(self.operation_mode.last_classified_animals))

    def url_input_dialog(self):
        """Method to run dialog for insertion of an URL to fetch image from."""

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

        if self.operation_mode_name is None:
            logger.error("No operation mode selected.")
            return
        else:
            if self.operation_mode_name == "test_model_mode":
                logger.info("Running test model mode....")
                self.operation_mode = TestModelMode()
            elif self.operation_mode_name == "animal_detection_mode":
                self.operation_mode = AnimalDetectionMode()
            #TODO: add elif with other operation modes

    def configure_email(self):
        """Method to run dialog for insertion of email parameters to enable notifications."""

        #TODO: implement email info persistency
        insert_email_dialog = DialogInsertEmail(self.email_config)
        if insert_email_dialog.exec_():
            self.email_config = insert_email_dialog.email_configuration

            logger.info("Email configuration added.")

            credentials = keyring.get_credential("WADAS_email", "")
            logger.info("Saved credentials for %s", credentials.username)
        else:
            logger.debug("Email configuration aborted.")
            return

    def check_notification_enablement(self):
        """Method to check whether a notification protocol has been set in WADAS."""

        credentials = keyring.get_credential("WADAS_email", "")
        if not self.email_config['smtp_hostname'] or not credentials.username:
            logger.warning("No notification protocol set.")

            message_box = QMessageBox
            message = "No notification protocol set. Do you wish to continue anyway?"
            answer = message_box.question(self,'', message, message_box.Yes | message_box.No)

            if answer == message_box.No:
                return False
            else:
                return True
        else:
            return True

    def select_local_cameras(self):
        """Method to trigger UI dialog for local cameras configuration."""

        select_local_cameras = DialogSelectLocalCameras(self.cameras_list)
        if select_local_cameras.exec_():
            logger.debug("Selecting cameras...")
            self.cameras_list = select_local_cameras.cameras_list
            self.update_toolbar_status()
