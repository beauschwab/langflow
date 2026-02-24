# Legacy Backend Removal and Non-Core Component Cleanup — Step-by-Step Plan

## Summary

This document describes every concrete change made (or to be made) to remove the **legacy graph execution backend** and eliminate **non-core third-party component integrations** from the Langflow codebase. The goal is to reduce surface area and dependency footprint while keeping the LangGraph-backed orchestrator and all first-party / core components intact.

> **Preserved components** — The following integrations were explicitly kept as-is:
> - `components/confluence/` — Confluence wiki document loader
> - `components/sharepoint/` — SharePoint Files Loader
> - `components/tools/datahub_graphql_mcp.py` — DataHub GraphQL MCP tool

## Repository locations reviewed

- `/home/runner/work/langflow/langflow/src/backend/base/langflow/graph/graph/base.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/processing/orchestrator.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/processing/process.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/helpers/flow.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/settings/base.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/interface/components.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/tools/__init__.py`
- `/home/runner/work/langflow/langflow/src/backend/base/pyproject.toml`
- `/home/runner/work/langflow/langflow/src/frontend/src/utils/styleUtils.ts`
- `/home/runner/work/langflow/langflow/src/frontend/src/pages/AgentsPage/components/constants.ts`
- `/home/runner/work/langflow/langflow/src/backend/tests/unit/test_orchestrator.py`
- `/home/runner/work/langflow/langflow/src/backend/tests/unit/test_interface_components.py`

---

## Part 1 — Legacy Backend Removal

### Background

Before this change the codebase maintained two parallel execution paths:

1. **Legacy path** — `Graph.arun()` — the custom scheduling loop inside `graph/graph/base.py` that walked `RunnableVerticesManager`, built vertices in topological order, and accumulated `RunOutputs`.
2. **LangGraph path** — a thin `StateGraph` wrapper (`_run_with_langgraph`) in `processing/orchestrator.py` that called `graph._run()` via a single LangGraph node named `execute_graph`.

A runtime setting `orchestrator_backend: Literal["legacy", "langgraph"]` (default `"legacy"`) determined which path ran. The LangGraph path was already wrapping the lower-level `graph._run()` method rather than replacing it, so switching is low-risk.

---

### Step 1 — Remove `Graph.arun()`

**File:** `src/backend/base/langflow/graph/graph/base.py`

`Graph.arun()` was the public entry-point for the legacy path. It iterated over multiple input configurations and delegated to `Graph._run()` for each. Because `Graph._run()` is still used by the LangGraph orchestrator, **only `arun()` is deleted** — `_run()` is untouched.

```python
# BEFORE — lines 815-877 (deleted)
async def arun(
    self,
    inputs: list[dict[str, str]],
    *,
    inputs_components: list[list[str]] | None = None,
    types: list[InputType | None] | None = None,
    outputs: list[str] | None = None,
    session_id: str | None = None,
    stream: bool = False,
    fallback_to_env_vars: bool = False,
    event_manager: EventManager | None = None,
) -> list[RunOutputs]:
    ...
    for run_inputs, components, input_type in zip(...):
        run_outputs = await self._run(...)
        vertex_outputs.append(RunOutputs(...))
    return vertex_outputs
```

Also remove the now-unused import:

```python
# BEFORE
from langflow.graph.schema import InterfaceComponentTypes, RunOutputs

# AFTER
from langflow.graph.schema import InterfaceComponentTypes
```

---

### Step 2 — Collapse the orchestrator to LangGraph-only

**File:** `src/backend/base/langflow/processing/orchestrator.py`

Remove:
- The `backend: str = "legacy"` parameter from `run_graph_with_orchestrator()`
- The `if backend != "langgraph": return await graph.arun(...)` branch
- The separate `_run_with_langgraph()` helper function
- The `try/except ImportError` fallback inside `_run_with_langgraph()`

Promote the LangGraph `StateGraph` construction into `run_graph_with_orchestrator()` directly.
Change `langgraph` import from a deferred `try/except` import to a top-level module import (it is now a required dependency).

