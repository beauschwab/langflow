---
title: Integrate DataHub with Langflow
slug: /integrations/datahub/setup
---

# Integrate DataHub with Langflow

Langflow integrates with [DataHub](https://datahubproject.io/), the open-source metadata platform for data discovery, governance, and observability. With Langflow's DataHub components, you can search, explore, and enrich metadata in your data ecosystem using flows or AI agents.

Langflow provides two ways to connect to DataHub:

- **DataHub components** — Direct GraphQL API access for search, lineage, metadata retrieval, and metadata enrichment (tags, glossary terms, domains, documentation, structured properties).
- **DataHub MCP Server** — Model Context Protocol bridge that dynamically loads tools from a running DataHub MCP server instance.

## Prerequisites

- A running [DataHub](https://datahubproject.io/docs/quickstart) instance (self-hosted or [DataHub Cloud](https://www.acryldata.io/)).
- A DataHub personal access token for authentication. See [DataHub Authentication](https://datahubproject.io/docs/authentication/personal-access-tokens/).
- The GraphQL API endpoint for your DataHub instance (default: `http://localhost:8080/api/graphql`).

## Configure DataHub in Langflow

All DataHub components share two common inputs:

| Input | Description |
|-------|-------------|
| **GraphQL Endpoint** | The DataHub GraphQL API URL. Default: `http://localhost:8080/api/graphql` |
| **Access Token** | Your DataHub personal access token. Optional for local development without auth. |

:::tip
Store your access token as a [global variable](/configuration-global-variables) to avoid entering it in every component.
:::

## DataHub components

Langflow provides 8 DataHub components organized into **read** (explore) and **write** (enrich) categories.

### Read / explore

These components retrieve metadata from DataHub without modifying it.

#### DataHub Search

Search across all DataHub entities using keywords and optional entity type filters.

| Input | Description |
|-------|-------------|
| **Search Query** | Keywords to search for across DataHub entities. |
| **Entity Type** | Filter by entity type: `ALL`, `DATASET`, `DASHBOARD`, `DATA_JOB`, `DATA_FLOW`, `GLOSSARY_TERM`, `CONTAINER`, or `DOMAIN`. Default: `ALL`. |
| **Max Results** | Maximum number of results (1–100). Default: `10`. |

**Output:** A list of matching entities with URN, type, name, description, platform, and matched fields.

#### DataHub Get Metadata

Retrieve comprehensive metadata for any DataHub entity by its URN.

| Input | Description |
|-------|-------------|
| **Entity URN** | The DataHub URN of the entity. Example: `urn:li:dataset:(urn:li:dataPlatform:snowflake,db.schema.table,PROD)` |

**Output:** Full entity profile including:
- Schema fields (field path, type, description, nullability)
- Ownership (owners and ownership types)
- Tags and glossary terms
- Domain assignment
- Deprecation status
- Custom properties
- Creation and modification timestamps

#### DataHub Lineage

Explore upstream and downstream data lineage for an entity.

| Input | Description |
|-------|-------------|
| **Entity URN** | The DataHub URN of the entity to explore lineage for. |
| **Direction** | `UPSTREAM` (dependencies) or `DOWNSTREAM` (dependents). Default: `DOWNSTREAM`. |
| **Max Hops** | Maximum number of hops to traverse (1–10). Default: `3`. |
| **Max Results** | Maximum number of lineage results. Default: `20`. |

**Output:** Related entities with URN, type, name, platform, degree of separation, direction, and traversal paths.

### Write / enrich

These components modify metadata in DataHub. They require appropriate permissions in your DataHub instance.

#### DataHub Add Documentation

Add or update documentation (Markdown supported) on an entity or individual column.

| Input | Description |
|-------|-------------|
| **Entity URN** | The DataHub URN of the entity to document. |
| **Documentation** | The documentation text (Markdown supported). |
| **Sub-Resource** | Optional. Field path for column-level documentation. |

#### DataHub Manage Tags

Add or remove tags on DataHub entities or columns.

| Input | Description |
|-------|-------------|
| **Action** | `add` or `remove`. |
| **Tag URN** | The URN of the tag. Example: `urn:li:tag:PII` |
| **Entity URN** | The URN of the entity to tag. |
| **Sub-Resource** | Optional. Field path for column-level tagging. |

#### DataHub Manage Glossary Terms

Add or remove glossary terms on entities for business vocabulary management.

| Input | Description |
|-------|-------------|
| **Action** | `add` or `remove`. |
| **Glossary Term URN** | The URN of the glossary term. Example: `urn:li:glossaryTerm:CustomerID` |
| **Entity URN** | The URN of the entity. |
| **Sub-Resource** | Optional. Field path for column-level term association. |

#### DataHub Manage Domains

Set or unset the business domain on entities for organizational hierarchy.

| Input | Description |
|-------|-------------|
| **Action** | `set` or `unset`. |
| **Domain URN** | The URN of the domain (required for `set`). Example: `urn:li:domain:Finance` |
| **Entity URN** | The URN of the entity. |

#### DataHub Manage Structured Properties

Upsert or remove structured properties for custom metadata enrichment.

| Input | Description |
|-------|-------------|
| **Action** | `upsert` or `remove`. |
| **Entity URN** | The URN of the entity. |
| **Property URN** | The URN of the structured property. Example: `urn:li:structuredProperty:retentionTime` |
| **Property Values** | Comma-separated values (required for `upsert`). |

## Component outputs

Each DataHub component provides two output types:

- **Data** — Returns structured `Data` objects for use in Langflow data pipelines and processing flows.
- **Tool** — Returns a LangChain `StructuredTool` for wiring to an [Agent](/components-agents) component, enabling AI-powered metadata exploration and enrichment.

## DataHub MCP Server

In addition to the direct GraphQL components, Langflow also provides the **DataHub GraphQL MCP Server** component under the **Tools** category. This component connects to a [DataHub MCP server](https://github.com/acryldata/mcp-server-datahub) and dynamically loads its tools.

| Input | Description |
|-------|-------------|
| **Mode** | `SSE` (Server-Sent Events) or `Stdio` (subprocess). Default: `SSE`. |
| **GraphQL Endpoint** | DataHub GraphQL endpoint used by the MCP server. |
| **MCP SSE URL** | URL for MCP SSE connection. Default: `http://localhost:8080/mcp`. |
| **MCP Command** | Command for Stdio mode. Default: `npx -y @datahub-project/datahub-mcp-server --graphql-endpoint ...` |

The MCP server provides read-only tools (search, entity metadata, lineage, queries). Use the direct GraphQL components above when you need write capabilities or more granular control.

## Additional resources

- [DataHub documentation](https://datahubproject.io/docs/)
- [DataHub GraphQL API reference](https://datahubproject.io/docs/api/graphql/overview)
- [DataHub MCP server](https://github.com/acryldata/mcp-server-datahub)
- [DataHub personal access tokens](https://datahubproject.io/docs/authentication/personal-access-tokens/)
- [DataHub metadata enrichment tutorial](/integrations/datahub/metadata-enrichment-agent)
- [DataHub technical reference](/integrations/datahub/technical-reference)
