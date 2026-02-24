from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.sharepoint import SharePointFilesLoaderComponent


class _DummyClient:
    def __init__(self):
        self.get = MagicMock()
        self.post = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_load_documents_returns_data(monkeypatch):
    component = SharePointFilesLoaderComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        site_hostname="contoso.sharepoint.com",
        site_path="/sites/FinanceOps",
        library_name="Documents",
        folder_path="",
        recursive=True,
        max_files=10,
        file_types=".txt",
    )

    dummy_client = _DummyClient()
    monkeypatch.setattr("langflow.components.sharepoint.sharepoint_files.httpx.Client", lambda **_: dummy_client)
    monkeypatch.setattr(component, "_get_access_token", lambda *_: "token")
    monkeypatch.setattr(component, "_get_site_id", lambda *_, **__: "site-id")
    monkeypatch.setattr(component, "_get_drive_id", lambda *_, **__: "drive-id")
    monkeypatch.setattr(
        component,
        "_list_files",
        lambda *_, **__: [
            {
                "id": "item-1",
                "name": "report.txt",
                "webUrl": "https://contoso.sharepoint.com/sites/FinanceOps/report.txt",
                "parentReference": {"siteId": "site-id"},
                "lastModifiedDateTime": "2026-02-20T00:00:00Z",
                "file": {"mimeType": "text/plain"},
            }
        ],
    )
    monkeypatch.setattr(component, "_read_content", lambda *_, **__: "report contents")

    result = component.load_documents()

    assert len(result) == 1
    assert result[0].text == "report contents"
    assert result[0].data["source"] == "sharepoint"
    assert result[0].data["drive_id"] == "drive-id"


def test_allowed_file_filter():
    component = SharePointFilesLoaderComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        file_types=".txt,.md",
    )
    assert component._is_allowed_file("notes.txt")
    assert component._is_allowed_file("README.MD")
    assert not component._is_allowed_file("photo.png")


def test_get_access_token_sanitizes_errors():
    component = SharePointFilesLoaderComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
    )
    client = MagicMock()
    client.post.side_effect = httpx.HTTPError("provider-specific details")

    with pytest.raises(ValueError) as exc_info:
        component._get_access_token(client)
    assert str(exc_info.value) == "Unable to authenticate with SharePoint. Verify tenant and client credentials."
