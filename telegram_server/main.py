import os
import signal
import sys

from telegram_client import TelegramClient
from wadas_server import WADASServer
from wadas_server_app import app as wadas_app

BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_CERT = os.getenv("SERVER_CERT")
SERVER_KEY = os.getenv("SERVER_KEY")


def handle_shutdown(client, fastapi_server):
    client.application.stop_running()
    fastapi_server.server.should_exit = True
    sys.exit(0)


tg_client = TelegramClient(BOT_TOKEN)
server = WADASServer("0.0.0.0", 8443, SERVER_CERT, SERVER_KEY, telegram_client=tg_client)

wadas_app.server = server

signal.signal(signal.SIGINT, lambda signum, frame: handle_shutdown(tg_client, server))
signal.signal(signal.SIGTERM, lambda signum, frame: handle_shutdown(tg_client, server))

server.run()

# Telegram needs to be started in the main thread
tg_client.start()
