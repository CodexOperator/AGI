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
    return _main_heal()


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
    Tests set AGI_REAPER_LOG to a tmp path so they never touch ~/logs; the
    unit (the systemd service) sets it in Environment= or lets it default.
    """
    log = os.environ.get("AGI_REAPER_LOG")
    if log:
        try:
            p = Path(log)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "a", encoding="utf-8") as fh:
                fh.write(line.rstrip("\n") + "\n")
            return
        except Exception as exc:
            print(f"watch: log write failed ({exc}); falling back to stderr",
                  file=sys.stderr)
    print(line, file=sys.stderr)


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
            _watch_log(f"watch: after_join performed for seat {seat!r} "
                       f"({len(result.get('results') or [])} command(s); "
                       f"record appended: {result.get('appended')}, "
                       f"dm sent: {result.get('sent')})")


def _sweep_season(branch: str) -> int | None:
    """Season from a `loop/<slug>-<agent8>@s<N>` branch name, or None.
    Used to fall back to `origin/season/s<N>` as the round's base when the
    worktree's own session records no `base_branch`."""
    if not branch:
        return None
    m = re.search(r"@s(\d+)\s*$", branch)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


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
        return f"origin/season/s{season}"
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
        ("not every agent record is terminal", "non-terminal"),
        ("target already exists and is not empty", "target exists"),
        ("a live lease is active", "live lease"),
        ("this source's own contribution did not verify", "verify failed"),
    ):
        if needle in text:
            return tag
    return "home failed"


def _sweep_bring_home(root: Path, main_sessions: Path, iter_name: str,
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
    """
    if iter_name in homed:
        # already attempted this pass; the memoized outcome holds, but the
        # on-disk target is always re-read because a sibling may have landed it
        return None if (main_sessions / iter_name).is_dir() else homed[iter_name]
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
    # LIVE: only the on-disk target is the proof, never a return code.
    if (main_sessions / iter_name).is_dir():
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
        wt_iters = sorted(wt.glob(".agi/sessions/iter-*"))
        if wt_iters:
            not_home = [d.name for d in wt_iters
                        if not (main_sessions / d.name).is_dir()]
            if not_home:
                rejected: list[str] = []
                homed_now: set[str] = set()
                for dn in not_home:
                    reason = _sweep_bring_home(root, main_sessions, dn,
                                               dry_run, homed)
                    if reason is None:
                        homed_now.add(dn)
                        _watch_log(f"[sweep] homed {agent_id} iter={dn}")
                    else:
                        rejected.append(f"{dn}:{reason}")
                # condition (4) is re-read from DISK for a LIVE pass; a
                # dry-run wrote nothing, so a would-home (helper returned
                # None) counts as home for the removal decision here.
                remaining = [d.name for d in wt_iters
                             if not (main_sessions / d.name).is_dir()
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
