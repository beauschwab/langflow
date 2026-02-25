---
title: DataHub Metadata Enrichment Agent
slug: /integrations/datahub/metadata-enrichment-agent
---

# Build a DataHub metadata enrichment agent

This tutorial shows you how to build an AI agent that can search, explore, and enrich metadata in DataHub using natural language. The agent uses DataHub components as tools to autonomously discover datasets, inspect their metadata, and add documentation, tags, glossary terms, and domains.

## Prerequisites

- [DataHub setup in Langflow](/integrations/datahub/setup)
- [An OpenAI API key](https://platform.openai.com/) (or another LLM provider)
- A running DataHub instance with some datasets ingested

## Overview

The metadata enrichment agent combines multiple DataHub components as tools for an AI agent. The agent can then respond to natural language requests like:

- *"Find all datasets related to customer transactions"*
- *"Show me the schema and owners of the orders table"*
- *"What tables are downstream of the customer_events dataset?"*
- *"Add PII tags to the email and phone columns in the users table"*
- *"Set the Finance domain on all revenue-related datasets"*
- *"Add documentation describing the purpose of the customers table"*

## Build the flow

### 1. Add the Agent

1. In the Langflow **Workspace**, add an **Agent** component.
2. Add an **OpenAI** model component and connect it to the Agent's **Model** port.
3. Paste your OpenAI API key in the model component (or use a [global variable](/configuration-global-variables)).

### 2. Add DataHub tools

Add the following DataHub components to the workspace, and connect each one's **Tool** output to the Agent's **Tools** port:

| Component | Purpose |
|-----------|---------|
| **DataHub Search** | Discover datasets, dashboards, and other entities by keyword |
| **DataHub Get Metadata** | Retrieve full entity profiles (schema, ownership, tags, terms) |
| **DataHub Lineage** | Explore upstream/downstream data dependencies |
| **DataHub Add Documentation** | Write or update entity and column descriptions |
| **DataHub Manage Tags** | Add or remove classification tags |
| **DataHub Manage Glossary Terms** | Associate business glossary terms |
| **DataHub Manage Domains** | Assign entities to business domains |

Configure the **GraphQL Endpoint** and **Access Token** on each DataHub component. Use a global variable for the access token so you only enter it once.

:::tip
You don't need to include every DataHub component. Start with Search + Get Metadata for a read-only explorer, then add write tools as needed.
:::

### 3. Add Chat Input and Output

1. Add a **Chat Input** component and connect it to the Agent's **Input** port.
2. Add a **Chat Output** component and connect the Agent's **Output** port to it.

### 4. (Optional) Add system prompt context

For best results, add a **Prompt** component connected to the Agent's **System Message** port with context about your data ecosystem. For example:

```
You are a data governance assistant with access to DataHub.
You help users discover datasets, understand data lineage,
and enrich metadata with documentation, tags, glossary terms, and domains.

When users ask about data, use the DataHub Search tool first to find relevant entities.
When they want details, use Get Metadata to retrieve the full profile.
For impact analysis questions, use Lineage to trace dependencies.

When enriching metadata:
- Use Add Documentation for entity or column descriptions (Markdown is supported)
- Use Manage Tags for classification labels like PII, Sensitive, or Deprecated
- Use Manage Glossary Terms for business vocabulary (e.g., Revenue, Customer ID)
- Use Manage Domains for organizational hierarchy (e.g., Finance, Marketing)

Always confirm with the user before making changes to metadata.
Always provide the entity URN when referencing specific entities.
```

## Example conversations

### Data discovery

```
User: Find datasets related to customer orders

Agent: I found 3 datasets matching "customer orders":
1. urn:li:dataset:(urn:li:dataPlatform:snowflake,analytics.orders,PROD)
   - Platform: Snowflake
   - Description: "Customer order transactions"
2. urn:li:dataset:(urn:li:dataPlatform:snowflake,analytics.order_items,PROD)
   - Platform: Snowflake
   - Description: "Line items for customer orders"
3. urn:li:dataset:(urn:li:dataPlatform:bigquery,warehouse.customer_orders,PROD)
   - Platform: BigQuery
   - Description: "Aggregated customer order summary"
```

### Metadata inspection

```
User: Show me the schema and owners of the first one

Agent: Here's the full profile for the orders dataset:

**Schema fields:**
| Field | Type | Description |
|-------|------|-------------|
| order_id | NUMBER | Primary key |
| customer_id | NUMBER | Foreign key to customers |
| order_date | TIMESTAMP | When the order was placed |
| total_amount | NUMBER | Order total in USD |
| status | STRING | Order status (pending/shipped/delivered) |

**Owners:** @jane.smith (Data Owner), @analytics-team (Technical Owner)
**Tags:** production, tier-1
**Domain:** Commerce
```

### Impact analysis

```
User: What downstream tables would be affected if I change the orders schema?

Agent: I found 5 downstream dependencies of the orders dataset:
1. analytics.order_metrics (1 hop) — Snowflake
2. analytics.revenue_dashboard (2 hops) — Looker Dashboard
3. ml.customer_churn_features (2 hops) — Snowflake
4. reporting.weekly_sales (2 hops) — BigQuery
5. analytics.order_items (1 hop) — Snowflake

Changes to the orders schema could impact all 5 downstream assets.
I recommend reviewing each before making changes.
```

### Metadata enrichment

```
User: Add PII tags to the customer_id and email columns in the orders table

Agent: I'll add the PII tag to those columns. Let me confirm:
- Tag: urn:li:tag:PII
- Entity: urn:li:dataset:(urn:li:dataPlatform:snowflake,analytics.orders,PROD)
- Columns: customer_id, email

Shall I proceed?

User: Yes

Agent: Done! PII tag has been added to both columns:
✅ customer_id — tagged with PII
✅ email — tagged with PII
```

## Best practices

### Start read-only
Begin with Search, Get Metadata, and Lineage tools to explore your data. Add write tools once you're comfortable with the agent's behavior.

### Use specific prompts
Guide the agent with clear system prompts about your data conventions, naming standards, and governance policies.

### Validate before writing
Include instructions in your system prompt to always confirm with the user before modifying metadata.

### Batch operations
For bulk enrichment tasks, describe the pattern and let the agent iterate. For example:
- *"Add the PII tag to all columns named 'email' or 'phone' across all datasets"*
- *"Set the Finance domain on all datasets in the finance schema"*

### Combine with MCP
The DataHub MCP Server component can complement the direct GraphQL components. Use MCP for dynamic tool discovery and the direct components for write operations.

## Additional resources

- [DataHub setup in Langflow](/integrations/datahub/setup)
- [DataHub technical reference](/integrations/datahub/technical-reference)
- [Agent component reference](/components-agents)
- [DataHub GraphQL API](https://datahubproject.io/docs/api/graphql/overview)
