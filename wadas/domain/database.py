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

from enum import Enum

import keyring


class DBTypes(Enum):
    SQLITE = "SQLite"
    MYSQL = "MySQL"


class DataBase:
    """Class to handle DB object."""

    def __init__(self, host, username=None, database_name=None, db_type=DBTypes.SQLITE):
        """
        Initialize the database connection object.

        :param host: The database host (e.g., file path for SQLite or hostname for MySQL).
        :param username: The username for database authentication (optional for SQLite).
        :param database: The name of the database (optional for SQLite).
        :param db_type: The type of database ('sqlite' or 'mysql').
        :param keyring_service: The keyring service name for storing/retrieving the password.
        """
        if not isinstance(db_type, DBTypes):
            raise TypeError(f"Expected 'DBTypes', got {type(db_type).__name__}")
        self.host = host
        self.username = username
        self.database_name = database_name
        self.db_type = db_type
        self.keyring_service = "WADAS_DB_SQLite" if db_type == DBTypes else "WADAS_DB_MySQL"

    def get_password(self):
        """Retrieve the password from the keyring."""

        if not self.keyring_service or not self.username:
            raise ValueError(
                "Keyring service and username must be defined to retrieve the password."
            )
        return keyring.get_password(self.keyring_service, self.username)

    def get_connection_string(self):
        """Generate the connection string based on the database type."""

        if self.db_type == DBTypes.SQLITE:
            return f"sqlite:///{self.host}"
        elif self.db_type == DBTypes.MYSQL:
            password = self.get_password()
            if not self.database_name:
                raise ValueError("Database name is required for MySQL.")
            return f"mysql+pymysql://{self.username}:{password}@{self.host}/{self.database_name}"
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    # TODO: add serialization/deserialization methods
