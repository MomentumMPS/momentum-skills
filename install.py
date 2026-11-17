#!/usr/bin/env python3
"""Copy skills globally for Codex by default, without replacing existing files."""

import argparse
from fnmatch import fnmatchcase
from pathlib import Path
import stat
import sys


HOST_ROOTS = {
    "codex": (".agents/skills",),
    "claude": (".claude/skills",),
    "cursor": (".agents/skills",),
    "all": (".agents/skills", ".claude/skills"),
}
EXCLUDED = (
    "__pycache__", "*.py[cod]", ".DS_Store", "._*", "Thumbs.db", "desktop.ini",
    ".git", ".venv", "node_modules", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".env", ".env.*", "project-memory.json", "skill-inventory.json", "work-journal.md",
)


def is_link(path: Path) -> bool:
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def contents(directory: Path) -> dict:
    """Read a filtered snapshot before writing; never follow skill resource links."""
    if is_link(directory) or not directory.is_dir():
        raise ValueError(f"Expected a real skill directory: {directory}")
    files = {}
    pending = [directory]
    while pending:
        for path in sorted(pending.pop().iterdir()):
            if is_link(path):
                raise ValueError(f"Linked resources are not supported: {path}")
            if any(fnmatchcase(path.name, pattern) for pattern in EXCLUDED):
                continue
            mode = path.stat().st_mode
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                files[path.relative_to(directory)] = (path.read_bytes(), stat.S_IMODE(mode))
            else:
                raise ValueError(f"Unsupported resource type: {path}")
    return files


def install(
    repo: Path, user_home: Path, *, host: str = "codex", dry_run: bool = False
) -> None:
    if host not in HOST_ROOTS:
        raise ValueError(f"Unknown host: {host}")
    source_root = repo / "skills"
    if is_link(source_root):
        raise ValueError("The source skills directory must not be a link.")
    sources = {}
    for source in sorted(source_root.glob("*/SKILL.md")):
        files = contents(source.parent)
        if Path("SKILL.md") not in files:
            raise ValueError(f"Missing regular SKILL.md: {source.parent}")
        sources[source.parent.name] = files
    if not sources:
        raise ValueError("No skills found beside install.py.")

    user_home = user_home.resolve()
    roots = [user_home / location for location in HOST_ROOTS[host]]
    conflicts = []
    for root in roots:
        for parent in (root, root.parent):
            if is_link(parent) or (parent.exists() and not parent.is_dir()):
                conflicts.append(str(parent))
    pending = []
    unchanged = []
    for root in roots:
        for name, files in sources.items():
            target = root / name
            if is_link(target):
                conflicts.append(str(target))
            elif target.exists():
                try:
                    existing = contents(target)
                    identical = {p: data for p, (data, _) in existing.items()} == {
                        p: data for p, (data, _) in files.items()
                    }
                except (OSError, ValueError):
                    identical = False
                if identical:
                    unchanged.append(target)
                else:
                    conflicts.append(str(target))
            else:
                pending.append((target, files))
    if conflicts:
        raise FileExistsError(
            "Existing paths need review; nothing was changed:\n  "
            + "\n  ".join(sorted(set(conflicts)))
            + "\nCompare and back up these paths outside skill discovery folders, then retry."
        )

    for target in unchanged:
        print(f"Already installed: {target}")
    for target, files in pending:
        if dry_run:
            print(f"Would copy: {target}")
            continue
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            # Reserve a new folder exclusively; a concurrently created target survives.
            target.mkdir()
            # Publish the skill entrypoint last so earlier copy errors leave it undiscoverable.
            for relative in sorted(files, key=lambda p: (p == Path("SKILL.md"), str(p))):
                data, mode = files[relative]
                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("xb") as stream:
                    stream.write(data)
                destination.chmod(mode)
        except OSError as error:
            raise OSError(
                f"Copy stopped at {target}; earlier copies or a partial folder may remain. "
                "No existing files were replaced. Inspect this folder before retrying."
            ) from error
        print(f"Installed: {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host", choices=HOST_ROOTS, default="codex",
        help="Installation target (default: codex; codex and cursor share a root)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Check paths without writing")
    args = parser.parse_args()
    try:
        install(Path(__file__).resolve().parent, Path.home(), host=args.host, dry_run=args.dry_run)
    except (OSError, ValueError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        sys.exit(1)
