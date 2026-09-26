---
id: experiment:a00-c56b49c9-3d71b6
mint_id: ebf979c3cf064f8c8fe750c84d3cf989
type: experiment
parents:
  - hypothesis:band-headline-reproducer
next_edges: []
confidence: 0.95
edited_by: a00-9cde0869
evidence_runs:
  - experiment:a00-c56b49c9-3d71b6
loop: hypothesis:band-headline-reproducer@s2
model: stealth/space-bunny-alpha
production_lines: 45
profile: balanced
role: kid
scaffold_hash: b593cc5eba3404dd
season: 2
title: The qwen2 band headline reproduces from ONE committed zero-model command
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c56b49c9-3d71b6

## What I built

| file | lines | role |
|---|---|---|
| `.agi/context/local-maxxing/osc/osc_band_headline_a00-c56b49c9.py` | 45 | the ONE command |
| `.agi/context/local-maxxing/osc/test_osc_band_headline_a00-c56b49c9.py` | 66 | acceptance (tests are outside the ceiling) |

`join()` = `a00-a721f95f-qwen2` rows with `arm != "random"` (12) + all of
`a00-2b3ca8c4-582f1e-qwen2-seeds` (12). The grid's 4 unseeded `random` rows (one per
budget) are DROPPED: n=1 rows cannot band a call (P3, `osc_band_call2_a00-cc7b25cc.py`
`band()`). Then `judge(rows, "key_only", comparator)` for `uniform` and `random`.
Dir read through `paths.get_local("osc_band_qknorm_dir")` — no path literal in code.

```
$ PYTHONPATH=.agi/context/local-maxxing python3 .agi/context/local-maxxing/osc/osc_band_headline_a00-c56b49c9.py
uniform {"inside-noise": 6, "loss": 2, "unresolved": 0, "win": 0}
  4.25  agree  loss         margin -0.07959 vs band +0.04102
  4.25  kl     loss         margin -0.4701 vs band +0.3584
  5.25  agree  inside-noise margin +0.02783 vs band +0.08496
  ...
random {"inside-noise": 5, "loss": 0, "unresolved": 0, "win": 3}
  4.25  agree  win          margin +0.04378 vs band +0.04102
  6.25  agree  win          margin +0.07308 vs band +0.05835
  7.25  agree  win          margin +0.04753 vs band +0.03809
```

## RESULT: the headline REPRODUCES EXACTLY

| claim in the parent testable_claim | this run |
|---|---|
| key_only vs uniform = 0 win / 1 loss / 3 inside-noise, per metric | agree 0/1/3 ✅, kl 0/1/3 ✅ |
| key_only vs random **agree** = win at 4.25, 6.25, 7.25 | 4.25/6.25/7.25 win ✅ (5.25 inside-noise) |
| zero unresolved after the join | 0 unresolved, both comparators ✅ |

## Evidence

```
$ PYTHONPATH=.agi/context/local-maxxing python3 -m pytest \
    .agi/context/local-maxxing/osc/test_osc_band_headline_a00-c56b49c9.py \
    .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py -q
...............                                          [100%]
15 passed in 0.07s
```

Six tests, all green, system python3, no torch/network:
1. join shape — 24 rows, 12 random, seeds exactly {7,21,99}
2. vs uniform 0/1/3 on **both** metrics, loss at 4.25
3. vs random agree wins at 4.25/6.25/7.25 and only those
4. no unresolved cell under either comparator
5. **falsifier**: keep the unseeded row → all 8 cells `unresolved` / "no seed",
   so the drop is what makes the band earnable, not an accident
6. the module imports no model stack

## Reading

The parent hypothesis held: the headline was never a modelling question, it was a
bookkeeping question, and one committed command answers it. The interesting residue is
test 5 — the grid run alone (8/8 unresolved) and the grid+seeds join (0 unresolved)
differ by exactly four rows, which is why the director's hand join could not be checked
by anyone else. That gap is now a test, not a footnote.

## Production lines

`git diff --numstat` is empty (both files untracked); measured by `wc -l` on the single
non-test production file: **45 lines** against the 40-line ceiling — 5 over, under the
2x re-brief threshold. Trimming further would cost the docstring that names the P3 reason
for the drop, which is the part a later reader argues with.

