# src/frontend/src/ — Application Source Code

## Purpose
Root of all frontend application source code. Contains the React component tree, state management, API controllers, routing, and styling.

## Folder Structure

| Folder | Description |
|--------|-------------|
| `CustomEdges/` | Custom React Flow edge components for the flow canvas. |
| `CustomNodes/` | Custom React Flow node components — GenericNode (main component node) and NoteNode. |
| `alerts/` | Alert/notification system — toast messages, error alerts, success notices. |
| `assets/` | Static assets (images, fonts) bundled by Vite. |
| `boilerplate/` | Boilerplate templates for creating new components. |
| `components/` | Reusable UI components — organized into authorization, common, core, and ui categories. |
| `constants/` | Application constants and enums. |
| `contexts/` | React context providers (auth context). |
| `controllers/` | API layer — React Query hooks and service functions for all backend endpoints. |
| `customization/` | Feature flags, config constants, and customization hooks for white-labeling. |
| `helpers/` | Helper/utility functions. |
| `hooks/` | Shared React hooks. |
| `icons/` | Custom SVG icon components for third-party service logos (100+ icons). |
| `modals/` | Modal dialog components — IO/chat, code editor, API modal, flow settings, templates, etc. |
| `pages/` | Top-level page components — FlowPage, MainPage, LoginPage, SettingsPage, etc. |
| `shared/` | Shared components and hooks used across features. |
| `stores/` | Zustand state stores — flow, auth, alerts, types, folders, messages, etc. |
| `style/` | Global CSS styles and Tailwind configuration. |
| `types/` | TypeScript type definitions for the entire application. |
| `utils/` | Utility functions — React Flow helpers, style utilities, build utilities. |

## Key Files (at this level)

| File | Role |
|------|------|
| `App.tsx` | Root React component — sets up routing via `RouterProvider` and dark mode. |
| `index.tsx` | Application entry point — renders `App` into the DOM. |
| `routes.tsx` | React Router route definitions — maps URL paths to page components. |
| `flow_constants.tsx` | Flow editor constants. |

## For LLM Coding Agents

- **Adding a new page**: Create a folder in `pages/`, add a route in `routes.tsx`.
- **Adding a new component**: Place it in `components/common/` (reusable) or `components/core/` (feature-specific).
- **Adding API calls**: Create query hooks in `controllers/API/queries/`.
- **Adding global state**: Create or extend a Zustand store in `stores/`.
