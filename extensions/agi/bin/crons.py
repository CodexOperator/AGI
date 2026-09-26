#!/usr/bin/env python3
"""crons.py — the crontab is a derivation of the graph, never a thing edited
by hand.

**goal:g1.5.** Setting up a project used to be three manual steps and a memory
test: install `grid.py cron`, remember `--publish-engine`, remember to check
which branch is actually pushed. Skip any one of those silently and the
crash-recovery window is not "5 minutes", it is "however long since someone
last remembered" — a failure that looks identical to a healthy project until
the day the history is needed and is not there.

This script removes the memory test. Cadence and enablement live in one
node — `nodes/.geometry/crons.md` (**goal:g10.2**: a geometry node is only
real once something reads it) — and `crons.py apply` is the one command that
makes the real crontab agree with it. The node deliberately carries neither a
command nor a path: **G8.2**'s rule that no machine's layout belongs in a
graph node applies here exactly as it does to the engine itself. Every path
in this file is resolved at apply time through `locations.py`, never stored.

## The branch check is why this file exists at all (S2, non-negotiable)

agi-tree's own history is the falsifier: work once sat 84 commits deep on a
stale `iter24-extend-300hop` branch while an installed cron pushed `master`
on a timer, forever, and reported nothing wrong, because a push that succeeds
looks exactly like a push that matters. **`grid.py`'s own installer never
re-derives the branch — it captures it once, at install time, and a checkout
made after that silently stops being covered.** Every push line this module
renders re-resolves the checked-out branch at *apply* time, and refuses
loudly — never guesses, never falls back to `master`/`main` — when HEAD is
detached. A rendered cron line always names a branch that was real at the
moment it was rendered; the alternative is a line that looks correct forever
and is wrong the day someone runs `git checkout --detach`.

## The self-reapply property

`grid_sync` is the one cadence that always runs (5 minutes, by default), and
the last thing its command does is re-run `crons.py apply` against the real
crontab. So editing `cadences:` or `crons_live:` in the node and letting the
graph get committed *is* the whole change — the running schedule converges
onto whatever the node says within one `grid_sync` interval, with nothing
typed against cron itself. The one edge case worth naming, because the node
names it too: `crons_live: false` removes the job that would have re-applied
the *next* edit, so turning cadences back on takes one manual `apply`, not a
wait for a cadence that no longer exists.

## The managed block, and why unrelated lines are sacred

This machine's crontab carries production lines this project has nothing to
do with. `crons.py` therefore only ever touches lines between one marker pair
it owns:

    # >>> agi-crons <repo-root-hash> >>> project=<repo-root>
    ...rendered lines...
    # <<< agi-crons <repo-root-hash> <<<

The hash is `sha256(repo_root)[:12]` — deterministic per checkout, distinct
per project, so a second project's block in the same crontab is untouched by
construction rather than by convention. Every line outside the matched
BEGIN/END pair is read back and rewritten byte-for-byte, in the same order,
on every `apply` and `remove` — proven in `test_crons.py` by seeding a fake
crontab with unrelated production lines plus another project's block and
asserting both survive an apply-then-remove cycle untouched.

**No write path here ever calls `crontab` unless the caller explicitly asks
for the real one** (the default, with no `--crontab-file`). Every test and
every `--dry-run` exercises `--crontab-file PATH` instead — dependency
injection at the boundary rather than a mock of `subprocess`, so the same
read/write functions run in tests and in production.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import grid  # noqa: E402 -- grid.push_spec_for: ONE spelling of the ref namespace

import yaml

from frontmatter import split_frontmatter  # noqa: E402

# The jobs this project runs today. Order here is the order every
# rendered block and every diff uses — fixed rather than dict/YAML-key order,
# which is what makes "running apply twice is byte-identical" true regardless
# of how the node happens to order its `cadences:` mapping.
KNOWN_JOBS = ("grid_sync", "branch_push", "publish_engine", "engine_push",
              "mail_poll", "nudge_sweep")

#: Relative to the project root `locations.find_project_root` resolves.
#: `rglob("*.md")` traverses dot-directories (confirmed against `level3.py`),
#: so `.geometry/` is an ordinary, reachable node directory, not a hideout.
CRONS_NODE_REL = Path("nodes") / ".geometry" / "crons.md"

MARKER_TAG = "agi-crons"

#: Any agi-owned managed-block marker, for ANY project hash — `audit` uses it
#: to see a block on this box that is not ours (and, matching ours too, to
#: know where our own managed region starts and ends).
AGI_BLOCK_RE = re.compile(r"^#\s*(?:>>>|<<<)\s+agi-crons\s+([0-9a-f]{12})\b")

#: Any agi-owned unit filename, hash-AGNOSTIC — `audit` matches this first so a
#: unit belonging to ANOTHER project's hash is recognised as declared-elsewhere
#: (silence), never as "not declared by this node". The hash is
#: `project_hash(...)[:8]`, the same 8 hex chars `unit_filename` writes.
AGI_UNIT_RE = re.compile(r"^agi-(.+)-([0-9a-f]{8})\.service$")


class CronsError(Exception):
    """A problem with the node, the config, or a repo's state.

    Every raise site names the file or path at fault and what was expected —
    `main()` prints it and exits 1. Deliberately never caught and patched
    over: **"silent in both directions" is the exact defect goal:g1.5 exists
    to remove**, so a cron manager that fails quietly is worse than one that
    does not exist.
    """


# --- reading the node --------------------------------------------------


def _node_path(root: Path) -> Path:
    return Path(root) / CRONS_NODE_REL


def _parse_frontmatter(path: Path) -> dict:
    """Same shape as `backfill-mint-ids.py::read_node` — `text.split("---",
    2)`, not a regex — but this caller cannot skip-and-report the way a bulk
    scan can: there is exactly one crons node, and if it does not parse there
    is nothing to fall back to. Every failure raises `CronsError` naming
    `path`."""
    if not path.is_file():
        raise CronsError(
            f"missing node file {path} — expected YAML frontmatter with "
            f"`crons_live: bool` and `cadences: {{job: {{every_mins|schedule, "
            f"enabled}}}}`"
        )
    text = path.read_text(encoding="utf-8")
    if not text.strip().startswith("---"):
        raise CronsError(f"{path}: no YAML frontmatter (expected a leading `---`)")
    parted = split_frontmatter(text)
    if parted is None:
        raise CronsError(f"{path}: unterminated frontmatter block (only one `---`)")
    try:
        fm = yaml.safe_load(parted[0])
    except yaml.YAMLError as exc:
        raise CronsError(f"{path}: malformed YAML frontmatter — {exc}") from exc
    if not isinstance(fm, dict):
        raise CronsError(f"{path}: frontmatter must be a YAML mapping")
    return fm


def _resolve_cadence(path: Path, name: str, job: dict) -> dict:
    """Validate one `cadences.<name>` entry's shared shape — schedule
    (`every_mins` XOR `schedule`), `enabled`, and the optional `box` gate —
    and return it normalized. Shared by KNOWN_JOBS and by generic (`cmd`)
    entries so an arbitrary job obeys exactly the same rules and the same
    `_on_this_box` gate; a second copy would drift from this one."""
    if not isinstance(job, dict):
        raise CronsError(f"{path}: cadences.{name} must be a mapping")

    enabled = job.get("enabled", True)
    if not isinstance(enabled, bool):
        raise CronsError(f"{path}: cadences.{name}.enabled must be true/false")

    every_mins = job.get("every_mins")
    schedule = job.get("schedule")
    if every_mins is not None and schedule is not None:
        raise CronsError(
            f"{path}: cadences.{name} declares both `every_mins` and "
            f"`schedule` — a job takes exactly one"
        )
    if enabled and every_mins is None and schedule is None:
        raise CronsError(
            f"{path}: cadences.{name} is enabled but declares neither "
            f"`every_mins` nor `schedule`"
        )
    if every_mins is not None and (
        isinstance(every_mins, bool)
        or not isinstance(every_mins, int)
        or every_mins <= 0
    ):
        raise CronsError(
            f"{path}: cadences.{name}.every_mins must be a positive integer"
        )
    if schedule is not None and (
        not isinstance(schedule, str) or len(schedule.split()) != 5
    ):
        raise CronsError(
            f"{path}: cadences.{name}.schedule must be a 5-field cron "
            f"expression, got {schedule!r}"
        )
    entry: dict = {"enabled": enabled, "every_mins": every_mins,
                   "schedule": schedule}
    # Optional `box` (hypothesis:l4-remote-thought-town): a job with NO `box`
    # key renders on EVERY box; an explicit string or list of strings
    # RESTRICTS the job to exactly those boxes. Refused BY NAME when
    # malformed (same pattern as mirror_towns).
    raw_box = job.get("box")
    if raw_box is not None:
        vals = raw_box if isinstance(raw_box, list) else [raw_box]
        if not vals or not all(isinstance(v, str) and v.strip() for v in vals):
            raise CronsError(
                f"{path}: cadences.{name}.box must be a non-empty string "
                f"or list of non-empty strings, got {raw_box!r}"
            )
        entry["box"] = ([v.strip() for v in vals]
                        if isinstance(raw_box, list) else vals[0].strip())
    # Optional `why_box`: a `box` gate is the EXCEPTION (absent = every box,
    # the documented default), so a gated KNOWN job must say why in this
    # sibling field. `audit` flags a gated job without it, by name.
    raw_why = job.get("why_box")
    if raw_why is not None:
        if not isinstance(raw_why, str) or not raw_why.strip():
            raise CronsError(
                f"{path}: cadences.{name}.why_box must be a non-empty string "
                f"— a `box` gate is the exception and says why"
            )
        entry["why_box"] = raw_why.strip()
    return entry


def load_crons_node(root: Path) -> dict:
    """Parse and fully validate the crons node. Returns
    `{"crons_live": bool, "jobs": {name: {"enabled", "every_mins", "schedule"}}}`
    with only the jobs the node actually declares — a job absent from
    `cadences:` never renders, same effect as `enabled: false` but recorded
    distinctly so `show` can tell "declared off" from "never declared".

    Validated in full regardless of `crons_live`: a malformed node is a
    malformed node whether or not it is currently live, and the kill switch
    must not become a way to hide a typo from validation.
    """
    path = _node_path(root)
    fm = _parse_frontmatter(path)

    if "crons_live" not in fm:
        raise CronsError(f"{path}: missing required key `crons_live` (bool)")
    crons_live = fm["crons_live"]
    if not isinstance(crons_live, bool):
        raise CronsError(f"{path}: `crons_live` must be true/false, got {crons_live!r}")

    cadences = fm.get("cadences") or {}
    if not isinstance(cadences, dict):
        raise CronsError(f"{path}: `cadences` must be a mapping of job -> settings")

    known = set(KNOWN_JOBS)
    generic = sorted(set(cadences) - known)
    for name in generic:
        job = cadences[name]
        cmd = job.get("cmd") if isinstance(job, dict) else None
        if not (isinstance(cmd, str) and cmd.strip()):
            raise CronsError(
                f"{path}: cadences declares unknown job {name!r} with no `cmd` "
                f"— known jobs are {list(KNOWN_JOBS)}; any other name needs a "
                f"non-empty `cmd` to run an arbitrary command"
            )

    jobs: dict = {}
    for name in KNOWN_JOBS:
        job = cadences.get(name)
        if job is None:
            continue  # never declared: never rendered, distinct from enabled:false
        jobs[name] = _resolve_cadence(path, name, job)
        if name == "grid_sync":
            # The town MIRROR flag (item 2 of the I-3a-2 order): when true,
            # `render_managed_lines` appends one GUARDED push per declared
            # town publishing `refs/heads/<town>/*` -> `refs/agi/<town>/*`.
            # Declared under the grid_sync cadence so the mirror runs on the
            # same 5-minute heartbeat as the grid ref push. Absent means
            # false. Any non-bool value is refused BY NAME.
            mirror = job.get("mirror_towns", False)
            if not isinstance(mirror, bool):
                raise CronsError(
                    f"{path}: cadences.grid_sync.mirror_towns must be "
                    f"true/false, got {mirror!r}"
                )
            jobs[name]["mirror_towns"] = mirror

    # Generic entries: any name outside KNOWN_JOBS that carries a `cmd`. Same
    # schedule rules and same box gate as a built-in; rendered by the same
    # generic block in `render_managed_lines`. Deterministic order (sorted by
    # name) so `apply` stays byte-identical across runs regardless of how the
    # node's YAML happened to order its keys.
    for name in generic:
        entry = _resolve_cadence(path, name, cadences[name])
        entry["cmd"] = cadences[name]["cmd"]
        log = cadences[name].get("log")
        if log is not None and (not isinstance(log, str) or not log.strip()):
            raise CronsError(
                f"{path}: cadences.{name}.log must be a non-empty string path")
        entry["log"] = log
        jobs[name] = entry

    # Optional `services:` table — systemd unit files rendered from the graph
    # the way the crontab is (hypothesis:l4-the-reaper-is-one-persistent-
    # service). ABSENT (the live state until the prime lands the table) is a
    # byte-for-byte no-op on units, and `crons_live: false` removes them.
    # Units are only ever touched through the `--unit-dir` seam; a plain
    # `crons.py apply` (the grid_sync self-reapply line included) manages
    # nothing but the crontab.
    services: dict = {}
    svc_raw = fm.get("services") or {}
    if not isinstance(svc_raw, dict):
        raise CronsError(f"{path}: `services` must be a mapping of service -> settings")
    for name, svc in svc_raw.items():
        if not isinstance(name, str) or not name.strip():
            raise CronsError(f"{path}: `services` keys must be non-empty names")
        if not isinstance(svc, dict):
            raise CronsError(f"{path}: services.{name} must be a mapping")
        enabled = svc.get("enabled", True)
        if not isinstance(enabled, bool):
            raise CronsError(f"{path}: services.{name}.enabled must be true/false")
        exec_start = svc.get("exec_start")
        if enabled and not (isinstance(exec_start, str) and exec_start.strip()):
            raise CronsError(
                f"{path}: services.{name} is enabled but declares no `exec_start`"
            )
        env = svc.get("environment") or {}
        if not isinstance(env, dict):
            raise CronsError(f"{path}: services.{name}.environment must be a mapping")
        restart = svc.get("restart", "on-failure")
        if not isinstance(restart, str) or not restart.strip():
            raise CronsError(f"{path}: services.{name}.restart must be a non-empty string")
        services[name] = {
            "enabled": enabled,
            "exec_start": exec_start,
            "restart": restart,
            "working_directory": svc.get("working_directory"),
            "environment": env,
        }

    return {"crons_live": crons_live, "jobs": jobs, "services": services}


def _schedule_expr(job: dict) -> str:
    if job["every_mins"] is not None:
        return f"*/{job['every_mins']} * * * *"
    return job["schedule"]


# --- the branch check (S2) ----------------------------------------------


def resolve_branch(git_dir: Path) -> str:
    """The checked-out branch of `git_dir`, re-derived every call.

    Never cached across an install, unlike the defect this exists to fix
    (`grid.py cron install` captures the branch once, at install time). `-q`
    suppresses git's own detached-HEAD message on stderr; this function
    supplies its own, because "refuse loudly" means naming the repo and the
    reason, not forwarding git's wording.
    """
    res = subprocess.run(
        ["git", "-C", str(git_dir), "symbolic-ref", "--short", "-q", "HEAD"],
        capture_output=True, text=True,
    )
    branch = res.stdout.strip()
    if res.returncode != 0 or not branch:
        raise CronsError(
            f"{git_dir}: HEAD is not on a branch (detached?) — refusing to "
            f"render a push line rather than guess `master`/`main`. Check out "
            f"a branch first, or fix this in the node/config, not by hardcoding "
            f"a name here."
        )
    return branch


def _require_git_repo(git_dir: Path, why: str) -> None:
    if not (Path(git_dir) / ".git").exists():
        raise CronsError(f"{git_dir}: not a git repository — needed for {why}")


def _require_dir(path: Path, why: str) -> None:
    if not Path(path).is_dir():
        raise CronsError(f"{path}: no such directory — needed for {why}")


# --- the town mirror -----------------------------------------------------


def _mirror_towns(root: Path) -> list[str]:
    """The town set the mirror renders: `towns.town_tuples(root)` when a
    `town:*` node exists, else the ladder.md `towns:` fallback — the SAME
    resolution `cli.py::_rs_town_set` uses, so the mirror describes the same
    towns the branch reshuffle plans (single source of truth, per the round;
    never a hardcoded app town, goal:g8.2). Imported lazily so grid_sync's
    5-minute cron does not pay cli.py's import cost unless the node asks for
    the mirror.

    Returns `[]` (no mirror lines) when the set is undeclared — a graph with
    no `town:*` node AND no ladder `towns:` list — or when the town set
    cannot be resolved. A corrupt geometry must not brick the crontab apply:
    the mirror is a best-effort publication helper, its lines are guarded
    no-ops until town refs exist anyway, and the live crontab is the higher-
    order invariant."""
    try:
        import cli  # local: same bin dir (may be absent or fail to import)
        tuples, _, declared = cli._rs_town_set(root)
        if not declared:
            return []
        return [t["town"] for t in tuples]
    except Exception:  # noqa: BLE001
        return []


def _mirror_push_line(town: str, root: Path, repo_root: Path, log: Path,
                      sched: str) -> str:
    """One guarded push line rendering every `refs/heads/<town>/*` to
    `refs/agi/<town>/*` on `origin`. The shape (pinned byte-for-byte by
    test_crons_mirror.py): the `for-each-ref` guard runs BEFORE the push, so
    with no `<town>` refs the whole line is a NO-OP — rc 0, nothing pushed,
    nothing logged. Pushes ONLY under `refs/agi/<town>/*`, never
    `refs/heads/...` (the hidden namespace, restored by
    `git config --add remote.origin.fetch '+refs/agi/*:refs/agi/*'`)."""
    return (
        f"{sched} cd {root} && if git -C {repo_root} for-each-ref "
        f"--format='%(refname)' refs/heads/{town}/ | grep -q .; then "
        f"git -C {repo_root} push -q origin "
        f"'refs/heads/{town}/*:refs/agi/{town}/*' >> {log} 2>&1; fi"
    )


# --- rendering -----------------------------------------------------------


def project_hash(repo_root: Path) -> str:
    """Stable per checkout, distinct per project — the whole reason two
    projects can share one crontab without either seeing the other's lines."""
    return hashlib.sha256(str(Path(repo_root).resolve()).encode("utf-8")).hexdigest()[:12]


