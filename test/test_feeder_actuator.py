import pytest

from domain.feeder_actuator import FeederActuator


def test_send_command_valid():
    actuator = FeederActuator(actuator_id="123", enabled=True)
    command = FeederActuator.Commands.OPEN
    actuator.send_command(command)
    # Assuming send_command method has some side effect or state change to verify
    # Here we just check if no exception is raised


def test_send_command_invalid():
    actuator = FeederActuator(actuator_id="123", enabled=True)
    invalid_command = "INVALID_COMMAND"
    with pytest.raises(Exception) as excinfo:
        actuator.send_command(invalid_command)
    assert "Unknown command" in str(excinfo.value)


def test_serialize():
    actuator = FeederActuator(actuator_id="123", enabled=True)
    serialized_data = actuator.serialize()
    expected_data = {
        "type": "FeederActuator",
        "id": "123",
        "enabled": True,
    }
    assert serialized_data == expected_data


def test_deserialize():
    data = {
        "actuator_id": "123",
        "enabled": True,
    }
    actuator = FeederActuator.deserialize(data)
    assert isinstance(actuator, FeederActuator)
    assert actuator.actuator_id == "123"
    assert actuator.enabled is True
