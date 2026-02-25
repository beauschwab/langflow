# Playground Modal — AI Elements SDK Integration Deep Dive

## Executive Summary

This document provides a comprehensive analysis of the Langflow Playground modal chat UI/UX and identifies specific opportunities for incorporating Vercel AI Elements SDK patterns to deliver a richer, more modern chat experience. The analysis maps each current component to its AI Elements equivalent, identifies architectural gaps, and proposes a phased implementation roadmap.

---

## 1. Current Architecture Overview

### Component Hierarchy

```
IOModal (new-modal.tsx)
├── BaseModal (shell, full-screen support)
├── Sidebar (sessions list, theme controls)
│   └── SidebarOpenView (session management)
├── SelectedViewField (non-chat I/O fields)
└── ChatViewWrapper (chat-view-wrapper.tsx)
    └── ChatView (chat-view.tsx)
        ├── Empty State (logo + "New chat" text)
        ├── Message List
        │   └── MemoizedChatMessage (chat-message.tsx)
        │       ├── Avatar (robot icon / profile icon)
        │       ├── Sender Name
        │       ├── ContentBlockDisplay (agent steps)
        │       │   └── ContentDisplay (text/code/json/tool_use/media/error)
        │       ├── MarkdownField (message body)
        │       ├── EditMessageField (inline editing)
        │       ├── FileCardWrapper (file attachments)
        │       └── EditMessageButton (copy/edit/evaluate actions)
        ├── FlowRunningSkeleton (loading state)
        └── ChatInput (chat-input.tsx)
            ├── VoiceAssistant (audio input mode)
            └── InputWrapper
                ├── TextAreaWrapper (auto-resize textarea)
                ├── FilePreview (attached files)
                ├── UploadFileButton
                ├── VoiceButton
                └── ButtonSendWrapper (send/stop toggle)
```

### Key Technical Details

| Aspect | Current Implementation |
|--------|----------------------|
| **Streaming** | Dual-layer SSE: build events via NDJSON + per-vertex token streaming via `EventSource` |
| **State Management** | Zustand stores (`messagesStore`, `flowStore`, `utilityStore`) |
| **Markdown** | `react-markdown` + `remark-gfm` + `rehype-mathjax` + `rehype-raw` |
| **Code Highlighting** | Custom `ChatCodeTabComponent` (simplified code tabs) |
| **Animations** | Framer Motion (`AnimatePresence`, `motion.div`) |
| **Scroll Management** | Manual `scrollIntoView` with `instant`/`smooth` behavior |
| **Message Memoization** | React.memo with shallow prop comparison |

### SSE Streaming Architecture (Backend ↔ Frontend)

The backend uses **two layers of SSE** for chat event streaming:

#### Layer 1: Build Event Stream (NDJSON)

Controls flow execution lifecycle. Configured by `event_delivery` setting (`"polling"` or `"streaming"`).

```
Frontend                              Backend
───────                               ───────
POST /build/{flow_id}/flow      →     start_flow_build() → job_id
GET  /build/{job_id}/events     →     DisconnectHandlerStreamingResponse
     ?stream=true                      (media_type: application/x-ndjson)
                                ←     { event: "vertices_sorted", ... }
                                ←     { event: "end_vertex", data: { message, stream_url, ... } }
                                ←     { event: "end", ... }
```

- **API entry:** `src/backend/base/langflow/api/v1/chat.py` → `build_flow()` (POST) and `get_flow_events_response()` in `api/build.py`
- **Frontend consumer:** `src/frontend/src/controllers/API/api.tsx` → `performStreamingRequest()` uses Fetch API with `ReadableStream` reader
- **Config check:** `new-modal.tsx` → `shouldStreamEvents()` reads `config.data?.event_delivery === EventDeliveryType.STREAMING`
- **Data format:** Newline-delimited JSON (`\n\n` separated), NOT standard SSE `text/event-stream`

#### Layer 2: Per-Vertex Token Stream (SSE)

Streams individual LLM tokens for real-time typing effect. Activated per-vertex when `will_stream` is true.

```
Frontend                              Backend
───────                               ───────
(receives stream_url from             Vertex.build_stream_url() →
 Layer 1 end_vertex event)              "/api/v1/build/{flow_id}/{vertex_id}/stream"

new EventSource(stream_url)     →     build_vertex_stream() → StreamingResponse
                                       (media_type: text/event-stream)
                                ←     data: {"chunk": "Hello"}
                                ←     data: {"chunk": " world"}
                                ←     event: close
```

