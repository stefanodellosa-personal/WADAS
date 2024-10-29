import os
import tempfile
import time
from ftplib import FTP

import pytest

from domain.ftps_server import FTPsServer


@pytest.fixture
def ftps_server():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir = tempfile.TemporaryDirectory()
    return FTPsServer(
        "0.0.0.0",
        21,
        50,
        5,
        os.path.join(curr_dir, "test_cert/server.pem"),
        os.path.join(curr_dir, "test_cert/keyserver.pem"),
        temp_dir.name,
    )


def test_ftp_server_init(ftps_server):
    assert ftps_server is not None
    assert isinstance(ftps_server, FTPsServer)
    assert ftps_server.ip == "0.0.0.0"
    assert ftps_server.port == 21


def add_user(ftps_server, username, password):
    temp_dir = tempfile.TemporaryDirectory()
    ftps_server.add_user(username, password, temp_dir.name)


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
    resp = ftp_client_connect("127.0.0.1", 21, username, password)
    assert resp == "230 Login successful."
    ftps_server.server.close_all()


def test_hot_add_user(ftps_server):
    username = "camera1"
    password = "pass1"
    thread = ftps_server.run()
    assert thread is not None
    time.sleep(2)
    add_user(ftps_server, username, password)
    resp = ftp_client_connect("127.0.0.1", 21, username, password)
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
    resp = ftp_client_connect("127.0.0.1", 21, username, password)
    assert resp == "230 Login successful."
    ftps_server.server.close_all()
