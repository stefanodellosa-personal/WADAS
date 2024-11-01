import os
import tempfile
import time
from ftplib import FTP

import pytest
import util

from domain.ftps_server import FTPsServer


@pytest.fixture
def ftps_server():
    temp_dir = tempfile.gettempdir()
    cert_path = os.path.join(temp_dir, "server.pem")
    key_path = os.path.join(temp_dir, "keyserver.pem")
    util.cert_gen(key_path, cert_path)
    return FTPsServer(
        "127.0.0.1",
        8888,
        50,
        5,
        cert_path,
        key_path,
        temp_dir,
    )


def test_ftp_server_init(ftps_server):
    assert ftps_server is not None
    assert isinstance(ftps_server, FTPsServer)
    assert ftps_server.ip == "127.0.0.1"
    assert ftps_server.port == 8888


def add_user(ftps_server, username, password):
    user_folder = os.path.join(ftps_server.ftp_dir, username)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    ftps_server.add_user(username, password, user_folder)


def test_add_user(ftps_server):
    add_user(ftps_server, "camera1", "pass1")
    assert ftps_server.has_user("camera1")


def ftp_client_connect(host, port, username, password):
    ftp = FTP()
    ftp.connect(host, port)
    resp = ftp.login(username, password)
    ftp.close()
    return resp


def test_server_working(ftps_server):
    username = "camera1"
    password = "pass1"
    add_user(ftps_server, username, password)
    thread = ftps_server.run()
    assert thread is not None
    time.sleep(2)
    resp = ftp_client_connect("127.0.0.1", 8888, username, password)
    assert resp == "230 Login successful."
    ftps_server.server.close_all()


def test_hot_add_user(ftps_server):
    username = "camera1"
    password = "pass1"
    thread = ftps_server.run()
    assert thread is not None
    time.sleep(2)
    add_user(ftps_server, username, password)
    resp = ftp_client_connect("127.0.0.1", 8888, username, password)
    assert resp == "230 Login successful."
    ftps_server.server.close_all()


def test_server_restart(ftps_server):
    username = "camera1"
    password = "pass1"
    add_user(ftps_server, username, password)
    thread = ftps_server.run()
    assert thread is not None
    time.sleep(2)
    ftps_server.server.close_all()
    time.sleep(1)
    thread = ftps_server.run()
    assert thread is not None
    time.sleep(2)
    resp = ftp_client_connect("127.0.0.1", 8888, username, password)
    assert resp == "230 Login successful."
    ftps_server.server.close_all()
