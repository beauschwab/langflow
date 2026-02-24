# schema/ — Pydantic Data Schemas

## Purpose
Central schema definitions used throughout the backend — messages, data objects, artifacts, content blocks, playground events, and serialization formats.

## Key Files

| File | Description |
|------|-------------|
| `message.py` | `Message` schema — the core message object passed between components. Contains text, sender, session_id, and metadata. |
| `data.py` | `Data` schema — the generic data container passed between components. Key-value store with metadata. |
| `dataframe.py` | DataFrame schema for tabular data handling. |
| `artifact.py` | `Artifact` schema — represents build artifacts from component execution. |
| `content_block.py` | `ContentBlock` schema — structured content blocks for rich output display. |
| `content_types.py` | Content type definitions for content blocks. |
| `graph.py` | Graph-related schemas. |
| `image.py` | Image handling schemas. |
| `log.py` | Log entry schemas. |
| `playground_events.py` | Playground event schemas — defines events sent to the frontend during execution. |
| `properties.py` | Property schemas for component metadata. |
| `schema.py` | Core schema definitions and type aliases (e.g., `InputType`). |
| `serialize.py` | Serialization helper schemas. |
| `table.py` | Table/tabular data schemas. |
| `validators.py` | Schema validators. |
| `dotdict.py` | `DotDict` — dictionary subclass with dot notation access. |
| `encoders.py` | Custom JSON encoders for complex types. |

## For LLM Coding Agents

- `Message` and `Data` are the two primary data types flowing between components.
- `Message` is used for chat/conversational data; `Data` is used for structured/generic data.
