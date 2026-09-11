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
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402

import yaml

# The four jobs this project runs today. Order here is the order every
# rendered block and every diff uses — fixed rather than dict/YAML-key order,
# which is what makes "running apply twice is byte-identical" true regardless
# of how the node happens to order its `cadences:` mapping.
KNOWN_JOBS = ("grid_sync", "branch_push", "publish_engine", "engine_push")

#: Relative to the project root `locations.find_project_root` resolves.
#: `rglob("*.md")` traverses dot-directories (confirmed against `level3.py`),
#: so `.geometry/` is an ordinary, reachable node directory, not a hideout.
CRONS_NODE_REL = Path("nodes") / ".geometry" / "crons.md"

MARKER_TAG = "agi-crons"


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
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise CronsError(f"{path}: unterminated frontmatter block (only one `---`)")
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise CronsError(f"{path}: malformed YAML frontmatter — {exc}") from exc
    if not isinstance(fm, dict):
        raise CronsError(f"{path}: frontmatter must be a YAML mapping")
    return fm


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

    unknown = sorted(set(cadences) - set(KNOWN_JOBS))
    if unknown:
        raise CronsError(
            f"{path}: cadences declares unknown job(s) {unknown} — known jobs "
            f"are {list(KNOWN_JOBS)}"
        )

    jobs: dict = {}
    for name in KNOWN_JOBS:
        job = cadences.get(name)
        if job is None:
            continue  # never declared: never rendered, distinct from enabled:false
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
        jobs[name] = {"enabled": enabled, "every_mins": every_mins, "schedule": schedule}

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


def _log_path(repo_root: Path) -> Path:
    # One log for every job in this project's block — matches grid.py's own
    # convention of one file per project rather than one per cadence.
    return Path.home() / "logs" / f"agi-crons-{Path(repo_root).name}-{project_hash(repo_root)[:8]}.log"


def render_managed_lines(root: Path, repo_root: Path, engine_root: Path, node: dict) -> list[str]:
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
    log = _log_path(repo_root)
    lines: list[str] = []

    if "grid_sync" in jobs and jobs["grid_sync"]["enabled"]:
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
            f"git -C {repo_root} push -q origin 'refs/grid/*:refs/grid/*' >> {log} 2>&1; "
            f"python3 {crons_py} apply --unit-dir {udir} >> {log} 2>&1"
        )
        lines.append(f"{sched} cd {root} && {cmd}")

    if "branch_push" in jobs and jobs["branch_push"]["enabled"]:
        _require_git_repo(repo_root, "branch_push")
        branch = resolve_branch(repo_root)
        sched = _schedule_expr(jobs["branch_push"])
        lines.append(
            f"{sched} cd {root} && git -C {repo_root} push -q origin {branch} >> {log} 2>&1"
        )

    if "publish_engine" in jobs and jobs["publish_engine"]["enabled"]:
        _require_dir(engine_root, "publish_engine")
        publisher = Path(engine_root) / "extensions" / "agi" / "bin" / "publish-engine.sh"
        sched = _schedule_expr(jobs["publish_engine"])
        lines.append(f"{sched} cd {root} && bash {publisher} >> {log} 2>&1")

    if "engine_push" in jobs and jobs["engine_push"]["enabled"]:
        _require_git_repo(engine_root, "engine_push")
        engine_branch = resolve_branch(engine_root)
        sched = _schedule_expr(jobs["engine_push"])
        lines.append(
            f"{sched} cd {root} && git -C {engine_root} push -q origin {engine_branch} >> {log} 2>&1"
        )

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


def _apply_systemctl(args: list[str], *, dry_run: bool) -> str:
    """Actually run `systemctl --user <args>` via PATH — a FAKE systemctl in
    tests (residue b: tests prove the exact argv and never touch the real
    user manager or ~/.config/systemd). The real user manager is only ever
    reached when a services table has landed and grid_sync self-reapplies
    with `--unit-dir`. Under `--dry-run` the intent is recorded and nothing
    runs. A failed systemctl becomes a visible action string, never an
    exception — a crontab apply must not die midway because one unit refused.
    """
    label = " ".join(["systemctl", "--user", *args])
    if dry_run:
        return f"{label} (dry-run)"
    try:
        res = subprocess.run(["systemctl", "--user", *args],
                             capture_output=True, text=True, timeout=60)
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
    for name, svc in node["services"].items():
        target = unit_filename(repo_root, name, ud)
        service_arg = target.name
        wanted = node["crons_live"] and svc["enabled"]
        if wanted:
            desired = "\n".join(render_unit_file(name, svc, repo_root)) + "\n"
            up_to_date = (target.is_file()
                          and target.read_text(encoding="utf-8") == desired)
            if up_to_date:
                actions.append(f"unit {target.name} up to date")
            elif dry_run:
                actions.append(f"write unit {target.name} (dry-run)")
            else:
                ud.mkdir(parents=True, exist_ok=True)
                target.write_text(desired, encoding="utf-8")
                actions.append(f"write unit {target.name}")
            # Make systemd SEE and START the unit. Idempotent in systemd, so
            # it also runs when the file was already current — a file written
            # by an earlier apply but never enabled converges on the next one.
            actions.append(_apply_systemctl(["daemon-reload"], dry_run=dry_run))
            actions.append(_apply_systemctl(["enable", "--now", service_arg],
                                            dry_run=dry_run))
        else:
            # crons_live false, or the service disabled: the kill switch
            # STOPS the unit through the real seam (disable --now), removes
            # the file, and reloads so the removal is seen by systemd.
            actions.append(_apply_systemctl(["disable", "--now", service_arg],
                                            dry_run=dry_run))
            if target.exists():
                if not dry_run:
                    target.unlink()
                    actions.append(f"remove unit {target.name}")
                else:
                    actions.append(f"remove unit {target.name} (dry-run)")
            else:
                actions.append(f"unit {target.name} absent")
            actions.append(_apply_systemctl(["daemon-reload"], dry_run=dry_run))
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

    return {
        "root": root, "repo_root": repo_root, "engine_root": engine_root,
        "crontab_lines": new_lines, "managed_lines": managed,
        "previous_managed_lines": existing, "changed": changed,
        "crons_live": node["crons_live"],
        "unit_actions": unit_actions, "unit_dir": unit_dir,
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
            else:
                print(f"crons: {verb} {len(result['managed_lines'])} line(s) "
                      f"for {result['repo_root']}:")
                for line in result["managed_lines"]:
                    print(f"  {line}")
            if not result["changed"]:
                print("crons: crontab already matched (no-op)")
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
    except CronsError as exc:
        print(f"ERR: crons.py: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
