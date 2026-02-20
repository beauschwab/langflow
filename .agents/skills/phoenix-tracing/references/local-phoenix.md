# Running Phoenix Locally for Development

## Start the Phoenix server

```bash
pip install arize-phoenix
python -m phoenix.server.main serve
# UI available at http://localhost:6006
# OTLP endpoint: http://localhost:6006/v1/traces
```

Or with Docker:

```bash
docker run -p 6006:6006 arizephoenix/phoenix:latest
```

## Configure Langflow to point at local Phoenix

```bash
export PHOENIX_API_KEY="any-non-empty-string"   # local server accepts any key
export PHOENIX_COLLECTOR_ENDPOINT="http://localhost:6006"
```

Then start Langflow as normal. Spans will appear in the local Phoenix UI at
`http://localhost:6006`.

## Verify spans are exported

1. Run a flow in Langflow.
2. Open `http://localhost:6006` → **Traces** tab.
3. You should see a trace named after your flow with one root span and one child
   span per component that executed.

## Tips

- Use `ARIZE_PHOENIX_BATCH=false` (default) locally so spans appear immediately
  without waiting for the batch flush interval.
- Set `LANGFLOW_LOG_LEVEL=DEBUG` to see `"Telemetry data sent successfully"` and
  tracer setup log lines in the Langflow console.
