"""FTPS server module"""

import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.handlers import TLS_FTPHandler
from PySide6.QtCore import QObject, Signal
from src.domain.camera import img_queue

logger = logging.getLogger(__name__)

class TLS_FTP_WADAS_Handler(TLS_FTPHandler):

    def on_connect(self):
        logger.info(f"Connected remote camera from {self.remote_ip}:{self.remote_port}")

    def on_file_received(self, file):
        img_queue.put({"img": file, "img_id": f"ftp_camera_id"}) #TODO: fix camera id

class FTPsServer(QObject):
    """FTP server class"""

    ftps_server = None

    # Signals
    run_finished = Signal()
    run_progress = Signal(int)
    ftp_user_connected = Signal(str)

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

        self.authorizer.add_user(username, password, directory, perm='elradfmwMT')

    def has_user(self, username):
        """Wrapper method of authorizer to check if a user already exists"""
        return self.authorizer.has_user(username)

    def run(self):
        """Method to run FTPS server"""

        self.check_for_termination_requests()
        if self.server:
            self.server.serve_forever()
        self.run_finished.emit()

    def check_for_termination_requests(self):
        """Terminate current thread if interrupt request comes from Dialog."""

        if self.thread().isInterruptionRequested():
            self.run_finished.emit()
            logger.info("Request to stop received. Aborting...")
            return

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
