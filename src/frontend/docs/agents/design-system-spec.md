# Frontend design system specification

## Scope

This specification defines the current frontend design system in `src/frontend`, based on implemented tokens and reusable UI primitives.

## Source of truth

- Theme and token declarations: `src/frontend/src/style/index.css`
- Tailwind token bindings and scales: `src/frontend/tailwind.config.mjs`
- Reusable Radix/CVA primitives: `src/frontend/src/components/ui`

## Design principles

1. **Semantic tokens first**: use semantic classes (`bg-background`, `text-foreground`, `border-input`) instead of raw color literals.
2. **Theme parity**: all semantic tokens must work in both `:root` and `.dark`.
3. **Composable primitives**: prefer `src/components/ui/*` primitives (Radix + CVA) before custom one-off styles.
4. **Accessibility baseline**: retain Radix keyboard/focus behavior and preserve visible focus/contrast states.

## Token model

### 1) Typography tokens

Defined in `:root`:

- `--font-sans` (`Inter`)
- `--font-mono` (`JetBrains Mono`)
- `--font-chivo` (`Chivo`)

Tailwind bindings:

- `font-sans` -> `var(--font-sans)`
- `font-mono` -> `var(--font-mono)`
- `font-chivo` -> `var(--font-chivo)`

### 2) Radius and border tokens

- `--radius` (base radius)
- Tailwind radius scale:
  - `rounded-lg` -> `var(--radius)`
  - `rounded-md` -> `calc(var(--radius) - 2px)`
  - `rounded-sm` -> `calc(var(--radius) - 4px)`
- Custom border widths: `1.5` and `1.75`

### 3) Core semantic color tokens

Core app semantics (light/dark aware):

- Surface/text: `background`, `foreground`, `card`, `card-foreground`, `popover`, `popover-foreground`
- Inputs/chrome: `border`, `input`, `ring`, `muted`, `muted-foreground`
- Actions: `primary`, `primary-foreground`, `primary-hover`, `secondary`, `secondary-foreground`, `secondary-hover`
- Feedback: `destructive`, `destructive-foreground`, `warning`, `warning-foreground`, `warning-text`

### 4) Accent and status tokens

- Accent families: `accent-emerald`, `accent-indigo`, `accent-pink`, `accent-amber`
- Status colors: `status-blue`, `status-green`, `status-red`, `status-yellow`, `status-gray`
- Utility/status families:
  - `error.background` / `error.foreground`
  - `success-background` / `success-foreground`
  - `info-background` / `info-foreground`

### 5) Domain-specific token groups

- Canvas/node: `canvas`, `canvas.dot`, `node-selected`, `node-ring`, `connection`
- Data type badges: `datatype-{yellow|blue|gray|lime|red|violet|emerald|fuchsia|purple|cyan|indigo|orange}` and foreground pairs
- Chat/tooling: `chat-send`, `chat-trigger`, `chat-trigger-disabled`, `build-trigger`
- Specialized visual sets (used by feature UIs): neon/cosmic tokens (`neon-fuschia`, `digital-orchid`, `plasma-purple`, etc.)

### 6) Motion tokens

Tailwind keyframes/animations:

- `wiggle` / `slow-wiggle`
- `border-beam` (`calc(var(--duration)*1s)`)

## Component standards

### Primitive layer

`src/components/ui/*` is the baseline layer for reusable UI:

- Radix primitives for behavior/accessibility
- Tailwind utilities for appearance
- `class-variance-authority` for variants (e.g., `Button`)

### Variant conventions

- Define visual variants with CVA (`variant`, `size`) instead of per-call class duplication.
- Keep tokens semantic inside variants (e.g., `bg-primary`, `text-primary-foreground`) rather than hardcoded hex.

## Compliance checklist

Use this checklist for UI PRs:

- [ ] No new hardcoded color literals when an existing token can be used.
- [ ] New components prefer `src/components/ui/*` or extend an existing primitive.
- [ ] New variant styles are added through CVA where applicable.
- [ ] Dark mode behavior verified for any new semantic token usage.
- [ ] Focus-visible and keyboard interactions preserved for Radix-based controls.

## Implementation notes for contributors and agents

1. If a token is missing, add it to `index.css` first, then bind it in `tailwind.config.mjs`.
2. If a pattern repeats across screens, promote it into `src/components/ui`.
3. Keep token names semantic (`status-*`, `accent-*`, `datatype-*`) rather than context-specific screen names.
