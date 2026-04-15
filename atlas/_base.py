from __future__ import annotations

from typing import Any

import httpx

from ._exceptions import AtlasError, NotFoundError, ValidationError
from ._models import (
    Collection,
    Filter,
    SearchResponse,
    SearchResult,
    VectorInsertResult,
)

DEFAULT_HOST = "http://localhost:8600"
DEFAULT_TIMEOUT = 30.0


def _build_client_kwargs(
    host: str,
    timeout: float,
    headers: dict[str, str] | None,
    **kwargs: Any,
) -> dict[str, Any]:
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    return {"base_url": host, "timeout": timeout, "headers": h, **kwargs}


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return
    try:
        body = response.json()
        msg = body.get("error", response.text)
    except Exception:
        msg = response.text

    status = response.status_code
    if status == 404:
        raise NotFoundError(status, msg)
    if status == 400:
        raise ValidationError(status, msg)
    raise AtlasError(status, msg)


def _parse_collection(data: dict[str, Any]) -> Collection:
    return Collection(
        id=data["id"],
        name=data["name"],
        dimension=data.get("dimension"),
        metric=data.get("metric"),
        vector_count=data.get("vector_count"),
    )


def _parse_insert(data: dict[str, Any]) -> VectorInsertResult:
    return VectorInsertResult(id=data["id"])


def _parse_search(data: dict[str, Any]) -> SearchResponse:
    return SearchResponse(
        results=[
            SearchResult(
                id=r["id"],
                score=r["score"],
                metadata=r["metadata"],
                vector=r.get("vector"),
                external_id=r.get("external_id"),
            )
            for r in data.get("results", [])
        ]
    )


def _build_insert_body(
    vector: list[float],
    metadata: dict[str, Any],
    external_id: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"vector": vector, "metadata": metadata}
    if external_id is not None:
        body["external_id"] = external_id
    return body


def _build_search_body(
    vector: list[float],
    k: int,
    filter: Filter | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"vector": vector, "k": k}
    if filter is not None:
        body["filter"] = filter.to_dict()
    return body


def _build_create_body(
    name: str,
    dimension: int,
    metric: str,
    index: str | None,
) -> dict[str, Any]:
    body: dict[str, Any] = {"name": name, "dimension": dimension, "metric": metric}
    if index is not None:
        body["index"] = index
    return body
