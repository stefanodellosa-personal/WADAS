"""FTPS server module"""

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.authorizers import WindowsAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import TLS_FTPHandler

class FTPsServer():
    """FTP server class"""

    def __init__(self, ip_address, port, max_conn, max_conn_per_ip,
                 certificate, key):
        # SSL handler and params
        self.handler = TLS_FTPHandler
        self.handler.certfile = certificate
        self.handler.keyfile = key
        # welcome banner
        self.handler.banner = "WADAS FTPS server!"

        # Authorizer
        self.authorizer = WindowsAuthorizer() #TODO: implement os independent init
        self.handler.authorizer = self.authorizer

        #TODO: check if ThrottledDTPHandler is needed

        # Server
        address = (ip_address, port)
        self.server = FTPServer(address, self.handler)
        self.server.max_cons = max_conn
        self.server.max_cons_per_ip = max_conn_per_ip

    def run(self):
        """Method to run FTPS server"""

        if self.server:
            self.server.serve_forever()