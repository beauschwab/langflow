# components/confluence/ — Confluence Components

## Purpose
Atlassian Confluence integration for loading and searching wiki content.

## Key Files

| File | Description |
|------|-------------|
| `confluence.py` | Confluence loader component — connects to Confluence API, loads all pages in a space. Uses `trace_type = "tool"`. |
| `confluence_knowledge_base.py` | Confluence knowledge base component for RAG integration. Inherits `ConfluenceComponent`. |
| `confluence_search.py` | CQL-based search component — supports raw CQL expressions and structured filters (type, space, label, title). |
| `confluence_page_fetcher.py` | Fetch a specific page by ID with optional child pages and attachment metadata. |

## Query Types

### Space Loader (`ConfluenceComponent` / `ConfluenceKnowledgeBaseComponent`)
- Bulk-loads all pages from a given space key using LangChain's `ConfluenceLoader`.
- Supports multiple content formats: `STORAGE`, `VIEW`, `EXPORT_VIEW`, etc.
- Best for: initial ingestion / full-space RAG indexing.

### CQL Search (`ConfluenceSearchComponent`)
- Executes a Confluence Query Language search via the REST API.
- Two modes:
  1. **Raw CQL** — provide a complete CQL expression in the *CQL Query* field.
  2. **Structured filters** — compose a query from *Content Type*, *Space Key*, *Label*, and *Title Contains*.
- Example CQL: `space = "PROJ" AND label = "release-notes" AND type = page`
- Returns page body (Storage format) and metadata per result.

### Page Fetcher (`ConfluencePageFetcherComponent`)
- Fetches a single page by its numeric Confluence page ID.
- Optional expansions: child pages (up to *Max Child Pages*) and attachment metadata.
- Returns version info, author, ancestor breadcrumb, labels, and space details.
- Best for: targeted retrieval of a known page and its sub-tree.

## Auth
All components accept:
- **Site URL** — e.g. `https://<company>.atlassian.net/wiki`
- **Username** — Atlassian account e-mail
- **API Key** — Atlassian API token (create at https://id.atlassian.com/manage-profile/security/api-tokens)

