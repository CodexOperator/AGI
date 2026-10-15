---
id: experiment:a00-7c94259b-23b7de
mint_id: 6a855b7759734008b25f404c8d7ee0cc
type: experiment
parents:
  - hypothesis:l4-quiet-posts-a-quiet-settings-token-on-a-row-writes-the-dm-but-types-no-nudge-never-refires-a-stale-marker-and-wake-repair-skips-the-row
next_edges: []
confidence: 0.85
edited_by: a00-f0ed4b5b
evidence_runs:
  - experiment:a00-7c94259b-23b7de
line_ceiling: 35
loop: hypothesis:l4-quiet-posts-a-quiet-settings-token-on-a-row-writes-the-dm-but-types-no-nudge-never-refires-a-stale-marker-and-wake-repair-skips-the-row@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "\"P1(wire/dm): send_dm to a QUIET row types zero send-keys and zero Enter (kid1 left this open; kid2 choke-point guard closes it) -- PASS. P2(wire/choke): _nudge_window(body=<dm>) on a quiet row types nothing -- PASS. P3(gate/conjunct4): existing test_send.py+test_send_quiet.py (329) and test_heal_watch+test_heal+test_rotate (398) pass UNCHANGED, so non-quiet nudge/wake/dm behavior is byte-intact -- PASS. Parent probe_final.py.\""
production_lines: 52
profile: balanced
role: kid
scaffold_hash: ce3e12b4562432d6
season: 2
title: "quiet posts: DM to a quiet row types nothing at the _nudge_window choke point"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7c94259b-23b7de

## Experiment

SECOND kid on the QUIET-POSTS build. Kid 1 (experiment:a00-b98f2ef1-0d6857)
landed the `quiet` machinery on its OWN sibling branch (`season2/loops/
...a00-b98f2ef1`), NOT in this worktree — the re-brief that said kid 1's edits
were uncommitted here was STALE (my HEAD == kid 1's parent commit ceb81713b).
I reconstructed kid 1's committed bytes into this tree with `patch -p1` off
`git show 0a4fb0061` (base matched exactly), verified the 4 files landed, then
built my assignment on top.

THE FAILING PROBE (parent a00-f0ed4b5b): a DM to a quiet row still TYPED a
nudge, because kid 1 guarded `send()` / `wake()` / `heal._repair_stranded_wakes`
but NOT the `_nudge_window` choke point that `send_dm` funnels through
(`send_dm` -> `_nudge_window(find_project_root(croot), other, sender=...,
body=text)`).

THE FIX (send.py, +7 lines): a quiet-skip at the very top of `_nudge_window`,
before resolution/capture/typing — `if _row_is_quiet(root, to): return True`
(+ 6 comment lines). Because `send_dm` writes the dm file BEFORE calling
`_nudge_window`, the dm/record still lands; the choke-point guard makes EVERY
nudge entry point (send, send_dm, wake, heal, stranded retry) skip a quiet
row by construction — no send-keys, no copy-mode cancel, no marker, no
pending/deferred write. The `root` handed to `_row_is_quiet` is the SAME root
that always resolved the nudge target, so it is consistent by construction.

The DM-probe reproduced as a regression test
(`test_send_dm_to_quiet_row_types_no_nudge` in test_send_quiet.py): writes the
dm (`project/dm/director--mee.md`), types NO `send-keys -l` and NO Enter.
KEY FIXTURE FINDING: `send_dm` resolves its nudge root via
`find_project_root(croot)` -> the `.agi` graph dir, so the seats row for this
test must live at `<project>/.agi/nodes/.geometry/seats.md` (the existing
`test_dm_stale_id_repairs_by_name` confirms this), NOT at the project-root
`nodes/.geometry/` layout kid 1's send()/wake()/status() tests use. The
production code needs no change for this — both roots resolve the same graph
in a real `.agi` tree.

## Evidence

All tests run with an isolated `--basetemp` under /tmp.
- `pytest extensions/agi/tests/test_send_quiet.py` -> 7 passed (kid 1's 6 +
  the new DM probe regression test).
- Falsifier, untouched suites -> `pytest test_send.py test_heal.py
  test_heal_watch.py test_rotate.py` -> 720 passed.
- Production lines (git diff --numstat HEAD): send.py +25/−3, rotate.py
  +21/−8, heal.py +6 = 52 total additions. Kid 1 already over the 35 ceiling
  (45); mine adds 7 -> 52, under the 70 hard-stop, so no re-brief.
- Pre-fix probe reproduced as a failing test first (typed nudge) then the
  choke-point guard made it pass — the falsifier is now a permanent regression
  guard.

## Agent Notes
DM to a quiet row is now silent at the _nudge_window choke point: guard returns True before any typing, covering send/send_dm/wake/heal/stranded by construction. Built on kid 1 (reconstructed from its sibling branch commit since the re-brief was stale). 7 quiet tests incl. the DM-probe regression; 720 falsifier tests pass.

"PARENT REVIEW (a00-f0ed4b5b): ACCEPTED. Covers all 4 conjuncts + the umbrella dm falsifier that disproofed kid1; choke-point guard in _nudge_window makes send_dm/wake/send/heal all honor quiet. Caveat: production_lines 52 > 35 ceiling, invoked the re-brief conflict rule (falsifier-safe); the falsifier requirement (token-list AND JSON-cells AND quiet+ultracode composition AND 4-entry-point suppression) cannot go materially narrower."
