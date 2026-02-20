import copy

from langflow.io import MessageTextInput

from .mcp_component import MCPToolsComponent


class DataHubGraphQLMCPComponent(MCPToolsComponent):
    display_name = "DataHub GraphQL MCP Server"
    description = "Connect to a DataHub MCP server to access data from a GraphQL endpoint."
    icon = "server"
    name = "DataHubGraphQLMCP"

    inputs = copy.deepcopy(MCPToolsComponent.inputs)
    default_keys = [*MCPToolsComponent.default_keys, "graphql_endpoint"]
    inputs[0].value = "SSE"
    inputs[1].value = "npx -y @datahub-project/datahub-mcp-server --graphql-endpoint http://localhost:8080/api/graphql"
    inputs[2].value = "http://localhost:8080/mcp"
    inputs.insert(
        1,
        MessageTextInput(
            name="graphql_endpoint",
            display_name="GraphQL Endpoint",
            info="DataHub GraphQL endpoint used by the MCP server.",
            value="http://localhost:8080/api/graphql",
            required=True,
            refresh_button=True,
        ),
    )
