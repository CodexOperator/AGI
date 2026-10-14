"""`write.py create build --payload` sets build_kind (belam 10:4xZ (A), SM 10:5xZ, DG3).

The [build] schema is discriminated on `build_kind`; `write.py create` never set it, so a created build node
reached the spawn gate UNVERIFIED and the growth gate (`grow.py`, goal:g7.16.1.11.8) refuses an unverified new
node. The default is `level3.build_kind_for(<payload>)` -- the payload suffix, the rule level3.py already applies --
and an explicit `--set build_kind=...` WINS.

bk1  create build + a .py payload      -> build_kind: code, and the spawn gate APPROVES the minted node
bk2  create build + a .conf payload    -> build_kind: prose, APPROVED
bk3  an explicit build_kind=prose on a .py payload is kept (the explicit value wins)
bk4  create build WITHOUT a payload    -> no build_kind invented (nothing to derive it from); unchanged
bk5  a non-build create is untouched   -> no build_kind key
bk6  the REAL grow.py piece (engine-post.md, once it is on the tree) APPROVES the minted nodes on a temp index
bk7  `--dry-run` and the real create give the SAME verdict for a build with a payload: an illegal parent shape is
     rc 2 on both, a legal one rc 0 on both (the default is derived ONCE, in write._with_build_kind)

MUTANTS: (1) delete the `extra.setdefault("build_kind", ...)` default in write._with_build_kind -> bk1, bk2, bk6, bk7 RED (bk3 stays green);
(2) the default on the REAL path only (the dry-run judge not calling the helper) -> bk7 RED.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
BIN = ROOT / "extensions" / "agi" / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(ROOT / "extensions" / "agi" / "src"))

import spawn_gate  # noqa: E402
import write  # noqa: E402

GOAL = ('---\nid: goal:g1\ntype: goal\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1\nparents: []\ngoal_id: G1\n'
        'goal_kind: perpetual\nstatus: active\ntitle: "G1: a parent"\n---\n\n# goal:g1\n')
IDEA = ('---\nid: idea:i0\ntype: idea\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2\nparents:\n  - goal:g1\n---\n\n# idea:i0\n')
#: [build] is parent-shaped: [goal, idea] is a legal shape, [goal] alone is not (the four live nodes use this one)
PARENTS = ["goal:g1", "idea:i0"]


def _engine_post() -> Path:
    return Path(os.environ.get("GROW_ENGINE_POST") or ROOT / ".agi" / "nodes" / ".geometry" / "engine-post.md")


def _grow_piece() -> str | None:
    m = re.search(r"^### grow\.py \(\d+ B\)\n~~~\w*\n(.*?)\n~~~\n", _engine_post().read_text(encoding="utf-8"), re.S | re.M)
    return m.group(1) + "\n" if m else None


@pytest.fixture()
def scratch(tmp_path: Path) -> Path:
    """A scratch repo: the engine's own schemas, one parent goal, one idea, one baseline commit (only bk6 also copies the engine)."""
    t = tmp_path / "t"
    t.mkdir()
    shutil.copytree(ROOT / ".agi" / "context" / "schemas", t / ".agi" / "context" / "schemas")
    (t / ".agi" / "config.json").write_text("{}")
    (t / ".agi" / "nodes" / "goal").mkdir(parents=True)
    (t / ".agi" / "nodes" / "goal" / "g1.md").write_text(GOAL)
    (t / ".agi" / "nodes" / "idea").mkdir(parents=True)
    (t / ".agi" / "nodes" / "idea" / "i0.md").write_text(IDEA)
    g = ["git", "-C", str(t), "-c", "user.name=x", "-c", "user.email=x@x", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "init", "-q", str(t)], check=True)
    subprocess.run(g + ["add", "-A"], check=True)
    subprocess.run(g + ["commit", "-qm", "base"], check=True)
    return t


def _fm(path) -> dict:
    return yaml.safe_load(Path(path).read_text().split("\n---", 1)[0].split("---\n", 1)[1])


def _approved(t: Path, res) -> str:
    """The spawn gate's verdict on the minted node's own front matter (grow.py's predicate: APPROVED or refused)."""
    fm = _fm(res.path)
    rules, index, season = spawn_gate.gate_for_root(t / ".agi")
    r = spawn_gate.check_spawn(fm["type"], fm["parents"], rules=rules, type_index=index, fm=fm,
                               node_id=fm["id"], current_season=season)
    return r.status


def _create(t: Path, slug: str, payload: str | None, **kw):
    res, made = write.create(t / ".agi", "build", slug, PARENTS, payload=payload, **kw)
    assert res.written, (res.status, res.reason)
    return res, made


