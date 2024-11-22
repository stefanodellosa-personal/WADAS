import json

import pytest
from fastapi.testclient import TestClient

from wadas.domain.actuator import Actuator
from wadas.domain.actuator_server_app import app
from wadas.domain.fastapi_actuator_server import FastAPIActuatorServer

client = TestClient(app)


@pytest.fixture
def mock_actuators(monkeypatch):
    class MockActuator:
        def get_command(self):
            return json.dumps({"cmd": "test_string"})

    actuators = {"123": MockActuator()}
    monkeypatch.setattr(Actuator, "actuators", actuators)


def test_get_actuator_command_existing(mock_actuators):
    response = client.get("/api/v1/actuators/123")
    print(response)
    assert response.status_code == 200
    assert response.json() == {"cmd": "test_string"}


def test_get_actuator_command_non_existing(mock_actuators):
    response = client.get("/api/v1/actuators/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Actuator does not exist"}


def test_server_serialize():
    server = FastAPIActuatorServer("127.0.0.1", 443, "mycert.pem", "mykey.pem")
    serialized_data = server.serialize()
    expected_data = {
        "ssl_certificate": "mycert.pem",
        "ssl_key": "mykey.pem",
        "ip": "127.0.0.1",
        "port": 443,
        "actuator_timeout_threshold": 30,
    }
    assert serialized_data == expected_data


def test_server_deserialize():
    data = {
        "ssl_certificate": "mycert.pem",
        "ssl_key": "mykey.pem",
        "ip": "127.0.0.1",
        "port": 443,
        "actuator_timeout_threshold": 30,
    }
    server = FastAPIActuatorServer.deserialize(data)
    assert isinstance(server, FastAPIActuatorServer)
    assert server.ip == "127.0.0.1"
    assert server.port == 443
    assert server.ssl_certificate == "mycert.pem"
    assert server.ssl_key == "mykey.pem"