def block_markers(repo_root: Path) -> tuple[str, str]:
    h = project_hash(repo_root)
    begin = f"# >>> {MARKER_TAG} {h} >>> project={repo_root}"
    end = f"# <<< {MARKER_TAG} {h} <<<"
    return begin, end


#: The alerts file the memory alarm appends to when a graph declares no
#: `logs.alerts_file` cell: a bare NAME, never a path — the directory is
#: `logs_dir()` below, the same dir `enforce_log_caps` bounds.
ALERTS_FILE = "memory-alarm-alerts.log"


def logs_dir() -> Path:
    """The box logs dir — the ONE place `enforce_log_caps` looks, so any
    writer that resolves its log through this directory is capped by
    construction rather than by coincidence."""
    return Path.home() / "logs"


def alerts_log(root: Path) -> Path:
    """The memory alarm's log: a declared `logs.alerts_file` NAME inside
    `logs_dir()`. A writer that re-derived its own path (the pre-fix
    `~/logs/sanctuary-guard/alerts.log`) wrote into a SUBDIRECTORY the
    non-recursive cap glob never reached, so it grew without bound."""
    raw = (locations.load_config(root).get("logs") or {}).get("alerts_file")
    # A NAME, or nothing: an absolute path, a separator, a traversal or an
    # empty value all put the log where the non-recursive cap glob cannot see
    # it, so a malformed cell raises BY NAME exactly as a malformed
    # `logs.cap_mb`/`logs.mode` does -- a cap that silently does not apply is
    # worse than no cap. Only an ABSENT cell falls back to the default: an
    # empty one is a declared-and-wrong value, not an undeclared one.
    name = ALERTS_FILE if raw is None else str(raw).strip()
    if (not name or "\\" in name or "/" in name or name in (".", "..")
            or Path(name).name != name):
        raise CronsError(
            f"config cell logs.alerts_file: must be a bare file NAME inside "
            f"{logs_dir()}, got {name!r} -- a path here would write where "
            f"enforce_log_caps does not look")
    return logs_dir() / name


