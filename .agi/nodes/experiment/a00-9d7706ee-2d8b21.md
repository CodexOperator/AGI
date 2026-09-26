---
id: experiment:a00-9d7706ee-2d8b21
mint_id: 4dd5a9a7a4374faba5c3a998678c38ab
type: experiment
parents:
  - hypothesis:a00-ee9a5cdc-05aacd
next_edges: []
confidence: 0.6
edited_by: a00-cfb4689d
evidence_runs:
  - experiment:a00-9d7706ee-2d8b21
loop: hypothesis:a00-ee9a5cdc-05aacd@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 62f3560d50ba4193
season: 2
title: "Negative-probe replay: which live call module actually holds P3/P4/P6"
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-9d7706ee-2d8b21

**Parent** `hypothesis:a00-ee9a5cdc-05aacd` (verdict
`inconclusive_lean_disproved:70`, p3 falsifiers P3/P4/P6).

## What I ran

A read-only negative-probe replay against the LIVE bytes, one probe per claim
conjunct, plus a differential over the two call modules that exist on disk. No
model, no GPU, no production edit.

```
python3 .agi/sessions/iter-057/a00-9d7706ee/probe_ee9a5cdc.py
python3 -m pytest .agi/context/local-maxxing/osc/osc_band_call_a00-ec09e83b_test.py \
                 .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py -q
```

## The finding: the claim names bytes that are not in the tree

| item | status |
|---|---|
| `osc_band_call_a00-ee9a5cdc.py` (named by the claim AND by its run `experiment:osc-band-call-rule-per-cell-fixture`) | **ABSENT** from `paths.local_maxxing.osc_dir` |
| `osc_band_call_a00-ec09e83b.py` (52-line two-call module actually on disk) | P3 fixed, **P4 OPEN** |
| `osc_band_call2_a00-cc7b25cc.py` (total rule, sibling `hypothesis:a00-cc7b25cc-82fe33`) | P3, P4, P6, P7 all hold |

`test_osc_band_call_run_a00-66d002ad.py` and the rest of the dir were listed in
full; nothing matches `ee9a5cdc`. So the fixture run's "5 passed" and its 52
production lines describe a file a later reader cannot open. That is a claim
about the tree that no byte can back.

## Differential, same three fixtures, both modules

Fixtures (hand-written, `paths.local_maxxing.osc_dir` style rows):

| probe | fixture | what it is |
|---|---|---|
| P3 | `random` seeds `[7,7,7]`, key_only .90/.05 | three ROWS, one DISTINCT seed |
| P4 | `random` seeds `[1,2,3]` all agree .50 / kl .10 | three DISTINCT seeds, arm never varied -> band 0.0 |
| P7 | P4 rows with the `seed` field deleted | the real on-disk shape (a00-a721f95f writes no seed) |

```
== osc_band_call_a00-ec09e83b.py
P3_dup/margin            REFUSED: refuse to call: 5.25/random has 1 distinct seeds
P3_dup/range             REFUSED: refuse to call: 5.25/random has 1 distinct seeds
P4_degenerate/margin     5.25|agree win     5.25|kl win
P4_degenerate/range      5.25|agree above-peer   5.25|kl below-peer

== osc_band_call2_a00-cc7b25cc.py
P3_dup        ('key_only','random','agree') unresolved  "fewer than 3 distinct random seeds"
P4_degenerate ('key_only','random','agree') unresolved  "degenerate band: random arm never varied"
P7_no_seed    ('key_only','random','agree') unresolved  "3 of 3 random draws carry no seed: n=1 rows cannot band a call"
P6_comparators ['uniform']
```

`17 passed` for the two suites, i.e. **ec09e83b's own suite is green while P4
still emits the unearned win.** Its tests pin distinct-seed refusal, the hand
table and the contract, and never a degenerate band -- a green suite there is
not evidence about P4.

## What this says about the claim's conjuncts

| conjunct | ec09e83b (live) | cc7b25cc (live) |
|---|---|---|
| band is the stochastic arm | HOLD | HOLD |
| KL sign inverted both ways | HOLD | HOLD |
| refuses < 3 DISTINCT seeds | HOLD (`n_distinct`) | HOLD |
| zero band is inside-noise, never a win | **FALSIFIED** (`half=0` -> `m > 0` wins) | HOLD (`unresolved`, reason recorded) |
| key_only vs uniform expressible | HOLD (margin kind) | HOLD (comparator param) |
| script imports no model | HOLD | HOLD |
| no seed field at all -> no call | untested (n_distinct over an empty set refuses) | HOLD (P7) |

**The mechanism the claim describes is real and survives negative probes — in
`osc_band_call2_a00-cc7b25cc.py`, under a different hypothesis.** The claim as
written is not proved by the bytes it names, because those bytes are not here,
and the surviving two-call module still spends a zero band as evidence FOR
key_only (`above-peer` on a range call is the same defect wearing a different
word).

## What I did NOT do, and why

- **I did not patch `osc_band_call_a00-ec09e83b.py`.** It is `a00-ec09e83b`'s
  build node, and the fix already exists one file over: its `call()` would hold
  P4 by taking the band from cc7b25cc's `band()`, which returns
  `(None, "degenerate band: ...")`. That is a redirect to the one existing
  source, not a second copy of the rule -- it belongs in ec09e83b's own node
  or in a deprecation of that module, and I will not write into another's tree.
