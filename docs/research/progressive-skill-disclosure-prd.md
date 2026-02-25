# Product Requirements Document: Progressive Skill Disclosure for Langflow

## Document metadata
- **Status:** Draft
- **Last updated:** 2026-02-25
- **Related research:** `docs/research/progressive-skill-disclosure-technical-research.md`
- **Related prior work:** `docs/research/skills-implementation-research-report.md`, `docs/research/langchain-deep-agents-harness-adaptation-plan.md`

---

## 1. Overview

### 1.1 Problem

Langflow's DeepAgentComponent currently supports four internal capabilities (planning, context management, sub-agent delegation, summarization) but lacks a mechanism for agents to dynamically access domain-specific knowledge. Users who want their agents to follow structured workflows for specific domains (e.g., code review, data analysis, API design) must either pack everything into the system prompt or build custom tool chains. Both approaches scale poorly.

### 1.2 Proposed solution

Integrate a **progressive skill disclosure system** into Langflow that allows agents to discover and load domain knowledge on demand. Skills are self-contained packages of expert knowledge (SKILL.md files with YAML frontmatter and structured instructions) that are stored as directories, scanned at startup for lightweight metadata, and loaded fully only when the agent determines they are relevant to the current task.

### 1.3 Goals

1. Enable Langflow agents to access structured domain knowledge without overloading the system prompt.
2. Provide a standard format for authoring and sharing reusable skills.
3. Integrate with the existing DeepAgentComponent capability toggle pattern.
4. Surface skill loading activity in the existing agent event streaming and UI.
5. Support governance and auditability for shared skill catalogs.

### 1.4 Non-goals (this iteration)

1. ~~Skill marketplace or cross-organization sharing~~ — Defer to a future iteration.
2. ~~Automatic skill suggestion based on user intent~~ — Agent self-selects from catalog; no ML-based recommendation.
3. ~~Sub-flow-as-skill publishing from Flow Editor~~ — Addressed in Phase 3 of the skills roadmap (see prior research).
4. ~~Persistent skill memory across sessions~~ — Skills are loaded per session; cross-session skill state is out of scope.

---

## 2. User stories

### 2.1 Skill consumer (agent user)

| ID | Story | Acceptance criteria |
|----|-------|-------------------|
| US-1 | As an agent user, I want my agent to automatically load relevant domain knowledge when I ask a domain-specific question, so I get expert-quality responses without manual setup. | Agent loads appropriate skill via `load_skill` tool call; response quality matches or exceeds manually-prompted agent. |
| US-2 | As an agent user, I want to see which skills my agent loaded during a conversation, so I can understand and trust the reasoning process. | Skill loading appears as a visible step in the agent's content blocks with skill name, description, and load time. |
| US-3 | As an agent user, I want my agent to handle skill loading errors gracefully, so the conversation doesn't break if a skill is misconfigured. | Agent returns a helpful error message and continues without the skill; no unhandled exceptions. |

### 2.2 Skill author (developer/admin)

| ID | Story | Acceptance criteria |
|----|-------|-------------------|
| US-4 | As a skill author, I want a simple file-based format for defining skills, so I can create and iterate on domain knowledge without code changes. | Skills follow SKILL.md format with YAML frontmatter; changes are picked up on agent restart. |
| US-5 | As a skill author, I want to include supporting reference files alongside my skill, so the agent can access detailed documentation when needed. | Supporting .md files in skill directory are accessible via `read_skill_file` tool; filenames listed in load response. |
| US-6 | As a skill author, I want metadata fields for name, description, version, and tags, so skills are discoverable and manageable. | All metadata fields parsed from frontmatter; catalog displays name + description; version tracked. |

### 2.3 Flow builder (advanced user)

| ID | Story | Acceptance criteria |
|----|-------|-------------------|
| US-7 | As a flow builder, I want to configure which skills directory my agent uses, so I can scope agents to specific domains. | `skills_directory` input on DeepAgentComponent accepts a path; only skills from that directory are loaded. |
| US-8 | As a flow builder, I want to enable or disable skills independently of other agent capabilities, so I have fine-grained control. | `enable_skills` toggle on DeepAgentComponent; when disabled, no skill tools are added and no catalog is injected. |
| US-9 | As a flow builder, I want skills to work alongside planning, context, and sub-agent capabilities, so I can build agents with combined powers. | All existing capability toggles continue to work when skills are enabled; no conflicts. |

