# Frameworks, Tooling, and Implementation Patterns

## 1) Frameworks and libraries used

## Core
- React 18 (`react`, `react-dom`)
- TypeScript 5
- Vite 5 build tooling (`vite`, `@vitejs/plugin-react-swc`)

## Routing
- `react-router-dom` v6 with nested route trees and route guards

## State & data
- Zustand (`src/stores/*`) for app/global state
- TanStack Query (`@tanstack/react-query`) for query/mutation orchestration
- Axios (`controllers/API/api.tsx`) for HTTP requests + interceptors

## Flow canvas / graph UI
- ReactFlow / XYFlow (`@xyflow/react`)
- Custom node implementations in `src/CustomNodes`

## Forms & validation
- `react-hook-form`
- `zod`
- `@hookform/resolvers`

## Styling/UI
- Tailwind CSS
- Radix UI primitives
- Custom UI primitives in `src/components/ui`
- Framer Motion for animation

## Content rendering / editors
- `react-markdown`, `remark-gfm`, `rehype-*`
- `react-ace` / ace editor
- AG Grid for table/grid display

## Testing/automation in frontend package
- Playwright dependencies/config present (`playwright.config.ts`)

## 2) Patterns used in this frontend

## a) Query/mutation abstraction pattern

`UseRequestProcessor` wraps TanStack query/mutation defaults:
- shared retry/backoff defaults
- common invalidation behavior for mutations

This yields per-domain hooks under `controllers/API/queries/*`.

## b) URL constant + URL builder pattern

`controllers/API/helpers/constants.ts` defines URL key registry and `getURL(key, params, v2)` helper.

Benefits:
- Avoids hard-coded endpoint duplication
- Allows central version switching (`BASE_URL_API` vs `BASE_URL_API_V2`)

## c) Interceptor-centered authentication pattern

`ApiInterceptor`:
- Injects bearer token into requests
- Adds custom headers
- Handles auth refresh/retry and logout flows
- Performs duplicate request cancellation logic

## d) Store-per-domain pattern (Zustand)

State is segmented by concern:
- auth/session (`authStore`)
- flow graph runtime (`flowStore`)
- flow list/metadata (`flowsManagerStore`)
- alerts, messages, utility, theme, shortcuts, etc.

## e) Canvas interaction pattern (ReactFlow + store reducers)

`flowStore` encapsulates:
- node/edge mutation APIs
- build status transitions
- copy/paste/group/delete behavior
- edge animation/status class updates during execution

## f) Feature-flag-driven UI pattern

`src/customization/feature-flags` controls behavior such as:
- file management visibility
- publish/playground-specific toggles

## g) Modal-first advanced workflows

Complex actions run via dedicated modal surfaces:
- I/O testing (`IOModal`)
- API generation (`apiModal`)
- flow settings/logs/share/export

## h) Public flow playground isolation pattern

Playground flow session keying uses deterministic UUID strategy (client + flow) for public sessions.