def test_bk1_a_code_payload_sets_build_kind_code_and_the_gate_approves(scratch):
    res, _ = _create(scratch, "bk1", "src/bk1.py")
    assert _fm(res.path)["build_kind"] == "code"
    assert _approved(scratch, res) == spawn_gate.APPROVED


def test_bk2_a_conf_payload_sets_build_kind_prose_and_the_gate_approves(scratch):
    res, _ = _create(scratch, "bk2", "etc/bk2.conf")
    assert _fm(res.path)["build_kind"] == "prose"
    assert _approved(scratch, res) == spawn_gate.APPROVED


def test_bk3_an_explicit_build_kind_wins(scratch):
    res, _ = _create(scratch, "bk3", "src/bk3.py", set_fm={"build_kind": "prose"})
    assert _fm(res.path)["build_kind"] == "prose", "the explicit --set build_kind must win over the payload suffix"


def test_bk4_no_payload_invents_no_build_kind(scratch):
    res, made = write.create(scratch / ".agi", "build", "bk4", PARENTS)
    assert res.written and made is None
    assert "build_kind" not in _fm(res.path)


def test_bk5_a_non_build_create_is_untouched(scratch):
    res, _ = write.create(scratch / ".agi", "idea", "i1", ["goal:g1"], payload="src/i1.py")
    assert res.written
    assert "build_kind" not in _fm(res.path)


@pytest.mark.skipif(_grow_piece() is None, reason="SKIPPED until goal:g7.16.1.11.8 lands: its '### grow.py' piece is not in engine-post.md on this tree (bk1/bk2 carry the same predicate in-process; GROW_ENGINE_POST=<engine-post.md> points this row at another tree's piece)")
def test_bk6_the_real_grow_piece_approves_a_created_build_node(scratch, tmp_path):
    for d in ("bin", "src"):   # grow.py runs from the scratch cwd and imports the engine from extensions/agi/<d>
        shutil.copytree(ROOT / "extensions" / "agi" / d, scratch / "extensions" / "agi" / d, ignore=shutil.ignore_patterns("__pycache__"))
    a, _ = _create(scratch, "bk6a", "src/bk6a.py")
    b, _ = _create(scratch, "bk6b", "etc/bk6b.conf")
    grow = tmp_path / "grow.py"
    grow.write_text(_grow_piece())
    ix = tmp_path / "ix"
    env = {**os.environ, "GIT_INDEX_FILE": str(ix)}
    tip = subprocess.run(["git", "-C", str(scratch), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "-C", str(scratch), "read-tree", tip], env=env, check=True)
    subprocess.run(["git", "-C", str(scratch), "add", "-A"], env=env, check=True)
    r = subprocess.run([sys.executable, "-B", str(grow), tip], cwd=scratch, env=env, capture_output=True, text=True)
    assert r.returncode == 0, f"grow.py refused a node write.py create minted: {r.stdout} {r.stderr}"
    assert "[growth-order]" not in r.stdout and "[spawn-gate" not in r.stdout


def test_bk7_dry_run_and_the_real_create_give_the_same_verdict(scratch, capsys):
    """SM 10:5xZ (2): `--dry-run` runs the same gates the real create runs; the build_kind default was only on the real path."""
    base = ["create", "build"]
    tail = ["--payload", "src/bk7.py", "--root", str(scratch)]
    # an illegal shape ([goal] alone): rc 2 on BOTH, the same rule named
    dry = write.main(base + ["bk7-bad", "--parent", "goal:g1"] + tail + ["--dry-run"])
    dry_err = capsys.readouterr().err
    real = write.main(base + ["bk7-bad", "--parent", "goal:g1"] + tail)
    real_err = capsys.readouterr().err
    assert (dry, real) == (2, 2), f"dry-run rc {dry}, real rc {real}: a preview must give the real verdict"
    assert "parent_shapes" in dry_err and "parent_shapes" in real_err
    assert not (scratch / ".agi" / "nodes" / "build" / "bk7-bad.md").exists()
    # a legal shape ([goal, idea]): rc 0 on BOTH; the dry run writes nothing, the real one does
    dry = write.main(base + ["bk7-ok", "--parent", "goal:g1", "--parent", "idea:i0"] + tail + ["--dry-run"])
    capsys.readouterr()
    assert dry == 0 and not (scratch / ".agi" / "nodes" / "build" / "bk7-ok.md").exists()
    real = write.main(base + ["bk7-ok", "--parent", "goal:g1", "--parent", "idea:i0"] + tail)
    capsys.readouterr()
    assert real == 0 and _fm(scratch / ".agi" / "nodes" / "build" / "bk7-ok.md")["build_kind"] == "code"
