#!/usr/bin/env python3
"""node_read.py <id> section <heading> | lines A:B -- read ONE slice of a tracked node file or a build node's payload.

goal:g7.16.1.11.46.23 3b (council decision alive 01:20:03Z 10-26, 3/3): the first_turn executor admits a producing
command only from {python3 <engine script>, git <read-only subcommand>, tmux, ps, curl}; `sed`, `cat` and `git show`
are refused as a first stage on purpose ("git log -p -- .env" once printed a tracked file into a successor's startup).
The retired write.py `read body|payload N:M` was the reader those four rotations.md exec lines (facts, skills) used;
this is its replacement. The judge admits ANY `python3 extensions/..` script and never reads its arguments, so THIS
file's refusals are the whole of the guard. It writes nothing, imports no engine module, and runs ONE fixed subprocess.

  node_read.py config:rotations section facts          the `## facts` heading through the line before the next heading
  node_read.py build:skills-agi-send-SKILL.md lines 2:7   lines 2..7 of the build node's payload (FILE-relative)

WHAT IS READ. The id (`<type>:<name>`) resolves to `.agi/nodes/<dir>/<name>.md` (config: -> `.geometry`; the retired
sibling `deprecated/<dir>/` second). A `build:` node is read through its `payload_ref` (else `link_ref`; relative to the repo root, the
default `location: source_root`); every other node is read as the file itself. `lines A:B` counts FILE lines of that
target, 1-based, inclusive, never body-relative. `section H` is the heading line whose text is H (any `#` level) through
the line before the next heading of the same or a higher level, TRAILING BLANK LINES DROPPED; a `#` line inside a
fenced code block is not a heading.

REFUSED (rc 1, ONE line `node_read: <why> <id>` on stdout, nothing else printed; never an empty print with rc 0):
  R1 the REALPATH of the node file and of the payload target (symlinks followed) is not under <repo>/.agi/nodes or
     <repo>/skills.  R2 the id is not `<type>:<name>` (no '/', no '..', no NUL, no space).  R3 the target is not
     TRACKED: `env GIT_LITERAL_PATHSPECS=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C <repo> ls-files
     --error-unmatch -- <path>` (argv fixed, no shell, after R1) fails, or cannot run (no git, not a repo, timeout):
     an ignored or untracked file (the .env class) never prints.  R4 the id does not resolve, a heading is not found
     or is found TWICE, a range is empty or past the end of the file, the file is not UTF-8.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ID_RE = re.compile(r"^([a-z][a-z0-9_]*):([A-Za-z0-9][A-Za-z0-9._@+-]*)$")
HOMES = {"config": ".geometry"}
GIT_TIMEOUT_S = 10


class Refused(Exception):
    pass


def _within(path: Path, *bases: Path) -> bool:
    return any(path == b or b in path.parents for b in bases)


def _allowed_bases() -> tuple:
    return (ROOT.resolve() / ".agi" / "nodes", ROOT.resolve() / "skills")


def check_id(node_id: str) -> tuple:
    if "\x00" in node_id or ".." in node_id or "/" in node_id:
        raise Refused("id must be <type>:<name> with no '/', '..' or NUL")
    m = ID_RE.match(node_id)
    if not m:
        raise Refused("id must be <type>:<name>")
    return m.group(1), m.group(2)


def node_file(node_type: str, name: str) -> Path:
    nodes = ROOT / ".agi" / "nodes"
    home = HOMES.get(node_type, node_type)
    for parent in (nodes, nodes / "deprecated"):
        p = parent / home / f"{name}.md"
        if os.path.lexists(p):          # a dangling link is a found-but-unreadable node, refused below, not "unresolved"
            return p
    raise Refused("does not resolve to a node file")


def payload_ref(node_text: str) -> str | None:
    """The build node's `payload_ref`, else its `link_ref` (a few prose build nodes carry only that one)."""
    head = node_text.split("\n---", 1)[0] if node_text.startswith("---") else ""
    for key in ("payload_ref", "link_ref"):
        m = re.search(rf"^{key}:[ \t]*(.+?)[ \t]*$", head, re.M)
        if m:
            v = m.group(1)
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                v = v[1:-1]
            return v
    return None


