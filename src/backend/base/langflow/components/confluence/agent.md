# components/confluence/ — Confluence Components

## Purpose
Atlassian Confluence integration for loading and searching wiki content.

## Key Files

| File | Description |
|------|-------------|
| `confluence.py` | Confluence loader component — connects to Confluence API, loads pages by space/page ID. Uses `trace_type = "tool"`. |
| `confluence_knowledge_base.py` | Confluence knowledge base component for RAG integration. |
