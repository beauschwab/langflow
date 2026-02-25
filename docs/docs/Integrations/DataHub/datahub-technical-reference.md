---
title: DataHub Technical Reference
slug: /integrations/datahub/technical-reference
---

# DataHub technical reference

This page provides technical details about the DataHub component bundle architecture, GraphQL queries used, and extension points for developers.

## Architecture overview

The DataHub bundle consists of 8 components under `components/datahub/`, all sharing a common `DataHubGraphQLMixin` for GraphQL transport:

```
components/datahub/
├── datahub_base.py              # DataHubGraphQLMixin — shared GraphQL client
├── datahub_search.py            # DataHubSearchComponent
├── datahub_get_metadata.py      # DataHubGetMetadataComponent
├── datahub_lineage.py           # DataHubLineageComponent
├── datahub_add_documentation.py # DataHubAddDocumentationComponent
├── datahub_manage_tags.py       # DataHubManageTagsComponent
├── datahub_manage_terms.py      # DataHubManageTermsComponent
├── datahub_manage_domains.py    # DataHubManageDomainsComponent
└── datahub_manage_properties.py # DataHubManagePropertiesComponent
```

### Component class hierarchy

Each component extends both the shared mixin and the Langflow `LCToolComponent` base class:

```python
class DataHubSearchComponent(DataHubGraphQLMixin, LCToolComponent):
    # run_model() → list[Data]    — for pipeline use
    # build_tool() → Tool         — for agent use
```

This dual-inheritance pattern provides:
- **`DataHubGraphQLMixin`** — `_execute_graphql()`, `_headers()`, connection parameters
- **`LCToolComponent`** — Langflow component lifecycle, dual outputs (Data + Tool)

### DataHubGraphQLMixin

The mixin handles all GraphQL communication:

```python
class DataHubGraphQLMixin:
    graphql_endpoint: str   # populated from component input
    access_token: str       # populated from component input

    def _headers(self) -> dict[str, str]:
        """Build auth headers with Bearer token."""

    def _execute_graphql(self, query, variables=None, *, timeout=30) -> dict:
        """Execute GraphQL query/mutation via httpx.
        Raises ValueError on HTTP or GraphQL-level errors."""
```

Key behaviors:
- Uses `httpx.Client` with configurable timeout (default 30s)
- Bearer token authentication via `Authorization` header
- Raises `ValueError` on HTTP errors or GraphQL error responses
- Returns the `data` field from the GraphQL response

## GraphQL operations

### Read operations

| Component | GraphQL Operation | Variables |
|-----------|------------------|-----------|
| **Search** | `query search($input: SearchInput!)` | `type`, `query`, `start`, `count` |
| **Get Metadata** | `query getEntity($urn: String!)` | `urn` |
| **Lineage** | `query searchAcrossLineage($input: SearchAcrossLineageInput!)` | `urn`, `direction`, `count`, `maxHops` |

#### Search query fields

The search query returns entity fragments for `Dataset`, `Dashboard`, `DataJob`, `DataFlow`, and `GlossaryTerm` types, including:
- Entity URN and type
- Name, qualified name, and description
- Platform information
- Matched search fields

#### Get Metadata query fields

The entity query retrieves comprehensive Dataset metadata:
- `properties` — name, qualifiedName, description, customProperties, created/lastModified timestamps
- `editableProperties` — user-edited description
- `schemaMetadata.fields` — field path, type, native type, description, nullability
- `ownership.owners` — owner URN, username/group name, ownership type
- `tags.tags` — tag URN and name
- `glossaryTerms.terms` — term URN and name
- `domain` — domain URN and name
- `deprecation` — deprecated flag and note
- `subTypes` — type names (e.g., `table`, `view`)

Also includes fragments for `Dashboard` and `GlossaryTerm` entity types.

#### Lineage query fields