def contained(path: Path) -> Path:
    """The realpath of `path` (symlinks followed), or Refused when it is outside .agi/nodes and skills."""
    try:
        real = Path(os.path.realpath(path, strict=True))
    except (OSError, RuntimeError):
        raise Refused("target is missing or a dangling link")
    if not _within(real, *_allowed_bases()):
        raise Refused("resolves outside .agi/nodes|skills")
    if not real.is_file():
        raise Refused("target is not a regular file")
    return real


def tracked(real: Path) -> None:
    rel = real.relative_to(ROOT.resolve())
    env = {"PATH": os.environ.get("PATH", ""), "GIT_LITERAL_PATHSPECS": "1", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": "/dev/null", "LC_ALL": "C"}
    try:
        r = subprocess.run(["git", "-C", str(ROOT.resolve()), "ls-files", "--error-unmatch", "--", str(rel)],
                           env=env, stdin=subprocess.DEVNULL, capture_output=True, timeout=GIT_TIMEOUT_S)
    except (OSError, subprocess.SubprocessError):
        raise Refused("cannot check that the target is tracked (git did not run)")
    if r.returncode != 0:
        raise Refused("target is not tracked by git")


def target(node_id: str) -> Path:
    node_type, name = check_id(node_id)
    nf = contained(node_file(node_type, name))
    tracked(nf)
    if node_type != "build":
        return nf
    try:
        text = nf.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        raise Refused("node file is not readable UTF-8")
    ref = payload_ref(text)
    if not ref:
        raise Refused("build node has no payload_ref or link_ref")
    real = contained(ROOT / ref if not os.path.isabs(ref) else Path(ref))
    tracked(real)
    return real


def _lines(real: Path) -> list:
    try:
        text = real.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        raise Refused("target is not readable UTF-8")
    return text.splitlines(keepends=True)


def section_span(lines: list, heading: str) -> tuple:
    """(start, end) 0-based, end exclusive, of the section whose heading text is `heading`: the heading line through the
    line before the next heading of the same or a higher level, trailing blank lines dropped. Lines may carry a
    trailing newline or not (rotate.facts_body_ranges asks with a body split on "\n"). Refused when the heading is
    absent or found more than once."""
    hit = []
    fence = False
    for i, ln in enumerate(lines):
        s = ln.rstrip("\n")
        if s.lstrip().startswith("```") or s.lstrip().startswith("~~~"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$", s)
        if m and m.group(2) == heading:
            hit.append((i, len(m.group(1))))
    if not hit:
        raise Refused(f"heading '{heading}' not found in")
    if len(hit) > 1:
        raise Refused(f"heading '{heading}' found {len(hit)} times in")
    start, level = hit[0]
    end = len(lines)
    fence = False
    for j in range(start + 1, len(lines)):
        s = lines[j].rstrip("\n")
        if s.lstrip().startswith("```") or s.lstrip().startswith("~~~"):
            fence = not fence
            continue
        m = None if fence else re.match(r"^(#{1,6})[ \t]+\S", s)
        if m and len(m.group(1)) <= level:
            end = j
            break
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    return start, end


def section(lines: list, heading: str) -> list:
    start, end = section_span(lines, heading)
    return lines[start:end]


def line_range(lines: list, spec: str) -> list:
    m = re.fullmatch(r"([0-9]+):([0-9]+)", spec)
    if not m:
        raise Refused(f"range '{spec}' must be A:B")
    a, b = int(m.group(1)), int(m.group(2))
    if a < 1 or b < a:
        raise Refused(f"range {a}:{b} is empty in")
    if b > len(lines):
        raise Refused(f"range {a}:{b} is past the end ({len(lines)} lines) of")
    return lines[a - 1:b]


def main(argv: list) -> int:
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    if len(argv) != 3 or argv[1] not in ("section", "lines"):
        print(__doc__, file=sys.stderr)
        print("usage: node_read.py <id> section <heading> | lines A:B", file=sys.stderr)
        return 2
    node_id, op, arg = argv
    try:
        lines = _lines(target(node_id))
        out = section(lines, arg) if op == "section" else line_range(lines, arg)
    except Refused as exc:
        print(f"node_read: {exc} {node_id}")
        return 1
    sys.stdout.buffer.write("".join(out).encode("utf-8"))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
