"""Module containing class to handle WADAS operation modes."""

from domain.ai_model import AiModel
from domain.feedereactuator import FeederActuator
from domain.ftps_server import FTPsServer
from domain.roadsignactuator import RoadSignActuator
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from PySide6.QtCore import QObject, Signal
import keyring
import logging
import os
import smtplib
import ssl

logger = logging.getLogger(__name__)


class OperationMode(QObject):
    """Class to handle WADAS operation modes."""

    class OperationModeTypes(Enum):
        TestModelMode = "Test Model Mode"
        AnimalDetectionMode = "Animal Detection Mode"
        AnimalDetectionAndClassificationMode = (
            "Animal Detection and Classification Mode"
        )
        TunnelMode = "Tunnel Mode"
        BearDetectionMode = "Bear Detection Mode"

    # Signals
    update_image = Signal(str)
    update_info = Signal()
    run_finished = Signal()
    run_progress = Signal(int)

    def __init__(self):
        super(OperationMode, self).__init__()
        self.type = None
        self.ai_model = None
        self.last_detection = ""
        self.last_classification = ""
        self.last_classified_animals = ""
        self.url = ""
        self.email_configuration = {}
        self.camera_thread = []
        self.ftp_thread = None

    def init_model(self):
        """Method to run the selected WADAS operation mode"""

        if self.ai_model is None:
            logger.info("initializing model...")
            self.ai_model = AiModel()
        else:
            logger.debug("Model already initialized, skipping initialization.")

    def send_notification(self, message, img_path):
        """Method to send notification through enabled protocols."""

        # Email notification
        credentials = keyring.get_credential("WADAS_email", "")
        if self.email_configuration["smtp_hostname"] and credentials.username:
            self.send_email(message, img_path)
        else:
            logger.warning("No notification protocol set. Skipping notification.")
        # TODO: add other notification protocols.

    def send_email(self, body, img_path):
        """Method to build email and send it."""

        credentials = keyring.get_credential("WADAS_email", "")
        sender = credentials.username
        recipients = self.email_configuration["recipients_email"]

        message = MIMEMultipart()
        # Set email required fields.
        message["Subject"] = "WADAS detection alert"
        message["From"] = sender
        message["To"] = ", ".join(recipients)

        # HTML content with an image embedded
        html = """\
        <html>
            <body>
                <p>Hi,<br>
                Here is the detection image: <img src="cid:image1">.</p><br>
            </body>
        </html>
        """
        # Attach the HTML part
        message.attach(MIMEText(html, "html"))

        # Open the image file in binary mode
        with open(img_path, "rb") as img:
            # Attach the image file
            msg_img = MIMEImage(img.read(), name=os.path.basename(img_path))
            # Define the Content-ID header to use in the HTML body
            msg_img.add_header("Content-ID", "<image1>")
            # Attach the image to the message
            message.attach(msg_img)

        # Connect to email's SMTP server using SSL.
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            self.email_configuration["smtp_hostname"],
            self.email_configuration["smtp_port"],
            context=context,
        ) as smtp_server:
            # Login to the SMTP server
            smtp_server.login(sender, credentials.password)
            # Send the email to all recipients.
            for recipient in recipients:
                smtp_server.sendmail(sender, recipient, message.as_string())
                logger.debug("Email notification sent to recipient %s .", recipient)
            smtp_server.quit()
        logger.info("Email notification for %s sent!", img_path)

    def actuate(self, actuator_list):
        """Method to trigger actuators when enabled"""
        # TODO @stefano
        for actuator in actuator_list:
            if actuator.enabled:
                if isinstance(actuator, RoadSignActuator):
                    actuator.send_command(RoadSignActuator.Commands.display_on)
                elif isinstance(actuator, FeederActuator):
                    actuator.send_command(FeederActuator.Commands.open)
                else:
                    raise Exception("Unknown actuator type")

    def execution_completed(self):
        """Method to perform end of execution steps."""
        self.run_finished.emit()
        self.stop_ftp_server()
        logger.info("Done with processing.")

    def stop_ftp_server(self):
        """Method to stop FTP server thread"""

        if self.ftp_thread and FTPsServer.ftps_server:
            FTPsServer.ftps_server.server.close_all()
            FTPsServer.ftps_server.server.close()
            self.ftp_thread.join()
