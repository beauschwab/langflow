# base/ — Component Base Classes

## Purpose
Contains abstract base classes and mixins that all concrete Langflow components extend. Each subdirectory defines the base class for a specific component category (agents, models, tools, embeddings, etc.). These base classes standardize the component interface, define common inputs/outputs, and provide shared functionality.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `agents/` | Base class for agent components — `AgentComponent`. Includes agent execution, tool binding, and CrewAI integration. |
| `astra_assistants/` | Utilities for DataStax Astra Assistants integration. |
| `chains/` | Base class for LangChain chain components. |
| `compressors/` | Base class for document compressor components. |
| `curl/` | cURL command parser for API request components. |
| `data/` | Base class for data/file loading components. |
| `document_transformers/` | Base class for document transformer components. |
| `embeddings/` | Base class for embedding model components. |
| `flow_processing/` | Utilities for flow-level processing. |
| `huggingface/` | HuggingFace model bridge utilities. |
| `io/` | Base classes for input/output components (ChatInput, ChatOutput, TextInput, TextOutput). |
| `langchain_utilities/` | Base class for LangChain utility components. |
| `mcp/` | Model Context Protocol (MCP) client utilities. |
| `memory/` | Base class for memory/chat history components. |
| `models/` | Base class for LLM/chat model components — `LCModelComponent`. Includes provider-specific constants. |
| `prompts/` | Base class for prompt template components. |
| `textsplitters/` | Base class for text splitter components. |
| `tools/` | Base class for tool components — `ComponentTool`, `FlowTool`. |
| `vectorstores/` | Base class for vector store components. |

## Key Files (at this level)

| File | Description |
|------|-------------|
| `__init__.py` | Exports all base classes. |
| `constants.py` | Shared constants for base classes. |

## For LLM Coding Agents

- When creating a new component, identify the correct base class from this directory.
- Base classes define the `build()` method signature and standard inputs that all components of that type share.
- The `io/` subdirectory contains `ChatInput` and `ChatOutput` — the primary user-facing I/O components.
