"""hypothesis:heal-ack-line-comes-from-config-rotations-by-role.

heal._recover_seat builds the recovered / resumed ack instruction from the
config:rotations `recovery_ack` cell keyed by the row's role (prime_director
vs every other role) and heal.py carries no ack text literal. The non-prime
tests pin the FIXTURE cell's arms (its non-prime recovered line has no `--gen`),
not the live cell: the LIVE default.recovered carries `--gen {gen}` (DH.1).
An absent cell refuses by name. Every launch goes to a fake launcher; fixture
roots only, no tmux, no live root.
"""
from __future__ import annotations

import importlib.util
import json
import re
import shlex
import sys
from types import SimpleNamespace
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
REPO = Path(__file__).resolve().parents[3]
LIVE_ROTATIONS = REPO / ".agi" / "nodes" / ".geometry" / "rotations.md"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
SID = "0f0f0f0f-1111-2222-3333-444444444444"
FIXTURE_CELL = """\
recovery_ack:
  prime_director:
    recovered: "FIXTURE-PRIME-RECOVERED {seat} gen={gen} --gen {gen} --ref <ref> continue"
    resumed: "FIXTURE-PRIME-RESUMED {seat} gen={gen} --gen {gen} --ref <ref> continue"
  default:
    recovered: "FIXTURE-OTHER-RECOVERED {seat} --post {seat} --ref <ref> continue"
    resumed: "FIXTURE-OTHER-RESUMED {seat} --post {seat} --ref <ref> continue"
"""


def _row(role, **kw):
    row = {"name": "mainseat", "role": role, "pid": 111, "worktree": "",
           "model": "claude-opus-5-5", "effort": "high", "generation": 4,
           "recover": True}
    row.update(kw)
    return row


def _recover(tmp_path, monkeypatch, row, *, cell=FIXTURE_CELL, transcript=False):
    rotate = _load("rotate")
    gdir = tmp_path / "main" / ".agi"
    geo = gdir / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\n" + cell + "---\n# fixture\n")
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "projects")
    if transcript:
        tree = heal._seat_tree_dir(gdir, {"worktree": ""})
        tp = Path(rotate.transcript_from_registry_dict(
            {"cwd": str(tree), "session_id": SID}))
        tp.parent.mkdir(parents=True, exist_ok=True)
        tp.write_text("{}\n")
        row = dict(row, session_id=SID)
    seen: list = []

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append(shell_cmd)
        return None, "@9"

    wf = tmp_path / "w.txt"
    wf.write_text("\n")
    out = heal._recover_seat(gdir, row, "pid gone", rotate, windows=[],
                             window_path=str(wf), launcher=launch, now=0.0)
    return out, seen


def test_prime_seat_is_told_its_line_with_gen(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, _row("prime_director"))
    assert out["respawned"], out
    (cmd,) = seen
    assert "FIXTURE-PRIME-RECOVERED" in cmd and "--gen 5" in cmd, cmd


def test_prime_seat_resumed_arm_is_its_own_cell(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, _row("prime_director"),
                         transcript=True)
    assert out["respawned"] and out["resumed"] is True, out
    (cmd,) = seen
    assert "FIXTURE-PRIME-RESUMED" in cmd and "--gen 4" in cmd, cmd


def test_fixture_non_prime_recovered_arm_is_what_heal_builds(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, _row("director"))
    assert out["respawned"], out
    (cmd,) = seen
    assert "FIXTURE-OTHER-RECOVERED mainseat --post mainseat" in cmd, cmd
    assert "--gen" not in cmd, cmd


def test_non_prime_seat_resumed_line_has_no_gen(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, _row("helper"), transcript=True)
    assert out["respawned"] and out["resumed"] is True, out
    (cmd,) = seen
    assert "FIXTURE-OTHER-RESUMED mainseat --post mainseat" in cmd, cmd
    assert "--gen" not in cmd, cmd


def test_missing_cell_refuses_by_name_and_launches_nothing(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, _row("director"),
                         cell="title: no cell here\n")
    assert out["respawned"] is False and seen == [], (out, seen)
    assert "recovery_ack" in out["reason"], out
    assert "rotations.md" in out["reason"], out


