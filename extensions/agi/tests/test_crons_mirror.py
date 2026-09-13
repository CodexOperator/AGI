"""Tests for the grid_sync town MIRROR — item 2 of the I-3a-2 order
(hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-
tuples-and-the-mirror-line-lands-inert, region C).

When `cadences.grid_sync.mirror_towns` is true, `render_managed_lines`
appends one GUARDED push per declared town, publishing every
`refs/heads/<town>/*` to `refs/agi/<town>/*` — NEVER to `refs/heads`. The
guard (`git for-each-ref refs/heads/<town>/ | grep -q .`) runs before the
push, so with no `<town>` refs the line is a byte-for-byte NO-OP: rc 0,
nothing pushed, nothing logged — the live state today.

Every test runs the REAL rendered guard line through `bash -c` against a
fixture git repo + a fake bare origin, and asserts the outcome by
`git ls-remote` on the fake origin. No test touches the real crontab, the
real crons node, or any real origin. `HOME` is redirected into `tmp_path` so
the rendered `>> <log>` appends land in the test sandbox.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import crons  # noqa: E402


def _git(path: Path, *args: str) -> str:
    res = subprocess.run(["git", *args], cwd=path, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {args} in {path}: {res.stderr}")
    return res.stdout.strip()


def _git_init(path: Path, branch: str = "master") -> None:
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q", "-b", branch)
    _git(path, "config", "user.email", "test@example.com")
    _git(path, "config", "user.name", "test")
    (path / ".keep").write_text("x")
    _git(path, "add", ".")
    _git(path, "commit", "-q", "-m", "init")


def _bare(tmp_path: Path, name: str = "origin") -> Path:
    b = tmp_path / name
    b.mkdir(parents=True)
    _git(b, "init", "-q", "--bare")
    return b


def _ls_remote(bare: Path) -> list[str]:
    """Full `git ls-remote` ref list of the fake bare origin (HEAD included;
    callers filter by refs/...)."""
    res = subprocess.run(["git", "ls-remote", str(bare)],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git ls-remote {bare}: {res.stderr}")
    return [line.split("\t")[1] for line in res.stdout.splitlines() if line]


def _mirror_cadences():
    return {
        "grid_sync": {"every_mins": 5, "enabled": True, "mirror_towns": True},
        "publish_engine": {"schedule": "37 * * * *", "enabled": False},
        "engine_push": {"schedule": "47 * * * *", "enabled": False},
    }


def _write_crons_node(root: Path, cadences=None) -> None:
    p = root / crons.CRONS_NODE_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = {
        "id": "cron:crons",
        "type": "cron",
        "crons_live": True,
        "cadences": cadences or _mirror_cadences(),
    }
    p.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\nBody.\n")


def _write_ladder(root: Path, towns: list[str]) -> Path:
    lp = root / "nodes/.geometry/ladder.md"
    lp.parent.mkdir(parents=True, exist_ok=True)
    lp.write_text("---\ntowns:\n" + "\n".join(f"  - {t}" for t in towns)
                  + "\n---\n\nladder body\n")
    return lp


def _setup(tmp_path: Path, monkeypatch, towns=("core",)):
    """A fixture project (legacy layout: root IS the graph dir) + a git repo
    + a fake bare origin, with the crons node declaring the mirror and the
    ladder naming the towns. `HOME` is sandboxed so rendered `>> <log>`
    appends stay inside tmp_path. Returns (root, repo_root, bare, mirror_cmd)."""
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / "logs").mkdir(exist_ok=True)  # the rendered `>> <log>` parent
    root = tmp_path / "proj"
    root.mkdir(parents=True)
    (root / "agi-tree.config.json").write_text("{}")
    _write_crons_node(root)
    _write_ladder(root, list(towns))
    # root IS both the graph dir and the git repo (legacy/make_project shape:
    # project root resolves as the repo_root for the crontab).
    _git_init(root)
    bare = _bare(tmp_path)
    _git(root, "remote", "add", "origin", str(bare))
    _git_init(root / "agi", branch="master")  # engine clone par

    _, cfg, repo_root, engine_root, node = crons._resolve(root)
    assert repo_root == root
    mirror = [
        l for l in crons.render_managed_lines(root, repo_root, engine_root, node)
        if "for-each-ref" in l and "refs/agi/" in l
    ]
    return root, repo_root, engine_root, node, bare, mirror


def _cmd(line: str) -> str:
    """Strip the 5-field schedule prefix, leaving `cd <root> && ...`."""
    return line.split(" ", 5)[5]


def _run(cmd: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["bash", "-c", cmd], capture_output=True, text=True,
                          cwd=str(cwd))


# --- the three claims ---------------------------------------------------


def test_guard_is_a_no_op_when_no_town_refs(tmp_path, monkeypatch):
    root, repo_root, engine_root, node, bare, mirror = _setup(tmp_path, monkeypatch)
    # towns declared (core only) but no refs/heads/core/* exists anywhere:
    # the rendered guard must do NOTHING — rc 0, origin ref list unchanged,
    # and refs/heads/* on origin untouched (there are none).
    assert len(mirror) == 1
    before = _ls_remote(bare)
    assert before == []

    res = _run(_cmd(mirror[0]), root)
    assert res.returncode == 0
    assert _ls_remote(bare) == []


def test_guard_pushes_only_under_refs_agi(tmp_path, monkeypatch):
    root, repo_root, engine_root, node, bare, mirror = _setup(tmp_path, monkeypatch)
    # Land a real refs/heads/core/main on the LOCAL repo and push it to the
    # fake origin once (so the origin already holds refs/heads/core/main) —
    # then the mirror guard must push a SECOND copy under refs/agi/core/main
    # ONLY: refs/heads/core/main stays, and no new refs/heads/* appears.
    _git(root, "checkout", "-q", "-b", "core/main")
    (root / "patch.txt").write_text("x")
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "core main")
    _git(root, "push", "-q", "origin", "core/main")
    assert "refs/heads/core/main" in _ls_remote(bare)

    res = _run(_cmd(mirror[0]), root)
    assert res.returncode == 0

    refs = [r for r in _ls_remote(bare) if r.startswith("refs/")]
    heads = sorted(r for r in refs if r.startswith("refs/heads/"))
    agis = sorted(r for r in refs if r.startswith("refs/agi/"))
    # refs/heads/core/main STILL exists and is the ONLY refs/heads/*.
    assert heads == ["refs/heads/core/main"]
    # the town branch landed under the hidden namespace, exactly one ref.
    assert agis == ["refs/agi/core/main"]


def test_guard_shape_is_pinned(tmp_path, monkeypatch):
    root, repo_root, engine_root, node, bare, mirror = _setup(tmp_path, monkeypatch)
    line = mirror[0]
    # A single cron line, grid_sync cadence, cd-into-root first.
    assert "\n" not in line
    assert line.startswith("*/5 * * * *")
    assert f"cd {root} &&" in line
    # The for-each-ref GUARD comes strictly BEFORE the push.
    i_guard = line.index("for-each-ref")
    i_push = line.index("push -q origin")
    assert i_guard < i_push
    # The push refspec is town-scoped and targets ONLY the hidden namespace.
    assert "'refs/heads/core/*:refs/agi/core/*'" in line
    assert "::refs/heads/" not in line
    assert ":refs/heads/" not in line


def test_load_crons_node_parses_mirror_towns(tmp_path):
    root = tmp_path / "proj"
    root.mkdir(parents=True)
    _write_crons_node(root)
    node = crons.load_crons_node(root)
    assert node["jobs"]["grid_sync"]["mirror_towns"] is True


def test_mirror_towns_absent_defaults_to_false(tmp_path):
    root = tmp_path / "proj"
    root.mkdir(parents=True)
    cad = _mirror_cadences()
    del cad["grid_sync"]["mirror_towns"]
    _write_crons_node(root, cad)
    node = crons.load_crons_node(root)
    assert node["jobs"]["grid_sync"].get("mirror_towns") is False


def test_mirror_towns_non_bool_refused(tmp_path):
    root = tmp_path / "proj"
    root.mkdir(parents=True)
    cad = _mirror_cadences()
    cad["grid_sync"]["mirror_towns"] = "yes"
    _write_crons_node(root, cad)
    with pytest.raises(crons.CronsError, match="mirror_towns"):
        crons.load_crons_node(root)