# services/socket/ — Socket.IO Service

## Purpose
Manages WebSocket connections via Socket.IO for real-time communication between the backend and frontend during flow execution.

## Key Files

| File | Description |
|------|-------------|
| `service.py` | `SocketIOService` — manages Socket.IO server, room management, and event emission. Streams vertex build events, chat messages, and playground events to the frontend. |
| `factory.py` | `SocketIOServiceFactory`. |
| `utils.py` | Socket utility functions. |

## Frontend Integration

- The frontend connects via Socket.IO to receive real-time build progress, streaming chat tokens, and error notifications.
- Events are scoped to flow-specific rooms.
