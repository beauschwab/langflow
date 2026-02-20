from langflow.components.tools import DataHubGraphQLMCPComponent


def test_datahub_graphql_mcp_component_defaults():
    component = DataHubGraphQLMCPComponent()
    frontend_node = component.to_frontend_node()
    node_data = frontend_node["data"]["node"]
    template = node_data["template"]

    assert node_data["display_name"] == "DataHub GraphQL MCP Server"
    assert node_data["name"] == "DataHubGraphQLMCP"
    assert template["mode"]["value"] == "SSE"
    assert template["graphql_endpoint"]["value"] == "http://localhost:8080/api/graphql"
