"""node_commit -- the by-exact-path commit of a node a runtime job just wrote (goal:g7.16.1.11.46.23, V8a step 3a).

Replaces the commit tail of the retired writer for its runtime callers (the board's metrics_cell, council_report,
failures --write-node, sensei apply_note, season cells). Council decision,
alive 23:28:02Z 10-25, 3/3: option (2) MINIMAL, KEEPING the already-dirty refusal.

  KEPT   a path ALREADY dirty against HEAD when the job starts is a hand edit: committing it would publish
         someone's bytes under the job's subject (the board commits in belam's tree, where belam hand-edits).
         The write is REFUSED BEFORE anything is written: `commit_paths: <path> already dirty: refused,
         nothing written`. The sampling is write.py's `_pre_dirty` as it was (ls-files + `git diff --quiet
         HEAD -- <p>`, one retry on rc >= 2, then FAIL CLOSED: an unknown state refuses the path).
  KEPT   a held suite lock (verification.suite_lock_holder) is waited for up to `hold_wait_s`, then refuses.
  NEW    `git add` + `git commit -- <paths>` by exact path (never -a, never a file a peer staged), a BOUNDED
         index.lock / ref-lock retry inside `values.core.suite_lock.write_commit_wait_s` (30 s when absent).
  LOUD   every refusal, and an exhausted retry, raises CommitRefused carrying ONE named line; a caller turns it
         into a non-zero exit with that line in its log. An hour is never skipped silently.
  DROPPED  the inflight markers / peer wait, and the `write.commit_message` template cell: the subject is the
         caller's, `<job>: <node> (<actor>)`.

THE BYTES are written by node_writer.update_node / replace_payload; this module only decides whether it is safe
to write them and then commits exactly them.
"""
from __future__ import annotations

import hashlib
import os
import random
import shlex
import subprocess
import sys
import time
from pathlib import Path

import node_writer

#: a refusal leaves the bytes either unwritten (already dirty) or written-but-uncommitted (lock, retry); a CLI
#: caller exits with this over the second kind (write.py's EXIT_UNCOMMITTED, same number).
EXIT_UNCOMMITTED = 3
NOTES_HEADING = "## Agent Notes"


class CommitRefused(RuntimeError):
    """The write or its commit was refused by name. `written` says whether bytes are on disk uncommitted."""

    def __init__(self, line: str, written: bool = False):
        super().__init__(line)
        self.line = line
        self.written = written


def _git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True)


def _commit_wait_s(root) -> float:
    """`values.core.suite_lock.write_commit_wait_s`, 30 s when absent or unreadable (an unreadable POLICY is
    refused by name in `_held`, so this fallback never lets a commit through under it)."""
    try:
        import verification  # noqa: PLC0415 -- the ONE lock-policy resolver
        v = float(verification.suite_lock_policy(root).get("write_commit_wait_s"))
        return v if v >= 0 else 30.0
    except (Exception, SystemExit):  # noqa: BLE001
        return 30.0


def pre_dirty(root, paths) -> set:
    """The paths ALREADY dirty against HEAD (write.py `_pre_dirty`, ported as it was minus the inflight
    markers). Untracked / absent = CLEAN. rc >= 2 from git = unknown: retried once, then FAIL CLOSED (the path
    is returned as dirty and the state is named on stderr)."""
    out: set = set()
    unknown: list = []
    for p in [os.path.abspath(str(p)) for p in paths if p]:
        dq = lambda: _git(root, "--no-optional-locks", "diff", "--quiet", "HEAD", "--", p).returncode  # noqa: E731
        rc = 0 if _git(root, "ls-files", "--error-unmatch", "--", p).returncode else dq()
        rc = dq() if rc > 1 else rc   # 0 clean, 1 dirty, >= 2 unknown: retry once, then FAIL CLOSED
        if rc:
            out.add(p)
        unknown += [rc] * (rc > 1)
    if unknown:
        print(f"note: git diff rc {unknown} sampling {', '.join(map(str, paths))}; state unknown, path refused",
              file=sys.stderr)
    return out


