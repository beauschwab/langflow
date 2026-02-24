# field_typing/ — Component Field Type System

## Purpose
Defines type constants and range specifications for component input fields. Controls what types of connections are valid between components in the flow editor.

## Key Files

| File | Description |
|------|-------------|
| `constants.py` | Type constants (e.g., `Text`, `Data`, `Message`, `LanguageModel`, `Embeddings`, `VectorStore`) that define the type system for component I/O ports. |
| `range_spec.py` | `RangeSpec` — defines numeric range constraints for slider/number inputs. |

## Frontend Integration

- These types determine which component outputs can connect to which inputs in the flow editor.
- The frontend uses these types to validate connections and show compatible ports.
