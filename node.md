---
id: experiment:a00-066fd887-4b53e2
mint_id: 6c3ef27326df4fc788bc3453e12b759b
type: experiment
parents:
  - hypothesis:l4-rotate-self-commits-its-own-spawn-row-write-so-the-ack-finds-seats-clean
next_edges: []
confidence: 0.82
edited_by: a00-d14bd402
evidence_runs:
  - experiment:a00-066fd887-4b53e2
loop: hypothesis:l4-rotate-self-commits-its-own-spawn-row-write-so-the-ack-finds-seats-clean@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0d2b3393c83ea793
season: 2
title: rotate-self commits its own s6.1 spawn-row write so the ack finds seats.md clean (g15.24 fix a, proven in git fixture)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-066fd887-4b53e2

## Experiment

g15.24 fix (a) — hypothesis:l4-rotate-self-commits-its-own-spawn-row-write-
so-the-ack-finds-seats-clean (Sensei's pick). This is a BUILD order, not a
measurement: reproduce the defect, implement the claim, prove it on the
built bytes.

### What I did

1. **Pre-fix reproduction (measured).** In a real git fixture (committed
   `seats.md` carrying the seat's own row), `cmd_rotate_self`'s s6.1
   `_successor_row_write` set the successor's own row fields
   (generation/session_id/window/pid) for generation 3 and left seats.md
   **DIRTY/uncommitted**: `_ack_seats_dirty` returned the seats.md rel. That
   dirt is exactly what the successor's `rotate.py ack --gen 3 --ref X
   continue` hits at the r3b gate (exit 3) — four seats, four hand-commits of
   the same write in one hour (Sensei 21:47Z dm).

2. **Implemented `_commit_spawn_row`** (rotate.py, placed beside
   `_ack_commit_seats`): ONE plain `git commit` in the seat worktree's
   toplevel — `git add -- <seats.md rel>` + `git commit -q -m '<seat> spawn
   row: gen <N>, session_id <uuid>, window <@id>, pid <pid>' -- <rel>`,
   touching seats.md ONLY. Mirrors `_ack_commit_seats` (same toplevel
   resolution, same seats.md-only pathspec, NEVER `git add -A`, never a grid
   commit, never a push). Records the outcome (sha) or the skip reason so it
   **never raises, never fails the rotation**.

3. **Wired it into `cmd_rotate_self`** at the top of the s6.1 block,
   immediately after `_successor_row_write` succeeds and BEFORE anything else
   runs; skipped for a THROWAWAY seat (`successor_row` = skipped ⇒ no row
   write ⇒ nothing to commit). Outcome lands in the handover as
   `spawn_row_commit` (and thereby the rotation record).

4. **Did NOT touch the r3b gate.** `_ack_seats_dirty` is unchanged — no
   lowering, no widening, no own-row carve-out. After (1) the ack's own
   commit is the only dirt, and a pre-dirtied seats.md from anyone else still
   refuses by name (exit 3) — re-proven by the still-passing
   `test_ack_dirty_seats_refused_before_write`.

5. **Claim (3) measure — first-seating spawn path.** `_successor_row_write`
   has a SINGLE call site (s6.1 in `cmd_rotate_self`). The spawn first-seating
   path (`_first_seating_spawn_writes`) writes only a meter pin and
   `seats/<S>.ack.json` into the GITIGNORED `sessions/` dir — it writes NO
   seat row, so it leaves seats.md byte-identical and needs no commit here.
   Claim (3) resolves to "no row written, nothing to measure/commit there".

### Tests added (extensions/agi/tests/test_rotate.py)

- `test_rotate_self_commits_own_spawn_row_write_then_ack_passes` — the core
  falsifier: spawn-row write dirties seats.md (PRE-FIX exit-3); `_commit_spawn_row`
  commits it (seats.md only, clean tree); the ack then passes the gate (rc 0,
  no exit-3) and lands a second commit. On seats.md: EXACTLY `[<seat> ack:,
  <seat> spawn row:, seats seed]`, each commit's diff-tree names seats.md and
  nothing else, working tree empty after each.
- `test_commit_spawn_row_records_skip_no_change_or_no_repo` — never raises;
  a clean-already seats.md records `spawn_row_commit: SKIPPED … already
  clean`, a truly gitless root records `SKIPPED — no git repo`; no commit is
  forced.

## Evidence

Command (all named files, run together):
`python3 -m pytest test_rotate.py test_session_start_seat_pre_spawn.py
test_session_start_bootstrap.py test_after_join_service.py
test_bin_help_smoke.py -q` → **219 passed, 2 skipped** (`test_rotate.py` +
the SessionStart/after-join/help smoke files). The two new g15.24 tests pass.

Pre-fix confirmed:
```
assert rotate._ack_seats_dirty(root, _git_toplevel(root))   # non-None
# → "proj/nodes/.geometry/seats.md"  (the exit-3 dirt before this round)
```
Post-fix spawn-row commit head subject (from the test):
```
<sha> belam spawn row: gen 3, session_id sess-123, window @w9, pid 4242
```
and the ack commit that follows it:
```
<sha> belam ack: gen 3, session_ref f52a4c, window @w9, pid 4242
```
`git show --stat` of the spawn-row commit names `proj/nodes/.geometry/seats.md`
and nothing else. `_git_toplevel` on a gitless root → None → the skip path.

Not done here (out of scope, per the hypothesis): no config:rotations /
director-template wording change — the exact lines a Prime edit would change
are the F8/director-template sentence telling a successor to hand-commit the
spawn row (outside rotate.py; owned by the Prime), so I named them in the
body here and edited no config node.

## Agent Notes
g15.24 fix (a): implemented _commit_spawn_row (seats.md-only plain git commit mirroring _ack_commit_seats; never -A/grid/push; never raises) wired into cmd_rotate_self right after _successor_row_write succeeds; r3b gate untouched. Reproduced pre-fix dirty-seats exit-3, proved post-fix ack passes with EXACTLY [ack, spawn-row] commits on seats.md, tree clean, seats.md-only diff-tree. First-seating spawn path writes no seat row (only gitignored sessions/) so nothing to commit there. Two new tests; named test suite 219 passed, 2 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-d14bd402, SL5.01). WHAT THE INSTRUCTION SAID: goal:g15.24 fix-only #2 ("rotate-self COMMITS its s6.1 spawn write itself ... ONE plain git commit ... touching seats.md ONLY ... the r3b gate `_ack_seats_dirty` is NOT lowered"). WHAT THE MACHINE ACTUALLY DOES: rotate.py:5025-5084 defines `_commit_spawn_row` (git add -- <seats.md rel>; git diff --cached guard; git commit -q -m "<seat> spawn row: gen N, session_id <uuid>, window <@id>, pid <pid>" -- <rel>); rotate.py:9237-9244 calls it immediately after `_successor_row_write` at s6.1, gated on `successor_row.startswith("config:seats row")` so a THROWAWAY seat commits nothing; `_ack_seats_dirty` (rotate.py:4960) is byte-identical to the pre-round version. I RAN the artifact, not the report: `python3 -m pytest test_rotate.py test_bin_help_smoke.py -q` -> 205 passed, 2 skipped (38s); the targeted `-k "spawn_row or ack_dirty or ack_continue_commits"` -> 5 passed. The falsifier test `test_rotate_self_commits_own_spawn_row_write_then_ack_passes` asserts PRE-FIX dirt (non-None `_ack_seats_dirty`), post-fix clean, EXACTLY three seats.md commits [ack, spawn row, seed], each `diff-tree` naming seats.md and nothing else, and a clean `git status` after each. NEAR MISS (unmeasured, recorded not fixed): `git commit -- <rel>` after `git add -- <rel>` commits EVERY hunk in seats.md, so if seats.md already carries a foreign dirt hunk when rotate-self runs, the spawn-row commit would bundle it -- the exact bundling the r3b gate refuses on the ack path. The hypothesis scoped r3b as unchanged and did not demand a rotate-self pre-dirt guard, so this is a forward note, not a demotion. DEVIATION: none -- the kid stayed inside FILE SCOPE (rotate.py + tests) and edited no config node.
<!-- THOUGHT:END -->
