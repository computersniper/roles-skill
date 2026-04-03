#!/usr/bin/env python3
"""Skill writer - list and manage generated roles."""

import argparse
import json
import os
import sys
from pathlib import Path


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
    for role in sorted(roles, key=lambda r: r["created_at"]):
        print(f"  {role['slug']} - {role['name']}")
        print(f"    Created: {role['created_at']}")
        print(f"    Updated: {role['updated_at']}")
        print(f"    Version: {role['version']}")
        if role.get("description"):
            print(f"    Description: {role['description']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Skill writer for roles")
    parser.add_argument(
        "--action",
        choices=["list"],
        default="list",
        help="Action to perform",
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default="./roles",
        help="Base directory for roles",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser()

    if args.action == "list":
        list_roles(base_dir)
    else:
        print(f"Unknown action: {args.action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
