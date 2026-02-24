# components/sharepoint/ — SharePoint Components

## Purpose
Microsoft SharePoint integration for loading files and documents from SharePoint sites.

## Key Files

| File | Description |
|------|-------------|
| `sharepoint_files.py` | SharePoint Files Loader — connects to SharePoint via Microsoft Graph API, loads files from document libraries. Uses httpx for HTTP calls with error handling. |

## For LLM Coding Agents

- Uses httpx for API calls; errors should be caught as `httpx.HTTPError` and re-raised as `ValueError`.
- The component must be added to `SIDEBAR_BUNDLES` in the frontend's `styleUtils.ts` to appear in the UI sidebar.
