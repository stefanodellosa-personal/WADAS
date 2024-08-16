"""Module containing MainWindows class and methods."""

import logging
import os
from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread
from ui.ui_mainwindow import Ui_MainWindow
from domain.qtextedit_logger import QTextEditLogger
from domain.operation_mode import OperationMode
from domain.select_mode import DialogSelectMode

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
        self.operation_mode = OperationMode()

        # Connect Actions
        self._connect_actions()
        # Connect Slots
        self._connect_slots()
        # Setup UI logger
        self.setup_logger()

        # Initialize startup image
        self.set_image(os.path.join(os.getcwd(), "src", "img","WADAS_logo_big.jpg"))
        # Set mainwindow icon
        self.setWindowIcon(QtGui.QIcon(os.path.join(os.getcwd(), "src", "img","mainwindow_icon.jpg")))

        # Update mainwindow UI methods
        self.update_toolbar_status()

        logger.info('Welcome to WADAS!')

    def _connect_actions(self):
        """List all actions to connect to MainWindow"""
        self.ui.actionSelect_Mode.triggered.connect(self.select_mode)
        self.ui.actionRun.triggered.connect(self.run)
        self.ui.actionStop.triggered.connect(self.interrupt_thread)

    def _connect_slots(self):
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
            logger.debug("Selected mode: %s", dialog.selected_mode)
            if dialog.selected_mode == "test_mode":
                self.operation_mode.set_mode("test_model")
            elif dialog.selected_mode == "tunnel_mode":
                self.operation_mode.set_mode("tunnel_model")
            elif dialog.selected_mode == "bear_detection_mode":
                self.operation_mode.set_mode("bear_detection_mode")
            else:
                # Default, we should never be here.
                logger.error("No valid model selected. Resetting to test_model.")
                self.operation_mode = OperationMode("test_model")

        self.update_toolbar_status()
        self.update_info_widget()

    def run(self):
        """Slot to run selected mode once run button is clicked.
       Since image processing is heavy task, new thread is created."""

        if self.operation_mode.mode is None:
            logger.error("No operation mode selected.")
        else:
            self.thread = QThread()
            self.operation_mode.moveToThread(self.thread)

            # Connect signals and slots
            self.thread.started.connect(self.operation_mode.run)
            self.operation_mode.run_finished.connect(self.thread.quit)
            #self.operation_mode.progress.connect(self.reportProgress)

            # Start the thread
            self.thread.start()
            # Enable Stop button in toolbar
            self.ui.actionStop.setEnabled(True)
            self.ui.actionRun.setEnabled(False)

    def on_run_completion(self):
        """Actions performed after a run is completed."""
        self.ui.actionStop.setEnabled(False)
        self.ui.actionRun.setEnabled(True)
        self.update_info_widget()

    def interrupt_thread(self):
        """Method to interrupt a running thread."""

        self.thread.requestInterruption()

    def update_toolbar_status(self):
        """Update status of toolbar and related buttons (actions)."""

        if self.operation_mode.mode is None:
            self.ui.actionRun.setEnabled(False)
        else:
            self.ui.actionRun.setEnabled(True)

        self.ui.actionStop.setEnabled(False)

    def update_info_widget(self):
        """Update information widget."""

        self.ui.label_op_mode.setText(self.operation_mode.mode)
        self.ui.label_last_detection.setText(self.operation_mode.last_detection)
        self.ui.label_last_classification.setText(self.operation_mode.last_classification)
        self.ui.label_classified_animal.setText(self.operation_mode.last_classified_animals)