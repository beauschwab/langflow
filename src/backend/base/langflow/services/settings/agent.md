# services/settings/ — Settings Service

## Purpose
Application configuration management — loads settings from environment variables, `.env` files, and defaults. Includes feature flags.

## Key Files

| File | Description |
|------|-------------|
| `base.py` | `Settings` Pydantic model — all application settings with defaults and validation. Includes `enterprise_first_pass_components_only` and other enterprise settings. |
| `service.py` | `SettingsService` — provides access to the settings instance. |
| `manager.py` | Settings manager for dynamic updates. |
| `factory.py` | `SettingsServiceFactory`. |
| `auth.py` | Authentication-specific settings. |
| `feature_flags.py` | Feature flag definitions and evaluation. |
| `constants.py` | Settings constants (e.g., `DEFAULT_SUPERUSER`). |
| `utils.py` | Settings utility functions. |

## For LLM Coding Agents

- Add new configuration options to `base.py` as Pydantic fields.
- Settings are accessed via `get_settings_service()` dependency injection.
