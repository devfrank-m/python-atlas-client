from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Collection:
    id: str
    name: str
    dimension: int | None = None
    metric: str | None = None
    vector_count: int | None = None


@dataclass
class VectorInsertResult:
    id: int


@dataclass
class SearchResult:
    id: int
    score: float
    metadata: dict[str, Any]
    vector: list[float] | None = None
    external_id: str | None = None


@dataclass
class SearchResponse:
    results: list[SearchResult] = field(default_factory=list)


@dataclass
class Filter:
    key: str
    value: Any
    op: str = "eq"

    def to_dict(self) -> dict[str, Any]:
        return {"op": self.op, "key": self.key, "value": self.value}