def _log_path(repo_root: Path) -> Path:
    # One log for every job in this project's block — matches grid.py's own
    # convention of one file per project rather than one per cadence.
    return logs_dir() / f"agi-crons-{Path(repo_root).name}-{project_hash(repo_root)[:8]}.log"


_ARCHIVE_RE = re.compile(r".+\.\d+$")
# The rotation MODE is a declared `logs.mode` cell, never a literal here.
_LOG_MODES = ("rename", "copytruncate")
#: What to do with a base a writer holds open WITHOUT `O_APPEND` (the NUL-hole
#: falsifier): `skip` refuses it by name, `rename` rotates it away instead --
#: the cap then holds and the stranded writer lands in an archive, which the
#: per-archive bound below keeps capped anyway. Declared as `logs.non_append`.
_NON_APPEND_ACTIONS = ("rename", "skip")


def _managed_names(root: Path, repo_root: Path) -> list[str]:
    """The base log NAMES this project declares -- its own cron log, the memory
    alarm's alerts file, plus any extra NAME in `logs.also_manage` (the reaper
    log, which shares the dir). A WILDCARD glob is the near-miss: it bounds
    every archive at the cost of rotating, unlinking and stat'ing files that
    belong to OTHER services (`sanctuary-guard/`, a sibling project's log)."""
    extra = (locations.load_config(root).get("logs") or {}).get("also_manage") or []
    if not isinstance(extra, list):
        raise CronsError("config cell logs.also_manage: must be a list of bare "
                         f"file NAMEs, got {extra!r}")
    names = {_log_path(repo_root).name, alerts_log(root).name}
    for n in extra:
        n = str(n).strip()
        if not n or "/" in n or "\\" in n or n in (".", "..") or Path(n).name != n:
            raise CronsError(f"config cell logs.also_manage: must be a bare file "
                             f"NAME inside {logs_dir()}, got {n!r}")
        names.add(n)
    return sorted(names)


def _non_append_holders(path: Path) -> tuple[bool | None, list[str]]:
    """(False, holders) when a process holds `path` open WITHOUT `O_APPEND` --
    it would resume at its stale offset and leave a NUL hole; (None, []) when
    /proc cannot be read (UNKNOWN, never a silent pass); (True, []) otherwise.
    A box with `hidepid` cannot enumerate other users' fd dirs, so UNKNOWN
    counts the pids this scan had to skip. An `O_APPEND` writer of THIS box is
    always visible -- same uid -- which is the writer the cap is about."""
    unseeable = 0
    try:
        pids = [p for p in Path("/proc").iterdir() if p.name.isdigit()]
    except OSError:
        return None, []
    try:
        want = path.resolve()
    except OSError:
        return None, []
    holders = []
    for pid in pids:
        try:
            fds = list((pid / "fd").iterdir())
        except OSError:
            unseeable += 1           # hidepid: said once per apply, below
            continue
        for fd in fds:
            try:
                if Path(os.readlink(fd)) != want:
                    continue
                info = (pid / "fdinfo" / fd.name).read_text()
            except OSError:
                unseeable += 1
                continue
            flags = next((ln.split()[1] for ln in info.splitlines()
                          if ln.startswith("flags:")), None)
            if flags is None:
                unseeable += 1
                continue
            if not int(flags, 8) & os.O_APPEND:
                holders.append(f"pid {pid.name} fd {fd.name}")
    if holders:
        return False, holders               # a real NUL-hole writer, by name
    return (None, []) if unseeable else (True, [])


def _tail_copy(src: Path, dst: Path, cap: int) -> None:
    """Copy the LAST `cap` bytes of `src` (the whole file when it is shorter)
    into a FRESH `dst`.

    The size is snapshotted once, so a writer still appending to `src` cannot
    make this read chase a moving EOF: `shutil.copyfile` on a live base blocked
    one apply for up to 127 s, and the copy-then-truncate race window is
    `writer_rate x copy duration` (experiment:a00-e4ba316a-1f6748). Cost here is
    a function of `cap` alone, and the archive is never over the cap, so no
    second trimming pass is needed."""
    with open(src, "rb") as fh:
        fh.seek(0, os.SEEK_END)
        size = fh.tell()
        fh.seek(max(0, size - cap))
        left = size - fh.tell()
        with open(dst, "wb") as out:
            while left > 0:
                chunk = fh.read(min(left, 1 << 20))
                if not chunk:      # the writer truncated under us; take what is there
                    break
                out.write(chunk)
                left -= len(chunk)


