# custom/directory_reader/ — Directory Component Scanner

## Purpose
Scans directories for Python files containing Langflow component definitions. Used to load components from external paths.

## Key Files

| File | Description |
|------|-------------|
| `directory_reader.py` | `DirectoryReader` — scans a directory tree for `.py` files, parses them for component classes, and registers discovered components. |
| `utils.py` | Directory scanning utility functions. |
