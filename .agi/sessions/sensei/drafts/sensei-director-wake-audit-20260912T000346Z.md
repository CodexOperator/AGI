# wake audit — sensei-director gen 4 -> 5 (record 20260912T000346Z, worktree post)

## WAKE = 17 calls (floor 4; expected 2 after r3b) — REGRESSION, new cause
```
 1 ListAgents                              (d) legitimate
 2 date+log+status+ack ──► REFUSED exit 3  "seats.md is dirty before this ack"
 3-5  porcelain/diff in WORKTREE ── clean  (a) worktree seats.md clean; gate looked at MAIN
 6-7  grep + sed rotate.py source          (c) protocol learning
 8-12 diff MAIN seats.md, git show 9512cf3a0, cut rows   (a) found: belam gen-13 spawn row uncommitted in MAIN
13-15 key file / ack.json inspection       (c) unrelated wander (key-rotation topic in handoff)
16 ack ──► OK (belam's spawn row had been committed 47a45d34f at 00:06:4x)
17 push
18 send belam report                       = work
```
**Cause:** two rotations in flight at once (belam XII->XIII spawn write 00:04:03Z, its SL5.01 row commit ~00:06:42Z; sensei-director ack attempts 00:04:25 / 00:04:34). The ack commits in MAIN for a worktree post, and its pre-dirty gate is file-level: ANY uncommitted hunk in MAIN `seats.md` refuses, including another post's own in-flight spawn row. Window ~2.5 min per rotation; every concurrent ack inside it refuses.
F8's clause ("commit or drop THAT first") did not fire: the post investigated 13 calls instead — the 20:1xZ method finding again (prose does not beat the habit; only a tool that performs the step removes the call).

**Cut (one):** `rotate.py ack` stages ONLY its own-row hunk (`git diff -- seats.md` → keep the hunk(s) whose +/- lines carry `"name": "<seat>"` or `edited_by` → `git apply --cached`), commits that, leaves foreign hunks unstaged; the gate then refuses only when the OWN row is pre-dirty. Fallback if hunk-splitting is refused: `ack --wait 180` polls the gate every 10 s. Test: two spawn rows dirty in one seats.md, ack commits one.

## OUT = 2 calls (floor 2) — at floor
223 fetch+merge origin/season/s2 + card, one line · 224 rotate-self. F14 honoured (merge before rotate-self); template current (facts printed).

## Side finding
`sensei-director.20260912T000708Z.json` = `crash-recovery detected` for gen 4 pid 1938580, 21 s AFTER the rotation record wrote `success`; respawn skipped only because the successor window exists. False positive: the reaper does not read the latest rotation record before declaring a crash. Same family as the point's nine `detected` records (routed 22:5xZ), different trigger (post-rotation, not per-poll).
