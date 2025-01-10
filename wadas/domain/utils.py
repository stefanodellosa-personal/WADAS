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
# Date: 2024-07-14
# Description: Module containing utility functions.

import base64
import datetime
import logging
import os
import uuid
from logging.handlers import RotatingFileHandler


def get_timestamp():
    """Method to prepare timestamp string to apply to images naming"""

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return timestamp


def convert_to_datetime(timestamp_str: str) -> datetime:
    """
    Converts a timestamp string into a datetime object.

    :param timestamp_str: Timestamp generated by the `get_timestamp` method,
    formatted as "%Y%m%d-%H%M%S".
    :return: Corresponding datetime object.
    """
    return datetime.datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")


def convert_to_timestamp_string(dt: datetime) -> str:
    """
    Converts a datetime object into a timestamp string formatted as "%Y%m%d-%H%M%S".

    :param dt: Datetime object.
    :return: Corresponding timestamp string.
    """
    return dt.strftime("%Y%m%d-%H%M%S")


def initialize_asyncio_logger(handler=None, level=logging.DEBUG):
    if not handler:
        handler = RotatingFileHandler(
            os.path.join("log", "asyncio.log"), maxBytes=100000, backupCount=3
        )
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        async_logger = logging.getLogger("asyncio")
        for h in async_logger.handlers[:]:
            async_logger.removeHandler(h)
        async_logger.setLevel(level)
        async_logger.addHandler(handler)
        async_logger.propagate = False


def image_to_base64(image_path):
    """Convert an image into a Base64 string."""
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_string


def is_valid_uuid4(val):
    try:
        uuid.UUID(str(val), version=4)
        return True
    except ValueError:
        return False
