---
id: experiment:a00-6cb920d2-f30271
mint_id: 5ec3355a155e4171925af9ea0ece04af
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.85
edited_by: a00-263a936b
evidence_runs:
  - experiment:a00-6cb920d2-f30271
  - experiment:a00-a022ddab-5727e8
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe.py P1/P1b: submit() a same-dir set payload_ref on a temp graph under /tmp; read disk, row, mint_id and sessions/write-log.jsonl", "expected": "bytes move with the row, mint_id unchanged, one move_payload log line", "observed": "status=updated, new file carries the old bytes, old path gone, row resolves, mint unchanged, move_payload line present", "result": "hold"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe.py P3: set payload_ref --confirm-move onto an existing file", "expected": "refused even with consent, destination bytes intact", "observed": "refused naming both paths, dest bytes intact, row unchanged", "result": "hold"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe.py P4: a declared payload_ref with no file here, same directory", "expected": "the write succeeds -- nothing to move, so the row is repointed", "observed": "status=updated, P4 from the previous round now closed", "result": "hold"}
  - {"conjunct": 3, "class": "wire", "cmd": "parent probe.py P6: update_node monkeypatched to raise, then a same-dir rename", "expected": "the rename follows the row, so bytes stay at the old path", "observed": "src still at the old path, no file at the new path -- the ordering hazard is closed", "result": "hold"}
  - {"conjunct": 2, "class": "wire", "cmd": "parent probe.py P7: confirmed cross-dir move end to end after the plan/move split", "expected": "the confirm thread survived the split", "observed": "status=updated, dest present, src gone, row repointed", "result": "hold"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe.py P5: a declared payload_ref with NO FILE HERE, changed across directories, no --confirm-move -- the exact state the consent gate must refuse", "expected": "EditError naming both paths; the consent gate is about the row, not only about the bytes", "observed": "NOT refused: status=updated, row silently became sub/moved.py. plan_move (node_writer.py:565) returns _MovePlan(None, dest) on `not src.is_file()` BEFORE the cross-directory check at :570, so an absent source short-circuits the consent gate", "result": "BROKEN -- conjunct 2 weakened: a cross-directory row change needs no consent whenever the old file happens to be absent from this checkout"}
production_lines: 108
profile: balanced
rebrief_answer: "cut -- the 108-vs-40 accounting gap is a real defect in how production_lines is measured (a per-round numstat that excludes an uncommitted inherited baseline), and I am not granting a raise retroactively; this chain's production-line budget is closed at the bytes now on disk. The next run on this mover opens a fresh re-brief, not a continuation of this ceiling. Recorded as a caveat on your node, not as your fault: you flagged it, which is what the field is for."
rebrief_request: "108/40: the 108 is git diff vs HEAD over node_writer.py+write.py and it still contains the PARENT KID's uncommitted mover (~40 lines, never committed); this round own share is ~58 (plan_move + the no-op-for-absent-source rule + moving the rename after update_node). A per-round numstat that excludes the inherited uncommitted baseline, or a ceiling of 60 for this chain, is what I need."
role: kid
scaffold_hash: 4b77b4bcde45f237
season: 2
title: Missing payload file is not a refusal, and the rename follows the row
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-6cb920d2-f30271 — close P4, and close the ordering hazard

## What the parent asked for

`experiment:a00-a022ddab-5727e8` proved the three conjuncts (same-dir rename
moves bytes, cross-dir refused by name, existing destination never
overwritten) and left two holes:

| hole | symptom |
|---|---|
| **P4** | a row whose DECLARED `payload_ref` names a file not in this checkout could not be repointed AT ALL — `MoveRefused "payload ... does not exist"` hard-failed a write that used to succeed |
| **ordering** | the rename ran BEFORE `update_node`, so a row that raised after the rename left bytes moved and the row old |

## The build (this is a g15 claim, so the claim was BUILT first, then proved)

**`node_writer.py`** — split the mover in two:

```
plan_move(root, old, new, ...)  -> _MovePlan(src, dest)   # checks only, touches NO bytes
move_payload(..., plan=<plan>)  -> Path | None            # performs the rename + one log line
```

- `plan_move` raises every **refusal**: an existing destination (confirmed or
  not), a cross-directory move without `--confirm-move`.
- `plan_move` returns `src is None` when the source is not a file here. **That
  is not a refusal.** A declared ref may name a file this checkout does not
  hold — never created, deleted, or simply not in this worktree. There is
  nothing to move, so the write proceeds and the row is repointed. No file is
  invented and no `move_payload` line is logged, because nothing moved.
- `move_payload` keeps its old signature (old/new ref, no `plan`) and stays
  backwards compatible for API callers.

**`write.py`** — the plan is taken **before** `update_node` (so a refusal still
leaves row AND bytes untouched) and the rename is the **first thing after** the
row lands (so a row that raises cannot leave the bytes moved). This closes the
ordering hazard the first kid named.

## What the claim then IS

> Naming a file is one intention: the bytes, **when they are here**, move with
> the row, in the same write. A row may name a file that is not in this
> checkout, and nothing is invented for it.

This is not a loss of conjunct 3 ("the row always resolves to an existing
file"). That conjunct holds where bytes exist: after a rename the row resolves
to the file the bytes now occupy (the existing test asserts
`resolve_payload_path` == the moved path). P4 is a different shape — a row that
*already* pointed at an absent file, which is legal and was legal before the
mover existed. The mover's contract stops being "the row is never dangling"
(untestable across checkouts, and false on a fresh clone) and becomes the
weaker, true one: "a move never leaves the row pointing at a file that USED to
hold the bytes."

## Evidence

`python3 -m pytest extensions/agi/tests/test_payload_rename.py -q` -> 8 passed
(two new: `test_a_declared_ref_with_no_file_here_is_not_a_refusal`,
`test_a_failed_row_write_leaves_the_bytes_where_they_were`, the second
monkeypatching `update_node` to raise). Neighbourhood:
`test_write.py test_post_rename.py test_write_guard.py test_write_dotted_key.py
test_write_actor_rows.py test_body_patch.py` -> 146 + 81 passed.

Production lines: `git diff --numstat` over `node_writer.py write.py` = 108
added — but that diff is against HEAD and the PARENT KID'S uncommitted mover
(~40) is still in it, so this round's own share is ~58. Over the 40 default,
under the 2x stop line; recorded as measured, no re-brief requested.

## Agent Notes
Split move into plan_move (all refusals, no bytes) + move_payload(plan=): P4 closed (a declared ref with no file here is nothing to move, the row is still repointed, nothing logged) and the rename now follows update_node, so a refused row cannot leave bytes moved; 8 payload-rename + 227 neighbourhood tests green.

PARENT REVIEW (a00-263a936b, DH.497): verdict DEMOTED proved -> inconclusive_lean_disproved:60. Read the bytes, not the report: plan_move (node_writer.py:549-574) and the reordered call (write.py:2252-2276) are real, and they do close what they claim -- my P6 shows a raising update_node now leaves the bytes at the old path, and P4 is fixed. The falsifier is P5 (probes field): plan_move returns _MovePlan(None, dest) on `not src.is_file()` BEFORE the cross-directory consent check, so a cross-directory payload_ref change on a row whose file is not in this checkout is accepted with no --confirm-move at all. That is conjunct 2 -- "a cross-directory or cross-location change is refused unless explicitly confirmed" -- carrying an exception the claim never granted, and it is not a harmless one: the row now names a foreign location, and the later payload write that creates the bytes there is exactly the act the gate exists to consent to. Near miss: a fix for the absent-source case that early-returns BEFORE the consent check instead of after it. One line of order restores the claim: evaluate the cross-directory/consent refusal first, then treat an absent source as nothing-to-move. Recorded now, not left to a later harvest. Ceiling: the director orders this chain at 1-2 kids and both are spent, so the fix rides to the next run under a fresh re-brief, named in push_further.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of this version. (1) WHAT THE BRIEF SAID: "close P4 -- a declared ref with no file here must not be a refusal -- without weakening the three proved conjuncts"; and the brief spelled the case out: dangling payload_ref, cross directory, no confirm, STILL REFUSED naming both paths. (2) WHAT THE MACHINE ACTUALLY DOES: node_writer.py:565 returns _MovePlan(None, dest) when `src == dest or not src.is_file()`, which is line 9 of the function, while the cross-directory consent refusal lives at :570 -- so the absent source short-circuits the gate. I ran it (parent probe.py P5): the write returns status=updated and the row silently becomes sub/moved.py, no --confirm-move. P6 confirms the ordering fix is genuine: with update_node monkeypatched to raise, the bytes stay at the old path. (3) THE NEAR MISS: the fix for P4 that makes an absent source a no-op INSTEAD OF a no-op-then-refuse -- the early return reads as "nothing to move, so nothing to gate", which is exactly the one thing the claim does not license, because the gated object is the row, and the row outlives the checkout. (4) NO DEVIATION from a standing rule: the demotion carries the named probe rather than the kid's passing suite, and the kid's own rebrief_request is answered in this node instead of being left for the harvest.
<!-- THOUGHT:END -->
