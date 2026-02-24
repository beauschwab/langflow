# components/logic/ — Logic & Control Flow Components

## Purpose
Control flow components that manage execution routing, looping, sub-flow invocation, and inter-component communication within flows.

## Key Files

| File | Description |
|------|-------------|
| `conditional_router.py` | Conditional router — routes messages based on text matching or LLM evaluation. |
| `data_conditional_router.py` | Data conditional router — routes based on data field values. |
| `loop.py` | Loop component — enables iterative processing with cycle edges. |
| `listen.py` | Listen component — subscribes to notifications from Notify components. |
| `notify.py` | Notify component — sends notifications to Listen components. |
| `pass_message.py` | Pass-through message component. |
| `flow_tool.py` | Flow-as-tool component — exposes a flow as a callable tool for agents. |
| `run_flow.py` | Run Flow component — executes another flow as a sub-flow. |
| `sub_flow.py` | Sub-flow component — embeds a flow within another flow. |
