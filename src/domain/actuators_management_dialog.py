""""""

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QTreeView,
    QVBoxLayout,
)

from domain.actuator import Actuator


class ActuatorManagementDialog(QDialog):
    def __init__(self, camera, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Manage Actuators for Camera ID: {camera.id}")
        self.camera = camera
        self.original_actuators = list(
            camera.actuators
        )  # Save the original actuators for "Cancel" action

        layout = QVBoxLayout(self)

        # Actuator List View
        self.actuator_model = QStandardItemModel()
        self.actuator_model.setHorizontalHeaderLabels(["Actuators"])

        # Populate actuators for the camera in the model
        self.populate_actuator_model()

        # Tree view for actuators
        self.actuator_tree_view = QTreeView()
        self.actuator_tree_view.setModel(self.actuator_model)
        layout.addWidget(self.actuator_tree_view)

        # Dropdown for selecting possible actuators
        self.actuator_dropdown = QComboBox()
        self.populate_actuator_dropdown()
        layout.addWidget(self.actuator_dropdown)

        # Buttons
        add_button = QPushButton("Add Actuator")
        remove_button = QPushButton("Remove Selected Actuator")
        layout.addWidget(add_button)
        layout.addWidget(remove_button)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)

        # Connect buttons
        add_button.clicked.connect(self.add_actuator)
        remove_button.clicked.connect(self.remove_selected_actuator)
        self.button_box.accepted.connect(self.apply_changes)
        self.button_box.rejected.connect(self.reject)

    def populate_actuator_model(self):
        """Populate the QTreeView model with the actuators associated with this camera."""
        self.actuator_model.removeRows(0, self.actuator_model.rowCount())

        for actuator in self.camera.actuators:
            item = QStandardItem(f"Actuator ID: {actuator.id} - {actuator.type.value}")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Make items non-editable
            self.actuator_model.appendRow(item)

    def populate_actuator_dropdown(self):
        """Populate the dropdown with the list of available actuators."""
        self.actuator_dropdown.clear()
        for actuator_id, actuator in Actuator.actuators.items():
            self.actuator_dropdown.addItem(f"{actuator_id} - {actuator.type.value}", actuator)

    def add_actuator(self):
        """Add the selected actuator to the camera's actuator list."""
        actuator = self.actuator_dropdown.currentData()
        if actuator and actuator not in self.camera.actuators:
            self.camera.actuators.append(actuator)
            self.populate_actuator_model()

    def remove_selected_actuator(self):
        """Remove the selected actuator from the camera's actuator list."""
        selected_indexes = self.actuator_tree_view.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            del self.camera.actuators[row]
            self.populate_actuator_model()

    def apply_changes(self):
        """Apply changes to the camera's actuator list and accept the dialog."""
        # Here, we assume that self.camera.actuators has the updated list
        # The changes are already reflected in the camera object, so just accept the dialog
        # TODO: change logic to avoid changes on original object list rather than pristine it.
        self.accept()

    def reject(self):
        """Discard changes by resetting actuators to the original list."""
        self.camera.actuators = self.original_actuators
        super().reject()
