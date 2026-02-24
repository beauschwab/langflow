from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.microsoft_teams import TeamsSendMessageComponent


class _DummyClient:
    def __init__(self):
        self.get = MagicMock()
        self.post = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_post_message_returns_data(monkeypatch):
    component = TeamsSendMessageComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        team_id="team-1",
        channel_id="channel-1",
        message="<p>Weekly Report</p>",
        content_type="html",
        require_approval=False,
        subject="",
        importance="normal",
    )

    dummy_client = _DummyClient()
    monkeypatch.setattr(
        "langflow.components.microsoft_teams.teams.httpx.Client",
        lambda **_: dummy_client,
    )
    monkeypatch.setattr(component, "_get_access_token", lambda *_: "token")

    post_response = MagicMock()
    post_response.raise_for_status = MagicMock()
    post_response.json.return_value = {"id": "msg-456", "webUrl": "https://teams.microsoft.com/msg/456"}
    dummy_client.post.return_value = post_response

    result = component.send_message()

    assert result.data["source"] == "teams"
    assert result.data["action"] == "post"
    assert result.data["status"] == "sent"
    assert result.data["message_id"] == "msg-456"
    assert "msg-456" in result.text


def test_preview_message_for_approval():
    component = TeamsSendMessageComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        team_id="team-1",
        channel_id="channel-1",
        message="<p>Needs review</p>",
        content_type="html",
        require_approval=True,
        subject="Report Review",
        importance="high",
    )

    payload = component._build_message_payload()
    result = component._preview_message(payload)

    assert result.data["source"] == "teams"
    assert result.data["action"] == "preview"
    assert result.data["status"] == "pending_review"
    assert result.data["subject"] == "Report Review"
    assert result.data["importance"] == "high"
    assert "approval" in result.text.lower()


def test_build_message_payload_with_subject():
    component = TeamsSendMessageComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        team_id="team-1",
        channel_id="channel-1",
        message="content",
        content_type="text",
        require_approval=False,
        subject="Meeting Summary",
        importance="normal",
    )

    payload = component._build_message_payload()

    assert payload["body"]["contentType"] == "text"
    assert payload["body"]["content"] == "content"
    assert payload["subject"] == "Meeting Summary"
    assert payload["importance"] == "normal"


def test_get_access_token_sanitizes_errors():
    component = TeamsSendMessageComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
    )
    client = MagicMock()
    client.post.side_effect = httpx.HTTPError("provider-specific details")

    with pytest.raises(ValueError) as exc_info:
        component._get_access_token(client)
    assert str(exc_info.value) == "Unable to authenticate with Microsoft. Verify tenant and client credentials."
