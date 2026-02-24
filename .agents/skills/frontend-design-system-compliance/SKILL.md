---
name: frontend-design-system-compliance
description: Enforce Langflow frontend design system compliance using semantic tokens, shared UI primitives, and accessibility-safe Radix patterns.
version: 1.0.0
category: frontend
author: Langflow Copilot
license: MIT
tags: [frontend, design-system, tokens, radix, tailwind]
---

# Frontend design system compliance skill

Use this skill when:

- Creating or updating frontend UI in `src/frontend/src`
- Adding component variants or visual styles
- Reviewing PRs for design consistency and token usage

## Do not use this skill when

- Task is backend-only and does not touch frontend styling or components
- Task is non-UI documentation-only

## Required compliance rules

1. **Use semantic tokens**

   - Prefer `bg-background`, `text-foreground`, `border-input`, `bg-primary`, etc.
   - Do not introduce hardcoded hex/rgb colors if an existing token already exists.

2. **Use shared primitives first**

   - Prefer `src/components/ui/*` components before creating one-off styled controls.
   - Extend existing CVA variants for reusable style changes.

3. **Preserve accessibility behavior**

   - Keep Radix interaction semantics intact (focus, keyboard, aria structure).
   - Ensure `focus-visible` behavior remains clear on interactive controls.

4. **Keep theme parity**
   - Any new semantic token usage must behave correctly in both light and dark modes.

## Workflow

1. Read the design specification:
   - `src/frontend/docs/agents/design-system-spec.md`
2. Verify token availability:
   - `src/frontend/src/style/index.css`
   - `src/frontend/tailwind.config.mjs`
3. Implement using existing `src/components/ui` primitives where possible.
4. Validate with existing frontend checks (at minimum build; formatting check where practical).

## PR review checklist

- [ ] No unnecessary hardcoded colors
- [ ] Uses semantic token classes
- [ ] Reuses or extends shared `ui` primitive components
- [ ] Preserves accessible keyboard/focus behavior
- [ ] Works in dark mode
