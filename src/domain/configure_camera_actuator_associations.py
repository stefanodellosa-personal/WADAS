"""Camera to Actuator associations module"""

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from domain.actuators_management_dialog import ActuatorManagementDialog
from domain.camera import cameras
from ui.ui_configure_camera_to_actuator_associations import (
    Ui_DialogCameraActuatorAssociation,
)

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class DialogConfigureCameraToActuatorAssociations(QDialog, Ui_DialogCameraActuatorAssociation):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DialogCameraActuatorAssociation()

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        # Create and populate the model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Camera to Actuator associations"])
        self.populate_model()

        # Set the model to the QTreeView
        self.ui.treeView.setModel(self.model)

        # Signal
        self.ui.treeView.doubleClicked.connect(self.handle_double_click)

    def handle_double_click(self, index):
        item = self.model.itemFromIndex(index)
        if "Camera ID" in item.text():  # Check if the clicked item is a camera
            # Retrieve the camera object associated with this item
            camera_id = item.text().split(": ")[1]
            camera = next((c for c in cameras if c.id == camera_id), None)
            if camera:
                dialog = ActuatorManagementDialog(camera, self)
                dialog.exec()
                # Refresh the camera item in the tree view after editing actuators
                self.populate_model()

    def populate_model(self):

        self.model.removeRows(0, self.model.rowCount())
        # Add cameras and actuators to the model
        for camera in cameras:
            if camera.enabled:
                camera_item = QStandardItem(f"Camera ID: {camera.id}")
                type_item = QStandardItem(
                    f"Type: {camera.type.value if camera.type else 'Unknown'}"
                )

                camera_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                type_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                # Append camera settings
                camera_item.appendRow(type_item)

                # Add actuators as children to the camera item
                for actuator in camera.actuators:
                    if actuator.enabled:
                        actuator_item = QStandardItem(f"Actuator ID: {actuator.id}")
                        actuator_type_item = QStandardItem(
                            f"Type: {actuator.type.value if actuator.type else 'Unknown'}"
                        )

                        actuator_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        actuator_type_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                        # Append child items to actuator item
                        actuator_item.appendRow(actuator_type_item)

                        # Append the actuator item to the camera item
                        camera_item.appendRow(actuator_item)

                # Append the camera item to the root of the model
                self.model.appendRow(camera_item)
