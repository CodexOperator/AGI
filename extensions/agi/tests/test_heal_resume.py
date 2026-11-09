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


# ------------------------------- the row's harness on recover (goal:g7.16.1.7.1.1.5)
def _fresh_cmd(tmp_path, monkeypatch, **cells):
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    # The project declares copilot-cli, as the live config.json does, so the
    # recover's harness passes `_validate_harness` by name.
    (gdir / "config.json").write_text(
        '{"harnesses": {"copilot-cli": {"adapter": "copilot_cli"}}}')
    row = {k: v for k, v in ROW.items() if k != "harness"}
    row.update(cells)
    out, seen = _recover(tmp_path, monkeypatch, transcript=False, row=row)
    assert out["respawned"], out
    (_name, cmd), = seen
    return cmd


def test_a_copilot_row_recovers_on_the_copilot_template(tmp_path, monkeypatch):
    """RED before the fix: _recover_seat passed no harness= to spawn_window,
    so a copilot-cli seat came back as a CLAUDE argv."""
    cmd = _fresh_cmd(tmp_path, monkeypatch, harness="copilot-cli")
    argv = cmd.split(" -- ", 1)[1]          # after rotate.py launch-wrapper
    assert argv.startswith("copilot --model "), argv[:120]
    assert "--remote-control" not in argv, argv[:120]


def test_an_absent_or_empty_harness_renders_the_claude_argv_unchanged(tmp_path, monkeypatch):
    """The fix moves no live row: today's 45 rows are claude-code 38, absent 3,
    '' 4 (council 19:49Z 11-06). Absent and '' render byte-identical to an
    explicit claude-code row."""
    explicit = _fresh_cmd(tmp_path / "a", monkeypatch, harness="claude-code")
    absent = _fresh_cmd(tmp_path / "b", monkeypatch)
    empty = _fresh_cmd(tmp_path / "c", monkeypatch, harness="")
    norm = lambda c, d: c.replace(str(tmp_path / d), "<T>")   # noqa: E731
    assert explicit.split(" -- ", 1)[1].startswith("claude --remote-control "), explicit
    assert norm(absent, "b") == norm(explicit, "a") == norm(empty, "c")


# ------------------------------- the resume proof is template-declared (goal:g7.31.1.2 ACT 2c)
def _grok_recover(tmp_path, monkeypatch, heal_mod=heal):
    gdir = tmp_path / "main" / ".agi"
    gdir.mkdir(parents=True, exist_ok=True)
    (gdir / "config.json").write_text(
        '{"harnesses": {"grok-bot": {"adapter": "grok_bot", "model": "grok-4"}}}')
    lines: list = []
    monkeypatch.setattr(heal_mod, "_watch_log", lambda m: lines.append(m))
    rotate = _load("rotate")
    _seed_recovery_ack(gdir)
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "projects")   # no transcript anywhere
    seen: list = []

    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        seen.append((name, shell_cmd))
        return None, "@9"

    wf = tmp_path / "w.txt"
    wf.write_text("\n")
    row = dict(ROW, harness="grok-bot", model="grok-4")
    out = heal_mod._recover_seat(gdir, row, "pid gone", rotate, windows=[],
                                 window_path=str(wf), launcher=launch, now=0.0)
    return out, seen, lines


def test_a_grok_row_resumes_on_its_session_id_and_names_the_proof_PROVISIONAL(tmp_path, monkeypatch):
    """grok-bot.toml declares resume_proof = "session_id": the row's sid is
    resumed with NO transcript, and heal's log names the proof PROVISIONAL +
    UNMEASURED every time (council 11-06 19:49:54Z (A)(3)); never a pass."""
    out, seen, lines = _grok_recover(tmp_path, monkeypatch)
    assert out["respawned"] and out["resumed"] is True, out
    (_name, cmd), = seen
    argv = cmd.split(" -- ", 1)[1]
    assert f" -r {SID}" in argv and " -s " not in argv, argv[:200]
    prov = [m for m in lines if "resume proof PROVISIONAL" in m]
    assert prov == [f"watch: seat mainseat resume proof PROVISIONAL "
                    f"(session_id present; UNMEASURED): resuming {SID}"], lines


def test_the_claude_transcript_proof_is_unchanged_for_a_claude_row(tmp_path, monkeypatch):
    """The same row on claude-code with no transcript stays a FRESH spawn and
    logs no PROVISIONAL line: the default proof did not move."""
    lines: list = []
    monkeypatch.setattr(heal, "_watch_log", lambda m: lines.append(m))
    out, seen = _recover(tmp_path, monkeypatch, transcript=False,
                         row=dict(ROW, harness="claude-code"))
    assert out["resumed"] is False and "--resume" not in seen[0][1], out
    assert not any("PROVISIONAL" in m for m in lines), lines


def test_mutant_heal_reads_only_the_transcript_proof_RED_on_the_grok_row(tmp_path, monkeypatch):
    src = (BIN / "heal.py").read_text()
    old = '        if _proof == "session_id":\n'
    assert src.count(old) == 1
    d = tmp_path / "mut"
    d.mkdir()
    (d / "heal_mut.py").write_text(src.replace(old, '        if False:\n'))
    spec = importlib.util.spec_from_file_location("heal_mut", d / "heal_mut.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out, seen, _lines = _grok_recover(tmp_path, monkeypatch, heal_mod=m)
    assert out["resumed"] is False and " -r " not in seen[0][1]     # a fresh spawn: RED
