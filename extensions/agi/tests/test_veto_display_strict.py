"""G-DISPLAY strict (goal:g7.16.1.11.13.3, DG1's falsifiers 1, 2 and 4; DG2 writes the rows FIRST, DG5 builds to them).

The six GATED acts read the veto cell strict and HOLD on a missing or malformed cell. The two DISPLAY readers did not move:

  S1 `send.veto_gate_status(root, scope)`   reads `_veto.read(graph)` non-strict: an absent or unparsable cell prints "scope ... is FREE"
  S2 `viewport.py --live`                   reads `_veto.read(root)` non-strict with ROOT = the post's OWN worktree: silence on a bad cell,
                                            and the worktree's copy of the cell, never MAIN's, which is the one every gate reads

Rows (the builder is free in wording: a row asks for the token HOLD and the cause text veto.read raises, never for a full sentence):
  d1  falsifier 1: the non-strict `_veto.read(graph|root)` reads in send.py + viewport.py count <= 2 (4 today: send.py x3, viewport.py x1; the two WRITER reads in send.py stay)
  d2  falsifier 2: per reader, the cell MISSING then MALFORMED: the output has HOLD and the cause ("missing veto cell" / "unreadable veto cell") and no FREE
  d3  stays-green: a well-formed cell prints byte-identical lines (GOLDEN below, measured on trunk 3bbfd7cf15): send FREE + FROZEN, viewport FROZEN, viewport FREE = no gate line
  d5  the INVARIANT (a display reader never frees a scope a gate holds), the import arm: since .13.2 every gate HOLDS when `seatsig` cannot be imported; `veto_gate_status` with a broken seatsig import must HOLD with the cause, not "treated as free"
  d6  the same for `viewport.py --live`: a HOLD line with the cause in both views, not the silence its outer `except Exception` gave
  d4  falsifier 4: a git worktree whose copy of the cell is FREE while MAIN's is FROZEN (and the reverse): `viewport.py --live` run from the worktree shows MAIN's verdict, the
      same as the gate and as `veto_gate_status` (which already resolves MAIN: those two rows stay green)
Each row runs the reader as a SUBPROCESS under a scratch HOME and git config; the engine under test is VETO_ROOT=<tree> (default: the repo holding this file).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
ROOT = Path(os.environ.get("VETO_ROOT") or HERE.parents[3])
EXT = ROOT / "extensions"
BIN = EXT / "agi" / "bin"
SRC = EXT / "agi" / "src"
VIEWPORT = BIN / "viewport.py"
SENDPY = BIN / "send.py"

CELL = Path(".agi") / "nodes" / ".geometry" / "vetoes.md"
HEAD = "---\nid: config:vetoes\nmint_id: 5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a\ntype: config\nparents: []\n"
TEXT = {
    "free": HEAD + "active_gates: []\nvetoes: []\n---\n\n# config:vetoes\n",
    "frozen": HEAD + "active_gates:\n  - scope: prime\n    since: 2026-10-10T00:00:00Z\n    veto_ref: v1\n    answered: \"\"\nvetoes: []\n---\n\n# config:vetoes\n",
    "malformed": "---\nactive_gates: [unclosed\n  - {\n---\nbody\n",
}
CAUSE = {"missing": "missing veto cell", "malformed": "unreadable veto cell"}
# GOLDEN: the lines a well-formed cell prints today (trunk 3bbfd7cf15), byte for byte
G_SEND_FREE = "veto: scope 'prime' is FREE (no active human gate; the owner answers in the 'veto' room when one is filed)"
G_SEND_FROZEN = ("GATE-FROZEN scope=prime room=veto; 'prime' is FROZEN by a human gate (veto v1) since 2026-10-10 00:00:00+00:00; "
                 "it is never auto-released -- only an owner answer in 'veto' clears it")
G_VP_FROZEN = "GATE-FROZEN scope=prime since=2026-10-10 00:00:00+00:00 veto=v1 (human gate; waits for an owner answer)"

BRK = ("import sys\n"
       "class _Break:\n"
       "    def find_spec(self, name, path=None, target=None):\n"
       "        if name == 'seatsig' or name.startswith('seatsig.'):\n"
       "            raise ImportError('boom-import-9')\n"
       "def install():\n"
       "    for k in [k for k in sys.modules if k == 'seatsig' or k.startswith('seatsig.')]:\n"
       "        del sys.modules[k]\n"
       "    sys.meta_path.insert(0, _Break())\n")
PROBE_BRK = ("import sys;sys.path[:0]=[%r,%r,%r,%r];from pathlib import Path;import send,brk;brk.install();"
             "print(send.veto_gate_status(Path(sys.argv[1]),sys.argv[2]))")
VP_BRK = ("import sys,runpy;sys.path.insert(0,%r);import brk;brk.install();"
          "sys.argv=['viewport.py','--live','--emit',sys.argv[1],'--project',sys.argv[2]];runpy.run_path(%r,run_name='__main__')")

PROBE = ("import sys;sys.path[:0]=[%r,%r,%r];from pathlib import Path;import send;"
         "print(send.veto_gate_status(Path(sys.argv[1]),sys.argv[2]))" % (str(EXT), str(BIN), str(SRC)))


def _env(home: Path) -> dict:
    return {"PATH": "/usr/bin:/bin", "HOME": str(home), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null",
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def _git(repo: Path, home: Path, *a: str) -> None:
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, env=_env(home))
    assert r.returncode == 0, (a, r.stderr)


class World:
    """A scratch repo MAIN (a goal node + the veto cell, committed FREE) and a detached worktree WT of it."""

    def __init__(self, tmp: Path):
        self.home = tmp / "home"
        self.home.mkdir()
        self.brk = tmp / "brk"
        self.brk.mkdir()
        (self.brk / "brk.py").write_text(BRK)
        self.main = tmp / "main"
        self.wt = tmp / "wt"
        self.main.mkdir()
        _git(self.main, self.home, "init", "-q", "-b", "trunk")
        (self.main / ".agi" / "nodes" / "goal").mkdir(parents=True)
        (self.main / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
        (self.main / ".agi" / "config.json").write_text("{}")
        (self.main / ".agi" / "nodes" / "goal" / "root.md").write_text(
            "---\nid: goal:root\nmint_id: 00000000000000000000000000000001\ntype: goal\nparents: []\n---\nbody\n")
        (self.main / CELL).write_text(TEXT["free"])
        _git(self.main, self.home, "add", "-A")
        _git(self.main, self.home, "commit", "-q", "-m", "base")
        _git(self.main, self.home, "worktree", "add", "-q", "--detach", str(self.wt))

    def cell(self, where: Path, state: str) -> None:
        p = where / CELL
        if state == "missing":
            p.unlink(missing_ok=True)
        else:
            p.write_text(TEXT[state])

    def send(self, where: Path, scope: str = "prime", broken: bool = False) -> str:
        code = PROBE_BRK % (str(self.brk), str(EXT), str(BIN), str(SRC)) if broken else PROBE
        r = subprocess.run([sys.executable, "-c", code, str(where / ".agi"), scope], capture_output=True, text=True,
                           env={**_env(self.home), "PYTHONDONTWRITEBYTECODE": "1"}, timeout=120)
        return r.stdout + r.stderr

    def viewport(self, where: Path, view: str = "human", broken: bool = False) -> str:
        cmd = ([sys.executable, "-c", VP_BRK % (str(self.brk), str(VIEWPORT)), view, str(where / ".agi")] if broken
               else [sys.executable, str(VIEWPORT), "--live", "--emit", view, "--project", str(where / ".agi")])
        r = subprocess.run(cmd, cwd=where,
                           capture_output=True, text=True, env={**_env(self.home), "PYTHONDONTWRITEBYTECODE": "1"}, timeout=180)
        return r.stdout + r.stderr


@pytest.fixture
def world(tmp_path):
    return World(tmp_path)


def gate_lines(out: str) -> list:
    """The viewport's gate text: the part of the status line before ' — anchor=' (a GATE-FROZEN or HOLD segment), per line that has one."""
    return [l.split(" — anchor=")[0] for l in out.splitlines() if " — anchor=" in l and not l.startswith("anchor=") and l.split(" — anchor=")[0].strip()]


