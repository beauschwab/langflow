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

---

## Deep Agent node design for flow designer

This section describes a concrete design for a custom Deep Agent node in the Langflow flow designer that exposes the planning, context management, sub-agent delegation, and enhanced prompt capabilities from the Deep Agents harness. It also covers integration as a template in the agents page manager framework.

### Design approach

The Deep Agent node extends the existing `AgentComponent` pattern rather than replacing it. It reuses the proven dynamic model provider selection, tool HandleInput, and memory integration while adding new capability toggles and configuration surfaces. This follows the same `BoolInput` toggle pattern used by the existing `add_current_date_tool` input.

### Node inputs specification

The `DeepAgentComponent` node exposes the following inputs, organized into logical groups. Inputs marked `advanced=True` are hidden by default and appear in the node's advanced settings panel or when an edge is connected.

#### Core inputs (always visible)

| Input name | Type | Default | Description |
|-----------|------|---------|-------------|
| `agent_llm` | DropdownInput | `"OpenAI"` | Model provider selection (same as current Agent) with `real_time_refresh=True` |
| `system_prompt` | MultilineInput | Enhanced Deep Agent prompt | Agent instructions with built-in behavioral scaffolding |
| `tools` | HandleInput | `[]` | External tools connected from other nodes |
| `input_value` | MessageTextInput | `""` | User task/input for the agent |

#### Capability toggles (visible, grouped)

