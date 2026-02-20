from collections import deque
from pathlib import Path

import httpx

from langflow.custom import Component
from langflow.io import BoolInput, IntInput, Output, SecretStrInput, StrInput
from langflow.schema import Data


class SharePointFilesLoaderComponent(Component):
    display_name = "SharePoint Files Loader"
    description = "Loads files from SharePoint document libraries using Microsoft Graph."
    documentation = "https://learn.microsoft.com/graph/api/resources/sharepoint"
    icon = "Microsoft"
    name = "SharePointFilesLoader"

    inputs = [
        StrInput(name="tenant_id", display_name="Tenant ID", required=True),
        StrInput(name="client_id", display_name="Client ID", required=True),
        SecretStrInput(name="client_secret", display_name="Client Secret", required=True),
        StrInput(name="site_hostname", display_name="Site Hostname", value="contoso.sharepoint.com", required=True),
        StrInput(name="site_path", display_name="Site Path", value="/sites/FinanceOps", required=True),
        StrInput(name="library_name", display_name="Library Name", value="Documents", required=True),
        StrInput(name="folder_path", display_name="Folder Path", value="", required=False),
        BoolInput(name="recursive", display_name="Recursive", value=True, required=False),
        IntInput(name="max_files", display_name="Max Files", value=50, required=False),
        StrInput(
            name="file_types",
            display_name="File Types",
            value=".txt,.md,.json,.csv",
            required=False,
            info="Comma-separated file extensions to include. Leave blank for all file types.",
        ),
    ]

    outputs = [Output(name="data", display_name="Data", method="load_documents")]

    graph_base_url = "https://graph.microsoft.com/v1.0"
    token_scope = "https://graph.microsoft.com/.default"

    def load_documents(self) -> list[Data]:
        try:
            with httpx.Client(timeout=20) as client:
                token = self._get_access_token(client)
                headers = {"Authorization": f"Bearer {token}"}
                site_id = self._get_site_id(client, headers=headers)
                drive_id = self._get_drive_id(client, site_id=site_id, headers=headers)
                files = self._list_files(client, drive_id=drive_id, headers=headers)

                data = [
                    self._build_data(client, drive_id=drive_id, item=file_item, headers=headers) for file_item in files
                ]
                self.status = data
                return data
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to load SharePoint files with the provided configuration."
            raise ValueError(msg) from exc

    def _get_access_token(self, client: httpx.Client) -> str:
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.token_scope,
        }
        try:
            response = client.post(token_url, data=payload)
            response.raise_for_status()
            token = response.json().get("access_token")
            if not token:
                msg = "Unable to authenticate with SharePoint."
                raise ValueError(msg)
            return token
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to authenticate with SharePoint. Verify tenant and client credentials."
            raise ValueError(msg) from exc

    def _get_site_id(self, client: httpx.Client, *, headers: dict[str, str]) -> str:
        endpoint = f"{self.graph_base_url}/sites/{self.site_hostname}:{self.site_path}"
        try:
            response = client.get(endpoint, headers=headers)
            response.raise_for_status()
            site_id = response.json().get("id")
            if not site_id:
                msg = "SharePoint site not found."
                raise ValueError(msg)
            return site_id
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to resolve SharePoint site."
            raise ValueError(msg) from exc

    def _get_drive_id(self, client: httpx.Client, *, site_id: str, headers: dict[str, str]) -> str:
        endpoint = f"{self.graph_base_url}/sites/{site_id}/drives"
        try:
            response = client.get(endpoint, headers=headers)
            response.raise_for_status()
            drives = response.json().get("value", [])
            for drive in drives:
                if drive.get("name", "").lower() == self.library_name.lower():
                    drive_id = drive.get("id")
                    if drive_id:
                        return drive_id
            msg = "SharePoint library not found."
            raise ValueError(msg)
        except (httpx.HTTPError, ValueError) as exc:
            msg = "Unable to resolve SharePoint document library."
            raise ValueError(msg) from exc

    def _list_files(self, client: httpx.Client, *, drive_id: str, headers: dict[str, str]) -> list[dict]:
        folder_path = self.folder_path.strip("/")
        max_files = self._max_files_limit(self.max_files)
        root_endpoint = (
            f"{self.graph_base_url}/drives/{drive_id}/root:/{folder_path}:/children"
            if folder_path
            else f"{self.graph_base_url}/drives/{drive_id}/root/children"
        )
        queue = deque([root_endpoint])
        files: list[dict] = []

        while queue and len(files) < max_files:
            endpoint = queue.popleft()
            response = client.get(endpoint, headers=headers)
            response.raise_for_status()
            payload = response.json()

            for item in payload.get("value", []):
                if "folder" in item and self.recursive:
                    queue.append(f"{self.graph_base_url}/drives/{drive_id}/items/{item['id']}/children")
                    continue
                if "file" not in item:
                    continue
                if not self._is_allowed_file(item.get("name", "")):
                    continue
                files.append(item)
                if len(files) >= max_files:
                    break

            next_link = payload.get("@odata.nextLink")
            if next_link:
                queue.append(next_link)
        return files

    def _is_allowed_file(self, filename: str) -> bool:
        file_types = self._normalized_file_types(self.file_types)
        if not file_types:
            return True
        return Path(filename).suffix.lower() in file_types

    @staticmethod
    def _normalized_file_types(file_types: str | None) -> set[str]:
        if not file_types:
            return set()
        return {item.strip().lower() for item in file_types.split(",") if item.strip()}

    @staticmethod
    def _max_files_limit(max_files: int | None) -> int:
        return max(1, int(max_files or 50))

    def _build_data(self, client: httpx.Client, *, drive_id: str, item: dict, headers: dict[str, str]) -> Data:
        metadata = {
            "source": "sharepoint",
            "file_name": item.get("name"),
            "web_url": item.get("webUrl"),
            "site_id": item.get("parentReference", {}).get("siteId"),
            "drive_id": drive_id,
            "item_id": item.get("id"),
            "last_modified": item.get("lastModifiedDateTime"),
            "mime_type": item.get("file", {}).get("mimeType"),
        }
        content = self._read_content(client, drive_id=drive_id, item_id=item.get("id"), headers=headers)
        return Data(text=content, data=metadata)

    def _read_content(self, client: httpx.Client, *, drive_id: str, item_id: str | None, headers: dict[str, str]) -> str:
        if not item_id:
            return ""
        endpoint = f"{self.graph_base_url}/drives/{drive_id}/items/{item_id}/content"
        try:
            response = client.get(endpoint, headers=headers)
            response.raise_for_status()
            return self._decode_content(response.content)
        except httpx.HTTPError:
            return ""

    @staticmethod
    def _decode_content(content: bytes) -> str:
        return content.decode("utf-8", errors="ignore")
