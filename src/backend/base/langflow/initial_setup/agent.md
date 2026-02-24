# initial_setup/ — First-Run Setup

## Purpose
Handles first-run initialization — creating the super user, loading starter projects, setting up default folders, and loading profile pictures.

## Folder Structure

| Folder / File | Description |
|---------------|-------------|
| `starter_projects/` | JSON files for pre-built starter/template flows that appear in a new installation. |
| `profile_pictures/` | Default avatar images for users. |
| `setup.py` | Main setup orchestrator — `create_or_update_starter_projects()`, `initialize_super_user_if_needed()`, `load_flows_from_directory()`, `sync_flows_from_fs()`. |
| `load.py` | Flow loading utilities for initial setup. |
| `constants.py` | Setup constants. |

## For LLM Coding Agents

- Starter projects are JSON flow files — add new ones to `starter_projects/` to include them in fresh installations.
- The super user is created with credentials from `DEFAULT_SUPERUSER` settings constant.
