from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from enum import Enum


SENSITIVE_FIELDS = {"senha", "senha_hash", "password", "password_hash"}


def serialize(value):
    if is_dataclass(value):
        return serialize(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {
            key: serialize(item)
            for key, item in value.items()
            if key not in SENSITIVE_FIELDS
        }
    return value