def wait_lock(root):
    """Wait for the suite lock up to `hold_wait_s` and return `(holder, wait)`: holder None = free (or released
    inside the bound), else the live pid still holding it past the bound. ONE bounded loop for every caller (the
    job's start check and the commit both use it). An UNREADABLE lock policy or holder RAISES (callers fail
    closed: a hold we cannot rule out is a hold; goal:g1.42 row 2)."""
    import verification  # noqa: PLC0415 -- the ONE live-holder read
    holder = verification.suite_lock_holder(Path(root))
    wait = verification.suite_lock_policy(root)["hold_wait_s"]
    end = time.monotonic() + wait
    while holder and time.monotonic() < end:
        time.sleep(min(max(end - time.monotonic(), 0), 0.25 * (0.5 + random.random())))
        holder = verification.suite_lock_holder(Path(root))
    return holder, wait


def _held(root, recover: str):
    """The suite-lock refusal line if the lock is STILL held after waiting `hold_wait_s`, else None. An
    UNREADABLE lock policy or holder FAILS CLOSED."""
    try:
        import verification  # noqa: PLC0415
        holder, wait = wait_lock(root)
        if not holder:
            return None
        return (f"commit_paths: commit refused: {Path(root) / 'sessions' / verification.suite_lock_name(root)} is held by "
                f"live pid {holder} after waiting {wait:g}s (values.core.suite_lock.hold_wait_s); the bytes are on disk "
                f"UNCOMMITTED; recover once released: {recover}")
    except (Exception, SystemExit) as exc:  # noqa: BLE001
        return (f"commit_paths: commit refused: the suite-lock state is unreadable ({type(exc).__name__}: {str(exc)[:100]}); "
                f"NOT committed (fail closed); fix values.core.suite_lock or release the lock, then recover: {recover}")


def _has_git_dir(root) -> bool:
    """A `.git` ENTRY in root or any ancestor: os.path.lexists, so a directory, the FILE a linked worktree carries
    (`gitdir: <main>/.git/worktrees/<n>`) and a (even dangling) link all count. Never is_dir / exists: a worktree whose
    gitdir was pruned or moved must read as 'a .git git cannot read' (refused), not 'not a git checkout' (a note)."""
    r = Path(root).resolve()
    return any(os.path.lexists(d / ".git") for d in [r, *r.parents])


def git_state(root, written: bool = True) -> str:
    """'ok' when git can read `root` as a work tree; 'none' when NO `.git` exists in root or any ancestor (a plain
    directory: nothing to commit, said aloud by the caller); raises CommitRefused when a `.git` IS present but git
    cannot read it (dubious ownership / safe.directory, a broken .git, git missing): never read as 'nothing to
    commit' -- the hourly job would write, commit nothing and exit 0 every hour."""
    got = _git(root, "rev-parse", "--is-inside-work-tree")
    if got.returncode == 0:
        return "ok"
    if not _has_git_dir(root):
        return "none"
    raise CommitRefused(f"commit_paths: git cannot read {root} (rc {got.returncode}: "
                        f"{(got.stderr or got.stdout).strip()[:200] or 'no message'}): refused, a checkout that "
                        f"cannot be read is not 'nothing to commit'", written=written)


def _sha(p) -> str:
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except OSError:
        return ""


