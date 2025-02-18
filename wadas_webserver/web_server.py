import datetime
import logging
import threading

import uvicorn

from wadas_webserver.web_server_app import app as server_app

logger = logging.getLogger(__name__)


class WebServer:
    """Class to handle the HTTPS Server"""

    current_server = None

    def __init__(
        self,
        ip: str,
        port: int,
        ssl_certificate: str,
        ssl_key: str,
    ):
        self.ip = ip
        self.port = port
        self.ssl_certificate = ssl_certificate
        self.ssl_key = ssl_key
        self.thread = None
        self.server = None
        self.startup_time = None

        self.config = uvicorn.Config(
            app=server_app,
            host=self.ip,
            port=self.port,
            ssl_certfile=self.ssl_certificate,
            ssl_keyfile=self.ssl_key,
            timeout_graceful_shutdown=5,
        )

    def run(self):
        self.server = uvicorn.Server(self.config)
        self.thread = threading.Thread(target=self.server.run)
        if self.thread:
            self.thread.start()
            self.startup_time = datetime.datetime.now()
        else:
            logger.error("Unable to create new thread for FastAPI Actuator Server.")
        return self.thread

    def stop(self):
        logger.info("Stopping FastAPI Actuator Server...")
        if self.server:
            self.server.should_exit = True
            self.startup_time = None
