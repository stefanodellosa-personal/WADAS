"""Animal Detection and Classification module."""


import logging

from PySide6.QtCore import QThread

from src.domain.camera import Camera
from src.domain.camera import cameras
from src.domain.camera import img_queue
from src.domain.ftps_server import FTPsServer
from src.domain.operation_mode import OperationMode



logger = logging.getLogger(__name__)

class AnimalDetectionMode(OperationMode):
    """Animal Detection Mode class."""

    def __init__(self):
        super(AnimalDetectionMode, self).__init__()
        self.modename = "animal_detection_mode"
        self.process_queue = True

    def run(self):
        """WADAS animal detection mode"""

        # Initialize ai model
        self.init_model()
        self.check_for_termination_requests()

        logger.info("Instantiating cameras...")
        camera: Camera
        for camera in cameras:
            if camera.enabled:
                if camera.type == Camera.CameraTypes.USBCamera:
                    # Create thread for motion detection
                    logger.info("Instantiating thread for camera %s", camera.id)
                    camera.stop_thread = False
                    self.camera_thread.append(camera.run())
                elif camera.type == Camera.CameraTypes.FTPCamera and FTPsServer.ftps_server and not self.ftp_thread:
                    logger.info("Instantiating FTPS server...")
                    self.init_ftp_server() #TODO: fix thread reentrance
                    #FTPsServer.ftps_server.run_op_mode() TODO: remove once test is complete

        self.run_progress.emit(10)
        self.check_for_termination_requests()
        logger.info("Ready for video stream from Camera(s)...")
        # Run detection model
        while self.process_queue:
            self.check_for_termination_requests()
            if not img_queue.empty():
                logger.debug("Processing image from motion detection notification...")
                cur_img = img_queue.get()
                results, detected_img_path = self.ai_model.process_image(cur_img["img"], True)

                self.last_detection = detected_img_path
                self.check_for_termination_requests()
                if results and detected_img_path:
                    # Trigger image update in WADAS mainwindow
                    self.update_image.emit(detected_img_path)

                    # Send notification
                    message = "WADAS has detected an animal from camera %s!" % id
                    self.send_notification(message, detected_img_path)

        self.execution_completed()

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Mainwindow."""

        if self.thread().isInterruptionRequested():
            logger.info("Request to stop received. Aborting...")
            if self.ftp_camera_exist():
                self.ftp_thread.requestInterruption()
            self.process_queue = False
            for camera in cameras:
                if camera.type == Camera.CameraTypes.USBCamera:
                    camera.stop_thread = True
            self.run_finished.emit()
            return

    def ftp_camera_exist(self):
        for camera in cameras:
            if camera.type == Camera.CameraTypes.FTPCamera:
                return True
        return False

    def init_ftp_server(self):
        """Method to instantiate FTPS server thread"""

        # If no FTP camera is configured skip FTPS Server instantiation
        if not self.ftp_camera_exist():
            return

        logger.debug("Creating new thread for FTP Server..")
        self.ftp_thread = QThread()

        # Move operation mode in dedicated thread
        FTPsServer.ftps_server.moveToThread(self.ftp_thread)

        # Connect thread related signals and slots
        self.ftp_thread.started.connect(FTPsServer.ftps_server.run)
        FTPsServer.ftps_server.run_finished.connect(self.ftp_thread.quit)
        FTPsServer.ftps_server.run_finished.connect(FTPsServer.ftps_server.deleteLater)
        self.ftp_thread.finished.connect(self.ftp_thread.deleteLater)

        logger.debug("Starting FTP Server thread...")
        # Start the thread
        self.ftp_thread.start()