### 2.4 Platform admin

| ID | Story | Acceptance criteria |
|----|-------|-------------------|
| US-10 | As a platform admin, I want to audit which skills are loaded per conversation, so I can monitor usage and compliance. | Skill loading events are logged with skill name, load time, and session ID. |
| US-11 | As a platform admin, I want skill file access to be secure against directory traversal, so untrusted skill names can't access arbitrary files. | Filenames with `..` or absolute paths are rejected with a clear error. |

---

## 3. Functional requirements

### 3.1 Skill format

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-1 | Skills are stored as directories containing a `SKILL.md` file with YAML frontmatter and markdown body. | P0 |
| FR-2 | YAML frontmatter must include `name` (string, required) and `description` (string, required). | P0 |
| FR-3 | YAML frontmatter may include `version` (string, default "1.0"), `tags` (list of strings), and `dependencies` (list of skill names). | P1 |
| FR-4 | Supporting files are any `.md` files in the skill directory other than `SKILL.md`. | P0 |
| FR-5 | Skill names must be unique within a skills directory. Duplicate names detected during scan produce a warning log and the last-scanned skill wins. | P1 |

### 3.2 SkillStore backend

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-6 | `SkillStore` scans a configurable directory path for skill directories at initialization. | P0 |
| FR-7 | Only YAML frontmatter is parsed during scan (no markdown body parsing). | P0 |
| FR-8 | Parsed metadata is cached in memory for the lifetime of the agent execution. | P0 |
| FR-9 | Full markdown body is parsed and cached on first `load_skill()` call per skill per session. | P0 |
| FR-10 | Supporting files are read on demand via `read_skill_file()` and not cached. | P0 |
| FR-11 | `read_skill_file()` rejects filenames containing `..` or absolute path characters. | P0 |
| FR-12 | `get_skill_catalog()` returns a structured text catalog of all scanned skills (name + description + tags + supporting files). | P0 |
| FR-13 | `SkillStore` provides an `invalidate()` method that clears all caches and forces rescan on next access. | P2 |

### 3.3 Agent tools

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-14 | `load_skill(skill_name: str) -> str` tool returns JSON with `skill_name`, `description`, `instructions`, and `available_files`. | P0 |
| FR-15 | `load_skill` returns an error JSON with the list of valid skill names when the requested skill is not found. | P0 |
| FR-16 | `read_skill_file(skill_name: str, filename: str) -> str` tool returns JSON with `skill_name`, `filename`, and `content`. | P0 |
| FR-17 | Tool docstrings are dynamically set to include the list of available skill names. | P1 |
| FR-18 | Both tools are registered as LangChain `StructuredTool` instances compatible with the existing `HandleInput(input_types=["Tool"])` pattern. | P0 |

### 3.4 DeepAgentComponent integration

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-19 | Add `enable_skills` boolean input (default: `False`) to `DeepAgentComponent`. | P0 |
| FR-20 | Add `skills_directory` string input with advanced visibility, shown only when `enable_skills` is `True`. | P0 |
| FR-21 | When `enable_skills` is `True`, instantiate a `SkillStore`, scan the directory, and add `load_skill` + `read_skill_file` tools to the agent's tool list. | P0 |
| FR-22 | When `enable_skills` is `True`, inject the skill catalog into the agent's system prompt using a `{skill_catalog}` placeholder or append section. | P0 |
| FR-23 | Skill tools must coexist with all existing capability tools (write_todos, write_context, read_context, delegate_task, summarize). | P0 |
| FR-24 | When `enable_sub_agents` is also `True`, sub-agents should inherit the parent's skill store instance (shared cache, no re-scan). | P1 |

### 3.5 Event streaming and UI

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| FR-25 | Add `load_skill` and `read_skill_file` entries to `DEEP_AGENT_TOOL_DISPLAY` in `events.py` with appropriate icons and title prefixes. | P0 |
| FR-26 | Skill loading tool calls must appear in the agent's content blocks with the same expand/collapse behavior as existing tool calls. | P0 |
| FR-27 | The `load_skill` content display should show the skill name and description in a badge/card format. | P1 |
| FR-28 | The `read_skill_file` content display should show the skill name and filename being accessed. | P1 |