```python
# BEFORE — dual-path entry point
async def run_graph_with_orchestrator(
    graph: Graph,
    inputs: list[dict[str, str]],
    *,
    ...
    backend: str = "legacy",         # ← removed
) -> list[RunOutputs]:
    if backend != "langgraph":
        return await graph.arun(...)  # ← removed
    return await _run_with_langgraph(...)

# BEFORE — separate helper with fallback
async def _run_with_langgraph(...) -> list[RunOutputs]:
    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        return await graph.arun(...)  # ← removed
    ...

# AFTER — single-path, langgraph imported at module top
from langgraph.graph import END, StateGraph

async def run_graph_with_orchestrator(
    graph: Graph,
    inputs: list[dict[str, str]],
    *,
    ...
    # no backend parameter
) -> list[RunOutputs]:
    # LangGraph StateGraph directly here
    ...
```

---

### Step 3 — Remove `orchestrator_backend` setting

**File:** `src/backend/base/langflow/services/settings/base.py`

Delete the duplicated `a2a_enabled` definition and the `orchestrator_backend` field:

```python
# BEFORE (lines 167-171)
a2a_enabled: bool = True
"""Whether to expose Agent2Agent (A2A) interoperability endpoints."""
orchestrator_backend: Literal["legacy", "langgraph"] = "legacy"
"""Execution orchestrator backend. Use 'legacy' for the current graph runtime and
'langgraph' to route graph runs through the LangGraph adapter."""

a2a_enabled: bool = True    # ← duplicate declaration also removed
```

After removal only a single `a2a_enabled` field remains.

---

### Step 4 — Update `process.py` callers

**File:** `src/backend/base/langflow/processing/process.py`

Two call-sites read `settings.orchestrator_backend` and passed `backend=orchestrator_backend` into `run_graph_with_orchestrator()`. Remove both.

```python
# BEFORE
orchestrator_backend = get_settings_service().settings.orchestrator_backend
run_outputs = await run_graph_with_orchestrator(
    ...,
    backend=orchestrator_backend,   # ← removed
)

# AFTER
run_outputs = await run_graph_with_orchestrator(
    ...,
    # no backend= argument
)
```

---

### Step 5 — Update `helpers/flow.py` callers

**File:** `src/backend/base/langflow/helpers/flow.py`

`run_flow()` called `graph.arun()` directly. Replace with `run_graph_with_orchestrator()`. Use a **lazy local import** to avoid the circular import chain:
`helpers.flow` → `processing.orchestrator` → `graph.graph.base` → `custom.component` → `helpers.flow`.

```python
# BEFORE
return await graph.arun(
    inputs_list,
    outputs=outputs,
    inputs_components=inputs_components,
    types=types,
    fallback_to_env_vars=fallback_to_env_vars,
)

# AFTER
from langflow.processing.orchestrator import run_graph_with_orchestrator  # avoid circular import

return await run_graph_with_orchestrator(
    graph=graph,
    inputs=inputs_list,
    outputs=outputs,
    inputs_components=inputs_components,
    types=types,
    fallback_to_env_vars=fallback_to_env_vars,
)
```

---

### Step 6 — Add `langgraph` as a required dependency

**File:** `src/backend/base/pyproject.toml`

Add `langgraph` to the `dependencies` list, immediately after the other `langchain-*` packages:

```toml
# BEFORE
    "langchainhub~=0.1.15",
    "loguru>=0.7.1,<1.0.0",

# AFTER
    "langchainhub~=0.1.15",
    "langgraph>=0.2.0,<1.0.0",
    "loguru>=0.7.1,<1.0.0",
```

---

### Step 7 — Update orchestrator unit tests

**File:** `src/backend/tests/unit/test_orchestrator.py`

Remove two legacy-specific tests that tested the `backend="legacy"` path and the `backend="langgraph"` fallback when `langgraph` was not installed:

- `test_legacy_orchestrator_uses_graph_arun` — deleted (legacy path gone)
- `test_langgraph_falls_back_to_legacy_when_dependency_missing` — deleted (no fallback)

Also remove the no-longer-needed `DummyGraph.arun()` mock method and clean up unused `RunOutputs` import.

The single surviving test, `test_langgraph_backend_uses_graph_private_run`, is updated to call `run_graph_with_orchestrator()` without a `backend` keyword argument.

---

## Part 2 — Non-Core 3rd Party Component Removal

### Background

The Langflow component tree had grown to include many thin wrappers around external SaaS APIs and LangChain community integrations. Many of these:

- Depended on optional/unstable 3rd-party packages (e.g., `dspy-ai`, `metaphor-python`, `wolframalpha`, `pyarrow`).
- Were empty stub directories (`chains/`, `documentloaders/`, `link_extractors/`, etc.) with only an `__init__.py`.
- Duplicated functionality available via MCP or more generic tool patterns.

