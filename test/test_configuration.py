from unittest.mock import MagicMock, patch

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
from wadas.domain.email_notifier import EmailNotifier
from wadas.domain.fastapi_actuator_server import FastAPIActuatorServer
from wadas.domain.feeder_actuator import FeederActuator
from wadas.domain.ftps_server import DummyAuthorizer, FTPsServer, TLS_FTP_WADAS_Handler
from wadas.domain.notifier import Notifier
from wadas.domain.operation_mode import OperationMode
from wadas.domain.roadsign_actuator import RoadSignActuator


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
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
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
    assert AiModel.classification_treshold == 0
    assert AiModel.detection_treshold == 0
    assert AiModel.language == ""
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type is None


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
  actuator_timeout_threshold: 89
  ip: 1.2.3.4
  port: 567
  ssl_certificate: eshare_crt.pem
  ssl_key: eshare_key.pem
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
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
    assert FastAPIActuatorServer.actuator_server.actuator_timeout_threshold == 89
    assert FastAPIActuatorServer.actuator_server.ip == "1.2.3.4"
    assert FastAPIActuatorServer.actuator_server.port == 567
    assert FastAPIActuatorServer.actuator_server.ssl_certificate == "eshare_crt.pem"
    assert FastAPIActuatorServer.actuator_server.ssl_key == "eshare_key.pem"
    assert FastAPIActuatorServer.actuator_server.thread is None
    assert FastAPIActuatorServer.actuator_server.server is None
    assert FastAPIActuatorServer.actuator_server.startup_time is None
    assert AiModel.classification_treshold == 0
    assert AiModel.detection_treshold == 0
    assert AiModel.language == ""
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type is None


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_actuator_server_config(mock_file, init):
    FastAPIActuatorServer.actuator_server = FastAPIActuatorServer(
        "1.2.3.4", 567, "eshare_crt.pem", "eshare_key.pem", 89
    )
    save_configuration_to_file("")
    assert (
        mock_file.dump()
        == f"""actuator_server:
  actuator_timeout_threshold: 89
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


@patch(
    "builtins.open",
    new_callable=OpenStringMock,
    read_data="""
actuator_server:
actuators:
- enabled: true
  id: Actuator4
  type: Road Sign
- enabled: false
  id: Actuator1
  type: Feeder
- enabled: false
  id: Actuator3
  type: Road Sign
- enabled: true
  id: Actuator2
  type: Feeder
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
def test_load_actuators_config(mock_file, init):
    load_configuration_from_file("")
    assert Notifier.notifiers == {"Email": None}
    assert FTPsServer.ftps_server is None
    actuators = ["Actuator1", "Actuator2", "Actuator3", "Actuator4"]
    assert sorted(Actuator.actuators.keys()) == actuators
    assert [Actuator.actuators[key].id for key in actuators] == actuators
    assert [Actuator.actuators[key].enabled for key in actuators] == [False, True, False, True]
    assert [Actuator.actuators[key].type for key in actuators] == [
        Actuator.ActuatorTypes.FEEDER,
        Actuator.ActuatorTypes.FEEDER,
        Actuator.ActuatorTypes.ROADSIGN,
        Actuator.ActuatorTypes.ROADSIGN,
    ]
    assert cameras == []
    assert Camera.detection_params == []
    assert FastAPIActuatorServer.actuator_server is None
    assert AiModel.classification_treshold == 0.123
    assert AiModel.detection_treshold == 0.456
    assert AiModel.language == "xyz"
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type is None


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_actuators_config(mock_file, init):
    Actuator.actuators["Actuator1"] = FeederActuator("Actuator1", False)
    Actuator.actuators["Actuator2"] = FeederActuator("Actuator2", True)
    Actuator.actuators["Actuator3"] = RoadSignActuator("Actuator3", False)
    Actuator.actuators["Actuator4"] = RoadSignActuator("Actuator4", True)
    save_configuration_to_file("")
    assert (
        mock_file.dump()
        == f"""actuator_server: ''
actuators:
- enabled: false
  id: Actuator1
  type: Feeder
- enabled: true
  id: Actuator2
  type: Feeder
- enabled: false
  id: Actuator3
  type: Road Sign
- enabled: true
  id: Actuator4
  type: Road Sign
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
actuators: []
ai_model:
  ai_class_treshold: 0.98
  ai_detect_treshold: 0.76
  ai_language: it
cameras: []
camera_detection_params: []
ftps_server: []
notification: []
operation_mode:
""",
)
def test_load_ai_model_config(mock_file, init):
    load_configuration_from_file("")
    assert Notifier.notifiers == {"Email": None}
    assert FTPsServer.ftps_server is None
    assert Actuator.actuators == {}
    assert cameras == []
    assert Camera.detection_params == []
    assert FastAPIActuatorServer.actuator_server is None
    assert AiModel.classification_treshold == 0.98
    assert AiModel.detection_treshold == 0.76
    assert AiModel.language == "it"
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type is None


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_ai_model_config(mock_file, init):
    AiModel.classification_treshold = 0.98
    AiModel.detection_treshold = 0.76
    AiModel.language = "it"
    save_configuration_to_file("")
    assert (
        mock_file.dump()
        == f"""actuator_server: ''
actuators: []
ai_model:
  ai_class_treshold: 0.98
  ai_detect_treshold: 0.76
  ai_language: it
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
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
cameras: []
camera_detection_params:
  detection_per_second: 12
  min_contour_area: 345
  ms_sample_rate: 67
  treshold: 89
ftps_server: []
notification: []
operation_mode:
""",
)
def test_load_camera_detection_params_config(mock_file, init):
    load_configuration_from_file("")
    assert Notifier.notifiers == {"Email": None}
    assert FTPsServer.ftps_server is None
    assert Actuator.actuators == {}
    assert cameras == []
    assert Camera.detection_params == {
        "detection_per_second": 12,
        "min_contour_area": 345,
        "ms_sample_rate": 67,
        "treshold": 89,
    }
    assert FastAPIActuatorServer.actuator_server is None
    assert AiModel.classification_treshold == 0
    assert AiModel.detection_treshold == 0
    assert AiModel.language == ""
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type is None


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_camera_detection_params_config(mock_file, init):
    Camera.detection_params = {
        "detection_per_second": 12,
        "min_contour_area": 345,
        "ms_sample_rate": 67,
        "treshold": 89,
    }
    save_configuration_to_file("")
    assert (
        mock_file.dump()
        == f"""actuator_server: ''
actuators: []
ai_model:
  ai_class_treshold: 0.0
  ai_detect_treshold: 0.0
  ai_language: ''
camera_detection_params:
  detection_per_second: 12
  min_contour_area: 345
  ms_sample_rate: 67
  treshold: 89
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
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
cameras: []
camera_detection_params: []
ftps_server:
  ftp_dir: /Documents/ftp
  ip: 1.2.3.4
  max_conn: 50
  max_conn_per_ip: 5
  passive_ports: [1234, 5678]
  port: 567
  ssl_certificate: /Documents/ssl/eshare_crt.pem
  ssl_key: /Documents/ssl/eshare_key.pem
notification: []
operation_mode:
""",
)
def test_load_ftps_server_config(mock_file, init):
    load_configuration_from_file("")
    assert Notifier.notifiers == {"Email": None}
    assert FTPsServer.ftps_server is not None
    assert FTPsServer.ftps_server.ip == "1.2.3.4"
    assert FTPsServer.ftps_server.port == 567
    assert FTPsServer.ftps_server.max_conn == 50
    assert FTPsServer.ftps_server.max_conn_per_ip == 5
    assert FTPsServer.ftps_server.ftp_dir == "/Documents/ftp"
    assert FTPsServer.ftps_server.handler is TLS_FTP_WADAS_Handler
    assert FTPsServer.ftps_server.handler.passive_ports == [1234, 5678]
    assert FTPsServer.ftps_server.handler.certfile == "/Documents/ssl/eshare_crt.pem"
    assert FTPsServer.ftps_server.handler.keyfile == "/Documents/ssl/eshare_key.pem"
    assert FTPsServer.ftps_server.handler.banner == "WADAS FTPS server!"
    assert isinstance(FTPsServer.ftps_server.handler.authorizer, DummyAuthorizer)
    assert Actuator.actuators == {}
    assert cameras == []
    assert Camera.detection_params == []
    assert FastAPIActuatorServer.actuator_server is None
    assert AiModel.classification_treshold == 0
    assert AiModel.detection_treshold == 0
    assert AiModel.language == ""
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type is None


@patch(
    "builtins.open",
    new_callable=OpenStringMock,
    read_data="""
actuator_server:
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
cameras: []
camera_detection_params: []
ftps_server:
  ftp_dir: /Documents/ftp
  ip: 1.2.3.4
  max_conn: 50
  max_conn_per_ip: 5
  passive_ports: [1234, 5678]
  port: 567
  ssl_certificate: /Documents/ssl/eshare_crt.pem
  ssl_key: /Documents/ssl/eshare_key.pem
notification: []
operation_mode:
""",
)
def test_load_ftps_server_config_with_existing_server(mock_file, init):
    class ServerMock:
        pass

    FTPsServer.ftps_server = FTPsServer(
        "5.6.7.8", 321, [4321, 8765], 23, 7, "X/Y.pem", "A/B.pem", "/Z"
    )
    FTPsServer.ftps_server.server = ServerMock()
    FTPsServer.ftps_server.server.close_all = close_all_mock = MagicMock()
    load_configuration_from_file("")
    close_all_mock.assert_called_once_with()
    assert Notifier.notifiers == {"Email": None}
    assert FTPsServer.ftps_server is not None
    assert FTPsServer.ftps_server.ip == "1.2.3.4"
    assert FTPsServer.ftps_server.port == 567
    assert FTPsServer.ftps_server.max_conn == 50
    assert FTPsServer.ftps_server.max_conn_per_ip == 5
    assert FTPsServer.ftps_server.ftp_dir == "/Documents/ftp"
    assert FTPsServer.ftps_server.handler is TLS_FTP_WADAS_Handler
    assert FTPsServer.ftps_server.handler.passive_ports == [1234, 5678]
    assert FTPsServer.ftps_server.handler.certfile == "/Documents/ssl/eshare_crt.pem"
    assert FTPsServer.ftps_server.handler.keyfile == "/Documents/ssl/eshare_key.pem"
    assert FTPsServer.ftps_server.handler.banner == "WADAS FTPS server!"
    assert isinstance(FTPsServer.ftps_server.handler.authorizer, DummyAuthorizer)
    assert Actuator.actuators == {}
    assert cameras == []
    assert Camera.detection_params == []
    assert FastAPIActuatorServer.actuator_server is None
    assert AiModel.classification_treshold == 0
    assert AiModel.detection_treshold == 0
    assert AiModel.language == ""
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type is None


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_ftps_server_config(mock_file, init):
    FTPsServer.ftps_server = FTPsServer(
        "1.2.3.4",
        567,
        [1234, 5678],
        50,
        5,
        "/Documents/ssl/eshare_crt.pem",
        "/Documents/ssl/eshare_key.pem",
        "/Documents/ftp",
    )
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
ftps_server:
  ftp_dir: /Documents/ftp
  ip: 1.2.3.4
  max_conn: 50
  max_conn_per_ip: 5
  passive_ports:
  - 1234
  - 5678
  port: 567
  ssl_certificate: /Documents/ssl/eshare_crt.pem
  ssl_key: /Documents/ssl/eshare_key.pem
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
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
cameras: []
camera_detection_params: []
ftps_server: []
notification:
  Email:
    enabled: false
    recipients_email:
    - foo@wadas.org
    - bar@wadas.org
    sender_email: development@wadas.org
    smtp_hostname: smtp.wadas.org
    smtp_port: 123
operation_mode:
""",
)
def test_load_notification_config(mock_file, init):
    load_configuration_from_file("")
    assert sorted(Notifier.notifiers.keys()) == ["Email"]
    notifier = Notifier.notifiers["Email"]
    assert notifier.enabled is False
    assert notifier.type == Notifier.NotifierTypes.EMAIL
    assert notifier.sender_email == "development@wadas.org"
    assert notifier.smtp_hostname == "smtp.wadas.org"
    assert notifier.smtp_port == 123
    assert notifier.recipients_email == ["foo@wadas.org", "bar@wadas.org"]
    assert Actuator.actuators == {}
    assert FTPsServer.ftps_server is None
    assert Actuator.actuators == {}
    assert cameras == []
    assert Camera.detection_params == []
    assert FastAPIActuatorServer.actuator_server is None
    assert AiModel.classification_treshold == 0
    assert AiModel.detection_treshold == 0
    assert AiModel.language == ""
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type is None


@patch(
    "builtins.open",
    new_callable=OpenStringMock,
    read_data="""
actuator_server:
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
cameras: []
camera_detection_params: []
ftps_server: []
notification:
  Email:
    enabled: true
    recipients_email:
    - foo@wadas.org
    - bar@wadas.org
    sender_email: development@wadas.org
    smtp_hostname: smtp.wadas.org
    smtp_port: 123
operation_mode:
""",
)
def test_load_enabled_notification_config(mock_file, init):
    load_configuration_from_file("")
    assert sorted(Notifier.notifiers.keys()) == ["Email"]
    notifier = Notifier.notifiers["Email"]
    assert notifier.enabled is True


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_notification_config(mock_file, init):
    Notifier.notifiers["Email"] = EmailNotifier(
        "development@wadas.org", "smtp.wadas.org", 123, ["foo@wadas.org", "bar@wadas.org"], False
    )
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
notification:
  Email:
    enabled: false
    recipients_email:
    - foo@wadas.org
    - bar@wadas.org
    sender_email: development@wadas.org
    smtp_hostname: smtp.wadas.org
    smtp_port: 123
operation_mode: ''
version: {__version__}
"""
    )


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_enabled_notification_config(mock_file, init):
    Notifier.notifiers["Email"] = EmailNotifier(
        "development@wadas.org", "smtp.wadas.org", 123, ["foo@wadas.org", "bar@wadas.org"], True
    )
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
notification:
  Email:
    enabled: true
    recipients_email:
    - foo@wadas.org
    - bar@wadas.org
    sender_email: development@wadas.org
    smtp_hostname: smtp.wadas.org
    smtp_port: 123
