"""FTPS server module"""

import os
import logging
from logging.handlers import RotatingFileHandler
import threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

from src.domain.camera import img_queue

logger = logging.getLogger(__name__)

pyftpdlib_logger = logging.getLogger("pyftpdlib")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(os.path.join(os.getcwd(), 'log', 'ftps_server.log'), maxBytes=100000, backupCount=3)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
pyftpdlib_logger.addHandler(handler)
pyftpdlib_logger.propagate = False

class TLS_FTP_WADAS_Handler(TLS_FTPHandler):

    def on_connect(self):
        logger.info("Connected remote camera from %s:%s", self.remote_ip, self.remote_port)

    def on_disconnect(self):
        logger.info("Disconnected remote camera from %s:%s", self.remote_ip, self.remote_port)

    def on_login(self, username):
        logger.info("%s user logged in.", username)

    def on_logout(self, username):
        logger.info("%s user logged out.", username)

    def on_file_received(self, file):
        logger.info("Received %s file from FTPS Camera.", file)
        img_queue.put({"img": file, "img_id": os.path.basename(os.path.dirname(file))})

    def on_incomplete_file_received(self, file):
        logger.info("Partial file received. Removing %s", file)
        os.remove(file)

class FTPsServer():
    """FTP server class"""

    ftps_server = None

    def __init__(self, ip_address, port, max_conn, max_conn_per_ip,
                 certificate, key, ftp_dir):
        super(FTPsServer, self).__init__()
        # Store params to allow serialization
        self.ip = ip_address
        self.port = port
        self.max_conn = max_conn
        self.max_conn_per_ip = max_conn_per_ip
        self.certificate = certificate
        self.key = key
        self.ftp_dir = ftp_dir

        # SSL handler
        self.handler = TLS_FTP_WADAS_Handler
        self.handler.certfile = self.certificate
        self.handler.keyfile = self.key
        # welcome banner
        self.handler.banner = "WADAS FTPS server!"

        # Authorizer
        self.authorizer = DummyAuthorizer()
        self.handler.authorizer = self.authorizer

        #TODO: check if ThrottledDTPHandler is needed

        # Server
        address = (ip_address, port)
        self.server = ThreadedFTPServer(address, self.handler)
        self.server.max_cons = max_conn
        self.server.max_cons_per_ip = max_conn_per_ip

    def add_user(self, username, password, directory):
        """Method to add user(s) to the authorizer."""
        if not self.has_user(username):
            self.authorizer.add_user(username, password, directory, perm='elmwMT')
        else:
            logger.debug("%s user already exists. Skipping user addition...", username)

    def has_user(self, username):
        """Wrapper method of authorizer to check if a user already exists"""
        return self.authorizer.has_user(username)

    def run(self):
        """ Method to create new thread and run a FTPS server."""

        if self.server:
            thread = threading.Thread(target=self.server.serve_forever)

            if thread:
                thread.start()
                logger.info("Starting thread for FTPs Server...")
            else:
                logger.error("Unable to create new thread for FTPs Server.")

            return thread
        else:
            return None

    def serialize(self):
        """Method to serialize FTPS Server object"""

        return dict(
            ssl_certificate = self.certificate,
            ssl_key = self.key,
            ip = self.ip,
            port = self.port,
            max_conn = self.max_conn,
            max_conn_per_ip = self.max_conn_per_ip,
            ftp_dir = self.ftp_dir
        )

    @staticmethod
    def deserialize(data):
        """Method to deserialize FTPS Server object from file."""
        return FTPsServer(data["ip"], data["port"],  data["max_conn"], data["max_conn_per_ip"],
                          data["ssl_certificate"], data["ssl_key"], data["ftp_dir"])
