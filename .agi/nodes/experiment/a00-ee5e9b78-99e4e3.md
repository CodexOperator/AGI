---
id: experiment:a00-ee5e9b78-99e4e3
mint_id: c7673c87b7604088abb496693eba1ba3
type: experiment
parents:
  - hypothesis:l4-a-parent-cuts-five-and-merges-its-kids
next_edges: []
confidence: 0.85
edited_by: a00-e9b9b808
evidence_runs:
  - experiment:a00-ee5e9b78-99e4e3
loop: hypothesis:l4-a-parent-cuts-five-and-merges-its-kids@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f11aca41b02b3581
season: 2
title: A00 ee5e9b78 99e4e3
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-ee5e9b78-99e4e3

## Experiment

Kid 2/2 of hypothesis:l4-a-parent-cuts-five-and-merges-its-kids — the merge half.
Landed the `merge-kids` verb in `extensions/agi/bin/season.py` (next to the
merge-up template) and the FIXTURES-ONLY proof in
`extensions/agi/tests/test_season_merge_kids.py`. No git in this repo; every
merge runs inside a temp repo under tmp_path (fixtures, never this tree).

`season.py merge-kids <kidbranch>... [--suite CMD]` merges each named kid branch
into the CURRENT branch, one at a time, in order:
  * refuse zero-commits-ahead (`git rev-list --count` == 0)
  * `git merge --no-ff --no-commit <branch>`
  * on conflict, `git diff --name-only --diff-filter=U`; if EVERY path is under
    `.agi/nodes/` union-resolve each (below) and `git add`; if ANY path is
    SOURCE, print the paths, leave MERGE_HEAD in place, exit non-zero (the
    parent resolves it as an edit it owns) — never `git apply --3way`
  * run the suite on the merged bytes; red -> `git merge --abort` +
    `REFUSED: suite red after merging <branch>`; green -> `git commit --no-edit`
    with merge-up's FALSE-RED guard (MERGE_HEAD absent after a non-zero commit
    = the merge landed, treat as green)

The node-conflict resolver is built from PURE functions (no git needed,
testable): `_conflict_sides`, `_agent_notes_block`, `_union_notes`,
`_verdict_strength`, `_higher_confidence_verdict`, `_resolve_node_conflict`.
Resolution starts from the ours side, replaces the `## Agent Notes` block with
the union of BOTH sides' notes (dedup identical lines, first-seen order), and
writes the higher-confidence verdict/confidence pair into the frontmatter.
`_verdict_strength` ranks proved/disproved (3) > inconclusive_* (2) > pending
(1) > unknown (0), then the `:N` percent, then the confidence fraction; a tie
keeps ours. No new bin/*.py; scope exactly season.py + one test file + this node.

## Evidence

`python3 -m pytest extensions/agi/tests/test_season_merge_kids.py -v`: 9 passed.
Covered: clean merge; node-conflict UNION keeps BOTH distinct note lines and
the higher-confidence verdict; the KID-held `proved` beats the round's
`pending`; source-conflict REFUSES + names src.py + leaves MERGE_HEAD present +
commits nothing; suite-red aborts the merge + commits nothing; zero-ahead
refused; two clean branches merged in order; two pure-function tests (with the
module imported directly, no probe file).

`AGI_TIER= python3 -m pytest extensions/agi/tests/ -q`: 2772 passed, 2 failed —
both the pre-existing environmental `test_reconciler` frozen-L485 pid-liveness
failures (reconciler never reads `spawned_by_agent`; noted by kid 1, neither
caused here nor fixed). No new failures from this change.

Fixture design note: a node "conflict" had to be a GENUINE same-line
modify/modify — both sides branch from base and edit the SAME line. Git
auto-merges cleanly when one side only appends new lines while the other
leaves them, which is exactly why the union path fires only on a real conflict,
as the protocol intends.
<!-- BODY:END -->

## Agent Notes
merge-kids verb + fixtures-only proof landed; season.py union-resolves node conflicts keeping higher-confidence verdict, refuses+named SOURCE conflicts leaving MERGE_HEAD, suite-gated; 9/9 new tests, full suite 2772 passed / 2 pre-existing reconciler frozen-pid fails

PARENT REVIEW (a00-e9b9b808, iter 130): ACCEPTED at 85 (kept). (1) INSTRUCTION: 'the PARENT MERGES every kid branch ... a conflicts in a NODE file is resolved by UNION of the Agent Notes and the higher-confidence verdict line, never a blind git apply --3way' and 'FIXTURES ONLY: a temp repo ... 3 kid branches'. (2) MACHINE: read season.py:1436 cmd_merge_kids and its PURE resolvers (_conflict_sides/_agent_notes_block/_union_notes/_verdict_strength/_higher_confidence_verdict/_resolve_node_conflict at 1257-1380); _resolve_conflicted (1396) returns 3 for a SOURCE conflict and returns BEFORE aborting, so MERGE_HEAD survives for the parent; the suite runs on the merged bytes and a red run does git merge --abort before any commit. I re-ran test_season_merge_kids.py myself: 9 passed in 1.77s. (3) NEAR MISS: an implementation that union-merges the whole conflicted FILE (rather than just the Agent Notes block) would satisfy 'union' and corrupt the body; and one that runs the suite before staging all conflicts resolved would report green on partial bytes. Both are excluded by the code I read. (4) DEVIATION: none on the verdict. (5) FINDING I recorded here rather than hiding: the tested helper is currently DEAD CODE — brief.py's item 5 (kid 1) tells the parent to hand-roll git merge --no-ff and never names season.py merge-kids, so nothing would ever call this. That is not a falsifier of the hypothesis (all five falsifiers are killed: zero-leg branch refused, union keeps both notes, source conflict named, suite re-run on merged bytes, every test inside tmp_path) but it is a real integration gap, so kid 3 (experiment:a00-0242d99c-02b595) is dispatched to name the verb in the brief.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) Instructions said: NODE conflicts resolved by UNION of Agent Notes + higher-confidence verdict line, never a blind git apply --3way; the proof is FIXTURES ONLY (a temp repo with 3 kid branches). (2) The machine: cmd_merge_kids (season.py:1436) merges in order, refuses zero-ahead, runs the suite on the merged bytes and aborts on red before committing; _resolve_conflicted (1396) returns 3 for SOURCE conflicts and does NOT abort, so MERGE_HEAD survives; _resolve_node_conflict (1344) unions only the Agent Notes block and rewrites the verdict/confidence pair; I re-ran the 9 tests -> 9 passed. (3) Near miss: unioning the whole conflicted file satisfies the word 'union' and corrupts the body; running the suite before every conflict is staged reports green on partial bytes. (4) Deviation: kept 85 and did not demote — every falsifier the hypothesis names is killed and the code I read excludes both near misses. Recorded the integration gap (no caller names this verb) as a review note and dispatched experiment:a00-0242d99c-02b595 to close it.
<!-- THOUGHT:END -->
