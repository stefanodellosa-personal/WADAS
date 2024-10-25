"""FastAPI Actuator server module"""

import logging
import threading

import uvicorn

logger = logging.getLogger(__name__)


class FastAPIActuatorServer:
    """FastAPI-based HTTPS Server used to communicate with actuators"""

    actuator_server = None

    def __init__(self, ip_address: str, port: int, certificate: str, key: str):
        self.ip = ip_address
        self.port = port
        self.certificate = certificate
        self.key = key
        self.thread = None
        self.server = None

    def run(self):
        """Method to run the FastAPI Actuator server with SSL in a separate thread."""
        config = uvicorn.Config(
            app="actuatorserver_app:app",
            host=self.ip,
            port=self.port,
            ssl_certfile=self.certificate,
            ssl_keyfile=self.key,
        )
        self.server = uvicorn.Server(config)

        self.thread = threading.Thread(target=self.server.run)
        if self.thread:
            self.thread.start()
            logger.info("Starting thread for HTTPS Actuator Server with FastAPI...")
        else:
            logger.error("Unable to create new thread for FastAPI Actuator Server.")
        return self.thread

    def stop(self):
        """Method to safely stop the FastAPIActuatorServer thread"""
        if self.server:
            self.server.should_exit = True

    def serialize(self):
        """Method to serialize FastAPIActuatorServer object."""
        return {
            "ssl_certificate": self.certificate,
            "ssl_key": self.key,
            "ip": self.ip,
            "port": self.port,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize FastAPIActuatorServer from file."""
        return FastAPIActuatorServer(**data)
