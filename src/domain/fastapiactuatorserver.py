"""FastAPI Actuator server module"""

import logging
import threading
import uvicorn

logger = logging.getLogger(__name__)


class FastAPIActuatorServer:
    def __init__(self, ip_address: str, port: int, certificate: str, key: str):
        self.ip = ip_address
        self.port = port
        self.certificate = certificate
        self.key = key

    def run(self):
        """Method to run the FastAPI Actuator server with SSL in a separate thread."""
        config = uvicorn.Config(
            app="actuatorserver_app:app",
            host=self.ip,
            port=self.port,
            ssl_certfile=self.certificate,
            ssl_keyfile=self.key,
        )
        server = uvicorn.Server(config)

        thread = threading.Thread(target=server.run)
        if thread:
            thread.start()
            logger.info("Starting thread for HTTPS Actuator Server with FastAPI...")
        else:
            logger.error("Unable to create new thread for FastAPI Actuator Server.")
        return thread

    def serialize(self):
        """Method to serialize FastAPI Server object."""
        return {
            "ssl_certificate": self.certificate,
            "ssl_key": self.key,
            "ip": self.ip,
            "port": self.port,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize FastAPI Server object from file."""
        return FastAPIActuatorServer(**data)