- **API endpoint:** `src/backend/base/langflow/api/v1/chat.py` → `build_vertex_stream()` (GET, deprecated route)
- **Backend generator:** `_stream_vertex()` yields `StreamData` events as `{"chunk": "..."}` JSON
- **Frontend consumer:** `chat-message.tsx` → `streamChunks()` creates `EventSource(url)` and accumulates chunks: `setChatMessage(prev => prev + chunk)`
- **Data format:** Standard SSE `text/event-stream` with `message`, `error`, and `close` event types

#### How the Two Layers Connect

1. User sends message → `buildFlow({ stream: true })` in `new-modal.tsx`
2. Backend executes the graph, emitting build events via Layer 1
3. When a streaming-capable vertex (e.g., ChatOutput connected to an LLM) finishes, the `end_vertex` event includes a `stream_url`
4. The message is stored with `stream_url` in `messagesStore`
5. `ChatMessage` component detects `chat.stream_url` and opens an `EventSource` (Layer 2)
6. LLM tokens flow through Layer 2 in real-time, updating the message text character-by-character
7. On `close` event, the final message is persisted via `updateChat()`

#### Key Files

| Layer | Backend | Frontend |
|-------|---------|----------|
| Build events | `api/v1/chat.py` (L141-196), `api/build.py` (L83-144) | `controllers/API/api.tsx` (L268-349) |
| Token stream | `api/v1/chat.py` (L486-527), `graph/vertex/vertex_types.py` | `chatMessage/chat-message.tsx` (L72-119) |
| Config | `services/settings/base.py` (`event_delivery`) | `new-modal.tsx` (L163-165) |
| Orchestrator | `processing/orchestrator.py` (L49-80) | — |

### Intermediate Steps: Tool Calls & Sub-Agent Rendering

Agent intermediate steps (tool calls, sub-agent invocations) render in real-time through a **partial message update** mechanism that reuses the same message ID:

#### Backend: Event Processing Pipeline

1. **Agent streams events** — `base/agents/agent.py` initializes a message with `properties={"state": "partial"}` and empty `content_blocks`, then calls LangChain's `runnable.astream_events()` (v2 streaming API).

2. **Event handlers map LangChain events to content blocks** — `base/agents/events.py` contains `process_agent_events()` which routes events:
   - `on_tool_start` → Creates a `ToolContent` object (`type: "tool_use"`) with `name`, `tool_input`, and appends it to `agent_message.content_blocks[0].contents`. Calls `send_message()` to emit.
   - `on_tool_end` → Updates the same `ToolContent` with `output` and `duration`. Calls `send_message()` again.
   - `on_tool_error` → Updates with `error` field. Calls `send_message()`.
   - `on_chain_start/end/stream` → Handles sub-agent chain events similarly.

3. **Message emitted via EventManager** — `custom_component/component.py`'s `send_message()` stores the message in the database and calls `EventManager.on_message()`, which serializes the message as `{"event": "add_message", "data": {...}}` and puts it into an async queue.

4. **Same message ID reused** — Each `send_message()` call uses the **same message ID** throughout the agent's execution. This is the critical mechanism that enables partial updates rather than creating duplicate messages.

#### Frontend: Partial Update & Rendering

5. **Store merges partial updates** — `stores/messagesStore.ts`'s `addMessage()` checks if a message with the same ID already exists. If so, it calls `updateMessagePartial()` which merges the incoming data (including updated `content_blocks`) with the existing message via spread operator.

6. **ContentBlockDisplay renders streaming state** — `ContentBlockDisplay.tsx` reads the message's `state` property:
   - `state === "partial"` → Shows the latest step's header/icon (e.g., tool name with hammer icon), displays `<BorderTrail>` animated glow, and keeps the block title visible.
   - `state !== "partial"` (complete) → Shows a green checkmark icon with "Finished" header, hides the block title.
   - Each new `ToolContent` item in `content_blocks[0].contents` animates in via Framer Motion as it arrives.

7. **ContentDisplay renders tool_use type** — `ContentDisplay.tsx` handles `type: "tool_use"` by rendering:
   - Tool input as formatted JSON code block
   - Tool output as markdown (if string) or JSON (if object)
   - Tool error with red styling if present

