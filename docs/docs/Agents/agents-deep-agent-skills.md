---
title: Deep Agent skills
slug: /agents-deep-agent-skills
---

# Progressive skill disclosure for Deep Agents

The **Deep Agent** component includes a **Skills** system that lets your agent dynamically load domain-specific knowledge on demand, instead of packing everything into the system prompt.

Skills are self-contained packages of expert knowledge stored as markdown files. The agent sees a lightweight catalog of available skills, loads full instructions only when a task matches a skill's description, and drills into supporting reference files only when deeper detail is needed. This keeps token usage low while still providing deep domain knowledge.

## How skills work

Skills use a three-tier progressive loading strategy:

| Tier | What loads | When | Token cost |
|------|-----------|------|------------|
| **Catalog** | Skill names and one-line descriptions | Always (injected into system prompt) | ~50 tokens per skill |
| **Instructions** | Full SKILL.md body with workflow steps, rules, and examples | On demand, when the agent calls `load_skill()` | ~500–2000 tokens per skill |
| **Reference** | Supporting files (cheatsheets, API docs, templates) | On demand, when the agent calls `read_skill_file()` | Variable |

The agent decides which skills to load based on the user's request, making knowledge loading automatic and task-driven.

## Enable skills on the Deep Agent

1. Add a **Deep Agent** component to your flow.
2. Toggle **Skills** to **On**.
3. Set the **Skills Directory** field to the path of your skills folder.
4. Connect **Chat Input** and **Chat Output** components.
5. Run the flow. The agent will discover available skills and load them when relevant.

When Skills is enabled, two tools are added to the agent:

- **`load_skill`** — Loads the full instructions for a named skill and returns a list of available supporting files.
- **`read_skill_file`** — Reads a specific supporting file from a skill's directory.

## Deep Agent inputs

The following inputs are specific to the skills capability. For other Deep Agent inputs, see [Agent components](/components-agents).

| Name | Type | Description |
|------|------|-------------|
| enable_skills | Boolean | Adds `load_skill` and `read_skill_file` tools for progressive domain knowledge loading. Default: off. |
| skills_directory | String | Path to directory containing skill subdirectories with SKILL.md files. Shown when Skills is enabled. |

## Create a skill

Each skill is a directory containing a `SKILL.md` file and optional supporting markdown files.

### Directory structure

```
skills/
├── data-analysis/
│   ├── SKILL.md            # Required: metadata + instructions
│   ├── examples.md         # Optional: reference examples
│   └── cheatsheet.md       # Optional: quick reference
├── code-review/
│   ├── SKILL.md
│   └── checklist.md
└── api-design/
    ├── SKILL.md
    └── best-practices.md
```

### SKILL.md format

Each `SKILL.md` file has two parts:

1. **YAML frontmatter** — Machine-readable metadata between `---` delimiters.
2. **Markdown body** — Human-readable instructions for the agent.

```markdown
---
name: data-analysis
description: Structured data analysis workflow for CSV, JSON, and database query results
version: "1.0"
tags:
  - data
  - analysis
---

# Data Analysis Skill

## When to Use
- When the user asks to analyze, summarize, or visualize data
- When working with CSV files, JSON datasets, or database query results

## When NOT to Use
- For simple data format conversions (use direct tool calls)
- For database schema design (see: database-design skill)

## Instructions

1. **Understand the data source**: Identify the data format and use the appropriate loading tool.
2. **Profile the data**: Check row count, column types, null percentages, and basic statistics.
3. **Identify the goal**: Categorize the request as descriptive, diagnostic, predictive, or prescriptive.
4. **Execute the analysis**: Apply the appropriate analytical approach.
5. **Present results**: Include key findings, supporting data, confidence notes, and next steps.

## Common Pitfalls
- Do not assume column names; always verify with actual data headers.
- Do not present raw numbers without context (percentages, comparisons, trends).
```

### Frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier for the skill (use kebab-case). |
| `description` | Yes | One-line summary shown in the skill catalog. This is the only text the agent sees by default. |
| `version` | No | Semantic version string. Default: `"1.0"`. |
| `tags` | No | List of category labels for organization. |
| `dependencies` | No | List of other skill names that should be loaded alongside this skill. |

### Best practices for skill authoring

- **One skill, one domain.** Keep each skill focused on a single coherent area.
- **Write clear trigger conditions.** The "When to Use" section helps the agent decide whether to load the skill.
- **Include anti-patterns.** A "When NOT to Use" section prevents the agent from loading the skill for unrelated tasks.
- **Keep instructions concise.** Target less than 2000 tokens for the main SKILL.md body.
- **Move reference material to supporting files.** API specs, configuration tables, and example code belong in separate `.md` files, not in the main instructions.
- **Use numbered steps.** Agents follow explicit procedures more reliably than prose paragraphs.

## Viewing skill activity in the Playground

When the agent uses skills, tool calls appear as expandable steps in the chat:

- **Loading skill** — Shows the skill name badge, description, expandable instructions, and list of available supporting files.
- **Reading skill reference** — Shows the skill and file name breadcrumb with expandable content viewer.

Each step shows timing information and can be expanded to inspect the full content.

## Agent Manager integration

Skills are available in the **Agent Manager** when creating or editing agent profiles. The skills catalog includes preconfigured skills that can be attached to agent profiles:

- **Data Analysis** — Structured data analysis workflow for CSV, JSON, and database query results.
- **Code Review** — Systematic code review with quality checklists and best practices.
- **API Design** — RESTful API design patterns, versioning, and documentation standards.

Skills selected in the Agent Manager are stored in the agent's `skill_bundle_settings` configuration.

## Security

The skills system includes built-in security measures:

- **Directory traversal prevention** — Filenames containing `..` or absolute paths are rejected.
- **Path validation** — All file paths are resolved and verified to remain within the skill directory.
- **Read-only access** — Skills provide knowledge to the agent but cannot expand the agent's tool access.
