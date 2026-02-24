# LangChain Deep Agents Harness: Architecture Analysis and Adaptation Plan

## Executive summary

LangChain's [Deep Agents](https://github.com/langchain-ai/deepagents) library is a batteries-included agent harness built on top of LangGraph. It provides planning, virtual filesystem, sub-agent delegation, context summarization, persistent memory, and skills — all wired together as composable middleware around a LangGraph `StateGraph` runtime.

This document compares the Deep Agents architecture with Langflow's current agent implementation, identifies the key differences, and recommends concrete adaptations that can bring Deep Agents capabilities to agents created in the Langflow app while preserving the existing LangGraph backend integration and Langflow component/tool ecosystem.

## Repository locations reviewed

### Langflow (this repository)
- `src/backend/base/langflow/base/agents/agent.py` — `LCAgentComponent`, `LCToolsAgentComponent`
- `src/backend/base/langflow/base/agents/events.py` — Agent event streaming and processing
- `src/backend/base/langflow/base/agents/context.py` — `AgentContext` state model
- `src/backend/base/langflow/base/agents/callback.py` — `AgentAsyncHandler` callback handler
- `src/backend/base/langflow/base/agents/utils.py` — Agent factory specs (Tool Calling, XML, OpenAI Tools, JSON Chat)
- `src/backend/base/langflow/components/agents/agent.py` — `AgentComponent` (concrete agent component)
- `src/backend/base/langflow/processing/orchestrator.py` — LangGraph `StateGraph` orchestrator
- `src/backend/base/langflow/processing/process.py` — `run_graph_internal` entry point
- `src/backend/base/langflow/graph/graph/base.py` — Core `Graph._run()` execution engine

### LangChain Deep Agents (external: `langchain-ai/deepagents`)
- `libs/deepagents/deepagents/graph.py` — `create_deep_agent()` factory and `BASE_AGENT_PROMPT`
- `libs/deepagents/deepagents/__init__.py` — Public API surface
- `libs/deepagents/deepagents/middleware/` — Middleware implementations:
  - `filesystem.py` — File read/write/edit/search tools
  - `subagents.py` — Sub-agent spawning and delegation
  - `summarization.py` — Context window management
  - `memory.py` — Persistent cross-session memory
  - `skills.py` — Dynamic skill/tool registry
  - `patch_tool_calls.py` — Message history consistency
- `libs/deepagents/deepagents/backends/` — Pluggable storage/execution backends
- `libs/deepagents/deepagents/base_prompt.md` — Base system prompt template

---

## How LangChain Deep Agents work

### Core architecture

Deep Agents uses four layers:

1. **Entry points** — CLI (`deepagents-cli`), Python SDK (`create_deep_agent()`), ACP integration
2. **Core agent runtime** — A LangGraph `CompiledStateGraph` managing agent state, tool bindings, and execution
3. **Middleware layer** — Composable interceptors that modify agent behavior at lifecycle hooks
4. **Backend layer** — Pluggable storage and execution providers (in-memory, file system, sandboxed, remote)

### The `create_deep_agent()` factory

