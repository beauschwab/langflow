"""Tests for PowerBIDAXQueryComponent."""
from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.power_bi import PowerBIDAXQueryComponent


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


def _dax_response(rows):
    resp = MagicMock()
    resp.json.return_value = {
        "results": [
            {"tables": [{"rows": rows}]}
        ]
    }
    resp.raise_for_status = MagicMock()
    return resp


def _make_component(**kwargs):
    defaults = {
        "tenant_id": "tenant-123",
        "client_id": "client-456",
        "client_secret": "secret",
        "workspace_id": "ws-111",
        "dataset_id": "ds-222",
        "dax_query": "EVALUATE VALUES('Date'[Year])",
        "include_nulls": True,
        "max_rows": 1000,
    }
    defaults.update(kwargs)
    return PowerBIDAXQueryComponent(**defaults)


# ---------------------------------------------------------------------------
# _parse_response
# ---------------------------------------------------------------------------


def test_parse_response_cleans_column_names():
    component = _make_component()
    rows = [{"[Date].[Year]": 2023, "[Sales].[Amount]": 1000}]
    result = component._parse_response({"results": [{"tables": [{"rows": rows}]}]})
    assert result == [{"Year": 2023, "Amount": 1000}]


def test_parse_response_respects_max_rows():
    component = _make_component(max_rows=2)
    rows = [{"[A]": i} for i in range(10)]
    result = component._parse_response({"results": [{"tables": [{"rows": rows}]}]})
    assert len(result) == 2


def test_parse_response_empty_result():
    component = _make_component()
    result = component._parse_response({"results": []})
    assert result == []


def test_parse_response_multiple_tables():
    component = _make_component()
    payload = {
        "results": [
            {
                "tables": [
                    {"rows": [{"[A]": 1}]},
                    {"rows": [{"[B]": 2}]},
                ]
            }
        ]
    }
    result = component._parse_response(payload)
    assert len(result) == 2
    assert result[0] == {"A": 1}
    assert result[1] == {"B": 2}


# ---------------------------------------------------------------------------
# run_dax_query integration (mocked HTTP)
# ---------------------------------------------------------------------------


def test_run_dax_query_returns_data(monkeypatch):
    component = _make_component()
    dummy = _DummyClient()
    dummy.post.side_effect = [
        _token_response(),
        _dax_response([{"[Date].[Year]": 2024, "[Sales].[Total]": 500}]),
    ]

    monkeypatch.setattr(
        "langflow.components.power_bi.power_bi_dax_query.httpx.Client",
        lambda **_: dummy,
    )

    results = component.run_dax_query()
    assert len(results) == 1
    assert results[0].data["Year"] == 2024
    assert results[0].data["Total"] == 500


def test_run_dax_query_auth_failure(monkeypatch):
    component = _make_component()
    dummy = _DummyClient()
    dummy.post.side_effect = httpx.HTTPError("auth error")

    monkeypatch.setattr(
        "langflow.components.power_bi.power_bi_dax_query.httpx.Client",
        lambda **_: dummy,
    )

    with pytest.raises(ValueError, match="Power BI DAX query failed"):
        component.run_dax_query()


def test_run_dax_query_no_token(monkeypatch):
    component = _make_component()
    dummy = _DummyClient()
    token_resp = MagicMock()
    token_resp.json.return_value = {}
    token_resp.raise_for_status = MagicMock()
    dummy.post.return_value = token_resp

    monkeypatch.setattr(
        "langflow.components.power_bi.power_bi_dax_query.httpx.Client",
        lambda **_: dummy,
    )

    with pytest.raises(ValueError, match="Power BI DAX query failed"):
        component.run_dax_query()


def test_run_dax_query_api_failure(monkeypatch):
    component = _make_component()
    dummy = _DummyClient()
    dummy.post.side_effect = [
        _token_response(),
        MagicMock(raise_for_status=MagicMock(side_effect=httpx.HTTPError("500"))),
    ]

    monkeypatch.setattr(
        "langflow.components.power_bi.power_bi_dax_query.httpx.Client",
        lambda **_: dummy,
    )

    with pytest.raises(ValueError, match="Power BI DAX query failed"):
        component.run_dax_query()


# ---------------------------------------------------------------------------
# Frontend node defaults
# ---------------------------------------------------------------------------


def test_dax_query_component_defaults():
    component = PowerBIDAXQueryComponent()
    node = component.to_frontend_node()["data"]["node"]

    assert node["display_name"] == "Power BI DAX Query"
    assert "tenant_id" in node["template"]
    assert "client_id" in node["template"]
    assert "client_secret" in node["template"]
    assert "workspace_id" in node["template"]
    assert "dataset_id" in node["template"]
    assert "dax_query" in node["template"]
    assert node["template"]["max_rows"]["value"] == 1000
    assert node["template"]["include_nulls"]["value"] is True
