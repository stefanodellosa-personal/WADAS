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

from wadas.domain.db_model import Base

logger = logging.getLogger(__name__)
DB_VERSION = 0.1


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
            raise RuntimeError(
                "The database engine has not been initialized. Call 'initialize' first."
            )
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

    def __init__(self, host, port, username, database_name, enabled=False, version=DB_VERSION):
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

    def __init__(self, host, enabled=True, version=DB_VERSION):
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
            Base.metadata.create_all(DataBase.wadas_db_engine)
            return True
        else:
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
