# Backend API Inventory Called by Frontend

This inventory consolidates backend API usage across `src/frontend/src/controllers/API`, `src/frontend/src/utils/buildUtils.ts`, I/O/playground modules, and API snippet generation modules.

## 1) Base API roots

- `BASE_URL_API` (default `/api/v1/`)
- `BASE_URL_API_V2` (default `/api/v2/`)

## 2) Route key registry used by query hooks

From `controllers/API/helpers/constants.ts`:

- `monitor/transactions`
- `api_key`
- `files`
- `version`
- `monitor/messages`
- `monitor/builds`
- `store`
- `users`
- `logout`
- `login`
- `auto_login`
- `refresh`
- `build`
- `custom_component`
- `flows`
- `folders`
- `variables`
- `validate`
- `config`
- `starter-projects`
- `sidebar_categories`
- `all`
- `voice`
- `/flows/public_flow`
- `agents`

## 3) Endpoint inventory by domain

## Agents
- `POST /api/v1/agents/` — Create agent
- `GET /api/v1/agents/` — List agents (supports `search`, `agent_type` query params)
- `GET /api/v1/agents/{agent_id}` — Get agent by ID
- `PATCH /api/v1/agents/{agent_id}` — Update agent
- `DELETE /api/v1/agents/{agent_id}` — Delete agent

## Auth / identity
- `POST /api/v1/login`
- `POST /api/v1/logout`
- `GET /api/v1/auto_login`
- `POST /api/v1/refresh`
- `GET /api/v1/users/whoami`
- `GET /api/v1/users`
- `POST /api/v1/users`
- `PATCH /api/v1/users/{user_id}`
- `PATCH /api/v1/users/{user_id}/reset-password`
- `DELETE /api/v1/users/{user_id}`

## Flows / flow metadata
- `GET /api/v1/flows`
- `POST /api/v1/flows`
- `GET /api/v1/flows/{id}`
- `PATCH /api/v1/flows/{id}`
- `DELETE /api/v1/flows`
- `GET /api/v1/flows/basic_examples`
- `GET /api/v1/flows/public_flow/{id}`
- `POST /api/v1/flows/download/`
- `POST /api/v1/flows/upload`

## Flow build/execution + events
- `POST /api/v1/build/{flow_id}/vertices`
- `POST /api/v1/build/{flow_id}/vertices/{vertex_id}`
- `POST /api/v1/build/{flow_id}/flow`
- `POST /api/v1/build_public_tmp/{flow_id}/flow` (public playground mode)
- `GET /api/v1/build/{job_id}/events`
- `GET /api/v1/build/{job_id}/events?stream=false` (polling fallback)
- `POST /api/v1/build/{job_id}/cancel`
- `GET /api/v1/monitor/builds`
- `DELETE /api/v1/monitor/builds`

## Messaging / sessions
- `GET /api/v1/monitor/messages`
- `PUT /api/v1/monitor/messages`
- `PATCH /api/v1/monitor/messages`
- `DELETE /api/v1/monitor/messages`

## Components / templates / validation
- `GET /api/v1/all`
- `POST /api/v1/validate/code`
- `POST /api/v1/validate/prompt`
- `GET|POST /api/v1/custom_component`

## Global variables and config
- `GET /api/v1/variables`
- `POST /api/v1/variables`
- `PATCH /api/v1/variables`
- `DELETE /api/v1/variables`
- `GET /api/v1/config`
- `GET /api/v1/version`

## Files and folders
- `GET /api/v1/files`
- `POST /api/v1/files/upload/{flow_id}`
- `GET /api/v1/files/download/{path}`
- `GET /api/v1/files/images/{flow_id_or_path}`
- `GET /api/v1/files/profile_pictures/list`
- `GET /api/v1/folders`
- `GET /api/v1/folders/{id}`
- `POST /api/v1/folders`
- `PATCH /api/v1/folders`
- `DELETE /api/v1/folders`
- `GET /api/v1/folders/download/{folder_id}`
- `POST /api/v1/folders/upload/`

## File management v2
- `GET /api/v2/files`
- `POST /api/v2/files`
- `PUT /api/v2/files`
- `DELETE /api/v2/files`

## API keys
- `GET /api/v1/api_key`
- `POST /api/v1/api_key`
- `DELETE /api/v1/api_key`
- `POST /api/v1/api_key/store`

## Store/community
- `GET /api/v1/store/components`
- `GET /api/v1/store/components/{component_id}`
- `POST /api/v1/store/components`
- `PATCH /api/v1/store/components/{component_id}`
- `GET /api/v1/store/check/`
- `GET /api/v1/store/check/api_key`
- `GET /api/v1/store/tags`
- `POST /api/v1/store/users/likes/{component_id}`

## Voice
- `GET /api/v1/voice/elevenlabs/voice_ids`
- `WS /api/v1/voice/ws/flow_as_tool/{flow_id}/{session_id}`

## API execution snippet endpoints surfaced in UI
- `POST /api/v1/run/{flow_id_or_endpoint}?stream=false`
- `POST /api/v1/webhook/{flow_id_or_endpoint}`

## 4) External APIs called by frontend

- GitHub API: `https://api.github.com/repos/...` (store/github metadata)
- Raw GitHub content domain for examples