_NESTED_RE = re.compile(r".*\.\d+\.\d+$")


def _trim_in_place(src: Path, cap: int) -> None:
    """Keep the LAST `cap` bytes of `src`, IN THE SAME INODE.

    An over-cap ARCHIVE is trimmed, not replaced: a `rename`-mode rotation
    strands a long-lived writer on the archive, and replacing the file would
    strand it on a deleted inode -- its bytes going somewhere the cap never
    looks again. The write offset always trails the read offset, so the shift
    cannot overwrite bytes it has yet to read."""
    with open(src, "r+b") as fh:
        size = fh.seek(0, os.SEEK_END)
        fh.seek(max(0, size - cap))
        done = 0
        while done < cap:
            chunk = fh.read(min(1 << 20, cap - done))
            if not chunk:            # a writer truncated under us
                break
            fh.seek(done)
            fh.write(chunk)
            done += len(chunk)
        fh.truncate(done)

#: The same two shapes, matched on the SUFFIX (`x.log` + `.1.1`), because the
#: declared-name scope selects `x.log.*` and must then tell an archive tail
#: from a sibling that merely starts with the same characters.
_ARCHIVE_TAIL_RE = re.compile(r"\.\d+$")
_NESTED_TAIL_RE = re.compile(r"\.\d+\.\d+(\.\d+)*$")


def enforce_log_caps(root: Path, repo_root: Path, dry_run: bool = False,
                     live: bool = True) -> list[str]:
    """Rotate every file in the box logs dir that is over the declared cap.

    The cap is the `logs.cap_mb` / `logs.rotations` cells in
    `.agi/config.json`, read at apply time -- never a literal here. An ABSENT
    `logs` namespace is a no-op (nothing is declared to enforce); a PRESENT
    but malformed one raises by name, because a cap that silently does not
    apply is worse than no cap. The scope is this project's DECLARED names
    (`_log_path`, `alerts_log`, plus `logs.also_manage`) and their `.N`
    archives -- never a `*` glob, which reaches into other services' files --
    and EVERY managed archive is bounded, not only the one a rotation just
    made. `live=False` (the `crons_live: false` kill switch) is a no-op.
    The MODE is the `logs.mode` cell: `rename` (the default) renames the base,
    which strands a long-lived writer on an uncapped ARCHIVE; `copytruncate`
    copies the newest `cap` bytes to `.1` and truncates the base IN PLACE, so an
    `O_APPEND` writer keeps landing in a file the next apply still caps. The
    copy reads a snapshotted size, so its cost is bounded by the cap and the
    copy-then-truncate race costs only the bytes appended between the copy and
    the truncate. A writer that is NOT `O_APPEND` is REFUSED by name before the
    in-place truncate (falsifier 2): the cap holds, the file shape does not.
    """
    cells = locations.load_config(root).get("logs") or {}
    if not cells:
        return []
    cap_mb, keep = cells.get("cap_mb"), cells.get("rotations")
    mode = cells.get("mode", "rename")
    if not (isinstance(cap_mb, int) and cap_mb > 0
            and isinstance(keep, int) and keep >= 0):
        raise CronsError(
            f"config cells logs.cap_mb/logs.rotations: cap_mb must be a "
            f"positive integer and rotations a non-negative one, got "
            f"{cap_mb!r}/{keep!r} -- a cap that silently does not apply is "
            f"worse than no cap")
    if mode not in _LOG_MODES:
        raise CronsError(
            f"config cell logs.mode: must be one of {sorted(_LOG_MODES)}, got "
            f"{mode!r} -- a rotation mode this file does not implement would "
            f"silently leave the cap unenforced")
    non_append = cells.get("non_append", "skip")
    if non_append not in _NON_APPEND_ACTIONS:
        raise CronsError(f"config cell logs.non_append: must be one of "
                         f"{sorted(_NON_APPEND_ACTIONS)}, got {non_append!r}")
    # The kill switch: `crons_live: false` schedules NOTHING, so a cap that
    # keeps rotating and unlinking behind it is a surprise with no job to
    # explain it. Gated HERE, at the one function that touches the dir.
    if not live:
        return []
    cap, out, d = cap_mb * 1024 * 1024, [], logs_dir()
    if not d.is_dir():
        return []
    names = _managed_names(root, repo_root)
    entries = sorted(d.iterdir())
    unknown_said = False
    for name in names:
        p = d / name
        # (1) EVERY archive of a declared name is bounded, not just the base:
        # `_tail_copy` bounds only the NEW archive, so a pre-existing 172 MB
        # archive stayed over the cap forever, the apply saying nothing.
        for q in [q for q in entries if q.name.startswith(f"{name}.")]:
            tail = q.name[len(name):]
            if q.is_symlink() or not q.is_file():
                continue
            if _NESTED_TAIL_RE.match(tail):
                out.append(f"{q.name} pruned (legacy rotation residue)"
                           + (" (dry-run)" if dry_run else ""))
                if not dry_run:
                    q.unlink()
                continue
            if not _ARCHIVE_TAIL_RE.match(tail):
                continue
            if q.stat().st_size <= cap:
                continue
            if dry_run:
                out.append(f"{q.name} is over the {cap_mb} MB cap (dry-run)")
                continue
            _trim_in_place(q, cap)
            out.append(f"{q.name} bounded to the {cap_mb} MB cap (archive)")
        if p.is_symlink() or not p.is_file():
            continue
        if p.stat().st_size <= cap:  # over-cap is strictly `>`
            continue
        if dry_run:
            out.append(f"{p.name} is over the {cap_mb} MB cap (dry-run)")
            continue
        if mode == "copytruncate":
            # Truncating IN PLACE under a writer that did NOT open O_APPEND
            # leaves a NUL hole at its stale offset: the cap holds, the file
            # shape does not. UNKNOWN is said, never assumed.
            clean, holders = _non_append_holders(p)
            if clean is None and not unknown_said:
                unknown_said = True
                out.append(f"{name} writer check UNKNOWN (/proc not fully "
                           f"readable: hidepid) -- the O_APPEND contract is "
                           f"assumed, not proven")
            elif clean is False and non_append == "skip":
                out.append(f"{name} refused: held without O_APPEND by "
                           f"{', '.join(holders)} (logs.non_append: skip)")
                continue
        if Path(f"{p}.{keep}").exists():
            Path(f"{p}.{keep}").unlink()  # the oldest rotation leaves
        for i in range(keep - 1, 0, -1):
            if Path(f"{p}.{i}").exists():
                Path(f"{p}.{i}").replace(f"{p}.{i + 1}")
        if keep:
            if mode == "copytruncate":
                # The writer's fd is the BASE INODE (every crontab line is a
                # `>>` redirect), so COPY to `.1` and truncate the same inode
                # in place: later bytes re-enter a file the cap still governs,
                # never an ARCHIVE that `_ARCHIVE_RE` skips forever.
                arch = Path(f"{p}.1")
                _tail_copy(p, arch, cap)   # bounded, and <= cap by construction
                if arch.stat().st_size > cap:
                    # Only a live writer that SHRANK the base under us can land
                    # here (a concurrent truncation mid-copy); the cap is a cap.
                    with open(arch, "r+b") as fh:
                        fh.truncate(cap)
            else:
                arch = Path(f"{p}.1")
                p.replace(arch)
                # `rename` moved the WHOLE over-cap base into `.1`, and the
                # archive-bounding loop above ran BEFORE this rotation -- so
                # without this line the apply returns holding an over-cap
                # archive in the DEFAULT mode, and only `copytruncate` (whose
                # `_tail_copy` bounds by construction) was ever covered.
                # Bounded IN PLACE, in the same inode the stranded writer
                # still holds: a `replace()` here would strand it on a
                # deleted inode (experiment:a00-945d7ae4-8974f4).
                if arch.stat().st_size > cap:
                    _trim_in_place(arch, cap)
                    out.append(f"{arch.name} bounded to the {cap_mb} MB cap "
                               f"(new archive)")
        p.write_text("", encoding="utf-8")
        out.append(f"{p.name} rotated (cap {cap_mb} MB, {keep} kept)")
    return out


