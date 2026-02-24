# src/frontend — Langflow Frontend

## Purpose
React-based single-page application (SPA) that provides the visual flow editor, chat playground, and management UI for Langflow. Built with Vite, React, TypeScript, Tailwind CSS, and React Flow (xyflow). Communicates with the Python backend exclusively through REST APIs and Socket.IO WebSockets.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `src/` | Application source code — components, pages, stores, hooks, utilities, and assets. |
| `tests/` | End-to-end and integration tests using Playwright. |
| `docs/` | Frontend-specific documentation. |
| `public/` | Static assets served directly (favicon, etc.). |

## Key Files

| File | Role |
|------|------|
| `package.json` | Dependencies and scripts (`npm run dev`, `npm run build`, `npm run test`). |
| `vite.config.mts` | Vite build configuration with proxy settings for the backend API. |
| `tsconfig.json` | TypeScript configuration. |
| `tailwind.config.mjs` | Tailwind CSS theme and plugin configuration. |
| `playwright.config.ts` | Playwright E2E test configuration. |
| `index.html` | HTML entry point — mounts the React app. |
| `.eslintrc.json` | ESLint configuration. |
| `.prettierrc.mjs` | Prettier code formatting rules. |
| `postcss.config.js` | PostCSS configuration for Tailwind. |

## Tech Stack

- **React 18** with TypeScript
- **React Flow (xyflow)** for the node-based flow editor canvas
- **Zustand** for state management (stores/)
- **React Query (TanStack Query)** for API data fetching (controllers/API/)
- **Tailwind CSS** + **shadcn/ui** for styling and UI primitives
- **Socket.IO** for real-time streaming events
- **Vite** for development server and production builds
- **Playwright** for E2E testing

## For LLM Coding Agents

- Pages are in `src/pages/` — each top-level route has its own page component.
- Reusable components are in `src/components/` (common, core, ui categories).
- API calls go through `src/controllers/API/` using React Query.
- Global state lives in Zustand stores under `src/stores/`.
- Flow editor canvas logic is in `src/pages/FlowPage/` and `src/CustomNodes/`.
