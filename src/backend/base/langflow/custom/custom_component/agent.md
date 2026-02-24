# custom/custom_component/ — Core Component Classes

## Purpose
Defines the core component class hierarchy that all Langflow components extend.

## Key Files

| File | Description |
|------|-------------|
| `component.py` | `Component` class — the main base class for all components. Defines the component lifecycle: `build()`, inputs/outputs, and result handling. |
| `base_component.py` | `BaseComponent` — lower-level base with metadata, display name, and description handling. |
| `custom_component.py` | `CustomComponent` — adds custom code execution capabilities on top of `Component`. |
| `component_with_cache.py` | `ComponentWithCache` — adds caching behavior for expensive operations. |

## For LLM Coding Agents

- The inheritance chain is: `BaseComponent` → `CustomComponent` → `Component`.
- All concrete components in `components/` extend `Component` (or a category-specific base that extends `Component`).