def _on_this_box(job: dict, own: str) -> bool:
    """The job's `box` gate: absent = every box; a string/list restricts it.

    An empty `own` (a graph that declares no box anywhere) gates nothing.
    """
    b = job.get("box")
    if not b or not own:
        return True
    return own in b if isinstance(b, list) else own == b


def _this_box(root: Path, box_name: str | None = None) -> str:
    """The box this checkout is on, for the `box` gate and the `{box}`
    placeholder. Unresolved (no `AGI_BOX`, no `default_box` cell) is the empty
    string, which gates nothing in `_on_this_box` and substitutes to nothing."""
    if box_name:
        return box_name
    try:
        import boxes
        return boxes.this_box(root) or ""
    except Exception:  # noqa: BLE001 -- no box declared: gate/substitute nothing
        return ""


def _substitute(text, root: Path, repo_root: Path, own: str):
    """Resolve `{root}`, `{repo_root}`, `{logs}`, `{box}` through the ONE
    schema-declared map (`boxes.resolve_placeholders`), never a second literal
    token list here. Values come from what the renderers already compute --
    never `boxes.box_cells(root)`, whose live cells belong to a foreign box.
    Never `str.format()`: a cron `cmd` is arbitrary shell and may carry stray
    `{`/`}` `format` would mis-substitute. Non-strings pass through."""
    if not isinstance(text, str):
        return text
    import boxes
    cells = {"root": str(root),
             "logs_dir": str(_log_path(repo_root).parent),
             "repo_root": str(repo_root),
             "box": own}
    try:
        return boxes.resolve_placeholders(text, cells, Path(root))
    except boxes.BoxSchemaError as exc:
        # Fail closed BY NAME: an unrenderable token is `ERR: crons.py:` rc 1,
        # never a traceback out of main's CronsError-only handler.
        raise CronsError(f"placeholder render: {exc}") from exc


def render_managed_lines(root: Path, repo_root: Path, engine_root: Path, node: dict,
                         box_name: str | None = None) -> list[str]:
    """The job lines this project's node describes, in `KNOWN_JOBS` order.

    Every line starts with `cd {root} &&` — a cd-less cron line is a named
    failure mode in this project's design ethic, because cron itself runs
    from `$HOME` and every relative assumption a command makes silently
    breaks. `root` (not `repo_root`) is used for the `cd`, matching every
    other entry point in this engine ("run from anywhere inside this repo");
    git operations still address `repo_root`/`engine_root` explicitly via
    `-C`, since under goal:g11 those are not always the same directory as
    `root`.

    Returns `[]` when `crons_live` is false — the kill switch removes every
    line this function would otherwise emit, `grid_sync`'s self-reapply
    included.
    """
    if not node["crons_live"]:
        return []

    jobs = node["jobs"]
    own = _this_box(root, box_name)
    log = _log_path(repo_root)
    lines: list[str] = []

    if "grid_sync" in jobs and jobs["grid_sync"]["enabled"] and _on_this_box(jobs["grid_sync"], own):
        _require_git_repo(repo_root, "grid_sync's grid-ref push")
        grid_py = Path(engine_root) / "extensions" / "agi" / "bin" / "grid.py"
        # Deliberately NOT `Path(__file__)`. This path is persisted into a cron
        # line that outlives the process rendering it, so it must name the
        # durable copy of the applier, not whichever copy happened to run
        # `apply`. Rendering from `payloads/` — the normal way engine work is
        # done today (goal:g6.3) — would bake a gitignored staging path into
        # the one job that re-applies every other job: `grid.py checkout
        # --force` can overwrite it and a fresh clone does not have it at all.
        # Same `engine_root` arithmetic as every other command here.
        crons_py = Path(engine_root) / "extensions" / "agi" / "bin" / "crons.py"
        # Residue (b): the self-reapply carries --unit-dir so crons_live:false
        # genuinely STOPS the unit (disable --now + file removal + reload) the
        # moment the node says so — the kill switch is real, not prose. The
        # path is the real user-manager dir systemd --user reads; it is safe
        # to bake today because `reconcile_units` is a no-op until a services
        # table lands in the live node, and it never holds a credential.
        udir = Path.home() / ".config" / "systemd" / "user"
        sched = _schedule_expr(jobs["grid_sync"])
        # `;` between the three steps, deliberately NOT `&&`: the last step is
        # the self-reapply, and it must run whether or not the grid commit
        # succeeded (`hypothesis:l4-a-worktree-looks-like-a-project-to-the-
        # crontab` ITEM 2). A `&&`-chain made the declaration's own healing
        # step a victim of an unrelated step's exit code — a grid refusal
        # silently stopped the crontab from tracking the node. With `;`, each
        # step runs on its own, and because each still redirects `>> {log}
        # 2>&1`, a grid failure is still written to the log — visible, not
        # swallowed. The leading `cd {root} &&` is kept: cd is a premise,
        # not a failure domain.
        cmd = (
            f"python3 {grid_py} commit --all --prefix 'cron: ' >> {log} 2>&1; "
            f"python3 {grid_py} push-changed >> {log} 2>&1; "
            f"python3 {crons_py} apply --unit-dir {udir} >> {log} 2>&1"
        )
        lines.append(f"{sched} cd {root} && {cmd}")

        # The town MIRROR (item 2): when grid_sync's `mirror_towns` is true,
        # append one GUARDED push per declared town. Runs on the same
        # grid_sync schedule. Each line is inert (rc 0, no push, no log
        # noise) while no `refs/heads/<town>/*` exists — the live state
        # today — and lands under `refs/agi/<town>/*` only when the branch
        # reshuffle actually creates town branches.
        if jobs["grid_sync"].get("mirror_towns"):
            for tn in _mirror_towns(root):
                lines.append(
                    _mirror_push_line(tn, root, repo_root, log, sched)
                )

    if "branch_push" in jobs and jobs["branch_push"]["enabled"] and _on_this_box(jobs["branch_push"], own):
        _require_git_repo(repo_root, "branch_push")
        branch = resolve_branch(repo_root)
        sched = _schedule_expr(jobs["branch_push"])
        lines.append(
            f"{sched} cd {root} && git -C {repo_root} push -q origin {branch} >> {log} 2>&1"
        )

    if "publish_engine" in jobs and jobs["publish_engine"]["enabled"] and _on_this_box(jobs["publish_engine"], own):
        _require_dir(engine_root, "publish_engine")
        publisher = Path(engine_root) / "extensions" / "agi" / "bin" / "publish-engine.sh"
        sched = _schedule_expr(jobs["publish_engine"])
        lines.append(f"{sched} cd {root} && bash {publisher} >> {log} 2>&1")

    if "engine_push" in jobs and jobs["engine_push"]["enabled"] and _on_this_box(jobs["engine_push"], own):
        _require_git_repo(engine_root, "engine_push")
        engine_branch = resolve_branch(engine_root)
        sched = _schedule_expr(jobs["engine_push"])
        lines.append(
            f"{sched} cd {root} && git -C {engine_root} push -q origin {engine_branch} >> {log} 2>&1"
        )

    if "mail_poll" in jobs and jobs["mail_poll"]["enabled"] and _on_this_box(jobs["mail_poll"], own):
        _require_git_repo(repo_root, "mail_poll's hub fetch")
        send_py = Path(engine_root) / "extensions" / "agi" / "bin" / "send.py"
        rotate_py = Path(engine_root) / "extensions" / "agi" / "bin" / "rotate.py"
        sched = _schedule_expr(jobs["mail_poll"])
        # Fetch the hub, then read every LOCAL row's inbox. `read --box-local`
        # is the one service reader that is allowed to consume more than its
        # own inbox; every foreign-box row is skipped inside it by name. The
        # SAME tick then receives: `migrate --receive` seats a verified
        # quick-migrate record addressed to THIS box (SM.123 conjunct 2).
        # `;` not `&&` -- a read refusal must never skip the receive half.
        lines.append(
            f"{sched} cd {root} && git -C {repo_root} fetch -q origin && "
            f"python3 {send_py} read --box-local >> {log} 2>&1; "
            f"python3 {rotate_py} migrate --receive >> {log} 2>&1"
        )

    if "nudge_sweep" in jobs and jobs["nudge_sweep"]["enabled"] and _on_this_box(jobs["nudge_sweep"], own):
        # The sweep walks every LOCAL row itself (`wake --all-local`), so no
        # seat list is hardcoded here: the whole point is that a busy pane's
        # nudge is retried until it lands, box default = every box.
        send_py = Path(engine_root) / "extensions" / "agi" / "bin" / "send.py"
        sched = _schedule_expr(jobs["nudge_sweep"])
        lines.append(
            f"{sched} cd {root} && python3 {send_py} wake --all-local "
            f">> {log} 2>&1"
        )

    # Generic entries last, sorted by name: KNOWN_JOBS keep their own
    # special-cased renderers above (unchanged), and any other declared name
    # carrying a `cmd` renders in one fixed shape through the SAME
    # `_on_this_box` gate and the same `cd {root} && … >> log 2>&1` shape as a
    # built-in.
    for name in sorted(jobs):
        if name in KNOWN_JOBS:
            continue
        job = jobs[name]
        if not (job["enabled"] and _on_this_box(job, own)):
            continue
        sched = _schedule_expr(job)
        cmd = _substitute(job["cmd"], root, repo_root, own)
        glog = Path(job["log"]) if job.get("log") else _log_path(repo_root)
        lines.append(f"{sched} cd {root} && {cmd} >> {glog} 2>&1")

    return lines


