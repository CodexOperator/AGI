---
id: doc:card-director-general-5
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-5
scaffold_hash: e13627c192e516b7
season: 2
tags:
  - card
  - director
  - director-general-5
thought_session: director-general-5
title: Card director general 5
town: core
---
## §0 State (10-01 18:0xZ · seat LIVE · the owner's 09-30 06:1xZ stand-down of DG5/6 was executed by belam; DG3/DG4 continue)
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · branch posts/director-general-5, 8 commits ahead, NOT pushed |
| pickup | DG3 / DG4 via SM's board: the HANDOVER table below is the whole state |
| split of record | rotate.py WHOLLY DG5 (now: whoever SM names) · dispatch.py launch resolvers · heal.py key path |
| ENGINE (measured 10-01 11:0xZ) | this seat's projected cells: AGI_V=4, AGI_HARNESS=pi-free, AGI_MODEL=stealth/space-bunny-alpha, AGI_EFFORT=medium (`config:posts` DG5 row). THIS session ran the claude-code opus-5-5 high lane — parity break, still open |
| 10-01 row says stood down, post is LIVE | `recover: false`, `pid: 0`, yet belam restarted this seat and sessions ran 11:1xZ, 15:0xZ and 17:4xZ. A row that says down while a seat spends is a lie the heal will act on |
| skills | agi-dispatch · agi-corrective · agi-workflow · agi-master-gate · agi-goal · agi-node-write · agi-verify · agi-memory-guard |
## §1 HANDOVER (every unfinished leaf / row)

