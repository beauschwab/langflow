# Progressive Skill Disclosure: Technical Research Document

## Executive summary

Progressive skill disclosure is an architectural pattern for AI agents that loads domain-specific knowledge on demand rather than front-loading all possible instructions into the system prompt. This report provides a deep analysis of the pattern as implemented in the `pessini/langgraph-skills-agent` repository and the LangChain Deep Agents framework, maps it to the existing Langflow deep agent architecture, and consolidates best practices for adoption.

## Repositories and sources reviewed

### Primary reference: pessini/langgraph-skills-agent
- `graphs/skills_agent/skills.py` — `SkillStore` with multi-tier loading (metadata → content → supporting files)
- `graphs/skills_agent/utils/tools.py` — `load_skill` / `read_skill_file` tool factories
- `graphs/skills_agent/utils/prompts.py` — System prompt with `{skill_catalog}` placeholder
- `graphs/skills_agent/utils/nodes.py` — ReAct loop with retry and error-summary degradation
- `graphs/skills_agent/config.py` — `Context` dataclass with lazy initialization
- `graphs/skills_agent/agent.py` — LangGraph `StateGraph` wiring

### Secondary reference: LangChain Deep Agents (langchain-ai/deepagents)
- `libs/deepagents/deepagents/middleware/skills.py` — Skills middleware with SKILL.md parsing
- `libs/deepagents/deepagents/graph.py` — `create_deep_agent()` factory
- `libs/deepagents/deepagents/base_prompt.md` — Base system prompt template

### Langflow (this repository)
- `src/backend/base/langflow/components/agents/deep_agent.py` — `DeepAgentComponent`
- `src/backend/base/langflow/base/agents/agent.py` — `LCToolsAgentComponent` base class
- `src/backend/base/langflow/base/agents/events.py` — Agent event streaming and tool display
- `src/backend/base/langflow/base/agents/context.py` — `AgentContext` state model
- `src/backend/base/langflow/processing/orchestrator.py` — LangGraph orchestrator

---

## 1. What is progressive skill disclosure?

### 1.1 Problem statement

Traditional agent architectures front-load all tool descriptions, domain knowledge, and behavioral instructions into the system prompt. This creates three compounding problems:

1. **Context window saturation** — As skills grow, the system prompt consumes an increasing share of the available context, leaving less room for conversation history, tool outputs, and reasoning.
2. **Attention dilution** — LLMs perform worse when forced to attend to large volumes of irrelevant instructions. Research shows a U-shaped attention curve where information in the middle of long contexts is most likely to be missed.
3. **Scalability ceiling** — Adding new skills requires expanding the prompt, eventually hitting hard token limits or degrading response quality.

### 1.2 The progressive disclosure solution

Progressive skill disclosure addresses these problems through a **multi-tier loading strategy**:

| Tier | What is loaded | When | Token cost |
|------|---------------|------|------------|
| **Tier 0: Catalog** | Skill names + one-line descriptions | Always (system prompt) | ~50 tokens/skill |
| **Tier 1: Instructions** | Full SKILL.md body (workflow, rules, examples) | On demand via `load_skill()` tool call | ~500–2000 tokens/skill |
| **Tier 2: Reference** | Supporting files (cheatsheets, API docs, templates) | On demand via `read_skill_file()` tool call | Variable |

The LLM decides which tier to activate based on task relevance, making knowledge loading emergent rather than hard-coded.

### 1.3 Key insight

Skills are not tools. Tools are callable functions (API wrappers, code executors, search engines). Skills are **structured domain knowledge** that teaches the agent *how* and *when* to use its tools effectively. Progressive disclosure is the mechanism that delivers this knowledge efficiently.

---

## 2. Architecture analysis: pessini/langgraph-skills-agent

### 2.1 Skill storage format

Each skill is a filesystem directory containing:

