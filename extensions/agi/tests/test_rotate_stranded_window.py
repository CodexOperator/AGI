"""a skipped rotate join leaves NO stranded successor window
(hypothesis:a-skipped-rotate-join-leaves-no-stranded-window).

Measured (seq 348): the rotate-self handoff spawned the successor window, the
bounded JOIN found no registry file, the rotation recorded `skipped` and
returned rc 1 -- leaving the successor window ALIVE under the bare post name,
where it swallowed Remote Control dms meant for the live post.

The build: on the not-found join branch the successor window is torn down by
its captured @id with the SAME `_kill_window` the reap-by-@id path uses, and
`handover["stranded"]` records the action. A FOUND join never reaches the
branch, so it is byte-for-byte unchanged (falsifier 2).

No real tmux: the `--window-path` seam file stands in for `list-windows`.
"""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import heal  # noqa: E402
import rotate  # noqa: E402


@pytest.fixture
def _fix(tmp_path, monkeypatch):
    monkeypatch.setattr(rotate, "DEFAULT_AFTER_JOIN_TIMEOUT_S", 0)
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "load_ladder_field",
                        lambda r, f, d: 0.25 if f == "director_rotate_at"
                        else d)
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent: {brief_file: extensions/agi/briefs/parent-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n---\n\nbody\n",
        encoding="utf-8")
    (g / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        '  - {"name": "adv-alive", "role": "parent", "model": "x", '
        '"effort": "max", "settings": ""}\n---\n', encoding="utf-8")
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    return root


class _FakeTmux:
    """Window-name FILE as `tmux list-windows`; the spawn appends a NEW
    @id line for the successor, exactly as a real spawn would."""

    def __init__(self, tmp_path, initial=("@9 adv-alive",)):
        self.win = tmp_path / "windows.txt"
        self.win.write_text("\n".join(initial) + "\n", encoding="utf-8")

    def fake_spawn(self, **kw):
        with open(self.win, "a", encoding="utf-8") as fh:
            fh.write(f"@10 {kw['name']}\n")
        return 0, "echo hi"

    def names(self):
        return [ln.split(" ", 1)[1] for ln in
                self.win.read_text(encoding="utf-8").splitlines() if ln]


def _args(tmp_path, ft, reg, poll):
    return SimpleNamespace(
        name="adv-alive", force=False, timeout=5, debug_file=None,
        model=None, effort=None, settings=None, prompt_file=None,
        tmux_session="t", window_path=str(ft.win), dry_run=False,
        throwaway=False, successor_argv=None, role="parent", session_ref=None,
        successor_transcript=None, own_pid=None, belam_prefix=None,
        ask_diff=False, stops=None, stops_file=None, template=None,
        comms_root=None, in_flight=None, trigger=None,
        grid_commit_legal=False, grid_commit_branch=None,
        verification_argv=None, registry_dir=str(reg), registry_poll=poll,
        after_join=False, own_chain=None, view_path=None, prepare=False)


def _record(root):
    rot = root / "sessions" / "rotations"
    recs = sorted(rot.glob("adv-alive.*.json"))
    assert recs, f"no rotation record under {rot}"
    return json.loads(recs[-1].read_text(encoding="utf-8"))


def test_not_found_join_tears_the_successor_window_down(_fix, tmp_path,
                                                        monkeypatch):
    """FALSIFIER 1: an empty registry dir + the fake runner. rc 1, result
    `skipped`, the successor window GONE from the window list, and the ONE new
    field names the action."""
    reg = tmp_path / "reg"
    reg.mkdir()                       # EMPTY: the join can never match
    ft = _FakeTmux(tmp_path)
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    rc = rotate.cmd_rotate_self(_args(tmp_path, ft, reg, 0), tmp_path)
    assert rc == 1
    assert "adv-alive" not in ft.names(), (
        f"stranded successor window survives: {ft.names()}")
    rec = _record(tmp_path)
    assert rec["result"] == "skipped"
    assert "registry file for @10" in rec["refusal_reason"]
    st = rec["handover"]["stranded"]
    assert st["action"] == "killed"
    assert st["window"] == "adv-alive" and st["id"] == "@10"


def test_found_join_is_unchanged_and_claims_no_cleanup(_fix, tmp_path,
                                                       monkeypatch):
    """FALSIFIER 2: a registry file that DOES match the successor's @id takes
    the success branch -- record `success`, and NO `stranded` field, so the
    found path is byte-for-byte what it was."""
    reg = tmp_path / "reg"
    reg.mkdir()
    (reg / "4242.json").write_text(json.dumps({
        "session_id": "sid-adv", "cwd": "/home/u/adv", "name": "adv-alive",
        "tmux": "t:@10.%10"}), encoding="utf-8")
    ft = _FakeTmux(tmp_path)
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": "adv-alive", "gen_after": 1,
                         "answer": "continue", "session_ref": ""})
    rc = rotate.cmd_rotate_self(_args(tmp_path, ft, reg, 3), tmp_path)
    assert rc == 0
    rec = _record(tmp_path)
    assert rec["result"] == "success"
    assert "stranded" not in rec["handover"]
    assert "@10 adv-alive" in ft.win.read_text(encoding="utf-8")


@pytest.mark.parametrize("disp", ["error", "already_gone"])
def test_record_is_written_first_and_names_what_the_kill_did(
        _fix, tmp_path, monkeypatch, disp):
    """Row 34 flags first: at kill time the record ALREADY exists (`pending`);
    after it the record carries the helper's real disposition, never a
    constant `killed`; a non-killed window stays listed (truth, not claim)."""
    reg = tmp_path / "reg"
    reg.mkdir()
    ft = _FakeTmux(tmp_path)
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    seen = []

    def _kill(name, sess, wp=None, window_id=None):
        seen.append(_record(tmp_path)["handover"]["stranded"]["action"])
        return disp
    monkeypatch.setattr(rotate, "_kill_window", _kill)
    assert rotate.cmd_rotate_self(_args(tmp_path, ft, reg, 0), tmp_path) == 1
    assert seen == ["pending"]
    assert _record(tmp_path)["handover"]["stranded"]["action"] == disp
    assert "adv-alive" in ft.names()


def test_heal_late_reap_skips_a_torn_down_successor_only(_fix, tmp_path):
    """A `killed` successor is never late-reaped (its registry file is stale
    and the predecessor chain would go with it); `already_gone`/`error` keep
    heal's bounded late-reap recovery (`waiting` inside the bound)."""
    reg = tmp_path / "reg"
    reg.mkdir()
    rec = {"result": "skipped", "seat": "adv-alive",
           "refusal_reason": "no registry file for @10",
           "recorded_at": "2999-01-01T00:00:00+00:00",
           "handover": {"own_window": {"name": "adv-alive.prev"},
                        "successor_window": {"id": "@10", "name": "adv-alive"}}}
    def run(action):
        rec["handover"]["stranded"] = {"action": action}
        return heal._late_reap_for_skipped(
            tmp_path, rec, registry_dir=str(reg), rot=rotate)["action"]
    assert run("killed") == "skip"
    assert run("already_gone") == run("error") == "waiting"
