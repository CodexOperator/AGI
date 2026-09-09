#!/usr/bin/env python3
"""write_guard.py — detect unsanctioned node writes.

Sanctioned writes are logged by `node_writer.write_node` and
`node_writer.update_node` to `.agi/sessions/write-log.jsonl`. Any node or
payload file whose bytes have changed since HEAD without appearing in that
log is an unsanctioned write.

Commands
--------
  check [--strict]     Print WARN for each unsanctioned write; exit 1 if any
                       and --strict is set, else 0.
  hook                 Print a two-line git pre-commit hook body that runs
                       `write_guard.py check --strict` and exits non-zero if
                       there are unsanctioned writes.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

#: Known log path relative to the project root.
WRITE_LOG = "sessions/write-log.jsonl"

#: Fields a payload_ref in a build node stores the link under.
LINK_FIELDS = ("payload_ref", "link_ref")


def find_project_root(start: Path | None = None) -> Path | None:
    """Resolve the nearest .agi/ that holds a config (goal:g11).

    Phase order from locations.py (simplified inline):
      0. <d>/.agi/ holding a config  -> <d>/.agi
      1. <d>/agi-tree.config.json     -> <d>
    """
    if start is None:
        start = Path.cwd()
    for parent in [start] + list(start.parents):
        agi = parent / ".agi"
        if agi.is_dir() and (agi / "config.json").is_file():
            return agi
        if (parent / "agi-tree.config.json").is_file():
            return parent
    return None


def _git_root(cwd: Path) -> Path | None:
    """Return the git worktree root, or None."""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return Path(r.stdout.strip())
    except BaseException:
        pass
    return None


def _git_changed_files(root: Path, agi_root: Path, subdir: str = "nodes") -> list[dict]:
    """List of {path, old_sha256} for files under .agi/<subdir>/ changed vs HEAD.

    `subdir` defaults to `nodes` (the node tree); the context pass passes
    `"context"` to sweep `.agi/context/*.md` design docs (l3w4). Includes
    modified and untracked files. Returns paths relative to the repo root
    (agi_root is under the repo).
    """
    git = _git_root(root)
    if git is None:
        return []  # not a git repo, cannot check
    try:
        # Modified (tracked, differs from HEAD)
        r = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=git, capture_output=True, text=True, timeout=30)
        modified = r.stdout.strip().splitlines() if r.returncode == 0 else []
        # Untracked
        r2 = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=git, capture_output=True, text=True, timeout=30)
        untracked = r2.stdout.strip().splitlines() if r2.returncode == 0 else []
    except BaseException:
        return []

    # Filter to files under the agi subdir (nodes/ or context/)
    prefix = _rel_dir_prefix(agi_root, git, subdir)
    interesting = []
    seen = set()
    for fname in modified + untracked:
        f = Path(fname)
        if not f.as_posix().startswith(prefix):
            continue
        # .lock files created by _claim_node are not node writes -- skip
        if f.suffix == ".lock":
            continue
        key = f.as_posix()
        if key in seen:
            continue
        seen.add(key)
        abspath = git / f
        try:
            sha = hashlib.sha256(abspath.read_bytes()).hexdigest()
        except BaseException:
            sha = ""
        interesting.append({"path": f.as_posix(), "old_sha256": sha,
                             "abspath": str(abspath)})
    return interesting


def _rel_node_prefix(agi_root: Path, git_root: Path) -> str:
    """The relative path prefix for node files: e.g. '.agi/nodes/'."""
    return _rel_dir_prefix(agi_root, git_root, "nodes")


def _rel_dir_prefix(agi_root: Path, git_root: Path, subdir: str) -> str:
    """The relative path prefix for a tree under .agi/: e.g. '.agi/nodes/'."""
    try:
        rel = agi_root.resolve().relative_to(git_root.resolve())
        return (rel / subdir).as_posix()
    except (ValueError, OSError):
        return f".agi/{subdir}"


def _load_log(agi_root: Path):
    """Index the write log for sanctioned-write matching.

    Returns `(keyed_sets, sha_to_path)`:

    - `keyed_sets`: a `Sanctioned` bundle holding `{mint_id, sha256}` pairs and
      `{sha256}` (the fallback for bytes written before a node carried a
      mint_id).
    - `sha_to_path`: sha256 -> last path, for the redo hint.

    The log is per-box scratch under sessions/ and gitignored; an absent log
    means nothing is sanctioned yet, which the caller treats as a warning
    state, not a crash (l2w15-write-guard SETTLED rekey).
    """
    class Sanctioned:
        __slots__ = ("by_key", "by_sha")

        def __init__(self):
            self.by_key = set()   # (mint_id, sha256)
            self.by_sha = set()   # sha256 only (fallback)

        def has(self, mint_id: str, sha: str) -> bool:
            """True when these bytes were written through a sanctioned path.

            Matches by (mint_id, sha256) first; falls back to sha256-alone for
            bytes logged before a node existed with a mint_id (SETTLED rekey:
            the grid-ref identifier is what version history keys on, so a clean
            `git mv` / retitle of an already-logged node stays silent).
            """
            if (mint_id, sha) in self.by_key:
                return True
            return sha in self.by_sha

    san = Sanctioned()
    sha_to_path: dict[str, str] = {}
    log_path = agi_root / WRITE_LOG
    if not log_path.is_file():
        return san, sha_to_path
    try:
        for line in log_path.read_text().strip().splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            sha = entry.get("sha256", "")
            p = entry.get("path", "")
            if sha:
                san.by_sha.add(sha)
                mi = entry.get("mint_id", "")
                if mi:
                    san.by_key.add((mi, sha))
                sha_to_path.setdefault(sha, p)
    except BaseException:
        pass
    return san, sha_to_path


def _read_payload_refs(agi_root: Path) -> list[dict]:
    """Read payload_ref from build nodes, return {path, sha256, node_id}."""
    payloads = []
    nodes_dir = agi_root / "nodes"
    if not nodes_dir.is_dir():
        return payloads
    for nf in sorted(nodes_dir.rglob("*.md")):
        text = nf.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            import yaml
            fm = yaml.safe_load(parts[1]) or {}
        except BaseException:
            continue
        nid = fm.get("id", "")
        mi = str(fm.get("mint_id", "") or "")
        # Every link field that a build node uses to declare its file
        ref = None
        for fld in LINK_FIELDS:
            v = fm.get(fld)
            if isinstance(v, str) and v.strip():
                ref = v.strip()
                break
        if not ref:
            continue
        # Resolve the payload relative to the git root (source root)
        git = _git_root(agi_root)
        if git is None:
            continue
        payload_path = git / ref
        if not payload_path.is_file():
            continue
        try:
            sha = hashlib.sha256(payload_path.read_bytes()).hexdigest()
        except BaseException:
            continue
        payloads.append({"node_id": str(nid), "mint_id": mi, "ref": str(ref),
                         "path": str(payload_path), "sha256": sha})
    return payloads


def _redo_hint(abi_path: str, agi_root: Path) -> str:
    """Suggest the write.py command to redo this write properly."""
    # Try to extract node id from the path
    p = Path(abi_path)
    # Path is like .agi/nodes/hypothesis/some-slug.md
    parts = p.parts
    node_type = None
    slug = None
    for i, part in enumerate(parts):
        if part == "nodes" and i + 2 < len(parts):
            node_type = parts[i + 1]
            slug = parts[i + 2].replace(".md", "")
            break
    if node_type and slug:
        node_id = f"{node_type}:{slug}"
        return (f"python3 extensions/agi/bin/write.py {node_id} "
                f"'note <content>'  (or set/thought/payload as needed)")
    return ("python3 extensions/agi/bin/write.py <node-id> "
            "'note <content>'  # find the node id in the file")


def cmd_check(argv: list[str]) -> int:
    strict = "--strict" in argv
    explicit_root = None
    rest = []
    i = 0
    while i < len(argv):
        if argv[i] == "--root" and i + 1 < len(argv):
            explicit_root = argv[i + 1]
            i += 2
        elif argv[i].startswith("--root="):
            explicit_root = argv[i][len("--root="):]
            i += 1
        else:
            rest.append(argv[i])
            i += 1

    if explicit_root:
        root = Path(explicit_root).resolve()
    else:
        root = find_project_root()
    if root is None:
        print("write_guard: not in an agi project", file=sys.stderr)
        return 2 if strict else 0
    root = Path(root)

    log_data = _load_log(root)
    san, sha_to_path = log_data
    changes = _git_changed_files(root, root)
    warnings = []

    def _node_mint_id(abspath: str) -> str:
        """Read the changed node's mint_id from its frontmatter, if any."""
        try:
            text = Path(abspath).read_text(encoding="utf-8", errors="replace")
            parts = text.split("---", 2)
            if len(parts) < 3 or not text.startswith("---"):
                return ""
            import yaml
            fm = yaml.safe_load(parts[1]) or {}
            return str(fm.get("mint_id", "") or "")
        except BaseException:
            return ""

    for c in changes:
        sha = c.get("old_sha256", "")
        fpath = c.get("path", "")
        # Sanctioned check keys on (mint_id, sha256), falling back to sha-only.
        # A clean git mv / retitle of a logged node keeps its mint_id, so it
        # stays silent; a hand edit changes the bytes, so it warns (SETTLED).
        mi = _node_mint_id(c.get("abspath", ""))
        if not san.has(mi, sha) and sha:
            hint = _redo_hint(fpath, root)
            warnings.append(f"WARN unsanctioned write: {fpath}")
            warnings.append(f"  {hint}")

    # Second pass: unsanctioned writes under .agi/context/ (l3w4). These are
    # design docs, not node files, so they carry no mint_id frontmatter; a
    # sanctioned payload write is matched by sha256 alone, exactly like the
    # SETTLED rekey fallback above. .agi/context/schemas/*.md are exempt:
    # they are engine configuration versioned by git, have no node type, and
    # nothing can sanely claim them, so a legit edit must not WARN (l3w4
    # FOLLOW-UP).
    for c in _git_changed_files(root, root, subdir="context"):
        sha = c.get("old_sha256", "")
        fpath = c.get("path", "")
        if "/schemas/" in fpath:
            continue  # engine config under .agi/context/schemas/ — git-versioned
        if not san.has("", sha) and sha:
            warnings.append(f"WARN unsanctioned write under .agi/context/: {fpath}")
            warnings.append(
                f"  python3 extensions/agi/bin/write.py <doc-node-id> "
                f"'payload {fpath}'  # or write.py create doc <slug> ...")


    # Check payload files of modified build nodes
    try:
        payloads = _read_payload_refs(root)
    except BaseException:
        payloads = []
    # Get currently changed files by checking build node files in _git_changed_files
    changed_node_ids = set()
    for c in changes:
        fpath = c.get("path", "")
        parts = Path(fpath).parts
        for i, part in enumerate(parts):
            if part == "nodes" and i + 2 < len(parts):
                slug = parts[i + 2].replace(".md", "")
                node_type = parts[i + 1]
                changed_node_ids.add(f"{node_type}:{slug}")

    for p in payloads:
        if p["node_id"] in changed_node_ids:
            sha = p.get("sha256", "")
            if not san.has(p.get("mint_id", ""), sha) and sha:
                warnings.append(
                    f"WARN unsanctioned write to payload of {p['node_id']}: "
                    f"{p['ref']}")
                warnings.append(
                    f"  python3 extensions/agi/bin/write.py {p['node_id']} "
                    f"payload {p['ref']}")

    for w in warnings:
        print(w, file=sys.stderr if strict else sys.stdout)

    if warnings and strict:
        return 1
    return 0


def cmd_hook(argv: list[str]) -> int:
    print("""#!/bin/sh
# write_guard pre-commit hook — reject unsanctioned node writes
cd "$(git rev-parse --show-toplevel)" || exit 1
exec python3 extensions/agi/bin/write_guard.py check --strict
""".lstrip("\n"))
    return 0


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 0
    if argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[0]
    rest = argv[1:]
    if cmd == "check":
        return cmd_check(rest)
    if cmd == "hook":
        return cmd_hook(rest)
    print(f"write_guard: unknown command {cmd!r}. check | hook", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())