import json

import pytest
from fastapi.testclient import TestClient

from domain.actuator import Actuator
from domain.actuator_server_app import app

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