The primary entry point is `create_deep_agent()`, which assembles the full agent:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[my_custom_tool],
    system_prompt="You are a research assistant.",
)
# Returns a CompiledStateGraph
result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
```

Internally, `create_deep_agent()`:
1. Initializes the model (defaults to Claude Sonnet 4.5)
2. Creates a pluggable backend (defaults to `StateBackend`)
3. Assembles the middleware stack (planning, filesystem, sub-agents, summarization, caching, patching)
4. Builds a general-purpose sub-agent spec
5. Combines the base prompt with user system prompt
6. Calls `langchain.agents.create_agent()` with the assembled middleware
7. Returns a compiled LangGraph graph with `recursion_limit=1000`

### Middleware system

Each middleware implements lifecycle hooks that intercept and transform agent behavior:

| Order | Middleware | Purpose | Tools provided |
|-------|-----------|---------|---------------|
| 1 | `TodoListMiddleware` | Task planning and progress tracking | `write_todos` |
| 2 | `MemoryMiddleware` | Persistent cross-session memory via LangGraph Store | Memory injection |
| 3 | `SkillsMiddleware` | Dynamic skill/tool registry from filesystem sources | Skill loading |
| 4 | `FilesystemMiddleware` | Virtual filesystem for context persistence | `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep`, `execute` |
| 5 | `SubAgentMiddleware` | Hierarchical sub-agent delegation with isolated context | `task` |
| 6 | `SummarizationMiddleware` | Context window management and auto-summarization | Auto-triggered |
| 7 | `AnthropicPromptCachingMiddleware` | Prompt optimization for Anthropic models | Transparent |
| 8 | `PatchToolCallsMiddleware` | Consistent message history for tool calls | Transparent |

Middleware hooks include:
- `before_agent` — Runs before the agent LLM call
- `wrap_model_call` — Intercepts the model invocation
- `wrap_tool_call` — Intercepts tool execution

### Sub-agent pattern

Deep Agents can spawn **sub-agents** with isolated context windows:

```python
# The main agent can call the "task" tool to delegate work
# Each sub-agent gets its own middleware stack, context, and tools
# Results are returned to the parent agent
```

Sub-agents are defined as `SubAgent` specs (configuration dicts) or `CompiledSubAgent` (pre-compiled LangGraph graphs). Each sub-agent automatically receives its own middleware stack (TodoList, Filesystem, Summarization, Caching, Patching).

### Context management strategy

Deep Agents handles context overflow through multiple mechanisms:
1. **Virtual filesystem** — Large outputs are written to files instead of kept in message history
2. **Summarization** — When conversation length exceeds token thresholds, older messages are summarized
3. **Sub-agent isolation** — Each sub-agent operates in its own context window
4. **Planning tools** — Todo lists help the agent maintain task awareness across summarization boundaries

### Base prompt design

The base prompt (`BASE_AGENT_PROMPT`) is comprehensive and opinionated:
- Instructs the agent to be concise and direct
- Emphasizes "understand first, act, verify" workflow
- Encourages iterating rather than stopping partway
- Includes progress update guidance for longer tasks
- Teaches professional objectivity and accuracy-first behavior

---

## How Langflow agents work today

### Agent component hierarchy

```
Component (custom_component/component.py)
  └── LCAgentComponent (base/agents/agent.py)
        ├── Abstract base for all agents
        ├── Manages AgentExecutor lifecycle
        ├── Streams events via astream_events(v2)
        └── LCToolsAgentComponent
              ├── Adds tool handling (HandleInput for tools)
              ├── Builds AgentExecutor from tools + runnable
              └── AgentComponent (components/agents/agent.py)
                    ├── Concrete agent with LLM provider selection
                    ├── Memory integration via MemoryComponent
                    └── Dynamic build config for provider switching
