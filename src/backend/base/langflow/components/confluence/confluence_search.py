import base64

import httpx

from langflow.custom import Component
from langflow.io import BoolInput, DropdownInput, IntInput, Output, SecretStrInput, StrInput
from langflow.schema import Data


class ConfluenceSearchComponent(Component):
    """Search Confluence content using CQL (Confluence Query Language).

    Supports either a raw CQL expression or structured filters that are
    composed into a CQL query automatically.  Results are returned as a
    ``list[Data]`` where each item carries the page body and rich metadata.
    """

    display_name = "Confluence Search"
    description = (
        "Search Confluence pages and blog posts using CQL (Confluence Query Language) "
        "or structured filters for space, label, type, and title."
    )
    documentation = (
        "https://developer.atlassian.com/cloud/confluence/rest/v1/"
        "api-group-content/#api-rest-api-content-search-get"
    )
    trace_type = "tool"
    icon = "Confluence"
    name = "ConfluenceSearch"

    inputs = [
        StrInput(
            name="url",
            display_name="Site URL",
            required=True,
            info="The base URL of your Confluence instance. Example: https://<company>.atlassian.net/wiki.",
        ),
        StrInput(
            name="username",
            display_name="Username",
            required=True,
            info="Atlassian user e-mail. Example: email@example.com",
        ),
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            required=True,
            info="Atlassian API token. Create at: https://id.atlassian.com/manage-profile/security/api-tokens",
        ),
        StrInput(
            name="cql_query",
            display_name="CQL Query",
            required=False,
            value="",
            info=(
                "Confluence Query Language expression. When provided, the structured filters below are ignored. "
                'Example: space = "PROJ" AND label = "release-notes" AND type = page'
            ),
        ),
        DropdownInput(
            name="content_type",
            display_name="Content Type",
            options=["page", "blogpost", "any"],
            value="page",
            info="Filter results by content type. Used only when CQL Query is empty.",
        ),
        StrInput(
            name="space_key",
            display_name="Space Key",
            required=False,
            value="",
            info="Restrict search to a specific space key. Leave empty to search all spaces.",
        ),
        StrInput(
            name="label",
            display_name="Label",
            required=False,
            value="",
            info="Filter results by a Confluence label/tag.",
        ),
        StrInput(
            name="title_contains",
            display_name="Title Contains",
            required=False,
            value="",
            info="Restrict to pages whose title contains this text.",
        ),
        IntInput(
            name="max_results",
            display_name="Max Results",
            value=25,
            advanced=True,
            info="Maximum number of results to return (1-50).",
        ),
        BoolInput(
            name="include_archived",
            display_name="Include Archived",
            value=False,
            advanced=True,
            info="Include archived content in search results.",
        ),
    ]

    outputs = [
        Output(name="data", display_name="Data", method="search_content"),
    ]

    _api_base: str = ""

    def search_content(self) -> list[Data]:
        self._api_base = self.url.rstrip("/")
        cql = self._build_cql()
        try:
            with httpx.Client(timeout=20) as client:
                headers = self._auth_headers()
                results = self._execute_search(client, headers=headers, cql=cql)
                data = [self._item_to_data(item) for item in results]
                self.status = data
                return data
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to search Confluence with the provided configuration."
            raise ValueError(msg) from exc

    def _build_cql(self) -> str:
        """Return the CQL string to use for the search request.

        If *cql_query* is set it is returned verbatim.  Otherwise the
        structured filter inputs are composed into a CQL expression.
        """
        if self.cql_query and self.cql_query.strip():
            return self.cql_query.strip()

        clauses: list[str] = []
        if self.content_type and self.content_type != "any":
            clauses.append(f'type = "{self.content_type}"')
        if self.space_key and self.space_key.strip():
            clauses.append(f'space = "{self.space_key.strip()}"')
        if self.label and self.label.strip():
            clauses.append(f'label = "{self.label.strip()}"')
        if self.title_contains and self.title_contains.strip():
            clauses.append(f'title ~ "{self.title_contains.strip()}"')
        if not self.include_archived:
            clauses.append('status = "current"')

        return " AND ".join(clauses) if clauses else 'type = "page"'

    def _auth_headers(self) -> dict[str, str]:
        credentials = base64.b64encode(f"{self.username}:{self.api_key}".encode()).decode()
        return {"Authorization": f"Basic {credentials}", "Accept": "application/json"}

    def _execute_search(self, client: httpx.Client, *, headers: dict, cql: str) -> list[dict]:
        limit = max(1, min(int(self.max_results or 25), 50))
        params: dict = {
            "cql": cql,
            "limit": limit,
            "expand": "body.storage,metadata.labels,space,ancestors",
        }
        endpoint = f"{self._api_base}/rest/api/content/search"
        try:
            response = client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get("results", [])
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Confluence search request failed."
            raise ValueError(msg) from exc

    @staticmethod
    def _item_to_data(item: dict) -> Data:
        body = item.get("body", {}).get("storage", {}).get("value", "")
        labels = [
            lb.get("name", "")
            for lb in item.get("metadata", {}).get("labels", {}).get("results", [])
        ]
        space = item.get("space", {})
        ancestors = [a.get("title", "") for a in item.get("ancestors", [])]
        metadata = {
            "source": "confluence",
            "page_id": item.get("id"),
            "title": item.get("title"),
            "type": item.get("type"),
            "status": item.get("status"),
            "space_key": space.get("key"),
            "space_name": space.get("name"),
            "web_url": item.get("_links", {}).get("webui"),
            "labels": labels,
            "ancestors": ancestors,
        }
        return Data(text=body, data=metadata)
