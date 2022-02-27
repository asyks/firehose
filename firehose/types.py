from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from io import StringIO


class MessageType(Enum):
    HTTP = "http"
    RAW = "raw"


@dataclass
class Response:
    data: StringIO


def to_bytes(data: str | bytes, encoding: str) -> bytes:
    data_bytes: bytes
    if type(data) == str:
        return data.encode(encoding)
    else:
        data_bytes = data  # type: ignore[assignment]

    return data_bytes
