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
