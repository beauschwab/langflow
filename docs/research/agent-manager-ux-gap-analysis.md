# Agent Manager UX Gap Analysis: Open Agent Platform → Langflow / NovaFlow

## Executive summary

This document evaluates the [Open Agent Platform frontend UX spec](https://github.com/beauschwab/open-agent-platform/blob/copilot/deep-dive-analysis-frontend/apps/docs/setup/frontend-ux-spec.mdx) against the current Langflow codebase to identify features that should be incorporated for building and managing custom agents, tools, and MCP nodes within NovaFlow workflows. It focuses on gaps that, once addressed, would create an intuitive, organized, enterprise-ready experience supporting a multi-tenant approach.

### Implementation status

Phase 1 foundational work has been implemented:
- **Backend:** `Agent` SQLModel entity (`models/agent/`), CRUD API at `/api/v1/agents/` with auth, search, and type filtering
- **Frontend:** `/agents` page with card grid, search, create dialog; Zustand store (`agentStore.ts`); React Query hooks
- **Tests:** Backend pytest suite at `tests/unit/api/v1/test_agents.py` covering full CRUD lifecycle

### Reference artifacts reviewed

| Source | Path / URL | Location |
|--------|-----------|----------|
| Open Agent Platform UX spec | `apps/docs/setup/frontend-ux-spec.mdx` (copilot/deep-dive-analysis-frontend branch) | [beauschwab/open-agent-platform](https://github.com/beauschwab/open-agent-platform) repo |
| Langflow frontend | `src/frontend/src/` (routes, stores, components) | This repo |
| Langflow backend | `src/backend/base/langflow/` (API, models, services) | This repo |
| LangGraph migration research | `docs/research/python-backend-langgraph-deep-dive.md` | This repo |
| Frontend architecture docs | `src/frontend/docs/agents/` | This repo |

---

## 1. Current Langflow capabilities inventory

### 1.1 Agent management

| Capability | Status | Details |
|-----------|--------|---------|
| Agent as flow component | ✅ Present | `LCAgentComponent`, `ToolCallingAgentComponent` in `base/agents/agent.py` |
| Agent templates | ✅ Partial | Starter templates (Travel Planning, Dynamic Agent, etc.) available in flow-template constants |
| Agent CRUD lifecycle | ❌ Missing | Agents are not standalone entities — they only exist as nodes inside flows |
| Agent versioning | ❌ Missing | No revision history, rollback, or draft/published model |
| Agent performance dashboard | ❌ Missing | No agent-level metrics or execution analytics |
| Agent access control | ❌ Missing | No per-agent sharing policies or role scoping |

### 1.2 Tool and MCP management

| Capability | Status | Details |
|-----------|--------|---------|
| Tool catalog | ✅ Present | 25+ tool components in `components/tools/` |
| MCP server integration | ✅ Present | SSE and Stdio MCP connection modes in `mcp_component.py` |
| MCP server endpoint | ✅ Present | `api/v1/mcp.py` implements `langflow-mcp-server` |
| Centralized tool registry | ❌ Missing | Tools are per-component instances, not a shared catalog |
| Tool playground/testing | ❌ Missing | No interactive tool testing sandbox |
| Tool governance and audit | ❌ Missing | No approval workflows, usage tracking, or permission scoping |

### 1.3 Multi-tenancy and RBAC

| Capability | Status | Details |
|-----------|--------|---------|
| User authentication | ✅ Present | Login, signup, API key auth via FastAPI |
| User-scoped flows | ✅ Present | `user_id` FK on flows, variables, folders |
| Organization/workspace model | ❌ Missing | No `Organization`, `Workspace`, or `Team` models |
| Role-based access control | ❌ Missing | Only `is_superuser` flag; no fine-grained roles |
| Tenant isolation middleware | ❌ Missing | No org-level data isolation or quota enforcement |
| Org-level settings | ❌ Missing | No org-scoped billing, usage tracking, or configuration |

### 1.4 UI architecture

| Capability | Status | Details |
|-----------|--------|---------|
| Flow canvas editor | ✅ Present | Full node/edge visual programming |
| Zustand state management | ✅ Present | Multiple domain stores (`flowStore`, `authStore`, `typesStore`) |
| React Query API layer | ✅ Present | Custom hooks with centralized request processor |
| URL-driven state | ❌ Missing | Flow IDs in paths, but no deep query-param synchronization for agents/tools |
| Schema-driven forms | ❌ Missing | Component params are hardcoded per type, not dynamically generated from backend schemas |

---

## 2. Open Agent Platform UX features breakdown

The OAP UX spec defines seven primary tabs and four cross-cutting interaction patterns. Below is a feature-by-feature summary with relevance assessment for Langflow/NovaFlow.

### 2.1 Agent management features (high relevance)

| OAP Feature | Description | Langflow equivalent | Gap level |
|------------|-------------|-------------------|-----------|
| **Two-lens agent navigation** | Templates tab (grouped by deployment/graph) + All Agents tab (flat searchable inventory) | Flows page with folder organization | 🔴 Major |
| **Agent card metadata** | Name, deployment badges, description, config badges (RAG, MCP Tools, Supervisor) | Flow list with name/description only | 🟡 Moderate |
| **Create Agent dialog** | Multi-step: graph targeting → schema-driven form → sectioned fields (details, config, tools, RAG, supervisor) | No agent creation workflow; agents are flow nodes | 🔴 Major |
| **Edit Agent dialog** | Schema-driven form prefilled from existing config with update/delete | No agent editing; only flow node property editing | 🔴 Major |
| **Schema-driven agent config** | Backend metadata defines form fields; frontend renders typed controls dynamically | Component params use fixed templates | 🟡 Moderate |
| **Agent template grouping** | Agents grouped by `deploymentId:graphId` with expand/collapse | No deployment/graph grouping concept | 🔴 Major |
| **Agent state architecture** | Global `AgentsProvider` + `useAgents` CRUD hook + `useAgentConfig` schema hook | No equivalent provider; agents are flow-embedded | 🔴 Major |

### 2.2 Tool management features (high relevance)

| OAP Feature | Description | Langflow equivalent | Gap level |
|------------|-------------|-------------------|-----------|
| **Tool discovery catalog** | Searchable card grid with pagination, skeleton loading, empty states | Component sidebar with category tree | 🟡 Moderate |
| **Tool card interaction** | Title, description, playground link, details dialog | No per-tool cards; tools are sidebar list items | 🟡 Moderate |
| **Tool playground** | Schema-driven input form → execute → response viewer with Pretty/Raw tabs | No tool testing sandbox | 🔴 Major |
| **Tool details dialog** | Full tool metadata with schema inspection | Minimal — node tooltip shows basic info | 🟡 Moderate |
| **URL-addressable playground** | `?tool=<name>` deep-link for tool testing | No URL-based tool state | 🟡 Moderate |
| **Schema-native form generation** | Input fields auto-generated from `inputSchema.properties` (enum, string, number, boolean, slider) | Not present; tools have fixed input templates | 🔴 Major |
| **Cursor pagination** | Load-more pagination for large tool inventories | No pagination in component sidebar | 🟡 Moderate |

### 2.3 Chat features (moderate relevance)

| OAP Feature | Description | Langflow equivalent | Gap level |
|------------|-------------|-------------------|-----------|
| **Thread-based chat** | Conversational turns with tool-call rendering | Playground chat available per-flow | 🟢 Minor |
| **Side panel progressive disclosure** | Thread history + configuration sidebars | Playground has basic chat panel | 🟡 Moderate |
| **Stream provider** | Runtime host for conversation state and LangGraph streaming | Event streaming exists via SSE | 🟢 Minor |
| **Agent/deployment context in URL** | `agentId`, `deploymentId`, `threadId` as query params | Flow ID in URL path only | 🟡 Moderate |

### 2.4 RAG management features (moderate relevance)

| OAP Feature | Description | Langflow equivalent | Gap level |
|------------|-------------|-------------------|-----------|
| **Collection management** | Create/edit/delete collections with document upload | RAG components exist (vector stores, embeddings) but no collection management UI | 🟡 Moderate |
| **Document table** | Per-collection document listing with CRUD | No document management outside flow canvas | 🟡 Moderate |

### 2.5 Cross-cutting UX patterns (high relevance)

| OAP Pattern | Description | Langflow equivalent | Gap level |
|------------|-------------|-------------------|-----------|
| **URL as state contract** | `nuqs` query-param sync for all entity selections | URL paths used for routing only; no deep query-param sync | 🟡 Moderate |
| **Schema-driven UIs** | Backend metadata drives form generation across agents and tools | Component forms use fixed templates per type | 🔴 Major |
| **Progressive disclosure** | Complexity moved into dialogs, sidebars, and tabs | Basic modal usage; canvas is primary surface | 🟡 Moderate |
| **Operational feedback** | Skeletons, empty states, toast alerts, loading button states | Toast alerts present; skeletons and empty states inconsistent | 🟡 Moderate |
| **Global provider stack** | `SidebarProvider > MCPProvider > AgentsProvider > RagProvider` | Zustand stores loaded independently; no unified provider hierarchy | 🟡 Moderate |

---

## 3. Gap analysis matrix

### 3.1 Priority classification

| Priority | Criteria |
|----------|---------|
| **P0 — Critical** | Core missing feature that blocks enterprise agent management use cases |
| **P1 — High** | Feature that significantly improves usability and operator efficiency |
| **P2 — Medium** | Enhancement that improves consistency and discoverability |
| **P3 — Low** | Polish or parity feature with diminishing enterprise ROI |

### 3.2 Gap matrix

| # | Gap | OAP reference | Current state | Priority | Enterprise impact |
|---|-----|--------------|---------------|----------|------------------|
| G1 | **No standalone agent entity model** | Agents tab, `AgentsProvider`, agent CRUD | Agents are flow nodes only | P0 | Blocks agent lifecycle, sharing, and governance |
| G2 | **No multi-tenant data model** | N/A (implicit in enterprise context) | Flat `user_id` scoping only | P0 | Blocks org isolation, RBAC, and quota management |
| G3 | **No agent CRUD workflow** | Create/Edit Agent dialogs, `useAgents` hook | No agent management UI or API | P0 | No way to manage agents outside flow editing |
| G4 | **No schema-driven form generation** | `AgentFieldsForm`, `SchemaForm`, `ConfigField` | Hardcoded component templates | P1 | Limits extensibility and dynamic tool/agent config |
| G5 | **No tool playground** | `/tools/playground`, `SchemaForm`, `ResponseViewer` | No interactive tool testing | P1 | Operators cannot validate tools before production use |
| G6 | **No tool catalog page** | `/tools` page with search, cards, pagination | Sidebar list in flow editor only | P1 | Tools are invisible outside flow editing context |
| G7 | **No agent inventory views** | Templates tab + All Agents tab | Flow list is the only navigation | P1 | No way to see all agents across flows/deployments |
| G8 | **No agent card metadata** | Config badges, deployment badges, description | Flow cards show minimal metadata | P2 | Reduced comprehension for operators managing many agents |
| G9 | **No URL-driven entity context** | `nuqs` query-param sync | URL paths for routing only | P2 | No deep-linking or shareable agent/tool context |
| G10 | **No RBAC beyond superuser** | N/A (implicit) | `is_superuser` flag only | P0 | No role-based permissions for enterprise workflows |
| G11 | **No agent template grouping** | `groupAgentsByGraphs` deployment/graph accordion | Flat flow list with folders | P2 | Harder to organize agents at scale |
| G12 | **No RAG collection management UI** | RAG tab with collection/document CRUD | RAG components in flows only | P2 | No standalone data management outside flow editing |
| G13 | **No consistent empty/loading states** | Skeleton cards, empty-state CTAs, load-more | Inconsistent loading patterns | P3 | Reduced polish but not blocking |
| G14 | **No global provider architecture** | Sidebar → MCP → Agents → RAG provider stack | Independent Zustand stores | P3 | Current approach works; provider stack is a nice-to-have |

---

## 4. Feature recommendations with implementation guidance

### 4.1 P0: Agent entity model and CRUD (G1, G3)

**What to build:**
An `Agent` database model and API surface that treats agents as first-class entities independent of (but composable within) flows.

**Backend changes:**

```
src/backend/base/langflow/services/database/models/agent/
├── model.py          # Agent SQLModel: id, name, description, config_json,
│                     #   graph_id, deployment_id, user_id, org_id, created_at, updated_at
└── crud.py           # CRUD operations: create, read, update, delete, list with filters

src/backend/base/langflow/api/v1/agents.py
    # REST endpoints: GET/POST /agents, GET/PUT/DELETE /agents/{agent_id}
    # Query params: graph_filter, search, page, per_page
```

**Frontend changes:**

```
src/frontend/src/pages/agents/
├── index.tsx         # Agents page with two-tab layout (Templates + All Agents)
├── components/
│   ├── agent-card.tsx           # Card with name, badges, description, actions
│   ├── agent-dashboard.tsx      # Searchable grid with graph filter
│   ├── templates-list.tsx       # Deployment/graph grouped accordion
│   ├── create-agent-dialog.tsx  # Multi-step create form
│   └── edit-agent-dialog.tsx    # Schema-driven edit form

src/frontend/src/stores/agentStore.ts   # Zustand store for agent state
src/frontend/src/api/agents/            # React Query hooks for agent CRUD
```

**Key design decisions:**
- Agents reference flows/graphs but are independently manageable
- Agent config stored as typed JSON with schema validation (Pydantic model)
- Two-lens navigation (Templates + All Agents) as described in OAP spec
- Inline modal CRUD to preserve operator context (no full-page mode switches)

### 4.2 P0: Multi-tenant data model (G2, G10)

**What to build:**
Organization and workspace models with RBAC, enabling tenant-scoped data isolation and role-based access control.

**Backend changes:**

```
src/backend/base/langflow/services/database/models/
├── organization/
│   └── model.py      # Organization: id, name, slug, settings_json, created_at
├── workspace/
│   └── model.py      # Workspace: id, name, org_id, settings_json
├── membership/
│   └── model.py      # OrgMembership: user_id, org_id, role (owner|admin|member|viewer)
└── rbac/
    └── permissions.py # Permission definitions and evaluation logic

src/backend/base/langflow/middleware/tenant.py
    # Middleware: extract org context from request, enforce data isolation

src/backend/base/langflow/api/v1/organizations.py
    # REST endpoints: org CRUD, membership management, workspace management
```

**Data isolation strategy:**
- Add `org_id` FK to `Flow`, `Agent`, `Variable`, `Folder`, and all entity tables
- Middleware intercepts requests and injects `org_id` into query context
- All queries automatically scoped to authenticated org
- Superuser bypasses org scoping for platform administration

**RBAC role model:**

| Role | Agents | Flows | Tools | Settings | Members |
|------|--------|-------|-------|----------|---------|
| Viewer | Read | Read | Read | — | — |
| Member | CRUD own | CRUD own | Read | — | — |
| Admin | CRUD all | CRUD all | CRUD all | Read/Write | Invite/Remove |
| Owner | CRUD all | CRUD all | CRUD all | Read/Write | Full control |

### 4.3 P1: Schema-driven form generation (G4)

**What to build:**
A dynamic form renderer that generates UI controls from backend-provided JSON Schema metadata, used for both agent configuration and tool execution.

**Implementation approach:**

```
src/frontend/src/components/schema-form/
├── index.tsx              # SchemaForm: renders fields from JSON Schema properties
├── config-field.tsx       # ConfigField: dispatches to typed control based on schema type
├── field-types/
│   ├── string-field.tsx   # text input, textarea
│   ├── enum-field.tsx     # select/combobox
│   ├── number-field.tsx   # numeric input or slider (when min/max present)
│   ├── boolean-field.tsx  # switch/checkbox
│   └── object-field.tsx   # nested object renderer
└── response-viewer.tsx    # Pretty (nested object) + Raw (JSON) tabs
```

**Backend support:**
- Agent `config_schema` endpoint returns JSON Schema for dynamic form hydration
- Tool `inputSchema` already available via MCP protocol; surface it through Langflow API
- Required fields visually marked; descriptions surfaced inline

**Mapping rules (from OAP spec):**

| Schema type | Constraints | UI control |
|------------|------------|------------|
| `string` | `enum` present | Select/Combobox |
| `string` | no enum | Text Input |
| `number`/`integer` | `minimum` + `maximum` | Slider + numeric readout |
| `number`/`integer` | no range | Numeric input |
| `boolean` | — | Switch |
| `object` | — | Nested form or JSON editor |
| fallback | — | Text input |

### 4.4 P1: Tool catalog page (G6)

**What to build:**
A standalone `/tools` page that provides tool discovery, inspection, and management outside the flow editor.

**Frontend changes:**

```
src/frontend/src/pages/tools/
├── index.tsx               # Tool catalog: header, search, responsive card grid
├── playground/
│   └── index.tsx           # Tool playground: select tool → schema form → execute → response
└── components/
    ├── tool-card.tsx        # Title, description, playground link, details button
    ├── tool-details-dialog.tsx  # Full schema inspection
    └── tool-card-loading.tsx    # Skeleton loading placeholder
```

**Interaction model (from OAP spec):**
1. **Catalog first** — browse/search tools in card grid with cursor pagination
2. **Inspect** — open details dialog to see full schema and metadata
3. **Test** — navigate to playground with `?tool=<name>` deep-link
4. **Use** — drag tools into flow editor (existing capability)

**Playground execution model:**
- Schema-driven input form generated from `inputSchema.properties`
- Execute via `callTool({ name, args })` API endpoint
- Response viewer with Pretty (nested object renderer) and Raw (JSON) tabs
- MCP auth-required handling with specialized info card when `code -32003` received

### 4.5 P1: Agent inventory views (G7)

**What to build:**
Two complementary navigation views for agents, matching the OAP two-lens model.

**Templates tab:**
- Groups agents by deployment and graph using accordion-style cards
- Expand/collapse state stored locally as `deploymentId:graphId` keys
- Search filters by graph ID or agent name
- Empty state with guidance copy and create CTA

**All Agents tab:**
- Flat searchable grid with graph filter dropdown (`All Templates` + deployment/graph options)
- Count header (`N Agent(s)`)
- Responsive card grid (1/2/3 columns)
- Sequential filters: graph filter → name text match

### 4.6 P2: Agent card metadata and badges (G8)

**What to build:**
Rich agent cards that communicate configuration state at a glance.

**Card contents:**
- Agent name and description
- Deployment + graph badges with tooltips
- Config capability badges:
  - 🔵 **RAG** — agent has RAG collections configured
  - 🟢 **MCP Tools** — agent has MCP tool connections
  - 🟡 **Supervisor** — agent acts as supervisor over sub-agents
- Actions: **Edit** (modal) and **Chat** (deep-link to playground)

### 4.7 P2: URL-driven entity context (G9)

**What to build:**
Query-parameter synchronization for entity selections across pages, enabling deep-linking and browser navigation correctness.

**Implementation:**
- Use a URL state management library (equivalent to `nuqs` in OAP) — consider `use-query-params` or built-in React Router search params
- Key state parameters:
  - `/agents`: `tab`, `search`, `graphFilter`
  - `/tools`: `search`
  - `/tools/playground`: `tool`
  - `/chat`: `agentId`, `deploymentId`, `threadId`
- Benefits: shareable URLs, back/forward correctness, reload persistence

### 4.8 P2: RAG collection management UI (G12)

**What to build:**
A standalone `/rag` page with collection and document management.

**Layout (from OAP spec):**
- Responsive 1:2 column split
- Left: collections list with create/edit/delete dialogs
- Right: document table for selected collection with upload/delete

### 4.9 P2: Agent template grouping (G11)

**What to build:**
Grouping logic that organizes agents by their underlying graph/deployment for the Templates view.

**Implementation:**
- `groupAgentsByGraphs(agents)` utility that groups agent array by `deploymentId:graphId`
- Accordion-style UI with deployment name as group header
- Filter applies across both group label and child agent names

### 4.10 P3: Consistent operational feedback (G13)

**What to build:**
Standardized loading, empty, and error state patterns across all pages.

**Patterns to implement:**
- **Skeleton loading**: 6-card skeleton grid during initial fetch (matching OAP `ToolCardLoading`, `TemplatesLoading`)
- **Empty states**: Dashed container with icon, help text, and primary action CTA
- **Toast feedback**: Already partially present; standardize for all mutations
- **Loading buttons**: Disabled state with spinner during mutations

### 4.11 P3: Global provider architecture (G14)

**What to build:**
A unified provider hierarchy that gives all pages access to core entities.

**Recommended stack (adapted from OAP):**

```
AuthProvider
  └── OrganizationProvider    (multi-tenant context)
        └── MCPProvider       (tool state)
              └── AgentsProvider  (agent state)
                    └── RagProvider   (RAG collection state)
                          └── AppShell  (sidebar, navigation, content)
```

This can coexist with existing Zustand stores — providers handle cross-cutting entity lifecycle while stores handle page-specific UI state.

---

## 5. Multi-tenant enterprise considerations

### 5.1 Data isolation model

```
┌─────────────────────────────────┐
│           Platform              │
│  ┌───────────┐  ┌───────────┐  │
│  │  Org A    │  │  Org B    │  │
│  │  ┌─────┐  │  │  ┌─────┐  │  │
│  │  │ WS1 │  │  │  │ WS1 │  │  │
│  │  └─────┘  │  │  └─────┘  │  │
│  │  ┌─────┐  │  │  ┌─────┐  │  │
│  │  │ WS2 │  │  │  │ WS2 │  │  │
│  │  └─────┘  │  │  └─────┘  │  │
│  └───────────┘  └───────────┘  │
└─────────────────────────────────┘
```

**Isolation guarantees required:**
- All database queries scoped to `org_id` via middleware
- API keys and secrets are org-scoped (never leak across orgs)
- MCP server connections are org-scoped (tool namespacing)
- Flow execution runs within org context (no cross-org state leakage)
- Admin panel restricted to org admins; platform admin separate

### 5.2 Tenant-aware entity scoping

| Entity | Current scope | Required scope |
|--------|--------------|----------------|
| Flow | `user_id` | `org_id` + `user_id` (personal) or `org_id` (shared) |
| Agent | N/A | `org_id` + `workspace_id` (optional) |
| Tool connection | Per-component instance | `org_id` (shared MCP connections) |
| Variable | `user_id` | `org_id` + visibility (org/personal) |
| API key | `user_id` | `org_id` + `user_id` |
| Folder | `user_id` | `org_id` + visibility |

### 5.3 RBAC implementation approach

**Recommended approach:** middleware + decorator pattern

```python
# Middleware: extract org context
class TenantMiddleware:
    async def __call__(self, request, call_next):
        org_id = extract_org_from_request(request)
        request.state.org_id = org_id
        return await call_next(request)

# Decorator: enforce permissions
@require_permission("agents:write")
async def create_agent(request, agent_data):
    # org_id automatically applied
    ...

# Permission evaluation
def check_permission(user_membership, resource, action):
    role_permissions = ROLE_PERMISSION_MAP[user_membership.role]
    return f"{resource}:{action}" in role_permissions
```

### 5.4 MCP tool management in multi-tenant context

**Challenges:**
- MCP server connections may expose tools that should be tenant-isolated
- Tool credentials (API keys for external services) must not leak across orgs
- Tool execution must run in org-scoped context

**Recommended approach:**
- Org-level MCP connection registry: each org configures its own MCP servers
- Tool credential vault: org-scoped secret storage for tool API keys
- Tool allowlist/blocklist: org admins can control which tools are available to members
- Tool execution logging: per-org audit trail for tool invocations

### 5.5 Agent sharing and governance

| Sharing model | Description | Use case |
|--------------|-------------|----------|
| Private | Agent visible only to creator | Development/testing |
| Workspace | Agent shared within workspace | Team collaboration |
| Organization | Agent available to all org members | Standard deployment |
| Published | Agent available across platform | Marketplace/template |

**Governance controls:**
- Agent approval workflow for org-level and published sharing
- Agent version history with diff and rollback
- Agent usage metrics (invocations, errors, latency) per org
- Agent archival without deletion (preserve audit history)

---

## 6. Prioritized implementation roadmap

### Phase 1: Foundation (weeks 1–4)

**Goal:** Establish agent entity model and basic management UI.

| Task | Gap ref | Effort |
|------|---------|--------|
| Create `Agent` database model with Alembic migration | G1 | M |
| Implement agent CRUD API endpoints | G3 | M |
| Build Agents page with All Agents tab | G7 | L |
| Build agent card component | G8 | S |
| Build Create Agent dialog | G3 | M |
| Build Edit Agent dialog | G3 | M |
| Add `/agents` route to frontend routing | G7 | S |

### Phase 2: Tool management (weeks 3–6)

**Goal:** Standalone tool discovery and testing experience.

| Task | Gap ref | Effort |
|------|---------|--------|
| Build Tool catalog page with search and cards | G6 | M |
| Build Tool details dialog | G6 | S |
| Build Tool playground with schema-driven forms | G5, G4 | L |
| Implement response viewer (Pretty + Raw) | G5 | M |
| Add `?tool=` URL state to playground | G9 | S |
| Add `/tools` and `/tools/playground` routes | G6 | S |

### Phase 3: Schema-driven forms and multi-tenancy (weeks 5–10)

**Goal:** Dynamic form generation and enterprise data isolation.

| Task | Gap ref | Effort |
|------|---------|--------|
| Build `SchemaForm` component with typed field dispatch | G4 | L |
| Integrate schema-driven forms into agent create/edit | G4 | M |
| Create `Organization` and `Membership` models | G2 | L |
| Implement tenant isolation middleware | G2 | M |
| Implement RBAC permission model | G10 | L |
| Add org management API endpoints | G2 | M |
| Add org switcher to frontend shell | G2 | M |

### Phase 4: Advanced features (weeks 9–14)

**Goal:** Templates view, RAG management, and polish.

| Task | Gap ref | Effort |
|------|---------|--------|
| Build Templates tab with deployment/graph grouping | G11 | M |
| Build RAG collection management page | G12 | L |
| Implement URL-driven state across pages | G9 | M |
| Standardize loading/empty/error patterns | G13 | M |
| Implement global provider architecture | G14 | M |
| Add agent sharing and governance controls | G2 | L |

**Effort key:** S = small (1–2 days), M = medium (3–5 days), L = large (1–2 weeks)

---

## 7. Implementation principles

These principles ensure the new features integrate smoothly with the existing Langflow architecture:

1. **Additive, not disruptive** — New pages and APIs are added alongside existing flow-centric experience. Flow editor and canvas remain unchanged.

2. **Schema-driven extensibility** — Agent config and tool execution forms render from backend metadata. No frontend changes needed when new tool types or agent config fields are added.

3. **Entity independence with composability** — Agents, tools, and RAG collections are independently manageable entities that can be composed into flows. This matches OAP's model while preserving Langflow's strength.

4. **Org-scoped by default** — All new entities include `org_id` from day one. Existing single-tenant behavior is preserved as a single implicit default org during migration.

5. **Modal-first CRUD** — Create/edit/delete operations use inline dialogs (not full-page mode switches) to preserve operator context. This matches OAP's pattern and keeps navigation lightweight.

6. **Progressive disclosure** — Complexity is hidden behind tabs, dialogs, and sidebars. Primary views show the most important information; details are revealed on demand.

7. **URL contract for entity state** — Selected agents, tools, filters, and tabs are reflected in URL query parameters for deep-linking and browser navigation correctness.

---

## 8. Relationship to existing LangGraph migration

This research document complements the existing [Python Backend LangGraph Deep-Dive](./python-backend-langgraph-deep-dive.md). Key interactions:

| This document proposes | LangGraph migration enables |
|----------------------|---------------------------|
| Agent entity model with deployment/graph targeting | LangGraph `StateGraph` provides the deployment and graph concepts that agents target |
| Tool playground with schema-driven execution | LangGraph tool nodes provide standardized execution and schema contracts |
| Agent versioning and lifecycle | LangGraph checkpointing provides state persistence and resumability |
| Multi-agent supervisor patterns | LangGraph subgraph composition supports hierarchical agent orchestration |

The agent management UX features described here are **backend-agnostic** — they work with both the current legacy orchestration engine and the planned LangGraph backend. The LangGraph migration strengthens the backend semantics that these UX features surface to operators.

---

## Appendix A: OAP UX pattern mapping

| OAP pattern | Recommended Langflow/NovaFlow implementation |
|------------|---------------------------------------------|
| Global shell provider stack | Extend existing Zustand stores; add `AgentStore` and `ToolCatalogStore`; use React context for org/auth scoping |
| Two-lens agent IA | Tabs component on `/agents` page — Templates (grouped accordion) + All Agents (searchable grid) |
| Tool discovery → inspect → test | `/tools` (catalog) → `ToolDetailsDialog` (inspect) → `/tools/playground?tool=x` (test) |
| Schema-rendered forms | `SchemaForm` component consuming JSON Schema; used in agent config, tool playground, and component editing |
| Query-param synchronization | React Router search params or `use-query-params` library for `agentId`, `tool`, `tab`, `search`, `graphFilter` |
| Skeleton + empty + toast feedback | Standardized `LoadingGrid`, `EmptyState`, and toast patterns extracted to shared components |
| Modal CRUD (context-preserving) | Dialog-based create/edit/delete with form state reset on open; no full-page navigation |

## Appendix B: File location recommendations

All new code should follow existing Langflow conventions:

| Layer | Convention | Example |
|-------|-----------|---------|
| Backend model | `services/database/models/<entity>/model.py` | `models/agent/model.py` |
| Backend API | `api/v1/<entity>.py` | `api/v1/agents.py` |
| Frontend page | `pages/<entity>/index.tsx` | `pages/agents/index.tsx` |
| Frontend store | `stores/<entity>Store.ts` | `stores/agentStore.ts` |
| Frontend API hook | `api/<entity>/index.ts` | `api/agents/index.ts` |
| Shared component | `components/<component-name>/index.tsx` | `components/schema-form/index.tsx` |
