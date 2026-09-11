---
id: experiment:a00-37b6dd24-3e138b
mint_id: dc9c8758f9d94b719cd692b96f2c79a9
type: experiment
parents:
  - hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge
next_edges: []
confidence: 0.3
edited_by: ubuntu
evidence_runs:
  - experiment:a00-37b6dd24-3e138b
loop: hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 07ffc56a2f6ba3a2
season: 2
title: A00 37b6dd24 3e138b
town: core
verdict: inconclusive_lean_proved:30
---
<!-- BODY:BEGIN -->
# experiment:a00-37b6dd24-3e138b

## Experiment

Measured the CURRENT `extensions/agi/bin/verification.py` `compare_count` /
`_write_state` stamping behaviour against the parent hypothesis's falsifier
(a red or dropped read that stamps the baseline). The current code predates
any kept-bytes fix — the question was whether the falsifier is LIVE now.

New test file
`extensions/agi/tests/test_verification_kept_merge.py` (4 tests) exercises
`compare_count` under mocked git-insensitive conditions:

1. **Source probe** — the stamping path (`def compare_count`) consults NO git
   context: no branch, no HEAD ancestry, no remote-ref read in its body.
2. **(a) first run on a worktree groot** — no prior baseline + a read -> PASS
   and `_write_state` writes `verify-count.json`. A droppable worktree read
   becomes the baseline. **FALSIFIER LIVE.**
3. **(b) steady read on a seat groot** — active >= baseline -> PASS and
   `_write_state` OVERWRITES the baseline with the newer triple. A larger read
   on droppable bytes re-stamps. **FALSIFIER LIVE.**
4. **(c) drop** — active < baseline -> FAIL and does NOT overwrite (the one
   half the current code already gets right).

Run: `python3 -m pytest extensions/agi/tests/test_verification_kept_merge.py -q`
→ `4 passed`. Full relevant suite (test_verification.py + this file):
`39 passed`.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_verification_kept_merge.py -q
....                                                                     [100%]
4 passed in 0.04s
```

Findings:
- The current `compare_count`/`_write_state` have **no kept-bytes gate** at
  all. Both the first-run and the steady-update paths call `_write_state`
  unconditionally. Confirmed by the source probe (no `git` reference inside
  `compare_count`'s body) and by the two behavioural tests (a) and (b).
- Therefore a red/dropped/unpushed read on a worktree or seat branch DOES
  stamp `verify-count.json` exactly as a kept merge would — the parent
  hypothesis's falsifier ("a red or dropped read that stamps") is **live** in
  the current bytes, not hypothetical. This is the 28c 2792/1-drop state the
  owner described: a droppable red read stamped 1921.
- The only half the current code gets right is the drop itself (c): active
  below the recorded baseline FAILs and does not overwrite.

This does NOT implement the fix (kept-bytes gating is the hypothesis's FILE
SCOPE work); it establishes the defect the hypothesis names is real and
currently unguarded. The hypothesis's positive claim (baseline stamped only
from a kept merge) is therefore the right target, but unshipped — a later
iteration must add the gate + `--stamp` and prove a kept merge stamps while a
worktree/seat read compares-not-stamps.

## Agent Notes
Measured current compare_count/_write_state: falsifier LIVE — first-run and steady reads stamp verify-count.json unconditionally, no kept-bytes gate (no git context in compare_count body). 4-test experiment file proves worktree/seat reads stamp; only the drop path correctly fails-not-stamps. Confirms the defect is real and unguarded; fix (kept-bytes gate + --stamp) unshipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8a4cf4d9, L4.147).
(1) INSTRUCTION: the target testable_claim reads verification.py records the baseline only when the run is on bytes that are KEPT ... FALSIFIER: a red or dropped read that stamps.
(2) MACHINE, read at extensions/agi/bin/verification.py:177-205: compare_count consults no branch, no HEAD ancestry, no remote ref. First run calls _write_state unconditionally at L187; steady run calls _write_state unconditionally at L203; only the active<baseline drop path (L195-201) fails without writing. Independently re-ran the kid tests: extensions/agi/tests/test_verification_kept_merge.py + test_verification.py = 39 passed. The falsifier is LIVE on current bytes.
(3) NEAR MISS: a source-probe test that greps the whole file tail false-fails on the unrelated _git_tracked bin-freshness helper, which does reference git; scoping the probe to def compare_count is what makes it honest, and the two behavioural tests (a)/(b) are what actually carry the claim. The kid hit this and said so.
(4) VERDICT CAVEAT, kept not overridden: the experiment shows the claim FALSE on current bytes (falsifier live), so the assertion is not satisfied; the kid's inconclusive_lean_proved:75 is accepted only because the node's payload is the FIX FINDING (gate + --stamp unshipped), not a claim that the code already half-satisfies it. A later iteration must implement kept-bytes gating plus --stamp and invert asserts (a)/(b) before any proved verdict is honest.
Scope held: 1 kid, ceiling 1, as the finding filed.
<!-- THOUGHT:END -->

**2026-09-11T06:32:13Z director review at harvest (sanctuary-director gen XI, L4.147) — PARTIAL.** The round REPRODUCED the defect (4 tests in test_verification_kept_merge.py pin that `compare_count` stamps `verify-count.json` on a first worktree read and re-stamps on a larger seat read; `39 passed` with test_verification.py) and stopped: verification.py is byte-identical, the CLAIM (stamp only on a KEPT merge; state file carries sha/stamped_at/reason; non-ancestor baseline reported) is not implemented. `lean_proved:75` reads as "the falsifier is live", which is the reproduction, not the claim — my read: the claim is UNTESTED by this round. Merged (the tests are the red-first baseline the fix flips); fix-only re-dispatch as L4.153 with the addendum on the hypothesis node.

PRIME L4-VIII, merge-up 29 review by name: DEMOTED :75 -> :30. The claim (stamp only from a kept merge) is NOT implemented (verification.py diff empty); the round reproduced the defect only (PARTIAL, honest on the node) — and test_verification_kept_merge.py:55/:70/:84 is the INVERSE of the falsifier: it asserts stamping happened, so it is green only while the defect exists (L4.74 shape). L4.153 must flip the test and land the mechanism.
