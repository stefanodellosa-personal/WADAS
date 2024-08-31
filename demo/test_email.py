

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import keyring
import ssl

def main():    
    send_email("", r"C:\Users\stefa\Documents\GitHub\WADAS\detection_output\image_test_model_20240831-174413.jpg")



def send_email(body, img_path):
        """Method to build email and send it."""

        credentials = keyring.get_credential("WADAS_email", "")
        sender = credentials.username
        recipients = "stefano.dellosa@gmail.com, dosrulez87@gmail.com"
        recipients_to_list = recipients.split(", ")

        message = MIMEMultipart()
        # Set email required fields.
        message['Subject'] = "WADAS detection alert"
        message['From'] = sender
        message['To'] = recipients

        # HTML content with an image embedded
        html = """\
        <html>
            <body>
                <p>Hi,<br>
                Here is the image: <img src="cid:image1">.</p>
            </body>
        </html>
        """
        # Attach the HTML part
        message.attach(MIMEText(html, "html"))

        # Open the image file in binary mode
        with open(img_path, 'rb') as img:
            # Attach the image file
            msg_img = MIMEImage(img.read(), name=os.path.basename(img_path))
            # Define the Content-ID header to use in the HTML body
            msg_img.add_header('Content-ID', '<image1>')
            # Attach the image to the message
            message.attach(msg_img)

        # Connect to email's SMTP server using SSL.
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com",
                              465,
                              context=context) as smtp_server:
            # Login to the SMTP server
            smtp_server.login(sender, credentials.password)
            # Send the email to all recipients.
            for recipient in recipients_to_list:
                smtp_server.sendmail(sender, recipient, message.as_string())
                print("Email notification sent to recipient %s .", recipient)
            smtp_server.quit()
        print("Email notification for %s sent!", img_path)

if __name__ == "__main__":
    main()
