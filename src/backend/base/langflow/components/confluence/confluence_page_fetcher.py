import base64

import httpx

from langflow.custom import Component
from langflow.io import BoolInput, IntInput, Output, SecretStrInput, StrInput
from langflow.schema import Data


class ConfluencePageFetcherComponent(Component):
    """Fetch a Confluence page by ID with optional child pages and attachments.

    Returns a ``list[Data]`` where the first item is the requested page.
    When *include_children* is enabled, direct child pages are appended.
    When *include_attachments* is enabled, attachment metadata records are
    appended after the child pages.
    """

    display_name = "Confluence Page Fetcher"
    description = (
        "Fetch a specific Confluence page by its ID. "
        "Optionally include child pages and attachment metadata."
    )
    documentation = (
        "https://developer.atlassian.com/cloud/confluence/rest/v1/"
        "api-group-content/#api-rest-api-content-id-get"
    )
    trace_type = "tool"
    icon = "Confluence"
    name = "ConfluencePageFetcher"

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
            name="page_id",
            display_name="Page ID",
            required=True,
            info="The numeric ID of the Confluence page to fetch.",
        ),
        BoolInput(
            name="include_children",
            display_name="Include Child Pages",
            value=False,
            advanced=True,
            info="Include direct child pages in the output.",
        ),
        BoolInput(
            name="include_attachments",
            display_name="Include Attachments",
            value=False,
            advanced=True,
            info="Include attachment metadata records for the page.",
        ),
        IntInput(
            name="max_children",
            display_name="Max Child Pages",
            value=20,
            advanced=True,
            info="Maximum number of child pages to retrieve (1-50).",
        ),
    ]

    outputs = [
        Output(name="data", display_name="Data", method="fetch_page"),
    ]

    _api_base: str = ""

    def fetch_page(self) -> list[Data]:
        self._api_base = self.url.rstrip("/")
        try:
            with httpx.Client(timeout=20) as client:
                headers = self._auth_headers()
                pages = self._collect_results(client, headers=headers)
                self.status = pages
                return pages
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to fetch Confluence page with the provided configuration."
            raise ValueError(msg) from exc

    def _auth_headers(self) -> dict[str, str]:
        credentials = base64.b64encode(f"{self.username}:{self.api_key}".encode()).decode()
        return {"Authorization": f"Basic {credentials}", "Accept": "application/json"}

    def _collect_results(self, client: httpx.Client, *, headers: dict) -> list[Data]:
        results: list[Data] = [self._get_page(client, headers=headers, page_id=self.page_id)]
        if self.include_children:
            results.extend(self._get_children(client, headers=headers, page_id=self.page_id))
        if self.include_attachments:
            results.extend(self._get_attachments(client, headers=headers, page_id=self.page_id))
        return results

    def _get_page(self, client: httpx.Client, *, headers: dict, page_id: str) -> Data:
        endpoint = f"{self._api_base}/rest/api/content/{page_id}"
        params = {"expand": "body.storage,metadata.labels,space,ancestors,version"}
        try:
            response = client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return self._item_to_data(response.json())
        except (httpx.HTTPError, ValueError) as exc:
            msg = f"Unable to fetch Confluence page {page_id}."
            raise ValueError(msg) from exc

    def _get_children(self, client: httpx.Client, *, headers: dict, page_id: str) -> list[Data]:
        limit = max(1, min(int(self.max_children or 20), 50))
        endpoint = f"{self._api_base}/rest/api/content/{page_id}/child/page"
        params = {"limit": limit, "expand": "body.storage,metadata.labels,space,ancestors,version"}
        try:
            response = client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return [self._item_to_data(item) for item in response.json().get("results", [])]
        except httpx.HTTPError:
            return []

    def _get_attachments(self, client: httpx.Client, *, headers: dict, page_id: str) -> list[Data]:
        endpoint = f"{self._api_base}/rest/api/content/{page_id}/child/attachment"
        params = {"expand": "metadata"}
        try:
            response = client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return [self._attachment_to_data(item) for item in response.json().get("results", [])]
        except httpx.HTTPError:
            return []

    @staticmethod
    def _item_to_data(item: dict) -> Data:
        body = item.get("body", {}).get("storage", {}).get("value", "")
        labels = [
            lb.get("name", "")
            for lb in item.get("metadata", {}).get("labels", {}).get("results", [])
        ]
        space = item.get("space", {})
        ancestors = [a.get("title", "") for a in item.get("ancestors", [])]
        version = item.get("version", {})
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
            "version_number": version.get("number"),
            "last_modified": version.get("when"),
            "author": version.get("by", {}).get("displayName"),
        }
        return Data(text=body, data=metadata)

    @staticmethod
    def _attachment_to_data(item: dict) -> Data:
        metadata = {
            "source": "confluence",
            "attachment_id": item.get("id"),
            "title": item.get("title"),
            "type": "attachment",
            "media_type": item.get("metadata", {}).get("mediaType", ""),
            "file_size": item.get("extensions", {}).get("fileSize"),
            "web_url": item.get("_links", {}).get("webui"),
            "download_url": item.get("_links", {}).get("download"),
        }
        return Data(text=f"[Attachment] {item.get('title', '')}", data=metadata)
