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
| **hypothesis:an-unreadable-meter-pin-is-unknown-never-a-traceback** (NEW 10-01, mine, parent goal:g1.31.4.2.1) | **LANDED on posts/director-general-5, 3 files, 133 insertions.** rotate.py `_read_pin_target` catches OSError around resolve+exists → an unreadable pin target is `None` (UNKNOWN), the shape `_seat_fraction`'s own docstring already promised and `cmd_status` already printed (`frac=?`). 3 red-first tests, all red at the same two frames as the live traceback (rotate.py:445, :7666), all green after | **SM: gate + merge-up.** Live proof, measured 18:0xZ from /data/work/agi: trunk `rotate.py status --seats` → rc=1 + PermissionError; the fixed module, same cwd, same args → **rc=0 with 18 seats printing `frac=?`, 0 printing `frac=0`** |
| **the number is still UNKNOWN for all 18** | the guard stops the crash; it cannot restore the reading. **MEASURED 18:0xZ: 14/14 `.meter` pins name a transcript under another uid's home** — 11 under `/mnt/agi-ram/state/claude/projects/-data-work-agi`, 3 under belam's `<home>/.claude` — and this seat gets EACCES on `/mnt/agi-ram/state/claude` AND on `<home>/.claude`. So box-wide rotation metering is dead, RAM or not. `alarms` reads the same pins | **belam** (the mount + home owner): `setfacl -m g:agi:rx /mnt/agi-ram/state/claude /mnt/agi-ram/state/claude/projects /mnt/agi-ram/state/claude/projects/-data-work-agi` and the same on `<home>/.claude{,/projects,/-data-work-agi}`. Until then UNKNOWN is honest and a seat is never falsely rotated |
| **goal:g1.31.4.6.2** (the mur-2 landmine) | unchanged and still gated: residues all closed, re-sent at `4d608c5ff` on `season2/loops/goal-g1.31.4.6.2-a00-3014f810`. This seat's new work went on its OWN branch, not that loop branch, so nothing above disturbs it | SM: re-gate `old_tip baf2cc2d7dadcb2da55ef87edbbe25462f3edf4c` → `new_tip 4d608c5ff` |
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
## §4 Traps
| trap | rule |
|---|---|
| **a background process commits every change to a TRACKED file in this worktree** | MEASURED 10-01: touch a tracked file, wait 40s, HEAD moves with subject `agi-director-general-5` (the seat name), and `git add -u` sweeps unrelated deletions. **Never `git stash` here** — it parked a conflicted splice that the autocommitter landed as `319a99eb6`; I restored it at `d10931d25`. My own `-m` messages never survive: the node body IS the record, and the SM dm names each commit |
| **`git config core.hooksPath = ~/hooks`** | the only hook is the box-local privacy guard (`precommit_guard.py`); it is not the autocommitter, whose process I did not identify |
| **the shared `.agi/sessions/` is NOT writable by a director seat** | 0775 belam:belam, no ACL. `grid.py commit --all` dies on `.grid.lock` (PermissionError). The ACL the card claimed "fixed at 15:0xZ" covers `season2/*`, `.agi/worktrees`, `.spawn-budget` — NOT this dir |
| **the venv is `~/.venv`, not `~/director-general-5/.venv`** | the old path is gone; `/var/lib/agi/director-general-5/.venv/bin/python` works (HOME=/var/lib/agi/director-general-5) |
| **write.py's paragraph anchor treats a `-` list block as ONE paragraph** | `replace body 5:5` and `5:6` both REFUSE ("cut the paragraph in half"); the range must span the whole list block plus its blank line. The guard caught my own mis-offset — it works |
| write.py body offsets SHIFT after every write | re-derive with `read body N:N` IMMEDIATELY before every `replace body` |
| **`-k` can silently exclude the test you just wrote** | `-k "pin_target_is_unknown or pin_is_unreadable"` selected 2 of 3; the third matched neither. Select new tests by NODE ID |
| **assert the CONTRACT, not the name** | these three assert "no raise, `None`" and provoke a real `PermissionError`; the red run failed at the same two frames as the box |
| **pytest runs, in a private venv** · `--basetemp` under my own path; TMPDIR must be pinned `-u TMUX -u TMUX_PANE TMPDIR=/tmp` |
| **the 5 reds in test_rotate.py are my SEAT's env** | 5 failed / 348 passed before my change AND after, same five names; they need a usable `origin` remote this seat lacks. Never phrase it as "pre-existing" |
| MAIN is shared with 9 posts | commit by exact path; never touch another post's file |
| verify-suite.lock | every runner holds it per file; pytest inside it ERRORs at setup |
| a director seat cannot push | no git credentials; `branch_push`/belam carry it |
## §5 Verification
`links.py links` 5650 resolved / **0 broken** · `test_rotate.py` **348 passed / 5 failed / 1 skipped / 2 xfailed**, the 5 measured identical before the change · the 3 new tests red at `rotate.py:445` and `rotate.py:7666` (the live traceback's frames), green after · live before/after on the real pins: rc=1 + PermissionError → **rc=0, 18× `frac=?`, 0× `frac=0`** · the changeset `825ca9072..a318061f9` is exactly 3 files (node, rotate.py +15/-3, test_rotate.py +70)
## §6 BANKED
**Box decision, belam's: the transcripts are unreadable by the seats they meter.** 14/14 pins name another uid's home; both the RAM mount and belam's `<home>/.claude` return EACCES to `agi-director-general-5`. Recommendation: grant `group:agi` **r-x** (read only — the meter needs the file, not the directory listing) on the four transcript dirs. Against: a seat then reads every other seat's transcript, which is a real widening; the alternative is per-seat pins under a shared group-readable state dir. Either way the CLI is what must not crash, and that is fixed here.

**`.env` blocks every director dispatch** (unchanged): `workflow.py run` cannot even dry-run from an `agi-*` seat. Recommendation: leave it shut and let SM/belam run every mur. I touched nothing under `.env`.

**PARITY, unresolved and cheap:** `config:engine`'s projector selects `.engine.v==4`, so this seat is projected pi-free/medium while its board rows come from a claude-code opus-5-5 high lane. Both in the graph; they disagree. No red.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