# --- systemd unit rendering (opt-in via the --unit-dir seam) ------------


def unit_filename(repo_root: Path, name: str, unit_dir: Path) -> Path:
    """One unit file per service, hashed per checkout like the crontab block
    so a second project's units never collide and C4.4's naming stays
    deterministic."""
    return Path(unit_dir) / f"agi-{name}-{project_hash(repo_root)[:8]}.service"


def render_unit_file(name: str, svc: dict, repo_root: Path) -> list[str]:
    """The systemd unit lines for one service, in a fixed order so a second
    apply is byte-identical. No credentials ever go in `Environment=` — the
    claim's hard rule ("it never reads a credential") is enforced here by
    never templating a secrets source; callers bring only plain key=value
    settings."""
    log = _log_path(repo_root)
    wd = svc["working_directory"] or str(repo_root)
    lines = ["[Unit]", f"Description=agi {name} (project {Path(repo_root).name})",
             "After=network.target", "Wants=network.target", "", "[Service]",
             "Type=simple", f"ExecStart={svc['exec_start']}",
             f"WorkingDirectory={wd}", f"Restart={svc['restart']}"]
    for k, v in svc["environment"].items():
        lines.append(f"Environment={k}={v}")
    lines.append(f"StandardOutput=append:{log}")
    lines.append(f"StandardError=append:{log}")
    lines += ["", "[Install]", "WantedBy=default.target"]
    return lines


def _systemd_bus_env() -> dict[str, str] | None:
    """Env additions so `systemctl --user` can reach the user bus, or None
    when no bus is reachable and the call would necessarily fail.

    - Caller already has DBUS_SESSION_BUS_ADDRESS (an interactive shell has
      it and XDG_RUNTIME_DIR): reachable, adds nothing — the inherited env
      already carries the bus.
    - No caller bus but the XDG_RUNTIME_DIR bus socket exists (the CRON case:
      cron runs with neither var, the socket is there, give the call the
      address): returns XDG_RUNTIME_DIR + DBUS_SESSION_BUS_ADDRESS.
    - Socket absent too: None — any `systemctl --user` call is doomed (logs
      `No medium found`). The caller records ONE named skip instead of two
      FAILED actions, because a healing step that only runs when the bus is
      up and then FAILs is not a healing step (CLAUDE.md).
    """
    if os.environ.get("DBUS_SESSION_BUS_ADDRESS"):
        return {}
    runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/run/user/{os.getuid()}"
    if os.path.exists(f"{runtime}/bus"):
        return {"XDG_RUNTIME_DIR": runtime,
                "DBUS_SESSION_BUS_ADDRESS": f"unix:path={runtime}/bus"}
    return None


def _apply_systemctl(args: list[str], *, dry_run: bool,
                     env: dict[str, str] | None = None,
                     read_only: bool = False) -> str:
    """Actually run `systemctl --user <args>` via PATH — a FAKE systemctl in
    tests (residue b: tests prove the exact argv and never touch the real
    user manager or ~/.config/systemd). The real user manager is only ever
    reached when a services table has landed and grid_sync self-reapplies
    with `--unit-dir`. Under `--dry-run` the intent is recorded and nothing
    runs (unless `read_only`, see below). A failed systemctl becomes a
    visible action string, never an exception — a crontab apply must not die
    midway because one unit refused.

    `read_only` marks a genuinely READ-ONLY probe (`is-enabled` / `is-active`
    or any byte comparison that mutates nothing) so a `--dry-run` apply can
    ask the same question the live pass would ask and reach the same branch:
    with `dry_run and read_only` the subprocess still RUNS (it mutates
    nothing) and its real `(ok)`/`FAILED (...)` string is returned — a dry
    run must not answer a question the live pass does not ask (the original
    bug: every dry run printed seam intent for a unit the live pass marked
    `(no-op)`). Mutations (daemon-reload, enable/disable --now, writes,
    removes) keep `read_only=False` and so NEVER run under `--dry-run`.

    `env`, when given, is merged over the caller's environment before the
    subprocess runs so a cron-invoked apply can reach the user bus (see
    `_systemd_bus_env`). The env never changes the argv the FAKE records, so
    tests assert argv exactly as before with the caller's bus already set
    (`{}`).
    """
    label = " ".join(["systemctl", "--user", *args])
    if dry_run and not read_only:
        return f"{label} (dry-run)"
    merged = os.environ.copy()
    if env:
        merged.update(env)
    try:
        res = subprocess.run(["systemctl", "--user", *args],
                             capture_output=True, text=True, timeout=60,
                             env=merged)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return f"{label} FAILED ({exc})"
    if res.returncode != 0:
        detail = (res.stderr or res.stdout or "unknown error").strip()
        return f"{label} FAILED ({detail})"
    return f"{label} (ok)"


