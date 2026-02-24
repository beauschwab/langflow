from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.confluence import ConfluenceSearchComponent


class _DummyClient:
    def __init__(self):
        self.get = MagicMock()
        self.post = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


# ---------------------------------------------------------------------------
# _build_cql
# ---------------------------------------------------------------------------


def test_build_cql_raw_query_takes_precedence():
    component = ConfluenceSearchComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        cql_query='space = "PROJ"',
        content_type="page",
        space_key="OTHER",
    )
    assert component._build_cql() == 'space = "PROJ"'


def test_build_cql_structured_type_and_space():
    component = ConfluenceSearchComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        cql_query="",
        content_type="page",
        space_key="PROJ",
        label="",
        title_contains="",
        include_archived=False,
    )
    cql = component._build_cql()
    assert 'type = "page"' in cql
    assert 'space = "PROJ"' in cql
    assert 'status = "current"' in cql


def test_build_cql_blogpost_with_label():
    component = ConfluenceSearchComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        cql_query="",
        content_type="blogpost",
        space_key="",
        label="release-notes",
        title_contains="",
        include_archived=False,
    )
    cql = component._build_cql()
    assert 'type = "blogpost"' in cql
    assert 'label = "release-notes"' in cql


def test_build_cql_title_contains():
    component = ConfluenceSearchComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        cql_query="",
        content_type="any",
        space_key="",
        label="",
        title_contains="design doc",
        include_archived=False,
    )
    cql = component._build_cql()
    assert 'title ~ "design doc"' in cql
    # "any" type should NOT add a type clause
    assert "type" not in cql


def test_build_cql_include_archived_omits_status_clause():
    component = ConfluenceSearchComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        cql_query="",
        content_type="page",
        space_key="",
        label="",
        title_contains="",
        include_archived=True,
    )
    cql = component._build_cql()
    assert "status" not in cql


def test_build_cql_no_filters_returns_default():
    component = ConfluenceSearchComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        cql_query="",
        content_type="any",
        space_key="",
        label="",
        title_contains="",
        include_archived=True,
    )
    cql = component._build_cql()
    assert cql == 'type = "page"'


# ---------------------------------------------------------------------------
# search_content
# ---------------------------------------------------------------------------


def _make_api_item(page_id="123", title="Test Page", body="<p>Hello</p>"):
    return {
        "id": page_id,
        "title": title,
        "type": "page",
        "status": "current",
        "space": {"key": "PROJ", "name": "Project"},
        "ancestors": [{"title": "Home"}],
        "metadata": {"labels": {"results": [{"name": "important"}]}},
        "body": {"storage": {"value": body}},
        "_links": {"webui": f"/pages/{page_id}"},
    }


def test_search_content_returns_data(monkeypatch):
    component = ConfluenceSearchComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        cql_query='space = "PROJ"',
        max_results=10,
    )

    dummy_client = _DummyClient()
    search_resp = MagicMock()
    search_resp.json.return_value = {"results": [_make_api_item()]}
    search_resp.raise_for_status = MagicMock()
    dummy_client.get.return_value = search_resp

    monkeypatch.setattr(
        "langflow.components.confluence.confluence_search.httpx.Client",
        lambda **_: dummy_client,
    )

    results = component.search_content()

    assert len(results) == 1
    assert results[0].text == "<p>Hello</p>"
    assert results[0].data["page_id"] == "123"
    assert results[0].data["space_key"] == "PROJ"
    assert results[0].data["labels"] == ["important"]
    assert results[0].data["ancestors"] == ["Home"]
    assert results[0].data["source"] == "confluence"


def test_search_content_raises_on_http_error(monkeypatch):
    component = ConfluenceSearchComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        cql_query='space = "PROJ"',
    )

    dummy_client = _DummyClient()
    dummy_client.get.side_effect = httpx.HTTPError("network error")
    monkeypatch.setattr(
        "langflow.components.confluence.confluence_search.httpx.Client",
        lambda **_: dummy_client,
    )

    with pytest.raises(ValueError, match="Unable to search Confluence"):
        component.search_content()


# ---------------------------------------------------------------------------
# frontend node defaults
# ---------------------------------------------------------------------------


def test_confluence_search_component_defaults():
    component = ConfluenceSearchComponent()
    node = component.to_frontend_node()["data"]["node"]

    assert node["display_name"] == "Confluence Search"
    assert "cql_query" in node["template"]
    assert "space_key" in node["template"]
    assert "label" in node["template"]
    assert "content_type" in node["template"]
    assert node["template"]["content_type"]["value"] == "page"
    assert node["template"]["max_results"]["value"] == 25
    assert node["template"]["include_archived"]["value"] is False
