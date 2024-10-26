"""Configure actuators module"""

import logging
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QScrollArea,
    QWidget,
)
from validators import ipv4

from domain.actuator import Actuator
from domain.fastapi_actuator_server import FastAPIActuatorServer
from domain.feeder_actuator import FeederActuator
from domain.qtextedit_logger import QTextEditLogger
from domain.roadsign_actuator import RoadSignActuator
from ui.ui_configure_actuators import Ui_DialogConfigureActuators

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class DialogConfigureActuators(QDialog, Ui_DialogConfigureActuators):
    """Class to instantiate UI dialog to configure actuator server and client(s) parameters."""

    def __init__(self):
        super(DialogConfigureActuators, self).__init__()
        self.ui = Ui_DialogConfigureActuators()
        self.ui_actuator_idx = 0
        self.removed_actuators = []
        self.actuator_server = None
        self.actuator_server_thread = None

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.pushButton_stop_server.setEnabled(False)
        self.ui.pushButton_remove_actuator.setEnabled(False)
        self.ui.label_status.setStyleSheet("color: red")
        self.add_actuator()

        # Create scrollable area for Actuator list in Actuators tab
        scroll_area = QScrollArea(self.ui.tab_clients)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        actuators_grid_layout = QGridLayout(scroll_widget)
        actuators_grid_layout.setObjectName("gridLayout_actuators")
        self.ui.verticalLayout_actuators.addWidget(scroll_area)

        # Adding first row of actuators form
        self.add_actuator()

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.pushButton_add_actuator.clicked.connect(self.add_actuator)
        self.ui.pushButton_remove_actuator.clicked.connect(self.remove_actuator)
        self.ui.pushButton_key_file.clicked.connect(self.select_key_file)
        self.ui.pushButton_cert_file.clicked.connect(self.select_certificate_file)
        self.ui.lineEdit_server_ip.textChanged.connect(self.validate)
        self.ui.lineEdit_server_port.textChanged.connect(self.validate)
        self.ui.pushButton_start_server.clicked.connect(self.start_actuator_server)
        self.ui.pushButton_stop_server.clicked.connect(self.stop_actuator_server)

        # Init dialog
        self.initialize_dialog()
        self._setup_logger()

    def initialize_dialog(self):
        """Method to initialize dialog with existing values (if any)."""

        if FastAPIActuatorServer.actuator_server:
            self.ui.lineEdit_server_ip.setText(str(FastAPIActuatorServer.actuator_server.ip))
            self.ui.lineEdit_server_port.setText(str(FastAPIActuatorServer.actuator_server.port))
            self.ui.label_key_file.setText(FastAPIActuatorServer.actuator_server.ssl_key)
            self.ui.label_cert_file.setText(FastAPIActuatorServer.actuator_server.ssl_certificate)
        self.list_actuators_in_tab()

    def list_actuators_in_tab(self):
        """Method to list cameras in FTPCameras tab."""

        i = 0
        for key in Actuator.actuators:
            if i > 0:
                self.add_actuator()
            actuator_id_ln = self.findChild(QLineEdit, f"lineEdit_actuator_id_{i}")
            actuator_id_ln.setText(Actuator.actuators[key].id)
            actuator_type_cb: QComboBox
            actuator_type_cb = self.findChild(QComboBox, f"comboBox_actuator_type_{i}")
            if Actuator.actuators[key].type == Actuator.ActuatorTypes.ROADSIGN:
                actuator_type_cb.setCurrentText(Actuator.ActuatorTypes.ROADSIGN.value)
            elif Actuator.actuators[key].type == Actuator.ActuatorTypes.FEEDER:
                actuator_type_cb.setCurrentText(Actuator.ActuatorTypes.FEEDER.value)
            actuator_enablement: QCheckBox
            actuator_enablement = self.findChild(QCheckBox, f"checkBox_actuator_enablement_{i}")
            actuator_enablement.setChecked(Actuator.actuators[key].enabled)
            i += 1

    def validate(self):
        """Method to validate dialog input fields"""

        valid = True
        if not ipv4(self.ui.lineEdit_server_ip.text()):
            self.ui.label_status.setText("Invalid server IP address provided!")
            valid = False
        if port := self.ui.lineEdit_server_port.text():
            if int(port) < 1 or int(port) > 65535:
                self.ui.label_status.setText("Invalid server port provided!")
                valid = False
        else:
            self.ui.label_status.setText("No server port provided!")
            valid = False
        if not os.path.isfile(self.ui.label_key_file.text()):
            self.ui.label_status.setText("Invalid SSL key file provided!")
            valid = False
        if not os.path.isfile(self.ui.label_cert_file.text()):
            self.ui.label_status.setText("Invalid SSL certificate file provided!")
            valid = False

        for i in range(0, self.ui_actuator_idx):
            if not self.get_actuator_id(i):
                self.ui.label_status.setText("Missing Actuator ID!")
                valid = False
            elif self.is_duplicated_id(i):
                self.ui.label_status.setText(f"Duplicated Actuator ID {self.get_actuator_id(i)}!")
                valid = False

        if valid:
            self.ui.label_status.setText("")
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)
        self.ui.pushButton_start_server.setEnabled(valid)

    def add_actuator(self):
        """Method to add new actuator line edits."""

        grid_layout_actuators = self.findChild(QGridLayout, "gridLayout_actuators")
        if grid_layout_actuators:
            row = self.ui_actuator_idx
            # Actuator selection check box
            radio_button = QRadioButton()
            radio_button.setObjectName(f"radioButton_actuator_{row}")
            radio_button.setChecked(False)
            radio_button.clicked.connect(self.update_remove_actuator_btn)
            grid_layout_actuators.addWidget(radio_button, row, 0)
            # Actuator id
            label = QLabel("ID:")
            label.setObjectName(f"label_actuator_id_{row}")
            grid_layout_actuators.addWidget(label, row, 1)
            id_line_edit = QLineEdit()
            id_line_edit.setObjectName(f"lineEdit_actuator_id_{row}")
            id_line_edit.textChanged.connect(self.validate)
            grid_layout_actuators.addWidget(id_line_edit, row, 2)
            # Actuator type
            label = QLabel("Type:")
            label.setObjectName(f"label_actuator_type_{row}")
            grid_layout_actuators.addWidget(label, row, 3)
            combo_box = QComboBox(self)
            combo_box.setObjectName(f"comboBox_actuator_type_{row}")
            types = [type.value for type in Actuator.ActuatorTypes]
            combo_box.addItems(types)
            combo_box.currentIndexChanged.connect(self.validate)
            combo_box.setToolTip("Select actuator type")
            grid_layout_actuators.addWidget(combo_box, row, 4)
            # Actuator Enablement
            label = QLabel("Enable:")
            label.setObjectName(f"label_actuator_enable_{row}")
            grid_layout_actuators.addWidget(label, row, 5)
            check_box = QCheckBox()
            check_box.setObjectName(f"checkBox_actuator_enablement_{row}")
            check_box.setChecked(False)
            check_box.checkStateChanged.connect(self.validate)
            grid_layout_actuators.addWidget(check_box, row, 6)
            grid_layout_actuators.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.ui_actuator_idx += 1

            self.validate()

    def remove_actuator(self):
        """Method to remove Actuator from list."""

        for i in range(0, self.ui_actuator_idx):
            radiobtn = self.findChild(QRadioButton, f"radioButton_actuator_{i}")
            if radiobtn:
                actuator_id_ln = self.findChild(QLineEdit, f"lineEdit_actuator_id_{i}")
                if radiobtn.isChecked() and actuator_id_ln:
                    self.removed_actuators.append(actuator_id_ln.text())
                    gridLayout_actuators = self.findChild(QGridLayout, "gridLayout_actuators")
                    if gridLayout_actuators:
                        for j in range(0, 7):
                            gridLayout_actuators.itemAtPosition(i, j).widget().setParent(None)
        self.ui.pushButton_remove_actuator.setEnabled(False)
        self.ui_actuator_idx -= 1
        self.validate()

    def update_remove_actuator_btn(self):
        """Method to remove actuator from the list"""

        self.ui.pushButton_remove_actuator.setEnabled(True)

    def select_key_file(self):
        """Method to select SSL key file"""

        file_name = QFileDialog.getOpenFileName(
            self, "Open SSL key file", os.getcwd(), "Pem File (*.pem)"
        )
        self.ui.label_key_file.setText(str(file_name[0]))
        self.validate()

    def select_certificate_file(self):
        """Method to select SSL certificate file"""

        file_name = QFileDialog.getOpenFileName(
            self, "Open SSL certificate file", os.getcwd(), "Pem File (*.pem)"
        )
        self.ui.label_cert_file.setText(str(file_name[0]))
        self.validate()

    def get_actuator_id(self, row):
        """Method to get actuator id text from UI programmatically by row number"""
        actuator_id_ln: QLineEdit
        actuator_id_ln = self.findChild(QLineEdit, f"lineEdit_actuator_id_{row}")
        return actuator_id_ln.text() if actuator_id_ln else None

    def get_actuator_type(self, row):
        """Method to get actuator type from UI programmatically by row number"""
        actuator_type: QComboBox
        actuator_type = self.findChild(QComboBox, f"comboBox_actuator_type_{row}")
        return actuator_type.currentText()

    def get_actuator_enablement(self, row):
        """Method to get actuator enablement from UI programmatically by row number"""
        actuator_enablement: QCheckBox
        actuator_enablement = self.findChild(QCheckBox, f"checkBox_actuator_enablement_{row}")
        return actuator_enablement.isChecked()

    def is_duplicated_id(self, idx):
        """Method to check whether actuators have unique id."""

        actuators_id = set()
        for i in range(0, self.ui_actuator_idx):
            cur_id = self.get_actuator_id(i)
            if cur_id not in actuators_id:
                actuators_id.add(cur_id)
            elif i == idx:
                return True
        return False

    def accept_and_close(self):
        """When Ok is clicked, save Ai model config info before closing."""

        if FastAPIActuatorServer.actuator_server:
            FastAPIActuatorServer.actuator_server.ip = self.ui.lineEdit_server_ip.text()
            FastAPIActuatorServer.actuator_server.port = int(self.ui.lineEdit_server_port.text())
            FastAPIActuatorServer.actuator_server.ssl_certificate = self.ui.label_cert_file.text()
            FastAPIActuatorServer.actuator_server.ssl_key = self.ui.label_key_file.text()
        else:
            FastAPIActuatorServer.actuator_server = FastAPIActuatorServer(
                self.ui.lineEdit_server_ip.text(),
                int(self.ui.lineEdit_server_port.text()),
                self.ui.label_cert_file.text(),
                self.ui.label_key_file.text(),
            )
        if Actuator.actuators:
            actuators_id = set()
            for i in range(0, self.ui_actuator_idx):
                cur_actuator_id = self.get_actuator_id(i)
                cur_actuator_type = self.get_actuator_type(i)
                cur_actuator_enablement = self.get_actuator_enablement(i)
                if cur_actuator_id and cur_actuator_type:
                    actuators_id.add(cur_actuator_id)
                    if cur_actuator_id in Actuator.actuators:
                        # actuator exists and we update its enablement status
                        Actuator.actuators[cur_actuator_id].enabled = cur_actuator_enablement
                    else:
                        # actuator does not exist, therefore we add it to the dictionary
                        if cur_actuator_type == Actuator.ActuatorTypes.ROADSIGN.value:
                            actuator = RoadSignActuator(cur_actuator_id, cur_actuator_enablement)
                            Actuator.actuators[actuator.id] = actuator
                        elif cur_actuator_type == Actuator.ActuatorTypes.FEEDER.value:
                            actuator = FeederActuator(cur_actuator_id, cur_actuator_enablement)
                            Actuator.actuators[actuator.id] = actuator
            # If an actuator changes the id we have to remove previous orphaned ids from dictionary
            for key in list(Actuator.actuators.keys()):
                if key not in actuators_id:
                    del Actuator.actuators[key]
        else:
            for i in range(0, self.ui_actuator_idx):
                cur_actuator_id = self.get_actuator_id(i)
                cur_actuator_type = self.get_actuator_type(i)
                cur_actuator_enablement = self.get_actuator_enablement(i)
                if cur_actuator_id and cur_actuator_type:
                    if cur_actuator_type == Actuator.ActuatorTypes.ROADSIGN.value:
                        actuator = RoadSignActuator(cur_actuator_id, cur_actuator_enablement)
                        Actuator.actuators[actuator.id] = actuator
                    elif cur_actuator_type == Actuator.ActuatorTypes.FEEDER.value:
                        actuator = FeederActuator(cur_actuator_id, cur_actuator_enablement)
                        Actuator.actuators[actuator.id] = actuator
        self.accept()

    def start_actuator_server(self):
        """Method to start the Actuator server."""
        # TODO @stefano review
        if not self.actuator_server:
            self.actuator_server = FastAPIActuatorServer(
                self.ui.lineEdit_server_ip.text(),
                int(self.ui.lineEdit_server_port.text()),
                self.ui.label_cert_file.text(),
                self.ui.label_key_file.text(),
            )

        self.ui.pushButton_stop_server.setEnabled(True)
        # Start the thread
        self.actuator_server_thread = self.actuator_server.run()

    def stop_actuator_server(self):
        """Method to stop the Actuator server."""

        if self.actuator_server and self.actuator_server_thread:
            self.actuator_server.stop()
            self.actuator_server_thread.join()
            self.ui.pushButton_stop_server.setEnabled(False)

    def _setup_logger(self):
        """Initialize logger for UI logging."""

        # TODO: fix log redirectin to UI dialog only
        logger = logging.getLogger("fastapi")
        log_textbox = QTextEditLogger(self.ui.plainTextEdit_test_server_log)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_textbox)
