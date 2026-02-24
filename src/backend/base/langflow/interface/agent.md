# interface/ — Component Registry and Initialization

## Purpose
Manages the component type registry — discovers, categorizes, and serves all available component types to the frontend. Also handles component initialization and LLM caching setup.

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `importing/` | Dynamic import utilities for loading component classes. |
| `initialize/` | Component initialization and instantiation logic. |
| `components.py` | `get_and_cache_all_types_dict()` — builds the complete component type dictionary served to the frontend sidebar. Handles enterprise component filtering. |
| `listing.py` | Component listing and categorization. |
| `run.py` | Memory key management for LangChain objects. |
| `utils.py` | `setup_llm_caching()` and other interface utilities. |

## Frontend Integration

- `GET /api/v1/all` calls `get_and_cache_all_types_dict()` to return all component types.
- The frontend sidebar is built from this response.
- Enterprise mode can filter which components are shown via `enterprise_first_pass_components_only` setting.
