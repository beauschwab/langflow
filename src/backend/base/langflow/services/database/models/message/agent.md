# models/message/ — Message Database Model

## Purpose
SQLModel and CRUD operations for chat messages exchanged during flow execution.

## Key Files

| File | Description |
|------|-------------|
| `model.py` | `MessageModel` — SQLModel class for the messages table. Stores sender, text, session_id, timestamps. |
| `crud.py` | CRUD operations — create, list, delete messages by session. |
