"""hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-
hook-fires-at-turn-one — g15-7 FIX, the turn-one proof.

The measured defect (on today's bytes before the fix):
  * rotate.py _shell_cmd exported NO seat identity, so AGI_SEAT was never in
    the successor's environment; the hook COPY (cc-session-start.next.sh)
    keys its bootstrap injection on AGI_SEAT (`BOOTSTRAP_SEAT="${AGI_SEAT:-}"`)
    and is a silent no-op without it — the hook cannot fire at turn one.
  * the bootstrap record was written at s11, AFTER the spawn, so even a
    seat-exported spawn would find no record at turn one.

This test proves both halves on the FIXED bytes, hermetically (no real
spawn, no network, no tmux):
  (a) `rotate._shell_cmd` preprends `export AGI_SEAT=<seat> && ` BEFORE the
      claude argv when a seat is given, and stays byte-identical to today
      (reaper + argv) when NO seat is given (a plain `spawn` is untouched);
  (b) a bootstrap record written PRE-spawn by the production writer
      (`rotate._write_bootstrap`, the exact call cmd_rotate_self now makes
      at step 2.75) is read back by the SAME reader the hook uses —
      `rotate.py bootstrap-block --seat --root`, the path DERIVED in
      production, never hardcoded in this test — and the hook COPY emits the
      injected block when AGI_SEAT is set;
  (c) the join-only facts in a PRE-spawn record carry the explicit
      `pending: resolved after join` marker (never a blank, never a `SKIPPED:
      <predecessor owns>` reason);
  (d) MUTATION / falsifier: the SAME hook run with AGI_SEAT unset (the
      pre-fix artifact — nothing exported the seat) must NOT emit the block.
      A guard that cannot fail certifies nothing.
The live hook cc-session-start.sh and ~/.claude/settings.json are the
PRIME's install step; this test touches neither (proves on the COPY only).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))       # agi/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))  # rotate
import rotate  # noqa: E402

PLUGIN = Path(__file__).resolve().parents[3] / "extensions" / "agi"
NEXT_HOOK = PLUGIN / "hooks" / "cc-session-start.next.sh"
SEAT = "adv-alive"
BOOTSTRAP_MARKER = f"bootstrap: {SEAT} successor handover"
PENDING_MARKER = "pending: resolved after join"


def _git(root: Path, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


@pytest.fixture()
def project(tmp_path):
    """A minimal PROJECT that is also a git repo with one committed node, so
    `_git_head` resolves a real HEAD and the pre-spawn record is provably
    not-stale at turn one."""
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    (root / "context").mkdir(parents=True)
    (root / "agi-tree.config.json").write_text("{}")
    (root / "nodes" / "n.md").write_text(
        '---\nid: "goal:n"\ntype: goal\n---\n\nbody\n')
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "init")
    # a fresh, extant INJECTION.md so the hook's build-gate passes and only
    # the bootstrap section is under test.
    (root / "context" / "INJECTION.md").write_text(
        "## map\n\nfake map\n", encoding="utf-8")
    return root


def _head(root: Path) -> str:
    out = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, check=True)
    return out.stdout.strip()


def _pre_spawn_bootstrap(root: Path) -> Path:
    """Write the record EXACTLY the way cmd_rotate_self step 2.75 now writes
    it (the PRE-spawn write): production writer, telemetry facts the rotation
    template declares, the join-only facts marked pending. Returns the path
    the writer itself derived (never hardcoded here)."""
    p = rotate._write_bootstrap(
        root, seat=SEAT, generation=7,
        telemetry=["seed", "model", "ack"],
        verification=None,
        join_pending=set(rotate.BOOTSTRAP_JOIN_ONLY_FACTS))
    return Path(p)


def _bootstrap_block_via_rotate(root: Path) -> tuple[str, int]:
    """The reader half via the CLI the hook calls — the record PATH resolved
    in production (rotate.py bootstrap-block), never a literal in this test."""
    r = subprocess.run(
        [sys.executable, str(PLUGIN / "bin" / "rotate.py"),
         "bootstrap-block", "--seat", SEAT, "--root", str(root)],
        capture_output=True, text=True, check=False)
    return r.stdout, r.returncode


def _run_hook(cwd: Path, *, home: Path, seat: str | None):
    """Drive the .next hook copy the way CC drives the live hook. `seat=None`
    simulates the pre-fix artifact (nothing exported AGI_SEAT into the
    successor's env)."""
    env = dict(os.environ)
    env.pop("AGI_TREE_PROJECT_ROOT", None)
    env.pop("AUTORESEARCH_TREE_PROJECT_ROOT", None)
    env["HOME"] = str(home)
    if seat is not None:
        env["AGI_SEAT"] = seat
    else:
        env.pop("AGI_SEAT", None)
    return subprocess.run(["bash", str(NEXT_HOOK)], cwd=str(cwd),
                          capture_output=True, text=True, env=env)


# (a) the spawn path EXPORTS AGI_SEAT before claude; a no-seat spawn stays
#     byte-identical to today.
def test_shell_cmd_exports_seat_only_when_seat_given():
    no_seat = rotate._shell_cmd(["claude", "--remote-control", "s"], None)
    assert "AGI_SEAT" not in no_seat
    assert no_seat.startswith(
        "export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 && claude "
        "--remote-control s")
    seated = rotate._shell_cmd(["claude", "--remote-control", "s"], None,
                               seat=SEAT)
    assert f"export AGI_SEAT={SEAT} && claude --remote-control s" in seated
    # the export rides before the claude process, after the reaper knob.
    assert seated.index("export AGI_SEAT") < seated.index("claude")


# (b)+(c) a PRE-SPAWN record (production writer, join facts pending) is
#     readable via the production bootstrap-block reader and the hook COPY
#     injects the block at turn one.
def test_pre_spawn_record_fires_hook_at_turn_one(project, tmp_path):
    head = _head(project)
    p = _pre_spawn_bootstrap(project)
    doc = json.loads(p.read_text(encoding="utf-8"))
    # (c) every join-only fact is the explicit pending marker, never a blank
    #     and never a `SKIPPED: <predecessor owns>` reason.
    for key in rotate.BOOTSTRAP_JOIN_ONLY_FACTS:
        assert doc["telemetry"][key] == PENDING_MARKER, key
    assert not any(str(doc["telemetry"][k]).startswith("SKIPPED: 0b owns")
                   for k in doc["telemetry"])

    # the SAME reader the hook uses, path derived in production:
    block, rc = _bootstrap_block_via_rotate(project)
    assert rc == 0
    assert PENDING_MARKER in block
    assert "commit" in block and "seed" in block

    # full turn-one: run the hook COPY against that pre-spawn record.
    r = _run_hook(project, home=tmp_path / "home", seat=SEAT)
    assert r.returncode == 0
    assert BOOTSTRAP_MARKER in r.stdout
    assert "## ⚓ bootstrap" in r.stdout


# (d) MUTATION / falsifier: the SAME hook, AGI_SEAT unset (the pre-fix
#     artifact — no spawn path exported it), MUST NOT emit the block. If the
#     export were removed, this is exactly the silent no-op a successor got.
def test_without_seat_export_block_absent_is_the_falsifier(project, tmp_path):
    _pre_spawn_bootstrap(project)          # record PRESENT
    r = _run_hook(project, home=tmp_path / "home", seat=None)  # but no export
    assert r.returncode == 0
    assert BOOTSTRAP_MARKER not in r.stdout
    assert "## ⚓ bootstrap" not in r.stdout