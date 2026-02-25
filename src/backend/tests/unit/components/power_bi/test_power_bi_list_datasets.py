"""Tests for PowerBIListDatasetsComponent."""
from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.power_bi import PowerBIListDatasetsComponent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _DummyClient:
    def __init__(self):
        self.get = MagicMock()
        self.post = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _token_response():
    resp = MagicMock()
    resp.json.return_value = {"access_token": "test-token"}
    resp.raise_for_status = MagicMock()
    return resp


def _datasets_response(datasets):
    resp = MagicMock()
    resp.json.return_value = {"value": datasets}
    resp.raise_for_status = MagicMock()
    return resp


def _make_component(**kwargs):
    defaults = {
        "tenant_id": "tenant-123",
        "client_id": "client-456",
        "client_secret": "secret",
        "workspace_id": "ws-111",
    }
    defaults.update(kwargs)
    return PowerBIListDatasetsComponent(**defaults)


# ---------------------------------------------------------------------------
# _dataset_to_data
# ---------------------------------------------------------------------------


def test_dataset_to_data_maps_fields():
    ds = {
        "id": "ds-1",
        "name": "Sales Model",
        "configuredBy": "admin@contoso.com",
        "isRefreshable": True,
        "webUrl": "https://app.powerbi.com/...",
        "createdDate": "2024-01-15T10:00:00Z",
    }
    data = PowerBIListDatasetsComponent._dataset_to_data(ds)
    assert data.text == "Sales Model"
    assert data.data["dataset_id"] == "ds-1"
    assert data.data["name"] == "Sales Model"
    assert data.data["configured_by"] == "admin@contoso.com"
    assert data.data["is_refreshable"] is True
    assert data.data["source"] == "power_bi"


def test_dataset_to_data_missing_optional_fields():
    ds = {"id": "ds-2", "name": "Empty"}
    data = PowerBIListDatasetsComponent._dataset_to_data(ds)
    assert data.data["dataset_id"] == "ds-2"
    assert data.data["web_url"] is None
    assert data.data["configured_by"] is None


# ---------------------------------------------------------------------------
# list_datasets integration (mocked HTTP)
# ---------------------------------------------------------------------------


def test_list_datasets_returns_data(monkeypatch):
    component = _make_component()
    dummy = _DummyClient()
    dummy.post.return_value = _token_response()
    dummy.get.return_value = _datasets_response(
        [
            {"id": "ds-1", "name": "Sales"},
            {"id": "ds-2", "name": "Finance"},
        ]
    )

    monkeypatch.setattr(
        "langflow.components.power_bi.power_bi_list_datasets.httpx.Client",
        lambda **_: dummy,
    )

    results = component.list_datasets()
    assert len(results) == 2
    assert results[0].data["dataset_id"] == "ds-1"
    assert results[1].data["name"] == "Finance"


def test_list_datasets_empty_workspace(monkeypatch):
    component = _make_component()
    dummy = _DummyClient()
    dummy.post.return_value = _token_response()
    dummy.get.return_value = _datasets_response([])

    monkeypatch.setattr(
        "langflow.components.power_bi.power_bi_list_datasets.httpx.Client",
        lambda **_: dummy,
    )

    results = component.list_datasets()
    assert results == []


def test_list_datasets_raises_on_http_error(monkeypatch):
    component = _make_component()
    dummy = _DummyClient()
    dummy.post.side_effect = httpx.HTTPError("network error")

    monkeypatch.setattr(
        "langflow.components.power_bi.power_bi_list_datasets.httpx.Client",
        lambda **_: dummy,
    )

    with pytest.raises(ValueError, match="Unable to list Power BI datasets"):
        component.list_datasets()


# ---------------------------------------------------------------------------
# Frontend node defaults
# ---------------------------------------------------------------------------


def test_list_datasets_component_defaults():
    component = PowerBIListDatasetsComponent()
    node = component.to_frontend_node()["data"]["node"]

    assert node["display_name"] == "Power BI List Datasets"
    assert "tenant_id" in node["template"]
    assert "workspace_id" in node["template"]
