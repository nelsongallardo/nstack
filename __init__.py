from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hermes_cli.plugins import PluginContext

ROOT = Path(__file__).resolve().parent
# Hermes rejects a system prompt section over 4,000 characters.
MAX_SECTION_CHARS = 4_000


def core_sections(core: str) -> list[tuple[str, str]]:
    routing, rest = core.split("\n## Start\n", 1)
    workflow, autonomy = rest.split("\n## Autonomy\n", 1)
    return [
        ("nstack.1-routing", routing.strip()),
        ("nstack.2-workflow", ("## Start\n" + workflow).strip()),
        ("nstack.3-autonomy", ("## Autonomy\n" + autonomy).strip()),
    ]


def register(ctx: PluginContext) -> None:
    from agent.skill_utils import extract_skill_description, parse_frontmatter

    for section_id, content in core_sections((ROOT / "core.md").read_text(encoding="utf-8")):
        ctx.register_system_prompt_section(section_id, content, max_chars=len(content))

    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        frontmatter, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        ctx.register_skill(path.parent.name, path, extract_skill_description(frontmatter), frontmatter)
