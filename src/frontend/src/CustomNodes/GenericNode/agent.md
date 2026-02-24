# CustomNodes/GenericNode/ — Main Component Node

## Purpose
The primary node component rendered for every Langflow component on the flow canvas. Renders the node header, input fields, output handles, status indicator, and action buttons.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `components/` | Sub-components: input fields, output handles, status, description, icon, dialogs, etc. |
| `hooks/` | Node-specific React hooks. |

## Key Sub-Components
- `NodeInputField/` — renders individual input parameter fields on the node
- `NodeOutputfield/` — renders output connection handles
- `NodeStatus/` — shows build status (idle, building, success, error)
- `NodeName/` — editable node name display
- `NodeDescription/` — node description tooltip
- `nodeIcon/` — renders the component's icon
- `HandleTooltipComponent/` — tooltip on connection handles
- `outputModal/` — expanded output view modal
- `NodeDialogComponent/` — node configuration dialog
