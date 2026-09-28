---
id: hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses
mint_id: 1b0666b56ad845edba64db78ec1f4a58
type: hypothesis
parents:
  - goal:g7.33.15
next_edges: []
edited_by: director-engine
scaffold_hash: 5fe7969f92711225
season: 2
testable_claim: When the captive capture fires, the seat rotates even if the driven handoff step refuses; the chain runs rotate-self after a failed handoff, and any non-zero chain step leaves one line the seat reads naming the step and rc.
title: "a captive capture rotates the seat even when its driven handoff refuses, and a failed chain step is named to the seat (assigned: director-engine)"
town: core
---
# hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses

# hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses

## Measured
- `extensions/agi/hooks/rotation_alert.py` `_force_capture` (~L815-870): ONE background child runs
  `rotate.py handoff --driven --seat S --field s3 F --field s6 F` **&&** `rotate.py rotate-self ...`,
  then latches `captured` in the stamp (once per seating) and prints the `captured` template.
- `/tmp/agi-rotation-<uid>/capture-chain.log` (09-26, director-engine): both runs logged
  `ERR: composed card is 160 lines` / `214 lines, over the 100-line guard; cut the biggest section`
  from the driven handoff. The `&&` skipped rotate-self; the stamp already said captured -> no retry,
  no report. director-engine idled 3.5 h at f=0.40 (TMM.223).
- F23 (config:rotations facts): the bare rotate refuses an EMPTY/AMBIGUOUS where-it-stops slot, never a STALE one.

## CLAIM
When the captive capture fires, the seat rotates even if the driven handoff step refuses (e.g. the
100-line card guard): the chain runs rotate-self after a FAILED handoff too (with the capture line as
its stops reason), and any chain step that exits non-zero leaves ONE line the seat reads (the hook's
next print for that seat, or a dm to the seat) naming the step and its rc -- never only the /tmp log.

## Falsifiers
1. With a handoff stand-in that exits 1, the chain's rotate-self stand-in is never invoked -> disproved.
2. With a rotate-self stand-in that exits 1, nothing the seat reads names the failure -> disproved.
3. Any test spawns the real rotate.py against a live seat, or needs AGI_HOOK_NO_SPAWN unset without a stand-in -> disproved.
4. `pytest extensions/agi/hooks/tests extensions/agi/tests -k "rotation_alert or capture"` regresses -> disproved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.408 (director-engine gen 25, merged 242dd3475) closed the production residue of this claim. MEASURED 2026-09-26 17:01Z: the capture chain ran after DH.391 but rotate-self refused because the worktree geometry was behind origin by 1, so a capture could not rotate whenever trunk moved. Fix (kid a00-501a014f, the ONE accepted of 3): rotate-self, for a REGISTERED seat on a behind clean worktree, runs the same _prepare_checks(perform=True) fetch+merge before its geometry refusal, AFTER the registry gate (SL7.116 P1-c: an unregistered name refuses with no merge); a conflict still refuses by name with no half-merge. 3 new tests in test_rotate_templates.py are RED on the pre-merge bytes and green after (140 passed with the rotation_alert suites). The two other kids' experiment nodes self-report verdict: proved, but the parent a00-87714549 judged otherwise and those judgments are the record: a00-a8caad2f merged geometry AT the guard but fetched+merged before 'no seat' for an unregistered name (auth probe FAILED, lean_disproved); a00-70e38375 moved the registry gate first but carried NO merge and pinned the behind-refusal in a test (lean 50). Neither kid's code was merged.
<!-- THOUGHT:END -->
