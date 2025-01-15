# This file is part of WADAS project.
#
# WADAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WADAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WADAS. If not, see <https://www.gnu.org/licenses/>.
#
# Author(s): Stefano Dell'Osa, Alessandro Palla, Cesare Di Mauro, Antonio Farina
# Date: 2025-01-04
# Description: database module.

import json
import logging
from abc import ABC, abstractmethod
from enum import Enum

import keyring
from pymysql import OperationalError
from sqlalchemy import and_, create_engine, text, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError as SQLiteOperationalError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from wadas._version import __dbversion__
from wadas.domain.actuation_event import ActuationEvent
from wadas.domain.actuator import Actuator
from wadas.domain.camera import cameras
from wadas.domain.db_model import ActuationEvent as ORMActuationEvent
from wadas.domain.db_model import Actuator as ORMActuator
from wadas.domain.db_model import Base
from wadas.domain.db_model import Camera as ORMCamera
from wadas.domain.db_model import ClassifiedAnimals as ORMClassifiedAnimals
from wadas.domain.db_model import DBMetadata as ORMDBMetadata
from wadas.domain.db_model import DetectionEvent as ORMDetectionEvent
from wadas.domain.db_model import FeederActuator as ORMFeederActuator
from wadas.domain.db_model import FTPCamera as ORMFTPCamera
from wadas.domain.db_model import RoadSignActuator as ORMRoadSignActuator
from wadas.domain.db_model import USBCamera as ORMUSBCamera
from wadas.domain.detection_event import DetectionEvent
from wadas.domain.feeder_actuator import FeederActuator
from wadas.domain.ftp_camera import FTPCamera
from wadas.domain.roadsign_actuator import RoadSignActuator
from wadas.domain.usb_camera import USBCamera
from wadas.domain.utils import get_precise_timestamp

logger = logging.getLogger(__name__)


class DBMetadata:
    def __init__(self, description: str, project_uuid):
        self.version = __dbversion__
        self.applied_at = get_precise_timestamp()
        self.description = description
        self.project_uuid = project_uuid


