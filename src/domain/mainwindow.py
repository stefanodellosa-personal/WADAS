from PySide6 import QtGui
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread
from ui.ui_mainwindow import Ui_MainWindow
from domain.QTextEditLogger import QTextEditLogger
from domain.OperationMode import OperationMode
from domain.selectmode import DialogSelectMode
import logging
import os

"""Main Window class listing code customization. All code to manipulate
the mainwindow class shall be defined here.
ui/mainwindow.py represents auto generated code from Qt Creator, it is
overwritten every time a new modification is done on Qt Creator side."""
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.operation_mode = OperationMode()

        # Connect Actions
        self._connectActions()

        # Connect Slots
        self._connectSlots()
        
        # Setup UI logger
        self.setup_logger()

        logging.info('Welcome to WADAS!')
        
        # Initialize startup image
        self.set_image(os.path.join(os.getcwd(), "src", "img","WADAS_logo_big.jpg"))

    """List all actions to connect to MainWindow"""
    def _connectActions(self):
        self.ui.actionSelect_Mode.triggered.connect(self.select_mode)
        self.ui.actionRun.triggered.connect(self.run)

    def _connectSlots(self):
            # Connect Signal to update image in widget    
            self.operation_mode.update_image.connect(self.set_image)

    def setup_logger(self):
        logger = logging.getLogger()
        logTextBox = QTextEditLogger(self.ui.plainTextEdit_log)
        logTextBox.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logTextBox)
        logger.propagate = False

    """Set image to show in WADAS. This is used for startup, detected and
       classified images."""
    def set_image(self, img):
        if os.path.isfile(img):
            image_widget = self.ui.label_image
            image_widget.setPixmap(QtGui.QPixmap(img))
            image_widget.setMinimumSize(1, 1)
            image_widget.setScaledContents(True)
            image_widget.show
        else:
            logging.error("Provided image path is not valid. %s", img)

    """Slot for mode selection (toolbar button)"""
    def select_mode(self):
        dialog = DialogSelectMode()
        if dialog.exec_():
            logging.debug("Selected mode: %s", dialog.selected_mode)
            if dialog.selected_mode == "test_mode":
                self.operation_mode.set_mode("test_model")
            elif dialog.selected_mode == "tunnel_mode":
                self.operation_mode.set_mode("tunnel_model")
            elif dialog.selected_mode == "bear_detection_mode":
                self.operation_mode.set_mode("bear_detection_mode")
            else:
                # Default, we should never be here.
                logging.error("No valid model selected. Resetting to test_model.")
                self.operation_mode = OperationMode("test_model")
    
    """Slot to run selected mode once run button is clicked.
       Since image processing is heavy task, new thread is created."""
    def run(self):
        self.thread = QThread()
        self.operation_mode.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.operation_mode.run)
        self.operation_mode.run_finished.connect(self.thread.quit)
        #self.operation_mode.progress.connect(self.reportProgress)
        
        # Start the thread
        self.thread.start()