from langflow.components.confluence import ConfluenceKnowledgeBaseComponent


def test_confluence_knowledge_base_component_defaults():
    component = ConfluenceKnowledgeBaseComponent()
    frontend_node = component.to_frontend_node()
    node_data = frontend_node["data"]["node"]

    assert node_data["display_name"] == "Confluence Knowledge Base"
    assert node_data["name"] == "ConfluenceKnowledgeBase"
    assert "space_key" in node_data["template"]