#### Data Schema

```typescript
// ToolContent (backend: schema/content_types.py)
{
  type: "tool_use",
  name: "search_web",        // Tool name
  tool_input: { query: "..." }, // Input passed to tool
  output: "...",              // Result (added on_tool_end)
  error: null,                // Error if failed
  duration: 1250,             // Execution time in ms
  header: { title: "Searching web", icon: "Search" }
}

// Message update flow (same ID, incremental content_blocks)
// 1st emit: { id: "msg-1", content_blocks: [{contents: [tool1_start]}], state: "partial" }
// 2nd emit: { id: "msg-1", content_blocks: [{contents: [tool1_done]}], state: "partial" }
// 3rd emit: { id: "msg-1", content_blocks: [{contents: [tool1_done, tool2_start]}], state: "partial" }
// Final:   { id: "msg-1", content_blocks: [{contents: [tool1_done, tool2_done]}], state: "complete" }
```

---

## 2. AI Elements SDK Component Mapping

### 2.1 Conversation / ConversationContent → ChatView

**Current:** `ChatView` in `chat-view.tsx` — manual div-based layout with `chat-message-div` CSS class for scrolling. No built-in scroll-to-bottom anchoring or auto-scroll management.

**AI Elements Equivalent:** `<Conversation>` + `<ConversationContent>` provide:
- Automatic scroll-to-bottom on new messages
- Scroll anchor management (pause auto-scroll when user scrolls up)
- Consistent layout container with proper spacing

**Gap Analysis:**
- The current implementation manually handles scroll via `useEffect` + `scrollIntoView` with a `playgroundScrollBehaves` state toggle between `instant` and `smooth`. This is fragile and leads to scroll jank.
- No scroll-anchor detection — user scrolling up to read history is disrupted by new messages.

**Opportunity:** Replace the manual scroll logic with a Conversation-style container that uses `IntersectionObserver` for smart auto-scroll behavior. This would fix the common UX issue where users lose their scroll position when new streaming chunks arrive.

### 2.2 Message / MessageContent / MessageResponse → ChatMessage

**Current:** `ChatMessage` in `chat-message.tsx` — 467-line monolithic component handling:
- Avatar rendering (robot/user profile with custom icons)
- Sender name display
- Content blocks (agent steps)
- Markdown rendering
- Message editing
- File attachments
- Evaluation feedback (thumbs up/down)
- SSE streaming
- Error handling

**AI Elements Equivalent:** The `<Message>` component family decomposes this into:
```
Message (from="user"|"assistant")
├── MessageAvatar
├── MessageContent
│   ├── MessageResponse (markdown body)
│   ├── Reasoning (chain-of-thought)
│   └── Tool invocation displays
└── MessageActions (copy/edit/feedback)
```

**Gap Analysis:**
- `ChatMessage` violates single-responsibility — it manages streaming state, scroll behavior, edit state, AND rendering in one component.
- The streaming logic (`streamChunks`) is embedded directly in the message component rather than being managed at the conversation level.
- No role-based styling system — user vs. assistant distinction is handled through conditional CSS classes scattered throughout.

**Opportunity:**
1. Extract streaming logic out of `ChatMessage` into a dedicated hook or the parent `ChatView`.
2. Create a role-aware `<Message from={role}>` wrapper that applies consistent styling.
3. Decompose into `MessageAvatar`, `MessageContent`, and `MessageActions` sub-components.
4. The existing `ContentBlockDisplay` is actually a very strong equivalent to AI Elements' Reasoning component — it already handles agent step visualization with expand/collapse, loading borders, and duration tracking.

### 2.3 PromptInput / PromptInputTextarea / PromptInputActions → ChatInput

**Current:** `ChatInput` → `InputWrapper` → `TextAreaWrapper` + `ButtonSendWrapper` + `UploadFileButton` + `VoiceButton`

**AI Elements Equivalent:**
```
PromptInput (value, onValueChange)
├── PromptInputTextarea (auto-resize, placeholder, keyboard handling)
└── PromptInputActions
    ├── AttachButton
    ├── VoiceButton
    ├── StopButton (during generation)
    └── SendButton
```

