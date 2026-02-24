# Copilot instructions for Langflow backend work

## Scope and priorities
- Preserve the existing Langflow UI and component/tool framework as the product surface.
- Treat the Python backend graph/agent execution layer as the primary change surface.
- Prefer incremental, backward-compatible changes that preserve API contracts.

## Current backend orchestration (authoritative paths)
- API entry point: `langflow.processing.process.run_graph_internal(...)`.
- Orchestration runtime: `langflow.processing.orchestrator.run_graph_with_orchestrator(...)` (LangGraph `StateGraph`).
- Graph execution primitive: `langflow.graph.graph.base.Graph._run(...)`.
- Existing graph scheduling/state internals still exist in `Graph` (`RunnableVerticesManager`, `GraphStateManager`) and must remain compatible.

## Best-practice implementation guidance
- Make the smallest possible change required for the task; avoid broad refactors.
- Keep behavior stable: response payload shape, SSE/event streaming, and session semantics.
- Reuse existing components/services/utilities rather than introducing parallel abstractions.
- When changing execution or orchestration code, add/update focused backend tests near the touched area.
- Prefer explicit error handling with actionable messages; do not leak secrets or raw internal traces.
