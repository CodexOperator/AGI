"""goal:g7.16.1.7.1.1.3 (goal:g6.41.1 P2): a dead post RESUMES its own session.

heal._recover_seat resumes a dead seat whose row carries a session_id with a
transcript under the seat's tree: `--resume <sid>` from the harness template,
the row's model, the SAME name and generation, the session_id kept on the row.
Without a transcript it is today's fresh spawn. A harness whose template has
no resume slot refuses by name rather than fresh-spawning under a resume.
Every launch goes to a fake launcher; no tmux is touched.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
SID = "0f0f0f0f-1111-2222-3333-444444444444"
ROW = {"name": "mainseat", "role": "director", "pid": 111, "worktree": "",
       "model": "claude-opus-5-5", "effort": "high", "generation": 4,
       "session_id": SID, "recover": True}


def _seed_recovery_ack(gdir):
    """config:rotations `recovery_ack` -- the recovered-seat ack wording
    (hypothesis:heal-ack-line-comes-from-config-rotations-by-role)."""
    geo = Path(gdir) / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\nrecovery_ack:\n"
        "  prime_director: {recovered: \"RECOVERED SEAT {seat} --gen {gen}\","
        " resumed: \"RESUMED SEAT {seat} --gen {gen}\"}\n"
        "  default: {recovered: \"RECOVERED SEAT {seat}\","
        " resumed: \"RESUMED SEAT {seat}\"}\n---\n")


def _recover(tmp_path, monkeypatch, *, transcript: bool, row=None):
    rotate = _load("rotate")
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    _seed_recovery_ack(gdir)
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "projects")
    tree = heal._seat_tree_dir(gdir, {"worktree": ""})
    if transcript:
        tp = Path(rotate.transcript_from_registry_dict(
            {"cwd": str(tree), "session_id": SID}))
        tp.parent.mkdir(parents=True, exist_ok=True)
        tp.write_text("{}\n")
    seen: list = []

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append((name, shell_cmd))
        return None, "@9"

    wf = tmp_path / "w.txt"
    wf.write_text("\n")
    out = heal._recover_seat(gdir, dict(row or ROW), "pid gone", rotate,
                             windows=[], window_path=str(wf),
                             launcher=launch, now=0.0)
    return out, seen


def test_a_dead_post_with_a_transcript_resumes_the_same_session(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, transcript=True)
    assert out["respawned"] and out["resumed"] is True, out
    assert out["generation"] == 4 and out["name"] == "mainseat", out   # same gen, same name
    (_name, cmd), = seen
    assert f"--resume {SID}" in cmd and "--model claude-opus-5-5" in cmd, cmd
    assert "RESUMED SEAT" in cmd, cmd


def test_no_transcript_is_a_fresh_spawn(tmp_path, monkeypatch):
    out, seen = _recover(tmp_path, monkeypatch, transcript=False)
    assert out["respawned"] and out["resumed"] is False, out
    assert out["generation"] == 5, out   # the fresh rule: generation + 1
    (_name, cmd), = seen
    assert "--resume" not in cmd, cmd


def test_a_harness_without_a_resume_slot_refuses_by_name():
    rotate = _load("rotate")
    try:
        rotate._build_harness_command("copilot-cli", name="n", prompt_text="p",
                                      debug_file="d", resume=SID)
    except rotate.harness_template.HarnessTemplateError as exc:
        assert "no resume slot" in str(exc)
    else:
        raise AssertionError("a resume on a slot-less harness built an argv")
