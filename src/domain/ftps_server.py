"""FTPS server module"""

import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import TLS_FTPHandler

from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)
ftps_server = None


class FTPsServer(QObject):
    """FTP server class"""

    # Signals
    update_image = Signal(str)
    run_finished = Signal()
    run_progress = Signal(int)

    def __init__(self, ip_address, port, max_conn, max_conn_per_ip,
                 certificate, key, ftp_dir):
        super(FTPsServer, self).__init__()
        # Store params to allow serialization
        self.certificate = certificate
        self.key = key
        self.ip = ip_address
        self.port = port
        self.max_conn = max_conn
        self.max_conn_per_ip = max_conn_per_ip
        self.ftp_dir = ftp_dir

        # SSL handler
        self.handler = TLS_FTPHandler
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
        self.server = FTPServer(address, self.handler)
        self.server.max_cons = max_conn
        self.server.max_cons_per_ip = max_conn_per_ip

    def add_user(self, username, password, directory):
        """Method to add user(s) to the authorizer."""

        self.authorizer.add_user(username, password, directory, perm='elradfmwMT')


    def run(self):
        """Method to run FTPS server"""

        if self.server:
            self.server.serve_forever()

    def serialize(self):
        """Method to serialize FTPS Server object"""

        return dict(
            certificate = self.certificate,
            key = self.key,
            ip = self.ip,
            port = self.port,
            max_conn = self.max_conn,
            max_conn_per_ip = self.max_conn_per_ip
        )

    @staticmethod
    def deserialize(data):
        """Method to deserialize FTPS Server object from file."""
        return FTPsServer(data["certificate"], data["key"], data["ip"], data["port"],
                         data["max_conn"], data["max_conn_per_ip"])