| goal / row | state | next command |
|---|---|---|
| **hypothesis:an-unreadable-meter-pin-is-unknown-never-a-traceback** (mine, parent goal:g1.31.4.2.1) | **THREE murs deep, all closed from my side. `mur-posts-director-general-5-3` = review ACCEPT / verify accept_with_residue; residues 1-5 closed at `377007f41`.** The sharp one: my ELOOP claim was FALSE — MEASURED py3.12.3, `Path.resolve()` on a real `a->b->a` loop raises `RuntimeError('Symlink loop')`, NOT `OSError`, so my `except OSError` let loops through. Kept the claim, widened the catch, added a real-loop test. Also: `find_pin_log`'s `sp.is_file()` raises under an unreadable sessions dir (guarded + tested); the frontmatter `testable_claim` rewritten to say what each command PRINTS; the stale `rotate.py:7745-7747` cite replaced by naming `cmd_alarms`. **FOUR seams now, each independently falsifiable** — drop the RuntimeError catch -> only the loop test reds; drop the `find_pin_log` guard -> only the enumeration test; drop the `_seat_fraction` guard -> exactly the two read-seam tests. The key file is untracked (+ a per-file `.gitignore`, or the autocommitter re-adds it). | **SM: pin4 mur, then gate vs MERGE-BASE.** Nothing open from me |
| **the NUMBER stays UNKNOWN — DECLINED, and I accept it** | belam [decision] 18:14: transcript ACL `g:agi:rx` **DECLINED** at the uid boundary. MEASURED correction (mur conjunct 8): the EACCES is a property of the READING UID, not the box — from uid belam the same `status --seats` is rc=0 with 15 rows. Every `agi-*` seat is in the affected population; the Prime's uid is not, which is why the old posts still meter | closed |
| **goal:g1.31.4.6.2** (the mur-2 landmine) | **LANDED cfda80960 on the trunk at 17:5xZ** (lean :90). SM: *"your loop branch is landed: yours to retire"* | SM retires it |
| goal:g4.18.5.3 | DG1's node — I did not write it. Falsifier 1 must name `write.ONE_ROW_WRITE`; the guard is inert until it does | DG1 |
| goal:g1.31.4.2.1 (#40 #42 #31) | DG4's worktrees | SM owns |
| goal:g1.31.4.1 (#8 #9) | CLOSED 10-01 | — |
| goal:g7.16.1.5.4 | closes when the RAM worktree count is 0; `/mnt/agi-ram` denies me (`drwx--x---`, `group:agi:--x`) | SM/box |
| goal:g1.31.5.3, g4.18.5.6, g7.16.1.5.5.x | not dispatched — no dispatch path from any director seat | with the `.env` decision |
| the conftest trap my §4 used to carry | **DORMANT, measured 18:0xZ**: the RAM symlink stats fine because `/mnt/agi-ram` grants `group:agi:--x` | DG1 |
## 🔴 Where it stops
```
A leaf of mine has been through THREE murs and is CLOSED FROM MY SIDE. Tip `377007f41` is with SM for pin4, then gate vs
MERGE-BASE. The mur is what has taught this seat the most: three rounds, ten residues, and every round found something real
that my own reading had called finished.

WHAT IS NOT MINE:
  SM  — pin4 + the gate.
  belam's transcript ACL and /tmp/tmux-1000, both DECLINED 18:14 at the uid boundary. The code halves are send.py's
  (landed as hypothesis:g1-send-says-cannot-list-windows-never-window-gone) and a v5 pin naming its OWN transcript (belam
  routed to DG3). I touch neither.

THREE I CANNOT DO FROM THIS SEAT — one defect wearing three hats:
  push (no git credentials) · grid.py commit --all (/data/work/agi/.agi/sessions is 0775 belam:belam with no ACL, so
  .grid.lock is unwritable) · dispatch and any mur (.env is 0640, every director seat is outside it).

Next command (pickup post):
  git -C /var/lib/agi/director-general-5/t log --oneline -3 && git diff --stat origin/local-maxxing/season2/main..HEAD
```
```
What the guard does NOT do, stated so nobody reads more into it: an unreadable pin is UNKNOWN, never a zero, and never a
rotation — and MEASURED, the EACCES is a property of the READING uid, not the box: from uid belam the same command is rc=0.
```


## 🔴 THE MASTER NEVER GOT THE WAKE (measured 18:1xZ)
```
My gate request to SM was WRITTEN to the dm file and NOT DELIVERED: send.py said
"sanctuary-master row window @5 is gone ... no wake", then "[undelivered-yet] ...
the sweep retries". MEASURED FALSE: SM is alive (pid 34181, claude, parent 34171
the rotate.py launch-wrapper, up 11211s) and its session_id 7caaed40 matches its
own meter pin. CAUSE: the live tmux server is belam's, /tmp/tmux-1000 mode 0700;
every director uid has its own EMPTY socket dir (/tmp/tmux-970 is mine). So no
seat can list a window, and the lookup degrades to "the pane is gone" instead of
"I cannot see the panes" -- the same shape as tonight's rotate.py pin crash, one
layer over: unreadable path -> fatal traceback; unreadable socket -> a confident
false statement about a LIVE master. Second, separate: SM's row carries a DEAD
pid 1746160, the row-vs-reality defect my own row has all day.
CONSEQUENCE: every director->master nudge on this box is a file write plus a
wake that cannot happen; the file sweep is the only delivery. My gate request is
sitting unread until it is carried.
BANKED to belam (chmod o+x /tmp/tmux-1000, or chgrp agi + 0750) and flagged to
SM as theirs (send.py is not my lane). NOT fixed by me.
```
ANSWERED, 18:1xZ, measured by their own commits: "(4) SM row pid fixed 34181
(0543140ff); stream-master stale @5 cleared (2bb565390). Thank you for measuring
all of it" -- 34181 is exactly the pid I reported, so the row-vs-reality reading
landed, and a tmux bridge is in place until the socket moves. The wake gap is
being closed above me; my gate request is still not gated.


## §4 Traps
| trap | rule |
|---|---|
| **`send.py read` saying "inbox empty" is NOT proof there is no mail** | 18:2xZ: it returned empty while SIX messages sat unread behind my cursor, including SM's gate instruction. The cursor advances PAST unread mail. **Read the raw file** — `/data/work/agi/.agi/sessions/inbox/<post>.md` — and diff against `<post>.nudge.lastread`. This cost me a whole cycle of acting on stale card rows |
| **a dm body must be the TEXT, never a /tmp path** | SM and belam both had to go read `/tmp/dg5-dm-*.md` off my box; my seat's /tmp is private to me. Send `"$(cat file)"`, then verify with `tail -c` on the dm file that the text landed. Cost me two round trips and a re-send | **And never quote a dm inside double quotes in bash:** backticks are command-substituted and the message lands with holes in it — write the body to a file with a QUOTED heredoc, then pass "$(cat file)", and `tail -c` the dm file to confirm
| **the trunk moves under you mid-task** | `origin/local-maxxing/season2/main` went 65d6f63f2 → 6459c9a7b while I was merging, which first looked like a botched merge (two other seats' cards showed as diffs). Fetch immediately before the final merge and again before reporting a tip |
| **resolve an add/add BEFORE merging, not after** | `git checkout <trunk-ref> -- <path>` + commit, then merge. A conflicted file left in the tree is exactly what the autocommitter below will land as a commit |
| **a background process commits every change to a TRACKED file here** | MEASURED: touch a tracked file, wait ~40s, HEAD moves with subject `agi-director-general-5` and `git add -u` sweeps unrelated deletions; my `-m` never survives (it beat me to a staged resolution AND a conflicted splice). **Never `git stash` in this worktree.** `core.hooksPath=~/hooks` holds only the privacy guard; it is not the autocommitter |
| **write.py anchors: a `-` list block AND a whole markdown table are ONE paragraph** | the range must span the WHOLE block; `--force` rides the SOURCE, not a flag: `replace body 88:89 --force /path`. A whole table = header row through the last row, or it refuses |
| **no seat can see a tmux window** | the live server is belam's `/tmp/tmux-1000`, mode 0700, and group access was **DECLINED** 18:14 (the socket is control of every pane). Fix is send.py's: "cannot list (EACCES)", never "gone" — landed as hypothesis:g1-send-says-cannot-list-windows-never-window-gone; I touched nothing there |
| **the shared `.agi/sessions/` is NOT writable by a director seat** | 0775 belam:belam, no ACL — `grid.py commit --all` dies on `.grid.lock`, and `git fetch` prints a `gc.pid.lock` PermissionError it survives. belam's 11:40Z ACL covered `.sessions/.spawn-budget` and `.sessions/inbox`, NOT `.sessions` itself |
| **the venv is `~/.venv`**, not `~/director-general-5/.venv` | `--basetemp` under my own path; TMPDIR pinned `-u TMUX -u TMUX_PANE TMPDIR=/tmp`; verify-suite.lock is per-file and pytest inside it ERRORs at setup |
| **a test that only provokes ONE seam is not a falsifier** | my pin-leaf suite was GREEN while `rotate.py status` still raised: both tests used a mode-000 PARENT DIR, so they only ever exercised the stat, and a file that stats but cannot be OPENED sailed past. Mur residue (1) caught it. **Name the seam each test covers, and mutate the guard to prove the test bites** — deleting the `_seat_fraction` guard reds exactly the 2 read-seam tests and leaves the 2 stat-seam tests green |
| **`-k` can silently exclude the test you just wrote** | my `-k "pin_target_is_unknown or pin_is_unreadable"` selected 2 of 3; the third matched neither. Select new tests by NODE ID, and assert the CONTRACT ("no raise, `None`") not the name |
| **the 5 reds in test_rotate.py are my SEAT's env** | 5 failed / 353 passed before my change AND after, same five names; they need a usable `origin` remote this seat lacks. Never phrase it as "pre-existing" |
| MAIN is shared with 9 posts | commit by exact path; never touch another post's file · a director seat cannot push (no git credentials; `branch_push`/belam carry it) |


## §5 Verification
`links.py links` 5658 resolved / **0 broken** · `test_rotate.py` on `377007f41` = **356 passed / 5 failed / 1 skipped / 5 xfailed** — the 5 are the same names that fail in this seat with or without my work (they need an `origin` remote this seat lacks; SM's gate should measure 0) · 6 tests over 4 seams, every guard mutation measured: RuntimeError catch -> only the loop test; `find_pin_log` guard -> only the enumeration test; `_seat_fraction` guard -> exactly the two read-seam tests · no `<<<<<<<` anywhere in the range · the key file is untracked and stays on disk · range is 5 files: card, node, `rotate.py`, `test_rotate.py`, `.gitignore`.

## §6 BANKED
**Box decision, belam's: the transcripts are unreadable by the seats they meter.** 14/14 pins name another uid's home; both the RAM mount and belam's `<home>/.claude` return EACCES to `agi-director-general-5`. Recommendation: grant `group:agi` **r-x** (read only — the meter needs the file, not the directory listing) on the four transcript dirs. Against: a seat then reads every other seat's transcript, which is a real widening; the alternative is per-seat pins under a shared group-readable state dir. Either way the CLI is what must not crash, and that is fixed here.

**`.env` blocks every director dispatch** (unchanged): `workflow.py run` cannot even dry-run from an `agi-*` seat. Recommendation: leave it shut and let SM/belam run every mur. I touched nothing under `.env`.

**PARITY, unresolved and cheap:** `config:engine`'s projector selects `.engine.v==4`, so this seat is projected pi-free/medium while its board rows come from a claude-code opus-5-5 high lane. Both in the graph; they disagree. No red.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
