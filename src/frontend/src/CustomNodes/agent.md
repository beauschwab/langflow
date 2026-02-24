# CustomNodes/ — Custom React Flow Node Components

## Purpose
Custom node components rendered on the React Flow canvas. Each node represents a Langflow component (agent, model, tool, etc.) in the visual flow editor.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `GenericNode/` | The main component node type — renders any Langflow component with inputs, outputs, status, and configuration. |
| `NoteNode/` | Sticky note node — allows users to add text annotations to the canvas. |
| `helpers/` | Shared helper functions for node rendering. |
| `hooks/` | Shared React hooks for node behavior. |
| `utils/` | Shared utility functions for nodes. |

## For LLM Coding Agents
- `GenericNode` is the most important — it renders ALL Langflow component types.
- Node appearance is driven by data from the backend component type registry.
- Handle connections (input/output ports) are rendered as part of the node.
