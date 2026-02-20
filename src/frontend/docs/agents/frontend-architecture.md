# Frontend Architecture and Project Structure

## 1) Frontend app boundary

- Frontend root: `src/frontend`
- Source root: `src/frontend/src`
- App entrypoint: `src/frontend/src/index.tsx`
- Top-level app shell: `src/frontend/src/App.tsx`
- Router definition: `src/frontend/src/routes.tsx`
- Context composition: `src/frontend/src/contexts/index.tsx`

## 2) Runtime composition

`index.tsx` mounts React and global styles, then renders `App`.

`App.tsx`:
- Applies dark mode class from Zustand dark store.
- Uses `RouterProvider` and lazy route loading fallback (`LoadingPage`).

`ContextWrapper` composes global providers in this order:
1. `CustomWrapper`
2. `GradientWrapper`
3. `QueryClientProvider` (TanStack Query)
4. `AuthProvider`
5. `TooltipProvider`
6. `ReactFlowProvider`
7. `ApiInterceptor` (auth header injection + request/response interception)

## 3) Route map (high level)

From `routes.tsx`:

- Public playground route: `/playground/:id/`
- Main app route tree (optionally custom-prefixed):
  - Dashboard collection pages:
    - `/flows`, `/components`, `/all`, plus folder variants
    - optional `/files` page (feature flag)
  - Settings:
    - `/settings/general`, `/settings/global-variables`, `/settings/api-keys`, `/settings/shortcuts`, `/settings/messages`, `/settings/store`
  - Store pages: `/store`, `/store/:id/`
  - Admin pages: `/admin`, `/login/admin`
  - Flow editor: `/flow/:id/`
  - Flow view mode: `/flow/:id/view`
  - Auth routes: `/login`, `/signup`

Guard layers:
- `ProtectedRoute`
- `ProtectedAdminRoute`
- `ProtectedLoginRoute`
- `AuthSettingsGuard`
- `StoreGuard`

## 4) Source directory structure (functional)

- `src/components`
  - Reusable UI, app-shell, rendering primitives, and feature components.
- `src/pages`
  - Route-level pages and page-local composition.
- `src/modals`
  - Modal workflows, especially the I/O and API generation workflows.
- `src/CustomNodes`
  - ReactFlow node implementations (`GenericNode`, `NoteNode`) and related hooks/helpers.
- `src/controllers/API`
  - API client, interceptors, endpoint constants, and TanStack query/mutation hooks.
- `src/stores`
  - Zustand stores for global and feature state.
- `src/hooks`
  - Shared hooks and flow management hooks.
- `src/customization`
  - Feature flags, customization wrappers, and override points.
- `src/utils`
  - Build orchestration helpers, flow utilities, formatting, and common helper logic.

## 5) Core execution path from UI to backend

### Flow execution / build path

1. Flow UI triggers build via `useFlowStore().buildFlow(...)`.
2. `buildFlow` delegates to `buildFlowVerticesWithFallback` (`src/utils/buildUtils.ts`).
3. Build starts via `POST /api/v1/build/{flowId}/flow` (or `build_public_tmp` for playground-public flow mode).
4. Frontend consumes build events via:
   - streaming event endpoint `GET /api/v1/build/{job_id}/events`
   - or polling fallback `GET .../events?stream=false`
5. Cancel endpoint called on abort: `POST /api/v1/build/{job_id}/cancel`.
6. Build events update node/edge statuses and flow pool data in `flowStore`.

### Playground/chat path

1. `PlaygroundPage` loads public flow data.
2. `IOModal` renders chat and non-chat I/O panels.
3. `sendMessage` calls `buildFlow(...)` with `startNodeId` of `ChatInput` and session id.
4. Messages are fetched/updated through `/monitor/messages` endpoints via query hooks and message store.

### API code generation path

`modals/apiModal` generates snippets (curl/python/js) for:
- `POST /api/v1/run/{flow_id_or_endpoint}?stream=false`
- `POST /api/v1/webhook/{flow_id_or_endpoint}`