```
skills/
├── code-review/
│   ├── SKILL.md          # Required: YAML frontmatter + markdown body
│   ├── checklist.md      # Optional: supporting reference
│   └── examples.md       # Optional: supporting reference
└── api-design/
    ├── SKILL.md
    └── best-practices.md
```

**SKILL.md structure:**
```markdown
---
name: code-review
description: Systematic code review workflow with quality checklists
version: "1.0"
tags:
  - engineering
  - quality
dependencies:
  - api-design
---

# Code Review Skill

## When to Use
- When reviewing pull requests or code changes
- When evaluating code quality

## Instructions
1. Load the project context
2. Apply the checklist from checklist.md
3. Categorize findings by severity
```

The YAML frontmatter provides machine-readable metadata; the markdown body provides human-readable (LLM-readable) instructions.

### 2.2 SkillStore: The three-phase loading engine

The `SkillStore` class implements the progressive loading strategy:

**Phase 1: Discovery (startup)**
- Scans the skills directory tree for `SKILL.md` files
- Parses only YAML frontmatter (fast, no markdown body)
- Caches `SkillMetadata` objects indexed by name
- Generates an XML-formatted skill catalog for system prompt injection

**Phase 2: Content loading (on demand)**
- Triggered when agent calls `load_skill(skill_name)`
- Parses the full markdown body of the requested SKILL.md
- Caches the parsed result for subsequent requests
- Returns instructions + list of available supporting files

**Phase 3: Reference loading (on demand)**
- Triggered when agent calls `read_skill_file(skill_name, filename)`
- Reads a specific supporting file from the skill's directory
- Validates filenames to prevent directory traversal attacks
- Not cached (files may be large and infrequently accessed)

### 2.3 Tool design

Two tools expose the SkillStore to the LLM:

1. **`load_skill(skill_name: str) -> str`**
   - Returns JSON with `instructions`, `description`, and `available_files`
   - On error, returns the full list of valid skill names for self-correction
   - Docstring dynamically includes available skill names

2. **`read_skill_file(skill_name: str, filename: str) -> str`**
   - Returns JSON with `content`, `skill_name`, and `filename`
   - Validates filename security (no `..` or absolute paths)

**Key design decision:** Tool docstrings are overwritten at runtime to include the list of available skill names. This ensures the LLM sees valid options in the tool schema without relying on the system prompt for discovery.

### 2.4 System prompt design

```
You are a helpful AI assistant with access to a skills system...

## Progressive Discovery Workflow
1. Browse: Review the skill summaries below
2. Match: When a task aligns with a skill's description, load that skill first
3. Load: Call load_skill(skill_name) to get detailed instructions
4. Inspect: Check available_files in the response
5. Reference: Use read_skill_file for specific documentation as needed
6. Execute: Apply the skill's guidance to complete the user's task

## Available Skills
{skill_catalog}
```

The `{skill_catalog}` placeholder is replaced at runtime with an XML-structured catalog generated from cached metadata.

### 2.5 Graph topology

```
__start__ → agent_node ⟷ tool_node → __end__
                ↓ (max retries)
          error_summary_node → __end__
```

This is a standard ReAct loop with two key additions:
- **Retry logic with exponential backoff** in `tool_node` for transient failures
- **Graceful degradation** via `error_summary_node` when retries are exhausted (LLM called without tools to generate a user-friendly error summary)

### 2.6 Progressive logging

The implementation includes a structured logging system with three tiers matching the disclosure levels:
- Tier 1: Catalog operations (scan, render)
- Tier 2: Skill loading (cache hits/misses, load errors)
- Tier 3: Supporting file reads (per-file access patterns)

This enables observability into which skills are loaded and how often, supporting optimization of the skill catalog.

---

## 3. Architecture analysis: LangChain Deep Agents skills middleware

### 3.1 Middleware pattern

Deep Agents implements skills as **composable middleware** that modifies agent behavior at lifecycle hooks:

