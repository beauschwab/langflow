# Enterprise first-pass component reduction plan

## Objective
Define a low-risk first pass for enterprise deployments that keeps Langflow orchestration and generalized data-access capabilities, while excluding most third-party/vendor-specific component bundles.

## Repository locations reviewed
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/components/`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/settings/base.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/main.py`
- `/home/runner/work/langflow/langflow/src/backend/base/pyproject.toml`
- `/home/runner/work/langflow/langflow/src/frontend/src/utils/styleUtils.ts`
- `/home/runner/work/langflow/langflow/src/frontend/src/pages/FlowPage/components/flowSidebarComponent/index.tsx`
- `/home/runner/work/langflow/langflow/src/frontend/package.json`

## First-pass scope decision

### Include (first pass)
1. **Core orchestration/runtime**
   - Graph execution and orchestration paths (`langflow.graph.*`, `run_graph_internal(...)`, startup/service wiring).
2. **Core component categories (non-vendor-specific)**
   - `inputs`, `outputs`, `prompts`, `processing`, `logic`, `helpers`, `data`, `documentloaders`, `textsplitters`, `output_parsers`.
3. **Enterprise data access (generalized)**
   - Keep neutral/internal data components and enterprise connectors needed for initial rollout (for example `sharepoint`, `confluence`, and `datahub` where applicable).

### Exclude at first pass
Treat all current sidebar bundle providers as out-of-scope unless explicitly approved for the enterprise environment:
- `gmail`
- `apify`
- `langchain_utilities`
- `agentql`
- `assemblyai`
- `astra_assistants`
- `olivya`
- `langwatch`
- `notion`
- `needle`
- `nvidia`
- `vectara`
- `icosacomputing`
- `google`
- `crewai`
- `notdiamond`
- `composio`
- `cohere`
- `firecrawl`
- `unstructured`
- `git`
- `mem0`
- `youtube`
- `scrapegraph`

> Note: `sharepoint` can remain in-scope for enterprise data access if required by rollout policy.

## Action plan
1. **Create explicit allowlist policy**
   - Add a backend allowlist setting for component directories/types (instead of loading all directories under `BASE_COMPONENTS_PATH`).
   - Add a frontend allowlist for sidebar bundles so disallowed providers are not rendered.
2. **Backend pruning pass**
   - Remove excluded provider directories under `/src/backend/base/langflow/components/` from the enterprise distribution path.
   - Ensure startup no longer loads excluded bundles from URL bundle loading.
3. **Python dependency pruning**
   - Audit `/src/backend/base/pyproject.toml` and remove package requirements that were only needed by excluded bundles.
   - Re-lock dependencies after removal.
4. **Frontend dedicated component pruning**
   - Remove excluded entries from `SIDEBAR_BUNDLES` and related UI references.
   - Remove icon/component imports that become unused after bundle removal.
5. **Import and dead-code cleanup**
   - Remove orphaned Python imports in excluded component modules and any top-level registries/tests referencing them.
   - Remove orphaned frontend imports, icon mappings, and bundle selectors.
6. **Validation**
   - Run backend lint/tests for component loading and flow execution paths.
   - Run frontend type/build checks to confirm no unresolved imports from removed bundles.

## Implementation notes for smallest-risk rollout
- Introduce changes behind an enterprise feature flag first.
- Keep the current default behavior as fallback until enterprise mode validation is complete.
- Remove physical files/dependencies only after the allowlist mode is validated end-to-end.
