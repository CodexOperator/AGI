#!/usr/bin/env python3
"""board_job.py -- the hourly board line's commit, made G by the seat's own uid (goal:g7.16.1.11.42, option E).

The board job (metrics_cell.py: one cell of the town node) used to run as the human uid, which has no
signing key, so every commit it made on the trunk was N. Option E (belam 14:5xZ 10-11, council 3/3 15:07Z,
conditions C1-C6) moves the commit to the Prime's OWN uid, the hand agi-at and agi-turn already sign with,
and leaves the human uid one step that makes NO commit:

  board_job.py commit --main MAIN --post belam --job NAME -- <writer ... @WROOT@ ...>     (uid agi-belam)
      1. work = a job-owned shared clone (never ~/t, C5); the base is posts/<post> (or MAIN when MAIN is
         ahead: a pure ref move, no commit; or a signed `board: take MAIN` merge when they diverged and every
         commit on posts/<post> is the job's own);
         (.42.2: the Prime's landable NODE commits no longer block this step; a take-MAIN merge over them runs
         WITHOUT -X theirs, and a conflict names the Prime sha + path and waits: a Prime hunk is never dropped)
      2. the writer runs in the clone at @WROOT@ (= <work>/.agi) and makes ONE commit; the job re-signs it with
         a `Board-job:` trailer (C3: the subject stays exact, the trailer names the job);
      3. C2: the commit must verify G (`git log -1 --format=%G?`), else NOTHING is published, one line, rc 3;
      4. publish = a push to MAIN's posts/<post> with --force-with-lease=<base> (the CAS: new^1 == the current
         tip; a miss is rc 4 and the next hour retries, never a commit).
  board_job.py land --main MAIN --post belam                                              (uid belam)
      C6: `git merge --ff-only posts/<post>` into MAIN ONLY when every commit in MAIN..posts/<post> is the
      job's own (exact subject + a Board-job trailer + the seat's committer); otherwise no ff, ONE line to
      the notice file, rc 3 (posts/<post> is also the Prime's staging lane, so an unconditional ff from a
      cron would land unreviewed work: the `branch_push` class). The ff makes no commit (C5).
      goal:g7.16.1.11.42.2 (council 3/3 10-15): a commit is also landable when it is the Prime's own NODE
      commit (prime_node: G by belam@agi, only under .agi/nodes/ outside .geometry/ and town/, mode 100644,
      no delete) or a clean sync merge (its tree == merge-tree of its two checked parents). The first commit
      that is neither is named in the notice with the rule it failed, and nothing lands.

The committer is `<post> <post>@agi`: git verifies an ssh signature against the committer email, and
`belam@agi` is the ring principal of the Prime's key. Exit codes: 0 done / nothing to do, 2 usage or
refused setup, 3 refused by a rule (the line says which), 4 a raced CAS, 5 no posts/<post>.

`land` verifies every commit's signature and principal ITSELF against --signers (the ring file): uid belam's git
config names no signers file, and any uid in group agi can move posts/<post>, so the commit step's C2 check is
not something land may trust. Notices: the COMMIT job (uid of the seat) is the ONE notice carrier, writing to the
seat's own ~/.notice; land's lines go to uid belam's own ~/.notice, which no session reads, so they are
log-only in effect (the cron log carries them too).
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

SIGNERS = "/var/lib/agi/allowed_signers"   # the ring: uid belam's own git config names no signers file
TRAILER = "Board-job:"
#: the machinery's exact subject: `board: town:<slug> (<post>)` since goal:g7.16.1.11.46.23 V8a 3a (metrics_cell writes
#: through node_commit); `write.py: town:...` stays accepted for the commits made by the retired writer that are
#: still unlanded on posts/<post> at the cutover (drop the alternative one lap after the first board land).
SUBJECT_RE = re.compile(r"^(?:board|write\.py): town:[a-z0-9-]+ \([a-z0-9-]+\)$")
TAKE_PREFIX = "board: take MAIN"
WROOT = "@WROOT@"


def _clean(env=None) -> dict:
    """The job owns its git env: an inherited GIT_DIR / GIT_WORK_TREE / GIT_INDEX_FILE would point
    EVERY git call below (reads of MAIN included) at another repo."""
    e = dict(os.environ if env is None else env)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        e.pop(k, None)
    return e


def _git(repo, *args, env=None, input=None):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          env=_clean(env), input=input)


def _rev(repo, rev):
    got = _git(repo, "rev-parse", "-q", "--verify", rev)
    return got.stdout.strip() if got.returncode == 0 else None


def _is_ancestor(repo, a, b) -> bool:
    return _git(repo, "merge-base", "--is-ancestor", a, b).returncode == 0


def _identity_env(post: str) -> dict:
    env = _clean()
    env.update(GIT_AUTHOR_NAME=post, GIT_COMMITTER_NAME=post,
               GIT_AUTHOR_EMAIL=f"{post}@agi", GIT_COMMITTER_EMAIL=f"{post}@agi")
    return env


def _sig(repo, sha: str, signers: str) -> tuple[str, str]:
    """(%G?, %GS) of `sha`, verified against `signers` (-c gpg.ssh.allowedSignersFile): the verdict never
    depends on the invoking uid's git config. ('?', '') when git cannot say."""
    got = _git(repo, "-c", f"gpg.ssh.allowedSignersFile={signers}", "log", "-1", "--format=%G?%x00%GS", sha)
    if got.returncode:
        return "?", ""
    g, _, who = got.stdout.rstrip("\n").partition("\x00")
    return g or "?", who