**Gap Analysis:**
- The current `InputWrapper` has good structural separation but uses a raw `<Textarea>` with manual auto-resize via a hook (`useAutoResizeTextArea`).
- File upload is limited to images only (`ALLOWED_IMAGE_INPUT_EXTENSIONS`).
- The send/stop toggle in `ButtonSendWrapper` is well-implemented but could benefit from smoother transitions.
- The current textarea placeholder dynamically changes based on state (dragging, no input), which is a nice touch.

**Opportunity:**
- The current architecture already aligns well with the AI Elements `PromptInput` pattern.
- Main improvement: Add submit-on-Enter configuration to the input component level rather than the wrapper.
- Consider supporting richer file types beyond images.

### 2.4 CodeBlock → ChatCodeTabComponent

**Current:** `SimplifiedCodeTabComponent` / `ChatCodeTabComponent` — custom code display with copy button and language label.

**AI Elements Equivalent:** `<CodeBlock language="..." code="..." />` with built-in syntax highlighting and copy-to-clipboard.

**Gap Analysis:**
- The current implementation works well and has a copy button.
- Missing: line numbers, word wrap toggle, and download options for long code blocks.
- The code renderer is used in multiple places (message body, content display, error views) with slightly different configurations.

**Opportunity:** Minimal — current implementation is adequate. Could add line numbers for long code blocks.

### 2.5 Reasoning → ContentBlockDisplay

**Current:** `ContentBlockDisplay` — expandable section showing agent step-by-step progress with:
- Animated border trail during loading
- Expand/collapse with Framer Motion
- Individual step headers with icons
- Duration tracking per step
- Content type rendering (text, code, JSON, tool_use, media, error)

**AI Elements Equivalent:** `<Reasoning>` + `<ReasoningTrigger>` + `<ReasoningContent>`

**Gap Analysis:**
- `ContentBlockDisplay` is actually **more capable** than AI Elements' Reasoning component.
- It supports structured content types (tool_use with input/output, media with URLs) that go beyond simple text reasoning.
- The `BorderTrail` animation during loading is a unique and effective UX touch.

**Opportunity:** This is a strength of the current implementation. The main enhancement would be:
- Auto-expand the latest step when in "partial" (streaming) state
- Add a "thinking..." text animation while waiting for the first step

---

## 3. Key UX Gaps & Opportunities

### 3.1 Empty Chat State (High Priority)

**Current state:** Logo + "New chat" heading + "Test your flow with a chat prompt" subtitle with character-by-character animation.

**Improvement:** Add suggested prompt chips below the welcome message. This is a pattern used across modern AI chat interfaces (ChatGPT, Claude, Gemini) to reduce the blank-canvas problem and help users discover flow capabilities.

```
┌─────────────────────────────────────────┐
│              [Langflow Logo]            │
│               New chat                  │
│    Test your flow with a chat prompt    │
│                                         │
│   ┌──────────────┐  ┌───────────────┐   │
│   │ "Hello!"     │  │ "What can     │   │
│   │              │  │  you do?"     │   │
│   └──────────────┘  └───────────────┘   │
│   ┌──────────────┐  ┌───────────────┐   │
│   │ "Help me     │  │ "Summarize    │   │
│   │  get started"│  │  this..."     │   │
│   └──────────────┘  └───────────────┘   │
└─────────────────────────────────────────┘
```

### 3.2 Streaming Indicator (Medium Priority)

**Current state:** Pulsing `MoreHorizontal` (three dots) icon during streaming with no message context.

**Improvement:** Replace with animated typing dots that better indicate the AI is actively generating. The existing `FlowRunningSkeleton` uses `TextShimmer` which is good, but the in-message indicator (the pulsing `...`) could be more expressive.

### 3.3 Smart Auto-Scroll (Medium Priority)

**Current state:** Forces scroll-to-bottom on every message update, losing user's scroll position.

**Improvement:** Implement scroll-anchor pattern:
- Auto-scroll when user is at/near bottom
- Pause auto-scroll when user scrolls up to read history
- Show a "↓ New messages" pill button to jump back to bottom

### 3.4 Message Timestamp Display (Low Priority)

**Current state:** No visible timestamps on messages.

**Improvement:** Show relative timestamps (e.g., "2m ago") on hover or as subtle text below messages.

### 3.5 Keyboard Shortcuts (Low Priority)

**Current state:** Enter to send, Shift+Enter for newline.

**Improvement:** Add Ctrl+/ or ? for keyboard shortcut overlay showing available actions.