operation_mode: ''
version: {__version__}
"""
    )


@patch(
    "builtins.open",
    new_callable=OpenStringMock,
    read_data="""
actuator_server:
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
cameras: []
camera_detection_params: []
ftps_server: []
notification: []
operation_mode: Test Model Mode
""",
)
def test_load_test_model_mode_config(mock_file, init):
    load_configuration_from_file("")
    assert Notifier.notifiers == {"Email": None}
    assert FTPsServer.ftps_server is None
    assert Actuator.actuators == {}
    assert cameras == []
    assert Camera.detection_params == []
    assert FastAPIActuatorServer.actuator_server is None
    assert AiModel.classification_treshold == 0
    assert AiModel.detection_treshold == 0
    assert AiModel.language == ""
    assert OperationMode.cur_operation_mode is None
    assert OperationMode.cur_operation_mode_type == OperationMode.OperationModeTypes.TestModelMode


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_test_model_mode_config(mock_file, init):
    OperationMode.cur_operation_mode_type = OperationMode.OperationModeTypes.TestModelMode
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
operation_mode: Test Model Mode
version: {__version__}
"""
    )


@patch(
    "builtins.open",
    new_callable=OpenStringMock,
    read_data="""
actuator_server:
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
cameras: []
camera_detection_params: []
ftps_server: []
notification: []
operation_mode: Animal Detection Mode
""",
)
def test_load_animal_detection_mode_config(mock_file, init):
    load_configuration_from_file("")
    assert OperationMode.cur_operation_mode is None
    assert (
        OperationMode.cur_operation_mode_type
        == OperationMode.OperationModeTypes.AnimalDetectionMode
    )


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_animal_detection_mode_config(mock_file, init):
    OperationMode.cur_operation_mode_type = OperationMode.OperationModeTypes.AnimalDetectionMode
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
operation_mode: Animal Detection Mode
version: {__version__}
"""
    )


@patch(
    "builtins.open",
    new_callable=OpenStringMock,
    read_data="""
actuator_server:
actuators: []
ai_model:
  ai_class_treshold: 0
  ai_detect_treshold: 0
  ai_language: ''
cameras: []
camera_detection_params: []
ftps_server: []
notification: []
operation_mode: Animal Detection and Classification Mode
""",
)
def test_load_animal_detection_and_classification_mode_config(mock_file, init):
    load_configuration_from_file("")
    assert OperationMode.cur_operation_mode is None
    assert (
        OperationMode.cur_operation_mode_type
        == OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode
    )


@patch("builtins.open", new_callable=OpenStringMock, create=True)
def test_save_animal_detection_and_classification_mode_config(mock_file, init):
    OperationMode.cur_operation_mode_type = (
        OperationMode.OperationModeTypes.AnimalDetectionAndClassificationMode
    )
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
operation_mode: Animal Detection and Classification Mode
version: {__version__}
"""
    )
