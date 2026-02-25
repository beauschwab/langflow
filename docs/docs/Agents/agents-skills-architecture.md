---
title: Skills architecture
slug: /agents-skills-architecture
---

# Progressive skill disclosure — Technical architecture

This page describes the internal architecture of the progressive skill disclosure system for developers who want to extend, customize, or debug skill behavior.

For end-user documentation, see [Deep Agent skills](/agents-deep-agent-skills).

## System overview

The skills system adds domain-knowledge loading capabilities to the Deep Agent through a three-tier progressive loading pattern. Instead of stuffing all domain knowledge into the system prompt, the agent discovers skills from a lightweight catalog and loads detailed instructions on demand.

```
┌─────────────────────────────────────────────────────────┐
│                     System Prompt                       │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Skill Catalog (Tier 0)                           │  │
│  │  <skill>                                          │  │
│  │    <name>data-analysis</name>                     │  │
│  │    <description>Structured data analysis...</description> │
│  │    <tags>data, analysis</tags>                    │  │
│  │    <supporting_files>examples.md, cheatsheet.md</supporting_files> │
│  │  </skill>                                         │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         │                          │
         ▼                          ▼
  load_skill("data-analysis")  read_skill_file("data-analysis", "examples.md")
  ┌──────────────┐             ┌──────────────┐
  │  Tier 1      │             │  Tier 2      │
  │  Full SKILL.md│             │  Supporting  │
  │  instructions │             │  files       │
  └──────────────┘             └──────────────┘
```

## Backend components

### SkillStore (`langflow/base/agents/skills.py`)

The `SkillStore` class manages skill discovery, metadata caching, and content loading.

#### Data types

| Class | Purpose |
|-------|---------|
| `SkillMetadata` | Dataclass holding parsed YAML frontmatter (name, description, version, tags, dependencies, path). |
| `ParsedSkill` | Dataclass holding both `SkillMetadata` and the full markdown body content. |

#### Key methods

| Method | Description |
|--------|-------------|
| `scan()` | Walks the skills directory for `SKILL.md` files. Parses only YAML frontmatter (fast). Returns the number of skills discovered. |
| `load(skill_name)` | Parses the full markdown body of a skill. Caches the result for subsequent calls. Returns `None` if not found. |
| `read_supporting_file(skill_name, filename)` | Reads a supporting `.md` file from a skill's directory. Validates filenames to prevent directory traversal. |
| `list_supporting_files(skill_name)` | Lists all `.md` files in a skill directory except `SKILL.md`. |
| `get_skill_catalog()` | Generates an XML-structured catalog of all skills for system prompt injection. |
| `get_skill_names()` | Returns a list of all registered skill names. |
| `invalidate()` | Clears all caches and forces a rescan on next access. |

#### Caching strategy

- **Metadata cache**: Populated during `scan()`. Maps skill name → `SkillMetadata`. Persists for the lifetime of the `SkillStore` instance.
- **Content cache**: Populated lazily on first `load()` call per skill. Maps skill name → `ParsedSkill`. Persists for the lifetime of the instance.
- **Supporting files**: Not cached. Read from disk on every `read_supporting_file()` call.

#### Security

The `read_skill_supporting_file()` function validates filenames:

