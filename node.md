---
id: experiment:a00-f1812eb6-4ade63
mint_id: ecb39654e960447faedea9d13b673f80
type: experiment
parents:
  - hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:a00-f1812eb6-4ade63
  - experiment:a00-a041cdef-3b79fa
  - experiment:a00-ea0222b3-4ed78e
loop: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 292813cc0bb29209
season: 2
title: "EG.90 corrective: hypothesis names the cli.py landing commit e12a57722, cites all six proved children, and falsifier 3 runs green at fffb284f6"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f1812eb6-4ade63

## Experiment -- CORRECTIVE DH.EG.90 (closes mur-eg-19 EG.63-k1), text-only

Cut tip `fffb284f6`. 0 production lines, 0 test lines, 0 USD. Only git run: `git diff --numstat` reads.

| # | item | settled by | fix (write.py) |
|---|---|---|---|
| 1 | live state dated EG.63 | numstat below: cli.py changed in `e12a57722`, unchanged to `fffb284f6` | hypothesis body: `Live state (landed by commit e12a57722 ...)` |
| 2 | evidence_runs omit a041cdef + ea0222b3 | read both nodes: `verdict: proved`, code fix + wire test | hypothesis `set evidence_runs` = the 6 proved children (5 named in the review + 9a0bf8cb) + this node; count pasted below |
| 3 | falsifier 3 never run | full-checkout run at `fffb284f6`, pasted below: GREEN | FALSIFIER 3 bullet on the hypothesis. 9a0bf8cb row 4 annotated (not rewritten) |
| 4 | no line names the cli.py commit | `e12a57722` numstat vs `8005cdd06` numstat (node-only) | LANDING bullet on the hypothesis, both numstats pasted |
| 5 | numbers measured at final tip | NOT MET by the round: its ceiling block is one-operand (director close pastes the two-operand numstat below) | -- |

## Evidence (pasted)

```
$ git diff --numstat 8005cdd06^ 8005cdd06
110	21	.agi/nodes/experiment/a00-df914bba-114582.md
$ git diff --numstat e12a57722^ e12a57722
77	0	.agi/nodes/experiment/a00-a041cdef-3b79fa.md
9	7	extensions/agi/bin/cli.py
78	0	extensions/agi/tests/test_cli_claim_conjunct_scope.py
$ git diff --numstat e12a57722 fffb284f6 -- extensions/agi/bin/cli.py
(empty, rc=0)
```

Falsifier 3 (test_cli.py + test_heal_watch.py + test_dispatch.py, the node's named neighbourhood) plus the claim test and smoke, run from this full checkout at `fffb284f6`:
```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_cli_claim_conjunct_scope.py extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider --basetemp /tmp/eg90-f1812eb6
362 passed, 6 skipped, 55 warnings in 271.51s (0:04:31)
```
The 5 failures the reviewer saw in an extensions-only `git archive` extraction do not reproduce with `.agi/` present, so they were extraction artifacts as the reviewer suspected.

Ceiling, measured after the last edit to a tracked file (this node is untracked, so it is not listed):
```
$ git diff --numstat fffb284f6
6	2	.agi/nodes/experiment/a00-9a0bf8cb-864103.md
11	3	.agi/nodes/hypothesis/probe-gate-counts-claim-conjuncts-from-the-field-only.md
```
Production 0 · test 0 · USD 0. a00-df914bba-114582.md untouched (no item needed a change to it).

Director close (TMM.327, mur-eg-27 EG.90-k1 V1 V2): the block above is ONE-operand (base vs worktree) and omits this node. Two-operand, cut tip to the round's final tip 392f2ac1b (measured before this close's own commit, which it does not include):
```
$ git diff --numstat fffb284f6 392f2ac1b
6	2	.agi/nodes/experiment/a00-9a0bf8cb-864103.md
79	0	.agi/nodes/experiment/a00-f1812eb6-4ade63.md
11	3	.agi/nodes/hypothesis/probe-gate-counts-claim-conjuncts-from-the-field-only.md
```
Proved children of the hypothesis at 392f2ac1b, counted by command (never typed): SIX besides this node.
```
$ grep -l -x "  - hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only" .agi/nodes/experiment/*.md | xargs grep -l "^verdict: proved"
.agi/nodes/experiment/a00-7b5520ac-96a290.md
.agi/nodes/experiment/a00-9a0bf8cb-864103.md
.agi/nodes/experiment/a00-9f9aaacd-303434.md
.agi/nodes/experiment/a00-a041cdef-3b79fa.md
.agi/nodes/experiment/a00-df914bba-114582.md
.agi/nodes/experiment/a00-ea0222b3-4ed78e.md
.agi/nodes/experiment/a00-f1812eb6-4ade63.md
```

## Deviation from the brief
The TESTS line said run `test_bin_help_smoke.py` once. Item 3 named test_cli.py (plus its neighbourhood) as the probe that settles it, so it ran in the same single pytest invocation as the smoke. Smoke ran exactly once.

## OUTSIDE
- none.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director close (TMM.327) of mur-eg-27 EG.90-k1. EG.90's THOUGHT said the four review items were closed, but its table lists five and item 5 (numbers at the final tip) was not met: the ceiling block was one-operand and left out this node. This version pastes the two-operand numstat (fffb284f6 to 392f2ac1b) and the command that counts the proved children (six besides this node; the order seeded five and the round copied it). It marks row 5 NOT MET and fixes the count here and in two places on a00-9a0bf8cb. The verdict proved on the hypothesis is unchanged.
<!-- THOUGHT:END -->

## Agent Notes
EG.90 corrective text-only: hypothesis now names landing commit e12a57722 (cli.py 9/7) vs node-only 8005cdd06, evidence_runs add a041cdef+ea0222b3, falsifier 3 neighbourhood green at fffb284f6 (362 passed 6 skipped); numstat 6/2 + 11/3, 0 production lines
