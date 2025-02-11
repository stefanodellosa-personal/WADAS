import argparse
import base64
import logging
import os
import signal
import socket

from utils import cert_gen, setup_logger

from wadas_webserver.config import CERT_FILEPATH, CERT_FOLDER, KEY_FILEPATH
from wadas_webserver.database import Database
from wadas_webserver.web_server import WebServer
from wadas_webserver.web_server_app import app

flag_run = True
webserver = None

logger = logging.getLogger(__name__)


def handle_shutdown():
    """Method to catch the SIGINT and SIGTERM signals to properly shut down the process"""
    global flag_run, webserver
    logger.info("Killing WADAS web server")
    stop_server()
    flag_run = False


def stop_server():
    """Method to properly handle the FastAPI server shutdown"""
    if webserver:
        webserver.server.should_exit = True


def start_web_server():
    """Method to start the WADAS FastAPI web server on a separate thread
    N.B. HTTPS certificates are built on-the-fly and stored under CERT_FOLDER
    """

    if not os.path.exists(CERT_FOLDER):
        os.makedirs(os.path.join(CERT_FOLDER))
        cert_gen(KEY_FILEPATH, CERT_FILEPATH)
    elif not os.path.exists(CERT_FILEPATH) or not os.path.exists(KEY_FILEPATH):
        cert_gen(KEY_FILEPATH, CERT_FILEPATH)

    app.server = WebServer("0.0.0.0", 443, CERT_FILEPATH, KEY_FILEPATH)
    app.server.run()
    return app.server


def blocking_socket():
    """Method to instantiate a blocking socket on a fixed port
    to wait communication attempts from WADAS main process
    """
    global flag_run
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 65000)
    server_socket.bind(server_address)

    server_socket.listen(1)
    server_socket.settimeout(1)
    logger.info("WADAS Webserver listening on %s:%d", server_address[0], server_address[1])
    while flag_run:
        try:
            connection, client_address = server_socket.accept()
        except socket.timeout:
            continue

        try:
            logger.info("Connection established with %s", client_address)
            data = connection.recv(1024).decode("utf-8")
            match data:
                case "status":
                    logger.info("Received <status> command")
                    # todo check server status
                    response = "ok"
                case "kill":
                    logger.info("Received <kill> command")
                    handle_shutdown()
                    response = "killing"
                case _:
                    logger.info("Received unknown <%s> command", data)
                    response = "unknown"

            connection.sendall(response.encode("utf-8"))

        finally:
            connection.close()


if __name__ == "__main__":
    setup_logger()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--enc_conn_string", type=str, required=True, help="Encoded connection string"
    )

    try:
        args = parser.parse_args()
        encoded_string = args.enc_conn_string
        conn_string = base64.b64decode(encoded_string).decode("utf-8")

        Database.instance = Database(conn_string)
        webserver = start_web_server()
        signal.signal(signal.SIGINT, lambda signum, frame: handle_shutdown())
        signal.signal(signal.SIGTERM, lambda signum, frame: handle_shutdown())
        try:
            blocking_socket()
        except Exception:
            print("Impossible to create a listening socket. Exiting...")
            logger.error("Error create a listening socket")
            webserver.stop()
    except Exception:
        logger.exception("Generic Exception")

    logger.info("WADAS webserver exited")
