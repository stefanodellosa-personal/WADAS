import os

from telegram_server.telegram_client import TelegramClient
from telegram_server.wadas_server import WADASServer
from telegram_server.wadas_server_app import app as wadas_app

BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_CERT = os.getenv("SERVER_CERT")
SERVER_KEY = os.getenv("SERVER_KEY")

tg_client = TelegramClient(BOT_TOKEN)
server = WADASServer("127.0.0.1", 8443, SERVER_CERT, SERVER_KEY, telegram_client=tg_client)

wadas_app.server = server
server.run()

# Telegram needs to be started in the main thread
tg_client.start()
