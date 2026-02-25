# Skills implementation research report

## Objective
Map the skills concept to the Langflow UI and the agent manager framework so users have a low-code path for bundling domain context and tool access, including a sub-flow authoring option and UX trade-offs.

## Repository locations reviewed
- `.agents/skills/`
- `.agents/skills/find-skills/SKILL.md`
- `.agents/skills/playwright-skill/SKILL.md`
- `.agents/skills/pydantic/SKILL.md`

## Current state summary
- Skills are implemented as folder-scoped assets under `.agents/skills/<skill-name>/`.
- Each skill is documented with a `SKILL.md` file that defines:
  - purpose and trigger conditions,
  - boundaries/scope,
  - usage patterns and expected outcomes.
- Some skills include additional artifacts (for example, reference docs) when the skill requires richer operational guidance.

## Mapping skills to the UI and agent manager framework
- **Terminology**: use **Skills bundle** as the user-facing term (instead of "hybrid skill") for a package that combines selected skills with an optional sub-flow link.
- **Skill package**: reusable bundle that combines:
  - context assets (domain knowledge, prompt constraints, reference snippets),
  - tool access policy (allowed components/tools),
  - optional execution logic (sub-flow behavior).
- **Agent manager role**: attach one or more skill packages to an agent profile so the profile controls both what the agent knows and what it can call.
- **Flow editor role**: expose skill composition as low-code blocks (configure context + tool scope + optional sub-flow binding) instead of requiring direct markdown editing.

## Low-code implementation approaches in UX
### Approach A: Skill-first panel in Agent Manager
- **Experience**: users pick skills from a catalog, then bind them to an agent profile.
- **Pros**
  - fastest onboarding; simple mental model for non-technical users.
  - central governance point for permissions and approved knowledge packs.
  - easy to version and audit skills per agent profile.
- **Cons**
  - less flexible for advanced orchestration.
  - limited visibility into internal skill execution steps from the flow canvas.

### Approach B: Sub-flow authoring in Flow Editor (skill as flow template)
- **Experience**: users author a sub-flow that encapsulates context loading + tool calls, then publish it as a skill-like artifact.
- **Pros**
  - strongest low-code expressiveness for complex domain workflows.
  - native visual debugging and iteration in the existing flow editor UX.
  - natural reuse via sub-flow publishing/versioning.
- **Cons**
  - higher UX complexity for first-time users.
  - requires stronger guardrails to prevent unsafe tool exposure.
  - version compatibility concerns when sub-flow contracts change.

### Approach C: Hybrid model (recommended)
- **Experience**: users consume curated skills in Agent Manager, while advanced users can create/edit skill internals as sub-flows in Flow Editor.
- **Pros**
  - supports both beginner and power-user paths.
  - keeps governance centralized while preserving extensibility.
  - enables progressive disclosure (simple defaults, advanced editing when needed).
- **Cons**
  - requires clear ownership boundaries between skill catalog and flow authorship.
  - needs consistent metadata contracts across manager and editor surfaces.

## Observed implementation conventions
1. **Single responsibility per skill**: each skill focuses on one technical domain.
2. **Explicit trigger guidance**: descriptions include concrete phrases that should trigger invocation.
3. **Operational guardrails**: skills include what to do and what to avoid.
4. **Composable structure**: skills can be used together without coupling folder layouts.

## Gaps and risks for UI integration
- Trigger language is not fully standardized across skills, reducing predictability of when a skill is selected/applied (for example, one skill may trigger on "add animation" while another uses broader phrasing like "improve UX").
- Validation criteria (how to verify context/tool bundles were correctly attached) is not always explicit in existing skill docs.
- Sub-flow-as-skill introduces drift risk if flow I/O contracts are not versioned and enforced.

## Recommendations
1. Introduce a shared skill metadata schema used by both Agent Manager UI and Flow Editor sub-flow publishing.
2. Require explicit fields for bundled context sources, allowed tools, and invocation triggers.
3. Add a validation checklist in each skill definition to confirm policy, context source, and tool-binding integrity.
4. Start with a curated catalog in Agent Manager, then add sub-flow authoring behind an advanced toggle.

## Suggested implementation plan
1. Define and adopt a common skill metadata/template contract.
2. Deliver Agent Manager skill catalog UX first (attach/detach, inspect bundled context and tool access).
3. Add Flow Editor sub-flow publishing as an advanced path that outputs the shared metadata contract from step 1.
4. Add versioning + compatibility checks for sub-flow-based skills before broad rollout.

## Further research implications
1. **Governance model**: define ownership boundaries between platform owners (skill schema/policies) and domain teams (skill content/sub-flow logic).
2. **Discovery and ranking**: determine how the Agent Manager should recommend skills (manual selection only vs assisted suggestion from user intent).
3. **Evaluation framework**: define success metrics for hybrid adoption (attach rate, task completion time, fallback-to-manual-edit rate).
4. **Compatibility lifecycle**: establish versioning/deprecation policy for skill contracts and sub-flow interfaces.
5. **Trust and safety**: classify tool-risk tiers and map each tier to review/approval flows before skills are publishable in shared catalogs.

## Hybrid approach implementation (concrete)
### Phase 1: Agent Manager MVP (curated skills)
- Add a **Skills** section in Agent Manager where users can:
  - browse approved skills,
  - inspect bundled context and allowed tools,
  - attach/detach skills per agent profile.
- Persist attached skill metadata with stable identifiers and explicit versions.
- Enforce permission checks so only allowed tools in attached skills are exposed at runtime.

### Phase 2: Flow Editor advanced path (sub-flow-backed skills)
- Add **Publish as Skill** action for eligible sub-flows in Flow Editor.
- Require sub-flow input/output contract declaration before publishing.
- Validate published artifacts against the same shared skill metadata contract from the MVP.
- Route published artifacts into the same Agent Manager catalog with an `advanced` indicator.

### Phase 3: Runtime and operations
- Resolve skill attachments at run time as:
  - context bundle (prompt/domain memory injection),
  - tool access filter (allowlist enforcement),
  - optional sub-flow invocation hook.
- Log skill usage per run for observability, governance audits, and relevance tuning.
- Add rollback controls: disable a skill version without deleting historical run traces.
