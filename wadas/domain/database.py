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

import logging
from abc import ABC, abstractmethod
from enum import Enum

import keyring
from pymysql import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError as SQLiteOperationalError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from wadas._version import __dbversion__
from wadas.domain.camera import Camera as DomainCamera
from wadas.domain.db_model import Base
from wadas.domain.db_model import Camera as DBCamera
from wadas.domain.db_model import FTPCamera as ORMFTPCamera
from wadas.domain.db_model import USBCamera as ORMUSBCamera
from wadas.domain.ftp_camera import FTPCamera
from wadas.domain.usb_camera import USBCamera

logger = logging.getLogger(__name__)


class DataBase(ABC):
    """Base Class to handle DB object."""

    wadas_db = None  # Singleton instance of the database
    wadas_db_engine = None  # Singleton engine associated with the database

    class DBTypes(Enum):
        SQLITE = "SQLite"
        MYSQL = "MySQL"

    def __init__(self, host):
        self.host = host
        self.type = None
        self.enabled = True
        self.version = None

    @abstractmethod
    def get_connection_string(self):
        """Generate the connection string based on the database type."""

    @classmethod
    def initialize(cls, db_instance):
        """
        Initialize the singleton database instance and its engine.

        :param db_instance: An instance of a subclass of DataBase
        (e.g., MySQLDataBase or SQLiteDataBase).
        """
        if cls.wadas_db is not None:
            raise RuntimeError("The database has already been initialized.")

        cls.wadas_db = db_instance
        cls.wadas_db_engine = create_engine(db_instance.get_connection_string())
        return cls.wadas_db_engine

    @classmethod
    def get_engine(cls):
        """
        Retrieve the singleton engine. If not initialized, raise an exception.

        :return: SQLAlchemy engine instance.
        """
        if cls.wadas_db_engine is None:
            if cls.wadas_db is None:
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
        return cls.wadas_db

    @classmethod
    def destroy_instance(cls):
        """Destroy the current database instance and release resources."""

        if cls.wadas_db_engine:
            try:
                cls.wadas_db_engine.dispose()
            except Exception:
                logger.warning("Failed to dispose the database engine.")
        cls.wadas_db_engine = None
        cls.wadas_db = None

    @staticmethod
    def create_session():
        """Method to create a session to perform operation with the db"""

        engine = DataBase.get_engine()
        if engine:
            Session = sessionmaker(bind=engine)
            return Session()
        else:
            logger.error("Unable to create a session as DB engin is not initialized.")
            return None

    @staticmethod
    def insert_camera(camera):
        """Method to insert a camera object into the db."""

        session = DataBase.create_session()
        if session:
            try:
                orm_camera = DataBase.domain_to_orm(camera)
                session.add(orm_camera)
                session.commit()
                logger.debug("Camera '%s' successfully added to the db!", camera.id)
            except IntegrityError:
                session.rollback()  # Cancel modifications in case of error
                logger.exception("Error while inserting camera ''%s'' into db.", camera.id)

    @staticmethod
    def insert_detection_event(detection_event):
        session = DataBase.create_session()
        if session:
            # Make sure the camera exists in the db before adding the detection_event
            camera = session.query(DBCamera).filter_by(id=detection_event.camera_id).first()
            if camera:
                try:
                    session.add(detection_event)
                    session.commit()
                    logger.debug("DetectionEvent successfuly added into db!")
                except IntegrityError:
                    session.rollback()  # Cancel modifications in case of error
                    logger.exception("Error while inserting detection_event into db.")
            else:
                logger.error(
                    "No camera with id '%s' found. Aborting db insertion of detection_event",
                    detection_event.camera_id,
                )

    @staticmethod
    def domain_to_orm(camera):
        """Convert a domain camera instance to an ORM camera instance."""
        if isinstance(camera, FTPCamera):  # Camera dominio FTP
            return ORMFTPCamera(
                id=camera.id,
                enabled=camera.enabled,
                ftp_folder=camera.ftp_folder,
            )
        elif isinstance(camera, USBCamera):  # Camera dominio USB
            return ORMUSBCamera(
                id=camera.id,
                name=camera.name,
                enabled=camera.enabled,
                pid=camera.pid,
                vid=camera.vid,
                path=camera.path,
            )
        else:
            raise ValueError("Unsupported camera type")

    @staticmethod
    def orm_to_domain(camera_orm):
        """Convert an ORM camera instance to a domain camera instance."""
        try:
            if camera_orm.type == DomainCamera.CameraTypes.FTP_CAMERA:
                return FTPCamera(
                    id=camera_orm.id,
                    ftp_folder=camera_orm.ftp_folder,  # Usa il campo corretto del modello ORM
                    enabled=camera_orm.enabled,
                )
            elif camera_orm.type == DomainCamera.CameraTypes.USB_CAMERA:
                return USBCamera(
                    id=camera_orm.id,
                    name=camera_orm.name,
                    enabled=camera_orm.enabled,
                    pid=camera_orm.pid,
                    vid=camera_orm.vid,
                    path=camera_orm.path,
                )
            else:
                raise ValueError(f"Unsupported camera type: {camera_orm.type}")
        except AttributeError:
            logger.exception("Error mapping ORM camera to domain.")
            raise

    @abstractmethod
    def serialize(self):
        """Method to serialize DataBase object into file."""

    @staticmethod
    @abstractmethod
    def deserialize(data):
        """Method to deserialize DataBase object from file."""


class MySQLDataBase(DataBase):
    """
    MySQL DataBase class
    :param username: The username for database authentication.
    :param database_name: The name of the database.
    """

    def __init__(self, host, port, username, database_name, enabled=False, version=__dbversion__):
        super().__init__(host)
        self.type = DataBase.DBTypes.MYSQL
        self.port = port
        self.username = username
        self.database_name = database_name
        self.enabled = enabled
        self.version = version

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
            # PTry to connect to db to check whether it exists
            with DataBase.wadas_db_engine.connect() as conn:
                logger.debug("Database exists.")
        except OperationalError:
            # If db does not exist, creates it
            logger.info("Creating Database...")
            temp_engine = self.create_db_engine()
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

    @staticmethod
    def deserialize(data):
        """Method to deserialize MySQL DataBase object from file."""

        return MySQLDataBase(
            data["host"],
            data["port"],
            data["username"],
            data["database_name"],
            data["enabled"],
            data["version"],
        )


class SQLiteDataBase(DataBase):
    """SQLite DataBase class"""

    def __init__(self, host, enabled=True, version=__dbversion__):
        super().__init__(host)
        self.type = DataBase.DBTypes.SQLITE
        self.enabled = enabled
        self.version = version

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
                logger.exception("SQLAlchemyError during database creation:.")
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

    @staticmethod
    def deserialize(data):
        """Method to deserialize SQLite DataBase object from file."""

        return SQLiteDataBase(data["host"], data["enabled"], data["version"])