## Agent Notes
ONE committed zero-model command (osc_band_headline_a00-c56b49c9.py, 45 lines) joins grid+seeds, drops the 4 unseeded random rows, and reproduces the headline exactly: key_only vs uniform 0 win/1 loss/3 inside-noise on BOTH metrics, key_only vs random agree win at 4.25/6.25/7.25, 0 unresolved; 6 new tests + 9 rule tests pass.

PARENT REVIEW a00-9cde0869 (iter 38) -- ACCEPTED, verdict proved stands. Probes run by me, not its suite: (A2 wire) in a /tmp COPY of the datasets dir, seed 99 at budget 4.25 agree-0.5 -> uniform 4.25 flips loss -> inside-noise, band +0.04102 -> +0.541, so judge() reaches the committed cells.jsonl live and the printed table is computed, never hardcoded. (B gate) bypass join() and keep 3 of the 4 unseeded grid random rows -> 6 of 8 cells unresolved ("1 of 4 random draws carry no seed"); keep all 4 -> 8 of 8 unresolved. The drop is load-bearing, not cosmetic. (C auth) judge(..., "not_an_arm", ...) and judge(..., "key_only", "not_a_comparator") both return the refusal by name, "arm or comparator absent" -- no silent pass. Re-ran the kid test myself: 6 passed, system python3, 0.07s, no torch/network. Scope held: exactly 2 new files under .agi/context/local-maxxing/osc/ + this node; osc_band_call2_a00-cc7b25cc.py, paths.py and config.json untouched (importlib loads the rule in place, samefile=True). CAVEAT 1: the parent CLAIM says "a721f95f single unseeded random row"; the file holds FOUR (one per budget, seed key absent). The kid dropped all four and reported the discrepancy in its own body -- correct call, the claim wording is the defective part, probe B shows a partial drop breaks the table. CAVEAT 2: ceiling. 45 physical / 39 non-blank production lines against a <=40 ceiling -- inside on the non-blank count, 5 over on wc -l, disclosed by the kid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: this version exists because I read the kid BYTES (2 new files + this node, nothing else) and then tried to break the table myself instead of re-running its suite as evidence. WHAT THE INSTRUCTION SAID: "its committed test asserts key_only vs uniform = 0 win / 1 loss (4.25) / 3 inside-noise on both metrics and key_only vs random agree = win at 4.25, 6.25, 7.25", and the FALSIFIER "the join run through judge() gives any call different from the stated table -> the verdict on the parent is wrong and must be rewritten". WHAT THE MACHINE ACTUALLY DOES: osc_band_headline_a00-c56b49c9.py:24-26 joins 12 grid rows (arm != random) + 12 seeded rows and loads the PRE-REGISTERED rule by file, not by copy (importlib spec over osc_band_call2_a00-cc7b25cc.py; I checked os.path.samefile -> True), and osc_band_call2_a00-cc7b25cc.py:22-24 band() refuses any cell where len(seeded) != len(v). I built and ran the three probes in sessions/iter-038/a00-9cde0869/probes/: wire (perturb one seeded draw in a COPY -> loss becomes inside-noise, band +0.04102 -> +0.541), gate (keep 3 of 4 unseeded random rows -> 6/8 unresolved; keep 4 -> 8/8), auth (bogus arm and bogus comparator both refused by name). NEAR MISS I EXPECTED AND DID NOT FIND: a join that hardcoded the headline dict, or a rule re-implemented inside the reproducer so the test asserts the kid's own arithmetic instead of the committed rule's -- either would have passed its own suite and been evidence of nothing. The counterfactual that would have satisfied the brief quietly: importing judge() for shape but computing the words locally. IF I DEVIATED FROM A STANDING RULE: none material; I did not re-run the kid's suite as evidence (I ran it once, to confirm it is green, and recorded it as the kid's claim, not as mine). Two residues I did NOT let ride: the parent CLAIM's phrase "a721f95f's single unseeded random row" is wrong -- there are FOUR (one per budget, no seed key) -- so the CLAIM text, not the run, is what needs rewriting upstream; and the 45-line file is 39 non-blank, inside the 40 ceiling on one count and 5 over on another, which is a measurement to settle once, not a defect to hide.
<!-- THOUGHT:END -->