def is_own(repo, sha: str, post: str, signers: str = SIGNERS) -> bool:
    """True when `sha` is the board job's own commit: SIGNED (%G? == G) by the seat's principal
    (%GS == <post>@agi, not just any key on the ring), the exact subject (or the take-MAIN merge), a
    `Board-job:` trailer, and the seat's committer email. Council 18:06Z condition (b): land runs as the
    human uid, which can neither be told what C2 checked nor trust who moved posts/<post> (any uid in
    group agi can), so it checks the signature itself. The Prime's hand commits carry the same committer,
    so the subject + trailer are what tell the machinery from the hand."""
    got = _git(repo, "log", "-1", "--format=%ce%x00%s%x00%b", sha)
    if got.returncode:
        return False
    ce, subject, body = (got.stdout.rstrip("\n").split("\x00", 2) + ["", ""])[:3]
    if ce != f"{post}@agi":
        return False
    g, who = _sig(repo, sha, signers)
    if g != "G" or who != f"{post}@agi":
        return False
    if not (SUBJECT_RE.match(subject) or subject.startswith(TAKE_PREFIX)):
        return False
    return any(line.startswith(TRAILER) for line in body.splitlines())


def not_own(repo, base: str, tip: str, post: str, signers: str = SIGNERS) -> list[str]:
    """Commits in base..tip that are NOT the job's own (oldest first)."""
    out = _git(repo, "rev-list", "--reverse", f"{base}..{tip}")
    return [c for c in out.stdout.split() if not is_own(repo, c, post, signers)]


NODES, NOT_UNDER = ".agi/nodes/", (".agi/nodes/.geometry/", ".agi/nodes/town/")


def _committed_by_seat(repo, sha: str, post: str, signers: str) -> str:
    """"" when `sha` is committed by <post>@agi AND signed G by that principal (verified against `signers`
    here, never by the invoking uid's git config); else the reason, for the notice."""
    ce = _git(repo, "log", "-1", "--format=%ce", sha).stdout.strip()
    g, who = _sig(repo, sha, signers)
    if ce != f"{post}@agi" or g != "G" or who != f"{post}@agi":
        return f"(a) not signed G by {post}@agi (committer {ce or '?'}, %G?={g}, signer {who or '-'})"
    return ""


def _raw_diff(repo, sha: str) -> list[tuple[str, str, list[str]]]:
    """[(newmode, status, [path, ...])] of `git diff-tree -r -M` for `sha`: both paths of a rename."""
    got = _git(repo, "diff-tree", "-r", "-M", "--root", "--no-commit-id", "--raw", "-z", sha)
    f = got.stdout.split("\0")
    out, i = [], 0
    while i < len(f) and f[i].startswith(":"):
        meta = f[i][1:].split()
        status = meta[4] if len(meta) > 4 else "?"
        n = 2 if status[:1] in "RC" else 1
        out.append((meta[1] if len(meta) > 1 else "?", status, f[i + 1:i + 1 + n]))
        i += 1 + n
    return out


