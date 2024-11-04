"""Email notifier module"""

import logging
import os
import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import keyring
from domain.notifier import Notifier

logger = logging.getLogger(__name__)


class EmailNotifier(Notifier):
    """Email Notifier Class"""

    def __init__(self, sender_email, smtp_hostname, smtp_port, recipients_email, enabled=True):
        super().__init__(enabled)
        self.type = Notifier.NotifierTypes.EMAIL
        self.sender_email = sender_email
        self.smtp_hostname = smtp_hostname
        self.smtp_port = smtp_port
        self.recipients_email = recipients_email

    def send_email(self, img_path):
        """Method to build email and send it."""

        credentials = keyring.get_credential("WADAS_email", self.sender_email)
        if (
            not credentials
            or not self.sender_email
            or not self.smtp_hostname
            or not self.smtp_port
            or not self.recipients_email
        ):
            logger.debug("Email not configured. Skipping email notification.")
            return False

        message = MIMEMultipart()
        # Set email required fields.
        message["Subject"] = "WADAS detection alert"
        message["From"] = self.sender_email
        message["To"] = ", ".join(self.recipients_email)

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
            self.smtp_hostname,
            self.smtp_port,
            context=context,
        ) as smtp_server:
            # Login to the SMTP server
            smtp_server.login(self.sender_email, credentials.password)
            # Send the email to all recipients.
            for recipient in self.recipients_email:
                smtp_server.sendmail(self.sender_email, recipient, message.as_string())
                logger.debug("Email notification sent to recipient %s .", recipient)
            smtp_server.quit()
        logger.info("Email notification for %s sent!", img_path)

        return True

    def serialize(self):
        """Method to serialize email notifier object into file."""
        return {
            "sender_email": self.sender_email,
            "smtp_hostname": self.smtp_hostname,
            "smtp_port": self.smtp_port,
            "recipients_email": self.recipients_email,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize email notifier object from file."""
        return EmailNotifier(**data)