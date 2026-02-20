---
name: langflow-io-cli
description: Guide for interacting with the `langflow io` CLI for flow import/export, state snapshots, and resource analysis.
version: 1.0.0
category: toolchain
author: Langflow Copilot
license: MIT
tags: [langflow, cli, yaml, flows, agents]
---

# Langflow IO CLI skill

Use this skill when you need to:
- Analyze current Langflow state from terminal
- Export/import flows with JSON or YAML
- Produce multi-resource snapshots for copy/modify workflows

## Quick commands

```bash
# Show available io commands
python -m langflow io --help

# Summarize current state (flows/agents/folders/variables)
python -m langflow io state --base-url http://localhost:7860 --api-key <token>

# Export a multi-resource snapshot
python -m langflow io snapshot --output ./snapshot.yaml --base-url http://localhost:7860 --api-key <token>

# Import flows from YAML
python -m langflow io import-flows --file-path ./flows.yaml --base-url http://localhost:7860 --api-key <token>

# Export flows in YAML format
python -m langflow io export-flows \
  --flow-id <flow-id-1> \
  --flow-id <flow-id-2> \
  --file-format yaml \
  --output ./flows-export.zip \
  --base-url http://localhost:7860 \
  --api-key <token>
```

## Interaction pattern

1. Run `io state` first to understand existing resources.
2. Use `io snapshot` before mutations to keep a rollback artifact.
3. Use `io import-flows` for YAML/JSON ingestion.
4. Use `io export-flows` to verify round-trip output format.

## Reference YAML spec

See:
- `references/sample-agent-workflow.yaml`

This file is a starter spec for a flow upload payload compatible with:
- `POST /api/v1/flows/upload/`

You can keep a single flow document or a list under `flows`.