class DataBase(ABC):
    """Base Class to handle DB object."""

    wadas_db = None  # Singleton instance of the database
    wadas_db_engine = None  # Singleton engine associated with the database

    class DBTypes(Enum):
        SQLITE = "SQLite"
        MYSQL = "MySQL"
        MARIADB = "MariaDB"

    def __init__(self, host, enabled=True, version=__dbversion__):
        """Constructor is not public, no external code should call this directly"""

        if DataBase.wadas_db is not None:
            raise RuntimeError("Database instance already created.")

        self.host = host
        self.enabled = enabled
        self.version = version

    @classmethod
    def _create_instance(
        cls,
        db_type: DBTypes,
        host,
        port,
        username,
        database_name,
        enabled=True,
        version=__dbversion__,
    ):
        """Create the database instance."""

        if not host:
            return False

        # Create the appropriate database instance
        match db_type:
            case DataBase.DBTypes.MYSQL:

                return (
                    MySQLDataBase(host, port, username, database_name, enabled, version)
                    if (port and username and database_name)
                    else False
                )
            case DataBase.DBTypes.MARIADB:
                return (
                    MariaDBDataBase(host, port, username, database_name, enabled, version)
                    if (port and username and database_name)
                    else False
                )
            case DataBase.DBTypes.SQLITE:
                return SQLiteDataBase(host, enabled, version)
            case _:
                logger.error("Unsupported database type %s!", db_type)
                raise ValueError(f"Unsupported database type: {db_type}")

    @classmethod
    def initialize(
        cls,
        db_type: DBTypes,
        host,
        port,
        username,
        database_name,
        enabled=True,
        version=__dbversion__,
    ):
        """Initialize the singleton database instance."""

        if cls.wadas_db is not None:
            logger.error("Database is already initialized.")
            return False

        sb_instance = cls._create_instance(
            db_type, host, port, username, database_name, enabled=True, version=__dbversion__
        )
        if sb_instance:
            cls.wadas_db = sb_instance
        else:
            return False

        cls.wadas_db_engine = create_engine(cls.wadas_db.get_connection_string())
        logger.info("%s database initialized.", db_type.value)
        return True

    @classmethod
    def get_engine(cls):
        """
        Retrieve the singleton engine. If not initialized, raise an exception.

        :return: SQLAlchemy engine instance.
        """
        if cls.wadas_db_engine is None:
            if cls.wadas_db is None:
                logger.error("The database and db engine have not been initialized.")
                raise RuntimeError("The database and db engine have not been initialized.")
            else:
                logger.debug("Initializing engine...")
                cls.wadas_db_engine = create_engine(cls.wadas_db.get_connection_string())
        return cls.wadas_db_engine

    @classmethod
    def get_instance(cls):
        """
        Retrieve the singleton database instance.

        :return: The current database instance.
        """
        if cls.wadas_db is None:
            logger.debug("The database has not been initialized. Call 'initialize' first.")
            return None
        return cls.wadas_db

    @classmethod
    def destroy_instance(cls):
        """Destroy the current database instance and release resources."""

        logger.debug("Destroying db isntance...")
        if cls.wadas_db_engine:
            try:
                cls.wadas_db_engine.dispose()
            except Exception:
                logger.warning("Failed to dispose the database engine.")
        cls.wadas_db_engine = None
        cls.wadas_db = None

    @classmethod
    def create_session(cls):
        """Method to create a session to perform operation with the db"""

        if engine := cls.get_engine():
            Session = sessionmaker(bind=engine)
            return Session()
        else:
            logger.error("Unable to create a session as DB engine is not initialized.")
            return None

    @classmethod
    def run_query(cls, stmt):
        """Generic method to run a query starting forma statement as input and handling
        exceptions (if any)."""

        logger.debug("Running query: %s", str(stmt))
        if session := cls.create_session():
            try:
                session.execute(stmt)
                session.commit()
            except SQLAlchemyError:
                # Rollback the transaction in case of an error
                session.rollback()
                logger.exception(
                    "SQLAlchemy error occurred while running the query: %s.", str(stmt)
                )
            except Exception:
                # Handle other unexpected errors
                session.rollback()
                logger.exception(
                    "SQLAlchemy error occurred while running the query: %s.", str(stmt)
                )
        else:
            logger.error("DB session not initialized.")

    @classmethod
    def insert_into_db(cls, domain_object):
        """Method to insert a WADAS object into the db."""

        logger.debug("Inserting object into db...")
        if session := cls.create_session():
            foreign_key = []
            if isinstance(domain_object, DetectionEvent):
                # If Camera associated to the detection event is not in db abort insertion
                foreign_key.append(
                    session.query(ORMCamera.db_id)
                    .filter_by(camera_id=domain_object.camera_id)
                    .scalar()
                )
                if not foreign_key:
                    logger.error(
                        "Unable to add Detection event into db as %s camera id is not found in db.",
                        domain_object.camera_id,
                    )
                    return
            if isinstance(domain_object, ActuationEvent):
                # If Actuator associated to the actuation event is not in db abort insertion
                foreign_key.append(
                    session.query(ORMActuator.db_id)
                    .filter_by(actuator_id=domain_object.actuator_id)
                    .scalar()
                )
                if not foreign_key:
                    logger.error(
                        "Unable to add Actuation event into db as %s actuator id is not found"
                        " in db.",
                        domain_object.actuator_id,
                    )
                    return
                # If detection event associated to the actuation event is not in db abort insertion
                foreign_key.append(cls.get_detection_event_id(domain_object.detection_event))
                if not foreign_key[1]:
                    logger.error(
                        "Unable to add Actuation event into db as %s detection event id is not"
                        " found in db.",
                        domain_object.detection_event,
                    )
                    return
            try:
                orm_object = DataBase.domain_to_orm(domain_object, foreign_key)
                session.add(orm_object)

                # If instance is a camera, handle relationship with actuators
                if isinstance(domain_object, FTPCamera) or isinstance(domain_object, USBCamera):
                    for actuator in domain_object.actuators:
                        orm_actuator = (
                            session.query(ORMActuator).filter_by(actuator_id=actuator.id).first()
                        )
                        if orm_actuator:
                            orm_object.actuators.append(orm_actuator)

                session.commit()
                logger.debug(
                    "Object '%s' successfully added to the db!", type(domain_object).__name__
                )
            except IntegrityError:
                session.rollback()  # Cancel modifications in case of error
                logger.exception(
                    "Error while inserting object %s into db.", type(domain_object).__name__
                )

    def update_detection_event(cls, detection_event: DetectionEvent):
        """Update fields of a detection_events record in db.
        This is typically the case when classification details
        into an existing detection event object.
        """

        logger.debug("Updating detection event db entry...")
        # Retrieve the db id of the updated detection event
        detection_event_db_id = cls.get_detection_event_id(detection_event)
        if not detection_event_db_id:
            logger.error("Unable to update detection event as detection event not found in db.")

        if session := cls.create_session():
            # Update detection_event table
            stmt = (
                update(ORMDetectionEvent)
                .where(and_(ORMDetectionEvent.db_id == detection_event_db_id))
                .values(
                    classification=detection_event.classification,
                    classification_img_path=detection_event.classification_img_path,
                )
            )
            cls.run_query(stmt)

            try:
                if detection_event_db_id:
                    # Create ClassifiedAnimals table entries and link them with detection event
                    for classified_animal in detection_event.classified_animals:
                        orm_obj = ORMClassifiedAnimals(
                            detection_event_id=detection_event_db_id,  # Link to det event by ID
                            classified_animal=classified_animal["classification"][0],
                            probability=classified_animal["classification"][1],
                        )
                        session.add(orm_obj)
                    session.commit()

            except SQLAlchemyError:
                # Rollback the transaction in case of an error
                session.rollback()
                logger.exception("An error occurred while updating detection event into db.")
            except Exception:
                # Handle other unexpected errors
                session.rollback()
                logger.exception(
                    "Unexpected error occurred while updating detection event into db."
                )
        else:
            logger.error("unable to update detection event into db...")

    @classmethod
    def update_camera(cls, camera, delete_camera=False):
        """Method to reflect camera fields update in db."""

        logger.debug("Updating camera db entry...")
        stmt = (
            (
                update(ORMFTPCamera)
                .where(ORMFTPCamera.camera_id == camera.id)
                .values(enabled=camera.enabled)
            )
            if not delete_camera
            else (
                update(ORMFTPCamera)
                .where(ORMFTPCamera.camera_id == camera.id)
                .values(deleted_time=get_precise_timestamp())
            )
        )
        cls.run_query(stmt)

    @classmethod
    def add_actuator_to_camera(cls, camera, actuator):
        """Method to add new actuator to a given camera actuators list."""

        if cls.get_instance():
            logger.debug("Adding actuator %s to camera %s in db.", actuator.id, camera.id)
            if session := cls.create_session():
                try:
                    # Retrieve camera and actuator db instances
                    camera = session.query(ORMCamera).filter_by(camera_id=camera.id).one()
                    actuator = session.query(ORMActuator).filter_by(actuator_id=actuator.id).one()

                    # Add the actuator to the camera actuators list
                    camera.actuators.append(actuator)
                    session.commit()
                except SQLAlchemyError:
                    # Rollback the transaction in case of an error
                    session.rollback()
                    logger.exception(
                        "SQLAlchemy error occurred while updating actuator "
                        "association to camera into db."
                    )
                except Exception:
                    # Handle other unexpected errors
                    session.rollback()
                    logger.exception(
                        "Unexpected error occurred while updating actuator "
                        "association to camera into db."
                    )
        else:
            logger.debug("No db configured, skipping actuator association insert.")

    @classmethod
    def get_camera_id(cls, camera_id):
        """Method to return camera database id (primary key)"""

        if session := cls.create_session():
            return (
                session.query(ORMCamera.db_id)
                .filter(
                    and_(
                        ORMCamera.camera_id == camera_id,
                    )
                )
                .scalar()
            )  # Use scalar() to retrieve the value directly
        else:
            logger.debug("No camera id %s found in db.", camera_id)
            return None

    @classmethod
    def get_detection_event_id(cls, detection_event: DetectionEvent):
        """Method to return detection event database id (primary key)"""

        camera_db_id = cls.get_camera_id(detection_event.camera_id)
        if not camera_db_id:
            logger.error("Unable to find Camera id %s while getting Detection event id.")
            return None

        if session := cls.create_session():
            return (
                session.query(ORMDetectionEvent.db_id)
                .filter(
                    and_(
                        ORMDetectionEvent.camera_id == camera_db_id,
                        ORMDetectionEvent.time_stamp == detection_event.time_stamp,
                    )
                )
                .scalar()
            )  # Use scalar() to retrieve the value directly
        else:
            return None

    @staticmethod
    def domain_to_orm(domain_object, foreign_key=None):
        """Convert a domain object to an ORM object."""

        if isinstance(domain_object, FTPCamera):
            return ORMFTPCamera(
                camera_id=domain_object.id,
                enabled=domain_object.enabled,
                ftp_folder=domain_object.ftp_folder,
                creation_date=get_precise_timestamp(),
            )
        elif isinstance(domain_object, USBCamera):
            return ORMUSBCamera(
                camera_id=domain_object.id,
                name=domain_object.name,
                enabled=domain_object.enabled,
                pid=domain_object.pid,
                vid=domain_object.vid,
                path=domain_object.path,
                creation_date=get_precise_timestamp(),
            )
        elif isinstance(domain_object, RoadSignActuator):
            return ORMRoadSignActuator(
                actuator_id=domain_object.id,
                enabled=domain_object.enabled,
                creation_date=get_precise_timestamp(),
            )
        elif isinstance(domain_object, FeederActuator):
            return ORMFeederActuator(
                actuator_id=domain_object.id,
                enabled=domain_object.enabled,
                creation_date=get_precise_timestamp(),
            )
        elif isinstance(domain_object, ActuationEvent):
            command = json.loads(domain_object.command.value)

            return ORMActuationEvent(
                actuator_id=foreign_key[0],
                time_stamp=domain_object.time_stamp,
                detection_event_id=foreign_key[1],
                command=next(iter(command)),
            )
        elif isinstance(domain_object, DetectionEvent):
            return ORMDetectionEvent(
                camera_id=foreign_key[0],
                time_stamp=domain_object.time_stamp,
                original_image=domain_object.original_image,
                detection_img_path=domain_object.detection_img_path,
                detected_animals=len(
                    domain_object.detected_animals["detections"].xyxy
                ),  # detected_animals count
                classification=domain_object.classification,
                classification_img_path=domain_object.classification_img_path,
            )
        elif isinstance(domain_object, DBMetadata):
            return ORMDBMetadata(
                version=domain_object.version,
                applied_at=domain_object.applied_at,
                description=domain_object.description,
                project_uuid=str(domain_object.project_uuid),
            )
        else:
            raise ValueError(f"Unsupported domain object type: {type(domain_object).__name__}")

    @staticmethod
    def orm_to_domain(orm_object):
        """Convert an ORM object to a domain object."""

        try:
            if isinstance(orm_object, ORMFTPCamera):
                return FTPCamera(
                    id=orm_object.camera_id,
                    ftp_folder=orm_object.ftp_folder,
                    enabled=orm_object.enabled,
                )
            elif isinstance(orm_object, ORMUSBCamera):
                return USBCamera(
                    id=orm_object.camera_id,
                    name=orm_object.name,
                    enabled=orm_object.enabled,
                    pid=orm_object.pid,
                    vid=orm_object.vid,
                    path=orm_object.path,
                )
            elif isinstance(orm_object, ORMRoadSignActuator):
                return RoadSignActuator(id=orm_object.actuator_id, enabled=orm_object.enabled)
            elif isinstance(orm_object, ORMFeederActuator):
                return FeederActuator(id=orm_object.actuator_id, enabled=orm_object.enabled)
            else:
                raise ValueError(f"Unsupported ORM object type: {type(orm_object).__name__}")
        except AttributeError:
            logger.exception("Error mapping ORM object to domain.")
            raise

    @classmethod
    def populate_db(cls, uuid):
        """Method to create a db and optionally populate it with existing domain objects"""

        # Set db metadata
        db_metadata = DBMetadata("WADAS database", uuid)
        cls.insert_into_db(db_metadata)
        # Populate DB with existing cameras and actuators
        if Actuator.actuators:
            for actuator_id in Actuator.actuators:
                cls.insert_into_db(Actuator.actuators[actuator_id])
        if cameras:
            for camera in cameras:
                cls.insert_into_db(camera)

    @abstractmethod
    def get_connection_string(self):
        """Generate the connection string based on the database type."""

    @abstractmethod
    def serialize(self):
        """Method to serialize DataBase object into file."""

    @classmethod
    def deserialize(cls, data):
        """Method to deserialize DataBase object from file."""

        # If db is already initialized, destroy it before new init.
        if cls.get_instance():
            cls.destroy_instance()

        cfg_db_type = data["type"]
        match cfg_db_type:
            case DataBase.DBTypes.SQLITE.value:
                db_type = DataBase.DBTypes.SQLITE
                return cls.initialize(
                    db_type,
                    data["host"],
                    None,
                    "",
                    "",
                    data["enabled"],
                    data["version"],
                )
            case DataBase.DBTypes.MYSQL.value:
                db_type = DataBase.DBTypes.MYSQL
            case DataBase.DBTypes.MARIADB.value:
                db_type = DataBase.DBTypes.MARIADB
            case _:
                logger.error("Wrong deserialized db type!")
                return False

        return cls.initialize(
            db_type,
            data["host"],
            data["port"],
            data["username"],
            data["database_name"],
            data["enabled"],
            data["version"],
        )


