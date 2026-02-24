# parameterRenderComponent/ — Parameter Rendering Engine

## Purpose
**Core component** that renders all input field types for configuring Langflow components. Maps backend input type definitions to frontend input widgets (text, dropdown, slider, code editor, file upload, table, etc.).

## Subdirectories

| Folder | Description |
|--------|-------------|
| `components/` | Individual input type renderers — one per input type. |
| `helpers/` | Parameter rendering helper functions. |

## For LLM Coding Agents
- This is the bridge between backend input types and frontend UI widgets.
- When adding a new input type in the backend, add a corresponding renderer here.
