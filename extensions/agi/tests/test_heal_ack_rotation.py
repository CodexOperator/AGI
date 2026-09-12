"""GOAL:g15.25 (SL7.15) — the ack no-op is gen-aware, a completed rotation
rotates the ack file, and a heal crash-recovery still takes its identity.

The parent addendum measured two live defects on this base:
  (3) rotate.py cmd_ack `continue` no-op is GEN-BLIND — it returns 0 on
      `source == predecessor and answer == continue` WITHOUT comparing the
      ack file's `gen_after` to `--gen`, so a STALE prior-generation
      predecessor `continue` left on disk silences the NEXT generation's
      `ack --gen N+1 continue` and the recovered post never takes its
      identity (heal.py `_recover_seat`'s crash-recovery ack_gate is the
      L4.288 back-fill, reopened by SL7.06).
  (9) rotate.py `_derive_bootstrap_fact` `ack` key reads `row.get("ack")`,
      which no writer ever fills -> `ack: SKIPPED: seat row carries no ack`.

CLAIM PARTS BUILT + PROVED HERE:
  (a) cmd_ack `continue` no-ops ONLY when source==predecessor AND
      answer==continue AND gen_after == --gen; a predecessor answer for any
      OTHER generation is stale (prints `stale predecessor answer for gen N,
      this is gen M -- writing your continue`) and falls through to WRITE the
      successor's own ack.
  (b) a completed rotation ROTATES the ack file (`_rotate_ack_file` ->
      `seats/<seat>.ack.gen<N>.json`) — called in rotate-self's success path
      and in heal.py `_recover_seat` before spawning.
  (c) one end-to-end heal crash-recovery: predecessor continue on disk for
      gen N, crash-recovery respawn at gen N+1 — the recovered post's
      `ack --gen N+1 continue` WRITES (not no-op), back-fills session_ref, and
      the row carries the identity (taken).
  (d) the bootstrap `ack` fact derives from the ack FILE, never the row.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rotate = _load("rotate")
heal = _load("heal")


@pytest.fixture
def _fix(tmp_path, monkeypatch):
    """Fixture root (repo-root shape: nodes/, sessions/, context/schemas/,
    agi-tree.config.json marker) that both heal._recover_seat and
    rotate.cmd_ack resolve — never the live seats row."""
    root = tmp_path
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    schemas = root / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, "
        "fields: [session_ref, session_id, generation, window, pid]}\n"
        "---\nbody\n", encoding="utf-8")
    return root


def _write_seats(root, rows):
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _ack_path(root, seat):
    return root / "sessions" / "seats" / f"{seat}.ack.json"


def _predecessor_continue(root, seat, gen_after):
    p = _ack_path(root, seat)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({
        "seat": seat, "gen_after": gen_after, "answer": "continue",
        "source": "predecessor", "session_ref": "", "ts": "T",
        "text": ""}) + "\n", encoding="utf-8")
    return p


# --- part (a): the no-op is gen-aware ---------------------------------------

def test_cmd_ack_pred_continue_same_gen_still_noop(_fix, capsys):
    """A predecessor `continue` whose gen_after EQUALS --gen is STILL a no-op
    (SL7.06's contract kept — a successor re-running `ack continue` for the
    generation it already got has nothing to do)."""
    _write_seats(_fix, [{"name": "seat-a", "role": "parent"}])
    _predecessor_continue(_fix, "seat-a", 1)
    rc = rotate.cmd_ack(
        _ack_ns(gen=1, ref="r1"), _fix)
    assert rc == 0
    out = capsys.readouterr().out
    assert "already answered continue by your predecessor" in out
    ack = json.loads(_ack_path(_fix, "seat-a").read_text(encoding="utf-8"))
    assert ack["source"] == "predecessor" and ack["session_ref"] == ""


def test_cmd_ack_pred_continue_other_gen_is_stale_and_writes(_fix, capsys):
    """(a) A predecessor `continue` for a DIFFERENT generation is STALE: the
    no-op must NOT silence it — cmd_ack prints one line naming both
    generations and FALLS THROUGH to WRITE the successor's OWN ack (the 
    pre-SL7.06 path: write + ref back-fill). This is the recovered-post
    scenario: predecessor acked gen 4, the successor is gen 5."""
    _write_seats(_fix, [{"name": "seat-a", "role": "parent",
                         "session_ref": "",
                         "session_id": "", "window": "@77", "pid": 999999}])
    _predecessor_continue(_fix, "seat-a", 4)
    reg = _fix / "empty-reg"
    reg.mkdir()
    from types import SimpleNamespace
    rc = rotate.cmd_ack(SimpleNamespace(
        seat="seat-a", gen=5, ref="carefbeef", answer="continue",
        text=None, no_commit=False, wait=0, registry_dir=str(reg)), _fix)
    assert rc == 0
    out = capsys.readouterr().out
    # the stale line names BOTH generations.
    assert "stale predecessor answer for gen 4, this is gen 5" in out
    # NOT a no-op: a fresh ack was WRITTEN with the successor's identity.
    assert "already answered" not in out
    ack = json.loads(_ack_path(_fix, "seat-a").read_text(encoding="utf-8"))
    assert ack["gen_after"] == 5
    assert ack["answer"] == "continue"
    assert ack["session_ref"] == "carefbeef"     # successor took its identity
    assert ack.get("source") != "predecessor"    # a successor write
    assert "back-filled session_ref=carefbeef" in out


# --- part (b)+(c): rotation rotates the ack; heal recovery still takes ---- 
#                   its identity ------------------------------------------

def _working_launcher(records, pid=515151, window="@777"):
    def launch(root, name, shell_cmd, window_path=None, cwd=None):
        records.append({"name": name, "pid": pid, "window": window,
                        "cwd": str(cwd)})
        return pid, window
    return launch


def test_rotate_ack_file_renames_and_recover_takes_identity(_fix, capsys):
    """(b)+(c) END-TO-END through heal crash-recovery on the fake tmux:
    a predecessor `continue` sits on disk for gen 4 (what rotate-self left
    after the gen-4 rotation). heal._recover_seat respawns at gen 5 and
    ROTATES the stale ack to `seat-a.ack.gen5.json` BEFORE spawning, so the
    live ack is gone; the recovered post's `ack --gen 5 continue` then
    WRITES (not no-op), back-fills session_ref/pid, and the row carries the
    identity — the record shows it respawned (identity taken)."""
    _write_seats(_fix, [{"name": "seat-a", "role": "parent",
                         "generation": 4, "window": "@50",
                         "pid": 424242, "session_ref": "",
                         "session_id": "", "model": "x"}])
    _predecessor_continue(_fix, "seat-a", 4)   # rotate-self gen-4 continue on disk

    # heal crash-recovery respawn at gen 5 (row gen 4 + 1).
    launcher_rec: list = []
    win = _fix / "windows"
    win.write_text("\n", encoding="utf-8")
    out = heal._recover_seat(
        _fix, next(r for r in rotate._load_seats(_fix)
                   if r["name"] == "seat-a"),
        cause="test", _rotate=rotate, windows=[("", "@50")],
        window_path=str(win), launcher=_working_launcher(launcher_rec),
        now=time.time())
    assert out["respawned"] is True
    assert out["generation"] == 5
    assert len(launcher_rec) == 1, "respawn attempted once"
    # (b) the live ack is GONE — rotated to the generation-stamped name.
    assert not _ack_path(_fix, "seat-a").exists(), \
        "live ack must be rotated away before the recovered post spawns"
    rot = _fix / "sessions" / "seats" / "seat-a.ack.gen5.json"
    assert rot.exists(), "the rotated ack kept the generation-stamped name"
    cap = capsys.readouterr().err
    assert "seat-a.ack.gen5.json" in cap, "heal reports the ack rotation"

    # (c) the recovered post takes its identity: `ack --gen 5 continue`.
    reg = _fix / "empty-reg"
    reg.mkdir()
    from types import SimpleNamespace
    rc = rotate.cmd_ack(SimpleNamespace(
        seat="seat-a", gen=5, ref="recovered-ref", answer="continue",
        text=None, no_commit=False, wait=0, registry_dir=str(reg)), _fix)
    assert rc == 0
    out2 = capsys.readouterr().out
    # WRITES — never a no-op, never a stale-silence.
    assert "already answered" not in out2
    assert "stale predecessor answer" not in out2 or \
        "this is gen 5" in out2   # even the stale line proves it wrote
    ack = json.loads(_ack_path(_fix, "seat-a").read_text(encoding="utf-8"))
    assert ack["gen_after"] == 5 and ack["answer"] == "continue"
    assert ack["session_ref"] == "recovered-ref"
    assert "back-filled session_ref=recovered-ref" in out2
    own = next(r for r in rotate._load_seats(_fix)
               if r["name"] == "seat-a")
    assert own["session_ref"] == "recovered-ref", \
        "the recovered post's identity is back-filled into its row"
    assert out["row"] and "FAILED" not in out["row"]


# --- part (d): the bootstrap ack fact reads the ack file -------------------

def test_bootstrap_ack_fact_derives_from_ack_file(_fix):
    """(d) `_derive_bootstrap_fact('ack', ...)` returns the BARE
    `continue (source predecessor, gen 4)` FROM THE ACK FILE when one exists,
    and `none` when none does — never a row read (the row has no `ack` key;
    no writer fills it). The block writer prefixing the key ONCE is what
    renders `- ack: continue ...` (no doubled `ack: ack:`)."""
    _fix_sheet = _fix / "nodes" / ".geometry" / "seats.md"
    _fix_sheet.parent.mkdir(parents=True, exist_ok=True)
    (_fix / "sessions" / "seats").mkdir(parents=True, exist_ok=True)
    (rotate._ack_path(_fix, "seat-a")).write_text(json.dumps({
        "seat": "seat-a", "gen_after": 4, "answer": "continue",
        "source": "predecessor", "session_ref": "", "ts": "T",
        "text": ""}) + "\n", encoding="utf-8")
    row = {"name": "seat-a", "role": "parent"}   # NO ack key — as written
    val, reason = rotate._derive_bootstrap_fact(
        "ack", root=_fix, seat="seat-a", seat_row=row, commit=None)
    assert val == "continue (source predecessor, gen 4)"
    assert reason is None

    # no ack file -> `none`, still no reason (not a SKIPPED row read).
    (rotate._ack_path(_fix, "seat-b")).parent.mkdir(parents=True, exist_ok=True)
    val2, reason2 = rotate._derive_bootstrap_fact(
        "ack", root=_fix, seat="seat-b", seat_row={"name": "seat-b"},
        commit=None)
    assert val2 == "none"
    assert reason2 is None


def test_stale_prior_gen_ack_is_named_not_current(_fix):
    """(g15.25 SL7.42) `_derive_bootstrap_fact('ack', generation=G, ...)`
    never reads an ack file whose `gen_after` is NOT G — a leftover prior-gen
    ack (a re-seated post) is NAMED `stale: gen N`, never printed as the
    current seating's answer. generation=None (the pre-bound SL7.29 direct
    calls) keeps the unguarded read."""
    (_fix / "sessions" / "seats").mkdir(parents=True, exist_ok=True)
    (rotate._ack_path(_fix, "seat-a")).write_text(json.dumps({
        "seat": "seat-a", "gen_after": 4, "answer": "continue",
        "source": "predecessor", "session_ref": "", "ts": "T",
        "text": ""}) + "\n", encoding="utf-8")
    row = {"name": "seat-a", "role": "parent"}
    # stale: the write's generation (1, a fresh seating) != the file's gen 4.
    val, reason = rotate._derive_bootstrap_fact(
        "ack", root=_fix, seat="seat-a", seat_row=row, commit=None,
        generation=1)
    assert val == "stale: gen 4", val
    assert reason is None
    # a matching generation reads current...
    val2, _ = rotate._derive_bootstrap_fact(
        "ack", root=_fix, seat="seat-a", seat_row=row, commit=None,
        generation=4)
    assert val2 == "continue (source predecessor, gen 4)", val2
    # ...and the pre-bound None keeps the unguarded read.
    val3, _ = rotate._derive_bootstrap_fact(
        "ack", root=_fix, seat="seat-a", seat_row=row, commit=None)
    assert val3 == "continue (source predecessor, gen 4)", val3


def test_bootstrap_block_renders_no_doubled_ack(_fix):
    """(SL7.29 part (a)) the ack fact is prefixed ONCE — a rotate-self
    successor's STARTUP block renders `- ack: continue (source predecessor,
    gen N)` for a default-continue ack and `- ack: diff-requested (source
    predecessor, gen N)` for an --ask-diff ack, NEVER the doubled
    `- ack: ack: ...`. The template-driven rotate-self writes the ack
    (s6.3) then re-derives the bootstrap (s11) — this exercises that same
    real-write-then-render chain in both answer modes, against the real
    `_write_ack` ack shape."""
    seats = _fix / "sessions" / "seats"
    _fix_sheet = _fix / "nodes" / ".geometry" / "seats.md"
    _fix_sheet.parent.mkdir(parents=True, exist_ok=True)
    _fix_sheet.write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        "  - {\"name\": \"seat-a\", \"role\": \"parent\", "
        "\"model\": \"x\"}\n---\n", encoding="utf-8")
    for answer in ("continue", "diff-requested"):
        # the s6.3 -> s11 order: the ack is written first, then the
        # bootstrap re-derives its `ack` fact from the ack file.
        rotate._write_ack(root=_fix, seat="seat-a", gen_after=4,
                          answer=answer, source="predecessor",
                          session_ref="")
        rotate._write_bootstrap(
            _fix, seat="seat-a", generation=4,
            telemetry=["seed", "model", "effort", "window", "worktree",
                       "ack"],
            verification=None, commit="abc1234")
        block, reason = rotate._bootstrap_block(_fix, "seat-a",
                                                commit="abc1234")
        assert reason is None
        ack_lines = [ln for ln in block.splitlines()
                     if ln.strip().startswith("- ack")]
        assert ack_lines, f"no ack line rendered for {answer!r}; block={block}"
        assert ack_lines == [f"- ack: {answer} (source predecessor, gen 4)"]
        # the doubled prefix is the defect — assert it is absent everywhere.
        assert "ack: ack:" not in block


def test_pre_spawn_bootstrap_carries_ack_before_restart(_fix):
    """(SL7.29 part (b)) the ack answer is knowable BEFORE the spawn, so the
    PRE-SPAWN bootstrap write (cmd_rotate_self step 2.75, the EXACT call args
    it now makes) carries the ack fact verbatim through the `overrides` seam —
    `- ack: continue (source predecessor, gen N)` for a default rotation and
    `- ack: diff-requested (source predecessor, gen N)` when --ask-diff is
    set — read back by the SAME hook reader (`_bootstrap_block`). This is the
    record a rotate-self SUCCESSOR reads at TURN ONE (before s6.3 writes any
    ack file), so `ack: none` would be the defect. No `ack: ack:` anywhere; a
    test that only calls the post-join s11 writer does not cover this read."""
    seats = _fix / "sessions" / "seats"
    _fix_sheet = _fix / "nodes" / ".geometry" / "seats.md"
    _fix_sheet.parent.mkdir(parents=True, exist_ok=True)
    _fix_sheet.write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        "  - {\"name\": \"seat-a\", \"role\": \"parent\", "
        "\"model\": \"x\"}\n---\n", encoding="utf-8")
    # NO ack file exists yet — the s6.3 `_write_ack` has NOT run when the
    # pre-spawn record is written. `_derive_bootstrap_fact` would read `none`;
    # the pre-spawn overrides seam supplies the truthful answer instead.
    for ask_diff in (False, True):
        _answer = "diff-requested" if ask_diff else "continue"
        gen = 8
        # the EXACT pre-spawn step-2.75 call args cmd_rotate_self now makes:
        rotate._write_bootstrap(
            _fix, seat="seat-a", generation=gen,
            telemetry=["seed", "model", "effort", "window", "worktree",
                       "ack"],
            verification=None, commit="abc1234",
            join_pending=set(rotate.BOOTSTRAP_JOIN_ONLY_FACTS),
            overrides={"ack":
                       f"{_answer} (source predecessor, gen {gen})"})
        block, reason = rotate._bootstrap_block(_fix, "seat-a",
                                                commit="abc1234")
        assert reason is None
        ack_lines = [ln for ln in block.splitlines()
                     if ln.strip().startswith("- ack")]
        assert ack_lines, f"no ack line rendered for ask_diff={ask_diff}"
        assert ack_lines == [
            f"- ack: {_answer} (source predecessor, gen {gen})"]
        assert "ack: ack:" not in block
        assert "ack: none" not in block
        # the record on disk is the turn-one source of truth for the hook:
        doc = json.loads((seats / "seat-a.bootstrap.json")
                         .read_text(encoding="utf-8"))
        assert doc["telemetry"]["ack"] == \
            f"{_answer} (source predecessor, gen {gen})"


def _ack_ns(gen=1, ref="r1", reg=None):
    from types import SimpleNamespace
    return SimpleNamespace(seat="seat-a", gen=gen, ref=ref,
                           answer="continue", text=None, no_commit=False,
                           wait=0, registry_dir=(str(reg) if reg else None))