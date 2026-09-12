#!/usr/bin/env python3
"""heal.py — monitor agent timeouts; spawn healer subagent for hung agents.

Polls <project>/sessions/iter-NNN/manifest.json (or iter-L1.08 for a
loop-scoped id; `locations.iteration_dir`) + each agent.json. For agents
whose status is still 'running' past `timeout_seconds`:
  1. Kill the pid (gracefully → SIGKILL after grace)
  2. Mark agent.json status=hung
  3. Spawn a HEALER pi subprocess with:
     - The hung agent's last log tail
     - Diagnose-and-patch instruction
     - Completion CLI signal

Usage:
    heal.py <project_root> <iter_n> [--poll-interval-s 30] [--max-wait-mins 30]

Returns 0 when ALL agents are in terminal status (done/pending/hung-then-healed/failed).
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import importlib.util
import io
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
CLI_PY = PLUGIN_ROOT / "bin" / "cli.py"

# goal:g11.1 / goal:s8 — one definition of "which env is safe to hand pi" and
# one of "which model does a pi child run", shared with the other spawner
# rather than re-derived here. `bin/` is on sys.path when this runs as a
# script; the insert makes it so when it is imported as a module too.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import adapters  # noqa: E402 -- the shared (tier, role, harness) resolver
import spawn_gate  # noqa: E402
import spawn_budget  # noqa: E402 -- liveness reader for the worktree sweep (hyp:l4-a-finished-rounds-worktree-is-removed-after-harvest)
import branches  # noqa: E402 -- the ONE branch-name grammar (g15 round I)
def _default_role_for_tier(tier):
    """Mirror dispatch's default (role == tier) for the heal path."""
    return tier or "kid"


def _default_tier_for_role(role):
    """The canonical ladder tier a role lives at (mirror of dispatch's)."""
    return {"kid": 0, "parent": 1, "director": 1, "prime_director": 3}.get(
        role, 0)
from dispatch import pi_model_args, _reap_pass  # noqa: E402
from dispatch import scrubbed_env as _scrubbed_env  # noqa: E402
from spawn_budget import TERMINAL  # noqa: E402 -- the ONE terminal-status set (hyp:l4-one-definition-of-terminal)
import reaper_log  # noqa: E402 -- the ONE per-event log resolver (lifted from _watch_log; send.py's wake outcome line shares it)


def _pi_model_args(root: Path, tier: str = "kid",
                   role: str | None = None) -> list[str]:
    """Model flags for the healer, from the ladder when a row exists
    (hypothesis:l4-a-model-change-is-one-write), else the legacy config path.

    Sits on the same shared resolver (`adapters.ladder_role_row` +
    `adapters.spec_from_ladder_row`) dispatch.py uses, so a `write.py` on the
    ladder changes what a healed agent is re-spawned with -- same "one write"
    contract as a fresh dispatch. Never raises: healing runs when something is
    already broken, so a missing or malformed config must cost the healer its
    model preference, not its existence.
    """
    try:
        cfg_path = locations.config_path(root)
        if cfg_path is None:
            return []
        cfg = json.loads(cfg_path.read_text())
        roles = spawn_gate.read_ladder_roles(root / "nodes" if root else None)
        # `tier` here is the HEALED AGENT's record "tier" — a role-string like
        # `parent`/`kid` (dispatch writes args.tier), not the ladder's int. Map
        # the role to its canonical int tier for the lookup.
        _role = role or _default_role_for_tier(tier)
        if str(tier).isdigit():
            _tier_int = int(tier)
        else:
            _tier_int = _default_tier_for_role(_role)
        row = adapters.ladder_role_row(roles, _tier_int, _role)
        if row is not None and (row.get("model") or "").strip():
            spec = adapters.spec_from_ladder_row(row)
            harness = {"adapter": "pi", "models": {_role: spec["model"]}}
            if spec.get("thinking"):
                harness["thinking"] = spec["thinking"]
            return adapters.load("pi").model_args(harness, _role)
        return pi_model_args(cfg)
    except Exception as exc:  # noqa: BLE001 — see docstring
        print(f"heal: could not read model config ({exc}); using pi defaults",
              file=sys.stderr)
        return []


def main() -> int:
    # hypothesis:l4-the-reaper-is-one-persistent-service — `heal.py watch` is
    # a SUBCOMMAND of heal.py, never a new bin/*.py (test_bin_help_smoke stays
    # green). The legacy positional CLI (`heal.py <root> <iter_n>`) is
    # untouched so driver.sh's heal call parses identically.
    if len(sys.argv) > 1 and sys.argv[1] == "watch":
        return _main_watch()
    if len(sys.argv) > 1 and sys.argv[1] == "sweep":
        return _main_sweep()
    if len(sys.argv) > 1 and sys.argv[1] == "pin-reap":
        return _main_pin_reap()
    return _main_heal()


def _main_pin_reap() -> int:
    """(2b) `heal.py pin-reap [--dry-run] [--registry-dir D]` — ONE pass,
    LIST ONLY regardless of the flag: arming happens ONLY through
    `.agi/config.json` `reaper.pin_reap == "armed"`, never a CLI flag. The
    `--dry-run` flag is accepted for symmetry and the pass is still list-only.
    Exit 0. The live pass reads the real registry dir (`~/.claude/sessions`)
    unless `--registry-dir` is given."""
    ap = argparse.ArgumentParser(prog="heal.py pin-reap")
    ap.add_argument("--root", type=str, default=".",
                    help="the main checkout / graph root to scan")
    ap.add_argument("--dry-run", action="store_true",
                    help="accepted for symmetry; a pin-reap is ALWAYS list-only")
    ap.add_argument("--registry-dir", type=str, default=None,
                    help="override the cc session registry dir (test seam)")
    ap.add_argument("--window-path", type=str, default=None,
                    help="window-list seam (AGI_WINDOW_PATH); default real tmux")
    args = ap.parse_args(sys.argv[2:])
    given = Path(args.root).resolve()
    root = locations.find_project_root(given) or given
    _pin_reap_pass(root, registry_dir=args.registry_dir,
                   window_path=args.window_path, mode="dry-run")
    return 0


def _main_heal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=locations.iteration_id)
    ap.add_argument("--poll-interval-s", type=int, default=30)
    ap.add_argument("--max-wait-mins", type=int, default=30)
    args = ap.parse_args()

    # goal:g11.1 — resolve the given path the way every other entry point
    # resolves cwd, rather than demanding it already BE the graph root.
    # Identity when driver.sh passes an already-resolved root, so nothing
    # changes for the caller that exists today.
    given = Path(args.project_root).resolve()
    root = locations.find_project_root(given) or given
    iter_dir = locations.iteration_dir(root, args.iter_n)
    manifest_path = iter_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"ERR: no manifest at {manifest_path}", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text())
    timeout_s = int(manifest.get("timeout_seconds", 600))

    deadline = time.time() + args.max_wait_mins * 60
    healed_already: set[str] = set()

    while time.time() < deadline:
        all_terminal = True
        for entry in manifest["agents"]:
            agent_id = entry["id"]
            ap_file = iter_dir / agent_id / "agent.json"
            if not ap_file.exists():
                continue
            rec = json.loads(ap_file.read_text())
            status = rec.get("status", "running")
            # Sync manifest status from agent.json so post_wire sees current state
            if entry.get("status") != status:
                entry["status"] = status
            if status in TERMINAL:
                continue
            if status != "running":
                continue
            all_terminal = False
            elapsed = int(time.time()) - int(rec.get("started_at", 0))
            if elapsed > timeout_s and agent_id not in healed_already:
                _heal(root, args.iter_n, agent_id, rec)
                healed_already.add(agent_id)
                # hypothesis:l4-a-round-alarms-its-dispatcher-by-default — the
                # TIMEOUT event: exactly ONE dm to the seat that dispatched it,
                # naming the reason. No flag; the stamp came from dispatch.
                _alarm_dispatcher(rec, args.iter_n, "timeout", root)
            else:
                # Also detect if pid is dead w/o status update → mark failed.
                pid = int(rec.get("pid", 0))
                if pid > 0 and not _pid_alive(pid):
                    rec["status"] = "failed"
                    rec["finished_at"] = int(time.time())
                    rec["fail_reason"] = "pid disappeared without completion signal"
                    ap_file.write_text(json.dumps(rec, indent=2))
                    # Sync to manifest too
                    entry["status"] = "failed"
                    print(f"agent {agent_id} marked failed (pid {pid} gone)")
                    # hypothesis:l4-a-round-alarms-its-dispatcher-by-default —
                    # the DEATH event: exactly ONE dm naming the reason.
                    _alarm_dispatcher(rec, args.iter_n, "death", root)
        # Persist manifest so post_wire sees current status
        manifest_path.write_text(json.dumps(manifest, indent=2))
        if all_terminal:
            print("all agents terminal")
            return 0
        time.sleep(args.poll_interval_s)

    print("ERR: max-wait exceeded; some agents still non-terminal", file=sys.stderr)
    return 2


# --- heal.py watch: the ONE persistent reaper service ---
# hypothesis:l4-the-reaper-is-one-persistent-service part 2. `watch` is the
# service's loop: discover every live round, run the SAME `_reap_pass`
# dispatch.py's inline reaper runs, then mark timeouts and dm each terminal
# event. It exits only when told to (or after one pass with `--once`, which is
# what the tests drive). A round's deadline stays DATA in its manifest
# (`timeout_seconds`); the watcher has no per-round lifetime of its own.


class _WatcherAdapter:
    """The one hook `_reap_pass` needs from an adapter, backstopped by
    heal.py's own pid liveness probe (os.kill(pid, 0)). No harness, no
    restarts-from-the-service: `_reap_pass` is called with cap=1 cfg=None so
    a dead pid is recorded but the SERVICE does not decide concurrency."""

    def is_alive(self, pid: int) -> bool:
        return _pid_alive(pid)


def _watch_log(line: str) -> None:
    """Log ONE line per watcher event to the reaper log (the same dir and
    hash style as crons.py's), or to stderr when the log is not overridable.
    Delegates to the SHARED resolver `reaper_log.log` (lifted here so send.py's
    `wake` outcome line uses the SAME log path -- never a second one; clause
    (3) of hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box
    and-wake-names-its-path). A MOVE, not a behaviour change.
    Tests set AGI_REAPER_LOG to a tmp path so they never touch ~/logs; the
    unit (the systemd service) sets it in Environment= or lets it default.
    """
    reaper_log.log(line)


def _discover_rounds(root: Path) -> list[tuple[Path, Path]]:
    """`(iter_dir, manifest_path)` for every round manifest the watcher owns:
    under the main checkout's sessions dir and under every seat worktree's
    own `.agi/sessions/` (seat manifests live in their own worktrees during a
    run). The sessions dir is resolved through `locations.sessions_dir` so a
    graph-root path and a checkout path both land on the live rounds.
    """
    rounds: list[tuple[Path, Path]] = []
    try:
        sess = locations.sessions_dir(root)
        for mp in sorted(sess.glob(f"{locations.ITER_DIR_PREFIX}*/manifest.json")):
            rounds.append((mp.parent, mp))
    except OSError:
        pass
    wt_base = root / "worktrees"
    if wt_base.is_dir():
        try:
            for mp in sorted(wt_base.glob(
                    f"*/.agi/sessions/{locations.ITER_DIR_PREFIX}*/manifest.json")):
                rounds.append((mp.parent, mp))
        except OSError:
            pass
    return rounds


