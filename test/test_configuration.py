from unittest.mock import patch

import pytest
from mocks import OpenStringMock

from wadas._version import __version__
from wadas.domain.actuator import Actuator
from wadas.domain.ai_model import AiModel
from wadas.domain.camera import Camera, cameras
from wadas.domain.configuration import (
    load_configuration_from_file,
    save_configuration_to_file,
)
from wadas.domain.fastapi_actuator_server import FastAPIActuatorServer
from wadas.domain.ftps_server import FTPsServer
from wadas.domain.notifier import Notifier
from wadas.domain.operation_mode import OperationMode


@pytest.fixture
def init():
    Notifier.notifiers = {"Email": None}
    FTPsServer.ftps_server = None
    Actuator.actuators.clear()
    cameras.clear()
    Camera.detection_params.clear()
    FastAPIActuatorServer.actuator_server = None
    AiModel.classification_treshold = 0.0
    AiModel.detection_treshold = 0.0
    AiModel.language = ""
    OperationMode.cur_operation_mode = None


@patch(
    "builtins.open",
    new_callable=OpenStringMock,
    read_data="""
actuator_server:
actuators: []
ai_model:
  ai_class_treshold: 0.123
  ai_detect_treshold: 0.456
  ai_language: xyz
cameras: []
camera_detection_params: []
ftps_server: []
notification: []
operation_mode:
""",
)
def test_load_empty_config(mock_file, init):
    load_configuration_from_file("")
    assert Notifier.notifiers == {"Email": None}
    assert FTPsServer.ftps_server is None
    assert Actuator.actuators == {}
    assert cameras == []
    assert Camera.detection_params == []
    assert FastAPIActuatorServer.actuator_server is None
    assert AiModel.classification_treshold == 0.123
    assert AiModel.detection_treshold == 0.456
    assert AiModel.language == "xyz"
    assert OperationMode.cur_operation_mode is None


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_empty_config(mock_file, init):
    save_configuration_to_file("")
    assert (
        mock_file.dump()
        == f"""actuator_server: ''
actuators: []
ai_model:
  ai_class_treshold: 0.0
  ai_detect_treshold: 0.0
  ai_language: ''
camera_detection_params: []
cameras: []
ftps_server: ''
notification: ''
operation_mode: ''
version: {__version__}
"""
    )


@patch(
    "builtins.open",
    new_callable=OpenStringMock,
    read_data="""
actuator_server:
  ip: 1.2.3.4
  port: 567
  ssl_certificate: eshare_crt.pem
  ssl_key: eshare_key.pem
actuators: []
ai_model:
  ai_class_treshold: 0.123
  ai_detect_treshold: 0.456
  ai_language: xyz
cameras: []
camera_detection_params: []
ftps_server: []
notification: []
operation_mode:
""",
)
def test_load_actuator_server_config(mock_file, init):
    load_configuration_from_file("")
    assert Notifier.notifiers == {"Email": None}
    assert FTPsServer.ftps_server is None
    assert Actuator.actuators == {}
    assert cameras == []
    assert Camera.detection_params == []
    assert FastAPIActuatorServer.actuator_server is not None
    assert FastAPIActuatorServer.actuator_server.ip == "1.2.3.4"
    assert FastAPIActuatorServer.actuator_server.port == 567
    assert FastAPIActuatorServer.actuator_server.ssl_certificate == "eshare_crt.pem"
    assert FastAPIActuatorServer.actuator_server.ssl_key == "eshare_key.pem"
    assert FastAPIActuatorServer.actuator_server.thread is None
    assert FastAPIActuatorServer.actuator_server.server is None
    assert FastAPIActuatorServer.actuator_server.startup_time is None
    assert AiModel.classification_treshold == 0.123
    assert AiModel.detection_treshold == 0.456
    assert AiModel.language == "xyz"
    assert OperationMode.cur_operation_mode is None


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_actuator_server_config(mock_file, init):
    FastAPIActuatorServer.actuator_server = FastAPIActuatorServer(
        "1.2.3.4", 567, "eshare_crt.pem", "eshare_key.pem"
    )
    save_configuration_to_file("")
    assert (
        mock_file.dump()
        == f"""actuator_server:
  ip: 1.2.3.4
  port: 567
  ssl_certificate: eshare_crt.pem
  ssl_key: eshare_key.pem
actuators: []
ai_model:
  ai_class_treshold: 0.0
  ai_detect_treshold: 0.0
  ai_language: ''
camera_detection_params: []
cameras: []
ftps_server: ''
notification: ''
operation_mode: ''
version: {__version__}
"""
    )