1. Rejects filenames containing `..`
2. Rejects absolute paths (starting with `/` or `\`)
3. Resolves the full path and verifies it remains within the skill directory

### Skill tools (`langflow/base/agents/skill_tools.py`)

The `create_skill_tools()` factory function creates two LangChain `StructuredTool` instances bound to a `SkillStore` instance via closure.

#### Tools created

| Tool | Input schema | Returns |
|------|-------------|---------|
| `load_skill` | `LoadSkillInput(skill_name: str)` | JSON with `skill_name`, `description`, `instructions`, and `available_files`. On error: `error` and `available_skills`. |
| `read_skill_file` | `ReadSkillFileInput(skill_name: str, filename: str)` | JSON with `skill_name`, `filename`, and `content`. On error: `error` message. |

Both tools return JSON strings for structured LLM parsing. Tool descriptions are dynamically set to include the list of available skill names, so the LLM sees valid options in the tool schema.

### DeepAgentComponent integration (`langflow/components/agents/deep_agent.py`)

The Deep Agent component integrates skills through the following additions:

#### Inputs

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `enable_skills` | Boolean | `False` | Enables the skills capability. Adds `load_skill` and `read_skill_file` tools. |
| `skills_directory` | String | `""` | Path to directory with skill subdirectories. Visibility toggles with `enable_skills`. |

#### `_build_skills_tools()` method

When `enable_skills` is `True` and `skills_directory` is set:

1. Creates a `SkillStore` instance from the configured directory.
2. Calls `scan()` to discover skills.
3. Generates the skill catalog via `get_skill_catalog()`.
4. Appends the `SKILLS_PROMPT_SECTION` template (with the catalog) to the system prompt.
5. Returns the tools from `create_skill_tools()`.

The skills tools are injected in `message_response()` after summarization and before sub-agent delegation.

#### System prompt injection

When skills are enabled, the following section is appended to the agent's system prompt:

```
## Skills system

You have access to a skills system that provides domain expertise
via progressive disclosure.

### How to use skills

1. Browse: Review the skill summaries below.
2. Match: When a task aligns with a skill's description, load that skill first.
3. Load: Call load_skill(skill_name) to get detailed instructions.
4. Inspect: Check available_files in the response for reference documents.
5. Reference: Use read_skill_file(skill_name, filename) for specific docs.
6. Execute: Apply the skill's guidance to complete the user's task.

### Available skills

{skill_catalog}
```

The `{skill_catalog}` placeholder is replaced with the XML-formatted catalog generated by `SkillStore.get_skill_catalog()`.

### Event streaming (`langflow/base/agents/events.py`)

Two entries were added to the `DEEP_AGENT_TOOL_DISPLAY` dictionary to provide differentiated rendering for skill tools in the chat UI:

| Tool name | Icon | Title (start) | Title (end) |
|-----------|------|---------------|-------------|
| `load_skill` | `BookMarked` | "Loading skill" | "Skill loaded" |
| `read_skill_file` | `FileSearch` | "Reading skill reference" | "Reference loaded" |

These are consumed by `_get_tool_display()` and rendered in the `handle_on_tool_start` / `handle_on_tool_end` event handlers, which create `ToolContent` entries in the agent message's `content_blocks`.

## Frontend components

### ContentDisplay.tsx

Two skill-specific renderers were added to the `tool_use` case in `ContentDisplay`:

#### `load_skill` renderer

Parses the JSON output and displays:
- Skill name badge (styled inline element)
- Description text
- Expandable instructions viewer with character count
- List of available supporting files

#### `read_skill_file` renderer

Parses the JSON output and displays:
- Skill name badge + filename breadcrumb
- Expandable content viewer with character count

Both renderers handle error responses (showing the error message in red) and fall through to the generic tool renderer if JSON parsing fails.

### Agent Manager constants (`constants.ts`)

The `AVAILABLE_SKILLS` array in the Agent Manager includes preconfigured skills that map to the progressive disclosure system:

| Skill ID | Name | Description |
|----------|------|-------------|
| `data-analysis` | Data Analysis | Structured data analysis workflow for CSV, JSON, and database query results. |
| `code-review` | Code Review | Systematic code review with quality checklists and best practices. |
| `api-design` | API Design | RESTful API design patterns, versioning, and documentation standards. |

These are used in the `CreateAgentDialog` for selecting skills when creating agent profiles.

## File map

| File | Layer | Purpose |
|------|-------|---------|
| `langflow/base/agents/skills.py` | Backend | `SkillMetadata`, `ParsedSkill`, `SkillStore` classes |
| `langflow/base/agents/skill_tools.py` | Backend | `create_skill_tools()` factory, `LoadSkillInput`, `ReadSkillFileInput` schemas |
| `langflow/components/agents/deep_agent.py` | Backend | `DeepAgentComponent` with `enable_skills` toggle and `_build_skills_tools()` |
| `langflow/base/agents/events.py` | Backend | `DEEP_AGENT_TOOL_DISPLAY` entries for `load_skill` and `read_skill_file` |
| `ContentDisplay.tsx` | Frontend | Skill-specific renderers in chat content blocks |
| `constants.ts` | Frontend | `AVAILABLE_SKILLS` for Agent Manager |

## Testing

Skill tests are located in `src/backend/tests/unit/components/agents/`:

| Test file | Coverage |
|-----------|----------|
| `test_skill_store.py` | `SkillStore` scanning, loading, caching, security validation, catalog generation, tool creation and invocation |
| `test_deep_agent_component.py` | Skills toggle, directory configuration, tool creation, metadata, build config visibility |

Run skill tests with:

```bash
uv run pytest src/backend/tests/unit/components/agents/test_skill_store.py -v
uv run pytest src/backend/tests/unit/components/agents/test_deep_agent_component.py -v
```

## Extending the system

### Adding a new skill

1. Create a directory under your skills folder with a `SKILL.md` file.
2. Add YAML frontmatter with at least `name` and `description`.
3. Write instructions in the markdown body.
4. Optionally add supporting `.md` files for reference material.
5. Restart the agent (or call `store.invalidate()`) to pick up new skills.

### Adding skill tools to a custom agent component

If you are building a custom agent component that extends `LCToolsAgentComponent`, you can integrate the skills system:

```python
from langflow.base.agents.skills import SkillStore
from langflow.base.agents.skill_tools import create_skill_tools

# In your component's message_response or build_tools method:
store = SkillStore("/path/to/skills")
store.scan()

# Get the catalog for system prompt injection
catalog = store.get_skill_catalog()
self.system_prompt += f"\n\n## Available Skills\n\n{catalog}"

# Get the tools
skill_tools = create_skill_tools(store)
self.tools.extend(skill_tools)
```

### Customizing the catalog format

The default catalog uses XML tags. To change the format, subclass `SkillStore` and override `get_skill_catalog()`:

```python
class CustomSkillStore(SkillStore):
    def get_skill_catalog(self) -> str:
        """Generate a markdown-formatted catalog."""
        if not self._metadata_cache:
            return "No skills available."
        lines = []
        for name, meta in sorted(self._metadata_cache.items()):
            lines.append(f"- **{name}**: {meta.description}")
        return "\n".join(lines)
```