---

## 4. Non-functional requirements

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| NFR-1 | Skill scanning must complete in <500ms for up to 100 skills. | P0 |
| NFR-2 | `load_skill` must return in <100ms for cached skills. | P0 |
| NFR-3 | `read_skill_file` must return in <200ms for files up to 50KB. | P1 |
| NFR-4 | Total skill catalog in system prompt must not exceed 5000 tokens for up to 50 skills. | P1 |
| NFR-5 | No new Python dependencies required (use only `pyyaml` which is already in the dependency tree, `pathlib`, `re`, `dataclasses`). | P0 |
| NFR-6 | Skill store must be thread-safe for concurrent agent executions. | P1 |
| NFR-7 | All skill-related errors must produce actionable log messages with skill name and file path context. | P0 |

---

## 5. Technical design (high level)

### 5.1 New files

| File | Purpose |
|------|---------|
| `src/backend/base/langflow/base/agents/skills.py` | `SkillMetadata`, `ParsedSkill`, `SkillStore` classes |
| `src/backend/base/langflow/base/agents/skill_tools.py` | `create_skill_tools()` factory function |

### 5.2 Modified files

| File | Changes |
|------|---------|
| `src/backend/base/langflow/components/agents/deep_agent.py` | Add `enable_skills`, `skills_directory` inputs; wire SkillStore into `build_tools()`; inject catalog into system prompt |
| `src/backend/base/langflow/base/agents/events.py` | Add `load_skill` and `read_skill_file` to `DEEP_AGENT_TOOL_DISPLAY` |
| `src/frontend/src/components/core/chatComponents/ContentDisplay.tsx` | Add skill-specific renderers for `load_skill` and `read_skill_file` tool displays |

### 5.3 New test files

| File | Coverage |
|------|----------|
| `src/backend/tests/unit/base/agents/test_skills.py` | `SkillStore` scanning, loading, caching, validation, catalog generation |
| `src/backend/tests/unit/base/agents/test_skill_tools.py` | `load_skill` and `read_skill_file` tool behavior |
| `src/backend/tests/unit/components/agents/test_deep_agent_skills.py` | `DeepAgentComponent` with skills enabled/disabled |

### 5.4 Component input schema additions

```python
# New inputs for DeepAgentComponent
BoolInput(
    name="enable_skills",
    display_name="Enable Skills",
    info="Enable progressive skill disclosure for domain-specific knowledge loading.",
    value=False,
    advanced=False,
),
MessageTextInput(
    name="skills_directory",
    display_name="Skills Directory",
    info="Path to directory containing skill subdirectories with SKILL.md files.",
    value="",
    advanced=True,
),
```

### 5.5 DEEP_AGENT_TOOL_DISPLAY additions

```python
DEEP_AGENT_TOOL_DISPLAY = {
    # ... existing entries ...
    "load_skill": {"icon": "BookMarked", "title_start": "Loading skill"},
    "read_skill_file": {"icon": "FileSearch", "title_start": "Reading skill reference"},
}
```

---

## 6. Phased delivery plan

### Phase 1: Core backend (P0 requirements)

**Scope:** FR-1 through FR-18, NFR-1, NFR-2, NFR-5, NFR-7

**Deliverables:**
- `SkillStore` class with scan, load, read, and catalog generation
- `create_skill_tools()` factory with `load_skill` and `read_skill_file`
- Unit tests for store and tools
- Security validation for file access

**Estimated effort:** 2–3 days

### Phase 2: DeepAgentComponent integration (P0 requirements)

**Scope:** FR-19 through FR-23, FR-25, FR-26

**Deliverables:**
- `enable_skills` and `skills_directory` inputs on DeepAgentComponent
- SkillStore initialization and tool wiring in `build_tools()`
- System prompt catalog injection
- Event display configuration for skill tools
- Integration tests with DeepAgentComponent

**Estimated effort:** 2–3 days

### Phase 3: Frontend rendering (P1 requirements)

