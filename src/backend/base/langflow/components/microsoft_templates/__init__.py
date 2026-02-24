"""Pre-designed message templates for Microsoft Outlook and Teams components.

Templates provide selectable layouts for automated report delivery.  Each
template is a plain Python dictionary with ``name``, ``description``,
``platform`` (``"outlook"`` or ``"teams"``), ``fields`` (list of placeholder
names the caller can map structured data into), and a ``render`` callable
that accepts a ``dict[str, str]`` of field values and returns the formatted
content string.

The module intentionally avoids external templating engines so that it has
zero additional dependencies beyond the Python standard library.
"""

from langflow.components.microsoft_templates.registry import (
    get_outlook_template_names,
    get_teams_template_names,
    get_template,
    parse_field_mapping,
    render_template,
)

__all__ = [
    "get_outlook_template_names",
    "get_teams_template_names",
    "get_template",
    "parse_field_mapping",
    "render_template",
]
