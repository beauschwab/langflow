# Langflow to Neva flow: remaining implementation plan

## Objective
Define a **step-by-step execution plan** for completing the project rename from Langflow/Lang flow to **Neva flow** across source code, folders, components, docs, and agent markdown content, without implementing the rename in this change.

## Repository locations reviewed
- `/home/runner/work/langflow/langflow/pyproject.toml`
- `/home/runner/work/langflow/langflow/Makefile`
- `/home/runner/work/langflow/langflow/README.md`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/`
- `/home/runner/work/langflow/langflow/src/backend/langflow/`
- `/home/runner/work/langflow/langflow/src/frontend/`
- `/home/runner/work/langflow/langflow/docs/`
- `/home/runner/work/langflow/langflow/.agents/`
- `/home/runner/work/langflow/langflow/scripts/`

## Current-state snapshot (remaining rename surface)
- `Langflow/langflow/LANGFLOW` references exist in **918 files** across the repository.
- Approximate distribution from scan:
  - `src/backend/base`: 461 files
  - `src/backend/tests`: 178 files
  - `src/frontend`: 106 files
  - `docs`: 92 files
  - `scripts`: 23 files
  - `.github`: 16 files
  - `docker`/`docker_example`: 16 files
  - `.agents`: 6 files
- File/folder names still containing `langflow` include:
  - Backend package folders: `src/backend/base/langflow`, `src/backend/langflow`
  - Skill folder: `.agents/skills/langflow-io-cli`
  - Docs pages: `docs/docs/Get-Started/welcome-to-langflow.md`, Google integration pages, support pages
  - Static assets: `docs/static/img/langflow-*`, `docs/static/videos/langflow_*`
  - Scripts: `scripts/gcp/deploy_langflow_gcp.sh`, `scripts/gcp/deploy_langflow_gcp_spot.sh`
  - Frontend assets/tests: `src/frontend/src/assets/LangflowLogo*.svg`, `langflowShortcuts.spec.ts`, `add-flow-to-test-on-empty-langflow.ts`

## Naming target and compatibility rules (decide first)
1. **Canonical product name** in UI/docs/marketing copy: `Neva flow`.
2. **Canonical technical identifier** for package/module/CLI/file slugs: pick one and apply consistently:
   - Recommended: `nevaflow` (single token).
3. **Compatibility policy** (required before edits):
   - Keep `langflow` imports/CLI aliases temporarily (deprecation window), or
   - Hard cut-over with migration guide and breaking-change release.
4. **Case mapping rules** to standardize replacements:
   - `Langflow` -> `Neva flow` (UI/docs text) or `Nevaflow` (class/type names)
   - `langflow` -> `nevaflow` (module names, env vars only if intentionally renamed)
   - `LANGFLOW_*` -> either retain for compatibility, or rename to `NEVAFLOW_*` with alias support

## Step-by-step implementation plan

### Phase 0: freeze scope and prepare automation
1. Create a dedicated rename branch and announce freeze on concurrent broad refactors.
2. Generate a baseline inventory:
   - Content references: `rg -n "Langflow|langflow|LANGFLOW"`.
   - Path/name references: `find . -name '*langflow*' -o -name '*Langflow*'`.
3. Split findings into four tracked worklists:
   - Paths/folders to rename.
   - Import/module/package identifiers.
   - User-facing copy (docs/UI/errors/tooltips).
   - Operational identifiers (env vars, Docker image names, CI names, release names).
4. Define release strategy for breaking changes (major/minor) and migration timeline.

### Phase 1: package and folder rename (high-risk, do first)
1. Rename backend Python package directories:
   - `src/backend/base/langflow` -> `src/backend/base/nevaflow` (or chosen canonical token)
   - `src/backend/langflow` -> `src/backend/nevaflow`
2. Update all Python imports and module references throughout backend/tests/scripts.
3. Add compatibility package shims:
   - `langflow` package re-exporting from `nevaflow` during deprecation period.
4. Update entrypoints and script declarations in:
   - `pyproject.toml`
   - any package-level `__main__`/version modules.
5. Validate editable/dev installs and import discovery.

### Phase 2: CLI, env vars, and API-facing naming
1. CLI command strategy:
   - Add `nevaflow` command as canonical executable.
   - Keep `langflow` alias initially (with deprecation message).
2. Environment variables:
   - Decide whether to keep `LANGFLOW_*` as canonical compatibility layer.
   - If introducing `NEVAFLOW_*`, support dual-read + precedence + warnings.
3. API metadata and OpenAPI text:
   - App title/description, examples, and generated docs naming.
4. Update backend/frontend code snippets generated in UI modals (curl/python/js snippets).

### Phase 3: component and flow metadata rename
1. Scan component definitions for:
   - `display_name`, `description`, docstrings, examples, telemetry labels.
2. Rename any component titles or copy that still mention Langflow.
3. Update starter project JSON flow metadata and any embedded prompts/messages referencing old name.
4. Ensure generated component schemas and frontend node metadata remain stable.
5. Add targeted tests for renamed component copy where snapshots/assertions depend on branding text.

### Phase 4: frontend product rename
1. Rename frontend branding assets and references:
   - `LangflowLogo*.svg` and import usage.
2. Replace in-app strings:
   - headers, settings pages, auth screens, error boundaries, help links, share modal text.
3. Rename frontend test files and fixtures containing `langflow` in filename/content where appropriate.
4. Update Playwright/Cypress config names, project titles, and artifact naming strings.
5. Verify UI smoke flow and take updated screenshots for release docs.

### Phase 5: documentation and site rename
1. Update docs site identity:
   - Docusaurus config title/tagline/footer/social metadata.
2. Rename docs page filenames/slugs containing `langflow` and add redirects for old URLs.
3. Update all markdown content in:
   - `docs/docs/**`
   - `docs/research/**`
   - top-level `README.md`, `CONTRIBUTING.md`, `DEVELOPMENT.md`.
4. Rename static assets with `langflow` prefixes and update links/references.
5. Regenerate `docs/openapi.json` if branding appears in generated artifacts.

### Phase 6: agent markdown and skill assets (explicit requirement)
1. Rename skill path and metadata:
   - `.agents/skills/langflow-io-cli` -> `.agents/skills/nevaflow-io-cli` (or chosen token).
2. Update `SKILL.md` frontmatter fields (`name`, `description`, tags) and all command examples.
3. Update cross-skill references mentioning Langflow in:
   - `phoenix-tracing` skill docs and references.
4. Update sample files under skill `references/` that include old CLI commands.
5. Validate skill discovery still works with renamed skill identifiers.

### Phase 7: CI/CD, infra, and packaging artifacts
1. Update workflow names, job labels, and filters containing `langflow`.
2. Update Docker image tags and build args still hardcoded to `langflow`.
3. Update deployment scripts and docs:
   - GCP scripts (`deploy_langflow_gcp*.sh`)
   - AWS docs/images naming where practical.
4. Update package indexes/docs URLs and release automation metadata.
5. Validate nightly/release pipelines with both old and new command aliases during transition.

### Phase 8: tests, migration tooling, and rollout controls
1. Bulk-fix tests that assert old naming text or import paths.
2. Add migration tests:
   - old import path still resolves (if shim policy enabled),
   - old CLI command still works with warning.
3. Add static checks to prevent reintroduction of `Langflow/langflow` except approved compatibility allowlist.
4. Produce migration guide:
   - import changes, CLI changes, env var changes, redirects, deprecation schedule.
5. Execute staged rollout:
   - internal dogfood -> prerelease -> general release.

## Verification checklist (for the future implementation PRs)
- [ ] `rg -n "Langflow|langflow|LANGFLOW"` returns only approved compatibility cases.
- [ ] No remaining `*langflow*` file/folder names except intentional compatibility layers.
- [ ] Backend imports/tests pass with canonical `nevaflow` paths.
- [ ] Frontend build/tests pass with updated branding assets and strings.
- [ ] Docs build passes with redirects for renamed pages.
- [ ] Agent skills validation passes for renamed skill identifiers and references.
- [ ] CI release artifacts publish under new naming.

## Recommended execution order (minimal-risk sequence)
1. Phase 0 (scope + policy)  
2. Phase 1 (package/folder rename + shims)  
3. Phase 2 (CLI/env/API naming)  
4. Phase 3 (components/starter flows)  
5. Phase 4 + 5 + 6 in parallel by owners (frontend/docs/agent skills)  
6. Phase 7 (CI/CD packaging)  
7. Phase 8 (tests + rollout gates)
