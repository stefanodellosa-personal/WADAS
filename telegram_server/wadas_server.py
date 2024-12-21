"""FastAPI Actuator server module"""

import datetime
import threading

import uvicorn
from telegram_client import TelegramClient
from wadas_server_app import app as wadas_app


class WADASServer:
    current_server = None

    def __init__(
        self,
        ip: str,
        port: int,
        ssl_certificate: str,
        ssl_key: str,
        telegram_client: TelegramClient = None,
    ):
        self.ip = ip
        self.port = port
        self.ssl_certificate = ssl_certificate
        self.ssl_key = ssl_key
        self.thread = None
        self.server = None
        self.startup_time = None
        self.telegram_client = telegram_client

        self.config = uvicorn.Config(
            app=wadas_app,
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
            print("Unable to create new thread for FastAPI Actuator Server.")
        return self.thread

    def stop(self):
        print("Stopping FastAPI Actuator Server...")
        if self.server:
            self.server.should_exit = True
            self.startup_time = None
