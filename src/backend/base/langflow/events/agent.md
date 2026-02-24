# events/ — Event Management

## Purpose
Publish/subscribe event system used during graph execution to emit real-time events (vertex builds, streaming tokens, errors) to the frontend via Socket.IO.

## Key Files

| File | Description |
|------|-------------|
| `event_manager.py` | `EventManager` — central event bus. Components and the graph engine emit events; the Socket.IO service subscribes and forwards them to connected clients. |

## Frontend Integration

- Events flow: Component → EventManager → SocketIO Service → Frontend WebSocket
- Event types include: vertex build start/end, streaming tokens, errors, playground events.
