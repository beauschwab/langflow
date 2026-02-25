# components/datahub/ — DataHub Components

## Purpose
DataHub metadata platform integration for data discovery, lineage exploration,
and AI-assisted metadata enrichment. These components communicate directly with
the DataHub GraphQL API and can be wired as agent tools or used standalone in flows.

## Key Files

| File | Description |
|------|-------------|
| `datahub_base.py` | Shared mixin providing GraphQL client, auth headers, and error handling. |
| `datahub_search.py` | Search across DataHub entities (datasets, dashboards, data jobs, glossary terms) with keyword and type filters. |
| `datahub_get_metadata.py` | Retrieve comprehensive metadata for any entity by URN — schema, ownership, tags, terms, domain, and documentation. |
| `datahub_lineage.py` | Explore upstream and downstream data lineage with configurable hop depth for impact analysis. |
| `datahub_add_documentation.py` | Add or update documentation (Markdown) on entities or individual columns. |
| `datahub_manage_tags.py` | Add or remove tags on entities or columns. |
| `datahub_manage_terms.py` | Add or remove glossary terms on entities or columns for business vocabulary management. |
| `datahub_manage_domains.py` | Set or unset the business domain on entities for organizational hierarchy. |
| `datahub_manage_properties.py` | Upsert or remove structured properties for custom metadata enrichment. |

## Capabilities

### Read / Explore
- **Search** — keyword + entity-type filter, returns URNs, names, descriptions, matched fields.
- **Get Metadata** — full entity profile including schema fields, owners, tags, terms, domain, deprecation, custom properties, and timestamps.
- **Lineage** — upstream/downstream traversal with configurable max hops and result limit.

### Write / Enrich
- **Documentation** — entity-level or column-level description updates (Markdown).
- **Tags** — add/remove tag associations for classification and governance.
- **Glossary Terms** — attach/detach business glossary terms to maintain controlled vocabulary.
- **Domains** — assign entities to business domains for organizational hierarchy.
- **Structured Properties** — upsert/remove typed property values for custom metadata dimensions.

## Auth
All components accept:
- **GraphQL Endpoint** — e.g. `http://localhost:8080/api/graphql`
- **Access Token** — DataHub personal access token (optional for local development)

## MCP Bridge
The original `tools/datahub_graphql_mcp.py` component remains available for
connecting to a DataHub MCP server. The components in this directory provide
direct GraphQL API access, offering finer-grained control and write capabilities
that the MCP server's read-only tool set does not cover.

## For AI Agents
Each component exposes both:
- **Data output** (`run_model`) — for direct use in Langflow data pipelines.
- **Tool output** (`build_tool`) — for wiring to agents as callable tools.

This dual-output pattern allows agents to autonomously search, explore lineage,
understand datasets, and enrich metadata within DataHub — enabling AI-assisted
data governance workflows.