def _watch_round(root: Path, iter_dir: Path, adapter) -> None:
    """One watcher pass over one round: death reap (via `_reap_pass`), then a
    timeout check for every agent still `running`.

    Per-round deadlines stay DATA: a running agent past its manifest's
    `timeout_seconds` is marked `timeout` in BOTH the agent record and the
    manifest it was found in, and its dispatcher gets exactly ONE dm through
    the L4.113 path. A round with no `dispatched_by` stamp gets the mark and
    one log line, never silence. The round is NEVER killed here — kill is
    the round's own declared choice (`kill_on_timeout`); this pass only
    observes and marks.
    """
    try:
        outcome = _reap_pass(root, iter_dir, adapter, cap=1, cfg=None,
                             restart_ok=False)
    except Exception as exc:  # noqa: BLE001
        _watch_log(f"watch: reap pass failed for {iter_dir}: {exc}")
        return

    # Re-read the manifest: `_reap_pass` may have rewritten it with the reap
    # marks, and its timeout_seconds IS the round's deadline.
    manifest_path = iter_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError):
        manifest = {}
    timeout_s = int(manifest.get("timeout_seconds", 600))

    # Residue (a), service death path: `_reap_pass` already wrote each dead
    # pid as an honest DEATH (status `failed`, fail_reason "pid N died ...").
    # The dm is the watcher's job — exactly ONE death dm per dead agent, one
    # log line — so a service with inline_reaper off loses NO death dm
    # (dispatch.py's inline reaper wrote `failed` with a bogus "restart
    # unavailable" reason and no dm at all). The manifest already carries the
    # mark, so this is dm + log only.
    for agent_id in outcome.get("died", []):
        rec_path = iter_dir / agent_id / "agent.json"
        try:
            rec = json.loads(rec_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        # One status, one dm, distinguishable: death vs timeout are separate
        # events with separate dms; never re-dm an already-dm'd death on a
        # later pass (idempotence: skip once the record is terminal).
        if rec.get("status") == "failed" and rec.get("finished_at"):
            _alarm_dispatcher(rec, iter_dir.name, "death", root)
            _watch_log(f"watch: iter={iter_dir.name} agent={agent_id} marked "
                       f"DEAD ({rec.get('fail_reason') or 'pid died'}; "
                       f"dispatched_by={rec.get('dispatched_by') or '-'})")

    # hypothesis:l4-the-manifest-mirrors-terminal-agent-status — the CLEAN
    # terminal mirror. `_reap_pass` copied a terminal agent.json (done/failed/
    # timeout) onto a manifest entry that still read `running` and returned the
    # ids under `mirrored`. Here we log ONE line per reconciled entry and send
    # NO dm: a clean `done` is not an alarm. The manifest was already rewritten
    # by `_reap_pass`; this loop only reports it. Keeping it separate from the
    # death block (heal.py:316-338) means a mirror never re-derives a death or
    # timeout — it only heals the divergence between the two files.
    for agent_id in outcome.get("mirrored", []):
        rec_path = iter_dir / agent_id / "agent.json"
        try:
            rec = json.loads(rec_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        status = rec.get("status", "done")
        _watch_log(f"watch: iter={iter_dir.name} agent={agent_id} manifest "
                   f"MIRRORED to agent.json status={status} "
                   f"(dispatched_by={rec.get('dispatched_by') or '-'})")

    for agent_id in outcome["still"]:
        rec_path = iter_dir / agent_id / "agent.json"
        try:
            rec = json.loads(rec_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        # `_reap_pass` may have ALREADY made this agent terminal this pass
        # (a death it reaped, or a done-unreported). It sat in `still` only
        # because it was live at reap time; skip it rather than re-marking a
        # death as a timeout over six seconds later.
        if rec.get("status", "running") not in (None, "running"):
            continue
        started = int(rec.get("started_at", 0) or 0)
        if started <= 0:
            continue
        elapsed = int(time.time()) - started
        if elapsed <= timeout_s:
            continue
        pid = int(rec.get("pid", 0) or 0)
        # Residue (a): a dead pid past its deadline is DEATH, never a timeout
        # overwrite. `_reap_pass` may have seen it alive and left it in
        # `still`; if it has since died, record the death (one status, one dm)
        # instead of mis-recording the elapsed time as a timeout.
        if pid > 0 and not adapter.is_alive(pid):
            death = {
                "status": "failed",
                "finished_at": int(time.time()),
                "fail_reason": f"pid {pid} died (detected by reaper)",
            }
            rec.update(death)
            rec_path.write_text(json.dumps(rec, indent=2))
            for entry in manifest.get("agents", []):
                if entry.get("id") == agent_id:
                    entry["status"] = "failed"
                    entry["finished_at"] = rec["finished_at"]
                    entry["fail_reason"] = rec["fail_reason"]
            manifest_path.write_text(json.dumps(manifest, indent=2))
            _alarm_dispatcher(rec, iter_dir.name, "death", root)
            _watch_log(f"watch: iter={iter_dir.name} agent={agent_id} marked "
                       f"DEAD past deadline ({rec['fail_reason']}; "
                       f"dispatched_by={rec.get('dispatched_by') or '-'})")
            continue
        # hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal — a
        # LIVE pid past its deadline is OVERDUE, never terminal. The watcher
        # does not TERM (kill is the round's own declared choice), so a
        # `timeout` mark here would be a terminal word on a pid that is still
        # working — which the pi parent reads as a licence to cut a REPLACEMENT
        # kid into the same worktree (L4.155/L4.156: two kids editing one file
        # set). A live agent keeps status `running`, gains `overdue_since` +
        # `overdue_reason`, gets EXACTLY ONE dm whose body is
        # `iter=... agent=... reason=overdue` (`[agi-nudge]` is the wake-token
        # prefix the nudge path adds, not part of the body; the `overdue_since`
        # guard never admits a second), and the parent brief names `overdue`
        # as still-working so no replacement is cut. The admin heap
        # path that actually TERMs a hung pid is the one place a `timeout`
        # verdict is legal; the watcher never derives it.
        if rec.get("overdue_since"):
            _watch_log(f"watch: iter={iter_dir.name} agent={agent_id} STILL "
                       f"OVERDUE (elapsed {elapsed}s > {timeout_s}s; "
                       f"pid {pid} alive)")
            continue
        rec["overdue_since"] = int(time.time())
        rec["overdue_reason"] = (f"past manifest timeout_seconds={timeout_s} "
                                  f"at {elapsed}s; pid {pid} still alive")
        rec_path.write_text(json.dumps(rec, indent=2))
        for entry in manifest.get("agents", []):
            if entry.get("id") == agent_id:
                # status STAYS running — never a terminal word for a live pid.
                entry.setdefault("status", "running")
                entry["overdue_since"] = rec["overdue_since"]
                entry["overdue_reason"] = rec["overdue_reason"]
        manifest_path.write_text(json.dumps(manifest, indent=2))
        # hypothesis:l4-a-round-alarms-its-dispatcher-by-default — ONE dm per
        # event, through heal.py's own L4.113 helper. No stamp -> the helper
        # logs a warn line and returns; never silence, never crash.
        _alarm_dispatcher(rec, iter_dir.name, "overdue", root)
        _watch_log(f"watch: iter={iter_dir.name} agent={agent_id} marked "
                   f"OVERDUE (elapsed {elapsed}s > {timeout_s}s; pid {pid} "
                   f"alive; dispatched_by={rec.get('dispatched_by') or '-'})")


def _run_pending_after_joins(root: Path) -> None:
    """hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-
    hook-fires-at-turn-one, owed (i): the WATCH loop IS the service when
    `agent_dispatch.inline_reaper` is false, so it performs the captive
    after_join for any seat whose latest rotation record has not yet had its
    after_join run and is past its `after_join_delay_s`. Invokes the SAME
    `rotate.run_after_join_for_seat` the rotate-self fallback caller uses —
    one function, no parallel driver. Read-only discovery; best-effort; never
    raises into the watch loop. No seats / no rotate module -> silent no-op."""
    try:
        import rotate as _rotate
    except Exception:                                    # noqa: BLE001
        return
    try:
        if _rotate._inline_reaper_enabled(root):
            return  # an inline reaper / rotate-self owns after_join
    except Exception:                                    # noqa: BLE001
        return
    try:
        rows = _rotate._load_seats(root) or []
    except Exception:                                    # noqa: BLE001
        return
    for row in rows:
        seat = row.get("name") or row.get("seat")
        if not seat:
            continue
        try:
            result = _rotate.run_after_join_for_seat(root, seat)
        except Exception as exc:                         # noqa: BLE001
            print(f"warn: after_join for {seat!r} failed: {exc}",
                  file=sys.stderr)
            continue
        if result is not None:
            if result.get("skipped"):
                # (goal:g15.25 SL7.76 (a)) exactly ONE line for a definitely-
                # dead seat with no live session — no record append, no dm.
                _watch_log(f"after_join skipped for {seat!r}: "
                           f"{result['skipped']}")
            else:
                _watch_log(f"watch: after_join performed for seat {seat!r} "
                           f"({len(result.get('results') or [])} command(s); "
                           f"record appended: {result.get('appended')}, "
                           f"dm sent: {result.get('sent')})")


def _sweep_season(branch: str) -> int | None:
    """Season from a loop branch name, NEW (`season<n>/loops/<slug>-<agent>`)
    or OLD (`loop/<slug>-<agent8>@s<N>`), or None. Old names are accepted, never
    refused: an old round's worktree is never dropped because its branch
    spelling changed. Used to fall back to the round's base when the worktree's
    own session records no `base_branch`."""
    if not branch:
        return None
    try:
        parsed = branches.parse(branch)
        if parsed.get("kind") == "loop" and parsed.get("season") is not None:
            return parsed["season"]
    except ValueError:
        pass
    # legacy `loop/<slug>-<agent8>@s<N>`: pull the @s<N> suffix directly
    m = re.search(r"@s(\d+)\s*$", branch)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def _sweep_resolve_base(root: Path, base: str) -> str:
    """Resolve `origin/...` season-trunk base to a LIVE ref the ancestry check
    can prove against, accepting the old `origin/season/s<N>` spelling (via
    ref_candidates, canonical first) so a tree not yet renamed still resolves.
    Non-origin bases (a recorded base_branch) pass through unchanged."""
    if not base.startswith("origin/"):
        return base
    local = base[len("origin/"):]
    for name in branches.ref_candidates(local):
        probe = f"origin/{name}"
        _, rc = _git(["rev-parse", "--verify", f"{probe}^{{commit}}"], root)
        if rc == 0:
            return probe
    return base


def _git(args: list[str], cwd: Path) -> tuple[list[str], int]:
    """`git <args>` run in `cwd`, returning (stdout lines, returncode).
    Best-effort: a broken git yields (empty, nonzero), never raises."""
    try:
        out = subprocess.run(["git", "-C", str(cwd), *args],
                             capture_output=True, text=True)
    except (OSError, subprocess.SubprocessError):
        return [], 1
    return (out.stdout or "").splitlines(), out.returncode


def _sweep_worktree_base(root: Path, wt: Path, season: int | None) -> str | None:
    """The branch this round was cut from, for the ancestry check.

    Prefers the `base_branch` dispatch wrote into the worktree's own session
    records (the same tuple season.py merge-up climbs); falls back to
    `origin/season/s<N>` from the loop branch. None means the round's base
    cannot be resolved, so its worktree is NOT removed (a round whose landing
    cannot be proven must not be reaped)."""
    sess = wt / ".agi" / "sessions"
    if sess.is_dir():
        for it in sorted(sess.glob("iter-*")):
            ap = it / "agent.json"
            if ap.exists():
                try:
                    bb = json.loads(ap.read_text()).get("base_branch")
                except (json.JSONDecodeError, OSError):
                    bb = None
                if bb:
                    return bb
            mp = it / "manifest.json"
            if mp.exists():
                try:
                    man = json.loads(mp.read_text())
                except (json.JSONDecodeError, OSError):
                    man = {}
                for e in man.get("agents") or []:
                    bb = e.get("base_branch")
                    if bb:
                        return bb
    if season is not None:
        return f"origin/{branches.season_main(season)}"
    return None


def _sweep_iter_name(wt: Path) -> str:
    """The round's iter-dir name as carried in the worktree, or `?` when the
    worktree has none (the `worktree carries no iter-* dir` condition)."""
    dirs = sorted(wt.glob(".agi/sessions/iter-*"))
    return dirs[0].name if dirs else "?"


def _sweep_dirty_paths(status_lines: list[str]) -> list[str]:
    """The `git status --porcelain` entries that are NOT under a worktree's
    own `.agi/sessions/` (per-worktree session scratch is the one tolerated
    residue; everything else makes the tree dirty and therefore unremovable
    without `--force`)."""
    dirty: list[str] = []
    for ln in status_lines:
        path = ln[3:].strip().strip('"')
        if path.startswith(".agi/sessions/"):
            continue
        dirty.append(path)
    return dirty


# session-complete refusal markers we reduce to short named reasons in the
# `[sweep] refused ... session dir not home (<reason>)` line. Order matters:
# the FIRST match below wins for a refusal whose stdout carries more than one.
def _sweep_refusal_reason(text: str) -> str:
    for needle, tag in (
        (" is not terminal", "non-terminal"),
        ("no manifest.json in any source", "no manifest"),
        ("target already exists and is not empty", "target exists"),
        ("a live lease is active", "live lease"),
        ("this source's own contribution did not verify", "verify failed"),
    ):
        if needle in text:
            return tag
    return "home failed"


def _sweep_iter_home(wt_iter: Path, target: Path) -> bool:
    """Is THIS worktree's copy of the round's session dir genuinely HOME —
    its own contribution byte-equal under the main target?

    The fix for the empty/foreign-placeholder DATA-LOSS defect in condition
    (4): `home` must never be proven by a bare `is_dir()` on the main target.
    An EMPTY pre-created placeholder (dispatch pre-creates one), or a FOREIGN
    dir a `--branch` round's OTHER tree already filled, both would satisfy a
    bare `is_dir()`, so the bring-home was never attempted and `git worktree
    remove` reaped the tree WITH ITS OWN UNMIGRATED RECORDS — exactly the
    outcome cli._session_complete exists to prevent.

    Proof is PER-SOURCE, the same shape cli._source_landed uses to free a
    source, without needing the full merge plan: every migratable file under
    `wt_iter` (cli._migratable: everything but `.manifest.lock`; cli imported
    LAZILY, never at module import — heal must not load it at import time)
    must exist under `target` with EQUAL BYTES — at `target/rel` (the winner
    path) or at the two-tree loser path
    `target/.conflicts/<rel>.from-<cli._src_slug(wt_iter)>`. An absent or
    EMPTY target, or any missing/unequal file, is NOT home (fail CLOSED: the
    bring-home runs). A `wt_iter` that no longer EXISTS is home by
    session-complete's own contract — it removes a source only after its own
    contribution byte-verifies.
    """
    if not wt_iter.exists():
        return True  # session-complete removed it only after verification
    if not target.is_dir():
        return False
    try:
        import cli as _cli  # noqa: E402 — never at module import (see below)
        slug = _cli._src_slug(wt_iter)
        files = [p for p in wt_iter.rglob("*")
                 if p.is_file() and _cli._migratable(p.relative_to(wt_iter))]
    except Exception:  # noqa: BLE001 — a broken cli is not proof of home
        return False
    if not files:
        return False  # an existing source with no migratable file proves
        # nothing landed; fail CLOSED so the bring-home is attempted
    try:
        for sp in files:
            rel = sp.relative_to(wt_iter)
            loc = target / rel
            if loc.is_file() and loc.read_bytes() == sp.read_bytes():
                continue
            loser = target / ".conflicts" / f"{rel}.from-{slug}"
            if loser.is_file() and loser.read_bytes() == sp.read_bytes():
                continue
            return False
    except OSError:
        return False
    return True


def _sweep_bring_home(root: Path, main_sessions: Path, wt_iter: Path,
                      dry_run: bool, homed: dict) -> str | None:
    """hypothesis:l4-a-finished-rounds-session-dir-comes-home-before-the-\
sweep-judges-it.

    Bring a NOT-home round's session dir home via `cli._session_complete`, the
    one sanctioned caller of that normally-manual command. Resolves `root`
    (the main graph root the sweep already holds), calls it ONCE PER
    ITERATION per pass (the `homed` memo guards a `--branch` round whose
    iter dir sits in TWO worktrees -- `worktree=None` lets the one call
    merge every source into one target). session-complete's OWN guards stay
    the authority and are neither duplicated nor bypassed: no live lease for
    the iteration, every agent record terminal, target not already
    non-empty, copy-then-verify-then-remove-each-source-by-its-own-
    contribution. Returns None when the iter dir came home (or would, in a
    dry run); else a short refusal reason for the `session dir not home` log.
    Never writes anything itself -- the migrate is session-complete's, this
    only decides by its captured stdout (dry-run) or the on-disk target.
    HOME is proven PER-SOURCE and byte-exact (_sweep_iter_home), never a bare
    `is_dir()` on the target -- an EMPTY placeholder or a FOREIGN dir is not
    home, so the bring-home runs instead of reaping the tree with its own
    unmigrated records (hyp:l4-a-finished-rounds-worktree-is-removed-after-
    harvest, L4.257).
    """
    iter_name = wt_iter.name
    if iter_name in homed:
        # already attempted this pass; the memoized outcome holds, but the
        # on-disk target is always re-read because a sibling may have landed
        # it. A memoized "" means the iter came home (or WOULD, in a dry run
        # where nothing is on disk) -- the second tree of a two-tree round is
        # then home too, never refused with an empty reason (harvest fix,
        # L4.255). A re-read is a REAL proof, never a bare is_dir (L4.257).
        if homed[iter_name] == "" or _sweep_iter_home(
                wt_iter, main_sessions / iter_name):
            return None
        return homed[iter_name]
    try:
        import cli as _cli  # noqa: E402 — cli imports evidence_gate/locations/
        # spawn_budget, so heal must NOT load it at module import time
    except Exception as exc:  # noqa: BLE001
        homed[iter_name] = f"cli import failed ({exc})"
        return homed[iter_name]
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cli._session_complete(
                root, locations.iteration_id(iter_name),
                worktree=None, dry_run=dry_run)
        text = buf.getvalue()
    except Exception as exc:  # noqa: BLE001 — session-complete raised
        homed[iter_name] = f"home failed (raised: {exc})"
        return homed[iter_name]
    if dry_run:
        # a dry-run session-complete returns 0 for would-migrate, REFUSE and
        # no-candidate alike -- decide by the CAPTURED stdout, never the rc.
        if "WOULD migrate" in text and "REFUSE" not in text:
            homed[iter_name] = ""
            return None
        homed[iter_name] = _sweep_refusal_reason(text)
        return homed[iter_name]
    # LIVE: only the on-disk target is the proof, never a return code. HOME is
    # per-source and byte-exact (_sweep_iter_home), never a bare is_dir -- an
    # EMPTY placeholder or a foreign dir must still drive a home attempt
    # instead of reaping the tree with its own unmigrated records (L4.257).
    if not wt_iter.exists() or _sweep_iter_home(
            wt_iter, main_sessions / iter_name):
        homed[iter_name] = ""
        return None
    homed[iter_name] = _sweep_refusal_reason(text)
    return homed[iter_name]


def _sweep_finished_worktrees(root: Path, dry_run: bool = False,
                              grace_min: int | None = None
                              ) -> tuple[int, int, int]:
    """hypothesis:l4-a-finished-rounds-worktree-is-removed-after-harvest.

    ONE pass over the main checkout's agent worktrees under
    `<graph>/worktrees/a00-*`, removing each FINISHED round's worktree when
    ALL hold:
      (1) no live spawn-budget lease names the agent (the lease dir is the
          liveness source, never ps by name);
      (2) the worktree's HEAD is an ancestor of the branch it was cut from
          (a round that never landed is NOT removed -- `unmerged`);
      (3) `git status --porcelain` is empty apart from `.agi/sessions/`
          paths (a dirty tree is REFUSED by name, never forced);
      (4) the round's session dir has come home to the main checkout, or
          the worktree carries no `iter-*` dir at all;
      (5) the worktree directory is older than the grace
          (`reaper.worktree_grace_min`, default 30; `.agi/config.json` is
          read, never edited).
    Removal is `git -C <main> worktree remove <wt>` WITHOUT `--force`, then
    `git worktree prune`; the `loop/...` branch is KEPT (refs are history).
    `--dry-run` logs the same `[sweep] removed` lines and removes nothing.
    Logs one `[sweep]` line per action and a per-pass summary. Never raises
    into the watch loop. Returns `(removed, refused, kept)`."""
    removed = refused = kept = 0
    wt_base = root / "worktrees"
    if not wt_base.is_dir():
        return (0, 0, 0)
    main_checkout = locations.git_common_root(root)
    if grace_min is None:
        grace_min = 30
        try:
            cfg_path = locations.config_path(root)
            if cfg_path is not None:
                cfg = json.loads(cfg_path.read_text())
                grace_min = int(cfg.get("reaper", {}).get(
                    "worktree_grace_min", grace_min))
        except (ValueError, TypeError, OSError, json.JSONDecodeError):
            pass  # a malformed grace -> the default stays
    try:
        live_ids = {r.get("agent_id") for r in
                    spawn_budget.live_agents(root) if r.get("agent_id")}
    except Exception as exc:  # noqa: BLE001 — an unreadable budget must NOT
        # open a removal window. Fail CLOSED: skip the whole sweep this pass --
        # every worktree stays, live lease or not. `live_ids = set()` here would
        # wrongly treat every agent as dead and let a merged+clean+grace-old
        # live worktree be removed under a transient budget failure.
        _watch_log(f"[sweep] skipped: budget unreadable ({exc})")
        return (0, 0, 0)
    main_sessions = locations.sessions_dir(root)
    homed: dict[str, str] = {}  # iter dirname -> "" (home) | refusal reason,
    # memoized per pass so a `--branch` round's TWO trees home its iter dir ONCE
    now = time.time()
    # Pre-resolve each worktree's BASE (the branch it was cut from) READ-ONLY
    # BEFORE any bring-home runs. A `--branch` round's single merge-home
    # (session-complete, worktree=None) removes the iter dir from EVERY tree it
    # was found in, so a second tree's records would be gone by its turn in the
    # loop -- pre-resolving here (hyp:l4-a-finished-rounds-session-dir-comes-
    # home-before-the-sweep-judges-it) keeps every tree's ancestry provable.
    base_pre: dict[str, str] = {}
    for wt_p in sorted(wt_base.glob("a00-*")):
        if not wt_p.is_dir():
            continue
        b0, _ = _git(["rev-parse", "--abbrev-ref", "HEAD"], wt_p)
        base_pre[wt_p.name] = _sweep_worktree_base(
            root, wt_p, _sweep_season(b0[0] if b0 else ""))
    for wt in sorted(wt_base.glob("a00-*")):
        if not wt.is_dir():
            continue
        agent_id = wt.name
        # (1) liveness from the shared lease dir, never ps by name.
        if agent_id in live_ids:
            kept += 1
            _watch_log(f"[sweep] kept {agent_id}: live")
            continue
        branch_lines, _ = _git(["rev-parse", "--abbrev-ref", "HEAD"], wt)
        branch = branch_lines[0] if branch_lines else ""
        season = _sweep_season(branch)
        base = base_pre.get(agent_id, _sweep_worktree_base(root, wt, season))
        if base:
            base = _sweep_resolve_base(root, base)
        if not base:
            refused += 1
            _watch_log(f"[sweep] refused {agent_id}: unmerged (no base)")
            continue
        head_lines, _ = _git(["rev-parse", "HEAD"], wt)
        head = head_lines[0] if head_lines else ""
        # (2) a round that never landed is NOT removed.
        if not head:
            refused += 1
            _watch_log(f"[sweep] refused {agent_id}: unmerged (no HEAD)")
            continue
        _, anc_rc = _git(["merge-base", "--is-ancestor", head, base],
                         main_checkout)
        if anc_rc != 0:
            refused += 1
            _watch_log(f"[sweep] refused {agent_id}: unmerged")
            continue
        # (3) a dirty tree is REFUSED by name, never forced.
        status_lines, _ = _git(["status", "--porcelain"], wt)
        dirty = _sweep_dirty_paths(status_lines)
        if dirty:
            refused += 1
            _watch_log(f"[sweep] refused {agent_id}: dirty "
                       f"({len(dirty)} paths)")
            continue
        # (4)/(5) A finished round's session dir comes home before the sweep
        # judges condition (4): for a leaseless+merged+clean round, the GRACE
        # check moves AHEAD of the bring-home step, so a director's hand
        # harvest inside the 30-minute window is never raced by the reaper --
        # only a past-grace round is ever homed (or reaped) by the sweep.
        # The worktree directory must be older than the configured grace.
        try:
            age_min = (now - wt.stat().st_mtime) / 60.0
        except OSError:
            age_min = 0.0
        if age_min < grace_min:
            kept += 1
            _watch_log(f"[sweep] kept {agent_id}: grace "
                       f"({age_min:.0f}m < {grace_min}m)")
            continue
        # (4) the round's session dir must have come home (or there is none).
        # HOME is PER-SOURCE and byte-exact (_sweep_iter_home), never a bare
        # is_dir on the main target -- an EMPTY placeholder or a FOREIGN dir
        # is NOT home, so the bring-home runs instead of the tree being reaped
        # with its own unmigrated records (hyp:l4-a-finished-rounds-worktree-
        # is-removed-after-harvest, L4.257).
        wt_iters = sorted(wt.glob(".agi/sessions/iter-*"))
        if wt_iters:
            not_home = [d for d in wt_iters
                        if not _sweep_iter_home(d, main_sessions / d.name)]
            if not_home:
                rejected: list[str] = []
                homed_now: set[str] = set()
                for dn in not_home:
                    reason = _sweep_bring_home(root, main_sessions, dn,
                                               dry_run, homed)
                    iter_nm = dn.name
                    if reason is None:
                        homed_now.add(iter_nm)
                        _watch_log(f"[sweep] homed {agent_id} iter={iter_nm}")
                    else:
                        rejected.append(f"{iter_nm}:{reason}")
                # condition (4) is re-read from DISK for a LIVE pass; a
                # dry-run wrote nothing, so a would-home (helper returned
                # None) counts as home for the removal decision here.
                remaining = [d.name for d in wt_iters
                             if not _sweep_iter_home(d, main_sessions / d.name)
                             and d.name not in homed_now]
                if remaining:
                    refused += 1
                    _watch_log(f"[sweep] refused {agent_id}: session dir not "
                               f"home ({','.join(rejected)})")
                    continue
        iter_name = _sweep_iter_name(wt)  # read BEFORE the dir is freed
        if dry_run:
            _watch_log(f"[sweep] removed {agent_id} "
                       f"iter={iter_name} base={base} (dry-run)")
            removed += 1
            continue
        _, rm_rc = _git(["worktree", "remove", str(wt)], main_checkout)
        if rm_rc != 0:
            refused += 1
            _watch_log(f"[sweep] refused {agent_id}: remove failed")
            continue
        _git(["worktree", "prune"], main_checkout)
        _watch_log(f"[sweep] removed {agent_id} "
                   f"iter={iter_name} base={base}")
        removed += 1
    _watch_log(f"sweep: removed={removed} refused={refused} kept-live={kept}")
    return (removed, refused, kept)


def _watch(root: Path, once: bool = False, poll_s: int = 30) -> None:
    """The persistent watcher loop. Discovers rounds, reaps each, sleeps. The
    UNIT runs this without `--once`; the tests drive `--once` (one pass, exit).
    """
    adapter = _WatcherAdapter()
    while True:
        rounds = _discover_rounds(root)
        for iter_dir, _mp in rounds:
            _watch_round(root, iter_dir, adapter)
        # hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter:
        # the watch pass ALSO repairs stranded seat wakes (a rotation-alert
        # that landed in a BUSY recipient's dm and never woke it). `wake` is
        # read-only and silent when there is nothing to deliver, so polling
        # every configured seat row every pass costs nothing when nothing is
        # stranded and repairs a strand within ONE poll (30 s) with no
        # operator. The reaper logic above is untouched.
        _repair_stranded_wakes(root)
        _run_pending_after_joins(root)
        # hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human
        # (kid 1 of 2): the SAME seat rows the wake repair reads are now
        # scanned for a DEAD seat each pass — pid gone, window @id gone (the
        # live-first row; (1c) name-lineage deleted, prime XI 19:38Z), no
        # rotation in flight — and the dead seat is NAMED once and recorded
        # as a `crash-recovery` rotation record (the once-guard). kid 2 owns
        # the respawn half.
        _watch_seats(root)
        # hypothesis:l4-the-pin-is-the-lease (kid 2): ONCE per pass, right
        # after the dead-seat scan, run the pin/lease reap pass. MODE is read
        # from `.agi/config.json` `reaper.pin_reap` (absent/dry-run = LIST
        # ONLY; armed = reap rotate helpers + one dm); exactly ONE call site.
        _pin_reap_pass(root)
        # hypothesis:l4-a-finished-rounds-worktree-is-removed-after-harvest:
        # once per pass, sweep finished rounds' worktrees. Run unconditionally
        # (never gated on inline_reaper) so a harness that harvests with raw
        # `git merge` still gets its residue cleaned by the persistent
        # watcher. Best-effort; never raises into the watch loop.
        _sweep_finished_worktrees(root)
        if once:
            break
        _watch_log(f"watch: pass complete over {len(rounds)} round(s); "
                   f"sleeping {poll_s}s")
        time.sleep(poll_s)


def _main_watch() -> int:
    ap = argparse.ArgumentParser(prog="heal.py watch")
    ap.add_argument("--root", type=str, default=".",
                    help="the main checkout / graph root to watch")
    ap.add_argument("--poll-s", type=int, default=30)
    ap.add_argument("--once", action="store_true",
                    help="run ONE pass over every live round, then exit")
    # `main()` already consumed the leading `watch` token; parse what follows.
    args = ap.parse_args(sys.argv[2:])
    given = Path(args.root).resolve()
    root = locations.find_project_root(given) or given
    _watch(root, once=args.once, poll_s=args.poll_s)
    return 0


def _main_sweep() -> int:
    ap = argparse.ArgumentParser(prog="heal.py sweep")
    ap.add_argument("--root", type=str, default=".",
                    help="the main checkout / graph root to sweep")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be removed, remove nothing")
    # `main()` already consumed the leading `sweep` token; parse what follows.
    args = ap.parse_args(sys.argv[2:])
    given = Path(args.root).resolve()
    root = locations.find_project_root(given) or given
    removed, refused, kept = _sweep_finished_worktrees(root,
                                                       dry_run=args.dry_run)
    print(f"sweep: removed={removed} refused={refused} kept-live={kept}")
    return 0


def _repair_stranded_wakes(root: Path) -> None:
    """hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter --
    the watch pass's seat-wake repair. For every configured live seat row this
    calls `send.wake(<seat>)`, which resubmits a stranded nudge-shaped line
    in an IDLE pane (typed space + Enter, never Enter-only) or re-types the
    wake token for a seat with unread, and silently no-ops on a pane with
    nothing pending. Best-effort and read-only: missing seats / no tmux /
    busy panes are silent no-ops; never touches the reaper logic, never
    raises out of the watch loop."""
    try:
        import send as _send
    except Exception:                                     # noqa: BLE001
        return
    try:
        rows = _send._locally_loaded_rows(root) or []
    except Exception:                                     # noqa: BLE001
        return
    for row in rows:
        seat = row.get("name") or row.get("seat")
        if not seat:
            continue
        try:
            _send.wake(root, seat)
        except Exception as exc:                          # noqa: BLE001
            print(f"warn: wake repair for {seat!r} failed: {exc}",
                  file=sys.stderr)


# --- heal.py watch: dead-seat detection + classification + record -----
# hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human (kid 1 of
# 2: DETECT + CLASSIFY + RECORD; the respawn half is kid 2, a serial sibling
# spawned only after this node merges). The persistent watch pass already
# reads every seat row each poll; THIS pass decides which seat is DEAD (pid
# gone + window @id gone + no window named for the seat + no rotation in
# flight), reads a `probable_cause` from the tail of the seat's session log
# through an ordered signature table, NAMES the dead seat ONCE, and writes ONE
# durable `crash-recovery` rotation record that is ALSO the once-guard (a
# second pass never re-names / re-records). A row carrying `recover: false`
# is NAMED but never recorded as an action; absent means recover. This half
# never respawns — spawn is kid 2.

#: Test seam for the window list: a window-path file (one `@<N> <name>` or
#: bare `<name>` line per window) the same way rotate.py's `--window-path`
#: seams real tmux. Live passes read `tmux list-windows -a`, so a successor
#: window under any session is still seen (1c reads ACROSS sessions).
WINDOW_PATH_ENV = "AGI_WINDOW_PATH"

#: A `started` rotation record within this window means a rotation in flight,
#: not a crash (1d).
SEAT_DEAD_WINDOW_S = 600

#: Ordered signature table for `probable_cause`, keyed on literal substrings
#: in the tail of the seat's session log; first match wins, else `unknown`.
#: `must_also` guards a signature whose marker is only meaningful alongside
#: another (a pytest probe that reached cmd_rotate_self). Each entry is
#: `(cause, any_of, all_also)`.
_CAUSE_SIGNATURES = [
    ("pane-local-pytest-reap",
     ("cmd_rotate_self",), ("pytest_current_test", "test_probe", "pytest ")),
    ("idle-external-teardown",
     ("uds shutdown", "epoch mismatch (409, session_not_active)",
      "updatepidfile"), ()),
    ("remote-control-disconnect",
     ("disconnect", "connection closed"), ()),
]


def _classify_death(tail: str) -> str:
    """probable_cause for a dead seat from the tail of its session log.
    Literal-substring ordered table, first match wins, else `unknown`.
    Never guesses: an unmatched tail is `unknown`, never a made-up cause."""
    t = tail.lower()
    for cause, any_of, must_also in _CAUSE_SIGNATURES:
        if any(s in t for s in any_of):
            if not must_also or any(s in t for s in must_also):
                return cause
    return "unknown"


def _all_windows(window_path: str | None = None) -> list[tuple[str, str]]:
    """`[(window_id, window_name), ...]` across EVERY tmux session, or from
    the window-path test seam (`AGI_WINDOW_PATH` / explicit `window_path`):
    one `@<N> <name>` or bare `<name>` line per window. `-a` lists windows in
    all sessions so a successor's window under another session is still seen."""
    if window_path is None:
        window_path = os.environ.get(WINDOW_PATH_ENV)
    if window_path:
        p = Path(window_path)
        if not p.exists():
            return []
        out: list[tuple[str, str]] = []
        for ln in p.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            if ln.startswith("@"):
                wid, _, name = ln.partition(" ")
                out.append((wid.strip(), name.strip()))
            else:
                out.append(("", ln))
        return out
    try:
        res = subprocess.run(
            ["tmux", "list-windows", "-a", "-F", "#{window_id} #{window_name}"],
            capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            out = []
            for ln in res.stdout.splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                wid, _, name = ln.partition(" ")
                out.append((wid.strip(), name.strip()))
            return out
    except Exception:  # noqa: BLE001 — tmux absent/down: [] (pid gate is primary)
        pass
    return []


def _window_present(row: dict,
                    windows: list[tuple[str, str]]) -> tuple[bool, bool]:
    """(1b) the row's `window` @id is present in tmux. Returns
    `(id_present, False)` — the second cell is the DELETED (1c) name-lineage
    check, kept in the tuple shape so callers/tests read unchanged.

    (1c) matched any window named `<seat>` or `<seat>-…`. PRIME XI RULING
    2026-09-11 19:38Z (mur-40 window): a tmux window NAME IS NOT AN ADDRESS.
    For a numeral-chain seat the predecessor chain (belam-S1-L4-V … -XI) is
    an OWNER STANDING RULE — rotated primes idle in their windows, capped at
    five, never killed — so a name-lineage test is satisfied by every
    predecessor forever and crash-recovery for the prime was structurally
    dead, not merely masked (measured by the L4.283 harvest: belam with @289
    removed still read named=True). Its only justification was the worktree
    row lag (a live successor whose row has not merged up yet), and the row
    handed here is already read LIVE-FIRST from the seat's own worktree
    (`_live_seat_row`), so (1b) on that row is the whole check. Interim per
    the ruling until identity cells get one writer that writes MAIN; the
    falsifier is a corpse detected WITH the predecessor windows still open."""
    win_id = (row.get("window") or "").strip()
    id_present = bool(win_id) and any(
        w == win_id for (w, _n) in windows)
    return id_present, False


def _parse_record_ts(s: str) -> float | None:
    """Parse a rotation record `recorded_at`; None when unparsable.
    The `Z` suffix is UTC (rotate.py writes `datetime.utcnow().isoformat() +
    "Z"`), so a UTC-stamped record must NOT be read as local time on a
    non-UTC host (this box is EST). Naive-local (timezone-less) timestamps
    are a tolerated fallback for hand-written records."""
    for body in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.datetime.strptime(s, body + "Z")
            return dt.replace(tzinfo=datetime.timezone.utc).timestamp()
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(s, body).timestamp()
        except ValueError:
            continue
    return None


def _seat_geometry_dir(root: Path, row: dict) -> Path:
    """The seat's own geometry root (the dir whose `nodes/` holds its seats
    file and whose `sessions/` holds its live session log). For a worktree
    seat that is the worktree's own `.agi` (live-first, F2), else `root`."""
    wt = (row.get("worktree") or "").strip()
    if wt:
        gdir = Path(root) / "worktrees" / Path(wt).name / ".agi"
        if gdir.is_dir():
            return gdir
    return Path(root)


CRASH_LOOP_MAX_PER_HOUR = 3


def _crash_recovery_recorded(root: Path, seat: str, _rotate,
                             now: float | None = None) -> bool:
    """The once-guard, keyed on a RESPAWN OUTCOME, never on mere detection
    (the defect kid 2 holds) — and BOUNDED IN TIME, never "ever". A
    `crash-recovery` record whose `result` is `respawned` within the last
    `SEAT_DEAD_WINDOW_S` (10 min, the same window (1d) grants a rotation in
    flight) means the loop already healed this death and the successor is
    still waking -> a second pass must not re-name, re-record or re-spawn.
    An OLDER `respawned` record does NOT suppress: found by the L4.283
    harvest's live proof (sanctuary-director 182119Z 19:29Z) — on the round's
    bytes the guard scanned every record ever written, so the FIRST recovery
    of a seat was also its LAST (the recovered successor's own death, minutes
    later, read `0 dead` forever). A `result: detected`-only record never
    suppresses (the spawn failed or was never attempted; the NEXT pass must
    retry). CRASH LOOP: `CRASH_LOOP_MAX_PER_HOUR` or more `respawned` records
    in the last hour -> suppressed and NAMED in the watch log, because a seat
    that dies every few minutes is a finding for a human, not a spawn budget
    (the Belam cap of FIVE bounds the numeral chain the same way)."""
    rot = _rotate._rotations_dir(root)
    if not rot.is_dir():
        return False
    now = now if now is not None else time.time()
    recent: list[float] = []
    for path in sorted(rot.glob(f"{seat}.*.json")):
        try:
            rec = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if (rec.get("rotation") != "crash-recovery"
                or rec.get("result") != "respawned"):
            continue
        ts = _parse_record_ts(rec.get("recorded_at", ""))
        if ts is None:
            continue
        if (now - ts) <= SEAT_DEAD_WINDOW_S:
            return True
        if (now - ts) <= 3600:
            recent.append(ts)
    if len(recent) >= CRASH_LOOP_MAX_PER_HOUR:
        _watch_log(f"watch: seat {seat!r}: {len(recent)} crash-recoveries in the "
             "last hour -- CRASH LOOP, not respawning again; a human decides")
        return True
    return False


def _rotation_before_after(rec: dict) -> tuple:
    """The (before, after) generation on a rotation record, ONE shared
    extraction. Prefers top-level `gen_before`/`gen_after`, falling back to
    the NESTED `observations.b_generation.before/after` (the real incident
    shape -- sensei-director.20260912T000346Z.json carries its generation
    ONLY nested; top-level gens are null). NEVER a second inline copy of the
    fallback (hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-
    rotation-record-before-declaring-a-crash)."""
    before = rec.get("gen_before")
    after = rec.get("gen_after")
    if before is None or after is None:
        obs = rec.get("observations") or {}
        bg = obs.get("b_generation") if isinstance(obs, dict) else None
        if isinstance(bg, dict):
            if before is None:
                before = bg.get("before")
            if after is None:
                after = bg.get("after")
    return before, after


def _record_join(rec: dict) -> dict:
    """The ONE rotation-record join accessor — rotate.py's copy, imported by
    name (g15.26 (d): heal's same-named twin is deleted so a SINGLE definition
    serves both modules). Pid is STR-COERCED and a crash-recovery record's
    TOP-LEVEL `window_id` is read, exactly as heal's own copy did — widening
    rotate's was the merge, not keeping two. Missing/malformed fields never
    raise; absent join identity yields an empty dict.
    Reads BOTH durable record shapes:
      rotate-self:   `handover.join.{pid,window_id}` and
                     `handover.successor_window.id`
      crash-recovery: TOP-LEVEL `window_id` ONLY (the producer writes no
                     top-level pid/session_id — see test_heal_watch).
    The crash-recovery branch stays UNREACHABLE from the watcher (rotate's
    `_rotation_record_files` excludes those records) — it exists for direct
    accessor tests and any future reader that bypasses the exclusion; do NOT
    lower the guard (experiment:a00-8584ff07-645be9)."""
    import rotate as _rotate  # noqa: PLC0415  (heal's local-import pattern)
    return _rotate._record_join(rec)


def _rotation_identity(rec: dict) -> tuple[list, list, list, list]:
    """Extract the rotation record's identity fields ONCE, nothing else:
    returns `(pred_pids, pred_windows, succ_pids, succ_windows)`.
    - pred_* : the RETIRED predecessor's identity -- `s12_self_reap.chain[*].pid`
      (its process chain) and `handover.own_window.id` (its window @id).
    - succ_* : the SUCCESSOR's identity -- read through the single `_record_join`
      accessor (`handover.join.pid` / `handover.join.window_id` /
      `handover.successor_window.id` on a rotate-self record; a crash-recovery
      record contributes its TOP-LEVEL `window_id` ONLY -- it carries no
      top-level pid/session_id), so BOTH shapes yield what each actually
      writes, nothing more.
    Missing or malformed `s12_self_reap`/`handover` never raises -- absent
    identity simply yields empty lists (an OLDER record with no identity
    fields), which the caller treats as the gen/age fallback."""
    pred_pids: list = []
    pred_windows: list = []
    succ_pids: list = []
    succ_windows: list = []
    reap = rec.get("s12_self_reap")
    if isinstance(reap, dict):
        for c in reap.get("chain") or []:
            if isinstance(c, dict) and c.get("pid") is not None:
                pred_pids.append(str(c.get("pid")))
    hand = rec.get("handover")
    if isinstance(hand, dict):
        ow = hand.get("own_window")
        if isinstance(ow, dict) and ow.get("id") is not None:
            pred_windows.append(str(ow.get("id")))
    jn = _record_join(rec)
    if jn.get("pid") is not None:
        succ_pids.append(jn["pid"])
    if jn.get("window_id") is not None:
        succ_windows.append(jn["window_id"])
    return pred_pids, pred_windows, succ_pids, succ_windows


def _success_record_rotated(root: Path, seat: str, row: dict, _rotate,
                            now: float) -> tuple[dict | None, str | None]:
    """hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-
    never-by-gen-order-or-age: the seat's LATEST success rotation record
    (crash-recovery records EXCLUDED by construction) proves the row by its
    IDENTITY fields, never by gen ordering or record age alone. Returns
    `(record, arm)` -- the record when the row is the RETIRED predecessor
    (rotated, not dead), `(None, arm)` when the record proves the row is the
    DEAD SUCCESSOR, else `(None, None)`.
      pred-identity: row pid in `s12_self_reap.chain[*].pid` OR row window
          == `handover.own_window.id` -- the row IS the retired predecessor;
          NO age bound (a lagging row is exactly what this arm protects).
      succ-dead:      row pid == `handover.join.pid` OR row window in
          `handover.join.window_id` / `successor_window.id` -- the row is
          ALREADY the successor's; if the caller has established that pid is
          dead the death is NEVER masked by the 600 s window -> returns None.
      gen-fallback / age-fallback: ONLY for records carrying NONE of those
          identity fields (OLDER records): within SEAT_DEAD_WINDOW_S the
          gen-ordering (gen_after > row gen) and the age arm survive exactly
          as today; a record with no identity OLDER than the window proves
          nothing (returns None). A record that CARRIES identity but matches
          neither predecessor nor successor also returns None -- the guard is
          NEVER lowered (when in doubt, None and the pid arm decides)."""
    try:
        rec = _rotate._latest_rotation_record(root, seat)
    except Exception:  # noqa: BLE001
        return None, None
    if not isinstance(rec, dict) or rec.get("result") != "success":
        return None, None
    pred_pids, pred_windows, succ_pids, succ_windows = _rotation_identity(rec)
    if pred_pids or pred_windows or succ_pids or succ_windows:
        # the record carries identity -> identity decides, gen/age never
        # reaches a record that has identity (only OLDER records fall back).
        row_pid = str(row.get("pid") or 0)
        row_win = str(row.get("window") or "")
        if row_pid in pred_pids or row_win in pred_windows:
            return rec, "pred-identity"
        if row_pid in succ_pids or row_win in succ_windows:
            return None, "succ-dead"
        return None, None
    # no identity fields -> OLDER record: gen/age fallback, window-bounded.
    row_gen = row.get("generation")
    _, gen_after = _rotation_before_after(rec)
    ts = _parse_record_ts(rec.get("recorded_at", ""))
    within = ts is not None and (now - ts) <= SEAT_DEAD_WINDOW_S
    if not within:
        # condition (a) gen_after > row gen is NOW ALSO bounded by the window:
        # a no-identity record older than the window proves nothing.
        return None, None
    if row_gen is not None and gen_after is not None:
        try:
            if int(gen_after) > int(row_gen):
                return rec, "gen-fallback"
        except (TypeError, ValueError):
            pass
    return rec, "age-fallback"


def _rotation_in_flight(root: Path, seat: str, _rotate,
                        now: float, row: dict | None = None) -> bool:
    """(1d) a rotation record for the seat is `started` within the last
    10 minutes OR the latest record proves the seat already ROTATED (a
    success record newer than the row, clause (3)) -> a rotation in flight,
    not a crash. ONE helper -- `_success_record_rotated` -- is shared with
    `_watch_one_seat` (clause (2)); the comparison is never duplicated."""
    if row is None:
        try:
            rows = _rotate._load_seats(root) or []
        except Exception:  # noqa: BLE001
            rows = []
        row = next(((r for r in rows if (r.get("name") or "") == seat)), {})
    rot = _rotate._rotations_dir(root)
    if _success_record_rotated(root, seat, row, _rotate, now)[0] is not None:
        return True
    if not rot.is_dir():
        return False
    for path in sorted(rot.glob(f"{seat}.*.json")):
        try:
            rec = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if rec.get("result") != "started":
            continue
        ts = _parse_record_ts(rec.get("recorded_at", ""))
        if ts is not None and (now - ts) <= SEAT_DEAD_WINDOW_S:
            return True
    return False


# ---------------------------------------------------------------------------
# hypothesis:l4-the-pin-is-the-lease, KID 1 — the TABLES + the JUDGEMENT.
# Pure functions (no reap, no write, no dm, no live process); KID 2 consumes
# them in `_pin_reap_pass`. rotate.py is IMPORTED never edited; the reap chain
# (`_pane_pid`, `_descendant_chain`, `_reap_chain`, `_pid_alive`) is KID 2's
# arm. Nothing here reads `~/.claude/sessions`, kills a process, or touches
# `.agi/config.json`.
# ---------------------------------------------------------------------------


def _pin_table(root: Path, rows: list) -> tuple[dict, list]:
    """(1a) THE PIN TABLE. Returns `({session_id: (seat, pin_path, generation)},
    skipped)`. Reads every row's own seat-stable pin `<sessions>/<seat>.meter`
    (the file `pin_ref` in the row names, via the ONE `_sessions_dir`
    resolver the pins already share) and, for a row carrying
    `predecessor_pins: N` (READ the cell, absent = 0), the chain pins
    `<seat>.pred-1..N.meter` beside it. A pin names a transcript
    (`<gen><TAB><transcript>` or bare `<transcript>`, parsed by rotate's own
    `_parse_pin_record` — never copied); the session it leases is the
    transcript's STEM, the L4.114 identity `~/.claude/projects/<slug>/<sid>`
    `.jsonl`. A pin whose transcript FILE is missing is SKIPPED with a reason
    (clause 3) and is never a lease — its session therefore reads as
    unpinned. FIXTURES ONLY: reads only the fixture sessions dir; never
    `~/.claude/sessions`, never a real process."""
    import rotate as _rotate  # noqa: PLC0415
    sdir = _rotate._sessions_dir(root)
    pins: dict = {}
    skipped: list[dict] = []
    for row in rows or []:
        seat = (row.get("name") or "").strip()
        if not seat:
            continue
        pred_n = int(row.get("predecessor_pins", 0) or 0)
        own_pin = f"{seat}{_rotate.METER_PIN_EXT}"
        pred_pins = [f"{seat}.pred-{i}{_rotate.METER_PIN_EXT}"
                     for i in range(1, pred_n + 1)]
        for pin_name in [own_pin] + pred_pins:
            pf = sdir / pin_name
            if not pf.is_file():
                if pin_name != own_pin:
                    skipped.append({"seat": seat, "pin_path": str(pf),
                                    "reason": "predecessor pin file absent"})
                continue
            gen, target = _rotate._parse_pin_record(pf)
            if not target:
                skipped.append({"seat": seat, "pin_path": str(pf),
                                "reason": "pin empty/unparsable"})
                continue
            tp = Path(target).expanduser()
            if not tp.exists():
                skipped.append({"seat": seat, "pin_path": str(pf),
                                "reason": f"transcript missing: {tp}"})
                continue
            sid = tp.stem
            if sid:
                pins[sid] = (seat, str(pf), gen)
    return pins, skipped


def _seat_sessions(registry_dir: str | None = None,
                   windows: list[tuple[str, str]] | None = None) -> list[dict]:
    """(1b) THE SEAT SESSION TABLE — one entry per Claude Code session on the
    box whose registry file's `tmux` cell carries an `@id` that resolves,
    through the SAME window list `_all_windows` already builds, to a live
    window. Returns `[{pid, session_id, window_id, window_name}]`.

    (clause 4) every OTHER registry file — the owner's remote-control sessions
    (`tmux: None`), the streamer stub, anything unnamed — is NOT a seat
    session: never listed, never touched. @id-resolution through the window
    list is the whole gate at THIS layer (the one the fixed signature
    `(registry_dir, windows)` can decide); the seat/belam NAME gate lives in
    `_judge_leases`, which is the layer that holds the rows. NEVER reads a
    real process; reads only `<registry_dir>/<pid>.json`."""
    import rotate as _rotate  # noqa: PLC0415
    reg = Path(registry_dir or _rotate.REGISTRY_DEFAULT_DIR).expanduser()
    if not reg.is_dir():
        return []
    win_by_id = {wid: name for (wid, name) in (windows or [])}
    _RE_ID = re.compile(r"@(\d+)")
    out: list[dict] = []
    for fp in sorted(reg.glob("*.json")):
        try:
            data = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        tmux = data.get("tmux")
        if not isinstance(tmux, str):
            continue  # owner remote-control (`tmux: None`) / stub: no @id
        m = _RE_ID.search(tmux)
        if not m:
            continue
        wid = f"@{m.group(1)}"
        wname = win_by_id.get(wid)
        if wname is None:
            continue  # @id resolves to no live window -> not a seat session
        sess = data.get("session_id") or data.get("sessionId") or ""
        if not sess:
            continue
        try:
            pid = int(fp.stem)
        except ValueError:
            pid = None
        out.append({"pid": pid, "session_id": sess,
                    "window_id": wid, "window_name": wname})
    return out


def _judge_leases(pins: dict, sessions: list, rows: list, root: Path,
                  now: float | None = None) -> list[dict]:
    """(1c) THE JUDGEMENT — per seat session exactly ONE of:
      KEEP          its sessionId is pinned (a live lease),
      PROTECTED     row `protected: true` (READ the cell, absent = not),
      IN-FLIGHT     `_rotation_in_flight` (L4.283's guard, CALLED not copied),
      BELAM-UNPINNED a belam-prefixed session no pin names while the belam row
                    carries no `predecessor_pins` cell or its pred chain is
                    incomplete: LISTED with reason `no predecessor-pin table
                    yet`, NEVER reaped — the owner's standing rule that the
                    idle predecessor windows are never closed holds BY
                    CONSTRUCTION until the pin SHIFT (a rotate.py round)
                    exists,
      REAP          a plain-seat session no pin names.
    Verdict order is KEEP > PROTECTED > IN-FLIGHT > BELAM-UNPINNED > REAP.
    Only sessions whose window name matches a seat row or carries the belam
    row's name as a prefix are judged at all (clause 4); the rest fall out of
    the table. Returns `[{pid, session_id, window_id, window_name, seat,
    verdict, reason}]`."""
    import rotate as _rotate  # noqa: PLC0415
    now = now if now is not None else time.time()
    by_name: dict[str, dict] = {}
    belam_row = None
    belam_name = ""
    for r in rows or []:
        nm = (r.get("name") or "").strip()
        if not nm:
            continue
        by_name[nm] = r
        if nm == "belam":
            belam_row = r
            belam_name = nm
    pred_n = int((belam_row or {}).get("predecessor_pins", 0) or 0)
    pred_complete = False
    if belam_row and pred_n > 0:
        sdir = _rotate._sessions_dir(root)
        pred_complete = all(
            (sdir / f"{belam_name}.pred-{i}{_rotate.METER_PIN_EXT}").is_file()
            for i in range(1, pred_n + 1))
    res: list[dict] = []
    for s in sessions or []:
        wname = (s.get("window_name") or "").strip()
        row = by_name.get(wname)
        belam_pref = False
        if row is None and belam_name and \
                (wname == belam_name or wname.startswith(belam_name + "-")):
            row = belam_row
            belam_pref = True
        if row is None:
            continue  # not a seat/belam window: never listed, never touched
        seat = (row.get("name") or "").strip()
        sid = s.get("session_id") or ""
        reason = ""
        if sid and sid in pins:
            verdict = "KEEP"
        elif bool(row.get("protected")):
            verdict = "PROTECTED"
        elif _rotation_in_flight(root, seat, _rotate, now, row=row):
            verdict = "IN-FLIGHT"
        elif belam_pref and not pred_complete:
            verdict = "BELAM-UNPINNED"
            reason = "no predecessor-pin table yet"
        else:
            verdict = "REAP"
        res.append({"pid": s.get("pid"), "session_id": sid,
                    "window_id": s.get("window_id"),
                    "window_name": wname, "seat": seat,
                    "verdict": verdict, "reason": reason})
    return res


# ---------------------------------------------------------------------------
# hypothesis:l4-the-pin-is-the-lease, KID 2 — the PASS + the ARM.
# `_pin_reap_pass` is called once per `_watch` pass right after `_watch_seats`;
# `pin-reap` is a LIST-ONLY subcommand of heal.py. The MODE is read from
# `.agi/config.json` `reaper.pin_reap` (absent or `"dry-run"` = LIST ONLY;
# `"armed"` = reap via rotate.py's OWN imported helpers: `_pane_pid` ->
# `_descendant_chain` -> `_reap_chain`), then ONE dm via send.py to the REAP
# row's `rotated_by` holder + a watch-log line. rotate.py is IMPORTED never
# edited. FIXTURES ONLY: never edits `.agi/config.json`, never reads
# `~/.claude/sessions` under test (registry_dir pain), never kills a real
# process (`reaper`/`pid_alive` are the test seams).
# ---------------------------------------------------------------------------


def _pin_reap_mode(root: Path) -> str:
    """`"armed"` iff `.agi/config.json` `reaper.pin_reap == "armed"`; else
    `"dry-run"`. Never edits the config, never raises (a missing/malformed
    config -> dry-run, FAIL CLOSED: an unreadable mode must never arm)."""
    try:
        cfg_path = locations.config_path(root)
        if cfg_path is not None:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            if (cfg.get("reaper") or {}).get("pin_reap") == "armed":
                return "armed"
    except (OSError, json.JSONDecodeError, TypeError):
        pass
    return "dry-run"


def _pin_reap_arm(root: Path, j: dict, _rotate) -> dict:
    """The REAL reap arm (used when MODE is armed and no `reaper` seam is
    injected): rotate.py's OWN chain `_pane_pid(@window)` ->
    `_descendant_chain` -> `_reap_chain`. A window-id that yields no pane pid
    or an empty chain SKIPPED with the reason (never guesses). Never raises
    live; `_reap_chain` refuses the caller's own pid and any pid <= 0."""
    wid = j.get("window_id") or ""
    pane_pid = _rotate._pane_pid(wid) if wid else None
    if not pane_pid:
        return {"window_id": wid, "pane_pid": None, "pids": [],
                "observed": {"chain": []},
                "skipped": "no pane pid for window "
                            f"{wid!r}; nothing to reap"}
    pids = _rotate._descendant_chain(pane_pid)
    if not pids:
        return {"window_id": wid, "pane_pid": pane_pid, "pids": [],
                "observed": {"chain": []},
                "skipped": f"no chain under pane pid {pane_pid}"}
    observed = _rotate._reap_chain(pids)
    return {"window_id": wid, "pane_pid": pane_pid, "pids": pids,
            "observed": observed}


def _pin_reap_pass(root: Path, *, registry_dir: str | None = None,
                   window_path: str | None = None, pid_alive=None,
                   reaper=None, now: float | None = None,
                   mode: str | None = None,
                   ) -> list[dict]:
    """(2a) ONE pin-reap pass: read the pins, list the @id-resolved seat
    sessions, judge every one, log ONE summary line plus one line per
    non-KEEP session, and — only when MODE is `armed` and the verdict is
    REAP — reap (rotate helpers or the injected `reaper` seam) and dm the
    row's `rotated_by` holder once. Never reaps PROTECTED / IN-FLIGHT /
    BELAM-UNPINNED (kid 1's verdicts, BY CONSTRUCTION: only `REAP` arms).
    Idempotent: a session already reaped is no longer in the registry, so a
    later pass simply does not list it; an already-dead pid reap records
    not-alive and changes nothing. Returns the list of ARM actions taken
    (empty under dry-run / no REAP). Never raises into the watch loop."""
    import rotate as _rotate  # noqa: PLC0415
    try:
        rows = _rotate._load_seats(root) or []
    except Exception:  # noqa: BLE001
        rows = []
    windows = _all_windows(window_path)
    pins, _skipped = _pin_table(root, rows)
    sessions = _seat_sessions(registry_dir, windows)
    judged = _judge_leases(pins, sessions, rows, root,
                           now=now if now is not None else time.time())
    counts: dict[str, int] = {}
    for j in judged:
        counts[j["verdict"]] = counts.get(j["verdict"], 0) + 1
    _watch_log("watch: pin-reap pass: "
               + ", ".join(f"{v}={counts.get(v, 0)}"
                           for v in ("KEEP", "PROTECTED", "IN-FLIGHT",
                                     "BELAM-UNPINNED", "REAP")
                           if counts.get(v)))
    if mode is None:
        mode = _pin_reap_mode(root)
    armed = (mode == "armed")
    pid_is_alive = pid_alive or _pid_alive
    acted: list[dict] = []
    for j in judged:
        if j["verdict"] == "KEEP":
            continue
        _watch_log(f"watch: pin-reap {j['verdict']}: "
                   f"seat={j['seat']} sid={j['session_id']} "
                   f"pid={j['pid']} window={j['window_id']} "
                   f"({j['reason']})")
        if j["verdict"] != "REAP" or not armed:
            continue
        rec = {"seat": j["seat"], "session_id": j["session_id"],
               "pid": j["pid"], "window_id": j["window_id"]}
        # idempotence: skip arming a pid the liveness seam reports dead
        # (its registry file is stale but the process is already gone).
        already_gone = False
        if j.get("pid"):
            try:
                alive = pid_is_alive(int(j["pid"]))
            except Exception:  # noqa: BLE001
                alive = True
            if not alive:
                already_gone = True
                rec["reaped"] = False
                rec["note"] = "pid already gone; nothing to reap (idempotent)"
        if already_gone:
            _watch_log(f"watch: pin-reap REAP (skip gone): seat={j['seat']} "
                       f"pid={j['pid']}")
        else:
            if reaper is not None:
                try:
                    rec["reap"] = reaper(root, j, _rotate)
                except Exception as exc:  # noqa: BLE001
                    rec["reap"] = {"skipped": f"reaper raised: {exc}"}
            else:
                rec["reap"] = _pin_reap_arm(root, j, _rotate)
        row = next((r for r in rows
                    if (r.get("name") or "").strip() == j["seat"]), {})
        holder = str(row.get("rotated_by") or "").strip()
        # ONE dm to the REAP row's rotated_by holder (best-effort, never fatal)
        if holder:
            try:
                import send as _send  # noqa: PLC0415
                ts = datetime.datetime.utcnow().isoformat() + "Z"
                _send.send(root, holder,
                           f"[pin-reap] {j['seat']} window {j['window_id']} "
                           f"(sid={j['session_id']}, pid={j['pid']}) reaped "
                           f"at {ts} by heal pin-reap pass", "heal")
            except Exception as exc:  # noqa: BLE001
                print(f"warn: pin-reap dm to {holder!r} failed: {exc}",
                      file=sys.stderr)
        _watch_log(f"watch: pin-reap REAP: seat={j['seat']} "
                   f"window={j['window_id']} pid={j['pid']} -> armed")
        acted.append(rec)
    return acted


def _live_seat_row(gdir: Path, seat: str, _rotate) -> dict | None:
    """Read the seat row LIVE-FIRST from `<gdir>/nodes/.geometry/posts.md`
    (`seats.md` is the one-season alias; post-first via
    `geometry_config.resolve`, hypothesis:l4-a-seat-is-a-post-everywhere)
    (a worktree seat's row reaches MAIN only at its merge-up, so a worktree
    seat must be read from its own copy first). The IDENTITY cells
    (`generation`/`window`/`pid`/`session_ref`/`session_id`) are taken from
    the MAIN checkout's copy instead — a worktree rotation writes ONLY MAIN
    (hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main),
    so the worktree copy carries the PRE-rotation @id and reading it would
    misjudge the seat dead. Other cells stay live-first. None when absent."""
    live = _read_row(_rotate, gdir, seat)
    main = _read_row(_rotate, _main_graph_root(gdir), seat)
    if live is None and main is None:
        return None
    row: dict = dict(live) if live is not None else dict(main)
    if main is not None:
        for cell in IDENTITY_CELLS:
            if cell in main:
                row[cell] = main[cell]
    return row


#: The identity cells a rotation writes into config:seats. Read from MAIN.
IDENTITY_CELLS = ("generation", "window", "pid", "session_ref",
                  "session_id")


def _read_row(_rotate, gdir: Path, seat: str) -> dict | None:
    """The seat's row read from one geometry dir, or None."""
    try:
        rows = _rotate._load_seats(gdir) or []
    except Exception:  # noqa: BLE001
        return None
    for r in rows:
        if r.get("name") == seat:
            return r
    return None


def _main_graph_root(gdir: Path) -> Path:
    """The MAIN checkout's graph root, identity for a non-worktree caller —
    the resolution `locations.git_common_root` performs (hypothesis:l4-a-
    seats-identity-cell-has-one-writer-and-it-writes-main). Only a real
    linked-worktree call rebases to MAIN; a caller in the main checkout or
    outside git keeps `gdir` unchanged."""
    graph = Path(gdir)
    main = locations.git_common_root(graph)
    if main is not None and main != graph:
        graph = locations.find_project_root(main) or main
    if (graph / locations.GRAPH_DIR_NAME / "nodes").is_dir():
        return graph / locations.GRAPH_DIR_NAME
    return graph


def _read_seat_log_tail(root: Path, row: dict, _rotate,
                        nbytes: int = 8192) -> str:
    """The tail of the seat's session log, live-first from its own tree,
    falling back to the main copy; '' when neither is readable."""
    seat = (row.get("name") or "").strip()
    if not seat:
        return ""
    cands: list[Path] = []
    gdir = _seat_geometry_dir(root, row)
    own = _rotate._sessions_dir(gdir) / f"{seat}.log"
    cands.append(own)
    main = _rotate._sessions_dir(root) / f"{seat}.log"
    if main != own:
        cands.append(main)
    for p in cands:
        try:
            if p.exists():
                data = p.read_bytes()
                return data[-nbytes:].decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            continue
    return ""


#: Launcher seam for the recovered successor. A real recover launches through
#: tmux; the FIXTURE injects a fake launcher so it never spawns a real model.
RECOVER_LAUNCHER_ENV = "AGI_RECOVER_LAUNCHER"


def _seat_tree_dir(root: Path, row: dict) -> Path:
    """The repo root a recovered seat must cd-launch inside: the MAIN
    checkout's repo root (`locations.git_common_root`, never the graph dir)
    joined with the row's `worktree` cell -- empty cell => MAIN's repo root
    itself (hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-
    human, (3)). A worktree seat's cell is stored relative to MAIN's repo root
    (e.g. `.agi/worktrees/seat-wt`), so joining them names the seat's OWN
    worktree repo root; a main-checkout seat launches from MAIN. `root` is the
    graph root; `locations.git_common_root` rebases a linked-worktree or graph-
    dir caller onto MAIN (a path with no enclosing repo resolves to itself,
    which is exactly the fixture's standalone graph)."""
    base = locations.git_common_root(Path(root))
    base = base if base is not None else Path(root)
    wt = (row.get("worktree") or "").strip()
    if not wt:
        return base
    return base / wt


def _launch_recovered(root: Path, name: str, shell_cmd: str,
                      window_path: str | None = None,
                      cwd: Path | str | None = None) -> tuple[int | None, str]:
    """Real tmux new-window launch of a recovered successor (mirrors
    rotate._launch_window's shape; the PID is not derivable from tmux, so the
    successor ack resolves its own identity/ref). Returns `(pid, window @id)`:
    pid is `None` when launched-but-unknown (row skips pid), `0` when the
    spawn FAILED (the recover records `detected` and the next pass retries).
    Never raises into the watch pass.

    Launches inside the seat TREE (`cwd`, else `_seat_tree_dir` on an empty
    row): MAIN's repo root for a main-checkout seat, the seat's own worktree
    repo root for a worktree seat -- NEVER the graph dir (`cd .agi`), so the
    successor wakes already standing in the tree it edits (hypothesis:l4-a-
    dead-seat-is-recovered-by-the-loop-not-by-a-human, (3))."""
    import rotate as _rotate  # noqa: PLC0415 -- lazy, same bin dir
    tmux_session = _rotate.DEFAULT_TMUX_SESSION
    tree = Path(cwd) if cwd is not None else _seat_tree_dir(root, {})
    launch_cmd = f"cd {shlex.quote(str(tree))} && {shell_cmd}"
    try:
        proc = subprocess.run(
            ["tmux", "new-window", "-t", tmux_session, "-n", name,
             "-P", "-F", "#{window_id}", launch_cmd],
            capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001 — tmux absent/down counts as not-spawned
        return 0, ""
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip() or "<no output>"
        print(f"warn: recovered spawn of {name!r} failed: {detail}",
              file=sys.stderr)
        return 0, ""
    wid = (proc.stdout.strip().splitlines()[-1]
           if proc.stdout.strip() else "")
    return None, wid


def _load_launcher(launcher) -> callable | None:
    """Resolve the recover launcher callable: an explicit `launcher` wins;
    else `AGI_RECOVER_LAUNCHER` naming a python file that exports `launch(
    root, name, shell_cmd, window_path) -> (pid, window_id)`; else None (real
    tmux). Called once per `_watch_seats` pass."""
    if launcher is not None:
        return launcher
    envp = os.environ.get(RECOVER_LAUNCHER_ENV)
    if envp:
        p = Path(envp)
        if p.is_file():
            spec = importlib.util.spec_from_file_location("heal_launcher", p)
            mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
            spec.loader.exec_module(mod)  # type: ignore[union-attr]
            return getattr(mod, "launch", None)
    return None


def _clean_stale_layout_locks(root: Path, row: dict) -> None:
    """GRACEFUL: a stale `verify-suite.lock` under the dead seat's tree is
    removed with a log line (verification.py holds it under `<groot>/sessions/`;
    the dead seat is the only holder that could still be mid-suite, and a stale
    lock would wedge the next suite run forever). Live-first geometry tree;
    best-effort, never raises."""
    gdir = _seat_geometry_dir(root, row) / "sessions"
    lock = gdir / "verify-suite.lock"
    if lock.is_file():
        try:
            lock.unlink()
            _watch_log(f"watch: removed stale verify-suite.lock under "
                       f"{gdir} for dead seat {(row.get('name') or '')!r}")
        except OSError as exc:
            print(f"warn: could not remove stale lock {lock}: {exc}",
                  file=sys.stderr)


def _dm_crash_recovery(root: Path, row: dict, old_pid: int, cause: str,
                       name: str, window_id: str, gen: int) -> None:
    """Exactly ONE dm to the dead seat's `rotated_by` holder AND one to the
    Sensei, both naming the crash + the respawn outcome. Undeliverable -> one
    stderr line, never fatal."""
    seat = str(row.get("name") or "").strip()
    holder = str(row.get("rotated_by") or "").strip()
    recipients = [r for r in (holder, "master-sensei") if r]
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    wid = f"@{window_id}" if window_id and not str(window_id).startswith("@") \
        else (str(window_id or "-"))
    body = (f"[crash-recovery] {seat} pid {old_pid} dead at {ts} "
            f"({cause}); respawned {name} gen {gen} @id {wid}; "
            f"after_join: service-owed")
    try:
        import send as _send  # noqa: PLC0415
    except Exception:  # noqa: BLE001
        return
    for to in recipients:
        try:
            _send.send(root, to, body, "heal")
        except Exception as exc:  # noqa: BLE001
            print(f"warn: crash-recovery dm to {to} failed: {exc}",
                  file=sys.stderr)


def _recover_seat(root: Path, row: dict, cause: str, _rotate, *,
                  windows: list[tuple[str, str]], window_path: str | None,
                  launcher, now: float) -> dict:
    """RESPAWN a dead seat through its EXISTING spawn path and bind the
    successor's row. Builds the successor command with rotate.spawn_window
    (dry-run) using the ROW's own model/effort/settings, names the successor by
    the seat's rule exactly as rotate-self does (a chain seat — role
    prime_director — gets the next Roman numeral; a plain seat the seat name),
    launches through the launcher seam, writes `generation`/`window`/`pid`/
    `session_id` into the seat's own config:seats row via the row writer
    (`session_ref` stays empty for the successor's ack) and sends ONE dm each
    to the `rotated_by` holder and the Sensei. Returns
    `{respawned, name, generation, pid, window, reason, row}`."""
    seat = str(row.get("name") or "").strip()
    role = str(row.get("role") or "").strip()
    tier = str(row.get("tier") or role or "kid").strip()
    model = row.get("model")
    effort = row.get("effort")
    settings = row.get("settings")
    existing = [w for (_i, w) in windows]
    old_pid = int(row.get("pid", 0) or 0)

    is_chain = (role == "prime_director")
    if is_chain:
        # The successor NUMERAL is derived from the registry row's `generation`
        # and the latest rotation/crash-recovery record's `gen_after` -- max
        # them, +1 -- NEVER from open window names (prime XI 19:38Z: a name is
        # not an address; windows get reaped/renamed, so a numeral inferred
        # from them drifts from the truth). Open window names (`existing`) are
        # consulted ONLY for the collision refusal below. The chain BASE (e.g.
        # `belam-S1-L4`) is taken from the latest record's successor name when
        # one exists (crash-recovery `succ_name`, rotate-self
        # `handover.successor_window.name`), else the seat name itself.
        rec_name = ""
        rec_gen = 0
        _rec = _rotate._latest_rotate_record(root, seat)
        if _rec is not None:
            _r = _rec[0]
            rec_name = str(
                _r.get("succ_name")
                or (_r.get("handover") or {}).get("successor_window", {})
                   .get("name") or "").strip()
            try:
                rec_gen = int(_r.get("gen_after") or 0)
            except (TypeError, ValueError):
                rec_gen = 0
        row_gen = int(row.get("generation", 0) or 0)
        gen = max(rec_gen, row_gen) + 1
        base = (_rotate._split_roman_suffix(rec_name)[0] if rec_name
                else seat)
        spawn_name = f"{base}-{_rotate._int_to_roman(gen)}"
    else:
        spawn_name = seat
        # generation follows rotate-self's plain-seat rule (`_read_generation`
        # from the HANDOFF + 1), falling back to the ROW's own `generation`
        # cell when the handoff is gone: a crash can consume the handoff too,
        # and a recovery following a row already at gen 3 must be gen 4, not
        # restart at 1.
        base = _rotate._read_generation(root, seat)
        if base <= 0:
            base = int(row.get("generation", 0) or 0)
        gen = base + 1
    if spawn_name in existing:
        return {"respawned": False, "name": spawn_name, "generation": gen,
                "reason": f"successor window {spawn_name!r} already exists",
                "row": "skipped"}
    # GRACEFUL: a suite lock the dead seat owned must not wedge the next run.
    _clean_stale_layout_locks(root, row)

    dbg = str(_rotate._sessions_dir(root) / f"{seat}.log")

    # GOAL:g15.25 (SL7.15) — a crash-recovery respawn at gen `gen` must start
    #     with NO live ack. The seat was rotated (or last acked) at some
    #     earlier generation; a predecessor `continue` still sitting at
    #     `seats/<seat>.ack.json` would otherwise SILENCE the recovered post's
    #     `ack --gen N+1 continue` via the gen-blind no-op in cmd_ack (part
    #     (a)) and it would never take its identity. Rotate the stale ack to
    #     `seats/<seat>.ack.gen<gen>.json` BEFORE spawning, so this seat's
    #     recovered post writes its own ack fresh. None/no-op when there is
    #     no live ack.
    _rot = _rotate._rotate_ack_file(root, seat, gen)
    if _rot:
        print(_rot, file=sys.stderr)

    prompt_file = None
    if role == "prime_director":
        # the prime resumes on the standing prime brief.
        prompt_file = _rotate.DEFAULT_PROMPT_FILE
    else:
        # A director/helper resumes on ITS OWN quorum card — the file
        # rotate-self hands its successor (`--prompt-file
        # .agi/sessions/quorum/<seat>.md`, F16) — never the assembled generic
        # brief, which carries none of the seat's §0-§3 state (the 22-32-call
        # spawn-seating wakes the Sensei measured on 175816Z/181834Z). Found
        # by the L4.283 harvest's live proof (sanctuary-director 182119Z
        # 19:27Z): with prompt_file None, spawn_window assembled the generic
        # director brief. Absent card -> the assembled brief, as before.
        card = _rotate._sessions_dir(root) / "quorum" / f"{seat}.md"
        if card.is_file():
            prompt_file = str(card)
    ack_gate = (
        "RECOVERED SEAT (crash-recovery): first act after reading your handoff, "
        f"run `python3 extensions/agi/bin/rotate.py ack --seat {seat} --gen {gen} "
        "--ref <your ListAgents ref> continue` to take your identity."
    )
    try:
        rc, shell_cmd = _rotate.spawn_window(
            name=spawn_name, tier=tier, prompt_file=prompt_file,
            model=model, effort=effort, settings=settings,
            root=root, window_path=window_path, dry_run=True,
            debug_file=dbg, extra=ack_gate, seat=seat)
    except Exception as exc:  # noqa: BLE001
        return {"respawned": False, "name": spawn_name, "generation": gen,
                "reason": f"spawn_window raised: {exc}", "row": "skipped"}
    if rc != 0 or not shell_cmd:
        return {"respawned": False, "name": spawn_name, "generation": gen,
                "reason": f"spawn_window refused (rc={rc})", "row": "skipped"}

    launcher = launcher if launcher is not None else _launch_recovered
    tree = _seat_tree_dir(root, row)
    try:
        pid, window_id = launcher(root, spawn_name, shell_cmd, window_path,
                                  cwd=tree)
    except TypeError:
        # a launcher seam written against the pre-cwd signature has no
        # `cwd`; fall back to it launching from its own default. Real
        # recoveries run `_launch_recovered` (cwd-aware); only old seams land
        # here.
        pid, window_id = launcher(root, spawn_name, shell_cmd, window_path)
    if pid == 0:
        # spawn did not land -> the seat stays dead; record `detected` only so
        # the NEXT pass retries (the defect pin).
        return {"respawned": False, "name": spawn_name, "generation": gen,
                "reason": "launcher reported no successor process",
                "row": "skipped"}
    # pid is None (launched, unknown) or a real int -> the recovery landed.
    row_pid = pid if pid else None   # None keeps `_successor_row_write` pid-free
    try:
        row_text = _rotate._successor_row_write(
            root, actor=seat, seat=seat, role=role, session_ref="",
            generation=gen, window=window_id or spawn_name,
            pid=row_pid, session_id="")
    except Exception as exc:  # noqa: BLE001
        row_text = f"row write FAILED: {exc}"
    _dm_crash_recovery(root, row, old_pid, cause, spawn_name, window_id, gen)
    return {"respawned": True, "name": spawn_name, "generation": gen,
            "pid": pid, "window": window_id, "reason": "", "row": row_text}


def _latest_detected_path(root: Path, seat: str, _rotate, now: float) \
        -> Path | None:
    """The newest `rotation: crash-recovery` `result: detected` record file for
    `seat` still inside `SEAT_DEAD_WINDOW_S`, or None. This is the dedupe key
    (hypothesis:l4-a-rotation-alert-lands-in-the-inbox-..., clause 3): a seat
    that stays dead and unrecoverable is re-scanned every poll (~30 s) and each
    pass would otherwise mint a FRESH `<seat>.<stamp>.json`, the measured
    nine-detected-records-per-seating defect. Reusing the existing detected
    record's path keeps ONE record per death, updated in place."""
    rot = _rotate._rotations_dir(root)
    if not rot.is_dir():
        return None
    for path in sorted(rot.glob(f"{seat}.*.json"), reverse=True):
        try:
            rec = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if rec.get("rotation") != "crash-recovery" \
                or rec.get("result") != "detected":
            continue
        ts = _parse_record_ts(rec.get("recorded_at", ""))
        if ts is not None and (now - ts) <= SEAT_DEAD_WINDOW_S:
            return path
    return None


def _write_crash_recovery(root: Path, seat: str, cause: str, cells: dict,
                          _rotate, now: float, outcome: dict | None = None) \
        -> Path:
    """Write ONE durable `rotation: crash-recovery` record carrying the
    probable_cause AND the respawn outcome (`result: respawned` with the
    successor name/generation/pid/window when recovery landed, else `result:
    detected` so the next pass retries). Discoverable by
    `rotate.py status --record latest <seat>` and the Sensei audit glob.

    DEDUPE (clause 3): a `detected` (recovery did not land) write is keyed to
    the seat's newest EXISTING detected record inside `SEAT_DEAD_WINDOW_S` and
    UPDATES THAT FILE IN PLACE, so one death stays one record no matter how
    many polls re-scan the still-dead seat. A `respawned` write is always a
    fresh file (it is a distinct, terminal outcome)."""
    res = "respawned" if (outcome and outcome.get("respawned")) else "detected"
    # The successor generation the after_join service will bind: `gen_after`
    # is the key `rotate._latest_rotate_record` / `run_after_join_for_seat`
    # read (the SAME one they read on a rotate-self record), so a recovered
    # seat's join -> pin -> pending-ack runs at ITS generation, never a guess.
    gen_after = (outcome.get("generation") if outcome else None)
    # profile placeholders (L4.292 kid 1 (1a)): the same shape rotate-self's
    # record carries for the template's after_join list — `seat`, `succ_name`,
    # `gen`, `pin_ref`, `tmux_session`, `window_id`, `pred_pids` = the dead
    # pid, `recorded_at`. The meter pin is SERVICE-owed (the service pins
    # after `after_join_delay_s`, exactly as for a rotated seat), so `pin_ref`
    # stays empty here — the recovery itself pins nothing.
    _dpid = int(cells.get("pid") or 0)
    pred_pids = [_dpid] if _dpid > 0 else []
    rec = {
        "rotation": "crash-recovery",
        "seat": seat,
        "recorded_at": datetime.datetime.utcnow().isoformat() + "Z",
        "result": res,
        "probable_cause": cause,
        "succ_name": (outcome.get("name") if outcome else None) or seat,
        "gen": gen_after,
        "gen_after": gen_after,
        "pin_ref": "",
        "tmux_session": _rotate.DEFAULT_TMUX_SESSION,
        "window_id": (outcome.get("window") if outcome else None) or "",
        "pred_pids": pred_pids,
        "row": {k: cells.get(k) for k in (
            "name", "role", "model", "pid", "window", "session_id",
            "generation", "worktree")},
    }
    if outcome:
        rec["respawn_outcome"] = {
            "name": outcome.get("name"),
            "generation": outcome.get("generation"),
            "pid": outcome.get("pid"),
            "window": outcome.get("window"),
            "reason": outcome.get("reason") or "",
            "row": outcome.get("row") or "",
        }
    if res == "detected":
        # one record per death: update the existing detected record in place.
        existing = _latest_detected_path(root, seat, _rotate, now)
        if existing is not None:
            path = _rotate._write_rotation_record(root, rec, path=existing)
            _watch_log(f"watch: updated crash-recovery record for {seat}: "
                       f"{Path(path).name} (probable_cause={cause} "
                       "result=detected, deduped)")
            return path
    path = _rotate._write_rotation_record(root, rec)
    _watch_log(f"watch: wrote crash-recovery record for {seat}: "
               f"{Path(path).name} (probable_cause={cause} result={res})")
    return path


def _alive_via_pin(pins: dict, sessions: list, seat: str,
                   pid_alive) -> dict | None:
    """LIVENESS BEFORE DEATH (L4.292 kid 1 (5)): when this seat's meter pin
    leases a registry session whose pid is ALIVE, the seat is ALIVE regardless
    of its row -- the row is STALE, never a corpse (L4.291's ONE writer makes
    the stale window transient). Reuses the L4.289 tables (IMPORTED, never
    re-implemented): `pins` maps session_id -> (seat, pin_path, gen); this
    seat's own leased session_ids are the keys whose seat value matches.
    Returns the live session dict `{pid, session_id, ...}`, or None when no
    pin for the seat, or the pinned session's pid is gone / absent."""
    if not pins:
        return None
    mine = {sid for sid, (sseat, _pp, _g) in pins.items()
            if sseat == seat}
    if not mine:
        return None
    for s in sessions or []:
        if (s.get("session_id") or "") in mine:
            p = s.get("pid")
            if p is not None and pid_alive(int(p)):
                return s
    return None


def _watch_one_seat(root: Path, row: dict, windows: list[tuple[str, str]],
                    _rotate, *, now: float | None = None,
                    pid_alive=None, window_path: str | None = None,
                    launcher=None, pin_table=None, seat_sessions=None,
                    registry_dir: str | None = None) -> dict:
    """Decide DEAD for one seat row; NAME it once; then, if the seat is
    recoverable, RESPAWN it through its existing spawn path, write its row, dm
    the holder + Sensei, and record the crash-recovery OUTCOME once. Returns an
    empty dict when nothing is done, else
    `{seat, probable_cause, recorded, respawned?, outcome?}`."""
    now = now if now is not None else time.time()
    pid_alive = pid_alive if pid_alive is not None else _pid_alive

    seat = (row.get("name") or "").strip()
    if not seat:
        return {}
    # worktree seat -> re-read its row live-first from its own geometry.
    gdir = _seat_geometry_dir(root, row)
    row = _live_seat_row(gdir, seat, _rotate) or row

    pid = int(row.get("pid", 0) or 0)
    if pid <= 0:
        return {}  # only rows carrying a pid are candidate seats
    # once-guard keyed on a RESPAWN OUTCOME: an earlier `respawned` record
    # means this death is already healed — never re-name, never re-record,
    # never re-spawn on a later pass. A `detected`-only record does NOT stop
    # the respawn (the defect pin: that seat is still dead).
    if _crash_recovery_recorded(root, seat, _rotate, now=now):
        return {}
    # (1a) the row pid is gone from the process table.
    if pid_alive(pid):
        return {}
    # (1b) the LIVE-FIRST row's window @id is gone from tmux. (1c), the
    # window-name lineage, is DELETED (prime XI ruling 19:38Z: a name is not
    # an address; see _window_present).
    id_present, _named = _window_present(row, windows)
    if id_present:
        return {}
    # LIVENESS BEFORE DEATH (L4.292): a seat whose pin leases a live registry
    # session is ALIVE regardless of its row's stale pid/@id -- never DEAD,
    # never respawned. NAMED once per pass as `stale-row` with the row's pid/
    # @id versus the pinned session, so the transient (until L4.291's ONE
    # writer flips the row) is visible without a spawn storm.
    if pin_table is None or seat_sessions is None:
        _pt, _sk = _pin_table(root, [row])
        if pin_table is None:
            pin_table = _pt
        if seat_sessions is None:
            seat_sessions = _seat_sessions(registry_dir, windows) if _pt else []
    live = _alive_via_pin(pin_table, seat_sessions, seat, pid_alive)
    if live is not None:
        _pp = live.get("pid") or 0
        _sid = live.get("session_id") or ""
        line = (f"stale-row seat {seat}: row pid {pid} "
                f"window {str(row.get('window') or '-')} vs pinned session "
                f"{_sid} pid {_pp} alive")
        print(line, file=sys.stderr)
        _watch_log(f"watch: {line}")
        return {"seat": seat, "probable_cause": "stale-row",
                "recorded": False, "stale_row": True, "alive_pid": _pp}
    # (2) a SUCCESS rotation record newer than the row means the row's
    # pid/@id belong to the RETIRED predecessor -- the seat ROTATED, it is
    # not dead (hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-
    # rotation-record-before-declaring-a-crash). NAMED once, no crash-
    # recovery record, no launcher call, {} returned.
    _rotated, _arm = _success_record_rotated(root, seat, row, _rotate, now)
    if _rotated is not None:
        _gb, _ga = _rotation_before_after(_rotated)
        line = (f"rotated seat {seat}: success rotation record "
                f"{_gb} -> {_ga} ({_rotated.get('recorded_at','')}) -- "
                f"row pid {pid} belongs to the retired predecessor, not DEAD "
                f"[arm={_arm}]")
        print(line, file=sys.stderr)
        _watch_log(f"watch: {line}")
        return {}
    # (1d) a rotation in flight is not a crash.
    if _rotation_in_flight(root, seat, _rotate, now, row=row):
        return {}
    # (2b) the DEAD path still names WHY, even when the record was not a
    # rotation: the record's succ-dead arm proved the row IS the successor
    # the record joined, and that successor is gone. EVERY arm that decides
    # reaches the log -- succ-dead was the one SL7.01 left invisible (its
    # `None` return fell straight through to the generic DEAD line).
    if _arm == "succ-dead":
        line = (f"seat {seat}: DEAD — arm=succ-dead (row pid {pid} is the "
                f"successor the record joined, and it is gone)")
        print(line, file=sys.stderr)
        _watch_log(f"watch: {line}")

    cause = _classify_death(_read_seat_log_tail(root, row, _rotate))
    recover = bool(row.get("recover", True))
    cells = {k: row.get(k) for k in (
        "name", "role", "model", "pid", "window", "session_id",
        "generation", "worktree")}
    line = (f"DEAD seat {seat} (role={cells.get('role')} "
            f"model={cells.get('model')} pid={cells.get('pid')} "
            f"window={cells.get('window') or '-'} "
            f"generation={cells.get('generation')} "
            f"probable_cause={cause})")
    print(line, file=sys.stderr)
    _watch_log(f"watch: {line}")
    if not recover:
        # recover:false -> NAMED, never recorded as an action, NEVER respawned.
        _watch_log(f"watch: {seat} is recover:false; named only, no "
                   f"crash-recovery record")
        return {"seat": seat, "probable_cause": cause, "recorded": False}
    outcome = _recover_seat(root, row, cause, _rotate, windows=windows,
                            window_path=window_path, launcher=launcher,
                            now=now)
    _write_crash_recovery(root, seat, cause, cells, _rotate, now, outcome)
    return {"seat": seat, "probable_cause": cause, "recorded": True,
            "respawned": bool(outcome.get("respawned")), "outcome": outcome}


def _watch_seats(root: Path, *, now: float | None = None, pid_alive=None,
                 window_path: str | None = None, launcher=None,
                 registry_dir: str | None = None) -> list[dict]:
    """One dead-seat scan over every configured seat row that carries a pid.
    No-op when rotate cannot be imported or seats are unreadable. Returns the
    list of actions taken (empty = nothing dead) and logs a summary line that
    keeps the falsifier's seat count visible. A dead recoverable seat is
    RESPAWNED here through the launcher seam (real tmux by default; a fake
    launcher under test so no real model spawns)."""
    try:
        import rotate as _rotate
    except Exception:  # noqa: BLE001
        return []
    try:
        rows = _rotate._load_seats(root) or []
    except Exception:  # noqa: BLE001
        return []
    windows = _all_windows(window_path)
    launcher = _load_launcher(launcher)
    # LIVENESS tables (L4.292 kid 1 (5)): built ONCE so the dead-scan can tell
    # a STALE row from a corpse. `_pin_table` reads only tree meter files;
    # `_seat_sessions` reads a registry dir -- the fixture registry under test,
    # the LIVE `~/.claude/sessions` (REGISTRY_DEFAULT_DIR) on the real watch.
    # Guarded: the registry is read ONLY when a pin exists to cross-check, so
    # a pin-less scan never touches the live registry.
    pins, _skipped = _pin_table(root, rows)
    seat_sess = _seat_sessions(registry_dir, windows) if pins else []
    pid_rows = [r for r in rows
                if int(r.get("pid", 0) or 0) > 0 and (r.get("name") or "").strip()]
    acted: list[dict] = []
    for row in pid_rows:
        summary = _watch_one_seat(root, row, windows, _rotate,
                                  now=now, pid_alive=pid_alive,
                                  window_path=window_path, launcher=launcher,
                                  pin_table=pins, seat_sessions=seat_sess)
        if summary:
            acted.append(summary)
    _watch_log(f"watch: seat-dead scan over {len(pid_rows)} configured pid "
               f"row(s); {len(acted)} dead")
    return acted


def _alarm_dispatcher(rec: dict, iter_n: int | str, reason: str, root: Path) -> None:
    """hypothesis:l4-a-round-alarms-its-dispatcher-by-default — a round that
    DIES or TIMES OUT sends the seat that dispatched it exactly ONE dm naming
    the reason. ids/numbers plus a short reason token only. Absent stamp -> one
    stderr line, no crash; an undeliverable dm is logged, never fatal to a heal
    that is already handling a bad day. The dm must go to the ONE shared inbox
    (send.py resolves it through `locations.shared_sessions_dir`), never a
    CWD-local sessions dir that looks delivered to the recipient but is not
    the file they read.
    """
    dispatcher = rec.get("dispatched_by")
    agent_id = rec.get("id", "?")
    if not dispatcher:
        print(f"warn: no dispatcher stamp for {agent_id}; no {reason} dm "
              "(l4-a-round-alarms-its-dispatcher-)", file=sys.stderr)
        return
    try:
        import send as _send
        _send.send(root, dispatcher,
                   f"iter={iter_n} agent={agent_id} reason={reason}",
                   agent_id)
    except Exception as exc:
        print(f"warn: {reason} dm to {dispatcher} failed: {exc}",
              file=sys.stderr)


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _heal_cwd(root: Path, rec: dict) -> Path:
    """The working tree a healer must patch: the agent's OWN worktree when
    the record says it was a `--branch` spawn, else the resolved root.

    `hypothesis:l3-branch-isolation-partial-break`. A healer's cwd decides
    which tree its source edits touch. The old `cwd=str(root)` re-entered the
    MAIN checkout for every healer, so a healer for a branch agent wrote
    main's `extensions/` while the coherent work sat in the worktree. Prefer
    the recorded `worktree` when it is real on disk; fall back to `root`.
    """
    rec_wt = rec.get("worktree")
    if rec_wt:
        wt = Path(rec_wt).resolve()
        if wt.is_dir():
            return wt
    return Path(root)


def _heal(root: Path, iter_n: int | str, agent_id: str, rec: dict) -> None:
    pid = int(rec.get("pid", 0))
    print(f"healer: agent {agent_id} timed out (pid={pid}), killing + spawning healer")
    if pid > 0 and _pid_alive(pid):
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        time.sleep(2)
        if _pid_alive(pid):
            try:
                os.killpg(os.getpgid(pid), signal.SIGKILL)
            except ProcessLookupError:
                pass

    sess_dir = locations.iteration_dir(root, iter_n) / agent_id
    heal_root = _heal_cwd(root, rec)
    log_path = Path(rec.get("log_file", ""))
    log_tail = ""
    if log_path.exists():
        try:
            data = log_path.read_bytes()
            log_tail = data[-4096:].decode("utf-8", errors="replace")
        except Exception:
            log_tail = "(log unreadable)"

    healer_id = f"heal-{uuid.uuid4().hex[:8]}"
    healer_dir = sess_dir / healer_id
    healer_dir.mkdir(parents=True, exist_ok=True)

    healer_ctx = healer_dir / "context.md"
    healer_ctx.write_text(
        f"""# HEALER for hung agent {agent_id} (iter {iter_n})

The original agent timed out. Diagnose what blocked it and patch.

## Original Agent Record
```json
{json.dumps(rec, indent=2)}
```

## Last 4 KiB of Agent Output
```
{log_tail}
```

## Your Task
1. Identify the failure mode: stuck command, missing dep, infinite loop, syntax error, etc.
2. Apply the smallest patch that unblocks it. Leave it UNCOMMITTED in the
   working tree.
   **Do not commit. Do not push. Do not run git at all.** The loop owns every
   commit, and a commit made here is authored as the repo owner, lands
   unreviewed on the checked-out branch, and says something untrue about who
   changed the engine. This line used to read "NEW commit; do not amend" and a
   healer correctly obeyed it on 2026-09-01 (`7b57b5955`) -- the kid contract
   had forbidden git since 2026-08-31 and this one was never updated to match.
3. If unfixable in <5 turns, mark this agent's verdict as `pending` with reason.
4. When done:
   ```
   python3 {CLI_PY} done {iter_n} {agent_id} --verdict pending --confidence 0.0 \\
     --notes "healed by {healer_id}: <one-line diagnosis>"
   ```
   (Use the ORIGINAL `{agent_id}`, not your healer id, so the manifest closes out.)

Stay surgical. Don't refactor unrelated code.
"""
    )

    pi_bin = os.environ.get("PI_BIN", "/home/ubuntu/.npm-global/bin/pi")
    healer_log = healer_dir / "output.log"
    # Two defects fixed here on 2026-08-31, both silent, both on the path that
    # only runs once something else has already gone wrong:
    #
    #   `--max-turns 8`  pi has no such flag. It printed "Unknown option:
    #                    --max-turns" and exited — *with status 0* — so every
    #                    healer this file ever spawned died before reading its
    #                    own context, and the loop recorded it as launched.
    #   raw environment  this Popen had no `env=`, so a healer inherited the
    #                    ANTHROPIC_*/CLAUDE_CODE_* variables dispatch.py
    #                    scrubs, and billed the interactive Claude Code
    #                    subscription. The scrub existed; the healer sat
    #                    outside it.
    #
    # The model flags are new for the same reason dispatch.py grew them: a
    # healer that silently runs a different model than the kid it is repairing
    # is a confusing thing to debug.
    pi_args = [
        pi_bin,
        *_pi_model_args(root, rec.get("tier", "kid"), rec.get("role")),
        # Headless, matching `pi_adapter.build_command`. Note this path ran
        # WITHOUT `-p` and did not hang, which is why the hang that prompted
        # adding it is still unexplained -- see `7b57b5955`.
        "-p",
        "--append-system-prompt", f"@{healer_ctx}",
        f"You are healer {healer_id}. Diagnose and patch.",
    ]
    with open(healer_log, "wb") as logf:
        proc = subprocess.Popen(
            pi_args,
            stdout=logf,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            cwd=str(heal_root),
            env=_scrubbed_env(),
        )

    rec["status"] = "hung-healed"
    rec["healer"] = {
        "id": healer_id,
        "pid": proc.pid,
        "context_file": str(healer_ctx),
        "log_file": str(healer_log),
        "command": " ".join(shlex.quote(a) for a in pi_args),
    }
    rec["finished_at"] = int(time.time())
    (sess_dir / "agent.json").write_text(json.dumps(rec, indent=2))
    print(f"healer {healer_id} spawned pid={proc.pid} for hung agent {agent_id}")


if __name__ == "__main__":
    sys.exit(main())
