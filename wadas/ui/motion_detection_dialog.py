from PySide6.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QLabel)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Slot

from wadas.domain.motion_detection import MotionDetectionThread

class MotionDetectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Motion Detection")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        self.layout = QVBoxLayout(self)

        # Video display label
        self.video_label = QLabel(self)
        self.video_label.setText("Starting video stream...")
        self.video_label.setStyleSheet("background-color: black;")
        self.video_label.setFixedSize(800, 450)
        self.layout.addWidget(self.video_label)

        # Stop button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_motion_detection)
        self.layout.addWidget(self.stop_button)

        # Motion detection thread
        self.motion_thread = MotionDetectionThread()
        self.motion_thread.frame_ready.connect(self.update_frame)
        self.motion_thread.start()

    @Slot(QImage)
    def update_frame(self, q_image):
        self.video_label.setPixmap(QPixmap.fromImage(q_image))

    def stop_motion_detection(self):
        self.motion_thread.stop()
        self.close()