---

## 4. Deep Agent Functionality — Process Step Analysis & AI Elements Mapping

The Deep Agent (`DeepAgentComponent`) extends `LCToolsAgentComponent` with four capability toggles that each produce distinct process step types. This section maps every step type to its current rendering and proposes AI Elements component variations.

### 4.1 Capability Overview

| Capability | Toggle | Tool Name(s) | Content Type Emitted | Current Rendering |
|-----------|--------|--------------|---------------------|-------------------|
| **Planning** | `enable_planning` | `write_todos` | `tool_use` (generic) | JSON input/output in collapsible step |
| **Context Tools** | `enable_context_tools` | `write_context`, `read_context` | `tool_use` (generic) | JSON input/output in collapsible step |
| **Sub-Agents** | `enable_sub_agents` | `delegate_task` | `tool_use` (generic) | JSON input/output in collapsible step |
| **Summarization** | `enable_summarization` | `summarize` | `tool_use` (generic) | JSON input/output in collapsible step |
| **Thinking/Input** | always | (chain start) | `text` | Markdown "**Input**: ..." |
| **Final Output** | always | (chain end) | `text` | Markdown output text |
| **Memory** | always (via `MemoryComponent`) | — | Not displayed as step | Chat history injected into LLM context |

### 4.2 Current Rendering Pipeline

All deep agent process steps flow through the same pipeline:

```
DeepAgentComponent.message_response()
  → LCToolsAgentComponent.run_agent()
    → process_agent_events(runnable.astream_events())
      → on_tool_start  → ToolContent(type="tool_use", name="write_todos", header="Accessing **write_todos**")
      → on_tool_end    → ToolContent updated with output, header="Executed **write_todos**"
      → on_chain_start → TextContent(type="text", header="Input")
      → on_chain_end   → TextContent(type="text", header="Output") + state="complete"
```

**Key observation:** Every deep agent tool (planning, context, sub-agents, summarization) renders identically as a generic `tool_use` content type with a "Hammer" icon. There is **no visual distinction** between a planning step, a context save, a sub-agent delegation, or a summarization — they all appear as "Accessing **tool_name**" → "Executed **tool_name**" with raw JSON input/output.

### 4.3 Gap Analysis — What's Missing

| Process Step | What Users See Now | What Users Should See |
|-------------|-------------------|----------------------|
| **Planning (write_todos)** | `Hammer` icon, JSON `{todos: [{task, status}]}` | Checklist UI with ⬜/🔄/✅ status icons per task |
| **Thinking (chain start)** | `MessageSquare` icon, "**Input**: user text" | Collapsible "Thinking..." section with reasoning trace |
| **Context Write** | `Hammer` icon, JSON `{key, value}` | "Saved to memory" badge with key name |
| **Context Read** | `Hammer` icon, JSON `{key}` | "Retrieved from memory" with key→value display |
| **Sub-Agent Delegation** | `Hammer` icon, JSON `{task, context}` | Nested agent card showing sub-agent's task + result |
| **Summarization** | `Hammer` icon, JSON `{text, max_length}` | "Condensed" indicator with before/after length |
| **Memory** | Not visible | "Loaded N messages from history" indicator |
| **Tool Errors** | `Hammer` icon, red JSON error | Error banner with retry suggestion |

### 4.4 Proposed AI Elements Component Mapping

#### 4.4.1 Planning Steps → `<Reasoning>` with Checklist

The `write_todos` tool output contains a structured todo list with status icons (⬜/🔄/✅). This maps perfectly to AI Elements' `<Reasoning>` component pattern — a collapsible section showing the agent's structured thinking.

**Current rendering (generic tool_use):**
```
┌─ 🔨 Accessing write_todos ─────────────┐
│ Input: {"todos": [{"task": "...", ...}]} │
│ Output: "Todo List:\n⬜ Step 1\n..."     │
└──────────────────────────────────────────┘
```

**Proposed rendering (checklist variation):**
```
┌─ 📋 Planning ──────────────────────────┐
│ ⬜ Research available APIs              │
│ 🔄 Parse the input data                │
│ ✅ Set up the project structure         │
│ ⬜ Write the final report              │
└─────────────────────────────────────────┘
```

**Implementation:** Detect `tool_name === "write_todos"` in `ContentDisplay.tsx` and render a parsed checklist instead of raw JSON. The output string from `write_todos` already contains emoji status markers (⬜/🔄/✅) that can be parsed into a structured checklist view.

