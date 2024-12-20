""""Telegram configuration dialog module."""

import os
import requests
import keyring

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QRadioButton,
    QScrollArea,
    QWidget,
)

from wadas.domain.notifier import Notifier
from wadas.domain.telegram_notifier import TelegramNotifier
from wadas.ui.qt.ui_configure_telegram import Ui_DialogConfigureTelegram

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class HttpWorker(QThread):
    progress_updated = Signal(int)  # Emits the progress percentage
    id_fetched = Signal(str)  # Emits the fetched ID

    def __init__(self, receiver_name):
        super().__init__()
        self.receiver_name = receiver_name

    def run(self):
        try:
            # Simulate an HTTP request to fetch the receiver ID
            # Replace this URL with your actual API endpoint
            response = requests.get(f"http://127.0.0.1:5000/receiver?id=test_receiver")
            response.raise_for_status()
            fetched_id = response.json().get("id", "Unknown")
            self.id_fetched.emit(fetched_id)
        except requests.RequestException as e:
            fetched_id = "Error"
            print(f"Error fetching receiver ID: {e}")
            self.id_fetched.emit(fetched_id)
        finally:
            self.progress_updated.emit(100)

class DialogConfigureTelegram(QDialog, Ui_DialogConfigureTelegram):
    """Class to insert Telegram configuration data to enable WADAS for Telegram notifications."""

    def __init__(self):
        super(DialogConfigureTelegram, self).__init__()
        self.ui = Ui_DialogConfigureTelegram()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.ui.pushButton_test_message.setEnabled(False)
        self.ui.pushButton_remove_receiver.setEnabled(False)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.label_errorMessage.setStyleSheet("color: red")

        self.telegram_notifier = Notifier.notifiers[Notifier.NotifierTypes.TELEGRAM.value]
        self.ui_receiver_idx = 0
        self.removed_cameras = []
        self.removed_rows = set()
        self.worker = None

        # Create scrollable area for ftp camera list in Receivers tab
        scroll_area = QScrollArea(self.ui.tab_receivers)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        cameras_grid_layout = QGridLayout(scroll_widget)
        cameras_grid_layout.setObjectName("gridLayout_receivers")
        self.ui.verticalLayout_receivers.addWidget(scroll_area)

        # Add a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        self.ui.verticalLayout_receivers.addWidget(self.progress_bar)

        # Adding first row of receivers form
        self.add_receiver()

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.pushButton_test_message.clicked.connect(self.send_telegram_message)
        self.ui.pushButton_add_receiver.clicked.connect(self.add_receiver)
        self.ui.pushButton_remove_receiver.clicked.connect(self.remove_receiver)
        self.ui.lineEdit_org_code.textChanged.connect(self.validate)

        self.initialize_form()

    def initialize_form(self):
        """Method to initialize form with existing Telegram configuration data (if any)."""

        if Notifier.notifiers[Notifier.NotifierTypes.WHATSAPP.value]:
            self.ui.checkBox_enable_telegram_notifications.setEnabled(self.telegram_notifier.enabled)
            credentials = keyring.get_credential("WADAS_Telegram", self.telegram_notifier.sender_id)
            if credentials and credentials.username == self.telegram_notifier.sender_id:
                self.ui.lineEdit_org_code.setText(credentials.password)
            #TODO: initialize other fields
            self.ui.checkBox_enable_images.setChecked(self.telegram_notifier.allow_images)
        else:
            self.ui.checkBox_enable_telegram_notifications.setEnabled(True)

    def add_receiver(self):
        """Method to programmatically add receiver input fields with progress bar update."""
        receiver_name = "test_receiver"  # Replace with logic to fetch receiver name dynamically

        # Show the progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        # Create and start the worker
        self.worker = HttpWorker(receiver_name)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.id_fetched.connect(self.on_id_fetched)
        self.worker.start()

    def update_progress(self, value):
        """Update the progress bar value."""
        self.progress_bar.setValue(value)

    def on_id_fetched(self, fetched_id):
        """Handle the fetched ID and populate the row."""
        self.progress_bar.setVisible(False)  # Hide progress bar after completion

        if fetched_id == "Error":
            QMessageBox.critical(self, "Error", "Failed to fetch receiver ID.")
            return

        # Add the receiver row with the fetched ID
        grid_layout_receivers = self.findChild(QGridLayout, "gridLayout_receivers")
        if grid_layout_receivers:
            row = self.ui_receiver_idx
            # Receiver selection check box
            radio_button = QRadioButton()
            radio_button.setObjectName(f"radioButton_receiver_{row}")
            radio_button.setChecked(False)
            radio_button.clicked.connect(self.update_remove_receiver_btn)
            grid_layout_receivers.addWidget(radio_button, row, 0)
            # Receiver id
            label = QLabel("ID:")
            label.setObjectName(f"label_receiverId_{row}")
            grid_layout_receivers.addWidget(label, row, 1)
            id_line_edit = QLineEdit()
            id_line_edit.setObjectName(f"lineEdit_receiver_id_{row}")
            id_line_edit.setText(fetched_id)  # Populate the fetched ID
            id_line_edit.setReadOnly(True)  # Make the ID field read-only
            grid_layout_receivers.addWidget(id_line_edit, row, 2)
            # Receiver name
            label = QLabel("Name:")
            label.setObjectName(f"label_Receiver_name_{row}")
            label.setToolTip("Receiver name")
            grid_layout_receivers.addWidget(label, row, 3)
            user_line_edit = QLineEdit()
            user_line_edit.setObjectName(f"lineEdit_name_{row}")
            user_line_edit.textChanged.connect(self.validate)
            grid_layout_receivers.addWidget(user_line_edit, row, 4)

            grid_layout_receivers.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.ui_receiver_idx += 1

            self.validate()

    def update_remove_receiver_btn(self):
        """Method to update remove FTP Camera button enablement logic."""

        self.ui.pushButton_remove_receiver.setEnabled(True)

    def remove_receiver(self):
        """Method to programmatically remove receiver input fields"""

        for i in range(0, self.ui_receiver_idx):
            radiobtn = self.findChild(QRadioButton, f"radioButton_receiver_{i}")
            if radiobtn:
                camera_id_ln = self.findChild(QLineEdit, f"lineEdit_receiver_id_{i}")
                if radiobtn.isChecked() and camera_id_ln:
                    self.removed_cameras.append(camera_id_ln.text())
                    self.removed_rows.add(i)
                    grid_layout_receivers = self.findChild(QGridLayout, "gridLayout_receivers")
                    if grid_layout_receivers:
                        for j in range(0, 5):
                            grid_layout_receivers.itemAtPosition(i, j).widget().setParent(None)
        self.ui.pushButton_remove_receiver.setEnabled(False)

    def validate(self):
        """Method to validate form data."""

        if self.ui.lineEdit_org_code.text():
            self.ui.label_errorMessage.setText("")
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            self.ui.pushButton_test_message.setEnabled(True)
        else:
            if not self.ui.lineEdit_org_code.text():
                self.ui.label_errorMessage.setText("Organization code cannot be empty.")
            #TODO: add other fields validation checks
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            self.ui.pushButton_test_message.setEnabled(False)

    def add_telegram_credentials(self):
        """Method to add WhatsApp credentials to system keyring."""

        # If credentials exist remove them (workaround keyring bug)
        #TODO: check if keyring is needed or remove this method
        """credentials = keyring.get_credential(
            "WADAS_Telegram", ""
        )
        if credentials:
            try:
                keyring.delete_password("WADAS_Telegram", "")
            except keyring.errors.PasswordDeleteError:
                # Credentials not in the system
                pass

        # Set new/modified credentials for camera
        keyring.set_password(
            "WADAS_Telegram",
            "",
            token,
        )"""

    def accept_and_close(self):
        """When Ok is clicked, save email config info before closing."""

        if not Notifier.notifiers[Notifier.NotifierTypes.TELEGRAM.value]:
            Notifier.notifiers[Notifier.NotifierTypes.TELEGRAM.value] = TelegramNotifier(
                self.ui.lineEdit_org_code.text(), #Isn't this something to store in keyring?
                "", #TODO: fill up with recipients IDs
                self.telegram_notifier.enabled,
                self.telegram_notifier.allow_images
            )
            self.add_telegram_credentials() #TODO: remove if not needed
        else:
            self.telegram_notifier.enabled = self.ui.checkBox_enable_telegram_notifications.isChecked()
            #TODO: add other params initialization
            self.telegram_notifier.allow_images = self.ui.checkBox_enable_images.isChecked()

            Notifier.notifiers[Notifier.NotifierTypes.TELEGRAM.value] = self.telegram_notifier
        self.accept()

    def send_telegram_message(self):
        """Method to send WhatsApp message notification."""

        message = "WADAS Test Message!"
        #TODO: implement test message functionality