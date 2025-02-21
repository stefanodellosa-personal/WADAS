import logging
from contextlib import contextmanager
from typing import List, Optional, Tuple

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import joinedload, sessionmaker

from wadas.domain.actuator import Actuator
from wadas.domain.db_model import ActuationEvent as DB_ActuationEvent
from wadas.domain.db_model import Actuator as DB_Actuator
from wadas.domain.db_model import Camera as DB_Camera
from wadas.domain.db_model import ClassifiedAnimals as DB_ClassifiedAnimal
from wadas.domain.db_model import DetectionEvent as DB_DetectionEvent
from wadas.domain.db_model import User as DB_User
from wadas_webserver.mapper import Mapper
from wadas_webserver.view_model import ActuationEvent, Camera, DetectionEvent, User

logger = logging.getLogger(__name__)


class Database:
    instance = None

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(self.get_connection_string())

    @contextmanager
    def get_session(self):
        """Context manager to handle session"""
        session = sessionmaker(bind=self.engine)()
        try:
            yield session
        except Exception:
            logger.exception("An error occurred while creating a session")
        finally:
            session.close()

    def get_connection_string(self):
        return self.connection_string

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Method to get a user object from his username"""
        with self.get_session() as session:
            db_user = session.query(DB_User).filter(DB_User.username == username).first()
            user = Mapper.map_db_user_to_user(db_user) if db_user else None
            return user

    def get_all_detection_events(self) -> Tuple[int, List[DetectionEvent]]:
        """Method to get all detection events in the database and their count."""
        with self.get_session() as session:
            result = session.query(DB_DetectionEvent).all()
            events = [Mapper.map_db_detectionevent_to_detectionevent(x) for x in result]
            return len(result), events

    def get_detection_event_by_id(self, event_id) -> Optional[DetectionEvent]:
        with self.get_session() as session:
            item = (
                session.query(DB_DetectionEvent).where(DB_DetectionEvent.db_id == event_id).first()
            )
            return Mapper.map_db_detectionevent_to_detectionevent(item) if item else None

    def get_detection_events_by_filter(
        self,
        camera_ids=None,
        date_from=None,
        date_to=None,
        classified_animals=None,
        order_by="timestamp_desc",
        offset=0,
        limit=20,
    ) -> Tuple[int, List[DetectionEvent]]:
        """Method to get paginated detection events filtered
        by different filters and their total count"""
        with self.get_session() as session:
            query = session.query(DB_DetectionEvent)

            # filter section
            if camera_ids:
                query = query.filter(DB_DetectionEvent.camera_id.in_(camera_ids))
            if date_from:
                query = query.filter(DB_DetectionEvent.time_stamp >= date_from)
            if date_to:
                query = query.filter(DB_DetectionEvent.time_stamp <= date_to)
            if classified_animals:
                query = (
                    query.join(DB_ClassifiedAnimal)
                    .filter(DB_ClassifiedAnimal.classified_animal.in_(classified_animals))
                    .options(joinedload(DB_DetectionEvent.classified_animals))
                )

            # get the total number
            count = query.count()

            # order_by, offset, limit
            query = query.order_by(DB_DetectionEvent.time_stamp.desc())  # TODO: handle order_by
            query = query.offset(offset)
            query = query.limit(limit)

            result = query.all()
            events = [Mapper.map_db_detectionevent_to_detectionevent(x) for x in result]
            return count, events

    def get_actuation_events_by_filter(
        self,
        detection_id=None,
        date_from=None,
        date_to=None,
        actuator_types=None,
        commands=None,
        order_by="timestamp_desc",
        offset=0,
        limit=20,
    ) -> Tuple[int, List[ActuationEvent]]:
        """Method to get paginated actuation events filtered
        by different filters and their total count"""
        with self.get_session() as session:
            query = session.query(DB_ActuationEvent)

            # filter section
            if detection_id:
                query = query.filter(DB_ActuationEvent.detection_event_id == detection_id)
            if date_from:
                query = query.filter(DB_ActuationEvent.time_stamp >= date_from)
            if date_to:
                query = query.filter(DB_ActuationEvent.time_stamp <= date_to)
            if commands:
                query = query.filter(DB_ActuationEvent.command.in_(commands))
            if actuator_types:
                try:
                    enum_values = [Actuator.ActuatorTypes(value) for value in actuator_types]
                except Exception:
                    logger.exception("Unable to find appropriate ActuatorTypes Value")
                    enum_values = []
                query = (
                    query.join(DB_Actuator)
                    .filter(DB_Actuator.type.in_(enum_values))
                    .options(joinedload(DB_ActuationEvent.actuator))
                )

            # get the total number
            count = query.count()

            # order_by, offset, limit
            query = query.order_by(DB_ActuationEvent.time_stamp.desc())  # TODO: handle order_by
            query = query.offset(offset)
            query = query.limit(limit)

            result = query.all()
            events = [Mapper.map_db_actuationevent_to_actuationevent(x) for x in result]
            return count, events

    def get_cameras(self) -> List[Camera]:
        """Method to get all the enabled cameras"""
        with self.get_session() as session:
            result = (
                session.query(DB_Camera)
                .filter(and_(DB_Camera.deletion_date.is_(None), DB_Camera.enabled.is_(True)))
                .all()
            )
            return [Mapper.map_db_camera_to_camera(x) for x in result]

    def get_known_animals(self) -> List[str]:
        """Method to get all the known animals"""
        with self.get_session() as session:
            result = (
                session.query(DB_ClassifiedAnimal.classified_animal)
                .distinct(DB_ClassifiedAnimal.classified_animal)
                .order_by(DB_ClassifiedAnimal.classified_animal)
                .all()
            )
            return [x[0] for x in result]

    def get_known_actuator_types(self) -> List[str]:
        """Method to get all the known types for actuator"""
        with self.get_session() as session:
            result = (
                session.query(DB_Actuator.type)
                .distinct(DB_Actuator.type)
                .order_by(DB_Actuator.type)
                .all()
            )
            return [x[0] for x in result]

    def get_known_actuation_commands(self) -> List[str]:
        """Method to get all the known commands for actuation events"""
        with self.get_session() as session:
            result = (
                session.query(DB_ActuationEvent.command)
                .distinct(DB_ActuationEvent.command)
                .order_by(DB_ActuationEvent.command)
                .all()
            )
            return [x[0] for x in result]
