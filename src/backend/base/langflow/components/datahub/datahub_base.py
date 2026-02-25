"""Shared helpers for DataHub components.

Provides a mixin with common GraphQL execution and authentication logic
used by all DataHub tool components.
"""

from __future__ import annotations

from typing import Any

import httpx


class DataHubGraphQLMixin:
    """Mixin providing DataHub GraphQL API helpers.

    Expects the consuming component to have ``graphql_endpoint`` and
    ``access_token`` attributes (typically populated from Langflow inputs).
    """

    graphql_endpoint: str
    access_token: str

    # ------------------------------------------------------------------
    # GraphQL transport
    # ------------------------------------------------------------------

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def _execute_graphql(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        *,
        timeout: int = 30,
    ) -> dict[str, Any]:
        """Execute a GraphQL query/mutation and return the ``data`` payload.

        Raises ``ValueError`` on HTTP or GraphQL-level errors.
        """
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables

        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(
                    self.graphql_endpoint,
                    headers=self._headers(),
                    json=payload,
                )
                response.raise_for_status()
                result = response.json()
        except httpx.HTTPError as exc:
            msg = f"DataHub GraphQL request failed: {exc}"
            raise ValueError(msg) from exc

        if "errors" in result:
            errors = result["errors"]
            msg = f"DataHub GraphQL errors: {errors}"
            raise ValueError(msg)

        return result.get("data", {})
