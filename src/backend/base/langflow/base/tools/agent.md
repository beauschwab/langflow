# base/tools/ — Tool Base Classes

## Purpose
Defines base classes for tool components that agents can invoke. Includes both standalone tools and flow-as-tool wrappers.

## Key Files

| File | Description |
|------|-------------|
| `base.py` | Tool component base class. |
| `component_tool.py` | `ComponentTool` — wraps a Langflow component as a LangChain tool that agents can call. |
| `flow_tool.py` | `FlowTool` — wraps an entire Langflow flow as a callable tool. |
| `run_flow.py` | Utilities for running flows as tools. |
| `constants.py` | Tool-related constants. |

## For LLM Coding Agents

- `ComponentTool` is how agents invoke other components in the flow.
- `FlowTool` enables the "Run Flow" component that calls sub-flows.
