"""Skill store and loader for progressive skill disclosure.

This module implements the skills system for the Deep Agent. Skills are
self-contained packages of domain knowledge stored as directories on the
filesystem. Each skill directory contains:

- ``SKILL.md`` (required) — YAML frontmatter (metadata) + markdown body (instructions).
- Supporting files (optional) — additional ``.md`` files referenced by SKILL.md.

The ``SkillStore`` handles:

1. **Discovery** — scanning a directory tree for SKILL.md files.
2. **Metadata caching** — parsing only YAML frontmatter for the catalog.
3. **Lazy content loading** — full markdown body parsed on ``load_skill()`` call.
4. **On-demand file reading** — supporting files read via ``read_skill_file()``.

This implements progressive disclosure: the LLM sees a lightweight catalog
first, loads full instructions only when needed, and drills into supporting
files only if the instructions reference them.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# Regex to split SKILL.md into YAML frontmatter and markdown body.
FRONTMATTER_PATTERN = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n(.*)$",
    re.DOTALL,
)


@dataclass
class SkillMetadata:
    """Metadata from a SKILL.md file's YAML frontmatter.

    Lightweight representation used during discovery phase. The store keeps
    one ``SkillMetadata`` per skill for catalog generation without loading
    the full markdown body.
    """

    name: str
    description: str
    version: str = "1.0"
    tags: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    path: Path | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any], path: Path | None = None) -> SkillMetadata:
        """Create a ``SkillMetadata`` from a parsed YAML frontmatter dict."""
        return cls(
            name=data.get("name", "unknown"),
            description=data.get("description", ""),
            version=str(data.get("version", "1.0")),
            tags=data.get("tags", []),
            dependencies=data.get("dependencies", []),
            path=path,
        )


@dataclass
class ParsedSkill:
    """A fully parsed skill — metadata plus the markdown body."""

    metadata: SkillMetadata
    content: str


def parse_skill_file(path: Path) -> ParsedSkill:
    """Parse a SKILL.md file into metadata + markdown content.

    Args:
        path: Path to the SKILL.md file.

    Returns:
        ParsedSkill with metadata and content.

    Raises:
        ValueError: If frontmatter is missing or malformed.
    """
    raw = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(raw)
    if not match:
        msg = f"SKILL.md at {path} is missing valid YAML frontmatter (---...---)"
        raise ValueError(msg)

    frontmatter_str = match.group(1)
    content = match.group(2).strip()

    try:
        frontmatter = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError as e:
        msg = f"Invalid YAML frontmatter in {path}: {e}"
        raise ValueError(msg) from e

    if not isinstance(frontmatter, dict):
        msg = f"YAML frontmatter in {path} must be a mapping, got {type(frontmatter).__name__}"
        raise ValueError(msg)

    metadata = SkillMetadata.from_dict(frontmatter, path=path)
    return ParsedSkill(metadata=metadata, content=content)


def parse_skill_metadata(path: Path) -> SkillMetadata:
    """Parse only the YAML frontmatter of a SKILL.md file (fast, no body).

    Args:
        path: Path to the SKILL.md file.

    Returns:
        SkillMetadata extracted from frontmatter.

    Raises:
        ValueError: If frontmatter is missing or malformed.
    """
    raw = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(raw)
    if not match:
        msg = f"SKILL.md at {path} is missing valid YAML frontmatter (---...---)"
        raise ValueError(msg)

    frontmatter_str = match.group(1)
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
    except yaml.YAMLError as e:
        msg = f"Invalid YAML frontmatter in {path}: {e}"
        raise ValueError(msg) from e

    if not isinstance(frontmatter, dict):
        msg = f"YAML frontmatter in {path} must be a mapping, got {type(frontmatter).__name__}"
        raise ValueError(msg)

    return SkillMetadata.from_dict(frontmatter, path=path)


def read_skill_supporting_file(skill_dir: Path, filename: str) -> str:
    """Read a supporting file from a skill's directory.

    Security: rejects filenames with ``..`` or absolute paths.

    Args:
        skill_dir: Directory containing the skill.
        filename: Relative filename to read.

    Returns:
        File content as a string.

    Raises:
        ValueError: If filename contains directory traversal characters.
        FileNotFoundError: If the file does not exist.
    """
    if ".." in filename or filename.startswith("/") or filename.startswith("\\"):
        msg = f"Invalid filename '{filename}': directory traversal is not allowed"
        raise ValueError(msg)

    file_path = skill_dir / filename
    resolved = file_path.resolve()

    # Ensure resolved path is within the skill directory
    if not str(resolved).startswith(str(skill_dir.resolve())):
        msg = f"Invalid filename '{filename}': path escapes skill directory"
        raise ValueError(msg)

    if not file_path.is_file():
        msg = f"File '{filename}' not found in skill directory {skill_dir}"
        raise FileNotFoundError(msg)

    return file_path.read_text(encoding="utf-8")


class SkillStore:
    """Manages skill discovery, caching, and loading.

    The store scans a directory for skill folders (each containing SKILL.md),
    caches metadata for the catalog, and loads full content on demand.
    """

    def __init__(self, skills_dir: str | Path) -> None:
        self._skills_dir = Path(skills_dir)
        self._metadata_cache: dict[str, SkillMetadata] = {}
        self._content_cache: dict[str, ParsedSkill] = {}
        self._scanned = False

    @property
    def skills_dir(self) -> Path:
        return self._skills_dir

    def scan(self) -> int:
        """Scan the skills directory for SKILL.md files.

        Only parses YAML frontmatter (fast). Returns the number of
        skills discovered.
        """
        self._metadata_cache.clear()
        self._content_cache.clear()

        if not self._skills_dir.is_dir():
            logger.warning("Skills directory does not exist: %s", self._skills_dir)
            self._scanned = True
            return 0

        count = 0
        for skill_md in self._skills_dir.rglob("SKILL.md"):
            try:
                metadata = parse_skill_metadata(skill_md)
                if metadata.name in self._metadata_cache:
                    logger.warning(
                        "Duplicate skill name '%s' at %s (overwriting previous)",
                        metadata.name,
                        skill_md,
                    )
                self._metadata_cache[metadata.name] = metadata
                count += 1
            except (ValueError, OSError) as e:
                logger.error("Failed to parse skill at %s: %s", skill_md, e)

        self._scanned = True
        logger.info("Skill store scanned %d skills from %s", count, self._skills_dir)
        return count

    def load(self, skill_name: str) -> ParsedSkill | None:
        """Load a skill's full content (markdown body + metadata).

        Returns cached result on subsequent calls for the same skill.
        """
        if not self._scanned:
            self.scan()

        # Check content cache first
        if skill_name in self._content_cache:
            return self._content_cache[skill_name]

        metadata = self._metadata_cache.get(skill_name)
        if not metadata or not metadata.path:
            logger.warning("Skill not found: %s", skill_name)
            return None

        try:
            parsed = parse_skill_file(metadata.path)
            self._content_cache[skill_name] = parsed
            logger.debug("Loaded skill content: %s", skill_name)
            return parsed
        except (ValueError, OSError) as e:
            logger.error("Failed to load skill %s: %s", skill_name, e)
            return None

    def read_supporting_file(self, skill_name: str, filename: str) -> str:
        """Read a supporting file from a skill folder.

        Raises:
            ValueError: If skill not found or filename is invalid.
            FileNotFoundError: If the file does not exist.
        """
        metadata = self._metadata_cache.get(skill_name)
        if not metadata or not metadata.path:
            msg = f"Skill not found: {skill_name}"
            raise ValueError(msg)

        skill_dir = metadata.path.parent
        return read_skill_supporting_file(skill_dir, filename)

    def list_supporting_files(self, skill_name: str) -> list[str]:
        """List supporting files (non-SKILL.md .md files) in a skill's directory."""
        metadata = self._metadata_cache.get(skill_name)
        if not metadata or not metadata.path:
            return []

        skill_dir = metadata.path.parent
        return sorted(
            str(f.relative_to(skill_dir))
            for f in skill_dir.rglob("*.md")
            if f.is_file() and f.name != "SKILL.md"
        )

    def get_skill_catalog(self) -> str:
        """Generate a structured catalog of all available skills.

        Uses XML tags for reliable LLM parsing. Includes skill names,
        descriptions, tags, and supporting file lists.
        """
        if not self._scanned:
            self.scan()

        if not self._metadata_cache:
            return "No skills available."

        lines: list[str] = []
        for name, metadata in sorted(self._metadata_cache.items()):
            lines.append("<skill>")
            lines.append(f"  <name>{name}</name>")
            lines.append(f"  <description>{metadata.description}</description>")
            if metadata.tags:
                lines.append(f"  <tags>{', '.join(metadata.tags)}</tags>")
            files = self.list_supporting_files(name)
            if files:
                lines.append(f"  <supporting_files>{', '.join(files)}</supporting_files>")
            lines.append("</skill>")

        return "\n".join(lines)

    def get_skill_names(self) -> list[str]:
        """Get list of all registered skill names."""
        if not self._scanned:
            self.scan()
        return list(self._metadata_cache.keys())

    def invalidate(self) -> None:
        """Clear all caches and force rescan on next access."""
        self._metadata_cache.clear()
        self._content_cache.clear()
        self._scanned = False
        logger.info("Skill store cache invalidated")
