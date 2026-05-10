from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AtlasError(Exception):
    status_code: int
    message: str

    def __str__(self) -> str:
        return f"[{self.status_code}] {self.message}"


class ConnectionError(AtlasError):
    pass


class NotFoundError(AtlasError):
    pass


class ValidationError(AtlasError):
    pass
