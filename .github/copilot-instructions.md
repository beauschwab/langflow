# Copilot instructions for Langflow backend architecture work

## Scope and priorities
- Preserve the existing Langflow UI and tool/component framework as the product surface.
- Treat the Python backend graph/agent execution layer as the primary migration target.
- Prefer incremental, backward-compatible changes that keep existing API contracts stable.

## Current backend orchestration anchors
- Flow execution currently runs through `langflow.graph.graph.base.Graph` and `Graph.arun(...)`.
- Execution scheduling is handled by `RunnableVerticesManager`.
- Runtime state is handled by `GraphStateManager` and state services.
- API entry points use `run_graph_internal(...)` and flow build/event queue endpoints.

## LangGraph migration intent
- Replace custom graph scheduling/state progression with a LangGraph-backed runtime.
- Keep Langflow components, tools, and workflow builder semantics intact.
- Add an adapter layer so existing flow JSON can compile to LangGraph state graphs.

## Practical guidance for implementation tasks
- Minimize surface-area changes and avoid unnecessary refactors.
- Preserve response payloads, event stream behavior, and session semantics.
- Add migration behind a feature flag first; keep current graph engine as fallback.
- When changing orchestration logic, update targeted backend tests around graph execution, state updates, and streaming events.