**AI Elements parallel:** `<Reasoning>` → `<ReasoningTrigger>Planning</ReasoningTrigger>` → `<ReasoningContent>` with checklist items.

#### 4.4.2 Thinking/Chain Steps → `<Reasoning>` with Collapsible Trace

Chain start events emit a `TextContent` with "**Input**: ..." — this is the agent's initial processing of the user request. This maps to AI Elements' `<Reasoning>` component for showing chain-of-thought.

**Current rendering:**
```
┌─ 💬 Input ─────────────────────────────┐
│ **Input**: What is the weather today?   │
└─────────────────────────────────────────┘
```

**Proposed rendering:**
```
┌─ 🧠 Thinking ──────────────────────────┐
│ ▸ View reasoning (click to expand)      │
│   "I need to check the weather. I'll    │
│    use the search tool to find current  │
│    conditions..."                       │
└─────────────────────────────────────────┘
```

**AI Elements parallel:** `<Reasoning>` → `<ReasoningTrigger>View reasoning</ReasoningTrigger>` → `<ReasoningContent>{step.text}</ReasoningContent>`

#### 4.4.3 Context Tools → `<Message>` with Memory Badge

Context read/write operations are memory operations. They should render as compact status indicators rather than verbose JSON dumps.

**Current rendering:**
```
┌─ 🔨 Accessing write_context ───────────┐
│ Input: {"key": "results", "value": ...} │
│ Output: "Saved context 'results' (245   │
│          chars)."                        │
└──────────────────────────────────────────┘
```

**Proposed rendering:**
```
┌─ 💾 Saved to memory ───────────────────┐
│ Key: results  •  245 chars              │
│ ▸ View value (click to expand)          │
└─────────────────────────────────────────┘

┌─ 📖 Retrieved from memory ─────────────┐
│ Key: results                            │
│ ▸ View value (click to expand)          │
└─────────────────────────────────────────┘
```

**AI Elements parallel:** Compact `<Message from="system">` with badge styling — no direct AI Elements equivalent, but follows the pattern of system-level status messages.

#### 4.4.4 Sub-Agent Delegation → Nested `<Message>` with Agent Card

Sub-agent delegation creates an isolated child agent. This should render as a visually distinct nested section showing the sub-task and its result.

**Current rendering:**
```
┌─ 🔨 Accessing delegate_task ───────────┐
│ Input: {"task": "Search for...",        │
│         "context": "..."}               │
│ Output: "Sub-agent completed: ..."      │
└──────────────────────────────────────────┘
```

**Proposed rendering:**
```
┌─ 🤖 Delegated to Sub-Agent ────────────┐
│ Task: "Search for recent papers on..."  │
│ ┌─ Sub-Agent Result ──────────────────┐ │
│ │ Found 3 relevant papers:            │ │
│ │ 1. "Paper A" (2024)                 │ │
│ │ 2. "Paper B" (2023)                 │ │
│ └─────────────────────────────────────┘ │
│ ⏱ 3.2s                                 │
└──────────────────────────────────────────┘
```

**AI Elements parallel:** `<Message from="assistant">` nested within the parent message's content block, styled with distinct border/background to show agent hierarchy.

#### 4.4.5 Summarization → Compact `<CodeBlock>` Diff View

Summarization condenses long text. The UI should show the compression ratio and allow viewing the summary.

**Current rendering:**
```
┌─ 🔨 Accessing summarize ──────────────┐
│ Input: {"text": "...(very long)...",    │
│         "max_length": 500}              │
│ Output: "Condensed summary text..."     │
└──────────────────────────────────────────┘
```

**Proposed rendering:**
```
┌─ 📝 Summarized ────────────────────────┐
│ 2,450 chars → 480 chars (80% reduction) │
│ ▸ View summary (click to expand)        │
└──────────────────────────────────────────┘
```

**AI Elements parallel:** `<CodeBlock>` with language="markdown" for the summary content, wrapped in a compact disclosure.

#### 4.4.6 Memory (Chat History) → Status Indicator

Memory loading via `MemoryComponent` happens before the agent runs and is not currently visible in the chat. A brief indicator would improve transparency.

**Proposed rendering:**
```
┌─ 🧠 Memory ────────────────────────────┐
│ Loaded 12 messages from chat history    │
└──────────────────────────────────────────┘
```

