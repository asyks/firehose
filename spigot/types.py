from __future__ import annotations

from enum import Enum


class MessageType(Enum):
    HTTP = "http"
    RAW = "raw"


def to_bytes(data: str | bytes, encoding: str) -> bytes:
    data_bytes: bytes
    if type(data) == str:
        return data.encode(encoding)
    else:
        data_bytes = data  # type: ignore[assignment]

    return data_bytes
