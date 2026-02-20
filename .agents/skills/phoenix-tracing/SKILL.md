---
name: phoenix-tracing
description: Arize AI Phoenix / Arize tracing integration for Langflow — configure env vars, understand the OTEL-based wiring, and troubleshoot span export.
version: 1.0.0
category: observability
author: Claude MPM Team
license: MIT
tags: [python, tracing, arize, phoenix, opentelemetry, observability]
---

# Phoenix Tracing Skill

Langflow ships a built-in `ArizePhoenixTracer` (OpenInference + OTEL) that sends span data to either
**Arize AI** (gRPC) or **Phoenix** (HTTP) — or both simultaneously.

## Quick-start

### 1. Install optional dependencies (already bundled in Langflow extras)

```bash
pip install arize-phoenix-otel openinference-instrumentation-langchain
```

### 2. Set environment variables

**Phoenix (cloud):**
```bash
export PHOENIX_API_KEY="your-phoenix-api-key"
# optional — defaults to https://app.phoenix.arize.com
export PHOENIX_COLLECTOR_ENDPOINT="https://app.phoenix.arize.com"
```

**Arize:**
```bash
export ARIZE_API_KEY="your-arize-api-key"
export ARIZE_SPACE_ID="your-space-id"
# optional — defaults to https://otlp.arize.com
export ARIZE_COLLECTOR_ENDPOINT="https://otlp.arize.com"
```

**Both can be enabled at once.** Setting variables for both platforms will export spans to both.

### 3. Optional: batch span export

```bash
# Default is SimpleSpanProcessor; set to true to use BatchSpanProcessor
export ARIZE_PHOENIX_BATCH="true"
```

### 4. Disable tracing entirely

```bash
# In Langflow settings / env:
LANGFLOW_DEACTIVATE_TRACING=true
```

---

## How it works

See `references/architecture.md` for a full explanation of the OTEL wiring.

### Session ID propagation

Each flow run is assigned a `session_id` that is stamped onto the root span via
`SpanAttributes.SESSION_ID`. This links all component-level child spans to the
same Phoenix session for easy filtering in the UI.

### Span hierarchy

```
root span  (flow_id)
  └─ child span  (component trace_id)
  └─ child span  ...
```

The root span captures `chat_input_value` / `chat_output_value` from `ChatInput` /
`ChatOutput` components. All other components emit child spans with full
`INPUT_VALUE`, `OUTPUT_VALUE`, and log attributes.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| No spans in Phoenix UI | Check `PHOENIX_API_KEY` is set and not empty |
| `ImportError: arize-phoenix-otel` | Run `pip install arize-phoenix-otel` |
| `ImportError: LangChainInstrumentor` | Run `pip install openinference-instrumentation-langchain` |
| Spans missing session grouping | Ensure `session_id` is passed via the run API (`/api/v1/run/{flow_id}`) |
| Duplicate spans | `LangChainInstrumentor` double-instruments if Langflow is reloaded — restart the server |

---

## References

- `references/architecture.md` — OTEL wiring internals
- `references/env-vars.md` — Full environment variable reference
- `references/local-phoenix.md` — Running Phoenix locally for development
