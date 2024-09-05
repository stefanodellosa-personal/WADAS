"""Local cameras configuration module."""

from PySide6.QtWidgets import QDialog, QLabel, QCheckBox, QLineEdit, QHBoxLayout, QPushButton, QDialogButtonBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from cv2_enumerate_cameras import enumerate_cameras
import cv2

from domain.camera import Camera
from ui.ui_select_local_cameras import Ui_DialogSelectLocalCameras

class DialogSelectLocalCameras(QDialog, Ui_DialogSelectLocalCameras):
    """Class to select and configure local cameras (i.e., directly plugged to the WADAS node)."""
    def __init__(self, cameras_list):
        super(DialogSelectLocalCameras, self).__init__()
        self.ui = Ui_DialogSelectLocalCameras()
        self.ui.setupUi(self)
        self.cameras_list = cameras_list

        self.list_usb_cameras_in_ui()
        self.initialize_detection_params()

        # Slots
        self.ui.buttonBox.accepted.connect(self.accept_and_close)

    def list_usb_cameras_in_ui(self):
        """Method to initialize cameras list."""

        # Setting titles to columns
        table_titles =["Enabled", "Index", "Name", "PID", "VID", "WADAS ID", "Test"]
        boldFont=QFont()
        boldFont.setBold(True)
        row = col = 0
        for title in table_titles:
            label = QLabel(title)
            label.setFont(boldFont)
            self.ui.gridLayout_localCameras.addWidget(label, row, col)
            col = col+1

        row = 1
        for camera_info in enumerate_cameras(cv2.CAP_MSMF): 
            #TODO: check API preference for linux and implement it OS dependent.
            camera_index = str(camera_info.index)
          
            # Camera selection check box
            check_box = QCheckBox()
            checkbox_obj_name = "checkBox_camera"+camera_index
            check_box.setObjectName(checkbox_obj_name)
            check_box.checkStateChanged.connect(self.validate_cameras_selection)
            self.ui.gridLayout_localCameras.addWidget(check_box, row, 0)
             # Camera index
            label = QLabel(f'{camera_info.index}')
            label.setObjectName("label_cameraIdx"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(label, row, 1)
            # Camera name
            label = QLabel(f'{camera_info.name}')
            label.setObjectName("label_cameraName"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(label, row, 2)
            # Camera PID
            label = QLabel(f'{camera_info.pid}')
            label.setObjectName("label_cameraPid"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(label, row, 3)
            # Camera VID
            label = QLabel(f'{camera_info.vid}')
            label.setObjectName("label_cameraVid"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(label, row, 4)
            # Camera ID
            id_line_edit = QLineEdit()
            lnedit_obj_name = "lineEdit_cameraID"+camera_index
            id_line_edit.setObjectName(lnedit_obj_name)
            id_line_edit.textChanged.connect(self.validate_cameras_selection)
            self.ui.gridLayout_localCameras.addWidget(id_line_edit, row, 5)
            # Test button to preview video (and detection if enabled)
            test_button = QPushButton('Test video')
            test_button.setObjectName("button_camera"+camera_index)
            self.ui.gridLayout_localCameras.addWidget(test_button, row, 6)
            #TODO: connect slot test_button.clicked.connect()

            row = row +1
        self.ui.gridLayout_localCameras.setAlignment(Qt.AlignmentFlag.AlignTop)

    def initialize_usb_cameras(self):
        """Method to initialize attributes from existing camera configuration (if any)."""
        if not self.cameras_list:
            return
 
        # Initialize camera checkboxes (if any was selected before) and IDs
        camera_number = len(enumerate_cameras(cv2.CAP_MSMF))
        for i in range(camera_number):
            checkbox_obj_name = "checkBox_camera"+i
            id_line_edit_name = "label_cameraName"+i
            checkbox = self.ui.gridLayout_localCameras.findChild(QCheckBox, checkbox_obj_name)
            line_edit = self.ui.gridLayout_localCameras.findChild(QLineEdit, id_line_edit_name)
            for camera in self.cameras_list:
                if camera.id == line_edit.text():
                    checkbox.setChecked(camera.is_enabled)
                    camera.id = i

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
            checkbox_obj_name = "checkBox_camera"+camera_index
            id_line_edit_name = "label_cameraName"+camera_index
            checkbox = self.ui.formLayout_caleraList.findChild(QCheckBox, checkbox_obj_name)
            line_edit = self.ui.formLayout_caleraList.findChild(QLineEdit, id_line_edit_name)
            if checkbox and checkbox.isChecked() and not line_edit.text():
                self.ui.label_errorMessage.setText("Please add ID for Camera %s", camera_index)
                valid = False

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

    def accept_and_close(self):
        """When Ok is clicked, save camera config info before closing."""
        #TODO: complete save settings logic
        self.accept()