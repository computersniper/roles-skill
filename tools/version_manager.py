#!/usr/bin/env python3
"""Version manager - backup and rollback."""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def backup_role(slug: str, base_dir: Path):
    """Backup current version of a role."""
    role_dir = base_dir / slug
    if not role_dir.exists():
        print(f"Error: Role {slug} not found", file=sys.stderr)
        sys.exit(1)

    versions_dir = role_dir / "versions"
    versions_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = versions_dir / f"v{timestamp}"
    backup_dir.mkdir()

    # Copy all files except versions directory itself
    for item in role_dir.iterdir():
        if item.name != "versions":
            if item.is_dir():
                shutil.copytree(item, backup_dir / item.name)
            else:
                shutil.copy2(item, backup_dir / item.name)

    print(f"✅ Backed up {slug} to {backup_dir}")
    return timestamp


def rollback_role(slug: str, version: str, base_dir: Path):
    """Rollback to a specific version."""
    role_dir = base_dir / slug
    versions_dir = role_dir / "versions"

    if version == "latest":
        # Find the latest backup
        backups = sorted(list(versions_dir.iterdir()))
        if not backups:
            print(f"Error: No backups found for {slug}", file=sys.stderr)
            sys.exit(1)
        backup_dir = backups[-1]
    else:
        backup_dir = versions_dir / version
        if not backup_dir.exists():
            print(f"Error: Version {version} not found for {slug}", file=sys.stderr)
            sys.exit(1)

    # Remove current files except versions
    for item in role_dir.iterdir():
        if item.name != "versions" and item.name != ".git":
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    # Copy back from backup
    for item in backup_dir.iterdir():
        if item.is_dir():
            shutil.copytree(item, role_dir / item.name)
        else:
            shutil.copy2(item, role_dir / item.name)

    # Update meta.json version if it exists
    meta_path = role_dir / "meta.json"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        # increment version
        if "version" in meta and meta["version"].startswith("v"):
            try:
                current = int(meta["version"][1:])
                meta["version"] = f"v{current + 1}"
            except:
                pass
        meta["updated_at"] = datetime.now().isoformat()
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"✅ Rolled back {slug} to {backup_dir.name}")


def main():
    parser = argparse.ArgumentParser(description="Version manager for role skills")
    parser.add_argument(
        "--action",
        choices=["backup", "rollback"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument(
        "--slug",
        type=str,
        required=True,
        help="Role slug",
    )
    parser.add_argument(
        "--version",
        type=str,
        help="Version to rollback to (or 'latest')",
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default="./roles",
        help="Base directory for roles",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser()
    slug = args.slug

    if args.action == "backup":
        backup_role(slug, base_dir)
    elif args.action == "rollback":
        if not args.version:
            print("Error: --version is required for rollback", file=sys.stderr)
            sys.exit(1)
        rollback_role(slug, args.version, base_dir)
    else:
        print(f"Unknown action: {args.action}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
