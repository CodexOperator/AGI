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
| **hypothesis:an-unreadable-meter-pin-is-unknown-never-a-traceback** (mine, parent goal:g1.31.4.2.1) | **LANED to SM 18:3xZ, mur pi-free RUNNING.** rotate.py `_read_pin_target` catches OSError around resolve+exists → an unreadable pin target is `None` (UNKNOWN), the shape `_seat_fraction`'s docstring already promised and `cmd_status` already printed (`frac=?`). 3 red-first tests, red at the same two frames as the live traceback (rotate.py:445, :7666). Live proof from /data/work/agi: trunk `rotate.py status --seats` → rc=1 + PermissionError; fixed module → **rc=0, 18× `frac=?`, 0× `frac=0`** | **SM: mur then gate. Under the g7.16.1.11 hold — rotate code needs the mur first. Nothing due from me** |
| **the NUMBER stays UNKNOWN — DECLINED, and I accept it** | belam [decision] 18:14: transcript ACL `g:agi:rx` **DECLINED** at the uid boundary (every v5 post would read every old post's full transcript; old posts are metered by the belam uid; a v5 pin should name its OWN transcript — residue to DG3). The CLI guard is the part that survives, which is the right division. No permission touched by me | closed |
| **goal:g1.31.4.6.2** (the mur-2 landmine) | **LANDED cfda80960 on the trunk at 17:5xZ** (lean :90, 7794 + re-run 645 / 1 trunk red). SM 17:5xZ: *"your loop branch is landed: yours to retire"* — `season2/loops/goal-g1.31.4.6.2-a00-3014f810`. Nothing open | SM retires it |
| goal:g4.18.5.3 | DG1's node — I did not write it. Falsifier 1 must name `write.ONE_ROW_WRITE`; the guard is inert until it does. C3 must declare `post-rename` an exception with a test | DG1 (asked twice) |
| goal:g1.31.4.2.1 (#40 #42 #31) | DG4's worktrees | SM owns |
| goal:g1.31.4.1 (#8 #9) | CLOSED 10-01 | — |
| goal:g7.16.1.5.4 | closes when the RAM worktree count is 0; `/mnt/agi-ram` denies me (`drwx--x---`, `group:agi:--x`) | SM/box |
| goal:g1.31.5.3, g4.18.5.6, g7.16.1.5.5.x | not dispatched — no dispatch path from any director seat | with the `.env` decision |
| the conftest trap my §4 used to carry | **DORMANT, measured 18:0xZ**: `/data/work/agi/.agi/worktrees` iterates 720 entries with zero raising — the RAM symlink `a00-4576a1ff` stats fine because `/mnt/agi-ram` grants `group:agi:--x`. DG1's node owns it | DG1 |
## 🔴 Where it stops
```
A new leaf LANDED and is WAITING ON THE MASTER: SM must gate + merge-up
posts/director-general-5 (8 commits, 3 files). I cannot push (no git
credentials: "could not read Username for 'https://github.com'"), cannot
run grid.py commit --all (/data/work/agi/.agi/sessions is 0775 belam:belam,
no ACL — .grid.lock is belam:belam 0664), and cannot dispatch or run a mur
(.env is 0640). Every one of those three is the SAME defect: a director seat
has no write path outside its own branch.

Next command (pickup post):
  git -C /var/lib/agi/director-general-5/t log --oneline -8
```
```
What the guard does NOT do, stated so nobody reads more into it: an unreadable
pin is UNKNOWN, never a zero, and never a rotation. With all 14 pins sealed,
`rotate.py status` now prints the whole table and 18 UNKNOWNs instead of
crashing on row one — the shape the code already documented, finally reached.
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
| trap | rule |
|---|---|
| **`send.py read` saying "inbox empty" is NOT proof there is no mail** | 18:2xZ: it returned empty while SIX messages sat unread behind my cursor, including SM's gate instruction. The cursor advances PAST unread mail. **Read the raw file** — `/data/work/agi/.agi/sessions/inbox/<post>.md` — and diff against `<post>.nudge.lastread`. This cost me a whole cycle of acting on stale card rows |
| **a dm body must be the TEXT, never a /tmp path** | SM and belam both had to go read `/tmp/dg5-dm-*.md` off my box; my seat's /tmp is private to me. Send `"$(cat file)"`, then verify with `tail -c` on the dm file that the text landed. Cost me two round trips and a re-send |
| **the trunk moves under you mid-task** | `origin/local-maxxing/season2/main` went 65d6f63f2 → 6459c9a7b while I was merging, which first looked like a botched merge (two other seats' cards showed as diffs). Fetch immediately before the final merge and again before reporting a tip |
| **resolve an add/add BEFORE merging, not after** | `git checkout <trunk-ref> -- <path>` + commit, then merge. A conflicted file left in the tree is exactly what the autocommitter below will land as a commit |
| **a background process commits every change to a TRACKED file here** | MEASURED: touch a tracked file, wait ~40s, HEAD moves with subject `agi-director-general-5` and `git add -u` sweeps unrelated deletions; my `-m` never survives (it beat me to a staged resolution AND a conflicted splice). **Never `git stash` in this worktree.** `core.hooksPath=~/hooks` holds only the privacy guard; it is not the autocommitter |
| **write.py anchors: a `-` list block AND a whole markdown table are ONE paragraph** | the range must span the WHOLE block; `--force` rides the SOURCE, not a flag: `replace body 88:89 --force /path`. A whole table = header row through the last row, or it refuses |
| **no seat can see a tmux window** | the live server is belam's `/tmp/tmux-1000`, mode 0700, and group access was **DECLINED** 18:14 (the socket is control of every pane). Fix is send.py's: "cannot list (EACCES)", never "gone" — landed as hypothesis:g1-send-says-cannot-list-windows-never-window-gone; I touched nothing there |
| **the shared `.agi/sessions/` is NOT writable by a director seat** | 0775 belam:belam, no ACL — `grid.py commit --all` dies on `.grid.lock`, and `git fetch` prints a `gc.pid.lock` PermissionError it survives. belam's 11:40Z ACL covered `.sessions/.spawn-budget` and `.sessions/inbox`, NOT `.sessions` itself |
| **the venv is `~/.venv`**, not `~/director-general-5/.venv` | `--basetemp` under my own path; TMPDIR pinned `-u TMUX -u TMUX_PANE TMPDIR=/tmp`; verify-suite.lock is per-file and pytest inside it ERRORs at setup |
| **`-k` can silently exclude the test you just wrote** | my `-k "pin_target_is_unknown or pin_is_unreadable"` selected 2 of 3; the third matched neither. Select new tests by NODE ID, and assert the CONTRACT ("no raise, `None`") not the name |
| **the 5 reds in test_rotate.py are my SEAT's env** | 5 failed / 353 passed before my change AND after, same five names; they need a usable `origin` remote this seat lacks. Never phrase it as "pre-existing" |
| MAIN is shared with 9 posts | commit by exact path; never touch another post's file · a director seat cannot push (no git credentials; `branch_push`/belam carry it) |

## §5 Verification
`links.py links` 5650 resolved / **0 broken** · `test_rotate.py` **348 passed / 5 failed / 1 skipped / 2 xfailed**, the 5 measured identical before the change · the 3 new tests red at `rotate.py:445` and `rotate.py:7666` (the live traceback's frames), green after · live before/after on the real pins: rc=1 + PermissionError → **rc=0, 18× `frac=?`, 0× `frac=0`** · the changeset `825ca9072..a318061f9` is exactly 3 files (node, rotate.py +15/-3, test_rotate.py +70)
## §6 BANKED
**Box decision, belam's: the transcripts are unreadable by the seats they meter.** 14/14 pins name another uid's home; both the RAM mount and belam's `<home>/.claude` return EACCES to `agi-director-general-5`. Recommendation: grant `group:agi` **r-x** (read only — the meter needs the file, not the directory listing) on the four transcript dirs. Against: a seat then reads every other seat's transcript, which is a real widening; the alternative is per-seat pins under a shared group-readable state dir. Either way the CLI is what must not crash, and that is fixed here.

**`.env` blocks every director dispatch** (unchanged): `workflow.py run` cannot even dry-run from an `agi-*` seat. Recommendation: leave it shut and let SM/belam run every mur. I touched nothing under `.env`.

**PARITY, unresolved and cheap:** `config:engine`'s projector selects `.engine.v==4`, so this seat is projected pi-free/medium while its board rows come from a claude-code opus-5-5 high lane. Both in the graph; they disagree. No red.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
