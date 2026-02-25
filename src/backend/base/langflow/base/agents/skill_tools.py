"""Tool definitions for the progressive skill disclosure system.

Creates two LangChain tools that let the LLM interact with the skill store:

- ``load_skill(skill_name)`` — returns full SKILL.md content + available files.
- ``read_skill_file(skill_name, filename)`` — returns a specific supporting file.

Tools are exposed via a factory function that captures the SkillStore instance.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from langflow.base.agents.skills import SkillStore


class LoadSkillInput(BaseModel):
    """Input schema for the load_skill tool."""

    skill_name: str = Field(description="Exact name of the skill to load from the catalog.")


class ReadSkillFileInput(BaseModel):
    """Input schema for the read_skill_file tool."""

    skill_name: str = Field(description="Name of the skill that owns the file.")
    filename: str = Field(description="Name of the supporting file to read (from available_files).")


def create_skill_tools(store: SkillStore) -> list[StructuredTool]:
    """Create skill-loading tools bound to a SkillStore instance.

    Returns a list containing ``load_skill`` and ``read_skill_file`` tools.
    Both return JSON strings for structured LLM parsing.

    Args:
        store: The SkillStore instance to bind tools to.

    Returns:
        List of two StructuredTool instances.
    """
    available = ", ".join(store.get_skill_names()) or "none"

    def load_skill(skill_name: str) -> str:
        """Load expert knowledge for a skill. Returns JSON with instructions and available supporting files."""
        parsed = store.load(skill_name)
        if parsed is None:
            names = ", ".join(store.get_skill_names())
            return json.dumps(
                {"error": f"Skill '{skill_name}' not found", "available_skills": names}
            )

        available_files = store.list_supporting_files(skill_name)
        return json.dumps({
            "skill_name": skill_name,
            "description": parsed.metadata.description,
            "instructions": parsed.content,
            "available_files": available_files,
        })

    def read_skill_file(skill_name: str, filename: str) -> str:
        """Read a supporting file from a skill folder. Returns JSON with the file content."""
        try:
            content = store.read_supporting_file(skill_name, filename)
            return json.dumps({
                "skill_name": skill_name,
                "filename": filename,
                "content": content,
            })
        except (FileNotFoundError, ValueError) as e:
            return json.dumps({"error": f"Error reading file: {e}"})

    load_tool = StructuredTool.from_function(
        func=load_skill,
        name="load_skill",
        description=(
            f"Load expert knowledge for a skill. Returns JSON with the skill's "
            f"instructions and a list of available supporting files.\n\n"
            f"Available skills: {available}\n\n"
            f"Args:\n    skill_name: Exact name of the skill to load."
        ),
        args_schema=LoadSkillInput,
    )

    read_tool = StructuredTool.from_function(
        func=read_skill_file,
        name="read_skill_file",
        description=(
            f"Read a supporting file from a skill folder. Returns JSON with the "
            f"file content.\n\n"
            f"Use this to access reference documents listed in the "
            f"'available_files' field of a loaded skill.\n\n"
            f"Available skills: {available}\n\n"
            f"Args:\n    skill_name: Name of the skill that owns the file.\n"
            f"    filename: Name of the file to read (from the skill's available_files)."
        ),
        args_schema=ReadSkillFileInput,
    )

    return [load_tool, read_tool]