**Preserved integrations** that were explicitly excluded from removal:

| Component | Reason to keep |
|-----------|---------------|
| `confluence/` | Active enterprise use-case; enterprise first-pass filter already covers it |
| `sharepoint/` | Active enterprise use-case; uses only `httpx` (no extra dep) |
| `tools/datahub_graphql_mcp.py` | DataHub MCP integration; uses only `httpx` |

---

### Step 8 — Delete empty and deprecated component directories

The following directories contained only `__init__.py` stubs or deactivated components:

```
src/backend/base/langflow/components/chains/          # empty stub
src/backend/base/langflow/components/deactivated/     # all contents inactive
src/backend/base/langflow/components/documentloaders/ # empty stub
src/backend/base/langflow/components/link_extractors/ # empty stub
src/backend/base/langflow/components/output_parsers/  # empty stub
src/backend/base/langflow/components/textsplitters/   # empty stub
src/backend/base/langflow/components/toolkits/        # empty stub
```

**Command:**
```bash
rm -rf src/backend/base/langflow/components/chains/ \
       src/backend/base/langflow/components/deactivated/ \
       src/backend/base/langflow/components/documentloaders/ \
       src/backend/base/langflow/components/link_extractors/ \
       src/backend/base/langflow/components/output_parsers/ \
       src/backend/base/langflow/components/textsplitters/ \
       src/backend/base/langflow/components/toolkits/
```

---

### Step 9 — Delete the retrievers directory

**Directory:** `src/backend/base/langflow/components/retrievers/`

Contains `amazon_kendra.py`, `metal.py`, and `multi_query.py` — all require heavy optional dependencies (`boto3`, `metal_sdk`, `langchain-community`) and serve very niche use cases.

```bash
rm -rf src/backend/base/langflow/components/retrievers/
```

---

### Step 10 — Remove niche 3rd party tools

**Directory:** `src/backend/base/langflow/components/tools/`

The following tool files are removed (all depend on 3rd-party packages listed in the root `pyproject.toml` that can now be dropped):

| File removed | External dependency |
|---|---|
| `arxiv.py` | `arxiv` |
| `astradb.py` | `langchain-astradb` |
| `astradb_cql.py` | `astrapy` |
| `bing_search_api.py` | `langchain-community` (BingSearchAPI) |
| `duck_duck_go_search_run.py` | `duckduckgo_search` |
| `exa_search.py` | `exa_py` |
| `glean_search_api.py` | (proprietary Glean API) |
| `search.py` | `langchain-community` (SearchAPI) |
| `search_api.py` | `google-search-results` |
| `searxng.py` | (self-hosted SearXNG) |
| `serp.py` | `google-search-results` |
| `serp_api.py` | `google-search-results` |
| `tavily.py` | `tavily-python` |
| `tavily_search.py` | `tavily-python` |
| `wikidata.py` | `langchain-community` |
| `wikidata_api.py` | `httpx` (kept in base, but component removed) |
| `wikipedia.py` | `wikipedia` |
| `wikipedia_api.py` | `wikipedia` |
| `wolfram_alpha_api.py` | `wolframalpha` |
| `yahoo.py` | `yfinance` |
| `yahoo_finance.py` | `yfinance` |

**Retained tools** (core, no extra dependencies beyond `langchain-core`):

| File kept | Reason |
|---|---|
| `calculator.py` / `calculator_core.py` | Pure Python math, no 3rd-party dep |
| `mcp_component.py` | Core MCP protocol integration |
| `python_code_structured_tool.py` | Core code execution |
| `python_repl.py` / `python_repl_core.py` | Core code execution |
| `datahub_graphql_mcp.py` | DataHub — **explicitly preserved** |

---

### Step 11 — Update `tools/__init__.py`

**File:** `src/backend/base/langflow/components/tools/__init__.py`

Replace the full import list with only the retained tools plus DataHub:

```python
# AFTER
from .calculator import CalculatorToolComponent
from .calculator_core import CalculatorComponent
from .datahub_graphql_mcp import DataHubGraphQLMCPComponent
from .mcp_component import MCPToolsComponent
from .python_code_structured_tool import PythonCodeStructuredTool
from .python_repl import PythonREPLToolComponent
from .python_repl_core import PythonREPLComponent

__all__ = [
    "CalculatorComponent",
    "CalculatorToolComponent",
    "DataHubGraphQLMCPComponent",
    "MCPToolsComponent",
    "PythonCodeStructuredTool",
    "PythonREPLComponent",
    "PythonREPLToolComponent",
]
```