# --- d1: falsifier 1 (the count of non-strict reads), with a witness that the grep can hit
READ = re.compile(r"_veto\.read\((graph|root)\)")


def _reads(path: Path) -> list:
    return [i + 1 for i, l in enumerate(path.read_text().splitlines()) if READ.search(l)]


def test_d1_the_pattern_can_hit(tmp_path):
    p = tmp_path / "w.py"
    p.write_text("g = _veto.read(graph)\nh = _veto.read(root, strict=True)\n")
    assert _reads(p) == [1], "the count must be able to hit a non-strict read and miss a strict one"


def test_d1_the_non_strict_display_reads_are_gone_two_writer_reads_remain():
    hits = {f.name: _reads(f) for f in (SENDPY, VIEWPORT)}
    total = sum(len(v) for v in hits.values())
    assert total <= 2, f"{total} non-strict `_veto.read(graph|root)` reads (want <= 2: the owner-answer and accept paths in send.py): {hits}"
    assert hits["viewport.py"] == [], f"viewport.py still reads the cell non-strict: {hits['viewport.py']}"


# --- d2: falsifier 2 -- the cell MISSING then MALFORMED: HOLD with its cause, never FREE or silence
@pytest.mark.parametrize("state", ["missing", "malformed"])
def test_d2_send_veto_gate_status_holds_with_its_cause(world, state):
    world.cell(world.main, state)
    out = world.send(world.main)
    assert "HOLD" in out and CAUSE[state] in out, f"{state}: want HOLD + '{CAUSE[state]}', got {out[-300:]!r}"
    assert "is FREE" not in out, f"{state}: the display frees a scope the gates hold: {out[-300:]!r}"


