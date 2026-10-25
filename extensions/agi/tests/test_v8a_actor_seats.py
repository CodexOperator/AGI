"""goal:g7.16.1.11.46.23 V8a tip 2a: the two small library names that left write.py.

`write._default_actor` moved to `geometry_config.default_actor` and `write._load_seats`
callers read `geometry_config.load_rows` directly. Proves, on fixtures only:
  * a DIFFERENTIAL: the new `default_actor` agrees with a verbatim copy of the old
    `write._default_actor` body on every environment shape the old one had a branch for;
  * the caller grep: no live (non-test) module outside write.py reaches `write._load_seats`
    or `write._default_actor`; its MUTANT (a planted caller) reads RED.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import geometry_config  # noqa: E402
import locations  # noqa: E402


def _old_default_actor(root=None) -> str:
    """The pre-V8a write._default_actor body, verbatim (the oracle)."""
    actor = os.environ.get("AGI_ACTOR") or geometry_config.resolved_seat_env()
    if actor:
        return actor
    user = os.environ.get("USER")
    if not user:
        return "unknown"
    try:
        if root is None:
            root = locations.find_project_root(Path.cwd())
        rows = geometry_config.load_rows(root) if root is not None else []
        if not rows or any(r.get("name") == user for r in rows):
            return "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"
    return user


def _graph(tmp_path, names):
    g = tmp_path / ".agi" / "nodes" / ".geometry"
    g.mkdir(parents=True)
    body = "".join(f'  - {{"name": "{n}", "role": "kid"}}\n' for n in names)
    (g / "posts.md").write_text(
        "---\nid: config:posts\nmint_id: 11111111111111111111111111111111\ntype: config\n"
        f"parents: []\nposts:\n{body}---\n# posts\n", encoding="utf-8")
    return tmp_path / ".agi"


CASES = [  # (AGI_ACTOR, AGI_POST, USER, rows) -- every branch of the old body
    ("owner", None, "x", ["a"]),            # AGI_ACTOR wins
    (None, "belam", "x", ["a"]),            # the resolved seat
    (None, None, None, ["a"]),              # no USER -> unknown
    (None, None, "alice", ["a", "b"]),      # a user that is no post's name -> the user
    (None, None, "a", ["a", "b"]),          # a user that IS a post's name -> unknown
    (None, None, "alice", []),              # no rows -> fail closed
]


@pytest.mark.parametrize("actor,post,user,rows", CASES)
def test_default_actor_agrees_with_the_old_body(tmp_path, monkeypatch, actor, post, user, rows):
    root = _graph(tmp_path, rows) if rows else tmp_path / ".agi"
    for k, v in (("AGI_ACTOR", actor), ("AGI_POST", post), ("USER", user)):
        if v is None:
            monkeypatch.delenv(k, raising=False)
        else:
            monkeypatch.setenv(k, v)
    assert geometry_config.default_actor(root) == _old_default_actor(root)


def test_default_actor_no_root_fails_closed(tmp_path, monkeypatch):
    monkeypatch.delenv("AGI_ACTOR", raising=False)
    monkeypatch.delenv("AGI_POST", raising=False)
    monkeypatch.setenv("USER", "alice")
    monkeypatch.chdir(tmp_path)  # no .agi above: the root cannot resolve
    assert geometry_config.default_actor() == _old_default_actor() == "unknown"


_CALLER = re.compile(r"(?<![A-Za-z_])(?:write|_w|write_mod)\._(?:load_seats|default_actor)\(")


def _callers(files):
    hits = []
    for f in files:
        if f.name == "write.py":
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if _CALLER.search(line) and not line.lstrip().startswith("#"):
                hits.append(f"{f.name}:{i}")
    return hits


def _live_files():
    root = BIN.parents[2]
    out = subprocess.run(["git", "-C", str(root), "ls-files", "extensions/agi/bin", "extensions/agi/src"],
                         capture_output=True, text=True, check=True).stdout.split()
    return [root / p for p in out if p.endswith(".py")]


def test_no_live_caller_of_the_moved_names():
    assert _callers(_live_files()) == []


def test_the_caller_grep_mutant_reads_red(tmp_path):
    planted = tmp_path / "planted.py"
    planted.write_text("import write as _w\nrows = _w._load_seats(root)\n", encoding="utf-8")
    assert _callers([planted]) == ["planted.py:2"]