def prime_why(repo, sha: str, post: str, signers: str = SIGNERS) -> str:
    """"" when `sha` (a non-merge) is the Prime's own NODE commit; else the rule it failed, with the path.
    (a) the seat's committer + a G signature by its principal; (b) every path under .agi/nodes/, not under
    .geometry/ (engine pieces become ~/bin, crons.md the crontab, posts.md drives agi-boot) or town/ (the
    town_mirror timer reads them); (c) every new blob 100644 (no symlink, no exec bit); (e) no delete under
    .agi/nodes/; a rename into deprecated/ is the retire (a git rename, not a D status)."""
    why = _committed_by_seat(repo, sha, post, signers)
    if why:
        return why
    rows = _raw_diff(repo, sha)
    if not rows:
        return "(b) no readable diff"
    for mode, status, paths in rows:
        for path in paths:
            if not path.startswith(NODES) or path.startswith(NOT_UNDER):
                return f"(b) path {path}"
        if status[:1] != "D" and mode != "100644":
            return f"(c) path {paths[-1]} mode {mode}"
        if status[:1] == "D":   # a rename (R) keeps the node, in deprecated/ or elsewhere under nodes/: not a delete
            return f"(e) path {paths[0]} deleted"
    return ""


def land_why(repo, sha: str, post: str, signers: str, main_head: str, seen: dict | None = None) -> str:
    """"" when `sha` may land (the job's own commit, the Prime's node commit, or a clean sync merge); else
    the failed rule. A merge passes iff (a) holds, p2 is an ancestor of MAIN, p1 is in MAIN or lands itself,
    and its tree is exactly `git merge-tree --write-tree p1 p2` (no hand resolution): (b) and (e) are
    skipped for it, its content being exactly its two checked parents."""
    seen = {} if seen is None else seen
    if sha in seen:
        return seen[sha]
    if is_own(repo, sha, post, signers):
        seen[sha] = ""
        return ""
    parents = _git(repo, "log", "-1", "--format=%P", sha).stdout.split()
    if len(parents) < 2:
        seen[sha] = prime_why(repo, sha, post, signers)
        return seen[sha]
    why = _committed_by_seat(repo, sha, post, signers)
    if not why and len(parents) != 2:
        why = f"(m) {len(parents)} parents"
    if not why:
        p1, p2 = parents
        if not _is_ancestor(repo, p2, main_head):
            why = f"(m) parent 2 {p2[:7]} is not in MAIN"
        elif not _is_ancestor(repo, p1, main_head) and land_why(repo, p1, post, signers, main_head, seen):
            why = f"(m) parent 1 {p1[:7]} is not landable"
        else:
            mt = _git(repo, "merge-tree", "--write-tree", p1, p2)
            if mt.returncode or mt.stdout.split("\n", 1)[0] != _rev(repo, f"{sha}^{{tree}}"):
                why = "(m) the tree is not the clean merge of its parents (a hand resolution)"
    seen[sha] = why
    return why


def not_land_ok(repo, base: str, tip: str, post: str, signers: str = SIGNERS,
                main_head: str | None = None) -> list[tuple[str, str]]:
    """[(sha, failed rule)] for every commit in base..tip that may NOT land (oldest first). `main_head` is MAIN's
    head when `base` is not it (the diverged range starts at the merge-base)."""
    seen: dict = {}
    head = main_head or _rev(repo, base) or base
    out = _git(repo, "rev-list", "--reverse", f"{base}..{tip}")
    bad = []
    for c in out.stdout.split():
        why = land_why(repo, c, post, signers, head, seen)
        if why:
            bad.append((c, why))
    return bad



