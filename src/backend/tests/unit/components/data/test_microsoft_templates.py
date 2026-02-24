"""Tests for the Microsoft template registry."""

import json

import pytest

from langflow.components.microsoft_templates.registry import (
    _parse_facts,
    get_outlook_template_names,
    get_teams_template_names,
    get_template,
    render_template,
)


# ---------------------------------------------------------------------------
# Registry API
# ---------------------------------------------------------------------------


def test_outlook_templates_registered():
    names = get_outlook_template_names()
    assert isinstance(names, list)
    assert len(names) >= 3


def test_teams_templates_registered():
    names = get_teams_template_names()
    assert isinstance(names, list)
    assert len(names) >= 3


def test_get_template_by_name():
    tpl = get_template("Executive Summary Report")
    assert tpl is not None
    assert tpl["platform"] == "outlook"
    assert "title" in tpl["fields"]


def test_get_template_unknown_returns_none():
    assert get_template("Does Not Exist") is None


def test_render_template_unknown_raises():
    with pytest.raises(ValueError, match="not found"):
        render_template("Does Not Exist", {})


# ---------------------------------------------------------------------------
# Outlook templates
# ---------------------------------------------------------------------------


def test_executive_summary_renders_html():
    html = render_template(
        "Executive Summary Report",
        {
            "title": "Q4 Review",
            "summary": "Revenue grew 15%",
            "metrics": "ARR $10M",
            "action_items": "Hire 5 engineers",
            "footer": "Finance Team",
        },
    )
    assert "Q4 Review" in html
    assert "Revenue grew 15%" in html
    assert "ARR $10M" in html
    assert "Hire 5 engineers" in html
    assert "Finance Team" in html
    assert "<div" in html


def test_status_update_renders_html():
    html = render_template(
        "Status Update Email",
        {
            "project_name": "Phoenix",
            "status": "On Track",
            "highlights": "Milestone 3 complete",
            "next_steps": "Begin QA",
        },
    )
    assert "Phoenix" in html
    assert "On Track" in html
    assert "Milestone 3 complete" in html


def test_alert_notification_renders_html():
    html = render_template(
        "Alert / Notification Email",
        {
            "alert_title": "CPU Spike",
            "severity": "high",
            "description": "CPU exceeded 95%",
            "impact": "Latency increase",
            "remediation": "Scale horizontally",
        },
    )
    assert "CPU Spike" in html
    assert "CPU exceeded 95%" in html
    assert "#da3b01" in html  # high severity color


def test_template_escapes_html():
    html = render_template(
        "Executive Summary Report",
        {"title": "<script>alert('xss')</script>"},
    )
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


# ---------------------------------------------------------------------------
# Teams templates
# ---------------------------------------------------------------------------


def test_report_card_renders_adaptive_card():
    rendered = render_template(
        "Report Card",
        {"title": "Sprint 42", "summary": "All green", "facts": "Velocity: 42, Stories: 8"},
    )
    card = json.loads(rendered)
    assert card["type"] == "AdaptiveCard"
    assert card["version"] == "1.4"
    assert any(b.get("text") == "Sprint 42" for b in card["body"])


def test_status_card_renders_adaptive_card():
    rendered = render_template(
        "Status Card",
        {"project_name": "Nova", "status": "At Risk", "details": "Blocked on API", "owner": "Alice"},
    )
    card = json.loads(rendered)
    assert card["type"] == "AdaptiveCard"


def test_simple_message_renders_html():
    html = render_template("Simple Message", {"title": "Hello", "body": "World"})
    assert "<h2>" in html
    assert "Hello" in html
    assert "World" in html


# ---------------------------------------------------------------------------
# Helper: _parse_facts
# ---------------------------------------------------------------------------


def test_parse_facts_basic():
    facts = _parse_facts("Revenue: $1M, Users: 500")
    assert len(facts) == 2
    assert facts[0] == {"title": "Revenue", "value": "$1M"}
    assert facts[1] == {"title": "Users", "value": "500"}


def test_parse_facts_empty():
    assert _parse_facts("") == []
    assert _parse_facts(None) == []


def test_parse_facts_no_colon():
    facts = _parse_facts("standalone")
    assert facts == [{"title": "standalone", "value": ""}]


# ---------------------------------------------------------------------------
# Template field metadata
# ---------------------------------------------------------------------------


def test_all_templates_have_required_keys():
    for name in get_outlook_template_names() + get_teams_template_names():
        tpl = get_template(name)
        assert tpl is not None, f"Template '{name}' not found"
        assert "name" in tpl
        assert "description" in tpl
        assert "platform" in tpl
        assert "fields" in tpl
        assert callable(tpl["render"])


def test_all_templates_render_without_error():
    for name in get_outlook_template_names() + get_teams_template_names():
        result = render_template(name, {})
        assert isinstance(result, str)
        assert len(result) > 0
