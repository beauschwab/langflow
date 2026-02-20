import copy
import re
import shlex

from langflow.io import MessageTextInput

from .mcp_component import MCPToolsComponent


class DataHubGraphQLMCPComponent(MCPToolsComponent):
    DEFAULT_GRAPHQL_ENDPOINT = "http://localhost:8080/api/graphql"

    display_name = "DataHub GraphQL MCP Server"
    description = "Connect to a DataHub MCP server to access data from a GraphQL endpoint."
    icon = "server"
    name = "DataHubGraphQLMCP"

    inputs = copy.deepcopy(MCPToolsComponent.inputs)
    default_keys = [*MCPToolsComponent.default_keys, "graphql_endpoint"]

    for _input in inputs:
        if _input.name == "mode":
            _input.value = "SSE"
        elif _input.name == "command":
            _input.value = f"npx -y @datahub-project/datahub-mcp-server --graphql-endpoint {DEFAULT_GRAPHQL_ENDPOINT}"
        elif _input.name == "sse_url":
            _input.value = "http://localhost:8080/mcp"

    inputs.insert(
        1,
        MessageTextInput(
            name="graphql_endpoint",
            display_name="GraphQL Endpoint",
            info="DataHub GraphQL endpoint used by the MCP server.",
            value=DEFAULT_GRAPHQL_ENDPOINT,
            required=True,
            refresh_button=True,
        ),
    )

    async def update_tools(self):
        if self.mode == "Stdio" and self.graphql_endpoint:
            endpoint_arg = shlex.quote(self.graphql_endpoint)
            if "--graphql-endpoint" in self.command:
                self.command = re.sub(
                    r"--graphql-endpoint\s+(?:\"[^\"]*\"|'[^']*'|\S+)",
                    lambda _: f"--graphql-endpoint {endpoint_arg}",
                    self.command,
                )
            else:
                self.command = f"{self.command} --graphql-endpoint {endpoint_arg}"
        return await super().update_tools()
