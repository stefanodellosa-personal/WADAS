from wadas.domain.db_model import Actuator as DB_Actuator
from wadas.domain.db_model import Camera as DB_Camera
from wadas.domain.db_model import DetectionEvent as DB_DetectionEvent
from wadas.domain.db_model import User as DB_User
from wadas_webserver.view_model import Actuator, Camera, DetectionEvent, User


class Mapper:

    @staticmethod
    def map_db_user_to_user(db_user: DB_User) -> User:
        return User(
            username=db_user.username,
            password=db_user.password,
            email=db_user.email,
            role=db_user.role,
        )

    @staticmethod
    def map_db_camera_to_camera(db_camera: DB_Camera) -> Camera:
        return Camera(
            id=db_camera.db_id,
            name=db_camera.camera_id,
            type=db_camera.type,
            enabled=db_camera.enabled,
            actuators=[Mapper.map_db_actuator_to_actuator(x) for x in db_camera.actuators],
        )

    @staticmethod
    def map_db_actuator_to_actuator(db_actuator: DB_Actuator) -> Actuator:
        return Actuator(id=db_actuator.db_id, name=db_actuator.actuator_id, type=db_actuator.type)

    @staticmethod
    def map_db_detectionevent_to_detectionevent(db_detevent: DB_DetectionEvent) -> DetectionEvent:
        return DetectionEvent(
            id=db_detevent.db_id,
            camera_id=db_detevent.camera_id,
            detection_img_path=db_detevent.detection_img_path,
            classification_img_path=db_detevent.classification_img_path,
            detected_animals=db_detevent.detected_animals,
            classification=db_detevent.classification,
            classified_animals=[x.classified_animal for x in db_detevent.classified_animals],
            timestamp=db_detevent.time_stamp,
        )