```

### Execution flow

1. **API request** → `run_graph_internal()` in `processing/process.py`
2. **Orchestrator** → `run_graph_with_orchestrator()` creates a LangGraph `StateGraph` with a single `execute_graph` node
3. **Graph execution** → `Graph._run()` processes vertices in topological layers
4. **Agent vertex** → `AgentComponent.message_response()` is called when the agent vertex is built
5. **Agent execution** → Creates `AgentExecutor` from LangChain's `create_tool_calling_agent()`
6. **Event streaming** → `astream_events(v2)` produces events processed by `process_agent_events()`
7. **Message building** → Events are mapped to `ContentBlock` updates with `ToolContent` and `TextContent`

### Agent execution internals

The agent loop uses LangChain's `AgentExecutor`:

```python
# In LCAgentComponent.run_agent()
runnable = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=self.tools,
    handle_parsing_errors=True,
    verbose=True,
    max_iterations=15,
)
result = await process_agent_events(
    runnable.astream_events(input_dict, config={"callbacks": [...]}, version="v2"),
    agent_message,
    send_message_method,
)
```

### Event processing

Events from `astream_events` are categorized and handled:

| Event type | Handler | Purpose |
|-----------|---------|---------|
| `on_chain_start` | `handle_on_chain_start` | Initializes content blocks, records input |
| `on_chain_end` | `handle_on_chain_end` | Captures final output, marks complete |
| `on_chain_stream` | `handle_on_chain_stream` | Handles streaming output chunks |
| `on_tool_start` | `handle_on_tool_start` | Creates `ToolContent` block with input |
| `on_tool_end` | `handle_on_tool_end` | Updates `ToolContent` with output and duration |
| `on_tool_error` | `handle_on_tool_error` | Records tool errors |

### Agent context state

`AgentContext` (in `base/agents/context.py`) tracks:
- `tools` — Available tools dict
- `llm` — Language model instance (with `bind_tools()` support)
- `iteration` / `max_iterations` — Loop counters
- `thought`, `last_action`, `last_action_result` — Internal reasoning state
- `context_history` — Timestamped list of `(key, value, timestamp)` tuples

### LangGraph integration (orchestrator level)

The current LangGraph usage is minimal — a single-node `StateGraph`:

```python
# In orchestrator.py
workflow = StateGraph(OrchestratorState)
workflow.add_node("execute_graph", execute_graph)
workflow.set_entry_point("execute_graph")
workflow.add_edge("execute_graph", END)
app = workflow.compile()
result = await app.ainvoke({"run_configs": run_configs})
```

LangGraph is used as a wrapper around the existing `Graph._run()` execution engine, not as the agent's internal reasoning graph.

---

## Key differences between Deep Agents and Langflow agents

### 1. Agent runtime architecture

| Aspect | Deep Agents | Langflow |
|--------|------------|----------|
| **Agent loop** | LangGraph `StateGraph` with `create_agent()` — native LangGraph react agent | LangChain `AgentExecutor` with `astream_events()` |
| **Tool binding** | Model-level tool binding via LangGraph agent | `create_tool_calling_agent()` → `AgentExecutor` |
| **State management** | LangGraph state + checkpointer + store | `AgentContext` Pydantic model (per-execution) |
| **Middleware** | Composable middleware stack with lifecycle hooks | None — behavior is hardcoded in component hierarchy |
| **Sub-agents** | First-class `SubAgentMiddleware` with isolated contexts | Not supported (agents are monolithic vertices) |

### 2. Planning and task decomposition

| Aspect | Deep Agents | Langflow |
|--------|------------|----------|
| **Task planning** | Built-in `TodoListMiddleware` with `write_todos` tool | No planning capability |
| **Progress tracking** | Todo list persisted via backend, survives summarization | No progress tracking |
| **Task decomposition** | Agent can break down complex goals into tracked subtasks | Agent reasons in a single pass with max iteration limit |

### 3. Context and memory management

| Aspect | Deep Agents | Langflow |
|--------|------------|----------|
| **Context overflow** | `SummarizationMiddleware` auto-summarizes when tokens exceed threshold | Fixed `max_iterations` limit (default 15), no summarization |
| **Persistent memory** | `MemoryMiddleware` with LangGraph Store for cross-session memory | `MemoryComponent` retrieves chat history for current session |
| **File-based context** | `FilesystemMiddleware` offloads large outputs to virtual files | No file-based context management |
| **Context isolation** | Sub-agents get their own context windows | All tools share the same context window |

### 4. Tool and skill management

| Aspect | Deep Agents | Langflow |
|--------|------------|----------|
| **Built-in tools** | File ops, shell, todos, sub-agent delegation | User-configured tools via HandleInput |
| **Dynamic skills** | `SkillsMiddleware` loads tools from filesystem sources at runtime | Static tool configuration at build time |
| **Tool interception** | `wrap_tool_call` middleware hook for validation/transformation | Direct tool execution via AgentExecutor |

### 5. System prompt and agent behavior

| Aspect | Deep Agents | Langflow |
|--------|------------|----------|
| **Base prompt** | Comprehensive, opinionated prompt teaching tool usage patterns | Simple "You are a helpful assistant" default |
| **Prompt composition** | User prompt + base prompt concatenated | User-configurable `system_prompt` field |
| **Behavioral guidance** | Explicit instructions for planning, verification, progress updates | No behavioral scaffolding beyond tool access |

### 6. LangGraph depth of integration

| Aspect | Deep Agents | Langflow |
|--------|------------|----------|
| **Agent graph** | Agent IS a LangGraph graph — uses `create_agent()` to build a full StateGraph with tool nodes, conditional edges | Agent uses `AgentExecutor` (legacy LangChain pattern) |
| **Orchestrator graph** | N/A (agent is the graph) | Minimal single-node StateGraph wrapper around `Graph._run()` |
| **Checkpointing** | Native LangGraph checkpointer support for resumability | No checkpointing at agent level |
| **Streaming** | LangGraph native streaming | `astream_events(v2)` on AgentExecutor |

---

## Adaptation recommendations

The following adaptations would bring Deep Agents capabilities to Langflow agents while preserving the existing component/tool ecosystem, flow builder UX, and LangGraph backend integration.

### Phase 1: Middleware-inspired agent enhancements (minimal change)

These changes enhance the existing `AgentComponent` without restructuring the agent runtime.

#### 1a. Add planning capability via TodoList tool

Add a built-in planning tool to `AgentComponent`, similar to Deep Agents' `write_todos`:

- Create a `TodoListComponent` in `components/helpers/` that provides a `write_todos` structured tool
- Add an `add_planning_tool` BoolInput to `AgentComponent` (similar to existing `add_current_date_tool`)
- When enabled, inject the planning tool into the agent's tool list
- Store todo state in agent message content blocks for UI visibility

**Impact**: Enables task decomposition and progress tracking without changing agent architecture.

#### 1b. Enhance system prompt with behavioral scaffolding

Update the default `system_prompt` in `AgentComponent` to include Deep Agents-style behavioral guidance:

- "Understand first, act, verify" workflow instructions
- Concise communication style guidance
- Progress update instructions for multi-step tasks
- Tool usage patterns and best practices

**Impact**: Improves agent behavior quality with no code changes to the runtime.

### Phase 2: Context management improvements (moderate change)

#### 2a. Add context summarization support

Implement conversation summarization to handle long agent interactions:

- Add a `SummarizationComponent` that can summarize chat history when it exceeds a token threshold
- Integrate with `MemoryComponent` to provide summarized context rather than raw history
- Add `max_context_tokens` parameter to `AgentComponent` to control when summarization triggers

**Impact**: Prevents context overflow for complex, multi-step agent tasks.

#### 2b. Enhance persistent memory

Extend `MemoryComponent` integration to support cross-session persistent memory:

- Add ability to persist key learnings/notes across sessions
- Use existing database infrastructure for memory storage
- Allow agent to read/write persistent notes via a dedicated tool

**Impact**: Enables long-horizon workflows that span multiple sessions.

### Phase 3: Sub-agent delegation (significant change)

#### 3a. Add sub-agent support as a tool

Create a `SubAgentTool` component that allows agents to delegate work:

- Build a `SubAgentComponent` that wraps another `AgentComponent` invocation
- Provide context isolation — sub-agent gets its own tool set and context window
- Return sub-agent results to the parent agent
- Expose as a standard Langflow tool that can be connected to agent tool inputs

**Impact**: Enables hierarchical agent architectures for complex workflows.

#### 3b. Add filesystem context tools

Create filesystem-like tools for context management:

- `WriteContextTool` — Save intermediate results/notes to persistent storage
- `ReadContextTool` — Retrieve saved context
- These map to database-backed storage rather than actual filesystem

**Impact**: Allows agents to manage their own context more effectively.

### Phase 4: Native LangGraph agent runtime (architectural change)

#### 4a. Migrate from AgentExecutor to LangGraph react agent

Replace the LangChain `AgentExecutor` pattern with LangGraph's native `create_react_agent()`:

- Replace `AgentExecutor.from_agent_and_tools()` with `langgraph.prebuilt.create_react_agent()`
- Preserve existing event streaming by adapting to LangGraph's streaming interface
- Maintain backward compatibility with existing `ContentBlock` and `ToolContent` message format
- Add support for LangGraph checkpointing at the agent level

**Impact**: Aligns agent internals with LangGraph patterns, enables checkpointing, and positions for middleware support.

#### 4b. Add middleware support to agent components

Implement a middleware system for Langflow agent components:

- Define a `AgentMiddleware` protocol with `before_agent`, `wrap_model_call`, `wrap_tool_call` hooks
- Allow middleware to be connected to agents via HandleInput
- Create middleware components for planning, summarization, and context management
- This mirrors Deep Agents' middleware system but expressed as Langflow components

**Impact**: Makes agent behavior composable and extensible through the flow builder.

---

## Implementation priorities

For the stated goal of adapting Deep Agents patterns to the Langflow LangGraph backend:

| Priority | Recommendation | Effort | Impact |
|----------|---------------|--------|--------|
| **High** | Phase 1b: Enhanced system prompt | Low | High — immediate behavior improvement |
| **High** | Phase 1a: Planning tool | Low | High — enables task decomposition |
| **Medium** | Phase 2a: Context summarization | Medium | High — solves context overflow |
| **Medium** | Phase 2b: Persistent memory | Medium | Medium — enables long-horizon work |
| **Medium** | Phase 3b: Filesystem context tools | Medium | Medium — better context management |
| **Lower** | Phase 3a: Sub-agent delegation | High | High — but requires significant architecture |
| **Lower** | Phase 4a: LangGraph react agent | High | High — but significant migration effort |
| **Lower** | Phase 4b: Middleware system | High | High — most architectural change |

## Key architectural boundaries to preserve

- Existing REST and stream interfaces (`api/v1/endpoints.py`, `api/build.py`, chat build endpoints)
- Existing component contracts and tool definitions
- Existing flow serialization format consumed by UI and backend
- Existing `Graph._run()` execution engine and topological vertex scheduling
- Existing event contract (`PlaygroundEvent`, `MessageEvent`, `ErrorEvent`, `TokenEvent`)
- Current `ContentBlock` / `ToolContent` message format for UI rendering

## Risks and mitigations

- **Risk**: Deep Agents middleware patterns may not map cleanly to Langflow's component-based architecture.
  - **Mitigation**: Express middleware as composable Langflow components rather than requiring a new middleware protocol.

- **Risk**: Sub-agent delegation could create unbounded recursion or resource consumption.
  - **Mitigation**: Enforce depth limits and resource budgets at the sub-agent boundary.

- **Risk**: Context summarization may lose important information.
  - **Mitigation**: Use Deep Agents' approach of keeping recent messages intact and only summarizing older history.

- **Risk**: Migrating from AgentExecutor to LangGraph react agent may break existing event streaming.
  - **Mitigation**: Phase the migration behind a feature flag and maintain AgentExecutor as fallback.

## References

- [LangChain Deep Agents Repository](https://github.com/langchain-ai/deepagents)
- [Deep Agents Documentation](https://docs.langchain.com/oss/python/deepagents/overview)
- [Deep Agents Architecture Overview (DeepWiki)](https://deepwiki.com/langchain-ai/deepagents/1.3-architecture-overview)
- [LangGraph create_react_agent](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)
- Langflow existing research: `docs/research/python-backend-langgraph-deep-dive.md`
