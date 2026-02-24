# template/ — Frontend Node Template Engine

## Purpose
Generates the frontend node template data that the React flow editor uses to render component nodes, their input fields, and connection ports.

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `field/` | Template field definitions — how individual input fields are rendered. |
| `frontend_node/` | Frontend node template generation — the complete node representation. |
| `template/` | Template base classes. |
| `utils.py` | Template utility functions. |

## Frontend Integration

- The template engine converts Python component definitions into JSON that the frontend understands.
- Each component's inputs, outputs, display name, icon, and metadata are translated into a frontend node template.
