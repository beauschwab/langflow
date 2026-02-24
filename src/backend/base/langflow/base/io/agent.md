# base/io/ — I/O Component Base Classes

## Purpose
Defines the base classes for user-facing input and output components — the primary interface between users and flows.

## Key Files

| File | Description |
|------|-------------|
| `chat.py` | `ChatInput` and `ChatOutput` base classes — the main chat interface components. Handle message creation, session management, and streaming. |
| `text.py` | `TextInput` and `TextOutput` base classes — simple text I/O components. |

## For LLM Coding Agents

- `ChatInput`/`ChatOutput` are the most commonly used components — they appear in almost every flow.
- These base classes handle message persistence via the message service.
