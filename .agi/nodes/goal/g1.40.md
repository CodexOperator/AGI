---
id: goal:g1.40
mint_id: 0cfd445832be405db45b8c69b4685369
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G1.40
goal_kind: subgoal
origin: goal
scaffold_hash: a5ccca18f730375e
season: 2
seeds:
  - goal:g1
status: horizon
tags:
  - send
  - inbox
  - comms
  - engine-finding
title: "G1.40: send.py inbox appends are never lost to a concurrent read: the mark-read rewrite and the append share one lock, so a send that printed the inbox path is a send that arrives"
town: core
---
# goal:g1.40

## Why this exists
goal:g1 (the engine's own fixes): SM (10-02, to DG1, "an engine finding for a goal:g1 engine-findings row; not urgent, no hold") reported that `send.py` inbox sends can silently vanish. Evidence (SM): all-is-one sent its merge-up 8 notice via send.py at about 14:1xZ 10-02 and send.py printed the inbox path (= accepted); in `.agi/sessions/inbox/sanctuary-master.md` (UNTRACKED, 1,121 lines) the -7 notice sits at :1054 and -9 at :1114 with NO -8 line between; all-is-one counts this as the 3rd such case.
MEASURED BY ME (director-general-1, 10-02, scratch git root, the real `send.send` / `send.read` functions, `nudge=False`): the mechanism is an unlocked read-modify-write. `send()` appends with `open(inbox, "a")` and one `f.write(block)`; `read()` with `mark=True` does `text = inbox.open("r", newline="").read()` and later `inbox.write_text(content[:cut] + READ_MARKER + tail)` (send.py, the "Mark read" block of `read`): an append that lands between that read and that write is overwritten by the stale copy, with no error on either side. Harness: 6 writer processes x 150 appends (900) against ONE reader looping `read` until the writers finish, then one final read, counting distinct bodies printed: run 1 received 890 (10 lost) · run 2 received 892 (8 lost) · run 3 received 878 (22 lost); control, the same 6 writers with NO reader: 900 of 900 in the file. So loss needs a concurrent mark-read, and one appears in about 1-2.5 % of a heavy burst; on the real box the reader is a post's own `read` plus the mail_poll cron.
The harness (a scratch git root with an `.agi/` dir; pass the root, writers, appends each; the control is the same writers with the reader process left out):
```python
import sys, os, io, contextlib, re, multiprocessing as mp
from pathlib import Path
sys.path.insert(0, "extensions/agi/bin"); os.environ.pop("TMUX", None); os.environ.pop("TMUX_PANE", None)
import send
ROOT, P, M = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
def writer(k):
    with contextlib.redirect_stdout(io.StringIO()):
        for j in range(M):
            send.send(ROOT, "zz-c", f"w{k}-{j}", "zz-a", nudge=False)
def reader(q):
    got, done = [], ROOT / ".writers-done"
    while True:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            send.read(ROOT, "zz-c", None)
        got.append(buf.getvalue())
        if done.exists():
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                send.read(ROOT, "zz-c", None)
            got.append(buf.getvalue()); break
    q.put("".join(got))
if __name__ == "__main__":
    (ROOT / ".writers-done").unlink(missing_ok=True)
    q = mp.Queue(); rp = mp.Process(target=reader, args=(q,)); rp.start()
    ws = [mp.Process(target=writer, args=(k,)) for k in range(P)]
    [w.start() for w in ws]; [w.join() for w in ws]
    (ROOT / ".writers-done").write_text("x"); out = q.get(timeout=60); rp.join()
    want = {f"w{k}-{j}" for k in range(P) for j in range(M)}
    seen = set(re.findall(r"\bw\d+-\d+\b", out))
    print(f"sent={len(want)} received={len(seen & want)} lost={len(want - seen)}")
```

NOT measured by me: whether another writer of the inbox file (the nudge/sidecar helpers, an after_join typing path) can also drop a line; the first round re-runs the harness with those running.

## Target end-state
- A send that returned (printed the inbox path) is a send that is in the file or already read: no append is lost to a concurrent `read`, for any N writers and any reader loop.
- The append and the mark-read rewrite are serialized: both take ONE advisory lock on the inbox (a `<inbox>.lock` sidecar via fcntl.flock), the writer around `open(inbox, "a")` + write, the reader around its read + `write_text`; the read never rewrites from a copy older than the lock. (Recommendation; an atomic temp-file + rename for the rewrite alone does NOT fix it: the stale copy is still older than the append.)
- The harness above is a committed test, so the next change to `read` cannot reintroduce the loss.

## Invariants
- The wire format is unchanged: blocks, the `# read up to here` marker, the signature line, the CR/newline preservation the mark step already guards (mur-39 order (d)).
- A reader never blocks a sender for longer than one rewrite; a sender never blocks past a bounded wait (a lock that cannot be taken in the bound falls back to the append, never drops it).
- No read-side change moves the cursor past an unprinted line (hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line stays true).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_send_inbox_concurrency.py -q` passes: the harness (6 writers x 150 against a looping reader, final read) reports lost = 0 on 5 consecutive runs, and the writers-only control is 900 of 900. (RED today by measurement: 8-22 lost per run.)
2. Negative: `git grep -n -E 'inbox.*write_text' -- extensions/agi/bin/send.py` shows no inbox rewrite outside the lock.

## Out of scope
goal:g7.16.1.11.11 (AA1 boxes; belam [owner] 18:1xZ M1: mail WITHOUT send.py and without Python = a message is a git commit to the recipient's branch / nearest remote head, a box cron cascades it to the branch then the worktree; a ref update is atomic and no shared file is rewritten, so it ENDS this race by design -- this leaf stays the fix for the inbox form every post uses until then; belam: re-send once if unanswered in 15 min) · goal:g7.32.6 (the send redesign: it replaces the inbox form; this is the fix to the form every post still uses until then) · the pane nudge path and its sidecars · the tracked-vs-untracked state of the inbox files (they are runtime, untracked by design).

## Agent Notes
Assigned to **director-general-1**.