class MySQLDataBase(DataBase):
    """MySQL DataBase class"""

    def __init__(self, host, port, username, database_name, enabled=True, version=__dbversion__):
        super().__init__(host, enabled, version)
        self.type = DataBase.DBTypes.MYSQL
        self.port = port
        self.username = username
        self.database_name = database_name

    def get_password(self):
        """Retrieve the password from the keyring."""

        if not self.username:
            raise ValueError("Username must be defined to retrieve the password.")
        return keyring.get_password("WADAS_DB_MySQL", self.username)

    def get_connection_string(self):
        """Generate the connection string based on the database type."""

        password = self.get_password()
        if not self.database_name:
            raise ValueError("Database name is required for MySQL.")
        return (
            "mysql+pymysql://"
            f"{self.username}:{password}@{self.host}:{self.port}/{self.database_name}"
        )

    def create_database(self):
        """Method to create a new database."""

        try:
            # Try to connect to db to check whether it exists
            with DataBase.wadas_db_engine.connect() as conn:
                logger.debug("Database exists.")
        except OperationalError:
            # If db does not exist, creates it
            logger.info("Creating Database...")
            temp_engine = create_engine(self.get_connection_string())
            with temp_engine.connect() as conn:
                conn.execute(f"CREATE DATABASE {self.database_name}")
            logger.info("Database '%s' successfully created.", self.database_name)

        # Create all tables
        Base.metadata.create_all(DataBase.wadas_db_engine)

    def serialize(self):
        """Method to serialize MySQL DataBase object into file."""

        return {
            "host": self.host,
            "port": self.port,
            "type": self.type.value,
            "username": self.username,
            "database_name": self.database_name,
            "enabled": self.enabled,
            "version": self.version,
        }


