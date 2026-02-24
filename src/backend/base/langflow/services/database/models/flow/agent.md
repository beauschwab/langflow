# models/flow/ — Flow Database Model

## Purpose
The most important database model — stores flow definitions including the full graph JSON that represents the visual flow.

## Key Files

| File | Description |
|------|-------------|
| `model.py` | `FlowModel` — SQLModel class for the flows table. Contains the `data` column (JSON) that holds the entire flow graph. |
| `schema.py` | Pydantic schemas for flow serialization/deserialization. |
| `utils.py` | Flow model utility functions. |

## For LLM Coding Agents

- The `data` field contains the flow graph JSON — this is the same JSON the frontend sends/receives.
- Flow import/export supports both JSON and YAML formats.
