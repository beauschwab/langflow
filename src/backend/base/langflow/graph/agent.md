# graph/ — Graph Execution Engine

## Purpose
The core runtime engine that executes Langflow flows. A flow is represented as a directed graph of vertices (components) connected by edges (data/control connections). This package handles graph construction, topological scheduling, vertex execution, state management, and cycle detection.

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `edge/` | Edge classes that represent connections between vertices. |
| `graph/` | The main `Graph` class, scheduling (`RunnableVerticesManager`), and state management. |
| `state/` | Graph-level state model for shared state across vertices. |
| `vertex/` | Vertex classes that wrap individual components in the graph. |
| `schema.py` | Shared graph-level schemas (`RunOutputs`, etc.). |
| `utils.py` | Graph-level utility functions. |

## Key Concepts

- **Graph** (`graph/base.py`): The central class. `Graph.arun()` is the main async execution entry point.
- **Vertex** (`vertex/base.py`): Wraps a component and manages its build lifecycle.
- **Edge** (`edge/base.py`): Connects two vertices; `CycleEdge` handles loop-back edges.
- **RunnableVerticesManager** (`graph/runnable_vertices_manager.py`): Determines which vertices are ready to execute based on dependency resolution.
- **GraphStateManager** (`graph/state_manager.py`): Manages shared mutable state across the graph execution.

## Execution Flow

1. Flow JSON → `Graph.__init__()` parses nodes/edges
2. `Graph.arun()` → topological sort → `RunnableVerticesManager` yields ready vertices
3. Each vertex calls its component's `build()` method
4. Results propagate along edges to downstream vertices
5. Events are emitted via `EventManager` for real-time streaming to the frontend

## Frontend Integration

- The frontend sends flow JSON to `/api/v1/build/{flow_id}/flow`
- Build progress events stream back via Socket.IO
- Each vertex build result is sent as a playground event
