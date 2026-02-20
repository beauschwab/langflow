# Custom Component + LangGraph Backend Explainer

This page explains the practical steps to build a custom component, connect it to the current Langflow backend runtime (including LangGraph mode), expose it in the UI, customize its appearance/iconography, and document it for users.

## 1) Build the component contract in Python

Create a class that inherits from `Component` and define the frontend metadata and IO contract at class level:

- `display_name`
- `description`
- `documentation`
- `icon`
- `name`
- `inputs`
- `outputs`

Use typed output methods so runtime/output typing is explicit.

```python
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data


class MyComponent(Component):
    display_name = "My Component"
    description = "Example custom component"
    documentation = "https://your-docs-url"
    icon = "Wrench"
    name = "MyComponent"

    inputs = [
        MessageTextInput(name="input_value", display_name="Input Value", required=True),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        return Data(value=self.input_value)
```

## 2) Tie it to existing backend execution (Legacy + LangGraph)

You do **not** need a separate custom-component runtime for LangGraph mode. The orchestrator chooses backend mode, but execution still calls the graph runtime path that resolves component IO contracts.

- Backend switch: `orchestrator_backend` supports `legacy` and `langgraph`.
- In `langgraph` mode, orchestrator execution still routes per-run work through `graph._run(...)`, preserving existing component behavior and event contracts.

Practical steps:

1. Build your component with correct typed outputs and stable input names.
2. Validate in normal mode first.
3. Set backend to LangGraph mode (`LANGFLOW_ORCHESTRATOR_BACKEND=langgraph`) and re-run the same flow to verify parity.

## 3) Expose the component in the UI

There are two standard exposure paths:

### A. Interactive editor path (inside canvas)

1. In the Flow sidebar, click **New Custom Component**.
2. Edit code in the code modal.
3. Click **Check & Save**.

Frontend calls `POST /api/v1/custom_component` to validate/build component metadata, then updates node schema for rendering and ports.

### B. File-based discovery path (persistent categories)

Use `LANGFLOW_COMPONENTS_PATH` and place files in category subfolders:

```text
/your/components/path/
  helpers/
    my_component.py
  tools/
    another_component.py
```

Notes:

- Category folder names map to sidebar category groups.
- Files in `deactivated` folders are skipped by component discovery.
- Frontend fetches complete type metadata via `GET /api/v1/all` and renders it in the sidebar.

## 4) Customize appearance and iconography

### Node appearance metadata

Set these class properties for the node card UX:

- `display_name`: label shown in sidebar/node header
- `description`: shown in node body and search context
- `icon`: icon key (or emoji)
- `documentation`: enables Docs action from node toolbar

### Icon behavior in UI

- Icons are resolved through frontend icon rendering.
- Valid names include Lucide icons and supported category/custom icon entries.
- Emoji values are also supported and rendered directly.

Tip: prefer stable icon names that exist in frontend icon registries to avoid fallback/unknown rendering.

## 5) Configuration options and ports

To expose configurable UI fields and typed handles:

1. Add inputs in `inputs = [...]` with explicit `name`, `display_name`, `required`, `info`, and optional `input_types/options/value`.
2. Define outputs in `outputs = [...]` with `display_name`, `name`, `method`.
3. Keep input names stable once flows rely on them.
4. If dynamic behavior is required, implement `update_build_config(...)` safely.

## 6) Documentation checklist for each custom component

For each production-ready custom component, document:

1. Purpose and expected usage.
2. All inputs (name, type, required/default/options).
3. All outputs (name, return type, when emitted).
4. External dependencies and required env vars.
5. Example flow wiring (upstream/downstream node types).
6. Behavior verified in both legacy and LangGraph backend modes.

## Source references

- Backend orchestration switch and LangGraph adapter:
  - `src/backend/base/langflow/services/settings/base.py`
  - `src/backend/base/langflow/processing/orchestrator.py`
- Backend custom component validate/update APIs:
  - `src/backend/base/langflow/api/v1/endpoints.py`
- Component path loading/discovery:
  - `src/backend/base/langflow/services/settings/base.py`
  - `src/backend/base/langflow/custom/directory_reader/directory_reader.py`
- Frontend type fetch + sidebar exposure:
  - `src/frontend/src/controllers/API/queries/flows/use-get-types.ts`
  - `src/frontend/src/pages/FlowPage/components/flowSidebarComponent/index.tsx`
  - `src/frontend/src/pages/FlowPage/components/flowSidebarComponent/components/sidebarFooterButtons/index.tsx`
- Frontend code validation path:
  - `src/frontend/src/controllers/API/queries/nodes/use-post-validate-component-code.ts`
  - `src/frontend/src/modals/codeAreaModal/index.tsx`
- Icon resolution and node icon rendering:
  - `src/frontend/src/CustomNodes/helpers/check-lucide-icons.ts`
  - `src/frontend/src/CustomNodes/GenericNode/components/nodeIcon/index.tsx`
