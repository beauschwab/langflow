# Skills implementation research report

## Objective
Document the current state of repository skills, identify implementation patterns, and provide a practical rollout approach for adding new skills consistently.

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

## Observed implementation conventions
1. **Single responsibility per skill**: each skill focuses on one technical domain.
2. **Explicit trigger guidance**: descriptions include concrete phrases that should trigger invocation.
3. **Operational guardrails**: skills include what to do and what to avoid.
4. **Composable structure**: skills can be used together without coupling folder layouts.

## Gaps and risks
- Trigger language is not fully standardized across all skills, which can reduce invocation consistency.
- Depth of examples varies across skills, increasing onboarding variability.
- Validation criteria (how to verify a skill was correctly applied) is not always explicit.

## Recommendations
1. Define a lightweight skill authoring template for `SKILL.md` sections.
2. Require a minimum trigger phrase set and one “non-trigger” example.
3. Add a short validation checklist section to every skill.
4. Keep optional reference artifacts for complex skills, but standardize naming and placement.

## Suggested implementation plan
1. Publish and adopt a common skill template.
2. Normalize existing skills to the template in small batches.
3. Add a review checklist to ensure new skills include triggers, guardrails, and validation.
4. Periodically audit skill usage outcomes and refine trigger wording.
