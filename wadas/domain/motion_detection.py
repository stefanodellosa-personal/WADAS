import time

import cv2
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from wadas.domain.camera import Camera


class MotionDetectionThread(QThread):
    frame_ready = Signal(QImage)

    def __init__(self, camera_index=0, parent=None):
        super().__init__(parent)
        self.running = False
        self.camera_index = camera_index

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(self.camera_index)
        background_sub = cv2.createBackgroundSubtractorMOG2()

        if not cap.isOpened():
            print("Error: Unable to open camera.")
            return

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            # Apply background subtraction
            foreground_mask = background_sub.apply(frame)
            contours, _ = cv2.findContours(
                foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            for cnt in contours:
                if cv2.contourArea(cnt) > Camera.detection_params["min_contour_area"]:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Convert frame to QImage
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

            self.frame_ready.emit(q_image)

            time.sleep(0.03)  # Simulate ~30 FPS

        cap.release()

    def stop(self):
        self.running = False
        self.wait()