def commit_paths(root, paths, msg: str, *, pre=frozenset(), expect=None) -> str:
    """Commit exactly `paths` under `msg`. Returns "" when committed, or a note line when a peer already
    committed these bytes (nothing to commit), or `node_commit: <root> is not a git checkout: written, not
    committed` when NO `.git` exists in root or any ancestor (never ""). Raises CommitRefused (written=True) on a held
    lock, an exhausted retry, a git failure, or a `.git` git cannot read (dubious ownership, a broken .git). `pre` is the already-dirty
    set sampled BEFORE the write: any path of it refuses here too (never launder a hand edit). `expect` maps a path
    to the sha256 of the bytes the job wrote: checked after any lock wait, right before `git add`, so a hand edit that
    lands DURING the wait (a path that was clean when we started) is refused too, never swept into the commit."""
    paths = [str(p if Path(p).is_absolute() else Path(root) / p) for p in paths if p]
    if not paths:
        return ""
    if git_state(root) == "none":
        return f"node_commit: {root} is not a git checkout: written, not committed"
    recover = (f"git -C {root} add -- {' '.join(paths)} && "
               f"git -C {root} commit -q -m {shlex.quote(msg)} -- {' '.join(paths)}")
    laundered = [p for p in paths if os.path.abspath(p) in pre]
    if laundered:
        raise CommitRefused(f"commit_paths: {' '.join(laundered)} already dirty: refused, nothing committed "
                            f"(a hand edit would ride along); recover once reviewed: {recover}", written=True)
    deadline = time.monotonic() + _commit_wait_s(root)
    tries = 0
    while True:
        tries += 1
        refused = _held(root, recover)   # a lock taken mid-retry waits / refuses, never commits under it
        if refused:
            _git(root, "reset", "-q", "--", *paths)
            raise CommitRefused(refused, written=True)
        moved = [p for p in paths if expect and os.path.abspath(p) in expect and _sha(p) != expect[os.path.abspath(p)]]
        if moved:
            raise CommitRefused(f"commit_paths: {' '.join(moved)} changed since this job wrote it (a hand edit during "
                                f"the wait?): refused, nothing committed, the bytes are left as they are; "
                                f"recover once reviewed: {recover}", written=True)
        add = _git(root, "add", "--", *paths)
        done = add if add.returncode else _git(root, "commit", "-q", "-m", msg, "--", *paths)
        if done.returncode == 0:
            return ""
        err = (done.stderr or "") + (done.stdout or "")
        busy = "index.lock" in err or "cannot lock ref" in err or ".lock': File exists" in err
        if not busy or time.monotonic() >= deadline:
            flags = [ln[:1] for ln in _git(root, "ls-files", "-v", "--", *paths).stdout.splitlines() if ln.strip()]
            at_head = (len(flags) == len(paths) and all(f == "H" for f in flags)
                       and not _git(root, "--no-optional-locks", "status", "--porcelain", "--", *paths).stdout.strip())
            if at_head:
                return "commit_paths: skipped: these bytes are already at HEAD (a peer committed them), nothing to commit"
            break
        time.sleep(min(2.0, 0.05 * 2 ** min(tries, 6)) * (0.5 + random.random()))
    reset = _git(root, "reset", "-q", "--", *paths)   # never left STAGED in a shared index
    state = "unstaged" if reset.returncode == 0 else f"STILL STAGED, reset failed rc {reset.returncode}: git reset -q -- {' '.join(paths)}"
    raise CommitRefused(f"commit_paths: commit failed after {tries} tr{'y' if tries == 1 else 'ies'} ({state}; the bytes are "
                        f"on disk UNCOMMITTED; recover: {recover}): {err.strip()[:300]}", written=True)


def provenance(root, actor: str = "") -> dict:
    """The `edited_by` stamp the retired writer put on every write: the named actor, else geometry_config.default_actor."""
    import geometry_config
    return {"edited_by": actor or geometry_config.default_actor(root)}


def coerce_value(value):
    """The retired writer's `set` coercion, kept for the callers that pass text: `"3"` -> 3, `"true"` -> True, `"null"` ->
    None, a JSON array / object string -> the parsed value, `"[a, b]"` -> a list, else the string. A non-string
    passes through unchanged."""
    import json
    if not isinstance(value, str):
        return value
    text = value.strip()
    low = text.lower()
    if low in {"true", "false"}:
        return low == "true"
    if low in {"none", "null"}:
        return None
    if text.startswith("[") and text.endswith("]"):
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass
        inner = text[1:-1].strip()
        return [coerce_value(p.strip()) for p in inner.split(",")] if inner else []
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass
    for conv in (int, float):
        try:
            return conv(text)
        except ValueError:
            pass
    return text


