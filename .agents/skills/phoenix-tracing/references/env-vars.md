# Environment Variable Reference — Arize/Phoenix Tracing

## Phoenix (cloud — app.phoenix.arize.com)

| Variable | Required | Default | Description |
|---|---|---|---|
| `PHOENIX_API_KEY` | Yes | — | API key from [phoenix.arize.com](https://app.phoenix.arize.com). Enables Phoenix tracing when set. |
| `PHOENIX_COLLECTOR_ENDPOINT` | No | `https://app.phoenix.arize.com` | Override the Phoenix OTLP collector base URL (do **not** include `/v1/traces`). |

## Arize AI

| Variable | Required | Default | Description |
|---|---|---|---|
| `ARIZE_API_KEY` | Yes (for Arize) | — | Arize API key. Both `ARIZE_API_KEY` and `ARIZE_SPACE_ID` must be set to enable Arize tracing. |
| `ARIZE_SPACE_ID` | Yes (for Arize) | — | Arize Space ID. |
| `ARIZE_COLLECTOR_ENDPOINT` | No | `https://otlp.arize.com` | Override the Arize gRPC collector endpoint. |

## Shared

| Variable | Required | Default | Description |
|---|---|---|---|
| `ARIZE_PHOENIX_BATCH` | No | `false` | Set to `true` / `1` / `yes` to use `BatchSpanProcessor` instead of `SimpleSpanProcessor`. Recommended for production. |

## Langflow tracing toggle

| Variable | Required | Default | Description |
|---|---|---|---|
| `LANGFLOW_DEACTIVATE_TRACING` | No | `false` | Set to `true` to disable **all** tracing (all tracer backends). |
