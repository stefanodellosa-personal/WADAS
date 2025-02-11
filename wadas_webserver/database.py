import logging
from typing import List, Optional, Tuple

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker

from wadas.domain.db_model import Camera as DB_Camera
from wadas.domain.db_model import ClassifiedAnimals as DB_ClassifiedAnimal
from wadas.domain.db_model import DetectionEvent as DB_DetectionEvent
from wadas.domain.db_model import User as DB_User
from wadas_webserver.mapper import Mapper
from wadas_webserver.view_model import Camera, DetectionEvent, User

logger = logging.getLogger(__name__)


class Database:
    instance = None

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(self.get_connection_string())

    def get_connection_string(self):
        return self.connection_string

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Method to get a user object from his username"""
        session = sessionmaker(bind=self.engine)()
        user = None
        try:
            db_user = session.query(DB_User).filter(DB_User.username == username).first()
            user = Mapper.map_db_user_to_user(db_user) if db_user else None
        finally:
            session.close()

        return user

    def get_all_detection_events(self) -> Tuple[int, List[DetectionEvent]]:
        """Method to get all detection events in the database and their count."""
        session = sessionmaker(bind=self.engine)()
        events = []
        count = 0
        try:
            count = session.query(DB_DetectionEvent).count()
            result = session.query(DB_DetectionEvent).all()
            events = [Mapper.map_db_detectionevent_to_detectionevent(x) for x in result]
        finally:
            session.close()
        return count, events

    def get_detection_events_by_filter(
        self,
        camera_ids=None,
        date_from=None,
        date_to=None,
        detected_animals_operator=None,
        detected_animals_value=None,
        order_by="timestamp_desc",
        offset=0,
        limit=20,
    ) -> Tuple[int, List[DetectionEvent]]:
        """Method to get paginated detection events filtered
        by different filters and their total count"""
        session = sessionmaker(bind=self.engine)()
        query = session.query(DB_DetectionEvent)

        # filter section
        if camera_ids:
            query = query.filter(DB_DetectionEvent.camera_id.in_(camera_ids))
        if date_from:
            query = query.filter(DB_DetectionEvent.time_stamp >= date_from)
        if date_to:
            query = query.filter(DB_DetectionEvent.time_stamp <= date_to)
        if detected_animals_value:
            query = query.filter(DB_DetectionEvent.detected_animals == detected_animals_value)

        try:
            # get the total number
            count = query.count()

            # order_by, offset, limit
            query = query.order_by(DB_DetectionEvent.time_stamp.desc())  # todo handle order_by
            query = query.offset(offset)
            query = query.limit(limit)

            result = query.all()
            events = [Mapper.map_db_detectionevent_to_detectionevent(x) for x in result]
        finally:
            session.close()
        return count, events

    def get_cameras(self) -> List[Camera]:
        """Method to get all the enabled cameras"""
        session = sessionmaker(bind=self.engine)()
        cameras = []
        try:
            result = (
                session.query(DB_Camera)
                .filter(and_(DB_Camera.deletion_date.is_(None), DB_Camera.enabled.is_(True)))
                .all()
            )
            cameras = [Mapper.map_db_camera_to_camera(x) for x in result]
        finally:
            session.close()
        return cameras

    def get_known_animals(self) -> List[str]:
        """Method to get all the enabled cameras"""
        session = sessionmaker(bind=self.engine)()
        animals_names = []
        try:
            result = (
                session.query(DB_ClassifiedAnimal.classified_animal)
                .distinct(DB_ClassifiedAnimal.classified_animal)
                .order_by(DB_ClassifiedAnimal.classified_animal)
                .all()
            )
            animals_names = [x[0] for x in result]
        finally:
            session.close()
        return animals_names
