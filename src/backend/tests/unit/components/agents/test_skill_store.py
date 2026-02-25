"""Tests for the SkillStore and skill tools (progressive skill disclosure)."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

import pytest

from langflow.base.agents.skills import SkillStore, parse_skill_file, parse_skill_metadata


@pytest.fixture
def skills_dir(tmp_path: Path) -> Path:
    """Create a temporary skills directory with sample skills."""
    # Skill 1: data-analysis (with supporting files)
    skill1_dir = tmp_path / "data-analysis"
    skill1_dir.mkdir()
    (skill1_dir / "SKILL.md").write_text(dedent("""\
        ---
        name: data-analysis
        description: Structured data analysis workflow for CSV and JSON datasets
        version: "1.0"
        tags:
          - data
          - analysis
        ---

        # Data Analysis Skill

        ## When to Use
        - When the user asks to analyze data

        ## Instructions
        1. Load the data
        2. Profile the data
        3. Present results
    """))
    (skill1_dir / "examples.md").write_text("# Examples\n\nSome examples here.")
    (skill1_dir / "cheatsheet.md").write_text("# Cheatsheet\n\nQuick reference.")

    # Skill 2: code-review (no supporting files)
    skill2_dir = tmp_path / "code-review"
    skill2_dir.mkdir()
    (skill2_dir / "SKILL.md").write_text(dedent("""\
        ---
        name: code-review
        description: Systematic code review with quality checklists
        version: "2.0"
        tags:
          - engineering
        dependencies:
          - data-analysis
        ---

        # Code Review

        ## Instructions
        1. Read the code
        2. Check for issues
    """))

    return tmp_path


@pytest.fixture
def store(skills_dir: Path) -> SkillStore:
    """Create and scan a SkillStore from the test skills directory."""
    s = SkillStore(skills_dir)
    s.scan()
    return s


class TestParseSkillMetadata:
    def test_parse_valid_metadata(self, skills_dir: Path):
        path = skills_dir / "data-analysis" / "SKILL.md"
        metadata = parse_skill_metadata(path)
        assert metadata.name == "data-analysis"
        assert metadata.description == "Structured data analysis workflow for CSV and JSON datasets"
        assert metadata.version == "1.0"
        assert metadata.tags == ["data", "analysis"]
        assert metadata.path == path

    def test_parse_metadata_with_dependencies(self, skills_dir: Path):
        path = skills_dir / "code-review" / "SKILL.md"
        metadata = parse_skill_metadata(path)
        assert metadata.name == "code-review"
        assert metadata.dependencies == ["data-analysis"]

    def test_parse_missing_frontmatter(self, tmp_path: Path):
        bad = tmp_path / "bad" / "SKILL.md"
        bad.parent.mkdir()
        bad.write_text("# No frontmatter here\n")
        with pytest.raises(ValueError, match="missing valid YAML frontmatter"):
            parse_skill_metadata(bad)


class TestParseSkillFile:
    def test_parse_full_skill(self, skills_dir: Path):
        path = skills_dir / "data-analysis" / "SKILL.md"
        parsed = parse_skill_file(path)
        assert parsed.metadata.name == "data-analysis"
        assert "Data Analysis Skill" in parsed.content
        assert "Load the data" in parsed.content

    def test_content_excludes_frontmatter(self, skills_dir: Path):
        path = skills_dir / "data-analysis" / "SKILL.md"
        parsed = parse_skill_file(path)
        assert "---" not in parsed.content
        assert "name: data-analysis" not in parsed.content


class TestSkillStore:
    def test_scan_finds_skills(self, store: SkillStore):
        names = store.get_skill_names()
        assert "data-analysis" in names
        assert "code-review" in names
        assert len(names) == 2

    def test_scan_nonexistent_directory(self, tmp_path: Path):
        s = SkillStore(tmp_path / "does-not-exist")
        count = s.scan()
        assert count == 0
        assert s.get_skill_names() == []

    def test_load_skill(self, store: SkillStore):
        parsed = store.load("data-analysis")
        assert parsed is not None
        assert parsed.metadata.name == "data-analysis"
        assert "Data Analysis Skill" in parsed.content

    def test_load_skill_caching(self, store: SkillStore):
        p1 = store.load("data-analysis")
        p2 = store.load("data-analysis")
        assert p1 is p2  # Same object (cached)

    def test_load_nonexistent_skill(self, store: SkillStore):
        result = store.load("nonexistent")
        assert result is None

    def test_list_supporting_files(self, store: SkillStore):
        files = store.list_supporting_files("data-analysis")
        assert "examples.md" in files
        assert "cheatsheet.md" in files
        assert len(files) == 2

    def test_list_supporting_files_empty(self, store: SkillStore):
        files = store.list_supporting_files("code-review")
        assert files == []

    def test_read_supporting_file(self, store: SkillStore):
        content = store.read_supporting_file("data-analysis", "examples.md")
        assert "Examples" in content

    def test_read_supporting_file_traversal_blocked(self, store: SkillStore):
        with pytest.raises(ValueError, match="directory traversal"):
            store.read_supporting_file("data-analysis", "../../../etc/passwd")

    def test_read_supporting_file_absolute_path_blocked(self, store: SkillStore):
        with pytest.raises(ValueError, match="directory traversal"):
            store.read_supporting_file("data-analysis", "/etc/passwd")

    def test_read_supporting_file_not_found(self, store: SkillStore):
        with pytest.raises(FileNotFoundError):
            store.read_supporting_file("data-analysis", "nonexistent.md")

    def test_read_supporting_file_skill_not_found(self, store: SkillStore):
        with pytest.raises(ValueError, match="Skill not found"):
            store.read_supporting_file("nonexistent-skill", "file.md")

    def test_get_skill_catalog(self, store: SkillStore):
        catalog = store.get_skill_catalog()
        assert "<skill>" in catalog
        assert "<name>data-analysis</name>" in catalog
        assert "<name>code-review</name>" in catalog
        assert "<description>" in catalog
        assert "examples.md" in catalog

    def test_get_skill_catalog_empty(self, tmp_path: Path):
        empty_dir = tmp_path / "empty-skills"
        empty_dir.mkdir()
        s = SkillStore(empty_dir)
        s.scan()
        assert s.get_skill_catalog() == "No skills available."

    def test_invalidate(self, store: SkillStore):
        assert len(store.get_skill_names()) == 2
        store.invalidate()
        # After invalidation, auto-rescan on next access
        assert len(store.get_skill_names()) == 2


class TestSkillTools:
    def test_create_skill_tools(self, store: SkillStore):
        from langflow.base.agents.skill_tools import create_skill_tools

        tools = create_skill_tools(store)
        assert len(tools) == 2
        tool_names = [t.name for t in tools]
        assert "load_skill" in tool_names
        assert "read_skill_file" in tool_names

    def test_load_skill_tool_success(self, store: SkillStore):
        from langflow.base.agents.skill_tools import create_skill_tools

        tools = create_skill_tools(store)
        load_tool = next(t for t in tools if t.name == "load_skill")

        result_str = load_tool.invoke({"skill_name": "data-analysis"})
        result = json.loads(result_str)
        assert result["skill_name"] == "data-analysis"
        assert "instructions" in result
        assert "Data Analysis Skill" in result["instructions"]
        assert "available_files" in result
        assert "examples.md" in result["available_files"]

    def test_load_skill_tool_not_found(self, store: SkillStore):
        from langflow.base.agents.skill_tools import create_skill_tools

        tools = create_skill_tools(store)
        load_tool = next(t for t in tools if t.name == "load_skill")

        result_str = load_tool.invoke({"skill_name": "nonexistent"})
        result = json.loads(result_str)
        assert "error" in result
        assert "available_skills" in result
        assert "data-analysis" in result["available_skills"]

    def test_read_skill_file_tool_success(self, store: SkillStore):
        from langflow.base.agents.skill_tools import create_skill_tools

        tools = create_skill_tools(store)
        read_tool = next(t for t in tools if t.name == "read_skill_file")

        result_str = read_tool.invoke({"skill_name": "data-analysis", "filename": "examples.md"})
        result = json.loads(result_str)
        assert result["skill_name"] == "data-analysis"
        assert result["filename"] == "examples.md"
        assert "Examples" in result["content"]

    def test_read_skill_file_tool_error(self, store: SkillStore):
        from langflow.base.agents.skill_tools import create_skill_tools

        tools = create_skill_tools(store)
        read_tool = next(t for t in tools if t.name == "read_skill_file")

        result_str = read_tool.invoke({"skill_name": "data-analysis", "filename": "../secret.txt"})
        result = json.loads(result_str)
        assert "error" in result
        assert "directory traversal" in result["error"]

    def test_tool_docstrings_include_skill_names(self, store: SkillStore):
        from langflow.base.agents.skill_tools import create_skill_tools

        tools = create_skill_tools(store)
        load_tool = next(t for t in tools if t.name == "load_skill")
        assert "data-analysis" in load_tool.description
        assert "code-review" in load_tool.description
