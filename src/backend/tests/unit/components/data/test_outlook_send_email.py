from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.microsoft_outlook import OutlookSendEmailComponent


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
        require_approval=False,
        cc_emails="cc@contoso.com",
        importance="high",
    )

    payload = component._build_message_payload()

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
