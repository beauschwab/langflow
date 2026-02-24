# base/mcp/ — Model Context Protocol Utilities

## Purpose
Client utilities for the Model Context Protocol (MCP), enabling Langflow to connect to external MCP tool servers.

## Key Files

| File | Description |
|------|-------------|
| `util.py` | `MCPStdioClient` — connects to MCP servers via stdio transport. Handles tool discovery and invocation. Note: command parsing uses `str.split()`, not `shlex.split()`. |

## For LLM Coding Agents

- MCP allows Langflow to dynamically discover and use tools from external servers.
- The MCP component in `components/tools/mcp_component.py` uses this utility.
