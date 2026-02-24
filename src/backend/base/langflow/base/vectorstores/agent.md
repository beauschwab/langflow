# base/vectorstores/ — Vector Store Base Class

## Purpose
Defines the base class for vector store components used in RAG (Retrieval-Augmented Generation) pipelines.

## Key Files

| File | Description |
|------|-------------|
| `model.py` | Vector store component base class with standard search/ingest interface. |
| `utils.py` | Vector store utility functions. |
| `vector_store_connection_decorator.py` | Decorator for managing vector store connections. |

## For LLM Coding Agents

- When adding a new vector store integration, extend the base class here and create a component in `components/vectorstores/`.
