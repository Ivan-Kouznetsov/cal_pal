from enum import Enum
from typing import Any, Iterable, Optional

import pytomlpp  # type: ignore


def load_config(filename: str = "config.toml") -> Optional[dict]:
    try:
        with open(filename, "r") as f:
            return pytomlpp.loads(f.read())
    except IOError:
        return None


def find_missing_field(
    settings: dict, required_fields: Iterable[Enum]
) -> Optional[str]:
    for field in required_fields:
        if field.value not in settings:
            return field.value

    return None