def test_heal_py_carries_no_ack_literal():
    src = (BIN / "heal.py").read_text(encoding="utf-8")
    assert "rotate.py ack" not in src
    assert "RECOVERED SEAT" not in src and "RESUMED SEAT" not in src
    i = src.index("def _recover_seat")
    body = src[i:src.index("\ndef ", i + 1)]
    assert not re.search(r"ack_gate\s*=\s*\(\s*\"", body), "ack_gate literal"


def test_live_config_rotations_holds_the_cell():
    rotate = _load("rotate")
    fm = rotate.frontmatter.load_node_file(LIVE_ROTATIONS).frontmatter
    cell = fm["recovery_ack"]
    for key in ("prime_director", "default"):
        for arm in ("recovered", "resumed"):
            assert cell[key][arm].strip(), (key, arm)
    assert "--gen {gen}" in cell["prime_director"]["recovered"]
    assert "--gen {gen}" in cell["default"]["recovered"]
    assert "--gen" not in cell["default"]["resumed"]


def _built_line_into_cmd_ack(tmp_path, monkeypatch, row, *, resumed):
    """Recover on a fixture root with the LIVE cell, then feed the BUILT ack
    line (parsed back out of the launch command) into rotate.cmd_ack."""
    gdir = tmp_path / "main" / ".agi"
    (gdir / "nodes" / ".geometry").mkdir(parents=True)
    (gdir / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    sch = gdir / "context" / "schemas"
    sch.mkdir(parents=True)
    (sch / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\nself_row: "
        "{list_key: seats, match_key: name, fields: [session_ref, session_name, "
        "session_id, generation, window, pid, session_label]}\n---\nbody\n",
        encoding="utf-8")
    (gdir / "sessions").mkdir()
    (gdir / "nodes" / ".geometry" / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n  - " + json.dumps(row)
        + "\n---\n", encoding="utf-8")
    out, seen = _recover(tmp_path, monkeypatch, row,
                         cell=LIVE_ROTATIONS.read_text(encoding="utf-8").split(
                             "---\n")[1].split("id: config:rotations\n")[1]
                         .split("type: config\n", 1)[-1], transcript=resumed)
    assert out["respawned"], out
    line = re.findall(r"python3 \S+rotate\.py ack [^`]*?continue", seen[0])[-1]
    tok = shlex.split(line.replace("<your ListAgents ref>", "refabc"))
    opt = dict(zip(tok[3:-1:2], tok[4:-1:2]))
    rotate = _load("rotate")
    reg = tmp_path / "empty-reg"
    reg.mkdir()
    return rotate.cmd_ack(SimpleNamespace(
        seat=opt.get("--seat") or opt.get("--post"),
        gen=int(opt["--gen"]) if "--gen" in opt else None, session=None,
        ref=opt["--ref"], answer="continue", text=None, no_commit=True,
        wait=0, registry_dir=str(reg)), gdir)


def test_built_ack_line_is_accepted_by_cmd_ack(tmp_path, monkeypatch, capsys):
    for n, (role, resumed) in enumerate([("director", False), ("helper", True),
                                         ("prime_director", False),
                                         ("prime_director", True)]):
        row = _row(role, name="mainseat")
        sub = tmp_path / str(n)
        rc = _built_line_into_cmd_ack(sub, monkeypatch, row, resumed=resumed)
        assert rc == 0, (role, resumed, capsys.readouterr().err)


def test_unusable_cell_refuses_by_name_to_stderr_and_log(tmp_path, monkeypatch,
                                                         capsys):
    log = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    for n, cell in enumerate([
            "recovery_ack: [unclosed\n",
            'recovery_ack: {default: {recovered: "a { b", resumed: "x"}}\n',
            'recovery_ack: {default: {recovered: "a {} b", resumed: "x"}}\n']):
        out, seen = _recover(tmp_path / str(n), monkeypatch, _row("director"),
                             cell=cell)
        assert out["respawned"] is False and seen == [], (n, out)
        assert "recovery_ack" in out["reason"], out
        assert "recovery_ack" in capsys.readouterr().err, n
    assert log.read_text(encoding="utf-8").count("recovery_ack") >= 3
