---
id: experiment:a00-566e47fe-b4df96
mint_id: 36f41134797349dfb1695a22f694a755
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.9
edited_by: a00-c7aa5f71
evidence_runs:
  - experiment:a00-566e47fe-b4df96
line_ceiling: 12
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 955e2bd96f0012d6
season: 2
title: "DH.544 corrective: verdict THOUGHT rewritten whole, the self-citation gate misread corrected, the dropped tmp-work arm re-added and canary-tested, suite re-run on this revision"
town: core
verdict: proved
---
# experiment:a00-566e47fe-b4df96 -- DH.544 corrective: the truncated THOUGHT, the misread gate, the dropped pattern arm, and the suite re-run on this revision

## What I did (4 dispatch items, node text and one test re-run; no production code touched)

| # | Item | Action | Where the bytes are |
|---|------|--------|---------------------|
| 1 | verdict THOUGHT landed truncated mid-sentence | rewrote the THOUGHT block from scratch, ordered: order quoted / machine behaviour with line numbers I read / the near miss / rule deviations | `.agi/nodes/verdict/a00-033193ed-599c69.md` THOUGHT (ends with `id -un`, not by quoting the name)` |
| 2 | experiment node misreads the gate it cites | corrected the residue: the check refuses SELF-citation only; the cited object counted fine | `.agi/nodes/experiment/a00-6cd691ef-5c399e.md` residue bullet 1 |
| 3 | detector rebuild dropped a pattern alternative | re-added it (assembled, so it still cannot self-match) and extended the canary so the re-add is TESTED | `.agi/nodes/experiment/a00-651ab5e8-e70670.md` sh block + canary text |
| 4 | suite claim not re-run on the round's bytes | re-ran the refusal-file suite in THIS checkout | below |

## Item 1 -- the truncated THOUGHT

The block ended at the fragment `- \`unset demote_reason` with `<!-- THOUGHT:END -->` on
the next line, so the ordered reason order 1 required was unreadable while the body
claimed it was recorded. Rewritten whole (never appended), carrying: the DH.485 order
quoted; the machine facts read by me (stamps absent from the key list, `evidence_runs`
now the two non-object runs, `inconclusive_lean_proved:70`); the near miss -- the
`demote_reason` text itself records the earlier `evidence_runs=0`, a bare int that
`normalize_evidence_runs` (evidence_gate.py:250-293) maps to 0, so the stamp was the
gate working, not failing; and deviations (none). The last line before
`THOUGHT:END` is a complete sentence, read back from the file after the write.

## Item 2 -- the misread gate, corrected against bytes I read

Old claim (false): "The self-citation check (evidence_gate.py:322-340) would have
demoted the verdict to a lean on its own." What I read in this checkout:

```sh
grep -n 'def \|_is_self_citation\|return sum(' extensions/agi/bin/evidence_gate.py
306:def _is_self_citation(value, self_id, allow_self: bool) -> bool:
295:        return sum(
299:            and not _is_self_citation(v, self_id, allow_self)
330:def is_unverifiable_attestation(value) -> bool:
```
- `_is_self_citation` = :306-327; the compare is `str(value).strip() == str(self_id).strip()`
  at :326-327 -- SELF only.
- the counting loop = the `return sum(...)` at :295-299.
- :322-340 (the range the node cited) is a docstring tail plus the head of
  `is_unverifiable_attestation` -- not the enforcement.
- the verdict cited its OBJECT (`experiment:a00-651ab5e8-e70670`), so the gate counted
  that entry and would NOT have demoted. The correction is written into the node.
  The stale stamps' own cause (an earlier `evidence_runs=0`) stands.

## Item 3 -- the dropped alternative, re-added and TESTED

The DH.485 pattern carried a tmp-root work-area alternative; the DH.528 rebuild dropped
it and the canary had no line of that class, so the loss was invisible. Re-added as
`alt tmp /work` (assembled, so no searched literal appears contiguously in the node and
the probe still cannot match its own line) and the canary extended to five lines.

Re-runs, pasted:

```
$ bash $S/pat.sh .agi/nodes/experiment/a00-651ab5e8-e70670.md   # after the edit
rc=1   (0 hits)
$ bash $S/pat.sh $S/canary.txt
(canary line content REDACTED here: this node is itself grepped by that pattern, and a
 node that quotes the paths it hunts is a self-hit. The canary file lives in my session
 dir and the numbers below are the measurement.)
rc=0   (4 hits over 5 lines -- lines 1,2,3,4; line 5 is a non-matching filler)
```
The canary hit on line 4 is the re-added arm firing: before the re-add the same canary
gave 3 hits. Probe over the three nodes I edited: rc=1 on the detector's own node, and
on the other two the only hits are the path/IP arms those nodes legitimately quote --
the user-name arm gives 0 hits on all three, which is the property under test.

Weakness that survives, stated because the order asked: the residue path this node
actually found was a data-root path, already covered by the `alt dat a` arm, so the
re-add restores coverage of the CLASS and changes no finding recorded in that node.

## Item 4 -- the suite, re-run on this revision

```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
    extensions/agi/tests/test_heal_worktree_refusal.py -q --noconftest \
    -p no:cacheprovider --basetemp=/tmp/pt544a
6 passed, 3 warnings in 0.21s
$ ... test_bin_help_smoke.py + test_heal_worktree_refusal.py (same flags, /tmp basetemp)
78 passed, 6 skipped, 3 warnings in 5.00s
```
Revision note: this is THIS worktree's file, where
`test_the_recorder_gate_is_not_vacuous` is at :124 (the round base's blob cited it at
:84-139) -- line numbers from the order do not transfer. No real pane, seat or worktree
is reachable: the autouse `_no_live_tmux` records tmux argv through a monkeypatched
`subprocess.run` (:103, :112) and `test_the_recorder_gate_is_not_vacuous` proves the
gate fires. Fixtures only. 0 USD.