def _now() -> str:
    """The UTC stamp every log line of this job carries (the log had none, so a run could not be placed against a ref move; goal:g7.16.1.11.42)."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _say(line: str, err: bool = True) -> None:
    """ONE line of the job's log: `<UTC stamp> <line>`. Every print of this file goes through it."""
    print(f"{_now()} {line}", file=sys.stderr if err else sys.stdout)


def _sh(rev) -> str:
    return (rev or "?")[:12]


def _notice(path: Path | None, line: str) -> None:
    _say(line)
    if path is not None:
        try:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError as exc:
            _say(f"[board] could not write the notice file {path}: {exc}")


def _staged_line(post: str, n: int, repo=None, first: str = "", signers: str = SIGNERS) -> str:
    """The one notice line; with `first` it names the first foreign commit and its %G? (an unsigned or
    forged commit reads `%G?=N`, the Prime's hand work `%G?=G`)."""
    named = f" (first {first[:7]}, %G?={_sig(repo, first, signers)[0]})" if first and repo else ""
    return f"[board] posts/{post} carries {n} commits not the job's{named}: no ff, the board line waits"


def _main_head(main: Path):
    return _rev(main, "HEAD")


def cmd_land(args) -> int:
    main, post = Path(args.main), args.post
    ref = f"refs/heads/posts/{post}"
    tip, head = _rev(main, ref), _main_head(main)
    if not tip or not head:
        _say(f"[no-branch] posts/{post} or MAIN's HEAD is unreadable: nothing landed")
        return 5
    if tip == head or _is_ancestor(main, tip, head):
        return 0   # nothing to land: MAIN already has everything on the branch
    if not _is_ancestor(main, head, tip):
        _notice(args.notice, f"[board] MAIN and posts/{post} have diverged: no ff, the board line waits")
        return 3
    refused = not_land_ok(main, head, tip, post, args.signers)
    if refused:
        _notice(args.notice, f"[board] {refused[0][0][:7]} refused: {refused[0][1]}")
        return 3
    try:   # the suite lock holds MAIN's working tree still while a verification suite runs
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import verification  # noqa: PLC0415
        holder = verification.suite_lock_holder(main / ".agi")
    except Exception:  # noqa: BLE001 -- no lock reading: the ff itself refuses a dirty tree
        holder = None
    if holder:
        _say(f"skip: the suite lock is held by live pid {holder}; posts/{post} not landed")
        return 0
    done = _git(main, "merge", "--ff-only", "-q", ref)
    if done.returncode or _main_head(main) != tip:
        _say(f"[board] ff refused: {(done.stderr or done.stdout).strip()[:160]}")
        return 3
    _say(f"board: MAIN {head[:7]} -> {tip[:7]} (ff, no commit)", err=False)
    return 0


def _work_ok(work: Path) -> bool:
    """C5: the job's clone is never the Prime's live tree."""
    home_t = Path(os.path.expanduser("~")) / "t"
    w = work.resolve()
    return not (w == home_t.resolve() or home_t.resolve() in w.parents)


def _ensure_clone(main: Path, work: Path, env) -> bool:
    if (work / ".git").exists():
        return True
    work.parent.mkdir(parents=True, exist_ok=True)
    got = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(main), str(work)],
                         capture_output=True, text=True, env=env)
    return got.returncode == 0