def append_note(body: str, text: str) -> str:
    """`note <text>` as the retired writer composed it: appended UNDER the one `## Agent Notes` heading (added when the
    body has none); text already present in the body is not appended twice."""
    text = (text or "").strip()
    if not text or text in body:
        return body
    if NOTES_HEADING in body:
        head, sep, tail = body.rpartition(NOTES_HEADING)
        return head + sep + tail.rstrip() + f"\n\n{text}\n"
    return body.rstrip() + f"\n\n{NOTES_HEADING}\n{text}\n"


def _payload_path(root, node_id: str):
    """(ref, location) of a node's payload from its OWN frontmatter, or None."""
    from graph_core.persistence import frontmatter as fm_reader
    path = node_writer.find_node_file(root, node_id)
    if path is None:
        return None
    fm = fm_reader.load_node_file(path, body=False).frontmatter
    ref = fm.get("payload_ref")
    if not isinstance(ref, str) or not ref.strip():
        return None
    loc = fm.get("location")
    return ref.strip(), (loc.strip() if isinstance(loc, str) and loc.strip() else None)


def land(root, node_id: str, subject: str, apply, *, payload: bool = False) -> node_writer.NodeWrite:
    """The one sequence every runtime caller runs: sample what is already dirty (the node, and its payload when
    `payload`), REFUSE before writing if any of it is, call `apply()` (which returns node_writer's result:
    update_node / replace_payload), then commit exactly the paths it wrote under `subject`.

    `root` is the graph (.agi) dir. Raises CommitRefused (a named line) on any refusal or a REJECTED write; the
    caller exits non-zero with `.line`. Returns the NodeWrite."""
    import locations
    root = Path(root)
    node_file = node_writer.find_node_file(root, node_id)
    if node_file is None:
        raise CommitRefused(f"commit_paths: no node file for {node_id}: refused, nothing written")
    git_state(root, written=False)   # a `.git` git cannot read refuses HERE, before anything is written
    watch = [node_file]
    if payload:
        ref = _payload_path(root, node_id)
        if ref is None:
            raise CommitRefused(f"commit_paths: {node_id} has no payload_ref: refused, nothing written")
        watch.append(locations.resolve_payload_path(root, ref[0], ref[1]))
    dirty = pre_dirty(root, watch)
    if dirty:
        raise CommitRefused(f"commit_paths: {' '.join(sorted(dirty))} already dirty: refused, nothing written")
    res = apply()
    if res is None or getattr(res, "status", None) == node_writer.REJECTED:
        raise CommitRefused(f"commit_paths: {node_id}: the write was rejected "
                            f"({getattr(res, 'reason', '') or 'no result'}): nothing written")
    paths = [p for p in (getattr(res, "path", None), getattr(res, "payload_changed", None) and getattr(res, "payload_path", None),
                         getattr(res, "moved_from", None)) if p]
    if payload and not any(os.path.abspath(str(p)) == os.path.abspath(str(watch[-1])) for p in paths):
        paths.append(watch[-1])
    expect = {os.path.abspath(str(p)): _sha(p) for p in paths}
    note = commit_paths(root, paths, subject, expect=expect)
    if note:
        print(note, file=sys.stderr)
    return res


def _main(argv=None) -> int:
    """`--help` prints what this module is. There is nothing to run from a shell: callers import `land`
    (this keeps the bin/ smoke lane, which runs every script with --help expecting output and rc 0, honest)."""
    import argparse
    ap = argparse.ArgumentParser(
        prog="node_commit.py",
        description=("The by-exact-path commit of a node a runtime job just wrote (goal:g7.16.1.11.46.23 V8a 3a): "
                     "import node_commit and call land(root, node_id, subject, apply). A path already dirty is "
                     "refused before anything is written; a held suite lock or an exhausted index.lock retry "
                     "raises CommitRefused with ONE named line. Nothing is run from this CLI."))
    ap.parse_args(argv)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(_main())
