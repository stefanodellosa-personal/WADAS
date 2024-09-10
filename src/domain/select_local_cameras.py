"""Local cameras configuration module."""

from PySide6.QtWidgets import QDialog, QLabel, QCheckBox, QLineEdit, QPushButton, QDialogButtonBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from cv2_enumerate_cameras import enumerate_cameras
import cv2
import functools

from domain.camera import Camera
from ui.ui_select_local_cameras import Ui_DialogSelectLocalCameras

class DialogSelectLocalCameras(QDialog, Ui_DialogSelectLocalCameras):
    """Class to select and configure local cameras (i.e., directly plugged to the WADAS node)."""
    def __init__(self, cameras_list):
        super(DialogSelectLocalCameras, self).__init__()
        self.ui = Ui_DialogSelectLocalCameras()
        self.ui.setupUi(self)
        self.cameras_list = cameras_list

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.label_errorMessage.setStyleSheet("color: red")

        self.list_usb_cameras()
        self.initialize_usb_cameras()
        self.initialize_detection_params()

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)

    def list_usb_cameras(self):
        """Method to initialize cameras list."""

        # Setting titles to columns
        table_titles =["Enabled", "Index", "Name", "PID", "VID", "WADAS ID", "Test"]
        bold_font=QFont()
        bold_font.setBold(True)
        row = col = 0
        for title in table_titles:
            label = QLabel(title)
            label.setFont(bold_font)
            self.ui.gridLayout_localCameras.addWidget(label, row, col)
            col = col+1

        row = 1
        for camera_info in enumerate_cameras(cv2.CAP_MSMF):
            #TODO: check API preference for linux and implement it OS dependent.
            camera_index = str(camera_info.index)

            # Camera selection check box
            check_box = QCheckBox()
            checkbox_obj_name = "checkBox_camera_"+camera_index
            check_box.setObjectName(checkbox_obj_name)
            check_box.checkStateChanged.connect(self.validate_cameras_selection)
            self.ui.gridLayout_localCameras.addWidget(check_box, row, 0)
             # Camera index
            label = QLabel(f'{camera_info.index}')
            label.setObjectName("label_cameraIdx_"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(label, row, 1)
            # Camera name
            label = QLabel(f'{camera_info.name}')
            label.setObjectName("label_cameraName_"+camera_index)
            label.setToolTip(str("Path: %s" % camera_info.path))
            self.ui.gridLayout_localCameras.addWidget(label, row, 2)
            # Camera PID
            label = QLabel(f'{camera_info.pid}')
            label.setObjectName("label_cameraPid_"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(label, row, 3)
            # Camera VID
            label = QLabel(f'{camera_info.vid}')
            label.setObjectName("label_cameraVid_"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(label, row, 4)
            # Camera ID
            id_line_edit = QLineEdit()
            lnedit_obj_name = "lineEdit_cameraID_"+camera_index
            id_line_edit.setObjectName(lnedit_obj_name)
            id_line_edit.textChanged.connect(self.validate_cameras_selection)
            self.ui.gridLayout_localCameras.addWidget(id_line_edit, row, 5)
            # Test button to preview video (and detection if enabled)
            test_button = QPushButton('Test video')
            test_button.setObjectName("button_camera_"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(test_button, row, 6)
            #TODO: connect slot test_button.clicked.connect()
            test_button.clicked.connect(functools.partial(self.test_camera_stream, camera_info.index))

            row = row +1
        self.ui.gridLayout_localCameras.setAlignment(Qt.AlignmentFlag.AlignTop)

    def initialize_usb_cameras(self):
        """Method to initialize attributes from existing camera configuration (if any)."""
        if not self.cameras_list:
            return

        # Initialize camera checkboxes (if any was selected before) and IDs
        enum_cameras = enumerate_cameras(cv2.CAP_MSMF)
        camera_number = len(enum_cameras)
        for i in range(camera_number):
            checkbox_obj_name = "checkBox_camera_"+str(i)
            lnedit_camera_id = "lineEdit_cameraID_"+str(i)
            checkbox = self.findChild(QCheckBox, checkbox_obj_name)
            line_edit = self.findChild(QLineEdit, lnedit_camera_id)
            if not checkbox or not line_edit:
                continue

            cur_enum_cam = enum_cameras[i]
            for camera in self.cameras_list:
                if (camera.idx == i and camera.path == cur_enum_cam.path and 
                    camera.pid == cur_enum_cam.pid and camera.vid == cur_enum_cam.vid):
                    checkbox.setChecked(camera.is_enabled)
                    line_edit.setText(camera.id)

    def initialize_detection_params(self):
        """Method to initialize detection parameters in UI."""

        self.ui.lineEdit_treshold.setText(str(Camera.detection_params['treshold']))
        self.ui.lineEdit_minContourArea.setText(str(Camera.detection_params['min_contour_area']))
        self.ui.lineEdit_detectionTreshold.setText(str(
            Camera.detection_params['detection_per_second']))

    def validate_cameras_selection(self):
        """This method validated the selected cameras."""

        valid = True
        for camera_info in enumerate_cameras(cv2.CAP_MSMF):
            camera_index = str(camera_info.index)
            checkbox_obj_name = "checkBox_camera_"+camera_index
            line_edit_camera_id = "lineEdit_cameraID_"+camera_index
            checkbox = self.findChild(QCheckBox, checkbox_obj_name)
            line_edit = self.findChild(QLineEdit, line_edit_camera_id)
            if checkbox and checkbox.isChecked() and not line_edit.text():
                self.ui.label_errorMessage.setText("Please add ID for Camera %s" % camera_index)
                valid = False
            else:
                self.ui.label_errorMessage.setText("")

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

    def accept_and_close(self):
        """When Ok is clicked, save camera config info before closing."""

        # USB Cameras
        enum_cameras = enumerate_cameras(cv2.CAP_MSMF)
        camera_number = len(enum_cameras)
        if self.cameras_list:
            # We need to update values of existing enabled cameras. 
            # The rest we will ignore unless they have an ID assigned.
            for idx in range(camera_number):
                checkbox_obj_name = "checkBox_camera_"+str(idx)
                line_edit_camera_id = "_"+str(idx)
                checkbox = self.findChild(QCheckBox, checkbox_obj_name)
                line_edit = self.findChild(QLineEdit, line_edit_camera_id)
                if (enum_cameras[idx].name == self.cameras_list[idx].name and
                    enum_cameras[idx].pid == self.cameras_list[idx].pid and
                    enum_cameras[idx].vid == self.cameras_list[idx].vid and
                    enum_cameras[idx].path == self.cameras_list[idx].path):

                    # Camera index has not changed, let's save ID and enablement status if changed.
                    self.cameras_list[idx].is_enabled = checkbox.isChecked()
                    self.cameras_list[idx].id = line_edit.text()
                else:
                    # Camera index has changed or camera is new.
                    self.cameras_list[idx].name
                    self.cameras_list[idx].pid
                    self.cameras_list[idx].vid
                    self.cameras_list[idx].path
                    self.cameras_list[idx].is_enabled = checkbox.isChecked()
                    self.cameras_list[idx].id = line_edit.text()
        else:
            # Save enabled cameras
            for idx in range(camera_number):
                checkbox_obj_name = "checkBox_camera_"+str(idx)
                line_edit_camera_id = "lineEdit_cameraID_"+str(idx)
                checkbox = self.findChild(QCheckBox, checkbox_obj_name)
                line_edit = self.findChild(QLineEdit, line_edit_camera_id)
                camera = Camera(line_edit.text(),
                                idx,
                                enum_cameras[idx].backend,
                                enum_cameras[idx].name,
                                checkbox.isChecked(),
                                True, enum_cameras[idx].pid,
                                enum_cameras[idx].vid,
                                enum_cameras[idx].path)
                self.cameras_list.append(camera)
        self.accept()

    def test_camera_stream(self, camera_idx):
        """Method to test camera video stream and motion detection"""

        enum_cameras = enumerate_cameras(cv2.CAP_MSMF)
        camera = Camera("test camera %s" % enum_cameras[camera_idx].name,
                        enum_cameras[camera_idx].index,
                        enum_cameras[camera_idx].backend,
                        enum_cameras[camera_idx].name,
                        True,
                        True,
                        enum_cameras[camera_idx].pid,
                        enum_cameras[camera_idx].vid,
                        enum_cameras[camera_idx].path)
        camera.detect(True)