```python
middlewares = [
    SkillsMiddleware(skills_dir="./skills"),
    SubagentMiddleware(max_depth=2),
    SummarizationMiddleware(max_tokens=4000),
    MemoryMiddleware(store=InMemoryStore()),
]
agent = create_deep_agent(model=model, middlewares=middlewares)
```

Each middleware can:
- Inject content into the system prompt
- Add tools to the agent's tool list
- Intercept tool call results
- Modify state before/after agent steps

### 3.2 Skills middleware specifics

The skills middleware:
1. Scans for SKILL.md files at initialization
2. Parses frontmatter for metadata
3. Injects a skill catalog into the system prompt
4. Provides `load_skill` and `read_skill_file` tools
5. Tracks which skills have been loaded in the current session

### 3.3 Key difference from pessini implementation

| Aspect | pessini/langgraph-skills-agent | LangChain Deep Agents |
|--------|-------------------------------|----------------------|
| Integration point | Context + tools injected at graph level | Middleware layer wrapping agent |
| Skill storage | Filesystem only | Pluggable backends (filesystem, remote) |
| Catalog format | XML tags in system prompt | Markdown list in system prompt |
| Dependency resolution | Declared but manual | Declared but manual |
| Session tracking | Implicit via tool call history | Explicit loaded-skills set in state |

---

## 4. Mapping to Langflow architecture

### 4.1 Current Langflow deep agent capabilities

The existing `DeepAgentComponent` provides four capability toggles:

| Capability | Toggle | Tool(s) created | Status |
|-----------|--------|-----------------|--------|
| Planning | `enable_planning` (default: on) | `write_todos` | Implemented |
| Context management | `enable_context_tools` (default: on) | `write_context`, `read_context` | Implemented |
| Sub-agent delegation | `enable_sub_agents` (default: off) | `delegate_task` | Implemented |
| Summarization | `enable_summarization` (default: off) | `summarize` | Implemented |

These are **internal agent capabilities** — procedural tools that extend how the agent thinks and works. They are distinct from skills (domain knowledge) and external tools (callable services).

### 4.2 Architectural alignment

Progressive skill disclosure maps naturally to the existing Langflow architecture at three levels:

**Level 1: Component level (DeepAgentComponent)**
- Add an `enable_skills` toggle alongside existing capability toggles
- Skills directory path as a configurable input
- Skill catalog injected into the agent's system prompt
- `load_skill` and `read_skill_file` tools added to the agent's tool list

**Level 2: Agent Manager level**
- Skills as attachable bundles in the Agent Manager UI
- Skill metadata stored in the agent config alongside existing `skill_bundle_settings`
- Skill catalog rendered from attached skill bundles at runtime

**Level 3: Flow Editor level (advanced path)**
- Sub-flows published as skills with SKILL.md-compatible metadata
- Visual skill composition in the flow canvas
- Skill outputs routed to agent context inputs

### 4.3 Integration points

| Langflow layer | Progressive disclosure integration |
|----------------|-----------------------------------|
| `DeepAgentComponent.build_tools()` | Add `load_skill` / `read_skill_file` to tool list |
| `DeepAgentComponent.get_system_prompt()` | Inject `{skill_catalog}` placeholder |
| `process_agent_events()` | Add skill-specific display config to `DEEP_AGENT_TOOL_DISPLAY` |
| Agent Manager config | Store attached skill names and metadata |
| Component inputs UI | Add skills directory path and `enable_skills` toggle |

---

## 5. Consolidated best practices

### 5.1 Skill authoring

1. **Single responsibility per skill.** Each skill should cover one coherent domain (e.g., "API design", not "API design + testing + deployment").
2. **Concise frontmatter.** The description field should be 1–2 sentences that clearly state when the skill applies. This is the only text the LLM sees by default.
3. **Actionable instructions.** The markdown body should contain numbered steps, not paragraphs. LLMs follow explicit procedures more reliably than abstract guidance.
4. **Trigger conditions.** Include a "When to Use" section with concrete examples of prompts or task types that should activate this skill.
5. **Anti-patterns section.** Include a "When NOT to Use" section to prevent the LLM from loading the skill for tangentially related tasks.
6. **Reference files for depth.** Keep the main SKILL.md focused (<2000 tokens). Move detailed reference material (API specs, configuration tables, example code) into separate supporting files.

