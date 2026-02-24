# components/tools/ — Tool Components

## Purpose
Individual tool components that agents can invoke. Includes search APIs, code execution, database queries, and external service integrations.

## Key Files

| File | Description |
|------|-------------|
| `duck_duck_go_search_run.py` | DuckDuckGo search tool. |
| `search.py` | Generic search tool. |
| `search_api.py` | SearchAPI.io integration. |
| `bing_search_api.py` | Bing Search API tool. |
| `serp.py` | SerpAPI search tool. |
| `serp_api.py` | Alternative SerpAPI integration. |
| `exa_search.py` | Exa AI search tool. |
| `searxng.py` | SearXNG meta-search engine tool. |
| `glean_search_api.py` | Glean enterprise search tool (uses httpx). |
| `calculator.py` | Calculator tool. |
| `calculator_core.py` | Calculator core logic. |
| `python_repl.py` | Python REPL tool. |
| `python_repl_core.py` | Python REPL core logic. |
| `python_code_structured_tool.py` | Structured Python code execution tool. |
| `astradb.py` | AstraDB tool. |
| `astradb_cql.py` | AstraDB CQL query tool (10s timeout, no retry). |
| `arxiv.py` | Arxiv paper search tool. |
| `mcp_component.py` | MCP (Model Context Protocol) tool — dynamically discovers and invokes tools from MCP servers. |
| `datahub_graphql_mcp.py` | DataHub GraphQL MCP integration. |
| `tavily_search.py` | Tavily search tool. |
| `wikidata_api.py` | Wikidata API tool. |

## For LLM Coding Agents

- Tool components use httpx or requests for HTTP calls with hardcoded 10-second timeouts.
- New tools should include `trace_type = "tool"` for proper tracing.
- Wrap HTTP operations in try-except catching `httpx.HTTPError`.
