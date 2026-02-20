# Python Backend Deep-Dive: MongoDB Persistence Option for Langflow

## Executive summary
Langflow backend persistence is currently tightly coupled to SQLModel/SQLAlchemy and Alembic. The runtime uses an async SQL session (`AsyncSession`) across API handlers, helper modules, and persistence utilities. To add a MongoDB backend option without breaking current behavior, the safest path is an **adapter-first, feature-flagged dual-backend design** that introduces a persistence contract and keeps relational mode as default.

This document provides:
- Research findings on the current persistence model.
- A technical specification for introducing MongoDB as an optional backend.
- A phased implementation plan with rollout, testing, and risk controls.

## Repository locations reviewed
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/database/service.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/database/factory.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/database/models/__init__.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/database/models/flow/model.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/database/models/transactions/crud.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/database/models/vertex_builds/crud.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/deps.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/api/utils.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/api/v1/flows.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/helpers/flow.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/alembic/env.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/settings/base.py`
- `/home/runner/work/langflow/langflow/src/backend/base/langflow/services/schema.py`
- `/home/runner/work/langflow/langflow/src/backend/base/pyproject.toml`

## Current-state research: persistence architecture

### 1) Persistence stack
- SQLModel models define both DB tables and typed schemas.
- SQLAlchemy async engine + `AsyncSession` drive data access.
- Alembic manages schema lifecycle and migration upgrades.
- The `DatabaseService` owns URL sanitization, engine creation, sessions, and migration orchestration.

### 2) Persistence entrypoints and lifecycle
- Service construction is centralized through `DatabaseServiceFactory` and `ServiceManager`.
- API/session dependency injection uses `get_session()` and `DbSession = Annotated[AsyncSession, Depends(get_session)]`.
- Session lifecycle and commit/rollback behavior is used broadly (`with_session`, `session_scope`).

### 3) Data model inventory (SQL-centric)
The exported persistence models include:
- `User`
- `Flow`
- `Folder`
- `MessageTable`
- `TransactionTable`
- `Variable`
- `ApiKey`

Model patterns observed:
- UUID primary keys and foreign keys.
- `Relationship(...)` links and SQL unique constraints.
- JSON-capable columns for flow payloads and tags.

### 4) Coupling depth
Persistence is not isolated behind a repository interface yet. The codebase has broad direct SQLModel/AsyncSession usage:
- API routers query models directly (`api/v1/flows.py`).
- Helpers query models directly (`helpers/flow.py`).
- Specialized CRUD modules assume SQL semantics (`transactions/crud.py`, `vertex_builds/crud.py`) including ordered subqueries and SQL deletes.
- Alembic migration metadata is bound to `SQLModel.metadata`.

### 5) Constraints for MongoDB option
Current assumptions that need adaptation:
- SQL joins/filters and constraints are relied upon directly.
- Multi-table relationship semantics are normalized relationally.
- Migration lifecycle is Alembic-specific.
- Many call sites assume `AsyncSession` and SQL query DSL.

## Architecture options considered

### Option A: Direct rewrite to Mongo (hard switch)
**Pros:** single backend after cutover.  
**Cons:** high risk, large blast radius, no safe rollback, breaks compatibility expectations.  
**Recommendation:** not suitable.

### Option B: Hybrid dual-write (SQL + Mongo always on)
**Pros:** migration confidence with reconciliation.  
**Cons:** operational complexity, consistency drift risk, larger scope than requested.  
**Recommendation:** not first step.

### Option C (recommended): Feature-flagged pluggable persistence backend
Keep relational backend as default and introduce a Mongo-backed implementation behind an explicit backend selector.

**Pros:** incremental rollout, low regression risk, clear fallback path.  
**Cons:** requires an abstraction layer and temporary duplicate logic during migration.

## Technical specification

### 1) New backend selector setting
Add a persistence backend setting, for example:
- `persistence_backend: Literal["sql", "mongo"] = "sql"`

Design notes:
- Keep existing `database_url` behavior unchanged for SQL mode.
- Add `mongo_url` and `mongo_database_name` settings for Mongo mode.
- Keep relational mode as the default to preserve current behavior.

### 2) New persistence service contract
Introduce a backend-agnostic contract (protocol or abstract service) for core operations currently spread across SQL callsites.

Minimum contract domains:
- Flows (create/read/update/delete/list/lookup by endpoint).
- Folders and folder-flow association.
- Messages (append/list/update).
- Transactions and vertex-build logs (append/list/retention cleanup).
- Users/API keys/variables read-write operations used by API/auth/runtime paths.

Key constraint: preserve existing API response schemas and runtime semantics.

### 3) Service factory and dependency wiring
- Keep `ServiceManager` and `ServiceType` integration.
- Replace direct `DatabaseServiceFactory` creation path with a backend-aware factory:
  - SQL mode: return current `DatabaseService`.
  - Mongo mode: return `MongoPersistenceService` (new).
- Keep `get_db_service()` API shape stable to minimize churn, but shift internals toward a persistence contract over time.

### 4) Mongo data model strategy
Use one collection per current aggregate root:
- `users`
- `flows`
- `folders`
- `messages`
- `transactions`
- `vertex_builds`
- `variables`
- `api_keys`

Document conventions:
- Store IDs as UUID strings to preserve external API compatibility.
- Keep `flow.data` JSON shape unchanged.
- Represent relationships with explicit reference IDs (no embedded duplication for first version).

Proposed indexes (initial):
- `flows`: `(user_id, name)` unique; `(user_id, endpoint_name)` unique; `folder_id`; `updated_at`.
- `messages`: `flow_id`, `session_id`, `timestamp`.
- `transactions`: `flow_id`, `timestamp`.
- `vertex_builds`: `(flow_id, id, timestamp)` and retention cleanup-friendly index.
- `api_keys`: `user_id`, `name` unique, token lookup index as needed by auth paths.

### 5) Behavior parity requirements
Mongo mode must preserve:
- API payload shape and status codes.
- Existing event and runtime flow execution contracts.
- Session/user scoping rules.
- Retention behavior (`max_transactions_to_keep`, `max_vertex_builds_to_keep`, `max_vertex_builds_per_vertex`).

### 6) Migration/versioning strategy
Because Alembic is SQL-only:
- Keep Alembic unchanged for SQL mode.
- Add a Mongo bootstrap/index manager for Mongo mode startup.
- Add schema version marker document (e.g., `meta.schema_version`) for controlled Mongo upgrades.

### 7) Security and compliance requirements
- Keep variable encryption and secret-handling behavior unchanged.
- Validate Mongo connection TLS/auth settings from config.
- Ensure indexes are created idempotently at startup.
- Ensure no logging of secrets from URI or credential fields.

## Implementation plan (phased)

### Phase 0: Design and scaffolding
1. Add persistence settings (`persistence_backend`, Mongo connection settings).
2. Add persistence service interface + DTO boundary types where needed.
3. Introduce backend-aware factory wiring without changing default behavior.

**Exit criteria:** SQL path unchanged and default; app boots without functional changes.

### Phase 1: Flow + folder parity
1. Implement Mongo persistence for flow/folder operations used by `/api/v1/flows`.
2. Migrate targeted read/write paths in one vertical slice to contract methods.
3. Add parity tests covering create/read/update/delete/list and endpoint-name resolution.

**Exit criteria:** Feature-flagged Mongo mode supports flow CRUD with API parity.

### Phase 2: Messages + chat-adjacent persistence
1. Implement Mongo message operations and update paths.
2. Route message persistence entrypoints through contract methods.
3. Validate behavior in chat-related APIs and helper paths.

**Exit criteria:** Message lifecycle parity in Mongo mode.

### Phase 3: Transactions + vertex build retention
1. Implement transaction logging and list APIs in Mongo mode.
2. Implement vertex-build logging and retention enforcement.
3. Validate retention policies against current settings.

**Exit criteria:** Monitoring/history endpoints behave equivalently in Mongo mode.

### Phase 4: Users/API keys/variables + auth-critical paths
1. Implement remaining auth and variable persistence operations.
2. Migrate service/auth utilities to persistence contract calls.
3. Add parity tests for auth-related DB interactions.

**Exit criteria:** End-to-end backend operation in Mongo mode for core authenticated usage.

### Phase 5: Hardening and rollout
1. Add observability counters/timers tagged by persistence backend.
2. Run performance comparison (SQL vs Mongo) for common workloads.
3. Roll out gradually with documented fallback to SQL.

**Exit criteria:** Mongo mode is production-ready for selected deployments.

## Testing and validation strategy

### Unit tests
- Contract-level tests for each persistence operation (shared test suite run against SQL and Mongo implementations).
- Edge cases: duplicate flow names/endpoints, missing IDs, UUID parsing, retention boundaries.

### API parity tests
- Reuse existing API tests with backend matrix (sql/mongo where practical).
- Ensure response models and error semantics match current contracts.

### Integration tests
- Startup behavior in Mongo mode (index/bootstrap success).
- End-to-end flow run lifecycle that depends on persisted entities.

### Rollback tests
- Verify switching `persistence_backend` back to SQL works without code changes.

## Full implementation test plan (detailed)

### Test matrix by phase

| Phase | Scope | Unit tests | API tests | Integration tests | Performance tests |
|---|---|---|---|---|---|
| 0 | Settings + factory wiring | settings parsing, backend selector default/fallback | N/A | app startup with SQL default | baseline startup time |
| 1 | Flow/folder persistence | create/update/list/name uniqueness | `/api/v1/flows` CRUD parity | startup + flow CRUD smoke in mongo mode | p50/p95 flow CRUD latency |
| 2 | Message persistence | append/update/query filters | chat/build endpoints using messages | chat session replay in mongo mode | message write/read throughput |
| 3 | Transactions/vertex-builds | retention logic and ordering | monitor/history endpoint parity | retention cleanup execution in mongo mode | retention job runtime |
| 4 | Users/API keys/variables | auth lookup + variable read/write parity | login/users/variable endpoint parity | authenticated E2E flow run | auth path latency |
| 5 | Hardening + rollout | retry/failure path behavior | mixed backend smoke tests | canary rollout + fallback verification | comparative SQL vs Mongo benchmark |

### Contract parity test suite structure
- `tests/unit/persistence_contract/`
  - `test_flows_contract.py`
  - `test_folders_contract.py`
  - `test_messages_contract.py`
  - `test_transactions_contract.py`
  - `test_vertex_builds_contract.py`
  - `test_users_auth_contract.py`
  - `test_variables_contract.py`
- Run each suite against both implementations:
  - SQL implementation fixture
  - Mongo implementation fixture

### API parity test matrix (minimum required)
- Flow lifecycle:
  - create, read, list, update, delete
  - endpoint-name lookup path
  - uniqueness conflict behavior
- Message lifecycle:
  - create/update/query by flow/session
- Monitoring:
  - transactions list order
  - vertex-build list and delete behavior
- Auth and variables:
  - active user fetch paths
  - API key create/list/revoke
  - variable create/read/update/delete

### CI implementation recommendations
- Add backend matrix job:
  - `PERSISTENCE_BACKEND=sql`
  - `PERSISTENCE_BACKEND=mongo`
- For mongo matrix leg:
  - Provision ephemeral MongoDB service in CI.
  - Run contract tests and selected API/integration suites.
- Keep existing SQL tests as mandatory gate while Mongo mode is maturing.

### Acceptance criteria for "full implementation tests"
1. Contract tests pass for SQL and Mongo implementations.
2. API parity tests pass for critical endpoints in both backends.
3. Integration smoke tests pass for startup + authenticated flow run in Mongo mode.
4. Rollback test confirms SQL fallback works by configuration switch only.
5. Benchmark report published with SQL vs Mongo p50/p95 latency and error rate.

## Documentation deliverables plan

### Documentation set required before enabling Mongo mode broadly
1. **Operator guide**
   - How to configure `persistence_backend`, `mongo_url`, and `mongo_database_name`.
   - TLS/auth configuration examples and secret-management guidance.
2. **Migration guide**
   - How to move from SQL deployments to Mongo mode (including coexistence strategy).
   - Validation checklist before/after switch.
3. **Runbook**
   - Startup/index bootstrap verification.
   - Failure handling and rollback steps.
4. **Compatibility guide**
   - Known differences or unsupported edge cases (if any).
   - Performance expectations and tuning knobs.
5. **Testing guide**
   - How to run contract/API/integration parity suites locally and in CI.

### Documentation acceptance criteria
- All config keys documented with examples.
- Rollback steps tested and documented.
- Production readiness checklist published.
- CI test matrix and local test commands documented in contributor docs.

## Risks and mitigations
- **Risk:** widespread SQL assumptions in callsites.
  - **Mitigation:** incremental vertical slices and contract-first refactor.
- **Risk:** uniqueness/consistency behavior differences.
  - **Mitigation:** explicit unique indexes and parity tests around conflicts.
- **Risk:** transactional differences for multi-document updates.
  - **Mitigation:** prefer single-document atomic patterns first; use transactions only where required.
- **Risk:** migration complexity.
  - **Mitigation:** avoid dual-write initially; keep SQL fallback and backend feature flag.

## Recommended next actions
1. Approve this adapter-first architecture and settings contract.
2. Implement Phase 0 + Phase 1 in a narrow PR focused on flow/folder persistence.
3. Add shared parity tests early, and enforce them in CI for both backends where environment permits.
