# Architecture: Arize/Phoenix OTEL Wiring in Langflow

## Components

```
TracingService.start_tracers(run_id, run_name, user_id, session_id, project_name)
    └─ _initialize_arize_phoenix_tracer(trace_context)
           └─ ArizePhoenixTracer.__init__(trace_name, trace_type, project_name, trace_id, session_id)
                  └─ setup_arize_phoenix()
                       ├─ reads ARIZE_* / PHOENIX_* env vars
                       ├─ builds TracerProvider + span processor(s)
                       ├─ registers GRPCSpanExporter (Arize) and/or HTTPSpanExporter (Phoenix)
                       └─ instruments LangChain via LangChainInstrumentor
```

## Span lifecycle

1. **`TracingService.trace_component(...)`** — context manager called per component build.
2. Enqueues `_start_component_traces` → calls `ArizePhoenixTracer.add_trace(...)`.
3. `add_trace` creates a child span under the root span via W3C TraceContext propagation.
4. On component exit, enqueues `_end_component_traces` → calls `ArizePhoenixTracer.end_trace(...)`.
5. `end_trace` records outputs/logs and closes the child span.
6. After the full flow run, `TracingService.end_tracers(outputs, error)` calls `ArizePhoenixTracer.end(...)`.
7. `end` stamps chat input/output on the root span, closes it, and uninstruments LangChain.

## Exporter configuration

| Platform | Exporter | Protocol | Default endpoint |
|---|---|---|---|
| Arize AI | `GRPCSpanExporter` | gRPC | `https://otlp.arize.com/v1` |
| Phoenix (cloud) | `HTTPSpanExporter` | HTTP/OTLP | `https://app.phoenix.arize.com/v1/traces` |
| Phoenix (local) | `HTTPSpanExporter` | HTTP/OTLP | `http://localhost:6006/v1/traces` |

Both exporters can be active simultaneously when both sets of credentials are present.

## OpenInference semantic conventions

Spans use the [OpenInference](https://github.com/Arize-ai/openinference) spec:

- `openinference.span.kind` — e.g. `"chain"`, `"llm"`, `"tool"`
- `input.value` / `input.mime_type` — JSON-serialised component inputs
- `output.value` / `output.mime_type` — JSON-serialised component outputs
- `session.id` — links all spans for a single user conversation
- `metadata.*` — component-level metadata key-value pairs
- `logs.*` — structured logs emitted during component execution

## Relevant source files

| File | Role |
|---|---|
| `src/backend/base/langflow/services/tracing/arize_phoenix.py` | `ArizePhoenixTracer` implementation |
| `src/backend/base/langflow/services/tracing/service.py` | `TracingService` — initialises and dispatches to all tracers |
| `src/backend/base/langflow/services/tracing/base.py` | `BaseTracer` abstract interface |
| `src/backend/base/langflow/services/settings/base.py` | `deactivate_tracing` setting |
