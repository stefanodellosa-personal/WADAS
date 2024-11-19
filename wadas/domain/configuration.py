"""WADAS configuration module."""

import logging
import os

import keyring
import yaml

from wadas._version import __version__
from wadas.domain.actuator import Actuator
from wadas.domain.ai_model import AiModel
from wadas.domain.camera import Camera, cameras
from wadas.domain.email_notifier import EmailNotifier
from wadas.domain.fastapi_actuator_server import FastAPIActuatorServer
from wadas.domain.feeder_actuator import FeederActuator
from wadas.domain.ftp_camera import FTPCamera
from wadas.domain.ftps_server import FTPsServer
from wadas.domain.notifier import Notifier
from wadas.domain.operation_mode import OperationMode
from wadas.domain.roadsign_actuator import RoadSignActuator
from wadas.domain.usb_camera import USBCamera

logger = logging.getLogger(__name__)

_OPERATION_MODE_TYPE_VALUE_TO_TYPE = {mode.value: mode for mode in OperationMode.OperationModeTypes}


def load_configuration_from_file(file_path):
    """Load configuration from YAML file."""

    with open(str(file_path)) as file_:
        logging.info("Loading configuration from file...")

        wadas_config = yaml.safe_load(file_)
        # Applying configuration to WADAS from config file values

        # Notifiers
        Notifier.notifiers.update(
            (key, EmailNotifier(**value))
            for key, value in (wadas_config["notification"] or {}).items()
            if key in Notifier.notifiers and key == Notifier.NotifierTypes.EMAIL.value
        )

        # FTP Server
        if FTPsServer.ftps_server and FTPsServer.ftps_server.server:
            FTPsServer.ftps_server.server.close_all()
        FTPsServer.ftps_server = (
            FTPsServer.deserialize(wadas_config["ftps_server"])
            if wadas_config["ftps_server"]
            else None
        )

        # Actuators
        Actuator.actuators.clear()
        for data in wadas_config["actuators"]:
            match data["type"]:
                case Actuator.ActuatorTypes.ROADSIGN.value:
                    actuator = RoadSignActuator.deserialize(data)
                    Actuator.actuators[actuator.id] = actuator
                case Actuator.ActuatorTypes.FEEDER.value:
                    actuator = FeederActuator.deserialize(data)
                    Actuator.actuators[actuator.id] = actuator

        # Camera(s)
        cameras.clear()
        for data in wadas_config["cameras"]:
            match data["type"]:
                case Camera.CameraTypes.USB_CAMERA.value:
                    usb_camera = USBCamera.deserialize(data)
                    cameras.append(usb_camera)
                case Camera.CameraTypes.FTP_CAMERA.value:
                    ftp_camera = FTPCamera.deserialize(data)
                    cameras.append(ftp_camera)
                    if FTPsServer.ftps_server:
                        if not os.path.isdir(ftp_camera.ftp_folder):
                            os.makedirs(ftp_camera.ftp_folder, exist_ok=True)
                        credentials = keyring.get_credential(
                            f"WADAS_FTP_camera_{ftp_camera.id}", ""
                        )
                        if credentials:
                            FTPsServer.ftps_server.add_user(
                                credentials.username,
                                credentials.password,
                                ftp_camera.ftp_folder,
                            )
        Camera.detection_params = wadas_config["camera_detection_params"]

        # FastAPI Actuator Server
        FastAPIActuatorServer.actuator_server = (
            FastAPIActuatorServer.deserialize(wadas_config["actuator_server"])
            if wadas_config["actuator_server"]
            else None
        )

        # Ai model
        AiModel.detection_treshold = wadas_config["ai_model"]["ai_detect_treshold"]
        AiModel.classification_treshold = wadas_config["ai_model"]["ai_class_treshold"]
        AiModel.language = wadas_config["ai_model"]["ai_language"]

        # Operation Mode
        if operation_mode_type := _OPERATION_MODE_TYPE_VALUE_TO_TYPE.get(
            wadas_config["operation_mode"]
        ):
            OperationMode.cur_operation_mode_type = operation_mode_type
        else:
            OperationMode.cur_operation_mode = None

        logger.info("Configuration loaded from file %s.", file_path)


def save_configuration_to_file(file_):
    """Save configuration to YAML file."""

    logger.info("Saving configuration to file...")

    # Prepare serialization for cameras per class type
    cameras_to_dict = [
        camera.serialize()
        for camera in cameras
        if camera.type in (Camera.CameraTypes.FTP_CAMERA, Camera.CameraTypes.USB_CAMERA)
    ]

    # Prepare serialization for notifiers per class type
    notification = {
        key: value.serialize() for key, value in Notifier.notifiers.items() if key and value
    }

    # Prepare serialization for actuators per class type
    actuators = [value.serialize() for key, value in Actuator.actuators.items() if key and value]

    # Build data structure to serialize
    data = {
        "version": __version__,
        "notification": notification or "",
        "cameras": cameras_to_dict,
        "camera_detection_params": Camera.detection_params,
        "actuators": actuators,
        "ai_model": {
            "ai_detect_treshold": AiModel.detection_treshold,
            "ai_class_treshold": AiModel.classification_treshold,
            "ai_language": AiModel.language,
        },
        "operation_mode": (
            OperationMode.cur_operation_mode_type.value
            if OperationMode.cur_operation_mode_type
            else ""
        ),
        "ftps_server": FTPsServer.ftps_server.serialize() if FTPsServer.ftps_server else "",
        "actuator_server": (
            FastAPIActuatorServer.actuator_server.serialize()
            if FastAPIActuatorServer.actuator_server
            else ""
        ),
    }

    with open(file_, "w") as yaml_file:
        yaml.safe_dump(data, yaml_file)

    logger.info("Configuration saved to file %s.", file_)
