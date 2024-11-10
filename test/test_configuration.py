from unittest.mock import mock_open, patch

from wadas.domain.actuator import Actuator
from wadas.domain.ai_model import AiModel
from wadas.domain.camera import Camera, cameras
from wadas.domain.configuration import (  # save_configuration_to_file,
    load_configuration_from_file,
)
from wadas.domain.fastapi_actuator_server import FastAPIActuatorServer
from wadas.domain.ftps_server import FTPsServer
from wadas.domain.notifier import Notifier
from wadas.domain.operation_mode import OperationMode


@patch(
    "builtins.open",
    new_callable=mock_open,
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
def test_load_empty_config(mock_file):
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


# @patch("builtins.open", new_callable=mock_open, create=True)
# def test_save_empty_config(mock_file):
#     save_configuration_to_file("")
#     mock_file.assert_called_once_with('', 'w')
#     mock = mock_file()
#     assert mock.write.call_args_list == 'OK'