### 5.2 Skill store design

1. **Metadata-only scanning.** Never parse the full markdown body during startup. YAML frontmatter parsing should complete in <100ms for 100+ skills.
2. **Content caching.** Cache parsed skill content after first load. Skills are read-only during a session, so cache invalidation is unnecessary at runtime.
3. **Supporting file validation.** Always validate filenames to prevent directory traversal. Reject paths containing `..`, absolute paths, and symbolic links.
4. **Catalog format.** Use structured formats (XML tags or JSON) for the skill catalog in the system prompt. LLMs parse structured data more reliably than free-form lists.
5. **Dynamic tool docstrings.** Include available skill names in tool docstrings so the LLM sees valid options in the tool schema, not just the system prompt.

### 5.3 Progressive loading strategy

1. **Three-tier loading is optimal.** Catalog → instructions → reference files provides the right granularity. Fewer tiers waste tokens; more tiers add unnecessary tool-call overhead.
2. **Let the LLM decide.** Do not hard-code skill activation rules. The LLM should decide which skills to load based on task context.
3. **Return available files with instructions.** When a skill is loaded, include the list of supporting files so the LLM knows what additional reference is available without making a discovery call.
4. **Error responses should be self-correcting.** When `load_skill` fails (e.g., invalid name), return the list of valid skill names so the LLM can retry without asking the user.

### 5.4 Observability and governance

1. **Log skill activation patterns.** Track which skills are loaded, how often, and whether supporting files are accessed. This data informs catalog optimization.
2. **Monitor token impact.** Measure the token cost of loaded skills versus baseline (catalog-only) to ensure progressive disclosure is actually saving tokens.
3. **Audit tool access.** Skills may include instructions that reference specific tools. Log the skill→tool usage chain for governance and safety review.
4. **Version skills independently.** Each skill should have a version field. This enables rollback, A/B testing, and compatibility tracking.

### 5.5 Agent integration patterns

1. **Skills complement, not replace, tools.** Skills teach the agent domain knowledge; tools give it executable capabilities. Both should coexist.
2. **Skills complement, not replace, planning.** The existing `write_todos` capability pairs well with skills — the agent can plan which skills to load as part of its task decomposition.
3. **Depth limits for sub-agent + skills.** When sub-agents inherit skills, enforce the same depth limits as for delegation to prevent unbounded context growth.
4. **Context management synergy.** The existing `write_context` / `read_context` tools can store skill outputs for cross-step reference, reducing redundant skill loads.

### 5.6 Security considerations

1. **Filename validation is mandatory.** Both the pessini implementation and LangChain Deep Agents validate filenames to prevent directory traversal. Any Langflow integration must do the same.
2. **Skill content is untrusted input.** Skill markdown bodies are injected into the LLM context. They should be treated as potentially adversarial (prompt injection risk) and sanitized if skills are user-authored.
3. **Tool access scoping.** Skills should not be able to expand the agent's tool access. Tool availability should be controlled by the Langflow component graph, not by skill instructions.
4. **Skill publishing controls.** If skills are shared across users or organizations, implement review/approval workflows before publishing to shared catalogs.

---

## 6. Comparison of approaches