| Input name | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable_planning` | BoolInput | `True` | Adds `write_todos` tool for task breakdown and progress tracking |
| `enable_context_tools` | BoolInput | `True` | Adds `write_context` / `read_context` tools for intermediate result persistence |
| `enable_sub_agents` | BoolInput | `False` | Adds `delegate_task` tool for spawning isolated sub-agent workers |
| `enable_summarization` | BoolInput | `False` | Enables auto-summarization when context exceeds token threshold |

#### Advanced configuration (hidden by default)

| Input name | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_iterations` | IntInput | `25` | Maximum agent loop iterations (higher default than standard Agent's 15) |
| `max_context_tokens` | IntInput | `100000` | Token threshold that triggers summarization (requires `enable_summarization`) |
| `summarization_keep_recent` | IntInput | `10` | Number of recent messages to preserve during summarization |
| `sub_agent_max_depth` | IntInput | `2` | Maximum sub-agent nesting depth (requires `enable_sub_agents`) |
| `sub_agent_max_iterations` | IntInput | `15` | Max iterations per sub-agent |
| `add_current_date_tool` | BoolInput | `True` | Adds current date tool (same as current Agent) |
| `handle_parsing_errors` | BoolInput | `True` | Error recovery mode |
| `verbose` | BoolInput | `True` | Logging verbosity |
| Memory inputs | (from MemoryComponent) | — | Chat history configuration |

### Node outputs

| Output name | Type | Description |
|------------|------|-------------|
| `response` | Message | Final agent response with `ContentBlock` steps |

### Dynamic field behavior

The node uses `update_build_config()` to show/hide fields based on capability toggles:

- When `enable_summarization` is toggled ON → `max_context_tokens` and `summarization_keep_recent` become visible
- When `enable_sub_agents` is toggled ON → `sub_agent_max_depth` and `sub_agent_max_iterations` become visible
- When `enable_planning` or `enable_context_tools` is toggled, no additional fields appear — they simply inject/remove the respective built-in tools

This mirrors the existing pattern where `agent_llm` dropdown dynamically shows/hides provider-specific fields via `real_time_refresh`.

### Built-in tools injected by capability toggles

#### Planning (`enable_planning=True`)

```
write_todos tool:
  - Input: { todos: list[{task: str, status: "pending"|"in_progress"|"done"}] }
  - Output: Formatted todo list string
  - Stored in: Agent message content_blocks as a dedicated TodoContent block
```

The agent can call `write_todos` at any point to create, update, or check off tasks. The todo state is rendered in the playground UI as a checklist within the agent's response card.

#### Context tools (`enable_context_tools=True`)

```
write_context tool:
  - Input: { key: str, value: str }
  - Output: Confirmation string
  - Stored in: Session-scoped key-value store (database-backed)

read_context tool:
  - Input: { key: str }
  - Output: Stored value string
  - Reads from: Same session-scoped store
```

These tools allow the agent to offload intermediate results, notes, and large outputs outside of the message history, preventing context overflow.

#### Sub-agent delegation (`enable_sub_agents=True`)

```
delegate_task tool:
  - Input: { task: str, context: str | None }
  - Output: Sub-agent's final response string
  - Behavior: Spawns a new AgentComponent with isolated context
  - Constraints: Respects sub_agent_max_depth, sub_agent_max_iterations
```

The sub-agent inherits the parent's LLM model and external tools but operates in a fresh context window. Results are returned as a string to the parent agent.

### Enhanced default system prompt

The `system_prompt` default value is upgraded from the basic "You are a helpful assistant" to a structured behavioral prompt inspired by Deep Agents:

```
You are an intelligent assistant with access to tools for completing tasks.

## How to work

1. **Understand first** — Read the user's request carefully. If ambiguous, ask for clarification.
2. **Plan** — For complex tasks, use write_todos to break the work into steps.
3. **Act** — Execute each step using available tools. Work accurately and efficiently.
4. **Verify** — Check your work against what was asked. Iterate if needed.

## Communication style

- Be concise and direct. Avoid unnecessary preamble.
- Don't say "I'll now do X" — just do it.
- For longer tasks, provide brief progress updates.

## Tool usage

- Use tools when they can help. Don't guess when a tool can provide the answer.
- If a tool fails, analyze why before retrying with a different approach.
- Save intermediate results with write_context if they'll be needed later.
```

### Node visual design

The node renders in the flow designer with:
- **Icon**: `bot` (same as current Agent, from the `agents` SIDEBAR_CATEGORY)
- **Color**: Purple (`#903BBE` — the existing `agents` category color)
- **Display name**: "Deep Agent"
- **Capability badges**: Small toggle indicators for enabled capabilities (Planning ✓, Context ✓, Sub-agents ✗, Summarization ✗)
- **Tool handles**: Same left-side HandleInput for connecting external tools

### Backend component class structure

```python
class DeepAgentComponent(LCToolsAgentComponent):
    display_name = "Deep Agent"
    description = "Advanced agent with planning, context management, and sub-agent delegation."
    icon = "bot"
    name = "DeepAgent"

    inputs = [
        # Core: model provider, system prompt, tools, input
        DropdownInput(name="agent_llm", ...),  # same as AgentComponent
        MultilineInput(name="system_prompt", value=DEEP_AGENT_PROMPT, ...),
        *LCToolsAgentComponent._base_inputs,

        # Capability toggles
        BoolInput(name="enable_planning", display_name="Planning", value=True,
                  info="Adds write_todos tool for task breakdown and progress tracking."),
        BoolInput(name="enable_context_tools", display_name="Context Tools", value=True,
                  info="Adds write_context/read_context tools for intermediate result persistence."),
        BoolInput(name="enable_sub_agents", display_name="Sub-Agents", value=False,
                  info="Adds delegate_task tool for spawning isolated sub-agent workers."),
        BoolInput(name="enable_summarization", display_name="Summarization", value=False,
                  info="Auto-summarizes conversation when context exceeds token threshold.",
                  real_time_refresh=True),

        # Advanced config
        IntInput(name="max_context_tokens", value=100000, advanced=True, ...),
        IntInput(name="summarization_keep_recent", value=10, advanced=True, ...),
        IntInput(name="sub_agent_max_depth", value=2, advanced=True, ...),
        IntInput(name="sub_agent_max_iterations", value=15, advanced=True, ...),
        *memory_inputs,
        BoolInput(name="add_current_date_tool", value=True, advanced=True, ...),
    ]

    async def message_response(self) -> Message:
        # 1. Build LLM model (same as AgentComponent)
        # 2. Retrieve memory/chat history
        # 3. Inject capability tools based on toggles
        # 4. Optionally wrap with summarization
        # 5. Run agent and return response
        ...
```

---

## Agents page template integration

The Deep Agent node integrates with the agents page manager framework as a pre-configured agent template. This bridges the flow designer (where users build custom agent graphs) with the agents page (where users manage reusable agent definitions).

### Agent template system design

#### Template definitions

Extend `constants.ts` with agent template presets that map to pre-configured `config` values on the Agent database model:

```typescript
// src/frontend/src/pages/AgentsPage/components/constants.ts

export const AGENT_TEMPLATES = [
  {
    id: "deep_agent_research",
    name: "Research Agent",
    description: "Plans research tasks, searches multiple sources, and synthesizes findings into structured reports.",
    agent_type: "deep_agent",
    config: {
      enable_planning: true,
      enable_context_tools: true,
      enable_sub_agents: true,
      enable_summarization: true,
      max_iterations: 30,
      system_prompt: "You are a research assistant. Break complex research into subtasks, search thoroughly, and synthesize findings into clear reports.",
    },
    tools: [],
    tags: ["research", "planning"],
    icon: "Search",
  },
  {
    id: "deep_agent_coding",
    name: "Coding Assistant",
    description: "Plans implementation tasks, writes and reviews code, and manages context across files.",
    agent_type: "deep_agent",
    config: {
      enable_planning: true,
      enable_context_tools: true,
      enable_sub_agents: false,
      enable_summarization: true,
      max_iterations: 25,
      system_prompt: "You are a coding assistant. Plan implementation carefully, write clean code, and verify your work.",
    },
    tools: [],
    tags: ["coding", "development"],
    icon: "Code",
  },
  {
    id: "deep_agent_data",
    name: "Data Analysis Agent",
    description: "Analyzes data, generates insights, and creates structured summaries with intermediate result tracking.",
    agent_type: "deep_agent",
    config: {
      enable_planning: true,
      enable_context_tools: true,
      enable_sub_agents: false,
      enable_summarization: false,
      max_iterations: 20,
      system_prompt: "You are a data analyst. Examine data carefully, track intermediate findings, and produce clear insights.",
    },
    tools: [],
    tags: ["data", "analytics"],
    icon: "BarChart",
  },
  {
    id: "standard_agent",
    name: "Standard Agent",
    description: "Simple tool-calling agent without planning or context management. Best for straightforward tasks.",
    agent_type: "tool_calling",
    config: {
      enable_planning: false,
      enable_context_tools: false,
      enable_sub_agents: false,
      enable_summarization: false,
      max_iterations: 15,
    },
    tools: [],
    tags: ["simple", "tool-calling"],
    icon: "Bot",
  },
];
```

#### Updated CreateAgentDialog

The Create Agent dialog adds a template selection step before the configuration form:

```
┌──────────────────────────────────────────────────┐
│  Create Agent                                     │
│                                                   │
│  Choose a template                                │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────┐ │
│  │ 🔍 Research │ │ 💻 Coding   │ │ 📊 Data    │ │
│  │ Agent       │ │ Assistant   │ │ Analysis   │ │
│  │             │ │             │ │            │ │
│  │ Plans tasks,│ │ Plans impl, │ │ Analyzes   │ │
│  │ researches, │ │ writes code │ │ data, gen  │ │
│  │ synthesizes │ │ reviews     │ │ insights   │ │
│  └─────────────┘ └─────────────┘ └────────────┘ │
│  ┌─────────────┐ ┌─────────────┐                 │
│  │ 🤖 Standard │ │ ✨ Custom   │                 │
│  │ Agent       │ │             │                 │
│  │             │ │ Start from  │                 │
│  │ Simple tool │ │ scratch     │                 │
│  │ calling     │ │             │                 │
│  └─────────────┘ └─────────────┘                 │
│                                                   │
│  ─── Configuration ───                            │
│  Name *:        [My Research Agent          ]     │
│  Description:   [Describe what this agent...]     │
│                                                   │
│  ─── Capabilities ───                             │
│  Planning:        [✓]                             │
│  Context Tools:   [✓]                             │
│  Sub-Agents:      [✓]                             │
│  Summarization:   [✓]                             │
│                                                   │
│  ─── Tools ───                                    │
│  [SharePoint Files Loader] [+ Add Tool]           │
│                                                   │
│            [Cancel]  [Create Agent]               │
└──────────────────────────────────────────────────┘
```

#### "Open in Flow Designer" action

Each agent in the agents page gets an "Open in Flow Designer" button that:

1. Creates a new flow with a pre-configured `DeepAgentComponent` node
2. Populates the node's inputs from the agent's `config` JSON
3. Links the agent record to the flow via `flow_id` foreign key
4. Opens the flow in the flow designer for further customization

This bridges the manager view (agents page) with the builder view (flow designer).

#### AgentCard enhancements

The `AgentCard` component is extended to show capability badges:

```
┌──────────────────────────────────────────────┐
│  Research Agent                    deep_agent │
│  Plans research tasks, searches multiple...  │
│                                              │
│  [Planning ✓] [Context ✓] [Sub-agents ✓]    │
│  [SharePoint Files Loader]                   │
│  [research] [planning]                       │
│                                              │
│  Edit  Open in Designer  Delete              │
└──────────────────────────────────────────────┘
```

### Agent `config` schema

The Agent model's `config: dict` field stores Deep Agent capability settings. The schema is:

```python
# Stored in Agent.config JSON column
{
    "enable_planning": bool,          # Default: True
    "enable_context_tools": bool,     # Default: True
    "enable_sub_agents": bool,        # Default: False
    "enable_summarization": bool,     # Default: False
    "max_iterations": int,            # Default: 25
    "max_context_tokens": int,        # Default: 100000
    "summarization_keep_recent": int, # Default: 10
    "sub_agent_max_depth": int,       # Default: 2
    "sub_agent_max_iterations": int,  # Default: 15
    "system_prompt": str,             # Default: DEEP_AGENT_PROMPT
}
```

When a user creates an agent from a template, the template's `config` is stored in the Agent record. When the agent is opened in the flow designer, these config values are mapped to the `DeepAgentComponent` node's input fields.

### Data flow: agents page → flow designer → execution

```
Agent Template Selection (agents page)
        │
        ▼
Agent Record Created (database: Agent model with config JSON)
        │
        ▼
"Open in Flow Designer" clicked
        │
        ▼
New Flow Created with DeepAgentComponent node
  - Node inputs populated from Agent.config
  - Agent.flow_id linked to new Flow
        │
        ▼
User customizes in Flow Designer
  - Add external tools (search, API, etc.)
  - Adjust capability toggles
  - Edit system prompt
  - Connect to other flow nodes
        │
        ▼
Flow Execution (run_graph_internal → orchestrator → Graph._run)
  - DeepAgentComponent vertex executes
  - Built-in tools injected based on toggles
  - AgentExecutor runs with enhanced tool set
  - Events streamed to playground UI
```

### Key design decisions

1. **Single node, not multiple nodes**: All Deep Agent capabilities are exposed as toggles on one node rather than separate component nodes. This matches how Deep Agents' `create_deep_agent()` assembles everything through a single factory with middleware parameters.

2. **Config-driven templates**: Agent templates are just pre-filled `config` values, not separate component classes. This keeps the component catalog clean and allows templates to be added without code changes.

3. **Backward compatible**: The existing `AgentComponent` ("Agent") remains unchanged. `DeepAgentComponent` ("Deep Agent") is a new, separate component in the same `agents` category. Users can use either.

4. **Progressive disclosure**: Capability toggles are visible by default for discoverability, but detailed configuration (token thresholds, depth limits) is hidden under `advanced=True`. Fields dynamically appear when their parent toggle is enabled via `real_time_refresh`.

5. **Database-backed context**: Unlike Deep Agents' virtual filesystem, Langflow's context tools use the existing database infrastructure. This avoids introducing new storage dependencies and works with the existing persistence layer.

---

## Sub-agents and context/skills: enablement details and backend changes

This section provides a concrete answer to how sub-agents and context/skills are enabled in both the flow designer UI and the agents page manager, and exactly what backend changes are required.

### How sub-agents are enabled

#### Flow designer UI

The `enable_sub_agents` toggle on the Deep Agent node controls sub-agent delegation. When the user toggles it ON:

1. **`update_build_config()`** fires (via `real_time_refresh`) and makes `sub_agent_max_depth` and `sub_agent_max_iterations` fields visible on the node
2. During execution, `message_response()` checks the toggle and injects the `delegate_task` StructuredTool into `self.tools`
3. The LLM can then call `delegate_task(task="...", context="...")` during its reasoning loop

```python
# In DeepAgentComponent.message_response()
if self.enable_sub_agents:
    delegate_tool = self._build_delegate_task_tool()
    self.tools.append(delegate_tool)
```

The tool itself spawns an isolated child `AgentExecutor`:

```python
def _build_delegate_task_tool(self) -> StructuredTool:
    parent_llm = self.llm
    max_depth = self.sub_agent_max_depth
    max_iters = self.sub_agent_max_iterations
    current_depth = getattr(self, "_sub_agent_depth", 0)

    # Capture parent's external tools (exclude delegate_task to prevent infinite recursion).
    # This list is built at tool-construction time from the tools already on self.tools.
    external_tools = [t for t in self.tools if t.name != "delegate_task"]

    async def delegate_task(task: str, context: str | None = None) -> str:
        next_depth = current_depth + 1
        if next_depth > max_depth:
            return f"Cannot delegate: maximum sub-agent depth ({max_depth}) reached."

        # Build sub-agent prompt
        sub_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a focused sub-agent. Complete the assigned task using available tools."),
            ("placeholder", "{chat_history}"),
            ("human", f"Context: {context or 'None'}\n\nTask: {task}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        # Create sub-agent with isolated context and incremented depth
        sub_agent = create_tool_calling_agent(parent_llm, external_tools, sub_prompt)
        sub_executor = AgentExecutor(
            agent=sub_agent,
            tools=external_tools,
            max_iterations=max_iters,
            handle_parsing_errors=True,
        )
        # Tag the executor so any nested delegate_task knows its depth
        sub_executor._sub_agent_depth = next_depth

        result = await sub_executor.ainvoke({"input": task})
        return result.get("output", "Sub-agent completed without output.")

    return StructuredTool.from_function(
        coroutine=delegate_task,
        name="delegate_task",
        description="Delegate a focused subtask to an isolated sub-agent. Use for independent work that doesn't need the full conversation context.",
        args_schema=DelegateTaskInput,  # Pydantic model with task: str, context: str | None
    )
```

**Key design**: The sub-agent inherits the parent's LLM and external tools but gets a fresh conversation context. It does NOT have access to the `delegate_task` tool itself (prevents infinite recursion). The `current_depth` counter enforces the configured `sub_agent_max_depth`.

#### Agent manager UI

In the agents page, sub-agents are controlled through the `config` JSON on the Agent model:

```
CreateAgentDialog → Capabilities section:
  Sub-Agents toggle: [ON/OFF]
  └── When ON, sets config.enable_sub_agents = true
  └── Advanced: sub_agent_max_depth, sub_agent_max_iterations
```

When the user clicks "Open in Flow Designer", the config values are mapped to the DeepAgentComponent node's inputs, and the toggle state is reflected in the node's UI.

The AgentCard displays a `[Sub-agents ✓]` badge when `agent.config.enable_sub_agents` is true.

#### Backend changes required for sub-agents

| Change | File | Description |
|--------|------|-------------|
| New Pydantic model | `base/agents/schemas.py` (new) | `DelegateTaskInput(BaseModel)` with `task: str`, `context: str \| None` |
| Tool builder method | `components/agents/deep_agent.py` (new) | `_build_delegate_task_tool()` as shown above |
| Depth tracking | `components/agents/deep_agent.py` (new) | `_sub_agent_depth` attribute on component instance |
| Event streaming | `base/agents/events.py` | Add `on_sub_agent_start` / `on_sub_agent_end` event handlers so playground shows sub-agent activity in nested ContentBlocks |
| ContentBlock type | `schema/content_types.py` | Add `SubAgentContent` type for rendering sub-agent steps in the playground UI |

**No database changes needed** for sub-agents — they are ephemeral execution-time constructs. The configuration is stored in the existing `Agent.config` JSON column.

---

### How context tools and skills are enabled

#### Flow designer UI

The `enable_context_tools` toggle on the Deep Agent node controls context persistence tools. When toggled ON:

1. `message_response()` injects `write_context` and `read_context` StructuredTools into `self.tools`
2. These tools read/write to a session-scoped key-value store backed by a new database table
3. The LLM can call `write_context(key="findings", value="...")` and `read_context(key="findings")` during reasoning

```python
# In DeepAgentComponent.message_response()
if self.enable_context_tools:
    # Session ID is always available via the graph object during execution
    session_id = self.graph.session_id
    write_tool = self._build_write_context_tool(session_id)
    read_tool = self._build_read_context_tool(session_id)
    self.tools.extend([write_tool, read_tool])
```

The tools use the session service:

```python
def _build_write_context_tool(self, session_id: str) -> StructuredTool:
    async def write_context(key: str, value: str) -> str:
        await self._context_service.set(session_id=session_id, key=key, value=value)
        return f"Saved context '{key}' ({len(value)} chars)."

    return StructuredTool.from_function(
        coroutine=write_context,
        name="write_context",
        description="Save intermediate results, notes, or data under a named key for later retrieval. Use this to avoid losing important information as the conversation grows.",
        args_schema=WriteContextInput,  # Pydantic: key: str, value: str
    )

def _build_read_context_tool(self, session_id: str) -> StructuredTool:
    async def read_context(key: str) -> str:
        value = await self._context_service.get(session_id=session_id, key=key)
        if value is None:
            return f"No context found for key '{key}'."
        return value

    return StructuredTool.from_function(
        coroutine=read_context,
        name="read_context",
        description="Retrieve previously saved context by key name. Returns the stored value or a not-found message.",
        args_schema=ReadContextInput,  # Pydantic: key: str
    )
```

#### Agent manager UI

Context tools are controlled through the `config` JSON:

```
CreateAgentDialog → Capabilities section:
  Context Tools toggle: [ON/OFF]
  └── When ON, sets config.enable_context_tools = true
```

The AgentCard displays a `[Context ✓]` badge when `agent.config.enable_context_tools` is true.

#### Skills in the agent manager

Skills (dynamic tool registries loaded at runtime from filesystem sources) are a more advanced Deep Agents concept. In Langflow's agent manager, skills map to the existing **tools** selection mechanism:

```
CreateAgentDialog → Tools section:
  Available tools grid (currently AVAILABLE_TOOLS from constants.ts)
  └── Each tool maps to a Langflow component name
  └── Stored as agent.tools = ["SharePointFilesLoader", "TavilySearch", ...]
```

When "Open in Flow Designer" creates a flow, these tool names are resolved to component nodes and connected to the DeepAgentComponent's `tools` HandleInput via edges. This is how the agent manager "skills" translate to the flow designer's tool connection model.

For a dedicated skills system (loading tools from custom Python files at runtime), a future enhancement would add:

```
CreateAgentDialog → Skills section (future):
  [+ Add Skill File] → Upload .py file with @tool decorated functions
  └── Stored as agent.config.skills = [{path: "...", name: "..."}]
  └── At execution time, dynamically loaded as StructuredTool objects
```

This mirrors Deep Agents' `SkillsMiddleware` but uses Langflow's existing custom component upload infrastructure rather than raw filesystem access.

#### Backend changes required for context tools

| Change | File | Description |
|--------|------|-------------|
| **New database table** | `services/database/models/agent_context/model.py` (new) | `AgentContextStore` table with `session_id`, `key`, `value` (Text), `created_at`, `updated_at` columns |
| **Alembic migration** | `alembic/versions/` (new) | Migration to create `agent_context_store` table |
| **Context service** | `services/agent_context/service.py` (new) | `AgentContextService` with `get(session_id, key)`, `set(session_id, key, value)`, `get_all(session_id)`, `delete(session_id, key)` methods |
| **Service registration** | `services/manager.py` | Register `AgentContextService` in the service manager |
| **Pydantic schemas** | `base/agents/schemas.py` (new) | `WriteContextInput(BaseModel)`, `ReadContextInput(BaseModel)` |
| **Tool builders** | `components/agents/deep_agent.py` (new) | `_build_write_context_tool()`, `_build_read_context_tool()` as shown above |
| **ContentBlock type** | `schema/content_types.py` | Add `ContextContent` type for rendering context read/write operations in playground |

##### AgentContextStore database model

```python
# services/database/models/agent_context/model.py

class AgentContextStore(SQLModel, table=True):
    __tablename__ = "agent_context_store"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: str = Field(index=True, nullable=False)
    key: str = Field(nullable=False)
    value: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(DateTime, default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    )

    __table_args__ = (
        UniqueConstraint("session_id", "key", name="unique_context_key_per_session"),
    )
```

##### AgentContextService

```python
# services/agent_context/service.py

class AgentContextService:
    def __init__(self, session_service):
        self.session_service = session_service

    async def get(self, session_id: str, key: str) -> str | None:
        async with self.session_service.get_session() as db:
            result = await db.exec(
                select(AgentContextStore)
                .where(AgentContextStore.session_id == session_id)
                .where(AgentContextStore.key == key)
            )
            record = result.first()
            return record.value if record else None

    async def set(self, session_id: str, key: str, value: str) -> None:
        async with self.session_service.get_session() as db:
            existing = await db.exec(
                select(AgentContextStore)
                .where(AgentContextStore.session_id == session_id)
                .where(AgentContextStore.key == key)
            )
            record = existing.first()
            if record:
                record.value = value
                # updated_at is handled by SQLAlchemy onupdate=func.now()
            else:
                record = AgentContextStore(session_id=session_id, key=key, value=value)
                db.add(record)
            await db.commit()

    async def get_all(self, session_id: str) -> dict[str, str]:
        async with self.session_service.get_session() as db:
            results = await db.exec(
                select(AgentContextStore)
                .where(AgentContextStore.session_id == session_id)
            )
            return {r.key: r.value for r in results.all()}

    async def delete(self, session_id: str, key: str) -> bool:
        async with self.session_service.get_session() as db:
            result = await db.exec(
                select(AgentContextStore)
                .where(AgentContextStore.session_id == session_id)
                .where(AgentContextStore.key == key)
            )
            record = result.first()
            if record:
                await db.delete(record)
                await db.commit()
                return True
            return False
```

---

### Summary of all backend changes

| Category | Files to create | Files to modify |
|----------|----------------|-----------------|
| **Deep Agent component** | `components/agents/deep_agent.py`, `base/agents/schemas.py` | `components/agents/__init__.py` |
| **Context store** | `services/database/models/agent_context/model.py`, `services/agent_context/service.py` | `services/manager.py`, `alembic/versions/` (new migration) |
| **Event streaming** | — | `base/agents/events.py`, `schema/content_types.py` |
| **Frontend constants** | — | `pages/AgentsPage/components/constants.ts` |
| **Frontend types** | — | `types/agents/index.ts` (extend config type) |
| **Agent manager dialog** | — | `pages/AgentsPage/components/CreateAgentDialog.tsx`, `pages/AgentsPage/components/AgentCard.tsx` |

**No changes to existing Agent model** — the `config: dict` JSON column already supports arbitrary configuration. The capability flags (`enable_sub_agents`, `enable_context_tools`, etc.) are stored as keys in this existing JSON column.

**No changes to existing AgentComponent** — the new `DeepAgentComponent` is a separate component class that coexists with the standard Agent in the `agents` category.

**No changes to orchestrator or Graph._run()** — sub-agents and context tools are injected as standard StructuredTools into the existing AgentExecutor loop. They don't require changes to the graph execution pipeline.

---

## References

- [LangChain Deep Agents Repository](https://github.com/langchain-ai/deepagents)
- [Deep Agents Documentation](https://docs.langchain.com/oss/python/deepagents/overview)
- [Deep Agents Architecture Overview (DeepWiki)](https://deepwiki.com/langchain-ai/deepagents/1.3-architecture-overview)
- [LangGraph create_react_agent](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)
- Langflow existing research: `docs/research/python-backend-langgraph-deep-dive.md`
