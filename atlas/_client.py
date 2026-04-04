from __future__ import annotations

from typing import Any

import httpx

from ._base import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    _build_client_kwargs,
    _build_create_body,
    _build_insert_body,
    _build_search_body,
    _parse_collection,
    _parse_insert,
    _parse_search,
    _raise_for_status,
)
from ._models import Collection, Filter, SearchResponse, VectorInsertResult


class AtlasClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        self._client = httpx.Client(
            **_build_client_kwargs(base_url, timeout, headers, **kwargs)
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        response = self._client.request(method, path, **kwargs)
        _raise_for_status(response)
        return response.json()

    def create_collection(
        self,
        name: str,
        dimension: int,
        metric: str,
        index: str | None = None,
    ) -> Collection:
        data = self._request(
            "POST",
            "/collections",
            json=_build_create_body(name, dimension, metric, index),
        )
        return _parse_collection(data)

    def get_collection(self, collection_id: str) -> Collection:
        data = self._request("GET", f"/collections/{collection_id}")
        return _parse_collection(data)

    def insert_vector(
        self,
        collection_id: str,
        vector: list[float],
        metadata: dict[str, Any],
        external_id: str | None = None,
    ) -> VectorInsertResult:
        data = self._request(
            "POST",
            f"/collections/{collection_id}/vectors",
            json=_build_insert_body(vector, metadata, external_id),
        )
        return _parse_insert(data)

    def search(
        self,
        collection_id: str,
        vector: list[float],
        k: int,
        filter: Filter | None = None,
    ) -> SearchResponse:
        data = self._request(
            "POST",
            f"/collections/{collection_id}/search",
            json=_build_search_body(vector, k, filter),
        )
        return _parse_search(data)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> AtlasClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