**Scope:** FR-27, FR-28

**Deliverables:**
- Skill-specific content renderers in ContentDisplay.tsx
- Skill name badge/card display for loaded skills
- File reference display for supporting file access

**Estimated effort:** 1–2 days

### Phase 4: Advanced features (P1/P2 requirements)

**Scope:** FR-3, FR-5, FR-13, FR-17, FR-24, NFR-4, NFR-6

**Deliverables:**
- Version, tags, and dependencies in metadata
- Duplicate name detection
- Cache invalidation
- Sub-agent skill store sharing
- Dynamic tool docstrings
- Thread safety
- Token budget enforcement for catalog

**Estimated effort:** 2–3 days

---

## 7. Success metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Skill loading latency (cached) | <100ms p95 | Server-side timing in skill tool calls |
| Catalog scan time (50 skills) | <200ms | Server-side timing during agent initialization |
| Context window savings | 40–60% reduction vs. all-in-prompt | Compare token usage with skills vs. equivalent static prompt |
| Skill activation accuracy | >80% correct skill loaded on first attempt | Sample review of agent tool call traces |
| Zero security incidents | 0 directory traversal or unauthorized file access | Automated test suite + security review |

---

## 8. Open questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | Should skills be scoped per-user or per-organization? | Product | Open |
| 2 | Should the default skills directory be relative to the flow file or a global config path? | Engineering | Open |
| 3 | Should skill loading count toward the agent's max_iterations limit? | Engineering | Open — recommended: no, skill loads are knowledge acquisition, not task execution |
| 4 | Should skills be loadable from remote URLs or only local filesystem? | Engineering | Open — recommended: filesystem only for Phase 1, remote in Phase 4 |
| 5 | Should the Agent Manager UI allow inline editing of SKILL.md files? | Product/Design | Open — recommended: read-only display for Phase 1 |
| 6 | Should dependency auto-loading be supported or left to the LLM's judgment? | Engineering | Open — recommended: LLM-driven for Phase 1 (matches reference implementations) |

---

## 9. Dependencies

| Dependency | Type | Risk |
|-----------|------|------|
| `pyyaml` library | Already in dependency tree | Low — no new dependency needed |
| `DeepAgentComponent` stability | Internal | Low — component is actively maintained |
| `DEEP_AGENT_TOOL_DISPLAY` extension | Internal | Low — additive change, no breaking modifications |
| `ContentDisplay.tsx` extension | Internal | Low — additive renderers, no existing renderer changes |
| Agent Manager config schema | Internal | Medium — requires coordination with Agent Manager UI work |

---

## 10. Appendix: Example SKILL.md for Langflow

```markdown
---
name: data-analysis
description: Structured data analysis workflow for CSV, JSON, and database query results
version: "1.0"
tags:
  - data
  - analysis
  - reporting
---

# Data Analysis Skill

## When to Use
- When the user asks to analyze, summarize, or visualize data
- When working with CSV files, JSON datasets, or database query results
- When asked to identify trends, outliers, or patterns in data

## When NOT to Use
- For simple data format conversions (use direct tool calls)
- For database schema design (see: database-design skill)

## Instructions

1. **Understand the data source**: Identify whether the data is in CSV, JSON, or database format. Use the appropriate data loading tool.

2. **Profile the data**: Before analysis, check:
   - Row count and column count
   - Data types per column
   - Null/missing value percentage
   - Basic statistics (min, max, mean, median) for numeric columns

3. **Identify the analysis goal**: Categorize the user's request as one of:
   - Descriptive (summarize what happened)
   - Diagnostic (explain why something happened)
   - Predictive (forecast what might happen)
   - Prescriptive (recommend actions)

4. **Execute the analysis**: Apply the appropriate analytical approach based on the goal category.

5. **Present results**: Format output with:
   - Key findings (3-5 bullet points)
   - Supporting data (tables or statistics)
   - Confidence notes (sample size, data quality caveats)
   - Suggested next steps

## Common Pitfalls
- Do not assume column names; always verify with the actual data headers
- Do not present raw numbers without context (percentages, comparisons, trends)
- Do not skip the profiling step; data quality issues propagate to analysis errors
```
