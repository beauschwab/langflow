# inputs/ — Component Input Definitions

## Purpose
Defines the input type system for Langflow components. Each input type (StrInput, IntInput, FloatInput, BoolInput, DropdownInput, FileInput, etc.) controls how a field renders in the frontend component panel.

## Key Files

| File | Description |
|------|-------------|
| `inputs.py` | All input type classes — `StrInput`, `IntInput`, `FloatInput`, `BoolInput`, `SecretStrInput`, `DropdownInput`, `MultilineInput`, `FileInput`, `HandleInput`, `DataInput`, `MessageInput`, `TableInput`, etc. |
| `input_mixin.py` | `InputMixin` — shared behavior for all input types (validation, serialization). |
| `constants.py` | Input-related constants. |
| `validators.py` | Input value validators. |
| `utils.py` | Input utility functions. |

## Frontend Integration

- Each input type maps to a specific UI widget in the frontend component configuration panel.
- `HandleInput` creates connection ports on the component node in the flow editor.
- `SecretStrInput` renders as a password field and stores values in the variable service.
