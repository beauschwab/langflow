# User Experience Flows and End-to-End User Actions

This section documents user-facing workflows based on frontend implementation and existing product docs.

## 1) Create and set up a new flow

1. Open dashboard (`/flows` or `/all`).
2. Click **New Flow** and select a template (or blank flow).
3. In `FlowPage`, drag components from sidebar categories into canvas.
4. Connect compatible handles (left=input, right=output).
5. Configure component fields in node panels.
6. Save flow (manual save or autosave if enabled).

## 2) Configure model and tools in flow

1. Add a model component (for example OpenAI model node).
2. Provide credentials (often via Global Variables).
3. Add tool components (for example URL tool, MCP tool, Run Flow tool).
4. Connect tools into an Agent/Toolset input.
5. If needed, enable **Tool Mode** on nodes that can expose tool behavior.
6. Run from playground and verify model/tool responses.

## 3) Configure looping and router logic

## Loop nodes
1. Add **Loop** logic component.
2. Feed a `Data/List` output (for example from Parse Data) into loop data input.
3. Connect loop `item` output into downstream processing (prompt/model/etc).
4. Use `done` output for aggregation/summary branch after iteration completes.

## Router nodes
1. Add **Conditional Router** (or Data Conditional Router).
2. Configure comparison fields/operator/case sensitivity and max iterations.
3. Connect true/false outputs to branch-specific downstream nodes.
4. Run and inspect branch behavior in build status/logs and outputs.

## 4) Test flow in chat interface (I/O Modal + Playground)

1. Ensure at least Chat Input or Chat Output exists in flow.
2. Click **Playground** (or open I/O modal from flow view).
3. Choose/confirm active session.
4. Enter chat message and submit.
5. Frontend triggers flow build with chat input start node.
6. Observe:
   - streaming/polling response behavior
   - message history
   - session logs and editable message history
7. Optional: attach files (subject to file size/type rules).

## 5) Validate non-chat I/O behavior

1. In I/O modal, switch to non-chat input/output tabs.
2. Provide values for exposed input fields.
3. Trigger run/build.
4. Inspect output renderers (text/json/table/pdf/image/csv depending on node outputs).

## 6) Export flow integration/API code

1. Open **API** modal from flow toolbar.
2. Select code tab (curl, Python API, JS API, Python code, chat widget).
3. Optionally configure tweaks and endpoint name.
4. Copy generated code for `run`/`webhook` invocation.

## 7) Expose flows as MCP-compatible tools

There are two common user flows:

## A) Use MCP server tools inside Langflow
1. Add **MCP Tools (stdio)** or **MCP Tools (SSE)** component.
2. For stdio mode, set MCP command (example: `uvx mcp-server-fetch`).
3. Connect MCP tools output into agent toolset.
4. Open Playground and test tool-calling behavior.

## B) Use Langflow as MCP server for external MCP clients
1. Ensure Langflow MCP server is enabled in deployment settings.
2. Configure MCP client (example: Claude Desktop) to connect through `mcp-sse-shim`.
3. Point MCP host to Langflow host.
4. Restart client and verify flow tools become available in MCP client.
5. Execute prompts that trigger tool usage.

## 8) Share/publish/reuse flows

1. Use share/publish actions from flow UI where enabled.
2. Open public playground route (`/playground/:id`) for public flows.
3. Validate access constraints: public flow + available IO components.