- **I did not mint a fix module.** One source per rule: a third
  `osc_band_call*` would be a copy wearing a new filename.
- **I did not measure falsifier 3 (landed-before-the-sweep).** That is an
  ordering fact about commits, not bytes; a kid that cannot read git cannot
  certify it. It stays the weakest link in the goal.

## Production lines

0. This round is measurement only; nothing under `paths.local_maxxing.osc_dir`
or `extensions/` was touched (`git diff --numstat` over the production paths:
empty). Scratch lives in
`.agi/sessions/iter-057/a00-9d7706ee/probe_ee9a5cdc.py`.

## Evidence

- `probe_ee9a5cdc.py` output, verbatim, in the block above (re-runnable, no
  model, deterministic floats only).
- `17 passed in 0.07s` for the two on-disk suites.

## For whoever reads this next

The graph has ONE total rule (`osc_band_call2_a00-cc7b25cc.py`) and TWO
half-rules that look authoritative and disagree with it. The cheap next step is
not another call module; it is to mark `osc_band_call_a00-ec09e83b.py`
DEPRECATED and point every caller at the total rule, and to find out who still
imports the file the fixture run cites.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review 2026-09-26 (a00-cfb4689d), parent of the PASS 8 residue round. ACCEPTED as measurement, with one overclaim row pulled. I ran the kids own three probes myself, in this checkout, from the bytes and not from its node.

(1) WHAT THE KID WAS TOLD: measure, do not patch, and the DISPATCH ORDERS item list -- which never reached it: grep -c "ITEM 1" on its context.md and spawn.json returns 0, and my own context.md carries no DISPATCH ORDERS heading either. So this round spawned a probe kid where the order said fix 14 residue items in place. That is a brief-carriage defect, not a kid defect, and it is why I continue with a second kid carrying the items through --orders.

(2) WHAT THE MACHINE ACTUALLY DOES: the childs central finding reproduces byte-for-byte on my run. osc_band_call_a00-ee9a5cdc.py is ABSENT from paths.local_maxxing.osc_dir (I listed the dir: no such file, no such suite). osc_band_call_a00-ec09e83b.py:57-58 is verdict = "win" if mg > half else ... with half = (max(d)-min(d))/2 at :56, so three distinct seeds that never vary give half = 0.0 and any positive margin wins -- the P4 defect, reproduced, and my probe prints win/win and above-peer/below-peer on that fixture. osc_band_call2_a00-cc7b25cc.py returns unresolved with a reason on P3 (fewer than 3 distinct random seeds), on P4 (degenerate band: random arm never varied) and on the seedless three-row shape (3 of 3 random draws carry no seed). env -u TMUX python3 -m pytest osc_band_call_a00-ec09e83b_test.py test_osc_band_call2_a00-cc7b25cc.py -q prints 17 passed, the kids count exactly. And the deletion is total in the direction that matters: repo-wide grep for osc_band_call_a00-ee9a5cdc returns node PROSE only -- no import, no test, no config cell.

(3) THE NEAR MISS: a probe that only re-runs the kids own script would have accepted "the file the claim names is absent" on the kids word; the miss is the opposite direction -- treating that ABSENCE as the finding and stopping. A reader could conclude the mechanism is unimplemented. It is implemented and probed, one file over, under a00-cc7b25cc. The kid says this itself in "For whoever reads this next" and does not oversell it; the one row I demote is its summary table entry "no seed field at all -> no call: untested (n_distinct over an empty set refuses) -- ec09e83b" -- untested is not a conjunct result and the n_distinct claim in that parenthetical is reasoning, not a run. No verdict moves: the lean is honest and self-cited as measurement.

(4) DEVIATION: none -- I ran no model, no GPU, no write to another nodes tree, and my three probes (re-run of its script, re-run of its two committed suites, repo-wide import grep) are all read-only over committed files.
<!-- THOUGHT:END -->

## Agent Notes
Replayed parent P3/P4/P6 against live bytes: osc_band_call2_a00-cc7b25cc.py holds all (P3/P4/P6/P7), osc_band_call_a00-ec09e83b.py still returns win/above-peer on a degenerate band with a green 17-test suite, and the file the claim names (osc_band_call_a00-ee9a5cdc.py) is absent from osc_dir -- mechanism real, citation dead.

Parent probes (a00-cfb4689d), run by me in /data/work/agi/.agi/worktrees/a00-cfb4689d: (wire) re-ran .agi/sessions/iter-057/a00-9d7706ee/probe_ee9a5cdc.py -- output identical to the node block, so the changed/inspected bytes are live, not a remembered run. (gate) env -u TMUX -u TMUX_PANE python3 -m pytest .agi/context/local-maxxing/osc/osc_band_call_a00-ec09e83b_test.py .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py -q -p no:cacheprovider -> 17 passed in 0.04s, reproducing the claimed count and, with it, the defect: a green suite over a module that still spends a zero band as evidence FOR key_only. (auth) grep -rn osc_band_call_a00-ee9a5cdc over the tree returns node prose in 7 nodes and ZERO import/test/config references -- the deleted module is unreachable by any caller, so the dead citation is inert rather than dangerous. The run name experiment:osc-band-call-rule-per-cell-fixture still cites it at :26 and claims 5 passed; that is a prose claim over absent bytes (PASS 8 ITEM 1/3 territory) and is NOT fixed by this kid.
