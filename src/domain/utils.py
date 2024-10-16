import datetime


def get_timestamp():
    """Method to prepare timestamp string to apply to images naming"""

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return timestamp