The lineage query uses `searchAcrossLineage` with:
- Entity fragments for `Dataset`, `DataJob`, `DataFlow`, and `Dashboard`
- Traversal paths (list of URN/type pairs)
- Degree of separation from the source entity

### Write operations

| Component | GraphQL Mutation | Variables |
|-----------|-----------------|-----------|
| **Add Documentation** | `mutation updateDescription($input: DescriptionUpdateInput!)` | `description`, `resourceUrn`, optional `subResourceType`, `subResource` |
| **Manage Tags** | `mutation addTag/removeTag($input: TagAssociationInput!)` | `tagUrn`, `resourceUrn`, optional `subResourceType`, `subResource` |
| **Manage Terms** | `mutation addTerm/removeTerm($input: TermAssociationInput!)` | `termUrn`, `resourceUrn`, optional `subResourceType`, `subResource` |
| **Manage Domains** | `mutation setDomain/unsetDomain(...)` | `domainUrn`, `entityUrn` |
| **Manage Properties** | `mutation upsertStructuredProperties/removeStructuredProperties(...)` | `assetUrn`, `structuredPropertyUrn`, `values` |

#### Sub-resource support

The Tags, Terms, and Documentation components support column-level operations via the optional **Sub-Resource** field. When provided:
- `subResourceType` is set to `DATASET_FIELD`
- `subResource` is set to the field path

This allows tagging or documenting individual columns within a dataset.

## Data output format

All components return `list[Data]` from `run_model()`. Each `Data` object contains:
- `text` — A human-readable text field (typically the description or name)
- `data` — A structured dictionary with all metadata fields

### Search result schema

```python
{
    "urn": "urn:li:dataset:...",
    "type": "DATASET",
    "name": "table_name",
    "qualified_name": "db.schema.table_name",
    "description": "Table description",
    "platform": "snowflake",
    "matched_fields": [{"name": "field", "value": "match"}]
}
```

### Get Metadata result schema

```python
{
    "urn": "urn:li:dataset:...",
    "type": "DATASET",
    "name": "table_name",
    "qualified_name": "db.schema.table_name",
    "description": "Editable description",
    "platform": "snowflake",
    "schema_fields": [
        {"field_path": "col", "type": "NUMBER", "native_type": "INT",
         "description": "...", "nullable": False}
    ],
    "owners": [{"urn": "urn:li:corpuser:...", "name": "user", "type": "DATAOWNER"}],
    "tags": [{"urn": "urn:li:tag:PII", "name": "PII"}],
    "glossary_terms": [{"urn": "urn:li:glossaryTerm:...", "name": "Term"}],
    "domain": {"urn": "urn:li:domain:...", "name": "Finance"},
    "sub_types": ["table"],
    "deprecated": false,
    "deprecation_note": "",
    "custom_properties": {"key": "value"},
    "created": 1700000000000,
    "last_modified": 1700100000000
}
```

### Write operation result schema

```python
{
    "urn": "urn:li:dataset:...",
    "action": "add",         # or "remove", "set", "unset", "upsert", "update_description"
    "success": true,
    "tag_urn": "...",         # for tag operations
    "term_urn": "...",        # for term operations
    "domain_urn": "...",      # for domain operations
    "property_urn": "...",    # for property operations
    "sub_resource": null      # or field path for column-level operations
}
```

## Tool schemas

Each component exposes a Pydantic `BaseModel` schema for its `StructuredTool`, enabling agents to call tools with validated arguments:

