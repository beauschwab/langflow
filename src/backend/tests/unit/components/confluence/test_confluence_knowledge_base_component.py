from unittest.mock import patch

from langflow.components.confluence import ConfluenceKnowledgeBaseComponent


def test_confluence_knowledge_base_component_defaults():
    component = ConfluenceKnowledgeBaseComponent()
    frontend_node = component.to_frontend_node()
    node_data = frontend_node["data"]["node"]

    assert node_data["display_name"] == "Confluence Knowledge Base"
    assert node_data["name"] == "ConfluenceKnowledgeBase"
    assert "space_key" in node_data["template"]
    assert "cloud" in node_data["template"]
    assert node_data["template"]["cloud"]["value"] is True


def test_confluence_knowledge_base_component_accepts_on_prem_mode():
    component = ConfluenceKnowledgeBaseComponent(
        cloud=False,
        url="https://confluence.example.local",
        username="onprem-user",
        api_key="test-key",
        space_key="OPS",
    )

    assert component.cloud is False

    with patch("langflow.components.confluence.confluence.ConfluenceLoader") as mock_loader:
        component.build_confluence()

    mock_loader.assert_called_once()
    assert mock_loader.call_args.kwargs["cloud"] is False
