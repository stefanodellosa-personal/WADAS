"""Camera to Actuator associations module"""

import os

from domain.actuators_management_dialog import DialogCameraActuatorManagement
from domain.camera import Camera, cameras
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog
from ui.ui_configure_camera_to_actuator_associations import (
    Ui_DialogCameraActuatorAssociation,
)

module_dir_path = os.path.dirname(os.path.abspath(__file__))


class DialogConfigureCameraToActuatorAssociations(QDialog, Ui_DialogCameraActuatorAssociation):
    """Dialog to configure Camera To Actuator(s) association."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_DialogCameraActuatorAssociation()
        self.original_cameras = cameras

        # UI
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(module_dir_path, "..", "img", "mainwindow_icon.jpg")))

        # Create and populate the model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Enabled cameras:"])
        self.populate_model()

        # Set the model to the QTreeView
        self.ui.treeView.setModel(self.model)

        # Signal
        self.ui.treeView.doubleClicked.connect(self.handle_double_click)
        self.ui.buttonBox.accepted.connect(self.accept_and_close)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.pushButton_expandTreeView.clicked.connect(self.ui.treeView.expandAll)
        self.ui.pushButton_collapseTreeView.clicked.connect(self.ui.treeView.collapseAll)

    def handle_double_click(self, index):
        item = self.model.itemFromIndex(index)
        item_data = item.data()
        if (
            "Camera" in item.text() and item_data.type in Camera.CameraTypes
        ):  # Check if the clicked item is a camera
            # Retrieve the camera object associated with this item
            camera_id = item_data.id
            camera = next((c for c in cameras if c.id == camera_id), None)
            if camera:
                dialog = DialogCameraActuatorManagement(camera, self)
                dialog.exec()
                # Refresh the camera item in the tree view after editing actuators
                self.populate_model()

    def populate_model(self):

        # Clean model before population
        self.model.removeRows(0, self.model.rowCount())

        if not cameras:
            no_items = QStandardItem("No enabled camera. Please edit cameras and retry.")
            self.model.appendRow(no_items)

        # Add cameras and actuators to the model
        for camera in cameras:
            if camera.enabled:
                type = camera.type.value if camera.type else "Unknown"
                camera_item = QStandardItem(f"Camera (ID: {camera.id}, Type: {type})")
                camera_item.setData(camera)
                camera_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                # Add actuators as children to the camera item
                for actuator in camera.actuators:
                    if actuator.enabled:
                        type = actuator.type.value if actuator.type else "Unknown"
                        actuator_item = QStandardItem(f"Actuator (ID: {actuator.id}, Type: {type})")
                        actuator_item.setData(actuator)
                        actuator_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                        # Append the actuator item to the camera item
                        camera_item.appendRow(actuator_item)

                # Append the camera item to the root of the model
                self.model.appendRow(camera_item)

    def accept_and_close(self):
        """When Ok is clicked, save Camera to Actuators associations."""

        self.accept()