def reconcile_units(root: Path, repo_root: Path, node: dict,
                    unit_dir: Path | None, dry_run: bool) -> list[str]:
    """Reconcile the node's `services:` table against `unit_dir`.

    Returns a list of action strings (what happened, or would happen in
    `--dry-run`). The unit FILE is only ever written under `unit_dir`; the
    `systemctl --user` calls (daemon-reload, enable/disable --now) run on
    PATH, which tests point at a FAKE systemctl that records argv — never the
    real user manager. The live install remains the prime's step at
    merge-up; a plain apply (no `--unit-dir`) still never touches units.

    No `services` table at all -> byte-for-byte no-op on units (the live
    state until the prime lands the table). `crons_live: false` is the kill
    switch: disable --now, remove the unit file, daemon-reload — genuinely
    stopping the unit, not just recording the prose.
    """
    if unit_dir is None:
        return []  # unit management is opt-in; plain apply never touches units
    ud = Path(unit_dir)
    actions: list[str] = []
    if not node["services"]:
        return actions
    own = _this_box(root)

    def _sub_svc(svc: dict) -> dict:
        """Resolve the four placeholders in every string-valued service
        field BEFORE it reaches the unit file, so the node carries no box
        path and a fresh box renders its own."""
        out = dict(svc)
        out["exec_start"] = _substitute(svc["exec_start"], root, repo_root, own)
        out["working_directory"] = _substitute(
            svc["working_directory"], root, repo_root, own)
        out["environment"] = {
            k: _substitute(v, root, repo_root, own)
            for k, v in (svc["environment"] or {}).items()}
        return out

    for name, svc in node["services"].items():
        target = unit_filename(repo_root, name, ud)
        service_arg = target.name
        wanted = node["crons_live"] and svc["enabled"]
        if wanted:
            desired = "\n".join(render_unit_file(name, _sub_svc(svc), repo_root)) + "\n"
            up_to_date = (target.is_file()
                          and target.read_text(encoding="utf-8") == desired)
            # Make systemd SEE and START the unit (idempotent in systemd).
            # Under cron there is no login session; reach the user bus via
            # _systemd_bus_env, or record one named skip when no bus exists
            # (was two FAILED `No medium found` actions every 5 minutes).
            def seam() -> None:
                bus_env = _systemd_bus_env()
                if bus_env is None:
                    actions.append(
                        f"unit {target.name} no user bus, skip systemctl")
                else:
                    actions.append(_apply_systemctl(["daemon-reload"],
                                                    dry_run=dry_run,
                                                    env=bus_env))
                    actions.append(_apply_systemctl(["enable", "--now",
                                                     service_arg],
                                                    dry_run=dry_run,
                                                    env=bus_env))

            if up_to_date:
                # Bytes are current. Probe whether systemd already sees the
                # unit enabled AND active (through the same seam, so the bus
                # env applies). If so, record ONE state line and run neither
                # daemon-reload nor enable — a :x5 apply stops churning two
                # `(ok)` actions every pass. Any other state (not enabled,
                # not active, probe FAILED) runs the real seam so a written-
                # but-never-enabled unit still converges on the next apply.
                actions.append(f"unit {target.name} up to date")
                bus_env = _systemd_bus_env()
                if bus_env is None:
                    actions.append(
                        f"unit {target.name} no user bus, skip systemctl")
                else:
                    enabled = _apply_systemctl(["is-enabled", service_arg],
                                               dry_run=dry_run, env=bus_env,
                                               read_only=True)
                    active = _apply_systemctl(["is-active", service_arg],
                                              dry_run=dry_run, env=bus_env,
                                              read_only=True)
                    if enabled.endswith("(ok)") and active.endswith("(ok)"):
                        actions.append(
                            f"unit {target.name} enabled+active (no-op)")
                    else:
                        seam()
            elif dry_run:
                actions.append(f"write unit {target.name} (dry-run)")
                seam()
            else:
                ud.mkdir(parents=True, exist_ok=True)
                target.write_text(desired, encoding="utf-8")
                actions.append(f"write unit {target.name}")
                seam()
        else:
            # crons_live false, or the service disabled: the kill switch
            # STOPS the unit through the real seam (disable --now), removes
            # the file, and reloads so the removal is seen by systemd.
            if target.exists():
                bus_env = _systemd_bus_env()
                if bus_env is not None:
                    actions.append(_apply_systemctl(
                        ["disable", "--now", service_arg],
                        dry_run=dry_run, env=bus_env))
                    if not dry_run:
                        target.unlink()
                        actions.append(f"remove unit {target.name}")
                    else:
                        actions.append(f"remove unit {target.name} (dry-run)")
                    actions.append(_apply_systemctl(["daemon-reload"],
                                                    dry_run=dry_run,
                                                    env=bus_env))
                else:
                    # No bus: cannot disable --now, so the unit may STILL be
                    # running. Do NOT remove the file — dropping it while the
                    # unit runs leaves a running unit systemd no longer knows
                    # (an orphan it can then never manage). Record one named
                    # skip governing the whole kill; a later apply with a bus
                    # comes back, disables, removes, reloads.
                    actions.append(
                        f"unit {target.name} present, no user bus: "
                        "disable --now SKIPPED (unit may still be running)")
                    actions.append(
                        f"unit {target.name} no user bus, skip daemon-reload")
            else:
                # Unit already gone (crons_live flipped after a manual remove,
                # or never landed): not loaded, so nothing to disable. Record
                # the state in one line — was `disable --now` on an absent
                # unit logging FAILED every 5 minutes.
                actions.append(f"unit {target.name} absent, nothing to disable")
    return actions


# --- crontab I/O: dependency-injected, never writes the real one uninvited --


def read_crontab(crontab_file: Path | str | None = None) -> list[str]:
    """`crontab -l`, or a fixture file when `crontab_file` is given.

    A missing fixture file reads as an empty crontab (a fresh machine has no
    crontab either, and `crontab -l` on one exits non-zero the same way).
    """
    if crontab_file is not None:
        p = Path(crontab_file)
        return p.read_text(encoding="utf-8").splitlines() if p.exists() else []
    res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    return res.stdout.splitlines() if res.returncode == 0 else []


def write_crontab(lines: list[str], crontab_file: Path | str | None = None) -> None:
    """`crontab -`, or a fixture file when `crontab_file` is given.

    This is the one function that mutates a real crontab, and it is called
    from exactly one place below (`cmd_apply`/`cmd_remove`, guarded by
    `dry_run`). Every test in `test_crons.py` and every `--dry-run` passes
    `crontab_file`, so the real path is exercised only by the parent's
    intentional, reviewed run — never by this script's own test suite.
    """
    text = "\n".join(lines) + ("\n" if lines else "")
    if crontab_file is not None:
        Path(crontab_file).write_text(text, encoding="utf-8")
        return
    res = subprocess.run(["crontab", "-"], input=text, capture_output=True, text=True)
    if res.returncode != 0:
        raise CronsError(f"crontab install failed: {res.stderr.strip()}")


def split_managed_block(lines: list[str], begin: str, end: str) -> tuple[list, list, list]:
    """`(before, managed, after)` — `before`/`after` are byte-for-byte,
    order-preserved copies of everything outside this project's block.

    No match at all: `(lines, [], lines-has-no-after)` — i.e. nothing to
    remove, and a fresh `apply` appends the new block at the end. A `BEGIN`
    with no matching `END` is a hand-edited or corrupted crontab, and this
    refuses rather than guessing where the block was meant to stop.
    """
    try:
        i = lines.index(begin)
    except ValueError:
        return list(lines), [], []
    try:
        j = lines.index(end, i + 1)
    except ValueError:
        raise CronsError(
            f"crontab has {begin!r} with no matching {end!r} — refusing to "
            f"guess where the managed block ends; fix or remove it by hand"
        )
    return lines[:i], lines[i + 1:j], lines[j + 1:]


# --- commands --------------------------------------------------------------


def _resolve(root: Path) -> tuple[Path, dict, Path, Path, dict]:
    """The five things every command needs: `(root, cfg, repo_root,
    engine_root, node)`."""
    cfg = locations.load_config(root)
    repo_root = locations.repo_root(root)
    engine_root = locations.source_root(root, cfg)
    node = load_crons_node(root)
    return root, cfg, repo_root, engine_root, node


def require_common_root(root: Path, repo_root: Path) -> None:
    """Refuse, loudly, when `repo_root` is a LINKED git worktree rather than
    the main checkout — the sixth face of the shared-state boundary
    (`hypothesis:l4-a-worktree-looks-like-a-project-to-the-crontab` ITEM 1).

    `locations.repo_root` resolves a linked worktree to the worktree itself
    (``.../.agi/worktrees/<name>``), which is correct for the graph a kid
    edits but wrong for a machine-global resource like the user's crontab:
    the block marker hashes that path, so an `apply` from a seat would APPEND
    A SECOND managed block beside the main checkout's — and because a seat
    branch is refused by `grid.py` (`master` or `season/*` only), that second
    block could never run, forever, while looking installed. The crontab is
    ONE PER USER, and the managed block must key on the one directory every
    worktree shares — `locations.git_common_root`. When the two disagree this
    raises `CronsError`; a caller must not guess. An ordinary non-worktree
    clone resolves both to the same root and is untouched.
    """
    common = locations.git_common_root(root)
    if Path(common).resolve() != Path(repo_root).resolve():
        raise CronsError(
            f"resolved repo_root {repo_root} is a LINKED GIT WORKTREE, not the "
            f"common root {common}. The user's crontab is ONE PER USER; an "
            f"apply/show from a worktree would key the managed block on a "
            f"hash no other checkout uses and append a second block that "
            f"could never run. Run from the main checkout instead: "
            f"cd {common} && extensions/agi/bin/crons.py apply"
        )


