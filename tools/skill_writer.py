#!/usr/bin/env python3
"""Skill writer - create and manage generated roles."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any

try:
    from tool_generator import generate_tool, generate_tools_from_spec
except ImportError:
    # When running from different working directory
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from tool_generator import generate_tool, generate_tools_from_spec


SKILL_MD_TEMPLATE = """\
---
name: {role_slug}
description: {description}
user-invocable: true
---

# {role_name}

{full_description}

---

## PART A：能力定义

{ability_content}

---

## PART B：角色性格

{personality_content}

---

## 运行规则

{rules}
"""


DEFAULT_RULES = """\
1. 明确你的角色身份，始终保持角色的一致性
2. 当需要调用外部工具时，使用提供的 Python 工具代码
3. 先思考问题，再选择合适的工具，最后给出回答
4. 如果工具调用失败，清晰说明错误原因
"""


def slugify(name: str) -> str:
    """Convert name to slug."""
    import re
    result = []
    for char in name.lower():
        if char.isascii() and (char.isalnum() or char in ("-", "_")):
            result.append(char)
        elif char == " ":
            result.append("_")
    slug = re.sub(r"_+", "_", "".join(result)).strip("_")
    return slug if slug else "role"


def list_roles(base_dir: Path):
    """List all existing roles."""
    if not base_dir.exists():
        print("No roles created yet.")
        return

    roles = []
    for item in base_dir.iterdir():
        if item.is_dir() and (item / "meta.json").exists():
            try:
                with open(item / "meta.json", "r", encoding="utf-8") as f:
                    meta = json.load(f)
                roles.append(meta)
            except Exception as e:
                print(f"Warning: Could not read {item}: {e}", file=sys.stderr)

    if not roles:
        print("No roles found.")
        return

    print(f"Found {len(roles)} role(s):\n")
    for role in sorted(roles, key=lambda r: r.get("created_at", "")):
        print(f"  {role.get('slug', role.get('name', 'unknown'))} - {role.get('name', 'unknown')}")
        print(f"    Created: {role.get('created_at', 'unknown')}")
        print(f"    Updated: {role.get('updated_at', 'unknown')}")
        print(f"    Version: {role.get('version', 'unknown')}")
        if role.get("description"):
            print(f"    Description: {role['description']}")
        if role.get("tools"):
            print(f"    Tools: {', '.join(role['tools'])}")
        print()


def create_role(
    base_dir: Path,
    slug: str,
    meta: Dict[str, Any],
    ability_content: str,
    personality_content: str,
    rules_content: Optional[str] = None,
    tools_spec: Optional[list[Dict[str, Any]]] = None,
) -> Path:
    """Create a new role directory structure.

    Args:
        base_dir: Base directory for all roles
        slug: Role slug (directory name)
        meta: Metadata dictionary
        ability_content: Content for ability/definition section
        personality_content: Content for personality section
        rules_content: Optional custom rules
        tools_spec: Optional list of tool specifications to generate

    Returns:
        Path to the created role directory
    """
    role_dir = base_dir / slug
    role_dir.mkdir(parents=True, exist_ok=True)

    # Create standard subdirectories
    (role_dir / "versions").mkdir(exist_ok=True)
    (role_dir / "knowledge").mkdir(parents=True, exist_ok=True)
    (role_dir / "tools").mkdir(parents=True, exist_ok=True)  # Tools directory for Python tools

    # Write content files
    (role_dir / "ability.md").write_text(ability_content, encoding="utf-8")
    (role_dir / "personality.md").write_text(personality_content, encoding="utf-8")

    # Generate tools if specification provided
    generated_tools = []
    if tools_spec:
        generated_paths = generate_tools_from_spec(
            base_dir=base_dir,
            role_slug=slug,
            tools_spec=tools_spec,
        )
        generated_tools = [p.stem for p in generated_paths]
        print(f"  Generated {len(generated_paths)} tool(s) in {role_dir / 'tools'}")

    # Generate complete SKILL.md
    role_name = meta.get("name", slug)
    description = meta.get("description", "")
    full_description = meta.get("full_description", description)

    skill_md = SKILL_MD_TEMPLATE.format(
        role_slug=slug,
        role_name=role_name,
        description=description,
        full_description=full_description,
        ability_content=ability_content,
        personality_content=personality_content,
        rules=rules_content or DEFAULT_RULES,
    )
    (role_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # Update metadata
    now = datetime.now(timezone.utc).isoformat()
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta["version"] = "v1"
    meta.setdefault("corrections_count", 0)
    if generated_tools:
        meta["tools"] = generated_tools

    (role_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return role_dir


def update_role(
    role_dir: Path,
    ability_patch: Optional[str] = None,
    personality_patch: Optional[str] = None,
    correction: Optional[Dict[str, str]] = None,
    new_tools: Optional[list[Dict[str, Any]]] = None,
) -> str:
    """Update an existing role, archive current version first."""

    meta_path = role_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    current_version = meta.get("version", "v1")
    try:
        version_num = int(current_version.lstrip("v").split("_")[0]) + 1
    except ValueError:
        version_num = 2
    new_version = f"v{version_num}"

    # Archive current version
    version_dir = role_dir / "versions" / current_version
    version_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("SKILL.md", "ability.md", "personality.md", "meta.json"):
        src = role_dir / fname
        if src.exists():
            shutil.copy2(src, version_dir / fname)

    # Apply ability patch
    if ability_patch:
        current_ability = (role_dir / "ability.md").read_text(encoding="utf-8")
        new_ability = current_ability + "\n\n" + ability_patch
        (role_dir / "ability.md").write_text(new_ability, encoding="utf-8")

    # Generate new tools if specified
    if new_tools:
        base_dir = role_dir.parent
        generated_paths = generate_tools_from_spec(
            base_dir=base_dir,
            role_slug=meta["slug"],
            tools_spec=new_tools,
        )
        generated_names = [p.stem for p in generated_paths]
        existing_tools = meta.get("tools", [])
        existing_tools.extend(generated_names)
        meta["tools"] = list(dict.fromkeys(existing_tools))  # deduplicate
        print(f"  Added {len(generated_names)} new tool(s)")

    # Apply personality patch or correction
    if personality_patch or correction:
        current_personality = (role_dir / "personality.md").read_text(encoding="utf-8")

        if correction:
            correction_line = (
                f"\n- [{correction.get('scene', '通用')}] "
                f"不应该 {correction['wrong']}，应该 {correction['correct']}"
            )
            target = "## Correction 记录"
            if target in current_personality:
                insert_pos = current_personality.index(target) + len(target)
                # Skip empty line and "no records" placeholder
                rest = current_personality[insert_pos:]
                skip = "\n\n（暂无记录）"
                if rest.startswith(skip):
                    rest = rest[len(skip):]
                new_personality = current_personality[:insert_pos] + correction_line + rest
            else:
                new_personality = (
                    current_personality
                    + f"\n\n## Correction 记录\n{correction_line}\n"
                )
            meta["corrections_count"] = meta.get("corrections_count", 0) + 1
        else:
            new_personality = current_personality + "\n\n" + personality_patch

        (role_dir / "personality.md").write_text(new_personality, encoding="utf-8")

    # Regenerate SKILL.md
    ability_content = (role_dir / "ability.md").read_text(encoding="utf-8")
    personality_content = (role_dir / "personality.md").read_text(encoding="utf-8")
    role_name = meta.get("name", role_dir.name)
    description = meta.get("description", "")
    full_description = meta.get("full_description", description)

    skill_md = SKILL_MD_TEMPLATE.format(
        role_slug=meta["slug"],
        role_name=role_name,
        description=description,
        full_description=full_description,
        ability_content=ability_content,
        personality_content=personality_content,
        rules=DEFAULT_RULES,
    )
    (role_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # Update metadata
    meta["version"] = new_version
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()
    meta_path.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return new_version


def main():
    parser = argparse.ArgumentParser(description="Skill writer for roles")
    parser.add_argument(
        "--action",
        choices=["list", "create", "update"],
        default="list",
        help="Action to perform",
    )
    parser.add_argument("--slug", help="Role slug (directory name)")
    parser.add_argument("--name", help="Role name")
    parser.add_argument("--meta", help="Meta JSON file path")
    parser.add_argument("--ability", help="ability.md content file path")
    parser.add_argument("--personality", help="personality.md content file path")
    parser.add_argument("--ability-patch", help="ability.md incremental update")
    parser.add_argument("--personality-patch", help="personality.md incremental update")
    parser.add_argument("--tools-spec", help="JSON file with tools specification")
    parser.add_argument(
        "--base-dir",
        type=str,
        default="./roles",
        help="Base directory for roles (default: ./roles)",
    )

    args = parser.parse_args()
    base_dir = Path(args.base_dir).expanduser()

    if args.action == "list":
        list_roles(base_dir)

    elif args.action == "create":
        if not args.slug and not args.name:
            print("Error: create requires --slug or --name", file=sys.stderr)
            sys.exit(1)

        # Load metadata
        meta: Dict[str, Any] = {}
        if args.meta:
            meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
        if args.name:
            meta["name"] = args.name

        slug = args.slug or slugify(meta.get("name", "role"))

        # Load content
        ability_content = ""
        if args.ability:
            ability_content = Path(args.ability).read_text(encoding="utf-8")

        personality_content = ""
        if args.personality:
            personality_content = Path(args.personality).read_text(encoding="utf-8")

        # Load tools spec
        tools_spec = None
        if args.tools_spec:
            tools_spec = json.loads(Path(args.tools_spec).read_text(encoding="utf-8"))

        role_dir = create_role(
            base_dir=base_dir,
            slug=slug,
            meta=meta,
            ability_content=ability_content,
            personality_content=personality_content,
            tools_spec=tools_spec,
        )
        print(f"✅ Role created: {role_dir}")
        print(f"   Trigger: /{slug}")
        if tools_spec:
            print(f"   Tools generated: {len(tools_spec)}")

    elif args.action == "update":
        if not args.slug:
            print("Error: update requires --slug", file=sys.stderr)
            sys.exit(1)

        role_dir = base_dir / args.slug
        if not role_dir.exists():
            print(f"Error: Role directory not found {role_dir}", file=sys.stderr)
            sys.exit(1)

        ability_patch = None
        if args.ability_patch:
            ability_patch = Path(args.ability_patch).read_text(encoding="utf-8")

        personality_patch = None
        if args.personality_patch:
            personality_patch = Path(args.personality_patch).read_text(encoding="utf-8")

        new_tools = None
        if args.tools_spec:
            new_tools = json.loads(Path(args.tools_spec).read_text(encoding="utf-8"))

        new_version = update_role(
            role_dir=role_dir,
            ability_patch=ability_patch,
            personality_patch=personality_patch,
            new_tools=new_tools,
        )
        print(f"✅ Role updated to {new_version}: {role_dir}")

    else:
        print(f"Unknown action: {args.action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