class MariaDBDataBase(DataBase):
    """MariaDB DataBase class"""

    def __init__(self, host, port, username, database_name, enabled=True, version=__dbversion__):
        super().__init__(host, enabled, version)
        self.type = DataBase.DBTypes.MARIADB
        self.port = port
        self.username = username
        self.database_name = database_name

    def get_password(self):
        """Retrieve the password from the keyring."""

        if not self.username:
            raise ValueError("Username must be defined to retrieve the password.")
        return keyring.get_password("WADAS_DB_MariaDB", self.username)

    def get_connection_string(self, create=False):
        """Generate the connection string based on the database type."""
        password = self.get_password()

        if not self.database_name and not create:
            raise ValueError("Database name is required for MariaDB.")

        base_string = (
            f"mariadb+mariadbconnector://{self.username}:{password}@{self.host}:{self.port}"
        )
        if not create:
            return f"{base_string}/{self.database_name}"
        return base_string

    def create_database(self):
        """Method to create a new database."""
        logger.info("Creating or verifying the existence of the database...")

        temp_engine = create_engine(self.get_connection_string(create=True))

        with temp_engine.connect() as conn:
            # Create db if not already existing
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database_name}"))
            logger.info("Database '%s' successfully created or already exists.", self.database_name)
        try:
            Base.metadata.create_all(DataBase.wadas_db_engine)
            logger.info("Tables created successfully in '%s'.", self.database_name)
        except Exception:
            logger.error("Error while creating the tables...")
            return False
        return True

    def serialize(self):
        """Method to serialize MariaDB DataBase object into file."""

        return {
            "host": self.host,
            "port": self.port,
            "type": self.type.value,
            "username": self.username,
            "database_name": self.database_name,
            "enabled": self.enabled,
            "version": self.version,
        }


class SQLiteDataBase(DataBase):
    """SQLite DataBase class"""

    def __init__(self, host, enabled=True, version=__dbversion__):
        super().__init__(host, enabled, version)
        self.type = DataBase.DBTypes.SQLITE

    def get_connection_string(self):
        """Generate the connection string based on the database type."""

        return f"sqlite:///{self.host}"

    def create_database(self):
        """Method to create database by creating all tables"""

        if DataBase.wadas_db_engine:
            try:
                Base.metadata.create_all(DataBase.wadas_db_engine)
            except SQLiteOperationalError:
                logger.exception("OperationalError during database creation.")
                return False
            except SQLAlchemyError:
                logger.exception("SQLAlchemyError during database creation.")
                return False
            except Exception:
                logger.exception("Unexpected error during database creation.")
                return False
            else:
                logger.info("SQLite Database created successfully.")
                return True
        else:
            logger.warning("Database engine is not initialized.")
            return False

    def serialize(self):
        """Method to serialize SQLite DataBase object into file."""

        return {
            "host": self.host,
            "type": self.type.value,
            "enabled": self.enabled,
            "version": self.version,
        }