## Production lines

`git diff --numstat -- extensions/agi/bin extensions/agi/tests` is EMPTY: 0 production
lines and 0 test lines against a ceiling of 12. Node text only, all through write.py.

## Residue, named not patched

- Nothing here changes the mechanism behind these findings: a node can still cite a
  reader (a gate, a line range) it never ran, and a rebuilt detector can still lose an
  alternative silently. Both cost a round to notice; the first is engine-side
  (evidence_gate / cli) and outside this slice.
- Unrelated uncommitted files from other agents are present in this tree; I left every
  one of them exactly where it was and staged nothing.

## Agent Notes
4 dispatch items fixed in the bytes: verdict THOUGHT rewritten whole (was truncated mid-token), the self-citation-gate misread corrected to the lines I read (_is_self_citation :306-327, sum loop :295-299), the dropped tmp-work arm re-added and the canary extended so it is tested (rc=1/0 hits on the node, rc=0/4 hits on the 5-line canary), suite re-run here -> 6 passed; 0 production lines

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.544 (a00-c7aa5f71) -- ACCEPTED, 0 production lines claimed and none I can see, write.py only, 1 kid, no second kid spawned (HARD CAP 1). I read the live node bytes in this worktree and ran my own probes; I did not re-run the kid suite as evidence of its claim.

probes (all mine, run by me, against the bytes):
- gate/ITEM-3 (the re-added arm FIRES on the class it was dropped for): I extracted the detector sh block out of experiment:a00-651ab5e8-e70670.md myself and ran it over a canary whose ONLY line is a tmp-root work-area path -> rc=0, one hit on line 1. Before the kid-s re-add that line was invisible; the coverage regression is closed and the measurement is reproducible, not asserted. HOLD.
- gate/ITEM-3 (still cannot match its own node): the same extracted block over experiment:a00-651ab5e8-e70670.md -> rc=1, 0 hits. The `alt tmp /work` re-add kept the assembly property, so restoring the arm did not buy coverage by re-introducing the self-match. HOLD.
- auth/ITEM-3 (wrong class must NOT be caught -- the re-add is not an over-broad /tmp arm): canary lines `/tmp/other/x` and `/var/tmp/x` -> rc=1, 0 hits. A fix that appended `alt tmp ` would also have satisfied "re-add the dropped alternative" in its weakest reading and would flag every tmp path; this one does not. HOLD.
- wire/ITEM-4 (the suite claim reaches live bytes, not a report): `env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_heal_worktree_refusal.py -q --noconftest -p no:cacheprovider --basetemp=/tmp/pt544b` -> `6 passed, 3 warnings in 0.21s` in MY worktree, and the parent had already run the same command on the round base before the spawn (`6 passed, 3 warnings in 0.62s`). Two independent runs, same count, and the kid-s revision note (:124 vs the order-s cited :84-139) is honest about which blob it ran. HOLD.
- gate/ITEM-2 (the false gate claim is gone, not merely hedged): `grep -n "would have demoted" .agi/nodes/experiment/a00-6cd691ef-5c399e.md` -> 0 hits; the residue bullet now names _is_self_citation :306-327, the return sum(...) loop at :295-299, and states that :322-340 is a docstring tail plus the head of is_unverifiable_attestation. I read those lines myself in evidence_gate.py before accepting: they are what the node now says they are. HOLD.
- gate/ITEM-1 (the THOUGHT is whole, not truncated): the block now runs order-quoted / machine-read / near-miss / deviations and its last line before THOUGHT:END is a complete sentence ending `...not by quoting the name.`; the old fragment `- \`unset demote_reason` is gone. HOLD.

MECHANISM, NOT WORDING. (1) WHAT THE ORDER SAID, quoted: "For EACH item: fix it in the bytes, OR -- when the item is already true or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number)." (2) WHAT THE MACHINE ACTUALLY DOES: the sh block is not prose about a probe, it is a runnable body, so I copied it out of the node with a regex over the fenced block and ran it against three canaries I wrote myself; grep -nE -f - reads its patterns from stdin, and the re-added `alt tmp /work` is assembled at run time exactly like the four arms that survived, which is why the node itself still measures 0 hits after the re-add instead of one more. (3) THE NEAR MISS: a kid can satisfy item 3 by writing that the arm was re-added and widening the canary to five lines, pasting the 4-hit count, and every number in the report stays true -- while the pattern in the sh block never gains the arm, because the canary hit it credits is indistinguishable from the three hits that were already there. My single-line tmp-root canary is what separates 4 hits-that-were-already-there from 1 hit that is new; the kid-s own claim is that the same canary gave 3 before and 4 after, and my probe reproduces the 4 from the block as it now stands. (4) RULE DEVIATIONS: none of mine. The kid ran a read-only `git diff --numstat` to justify its 0-production-lines claim and said so in the node; the harness forbids git to me, and I did not run any, so that number is the kid-s measurement, cited as such and not restated as mine.

RESIDUES I AGREE WITH, NAMED NOT PATCHED: the re-add changes no finding recorded in experiment:a00-651ab5e8-e70670.md (its residue path was a data-root path, already covered), so this round restores a CLASS and moves no verdict; and the engine-side hole the kid names -- a node can still cite a reader (a gate, a line range) it never ran -- is outside FILE SCOPE and goes to the director-s findings row, not to this slice.
<!-- THOUGHT:END -->
