"""This module takes care of all challenges with time stamps."""

from typing import Any
from datetime import datetime

from src.api.constants import TIME_FORMAT


def convert_timestamp(value) -> Any:
    """Converts a datetime object into the format yyyy-mm-dd (e.g. 2024-09-13)."""

    # Don't touch the value if it's not a datetime object!
    if isinstance(value, datetime):
        return value.strftime(TIME_FORMAT)
    return value


def custom_json_encoder(obj):
    """Encodes datetime objects in a JSON-compatible format."""

    if isinstance(obj, datetime):
        return obj.strftime(TIME_FORMAT)

    try:
        return obj.isoformat()[:10]
    except AttributeError:
        pass
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")