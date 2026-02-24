# components/ — Concrete Component Implementations

## Purpose
Contains all built-in Langflow components that users can drag onto the flow canvas. Each subdirectory represents a component category visible in the frontend sidebar. Components extend base classes from `base/` and implement specific integrations.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `agents/` | Agent components — pre-configured AI agent implementations. |
| `chains/` | LangChain chain components (currently minimal). |
| `confluence/` | Atlassian Confluence integration components. |
| `custom_component/` | The "Custom Component" meta-component for user-defined Python code. |
| `data/` | Data loading components — API requests, CSV, JSON, SQL, file upload, URL scraping, webhooks. |
| `deactivated/` | Deprecated/disabled components kept for backward compatibility. Not shown in the UI. |
| `documentloaders/` | Document loader components (currently uses registry from `__init__.py`). |
| `embeddings/` | Text embedding model components — OpenAI, Ollama, Azure, HuggingFace, Mistral, etc. |
| `helpers/` | Helper/utility components — memory management, output parsing, structured output, batch run. |
| `inputs/` | User input components — ChatInput, TextInput. |
| `link_extractors/` | Link extraction components (currently minimal). |
| `logic/` | Logic/control flow components — conditional router, loop, listen/notify, sub-flow, run flow. |
| `memories/` | Chat memory components — AstraDB, Cassandra, Redis, Zep. |
| `models/` | LLM/chat model components — OpenAI, Anthropic, Ollama, Groq, AWS Bedrock, Azure, DeepSeek, etc. |
| `output_parsers/` | Output parser components (currently uses registry). |
| `outputs/` | Output components — ChatOutput, TextOutput. |
| `processing/` | Data processing components — text combining, data filtering, JSON parsing, regex, merge, DataFrame operations. |
| `prompts/` | Prompt template components. |
| `prototypes/` | Experimental/prototype components — Python function executor. |
| `retrievers/` | Retriever components — Amazon Kendra, Metal, Multi-Query. |
| `sharepoint/` | Microsoft SharePoint integration components. |
| `textsplitters/` | Text splitting components (uses registry). |
| `toolkits/` | Toolkit components (uses registry). |
| `tools/` | Tool components — search APIs (DuckDuckGo, Tavily, SearXNG, Bing, Serp), calculators, Python REPL, AstraDB CQL, MCP, Arxiv. |
| `vectorstores/` | Vector store components — AstraDB, Chroma, FAISS, Pinecone, Qdrant, PGVector, Milvus, MongoDB Atlas, Redis, etc. |

## For LLM Coding Agents

- **Adding a new component**: Create a Python file in the appropriate category folder, extend the matching base class from `base/`, and export it in the folder's `__init__.py`.
- Each component file typically defines one class with `display_name`, `description`, `icon`, `inputs`, `outputs`, and a `build_*()` method.
- Components are auto-discovered by the interface registry in `interface/components.py`.
- The frontend sidebar categories map directly to these folder names.