def cmd_apply(root: Path, crontab_file: Path | str | None = None, dry_run: bool = False,
              unit_dir: Path | str | None = None) -> dict:
    """Render the node and reconcile the crontab. Idempotent by construction:
    the managed block replaces itself in place (or is appended once, on first
    install), so a second `apply` with nothing changed produces byte-identical
    output — proven in `test_crons.py::test_apply_twice_is_byte_identical`.

    When `unit_dir` is given (the fixture seam), also reconcile the node's
    `services:` table against that directory; without it, units are never
    touched.
    """
    root, cfg, repo_root, engine_root, node = _resolve(root)
    require_common_root(root, repo_root)
    managed = render_managed_lines(root, repo_root, engine_root, node)
    # Every managed line redirects `>> {log} 2>&1`, and `_log_path` lives in
    # `~/logs/` which nothing else creates: on a fresh box the first tick
    # wrote NOTHING and no error anywhere. Create it where the lines are
    # installed, never on a dry run.
    if managed and not dry_run:
        _log_path(repo_root).parent.mkdir(parents=True, exist_ok=True)
    begin, end = block_markers(repo_root)

    current = read_crontab(crontab_file)
    before, existing, after = split_managed_block(current, begin, end)

    if managed:
        new_lines = before + [begin] + managed + [end] + after
    else:
        # crons_live: false, or a node that declares no jobs at all: the
        # kill switch removes every line for this project, markers included.
        new_lines = before + after

    changed = new_lines != current
    if not dry_run:
        write_crontab(new_lines, crontab_file)

    unit_actions = reconcile_units(root, repo_root, node, unit_dir, dry_run)
    log_actions = enforce_log_caps(root, repo_root, dry_run,
                                  live=node["crons_live"])

    return {
        "root": root, "repo_root": repo_root, "engine_root": engine_root,
        "crontab_lines": new_lines, "managed_lines": managed,
        "previous_managed_lines": existing, "changed": changed,
        "crons_live": node["crons_live"],
        "unit_actions": unit_actions, "unit_dir": unit_dir,
        "log_actions": log_actions,
    }


def cmd_show(root: Path, crontab_file: Path | str | None = None) -> str:
    root, cfg, repo_root, engine_root, node = _resolve(root)
    require_common_root(root, repo_root)
    desired = render_managed_lines(root, repo_root, engine_root, node)
    begin, end = block_markers(repo_root)
    current = read_crontab(crontab_file)
    _, installed, _ = split_managed_block(current, begin, end)

    out = [f"project: {repo_root}", f"crons_live: {node['crons_live']}", ""]
    out.append("installed:")
    out.extend(f"  {l}" for l in installed) if installed else out.append("  (none)")
    out.append("")
    out.append("desired:")
    out.extend(f"  {l}" for l in desired) if desired else out.append(
        "  (none — crons_live is false, or no job is enabled)"
    )
    out.append("")
    if installed == desired:
        out.append("status: up to date")
    else:
        out.append("status: DRIFT — installed crontab does not match the node")
        out.extend(
            difflib.unified_diff(installed, desired, fromfile="installed",
                                 tofile="desired", lineterm="")
        )
    return "\n".join(out)


def cmd_remove(root: Path, crontab_file: Path | str | None = None) -> dict:
    """Drop this project's managed block only. Does not read or validate the
    node — removal must work even when the node is missing or malformed,
    which is exactly the state a broken edit can leave the graph in."""
    root = Path(root)
    repo_root = locations.repo_root(root)
    begin, end = block_markers(repo_root)
    current = read_crontab(crontab_file)
    before, removed, after = split_managed_block(current, begin, end)
    write_crontab(before + after, crontab_file)
    return {"root": root, "repo_root": repo_root, "removed_lines": removed}


def cmd_audit(root: Path, crontab_file: Path | str | None = None,
              unit_dir: Path | str | None = None) -> list[str]:
    """Read-only: every agi-owned thing this box runs that THIS node does not
    declare. Three sources: another project's `agi-crons` block in the
    crontab, drift inside our own managed block, and any `agi-*` systemd unit
    not named by the node's `services:` table (`--unit-dir` doubles as the
    listing seam, so no test touches the real user manager). Writes nothing;
    the caller decides the exit code."""
    root, cfg, repo_root, engine_root, node = _resolve(root)
    require_common_root(root, repo_root)
    begin, end = block_markers(repo_root)
    ours = project_hash(repo_root)
    current = read_crontab(crontab_file)
    _, managed, _ = split_managed_block(current, begin, end)
    found: list[str] = []
    for line in current:
        m = AGI_BLOCK_RE.match(line)
        if m and m.group(1) != ours:
            found.append(f"crontab: agi block from another project: {line}")
    if managed != render_managed_lines(root, repo_root, engine_root, node):
        found.append("crontab: this project's managed block drifts from the "
                     "node (run `crons.py apply`)")
    for name, job in node["jobs"].items():
        if job.get("box") and not job.get("why_box"):
            found.append(f"node: cadences.{name} gates on box {job['box']!r} "
                         f"with no `why_box` — a `box` gate is the exception "
                         f"and must say why")
    if unit_dir is None:
        unit_dir = Path.home() / ".config" / "systemd" / "user"
    if unit_dir is not None:
        ud = Path(unit_dir)
        declared = set(node["services"])
        for p in (sorted(ud.glob("*.service")) if ud.is_dir() else []):
            m = AGI_UNIT_RE.match(p.name)
            if m:
                if m.group(2) == ours[:8]:
                    if m.group(1) not in declared:
                        found.append(f"unit: {p.name} (service {m.group(1)!r} "
                                     f"is not in the node's services:)")
                # else: another project's own unit — not ours to judge, silent.
            else:
                # No agi unit shape at all (ordinary name, or a malformed
                # agi-* name): always undeclared by this node.
                found.append(f"unit: {p.name} (not declared by this node)")
    return found


# --- cli ---------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Derive the crontab from nodes/.geometry/crons.md (goal:g1.5).")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=None,
                        help="start resolving the project from here (default: cwd)")
    common.add_argument("--crontab-file", default=None,
                        help="read/write this file instead of the real crontab "
                             "(testing/dry-run; production omits this)")
    common.add_argument("--unit-dir", default=None,
                        help="reconcile systemd unit files (services table) "
                             "under this directory instead of the real user "
                             "manager (testing/dry-run; the live install is "
                             "the prime's step at merge-up)")

    sub = ap.add_subparsers(dest="cmd", required=True)
    ap_apply = sub.add_parser("apply", parents=[common],
                              help="reconcile the crontab against the node")
    ap_apply.add_argument("--dry-run", action="store_true",
                          help="render and report; write nothing")
    sub.add_parser("show", parents=[common],
                   help="print installed vs desired, and their diff")
    sub.add_parser("remove", parents=[common],
                   help="drop this project's managed block only")
    sub.add_parser("audit", parents=[common],
                   help="report agi cron lines/units the node does not declare "
                        "(read-only; exit 1 when anything is undeclared)")

    args = ap.parse_args(argv)

    start = args.root
    root = locations.find_project_root(start)
    if root is None:
        origin = start or "cwd"
        print(f"ERR: crons.py: no agi project found from {origin} — looked for "
              f"agi-tree.config.json walking up, then <dir>/*-tree/ below",
              file=sys.stderr)
        return 1

    try:
        if args.cmd == "apply":
            result = cmd_apply(root, args.crontab_file, dry_run=args.dry_run,
                               unit_dir=args.unit_dir)
            verb = "would install" if args.dry_run else "installed"
            if not result["crons_live"]:
                print(f"crons: crons_live is false — {verb} 0 line(s) "
                      f"(kill switch; {len(result['previous_managed_lines'])} "
                      f"removed)")
            elif result["changed"] or args.dry_run:
                print(f"crons: {verb} {len(result['managed_lines'])} line(s) "
                      f"for {result['repo_root']}:")
                for line in result["managed_lines"]:
                    print(f"  {line}")
            if not result["changed"]:
                print(f"crons: no-op — the crontab already matches the node "
                      f"({len(result['managed_lines'])} line(s))")
            for a in result.get("log_actions") or ():
                print(f"crons: log {a}")
            if result.get("unit_actions"):
                print(f"crons: units ({result['unit_dir']}):")
                for a in result["unit_actions"]:
                    print(f"  {a}")
        elif args.cmd == "show":
            print(cmd_show(root, args.crontab_file))
        elif args.cmd == "remove":
            result = cmd_remove(root, args.crontab_file)
            print(f"crons: removed {len(result['removed_lines'])} line(s) "
                  f"for {result['repo_root']}")
        elif args.cmd == "audit":
            found = cmd_audit(root, args.crontab_file, args.unit_dir)
            if found:
                print(f"crons: audit found {len(found)} undeclared item(s):")
                for item in found:
                    print(f"  {item}")
                return 1
            print("crons: audit clean — every agi cron line and unit this box "
                  "runs is declared by the node")
    except CronsError as exc:
        print(f"ERR: crons.py: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