@pytest.mark.parametrize("state", ["missing", "malformed"])
def test_d2_viewport_live_holds_with_its_cause(world, state):
    world.cell(world.main, state)
    out = world.viewport(world.main)
    assert "HOLD" in out and CAUSE[state] in out, f"{state}: want HOLD + '{CAUSE[state]}', got {out[-400:]!r}"
    assert "FREE" not in out


@pytest.mark.parametrize("view", ["human", "llm"])
def test_d2_viewport_shows_the_hold_in_both_views_of_one_stream(world, view):
    world.cell(world.main, "malformed")
    out = world.viewport(world.main, view)
    assert "HOLD" in out and CAUSE["malformed"] in out, (view, out[-300:])


# --- d3: a well-formed cell prints exactly what it prints today (GREEN on the trunk, must stay green)
def test_d3_send_free_and_frozen_lines_are_byte_identical(world):
    world.cell(world.main, "free")
    assert world.send(world.main).strip() == G_SEND_FREE
    world.cell(world.main, "frozen")
    assert world.send(world.main).strip() == G_SEND_FROZEN
    assert world.send(world.main, "other").strip().startswith("veto: scope 'other' is FREE"), "a different scope stays free"


def test_d3_viewport_frozen_line_is_byte_identical_and_a_free_cell_prints_no_gate_text(world):
    world.cell(world.main, "frozen")
    out = world.viewport(world.main)
    assert G_VP_FROZEN in gate_lines(out), (gate_lines(out), out[-300:])
    world.cell(world.main, "free")
    out = world.viewport(world.main)
    assert "GATE-FROZEN" not in out and "HOLD" not in out, out[-300:]
    assert "anchor=roots" in out, "the status line itself must still print (non-vacuous)"


# --- d4: falsifier 4 -- the worktree's copy of the cell differs from MAIN's: every reader shows MAIN's verdict, the gates' verdict
def test_d4_viewport_from_a_worktree_shows_MAINs_FROZEN_when_the_worktree_copy_is_FREE(world):
    world.cell(world.main, "frozen")
    world.cell(world.wt, "free")
    out = world.viewport(world.wt)
    assert G_VP_FROZEN in gate_lines(out), f"MAIN is FROZEN but the worktree's FREE copy was read: {gate_lines(out)} / {out[-300:]!r}"


def test_d4_viewport_from_a_worktree_shows_MAINs_FREE_when_the_worktree_copy_is_FROZEN(world):
    world.cell(world.main, "free")
    world.cell(world.wt, "frozen")
    out = world.viewport(world.wt)
    assert "GATE-FROZEN" not in out, f"MAIN is FREE but the worktree's FROZEN copy was read: {gate_lines(out)}"
    assert "anchor=roots" in out, "the status line itself must still print (non-vacuous)"


def test_d4_viewport_from_a_worktree_holds_on_MAINs_missing_cell(world):
    world.cell(world.main, "missing")
    world.cell(world.wt, "free")
    out = world.viewport(world.wt)
    assert "HOLD" in out and CAUSE["missing"] in out, f"MAIN's cell is missing but the worktree's copy was read: {out[-300:]!r}"


@pytest.mark.parametrize("main_state,wt_state,want", [("frozen", "free", G_SEND_FROZEN), ("free", "frozen", G_SEND_FREE)])
def test_d4_send_status_from_a_worktree_already_reads_MAIN_stays_green(world, main_state, wt_state, want):
    world.cell(world.main, main_state)
    world.cell(world.wt, wt_state)
    assert world.send(world.wt).strip() == want


# --- d5 / d6: the import arm. The gates HOLD whatever the cell says when `seatsig` cannot be imported; the displays must not free what they hold
@pytest.mark.parametrize("state", ["free", "frozen"])
def test_d5_send_veto_gate_status_holds_when_the_seatsig_import_is_broken(world, state):
    world.cell(world.main, state)
    out = world.send(world.main, broken=True)
    assert "HOLD" in out and "boom-import-9" in out, f"{state}: want HOLD + the import error, got {out[-300:]!r}"
    assert "treated as free" not in out and "is FREE" not in out, f"{state}: the display frees a scope the gates hold: {out[-300:]!r}"


@pytest.mark.parametrize("view", ["human", "llm"])
def test_d6_viewport_live_shows_a_hold_when_the_seatsig_import_is_broken(world, view):
    world.cell(world.main, "free")
    out = world.viewport(world.main, view, broken=True)
    assert "HOLD" in out and "boom-import-9" in out, f"{view}: want a HOLD line + the import error, not silence: {out[-300:]!r}"
    assert "anchor=roots" in out, "the status line itself must still print (non-vacuous: the viewport ran)"


def test_d5_d6_the_break_is_real_the_same_probe_without_it_reads_the_cell(world):
    """Non-vacuous: without the break the FREE cell prints today's FREE line and the viewport prints no HOLD."""
    world.cell(world.main, "free")
    assert world.send(world.main).strip() == G_SEND_FREE
    assert "HOLD" not in world.viewport(world.main)