| Dimension | pessini/langgraph-skills-agent | LangChain Deep Agents | Langflow (proposed) |
|-----------|-------------------------------|----------------------|-------------------|
| Skill storage | Filesystem directories | Filesystem + pluggable backends | Filesystem + DB-backed catalog |
| Discovery | Directory scan at startup | Middleware init scan | Component build + Agent Manager attachment |
| Catalog delivery | XML in system prompt | Markdown in system prompt | Structured injection in system prompt |
| Activation | `load_skill` tool | `load_skill` tool | `load_skill` tool |
| Reference access | `read_skill_file` tool | `read_skill_file` tool | `read_skill_file` tool |
| Caching | In-memory dict | In-memory with store backends | In-memory + optional persistent cache |
| Retry/degradation | Exponential backoff + error summary | Middleware-level retry | Existing agent retry + content block error display |
| UI integration | None (CLI/API only) | None (SDK/CLI only) | Component inputs + Agent Manager UI + flow canvas |
| Observability | Progressive logging (3 tiers) | LangSmith tracing | Event streaming + content blocks + Arize Phoenix |

---

## 7. Risk analysis

### 7.1 Low risk
- **Token overhead from catalog.** At ~50 tokens per skill, a catalog of 50 skills adds only ~2500 tokens to the system prompt. This is well within acceptable limits.
- **Cache memory usage.** Parsed skill content is typically <10KB per skill. Even with 100 skills cached, memory impact is negligible.

### 7.2 Medium risk
- **LLM skill selection accuracy.** The LLM may fail to match tasks to the correct skill based on catalog descriptions alone. Mitigation: include explicit trigger phrases in descriptions and monitor activation patterns.
- **Skill-tool mismatch.** A skill may reference tools that are not connected to the agent in the current Langflow graph. Mitigation: validate skill instructions against available tools at load time and warn if referenced tools are missing.
- **Circular dependencies.** Skills may declare dependencies on each other. Mitigation: detect cycles during scan phase and fail fast with a clear error.

### 7.3 High risk
- **Prompt injection via skills.** User-authored skills could contain adversarial instructions. Mitigation: implement content review for shared/published skills; sandbox skill content in a delineated prompt section.
- **Context window exhaustion.** An agent that loads many skills in a single session could exhaust its context window. Mitigation: enforce a maximum number of loaded skills per session and leverage the existing summarization tool to compress loaded skill content.

---

## 8. Recommended implementation sequence

1. **Backend: SkillStore + tools** — Port the `SkillStore` pattern to `src/backend/base/langflow/base/agents/skills.py`. Implement `load_skill` and `read_skill_file` as agent tools following the existing deep agent tool pattern.

2. **Backend: DeepAgentComponent integration** — Add `enable_skills` toggle and `skills_directory` input to `DeepAgentComponent`. Wire skill tools into `build_tools()`. Inject skill catalog into system prompt.

3. **Backend: Event streaming** — Add `load_skill` and `read_skill_file` entries to `DEEP_AGENT_TOOL_DISPLAY` in `events.py` for UI rendering support.

4. **Frontend: Content display** — Add skill-specific renderers in `ContentDisplay.tsx` (skill name badge, loaded instructions preview, supporting file access indicator).

5. **Agent Manager: Skill attachment** — Extend the Agent Manager config schema to include attached skill names. Add UI for browsing and attaching skills to agent profiles.

6. **Skill catalog** — Create a default set of skills for common Langflow use cases (data analysis, API integration, document processing) following the SKILL.md format.

---

## References

1. pessini/langgraph-skills-agent — https://github.com/pessini/langgraph-skills-agent
2. Medium article: "Stop Stuffing Your System Prompt" — https://medium.com/@pessini/stop-stuffing-your-system-prompt-build-scalable-agent-skills-in-langgraph-a9856378e8f6
3. LangChain Deep Agents — https://github.com/langchain-ai/deepagents
4. LangChain Deep Agents Skills Documentation — https://docs.langchain.com/oss/python/deepagents/skills
5. Langflow DeepAgentComponent — `src/backend/base/langflow/components/agents/deep_agent.py`
6. Langflow Agent Events — `src/backend/base/langflow/base/agents/events.py`
7. Langflow Skills Implementation Research — `docs/research/skills-implementation-research-report.md`
8. Langflow Deep Agents Harness Adaptation Plan — `docs/research/langchain-deep-agents-harness-adaptation-plan.md`