---

### Step 12 — Update `interface/components.py` standard types

**File:** `src/backend/base/langflow/interface/components.py`

The `discover_component_types()` function maintained a hard-coded `standard_types` set that included category names for the deleted directories. Remove the stale entries:

```python
# BEFORE
standard_types = {
    "agents",
    "chains",          # ← removed
    "embeddings",
    "llms",
    "memories",
    "prompts",
    "tools",
    "retrievers",      # ← removed
    "textsplitters",   # ← removed
    "toolkits",        # ← removed
    "utilities",
    "vectorstores",
    "custom_components",
    "documentloaders", # ← removed
    "outputparsers",   # ← removed
    "wrappers",
}

# AFTER
standard_types = {
    "agents",
    "embeddings",
    "llms",
    "memories",
    "prompts",
    "tools",
    "utilities",
    "vectorstores",
    "custom_components",
    "wrappers",
}
```

---

### Step 13 — Remove tests for deleted components

Delete the test files whose components no longer exist:

```
src/backend/tests/unit/components/tools/test_arxiv_component.py
src/backend/tests/unit/components/tools/test_datahub_graphql_mcp.py  ← KEEP (DataHub preserved)
src/backend/tests/unit/components/tools/test_google_search_api.py
src/backend/tests/unit/components/tools/test_google_serper_api_core.py
src/backend/tests/unit/components/tools/test_serp_api.py
src/backend/tests/unit/components/tools/test_wikidata_api.py
src/backend/tests/unit/components/tools/test_wikipedia_api.py
src/backend/tests/unit/components/tools/test_yfinance_tool.py
```

The confluence and sharepoint test directories are **preserved** because those components remain.

---

## Part 3 — Frontend Changes

### Step 14 — Remove deleted categories from sidebar

**File:** `src/frontend/src/utils/styleUtils.ts`

`SIDEBAR_CATEGORIES` renders category tabs in the component sidebar. Remove entries whose backend directories were deleted:

```typescript
// BEFORE
export const SIDEBAR_CATEGORIES = [
  ...
  { display_name: "Chains", name: "chains", icon: "Link" },           // ← removed
  { display_name: "Loaders", name: "documentloaders", icon: "Paperclip" }, // ← removed
  { display_name: "Link Extractors", name: "link_extractors", icon: "Link2" }, // ← removed
  { display_name: "Output Parsers", name: "output_parsers", icon: "Compass" }, // ← removed
  { display_name: "Prototypes", name: "prototypes", icon: "FlaskConical" }, // ← removed
  { display_name: "Retrievers", name: "retrievers", icon: "FileSearch" }, // ← removed
  { display_name: "Text Splitters", name: "textsplitters", icon: "Scissors" }, // ← removed
  { display_name: "Toolkits", name: "toolkits", icon: "Package2" }, // ← removed
  ...
];
```

`Confluence` and `SharePoint` remain in `SIDEBAR_BUNDLES` because those components are preserved.

Remove stale entries from `categoryIcons` and `nodeIconsLucide` objects for the deleted categories (`chains`, `documentloaders`, `langchain_utilities`, `link_extractors`, `output_parsers`, `prototypes`, `retrievers`, `textsplitters`, `toolkits`).

> Note: The `ConfluenceIcon` import and the `Confluence`/`SharePoint` entries in `nodeIconsLucide` are **not** removed because those bundle components are preserved.

---

### Step 15 — Update `SIDEBAR_BUNDLES` (no change needed)

`SIDEBAR_BUNDLES` in `styleUtils.ts` continues to include both `Confluence` and `SharePoint` entries since those components are preserved.

```typescript
// UNCHANGED
export const SIDEBAR_BUNDLES = [
  { display_name: "Confluence", name: "confluence", icon: "Confluence" },
  { display_name: "SharePoint", name: "sharepoint", icon: "SharePoint" },
];
```

---

### Step 16 — Keep `AVAILABLE_TOOLS` in AgentsPage

**File:** `src/frontend/src/pages/AgentsPage/components/constants.ts`

The `SharePointFilesLoader` entry in `AVAILABLE_TOOLS` is **preserved** because the SharePoint component remains:

