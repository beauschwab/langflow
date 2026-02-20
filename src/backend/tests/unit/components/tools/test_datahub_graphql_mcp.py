from unittest.mock import AsyncMock, patch

import pytest
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


@pytest.mark.asyncio
async def test_datahub_graphql_mcp_component_updates_command_endpoint():
    component = DataHubGraphQLMCPComponent(mode="Stdio", graphql_endpoint="https://datahub.example.com/api/graphql")
    component.command = (
        f"npx -y @datahub-project/datahub-mcp-server --graphql-endpoint "
        f"{DataHubGraphQLMCPComponent.DEFAULT_GRAPHQL_ENDPOINT}"
    )

    with patch("langflow.components.tools.datahub_graphql_mcp.MCPToolsComponent.update_tools", new_callable=AsyncMock) as mock_update:
        await component.update_tools()

    assert "--graphql-endpoint https://datahub.example.com/api/graphql" in component.command
    mock_update.assert_awaited_once()