| Tool Name | Schema Class | Key Fields |
|-----------|-------------|------------|
| `datahub_search` | `SearchSchema` | `search_query`, `entity_type`, `max_results` |
| `datahub_get_metadata` | `GetMetadataSchema` | `entity_urn` |
| `datahub_lineage` | `LineageSchema` | `entity_urn`, `direction`, `max_hops`, `max_results` |
| `datahub_add_documentation` | `AddDocumentationSchema` | `entity_urn`, `documentation`, `sub_resource` |
| `datahub_manage_tags` | `ManageTagsSchema` | `action`, `tag_urn`, `entity_urn`, `sub_resource` |
| `datahub_manage_terms` | `ManageTermsSchema` | `action`, `term_urn`, `entity_urn`, `sub_resource` |
| `datahub_manage_domains` | `ManageDomainsSchema` | `action`, `domain_urn`, `entity_urn` |
| `datahub_manage_properties` | `ManagePropertiesSchema` | `action`, `entity_urn`, `property_urn`, `property_values` |

## Error handling

All components raise `ValueError` with descriptive messages for:
- HTTP connection errors (unreachable endpoint, timeout, auth failures)
- GraphQL-level errors (invalid queries, permission denied, entity not found)
- Input validation errors (missing required fields like `domain_urn` for set action)

## Testing

Unit tests are located at `src/backend/tests/unit/components/datahub/test_datahub_components.py` and cover:
- Component default values and frontend node rendering
- Tool building (name, description, schema)
- Mocked GraphQL execution for all read and write operations
- Input validation (required fields, action-specific constraints)
- GraphQL error propagation

Run the tests:

```bash
uv run pytest src/backend/tests/unit/components/datahub/ -v
```

## Relationship to DataHub MCP Server

The DataHub MCP Server component (`tools/datahub_graphql_mcp.py`) remains available as a separate integration. Key differences:

| Feature | Direct GraphQL components | MCP Server component |
|---------|--------------------------|---------------------|
| **Connection** | Direct HTTP to DataHub GraphQL API | Via MCP protocol (SSE or Stdio) |
| **Read operations** | ✅ Search, Get Metadata, Lineage | ✅ Search, Get Entity, Lineage, Queries |
| **Write operations** | ✅ Documentation, Tags, Terms, Domains, Properties | ❌ Read-only |
| **Tool granularity** | Individual tools per action | Dynamic tool loading from MCP server |
| **Dependencies** | `httpx` only | Requires MCP server process |
| **Configuration** | GraphQL endpoint + token | MCP server URL or command |

Use the direct GraphQL components when you need write capabilities, fine-grained control over individual operations, or want to avoid running a separate MCP server process. Use the MCP Server component when you want dynamic tool discovery or need tools that the MCP server provides but the direct components don't (such as query analysis).

## Extension guide

To add a new DataHub component:

1. Create a new file in `components/datahub/` (e.g., `datahub_my_action.py`).
2. Define the GraphQL query/mutation as a module-level string constant.
3. Create a component class extending `DataHubGraphQLMixin` and `LCToolComponent`.
4. Define inputs (always include `graphql_endpoint` and `access_token`).
5. Define a Pydantic schema class for the tool arguments.
6. Implement `_my_action()`, `run_model()`, and `build_tool()`.
7. Export the class from `__init__.py`.
8. Add tests to `test_datahub_components.py`.

```python
from langflow.components.datahub.datahub_base import DataHubGraphQLMixin
from langflow.base.langchain_utilities.model import LCToolComponent

_MY_QUERY = """
query myQuery($urn: String!) {
  entity(urn: $urn) { urn type }
}
"""

class DataHubMyActionComponent(DataHubGraphQLMixin, LCToolComponent):
    display_name = "DataHub My Action"
    name = "DataHubMyAction"
    icon = "DataHub"
    trace_type = "tool"

    inputs = [...]  # graphql_endpoint, access_token, + custom inputs

    class MyActionSchema(BaseModel):
        ...

    def _my_action(self, ...) -> list[Data]:
        data = self._execute_graphql(_MY_QUERY, {"urn": urn})
        return [Data(text="...", data={...})]

    def run_model(self) -> list[Data]:
        return self._my_action(self.entity_urn)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="datahub_my_action",
            description="...",
            func=self._my_action,
            args_schema=self.MyActionSchema,
        )
```