def cmd_commit(args) -> int:
    main, post, work = Path(args.main), args.post, Path(args.work).expanduser()
    cmd = list(args.writer)
    if cmd[:1] == ["--"]:
        cmd = cmd[1:]
    if not cmd:
        _say("ERR: board_job.py commit: no writer command after --")
        return 2
    if not _work_ok(work):
        _say(f"[board] {work} is the Prime's own tree (~/t): the job never works there")
        return 2
    ref = f"refs/heads/posts/{post}"
    tip, head = _rev(main, ref), _main_head(main)
    if not tip or not head:
        _say(f"[no-branch] posts/{post} or MAIN's HEAD is unreadable: nothing committed")
        return 5
    env = _identity_env(post)
    # the base: posts/<post>'s tip, or MAIN when MAIN is ahead (a pure ref move: no commit)
    if tip != head and _is_ancestor(main, tip, head):
        if _git(main, "update-ref", ref, head, tip).returncode:
            _say(f"[raced] posts/{post} moved while the job took MAIN: old {_sh(tip)} -> seen {_sh(_rev(main, ref))}")
            return 4
        tip = head
    take, hand = False, []
    if tip != head:
        if _is_ancestor(main, head, tip):   # ahead: the job commits on top of work :28 lands whole (.42.2)
            refused = not_land_ok(main, head, tip, post, args.signers)
        else:   # diverged: only a branch that may land takes MAIN (a signed merge)
            mb = _git(main, "merge-base", head, tip).stdout.strip()
            refused = not_land_ok(main, mb, tip, post, args.signers, head) if mb else [(tip, "(m) no merge-base")]
            take = not refused
            hand = [c for c in _git(main, "rev-list", "--reverse", f"{mb}..{tip}").stdout.split()
                    if not is_own(main, c, post, args.signers)] if take else []
        if refused:
            _notice(args.notice, f"[board] {refused[0][0][:7]} refused: {refused[0][1]}")
            return 3
    if not _ensure_clone(main, work, env):
        _say(f"[board] could not make the job's clone at {work}")
        return 2
    for c in (["reset", "-q", "--hard"], ["clean", "-fdq"]):
        _git(work, *c, env=env)
    if _git(work, "checkout", "-q", "--detach", tip, env=env).returncode:
        _say(f"[board] could not check out {tip[:7]} in {work}")
        return 2
    base = tip
    if take:
        # -X theirs = MAIN's side of a CONTENT conflict (MAIN edited the same node between :23 and :28, e.g.
        # its edited_by stamp): the writer rewrites the cell right after, so nothing of the job's is lost.
        # Anything -X cannot settle (a modify/delete) is a REFUSAL that goes to the notice file too: a stall
        # that only the job log knew would leave the board line off with nobody told.
        # .42.2 (council 3/3 10-15): with the Prime's HAND node edits in the range, -X theirs would DROP a
        # conflicting Prime hunk, rc 0, no notice, inside a G merge nothing re-checks. A mixed range merges
        # WITHOUT -X: a conflict aborts (posts/<post> unchanged) and the notice names the Prime sha + the path.
        opts = [] if hand else ["-X", "theirs"]
        merged = _git(work, "merge", "-q", "--no-ff", *opts, "-m", f"{TAKE_PREFIX} {head[:7]}", "-m",
                      f"{TRAILER} {args.job}", head, env=env)
        if merged.returncode and hand:
            paths = _git(work, "diff", "--name-only", "--diff-filter=U", env=env).stdout.split()
            _git(work, "merge", "--abort", env=env)
            # R1 (council 3/3 03:21Z 10-16): the Prime is blamed only for a path one of ITS commits touched; the probe is
            # `-m --first-parent` because a plain diff-tree prints NOTHING for a merge (R1b, council 3/3 10:53Z 10-21): a
            # merge is blamed for what it changed vs its first parent (over-blaming is a notice = fail closed)
            hit = [(c, pa) for c in reversed(hand) for pa in paths
                   if _git(main, "diff-tree", "-r", "-m", "--first-parent", "--root", "--no-commit-id", "--name-only", c, "--", pa).stdout.strip()]
            if hit:   # the newest Prime commit that touches a conflicting path, and that path
                _notice(args.notice, f"[board] take MAIN: the Prime's {hit[0][0][:7]} conflicts with MAIN at {hit[0][1]}: "
                                     f"resolve it by hand, the board line waits")
                return 3
            # only the job's own hunks conflict (its cell): -X theirs settles ONLY conflicting hunks, so no Prime line is lost
            merged = _git(work, "merge", "-q", "--no-ff", "-X", "theirs", "-m", f"{TAKE_PREFIX} {head[:7]}", "-m",
                          f"{TRAILER} {args.job}", head, env=env)
        if merged.returncode:
            _git(work, "merge", "--abort", env=env)
            why = ((merged.stdout or "") + (merged.stderr or "")).strip().splitlines()
            _notice(args.notice, f"[board] take MAIN did not merge clean ({(why or ['?'])[0][:100]}): "
                                 f"the board line waits")
            return 3
        base = _rev(work, "HEAD")
        # the merge descends from the old tip (its first parent): publish it by ITS OWN CAS first, so
        # the board commit's parent is the tip posts/<post> really has
        sig = _git(work, "log", "-1", "--format=%G?", base, env=env).stdout.strip()
        if sig != "G":
            _say(f"[board] the take-MAIN merge {base[:7]} is not G (%G?={sig or '?'}): not published")
            return 3
        pushed = _git(work, "push", "-q", f"--force-with-lease={ref}:{tip}", str(main), f"{base}:{ref}", env=env)
        if pushed.returncode:
            _say(f"[raced] the take-MAIN push lost the CAS: old {_sh(tip)} -> seen {_sh(_rev(main, ref))}: {(pushed.stderr or '').strip()[-120:]}")
            return 4
    run = [c.replace(WROOT, str(work / ".agi")) for c in cmd]
    done = subprocess.run(run, cwd=str(work), env=env, capture_output=True, text=True)
    for line in done.stdout.splitlines():   # the writer's own lines carry the stamp too: the log is ONE timeline
        _say(line, err=False)
    for line in done.stderr.splitlines():
        _say(line)
    if done.returncode:
        return done.returncode
    new = _rev(work, "HEAD")
    if new == base:
        return 0   # the writer skipped (a held lock, a dirty node): nothing to publish
    if _rev(work, f"{new}^") != base or _git(work, "rev-list", "--count", f"{base}..{new}").stdout.strip() != "1":
        _say(f"[board] the writer made more than ONE commit on {base[:7]}: nothing published")
        return 3
    msg = _git(work, "log", "-1", "--format=%s", new).stdout.strip()
    amended = _git(work, "commit", "-q", "--amend", "-m", msg, "-m", f"{TRAILER} {args.job}", env=env)
    if amended.returncode:
        _say(f"[board] could not sign the commit: {(amended.stderr or amended.stdout).strip()[:160]}")
        return 3
    new = _rev(work, "HEAD")
    sig = _git(work, "log", "-1", "--format=%G?", new, env=env).stdout.strip()
    if sig != "G":   # C2: an N is never published
        _say(f"[board] the commit {new[:7]} is not G (%G?={sig or '?'}): not published, the node is unchanged")
        return 3
    if _rev(work, f"{new}^") != _rev(main, ref):   # new^1 must be the CURRENT tip
        _say(f"[raced] posts/{post} moved under the job: next hour (old {_sh(base)} -> seen {_sh(_rev(main, ref))})")
        return 4
    pushed = _git(work, "push", "-q", f"--force-with-lease={ref}:{base}", str(main), f"{new}:{ref}", env=env)
    if pushed.returncode:
        _say(f"[raced] the push to posts/{post} lost the CAS: old {_sh(base)} -> seen {_sh(_rev(main, ref))}: {(pushed.stderr or '').strip()[-120:]}")
        return 4
    _say(f"board: posts/{post} {base[:7]} -> {new[:7]} (G, {args.job})", err=False)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--main", required=True, help="the trunk's working copy (MAIN)")
    common.add_argument("--post", default="belam", help="the seat whose branch carries the board commit")
    common.add_argument("--signers", default=SIGNERS,
                        help="the allowed-signers ring land/commit verify the board commits against")
    common.add_argument("--notice", type=Path, default=Path(os.path.expanduser("~/.notice")),
                        help="the one-line notice file (default ~/.notice)")
    c = sub.add_parser("commit", parents=[common], help="make the signed board commit on posts/<post> (uid of the seat)")
    c.add_argument("--job", required=True, help="the job's name, written as the Board-job trailer")
    c.add_argument("--work", default="~/board-work", help="the job-owned clone (never ~/t)")
    c.add_argument("writer", nargs=argparse.REMAINDER, help="-- <writer command>; @WROOT@ = the clone's .agi")
    sub.add_parser("land", parents=[common], help="ff MAIN to posts/<post> when every commit is the job's own")
    args = ap.parse_args(argv)
    return cmd_commit(args) if args.verb == "commit" else cmd_land(args)


if __name__ == "__main__":
    sys.exit(main())
