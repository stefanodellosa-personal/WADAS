"""FastAPI Actuator server module"""

import datetime
import logging
import os
import threading
from logging.handlers import RotatingFileHandler

import uvicorn

logger = logging.getLogger(__name__)


def initialize_fastapi_logger():
    """Method to initialize Fastapi server logger"""
    handler = RotatingFileHandler(
        os.path.join("log", "fastapi_server.log"), maxBytes=100000, backupCount=3
    )
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger_names = ["uvicorn", "uvicorn.error", "uvicorn.access"]
    for logger_name in logger_names:
        server_logger = logging.getLogger(logger_name)
        for handler in server_logger.handlers[:]:
            server_logger.removeHandler(handler)

        server_logger.setLevel(logging.DEBUG)
        server_logger.addHandler(handler)
        server_logger.propagate = False


class FastAPIActuatorServer:
    """FastAPI-based HTTPS Server used to communicate with actuators"""

    actuator_server = None

    def __init__(self, ip: str, port: int, ssl_certificate: str, ssl_key: str):
        self.ip = ip
        self.port = port
        self.ssl_certificate = ssl_certificate
        self.ssl_key = ssl_key
        self.thread = None
        self.server = None
        self.startup_time = None

        config = uvicorn.Config(
            app="wadas.domain.actuator_server_app:app",
            host=self.ip,
            port=self.port,
            ssl_certfile=self.ssl_certificate,
            ssl_keyfile=self.ssl_key,
            timeout_graceful_shutdown=5,
        )
        self.server = uvicorn.Server(config)

    def run(self):
        """Method to run the FastAPI Actuator server with SSL in a separate thread."""
        self.thread = threading.Thread(target=self.server.run)
        if self.thread:
            self.thread.start()
            self.startup_time = datetime.datetime.now()
            logger.info("Starting thread for HTTPS Actuator Server with FastAPI...")
        else:
            logger.error("Unable to create new thread for FastAPI Actuator Server.")
        return self.thread

    def stop(self):
        """Method to safely stop the FastAPIActuatorServer thread"""
        logger.info("Stopping FastAPI Actuator Server...")
        if self.server:
            self.server.should_exit = True
            self.startup_time = None

    def serialize(self):
        """Method to serialize FastAPIActuatorServer object."""
        return {
            "ssl_certificate": self.ssl_certificate,
            "ssl_key": self.ssl_key,
            "ip": self.ip,
            "port": self.port,
        }

    @staticmethod
    def deserialize(data):
        """Method to deserialize FastAPIActuatorServer from file."""
        return FastAPIActuatorServer(**data)
