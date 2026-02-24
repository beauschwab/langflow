from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.confluence import ConfluencePageFetcherComponent


class _DummyClient:
    def __init__(self):
        self.get = MagicMock()
        self.post = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _make_page(page_id="42", title="My Page", body="<p>Content</p>"):
    return {
        "id": page_id,
        "title": title,
        "type": "page",
        "status": "current",
        "space": {"key": "DOCS", "name": "Documentation"},
        "ancestors": [{"title": "Parent"}],
        "metadata": {"labels": {"results": [{"name": "draft"}]}},
        "body": {"storage": {"value": body}},
        "version": {"number": 3, "when": "2026-01-01T00:00:00Z", "by": {"displayName": "Alice"}},
        "_links": {"webui": "/pages/42"},
    }


def _make_attachment(att_id="a1", title="diagram.png"):
    return {
        "id": att_id,
        "title": title,
        "metadata": {"mediaType": "image/png"},
        "extensions": {"fileSize": 4096},
        "_links": {"webui": "/att/a1", "download": "/download/a1"},
    }


# ---------------------------------------------------------------------------
# fetch_page
# ---------------------------------------------------------------------------


def test_fetch_page_returns_single_data(monkeypatch):
    component = ConfluencePageFetcherComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        page_id="42",
        include_children=False,
        include_attachments=False,
    )

    dummy_client = _DummyClient()
    page_resp = MagicMock()
    page_resp.json.return_value = _make_page()
    page_resp.raise_for_status = MagicMock()
    dummy_client.get.return_value = page_resp

    monkeypatch.setattr(
        "langflow.components.confluence.confluence_page_fetcher.httpx.Client",
        lambda **_: dummy_client,
    )

    results = component.fetch_page()

    assert len(results) == 1
    assert results[0].text == "<p>Content</p>"
    assert results[0].data["page_id"] == "42"
    assert results[0].data["source"] == "confluence"
    assert results[0].data["version_number"] == 3
    assert results[0].data["author"] == "Alice"
    assert results[0].data["labels"] == ["draft"]
    assert results[0].data["ancestors"] == ["Parent"]


def test_fetch_page_with_children(monkeypatch):
    component = ConfluencePageFetcherComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        page_id="42",
        include_children=True,
        include_attachments=False,
        max_children=5,
    )

    page_resp = MagicMock()
    page_resp.raise_for_status = MagicMock()
    children_resp = MagicMock()
    children_resp.raise_for_status = MagicMock()

    page_resp.json.return_value = _make_page("42", "Parent")
    child_item = _make_page("43", "Child Page", "<p>Child</p>")
    children_resp.json.return_value = {"results": [child_item]}

    call_count = {"n": 0}

    def _get(url, **_kwargs):
        call_count["n"] += 1
        if "child/page" in url:
            return children_resp
        return page_resp

    dummy_client = _DummyClient()
    dummy_client.get.side_effect = _get

    monkeypatch.setattr(
        "langflow.components.confluence.confluence_page_fetcher.httpx.Client",
        lambda **_: dummy_client,
    )

    results = component.fetch_page()

    assert len(results) == 2
    assert results[1].data["page_id"] == "43"
    assert results[1].text == "<p>Child</p>"


def test_fetch_page_with_attachments(monkeypatch):
    component = ConfluencePageFetcherComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        page_id="42",
        include_children=False,
        include_attachments=True,
    )

    page_resp = MagicMock()
    page_resp.raise_for_status = MagicMock()
    page_resp.json.return_value = _make_page()

    att_resp = MagicMock()
    att_resp.raise_for_status = MagicMock()
    att_resp.json.return_value = {"results": [_make_attachment()]}

    def _get(url, **_kwargs):
        if "attachment" in url:
            return att_resp
        return page_resp

    dummy_client = _DummyClient()
    dummy_client.get.side_effect = _get

    monkeypatch.setattr(
        "langflow.components.confluence.confluence_page_fetcher.httpx.Client",
        lambda **_: dummy_client,
    )

    results = component.fetch_page()

    assert len(results) == 2
    att = results[1]
    assert att.data["type"] == "attachment"
    assert att.data["media_type"] == "image/png"
    assert att.data["file_size"] == 4096
    assert att.text == "[Attachment] diagram.png"


def test_fetch_page_raises_on_http_error(monkeypatch):
    component = ConfluencePageFetcherComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        page_id="99",
    )

    dummy_client = _DummyClient()
    dummy_client.get.side_effect = httpx.HTTPError("not found")

    monkeypatch.setattr(
        "langflow.components.confluence.confluence_page_fetcher.httpx.Client",
        lambda **_: dummy_client,
    )

    with pytest.raises(ValueError, match="Unable to fetch Confluence page"):
        component.fetch_page()


def test_children_http_error_returns_empty(monkeypatch):
    component = ConfluencePageFetcherComponent(
        url="https://example.atlassian.net/wiki",
        username="user@example.com",
        api_key="key",
        page_id="42",
        include_children=True,
        include_attachments=False,
    )

    page_resp = MagicMock()
    page_resp.raise_for_status = MagicMock()
    page_resp.json.return_value = _make_page()

    def _get(url, **_kwargs):
        if "child/page" in url:
            raise httpx.HTTPError("forbidden")
        return page_resp

    dummy_client = _DummyClient()
    dummy_client.get.side_effect = _get

    monkeypatch.setattr(
        "langflow.components.confluence.confluence_page_fetcher.httpx.Client",
        lambda **_: dummy_client,
    )

    # Children error is swallowed; only the main page is returned
    results = component.fetch_page()
    assert len(results) == 1


# ---------------------------------------------------------------------------
# frontend node defaults
# ---------------------------------------------------------------------------


def test_confluence_page_fetcher_defaults():
    component = ConfluencePageFetcherComponent()
    node = component.to_frontend_node()["data"]["node"]

    assert node["display_name"] == "Confluence Page Fetcher"
    assert "page_id" in node["template"]