```typescript
// UNCHANGED
export const AVAILABLE_TOOLS = [
  {
    id: "SharePointFilesLoader",
    name: "SharePoint Files Loader",
    description:
      "Load files from SharePoint document libraries using Microsoft Graph.",
  },
];
```

---

## Summary of files changed / deleted

### Backend — files deleted

| Path | Reason |
|------|--------|
| `components/chains/__init__.py` | Empty stub |
| `components/deactivated/*` | All contents inactive |
| `components/documentloaders/__init__.py` | Empty stub |
| `components/link_extractors/__init__.py` | Empty stub |
| `components/output_parsers/__init__.py` | Empty stub |
| `components/retrievers/__init__.py` | 3rd-party retrievers removed |
| `components/retrievers/amazon_kendra.py` | `boto3` dependency |
| `components/retrievers/metal.py` | `metal_sdk` dependency |
| `components/retrievers/multi_query.py` | `langchain-community` |
| `components/textsplitters/__init__.py` | Empty stub |
| `components/toolkits/__init__.py` | Empty stub |
| `components/tools/arxiv.py` | `arxiv` dependency |
| `components/tools/astradb.py` | `langchain-astradb` |
| `components/tools/astradb_cql.py` | `astrapy` |
| `components/tools/bing_search_api.py` | `google-search-results` |
| `components/tools/duck_duck_go_search_run.py` | `duckduckgo_search` |
| `components/tools/exa_search.py` | `exa_py` |
| `components/tools/glean_search_api.py` | proprietary API |
| `components/tools/search.py` | `google-search-results` |
| `components/tools/search_api.py` | `google-search-results` |
| `components/tools/searxng.py` | self-hosted only |
| `components/tools/serp.py` / `serp_api.py` | `google-search-results` |
| `components/tools/tavily.py` / `tavily_search.py` | `tavily-python` |
| `components/tools/wikidata.py` / `wikidata_api.py` | `langchain-community` |
| `components/tools/wikipedia.py` / `wikipedia_api.py` | `wikipedia` |
| `components/tools/wolfram_alpha_api.py` | `wolframalpha` |
| `components/tools/yahoo.py` / `yahoo_finance.py` | `yfinance` |

### Backend — files modified

| Path | Change |
|------|--------|
| `graph/graph/base.py` | Deleted `Graph.arun()`, removed unused `RunOutputs` import |
| `processing/orchestrator.py` | Collapsed to single LangGraph path; removed `backend` param |
| `processing/process.py` | Removed `orchestrator_backend` usage |
| `helpers/flow.py` | Replaced `graph.arun()` with `run_graph_with_orchestrator()` |
| `services/settings/base.py` | Removed `orchestrator_backend` setting |
| `interface/components.py` | Removed stale category names from `standard_types` |
| `components/tools/__init__.py` | Export only retained tools + DataHub |
| `base/pyproject.toml` | Added `langgraph>=0.2.0,<1.0.0` dependency |

### Tests — files deleted

| Path | Reason |
|------|--------|
| `tests/unit/components/tools/test_arxiv_component.py` | Component removed |
| `tests/unit/components/tools/test_google_search_api.py` | Component removed |
| `tests/unit/components/tools/test_google_serper_api_core.py` | Component removed |
| `tests/unit/components/tools/test_serp_api.py` | Component removed |
| `tests/unit/components/tools/test_wikidata_api.py` | Component removed |
| `tests/unit/components/tools/test_wikipedia_api.py` | Component removed |
| `tests/unit/components/tools/test_yfinance_tool.py` | Component removed |

### Tests — files preserved

| Path | Reason |
|------|--------|
| `tests/unit/components/confluence/` | Confluence component kept |
| `tests/unit/components/data/test_sharepoint_files_loader.py` | SharePoint component kept |
| `tests/unit/components/tools/test_datahub_graphql_mcp.py` | DataHub component kept |

### Tests — files modified

| Path | Change |
|------|--------|
| `tests/unit/test_orchestrator.py` | Removed legacy-path tests; kept LangGraph test |
| `tests/unit/test_interface_components.py` | Removed stale confluence assertions (no change needed — component kept) |

### Frontend — files modified

| Path | Change |
|------|--------|
| `src/frontend/src/utils/styleUtils.ts` | Removed deleted categories from `SIDEBAR_CATEGORIES`, `categoryIcons`, `nodeIconsLucide`; **`SIDEBAR_BUNDLES` unchanged** |
