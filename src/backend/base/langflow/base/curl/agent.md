# base/curl/ — cURL Parser

## Purpose
Parses cURL commands into structured HTTP request data. Used by the API Request component to allow users to paste cURL commands.

## Key Files

| File | Description |
|------|-------------|
| `parse.py` | cURL command string parser — extracts method, URL, headers, body from cURL syntax. |
