from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.microsoft_outlook import OutlookSendEmailComponent
from langflow.components.microsoft_templates.registry import (
    get_outlook_template_names,
    get_template,
    render_template,
)


class _DummyClient:
    def __init__(self):
        self.get = MagicMock()
        self.post = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_send_email_returns_data(monkeypatch):
    component = OutlookSendEmailComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        sender_email="sender@contoso.com",
        recipient_emails="user@contoso.com",
        subject="Weekly Report",
        body="<h1>Report</h1>",
        body_content_type="HTML",
        template_name="None",
        field_mapping="",
        require_approval=False,
        cc_emails="",
        importance="normal",
    )

    dummy_client = _DummyClient()
    monkeypatch.setattr(
        "langflow.components.microsoft_outlook.outlook.httpx.Client",
        lambda **_: dummy_client,
    )
    monkeypatch.setattr(component, "_get_access_token", lambda *_: "token")

    send_response = MagicMock()
    send_response.raise_for_status = MagicMock()
    dummy_client.post.return_value = send_response

    result = component.send_email()

    assert result.data["source"] == "outlook"
    assert result.data["action"] == "send"
    assert result.data["status"] == "sent"
    assert result.text == "Email sent successfully."


def test_create_draft_returns_data(monkeypatch):
    component = OutlookSendEmailComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        sender_email="sender@contoso.com",
        recipient_emails="user@contoso.com",
        subject="Pending Report",
        body="<p>Needs review</p>",
        body_content_type="HTML",
        template_name="None",
        field_mapping="",
        require_approval=True,
        cc_emails="",
        importance="normal",
    )

    dummy_client = _DummyClient()
    monkeypatch.setattr(
        "langflow.components.microsoft_outlook.outlook.httpx.Client",
        lambda **_: dummy_client,
    )
    monkeypatch.setattr(component, "_get_access_token", lambda *_: "token")

    draft_response = MagicMock()
    draft_response.raise_for_status = MagicMock()
    draft_response.json.return_value = {"id": "draft-123", "webLink": "https://outlook.office.com/draft/123"}
    dummy_client.post.return_value = draft_response

    result = component.send_email()

    assert result.data["source"] == "outlook"
    assert result.data["action"] == "draft"
    assert result.data["status"] == "pending_review"
    assert result.data["draft_id"] == "draft-123"
    assert "draft-123" in result.text


def test_build_message_payload_with_cc():
    component = OutlookSendEmailComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        sender_email="sender@contoso.com",
        recipient_emails="a@contoso.com, b@contoso.com",
        subject="Report",
        body="body",
        body_content_type="Text",
        template_name="None",
        field_mapping="",
        require_approval=False,
        cc_emails="cc@contoso.com",
        importance="high",
    )

    payload = component._build_message_payload("body")

    assert len(payload["toRecipients"]) == 2
    assert payload["toRecipients"][0]["emailAddress"]["address"] == "a@contoso.com"
    assert len(payload["ccRecipients"]) == 1
    assert payload["importance"] == "high"


def test_get_access_token_sanitizes_errors():
    component = OutlookSendEmailComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
    )
    client = MagicMock()
    client.post.side_effect = httpx.HTTPError("provider-specific details")

    with pytest.raises(ValueError) as exc_info:
        component._get_access_token(client)
    assert str(exc_info.value) == "Unable to authenticate with Microsoft. Verify tenant and client credentials."


# ---------------------------------------------------------------------------
# Template tests
# ---------------------------------------------------------------------------


def test_outlook_template_names_available():
    names = get_outlook_template_names()
    assert len(names) >= 3
    assert "Executive Summary Report" in names
    assert "Status Update Email" in names
    assert "Alert / Notification Email" in names


def test_render_executive_summary_template():
    result = render_template(
        "Executive Summary Report",
        {"title": "Q4 Review", "summary": "Revenue grew 15%", "metrics": "ARR $10M", "action_items": "Hire 5"},
    )
    assert "Q4 Review" in result
    assert "Revenue grew 15%" in result
    assert "ARR $10M" in result
    assert "<div" in result  # HTML output


def test_render_template_unknown_raises():
    with pytest.raises(ValueError, match="not found"):
        render_template("Nonexistent Template", {})


def test_template_fields_exposed():
    tpl = get_template("Executive Summary Report")
    assert tpl is not None
    assert "title" in tpl["fields"]
    assert "summary" in tpl["fields"]


def test_parse_field_mapping():
    raw = "title: My Report\nsummary: All good\nmetrics: Revenue: $5M, Users: 1K"
    result = OutlookSendEmailComponent._parse_field_mapping_str(raw)
    assert result["title"] == "My Report"
    assert result["summary"] == "All good"
    assert result["metrics"] == "Revenue: $5M, Users: 1K"


def test_send_email_with_template(monkeypatch):
    component = OutlookSendEmailComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        sender_email="sender@contoso.com",
        recipient_emails="user@contoso.com",
        subject="Weekly Report",
        body="ignored",
        body_content_type="Text",
        template_name="Executive Summary Report",
        field_mapping="title: Weekly Report\nsummary: All targets met",
        require_approval=False,
        cc_emails="",
        importance="normal",
    )

    dummy_client = _DummyClient()
    monkeypatch.setattr(
        "langflow.components.microsoft_outlook.outlook.httpx.Client",
        lambda **_: dummy_client,
    )
    monkeypatch.setattr(component, "_get_access_token", lambda *_: "token")

    send_response = MagicMock()
    send_response.raise_for_status = MagicMock()
    dummy_client.post.return_value = send_response

    result = component.send_email()

    assert result.data["template"] == "Executive Summary Report"
    assert result.data["content_blocks"] is not None
    assert len(result.data["content_blocks"]) == 2  # header + template preview

    # Verify the sent payload used HTML content type (forced by template)
    call_args = dummy_client.post.call_args
    sent_json = call_args.kwargs.get("json") or call_args[1].get("json")
    assert sent_json["message"]["body"]["contentType"] == "HTML"


def test_content_blocks_without_template(monkeypatch):
    component = OutlookSendEmailComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        sender_email="sender@contoso.com",
        recipient_emails="user@contoso.com",
        subject="Plain",
        body="Hello",
        body_content_type="Text",
        template_name="None",
        field_mapping="",
        require_approval=False,
        cc_emails="",
        importance="normal",
    )

    dummy_client = _DummyClient()
    monkeypatch.setattr(
        "langflow.components.microsoft_outlook.outlook.httpx.Client",
        lambda **_: dummy_client,
    )
    monkeypatch.setattr(component, "_get_access_token", lambda *_: "token")

    send_response = MagicMock()
    send_response.raise_for_status = MagicMock()
    dummy_client.post.return_value = send_response

    result = component.send_email()

    assert result.data["template"] is None
    assert len(result.data["content_blocks"]) == 1  # header only, no template preview
