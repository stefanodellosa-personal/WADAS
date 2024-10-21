"""HTTPS Actuator server module"""

import json
import logging
import re
import ssl
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from actuator import Actuator

logger = logging.getLogger(__name__)


class HTTPActuatorRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if re.search("/api/v1/actuators/*", self.path):
            logger.info(
                "Connected remote actuator from %s:%s", self.client_address[0], self.client_address[1]
            )

            record_id = self.path.split("/")[-1]

            if record_id in Actuator.actuators_pool.keys():
                msg = Actuator.actuators_pool[record_id].get_command()
                if msg:
                    self.send_response(HTTPStatus.OK)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(msg.encode('utf-8'))
                else:
                    self.send_response(HTTPStatus.OK)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({'msg': None}).encode('utf-8'))

            else:
                self.send_response(
                    HTTPStatus.NOT_FOUND, "Not Found: record does not exist"
                )
        else:
            self.send_response(HTTPStatus.BAD_REQUEST)

        self.end_headers()


class HTTPSActuatorServer:
    def __init__(self, ip_address, port, certificate, key):
        self.ip = ip_address
        self.port = port
        self.certificate = certificate
        self.key = key

        # HTTP Handler
        self.handler = HTTPActuatorRequestHandler

    def run(self):
        """Method to create new thread and run the HTTPS Actuator server."""
        server = HTTPServer((self.ip, self.port), self.handler)
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslctx.minimum_version = ssl.TLSVersion.TLSv1_3
        sslctx.check_hostname = False  # If set to True, only the hostname that matches the certificate will be accepted
        sslctx.load_cert_chain(certfile=self.certificate, keyfile=self.key)
        server.socket = sslctx.wrap_socket(server.socket, server_side=True)

        thread = threading.Thread(target=server.serve_forever)
        if thread:
            thread.start()
            logger.info("Starting thread for HTTPS Actuator Server...")
        else:
            logger.error("Unable to create new thread for HTTPS Actuator Server.")
        return thread

    def serialize(self):
        """Method to serialize HTTPS Server object"""

        return dict(
            ssl_certificate=self.certificate,
            ssl_key=self.key,
            ip=self.ip,
            port=self.port,
        )

    @staticmethod
    def deserialize(data):
        """Method to deserialize HTTPS Server object from file."""
        return HTTPSActuatorServer(
            data["ip"],
            data["port"],
            data["ssl_certificate"],
            data["ssl_key"]
        )
