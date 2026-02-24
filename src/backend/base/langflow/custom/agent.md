# custom/ — Custom Component Infrastructure

## Purpose
Infrastructure for parsing, validating, and executing user-defined custom components. Handles Python code analysis, component class discovery, and directory-based component loading.

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `code_parser/` | Python AST-based code parser for extracting component class definitions from user code. |
| `custom_component/` | Core custom component classes — `BaseComponent`, `Component`, `CustomComponent`. |
| `directory_reader/` | Scans directories for custom component files. |
| `attributes.py` | Component attribute definitions and validation. |
| `eval.py` | Safe evaluation utilities for custom component code. |
| `schema.py` | Custom component schema definitions. |
| `tree_visitor.py` | AST tree visitor for analyzing custom component code structure. |
| `utils.py` | Custom component utility functions. |

## For LLM Coding Agents

- `custom_component/component.py` defines the `Component` class that all Langflow components ultimately extend.
- The code parser uses Python's `ast` module for safe code analysis — no `eval()` of arbitrary code.
- Directory reader enables loading components from external directories via `LANGFLOW_COMPONENTS_PATH`.
