# services/tracing/ — Distributed Tracing Service

## Purpose
Distributed tracing integration with multiple observability platforms. Tracks flow execution, component builds, and LLM calls.

## Key Files

| File | Description |
|------|-------------|
| `service.py` | `TracingService` — manages trace lifecycle and span creation. |
| `base.py` | Abstract tracer interface. |
| `factory.py` | `TracingServiceFactory`. |
| `langsmith.py` | LangSmith tracing integration. |
| `langfuse.py` | LangFuse tracing integration. |
| `langwatch.py` | LangWatch tracing integration. |
| `arize_phoenix.py` | Arize AI Phoenix tracing integration (OTEL-based). |
| `opik.py` | Opik tracing integration. |
| `schema.py` | Tracing schemas. |
| `utils.py` | Tracing utility functions. |

## For LLM Coding Agents

- Tracing is configured via environment variables (e.g., `LANGFLOW_LANGSMITH_API_KEY`).
- The Arize Phoenix integration uses OTEL-based span export.
- To add a new tracing provider: create a new file here, implement the base tracer interface, register in the factory.