**Implementation:** Add a `TextContent` step at the beginning of `run_agent()` when `chat_history` is non-empty, showing the count of loaded messages.

#### 4.4.7 Tool Errors → Error Banner with Context

Tool errors currently render with raw JSON. They should show a clear error message with the failed tool name and a hint about what went wrong.

**Current rendering:**
```
┌─ 🔨 Error using write_todos ───────────┐
│ Error: {"message": "Invalid input..."}  │
└──────────────────────────────────────────┘
```

**Proposed rendering:**
```
┌─ ❌ write_todos failed ────────────────┐
│ Invalid input: 'status' must be one of  │
│ pending, in_progress, done              │
│ ⏱ 0.1s                                 │
└──────────────────────────────────────────┘
```

### 4.5 Implementation Strategy

The proposed changes follow two tracks:

#### Track A: Backend — Differentiated Headers & Icons (Low Effort)

Update `events.py` to emit tool-specific icons and header titles based on tool name:

```python
# Proposed icon/header mapping for deep agent tools
DEEP_AGENT_TOOL_DISPLAY = {
    "write_todos":   {"icon": "ListTodo",   "title_start": "Planning",       "title_end": "Plan updated"},
    "write_context": {"icon": "Save",       "title_start": "Saving context", "title_end": "Saved to memory"},
    "read_context":  {"icon": "BookOpen",   "title_start": "Reading context","title_end": "Retrieved from memory"},
    "delegate_task": {"icon": "Users",      "title_start": "Delegating",     "title_end": "Sub-agent completed"},
    "summarize":     {"icon": "FileText",   "title_start": "Summarizing",    "title_end": "Summarized"},
}
```

This requires changes only to `handle_on_tool_start` and `handle_on_tool_end` in `events.py` — replacing the hardcoded `"Hammer"` icon with a lookup.

#### Track B: Frontend — Tool-Specific Renderers (Medium Effort)

Add tool-name-aware rendering in `ContentDisplay.tsx` for the `tool_use` case:

```typescript
case "tool_use":
  // Deep agent tool-specific renderers
  if (content.name === "write_todos") {
    return <TodoListDisplay content={content} />;
  }
  if (content.name === "write_context" || content.name === "read_context") {
    return <ContextToolDisplay content={content} />;
  }
  if (content.name === "delegate_task") {
    return <SubAgentDisplay content={content} />;
  }
  if (content.name === "summarize") {
    return <SummarizeDisplay content={content} />;
  }
  // Default: generic tool_use rendering
  ...
```

### 4.6 AI Elements Component Summary Table

| Deep Agent Step | AI Elements Component | Proposed Icon | Key Visual Change |
|----------------|----------------------|---------------|-------------------|
| Planning (write_todos) | `<Reasoning>` with checklist | `ListTodo` | Parsed todo items with status emojis |
| Thinking (chain start) | `<Reasoning>` collapsible | `Brain` | "Thinking..." with expandable reasoning |
| Context Write | Compact `<Message>` badge | `Save` | "Saved to memory" one-liner |
| Context Read | Compact `<Message>` badge | `BookOpen` | "Retrieved from memory" one-liner |
| Sub-Agent | Nested `<Message>` card | `Users` | Indented sub-agent task + result |
| Summarization | `<CodeBlock>` disclosure | `FileText` | Compression ratio + expandable summary |
| Memory Load | Status indicator | `Brain` | "Loaded N messages" system message |
| Tool Error | Error `<Message>` | `AlertCircle` | Clear error text instead of raw JSON |
| Final Output | `<MessageResponse>` | `MessageSquare` | Standard markdown response |

---

## 5. Implementation Roadmap

### Phase 1: Quick Wins (No New Dependencies)

These improvements use existing libraries and patterns:

1. **Enhanced empty chat state** with suggested prompt chips
2. **Improved streaming dots** animation using existing Framer Motion
3. **Scroll-to-bottom pill** button using IntersectionObserver
4. **Deep Agent differentiated icons** — Replace hardcoded `"Hammer"` icon in `events.py` with tool-name-aware icons (see §4.5 Track A)

### Phase 2: Component Decomposition (Refactor)

Structural improvements following AI Elements patterns:

1. **Extract streaming logic** from ChatMessage into a `useMessageStream` hook
2. **Create MessageAvatar component** to unify avatar rendering logic
3. **Create MessageActions component** to separate action buttons from message content
4. **Role-based message styling** via a wrapper component with `from` prop
5. **Deep Agent tool-specific renderers** — `TodoListDisplay`, `ContextToolDisplay`, `SubAgentDisplay`, `SummarizeDisplay` (see §4.5 Track B)

### Phase 3: AI Elements SDK Integration (New Dependencies)

Full integration requiring `@ai-sdk/react` and `ai-elements`:

1. **Install AI Elements** components into `components/ai-elements/`
2. **Wire `useChat` hook** alongside existing message store (hybrid approach)
3. **Replace PromptInput** with AI Elements' `<PromptInput>` component
4. **Replace Message rendering** with `<Message>` + `<MessageContent>` + `<MessageResponse>`
5. **Add `<Conversation>` wrapper** with native scroll management

> **Note:** Phase 3 requires careful evaluation of whether the Vercel AI SDK's streaming protocol (`useChat`) can be adapted to work with Langflow's existing SSE-based streaming via `EventSource`. The current backend streams responses via dedicated `stream_url` endpoints, which differs from the AI SDK's expected `POST /api/chat` streaming protocol. A compatibility adapter would be needed.

### Phase 4: Advanced Features

1. **Reasoning display** for agent steps (already strong via ContentBlockDisplay)
2. **Tool invocation cards** with structured input/output display
3. **Message threading** for multi-turn agent interactions
4. **Streaming markdown** that renders incrementally as tokens arrive

---

## 6. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI SDK streaming protocol mismatch | High | Build adapter layer between Langflow SSE and AI SDK data stream |
| Bundle size increase from new dependencies | Medium | Use tree-shaking, install only needed components |
| Breaking existing message store integration | High | Keep dual state management during transition |
| PlaygroundPage vs. ModalPlayground divergence | Medium | Ensure all changes work in both modes |
| Custom content blocks (tool_use, media) not supported by AI Elements | Medium | Keep ContentBlockDisplay as-is, only wrap standard messages |

---

## 7. Recommended Priority

1. **Immediate** (this PR): Enhanced empty state with prompt suggestions, improved streaming indicator
2. **Short-term**: Component decomposition following AI Elements patterns (no new deps)
3. **Medium-term**: Evaluate AI SDK compatibility and build adapter if feasible
4. **Long-term**: Full AI Elements integration with smart scroll, reasoning, and tool displays

---

## Appendix: File Reference

| File | Purpose |
|------|---------|
| `src/frontend/src/modals/IOModal/new-modal.tsx` | Main playground modal shell |
| `src/frontend/src/modals/IOModal/components/chat-view-wrapper.tsx` | Chat area wrapper with header |
| `src/frontend/src/modals/IOModal/components/chatView/components/chat-view.tsx` | Message list + input container |
| `src/frontend/src/modals/IOModal/components/chatView/chatMessage/chat-message.tsx` | Individual message rendering + streaming |
| `src/frontend/src/modals/IOModal/components/chatView/chatInput/chat-input.tsx` | Chat input with file upload + voice |
| `src/frontend/src/modals/IOModal/components/chatView/chatInput/components/input-wrapper.tsx` | Input field layout |
| `src/frontend/src/modals/IOModal/components/chatView/chatInput/components/text-area-wrapper.tsx` | Auto-resize textarea |
| `src/frontend/src/modals/IOModal/components/chatView/chatInput/components/button-send-wrapper.tsx` | Send/stop button |
| `src/frontend/src/components/core/chatComponents/ContentBlockDisplay.tsx` | Agent step visualization |
| `src/frontend/src/components/core/chatComponents/ContentDisplay.tsx` | Content type renderer |
| `src/frontend/src/modals/IOModal/components/chatView/chatMessage/components/edit-message.tsx` | Markdown renderer + edit mode |
| `src/frontend/src/modals/IOModal/components/chatView/chatMessage/components/message-options.tsx` | Copy/edit/feedback buttons |
| `src/frontend/src/modals/IOModal/components/chatView/chatMessage/components/content-view.tsx` | Error display view |
| `src/frontend/src/modals/IOModal/components/flow-running-squeleton.tsx` | Loading skeleton |
| `src/frontend/src/types/chat/index.ts` | Chat type definitions |
