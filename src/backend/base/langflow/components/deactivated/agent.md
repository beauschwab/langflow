# components/deactivated/ — Deactivated Components

## Purpose
Contains deprecated or disabled components that are kept for backward compatibility with existing flows but are hidden from the UI sidebar.

## Key Files

Notable deactivated components include `mcp_sse.py`, `mcp_stdio.py`, `sub_flow.py`, `merge_data.py`, `store_message.py`, `list_flows.py`, and others.

## For LLM Coding Agents

- Do not create new components here. This is for legacy/deprecated components only.
- If a user's flow references a deactivated component, it will still work — the component code is preserved.
