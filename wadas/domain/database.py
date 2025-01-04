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

from abc import abstractmethod
from enum import Enum

import keyring


class DBTypes(Enum):
    SQLITE = "SQLite"
    MYSQL = "MySQL"


class DataBase:
    """Base Class to handle DB object."""

    def __init__(self, host):
        """
        Initialize the database connection object.

        :param host: The database host (e.g., file path for SQLite or hostname for MySQL).
        """
        self.host = host
        self.db_type = None

    @abstractmethod
    def get_connection_string(self):
        """Generate the connection string based on the database type."""

    @abstractmethod
    def serialize(self):
        """Method to serialize DataBase object into file."""

    @staticmethod
    def deserialize(data):
        """Method to deserialize DataBase object from file."""


class MySQLDataBase(DataBase):
    """
    MySQL DataBase class
    :param username: The username for database authentication (optional for SQLite).
    :param database: The name of the database (optional for SQLite).
    """

    def __init__(self, host, username, database_name):
        super().__init__(host)
        self.db_type = DBTypes.MYSQL
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
        return f"mysql+pymysql://{self.username}:{password}@{self.host}/{self.database_name}"

    def serialize(self):
        """Method to serialize MySQL DataBase object into file."""

        return {
            "host": self.host,
            "db_type": self.db_type.value,
            "username": self.username,
            "database_name": self.database_name,
        }

    def deserialize(data):
        """Method to deserialize MySQL DataBase object from file."""

        return MySQLDataBase(**data)


class SQLiteDataBase(DataBase):
    """SQLite DataBase class"""

    def __init__(self, host):
        super().__init__(host)

    def get_connection_string(self):
        """Generate the connection string based on the database type."""

        return f"sqlite:///{self.host}"

    def serialize(self):
        """Method to serialize SQLite DataBase object into file."""

        return {"host": self.host, "db_type": self.db_type.value}

    def deserialize(data):
        """Method to deserialize SQLite DataBase object from file."""

        return SQLiteDataBase(**data)
