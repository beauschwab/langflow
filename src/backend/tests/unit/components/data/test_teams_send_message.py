from unittest.mock import MagicMock

import httpx
import pytest

from langflow.components.microsoft_teams import TeamsSendMessageComponent
from langflow.components.microsoft_templates.registry import (
    get_teams_template_names,
    get_template,
    parse_field_mapping,
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


def test_post_message_returns_data(monkeypatch):
    component = TeamsSendMessageComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        team_id="team-1",
        channel_id="channel-1",
        message="<p>Weekly Report</p>",
        content_type="html",
        template_name="None",
        field_mapping="",
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
        template_name="None",
        field_mapping="",
        require_approval=True,
        subject="Report Review",
        importance="high",
    )

    payload = component._build_message_payload("<p>Needs review</p>")
    result = component._preview_message(payload, "<p>Needs review</p>")

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
        template_name="None",
        field_mapping="",
        require_approval=False,
        subject="Meeting Summary",
        importance="normal",
    )

    payload = component._build_message_payload("content")

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


# ---------------------------------------------------------------------------
# Template tests
# ---------------------------------------------------------------------------


def test_teams_template_names_available():
    names = get_teams_template_names()
    assert len(names) >= 3
    assert "Report Card" in names
    assert "Status Card" in names
    assert "Simple Message" in names


def test_render_report_card_template():
    result = render_template(
        "Report Card",
        {"title": "Sprint Review", "summary": "All tasks done", "facts": "Velocity: 42, Stories: 8"},
    )
    assert "Sprint Review" in result
    assert "AdaptiveCard" in result  # JSON Adaptive Card


def test_render_simple_message_template():
    result = render_template("Simple Message", {"title": "Hello", "body": "World"})
    assert "Hello" in result
    assert "World" in result
    assert "<h2>" in result


def test_adaptive_card_detection():
    card_json = '{"type": "AdaptiveCard", "version": "1.4"}'
    assert TeamsSendMessageComponent._is_adaptive_card(card_json) is True
    assert TeamsSendMessageComponent._is_adaptive_card("<p>Hello</p>") is False


def test_parse_field_mapping():
    raw = "title: Sprint Review\nsummary: All done\nfacts: Velocity: 42, Stories: 8"
    result = parse_field_mapping(raw)
    assert result["title"] == "Sprint Review"
    assert result["summary"] == "All done"
    assert result["facts"] == "Velocity: 42, Stories: 8"


def test_adaptive_card_payload_structure():
    component = TeamsSendMessageComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        team_id="team-1",
        channel_id="channel-1",
        message="ignored",
        content_type="html",
        template_name="None",
        field_mapping="",
        require_approval=False,
        subject="",
        importance="normal",
    )

    card_json = '{"type": "AdaptiveCard", "version": "1.4", "body": []}'
    payload = component._build_message_payload(card_json, is_adaptive_card=True)

    assert "attachments" in payload
    assert payload["attachments"][0]["contentType"] == "application/vnd.microsoft.card.adaptive"
    assert payload["attachments"][0]["content"]["type"] == "AdaptiveCard"


def test_send_message_with_template(monkeypatch):
    component = TeamsSendMessageComponent(
        tenant_id="tenant",
        client_id="client",
        client_secret="secret",
        team_id="team-1",
        channel_id="channel-1",
        message="ignored",
        content_type="html",
        template_name="Report Card",
        field_mapping="title: Sprint Review\nsummary: All tasks done\nfacts: Velocity: 42",
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
    post_response.json.return_value = {"id": "msg-789", "webUrl": "https://teams.microsoft.com/msg/789"}
    dummy_client.post.return_value = post_response

    result = component.send_message()

    assert result.data["template"] == "Report Card"
    assert result.data["content_blocks"] is not None
    assert len(result.data["content_blocks"]) == 2  # header + template preview

    # Verify adaptive card was sent as attachment
    call_args = dummy_client.post.call_args
    sent_json = call_args.kwargs.get("json") or call_args[1].get("json")
    assert "attachments" in sent_json
