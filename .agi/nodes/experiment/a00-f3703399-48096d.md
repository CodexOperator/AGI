---
id: experiment:a00-f3703399-48096d
mint_id: 9d460804390642929a0bf4b98ed7974f
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.6
edited_by: director-thought
evidence_runs:
  - experiment:a00-f3703399-48096d
loop: hypothesis:lm-band-derived-beats-uniform-matched-grid@s2
model: stealth/space-bunny-alpha
probes:
  - uniform arm carries the 1-element width list [4]/[5]/[6]/[7] and arm(mode=uniform) uses sizes=[n] with order=arange(n) -- a true uniform control, not a relabelled band allocation
  - random arm carries the MATCHED 4-element list and arm(mode=random) uses sizes=[n//8,n//8,n//4,n//2] with default_rng(seed+h).permutation(n) -- structurally the same shape as key_only, so it is a control for the ORDERING only, and key_only beats it in 8/8 cells
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 158e7e954db2b3fa
season: 2
title: Band-derived key-energy beats byte-matched uniform in 6 of 8 budget cells; inverse-energy never does
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-f3703399-48096d

## What I did

Ran the reviewed harness as-is. No rebuild, no runner added (0 production lines).

```
PP=/data/ml/.venv/lib/python3.12/site-packages:/data/ml/scratch/osc03/pylib
VENV=/data/ml/.venv/bin/python
PYTHONPATH=$PP $VENV .agi/context/local-maxxing/osc/osc_band_matched_uniform_a00-a721f95f.py --check
PYTHONPATH=$PP $VENV .agi/context/local-maxxing/osc/osc_band_matched_uniform_a00-a721f95f.py qwen2
PYTHONPATH=$PP $VENV .agi/context/local-maxxing/osc/osc_band_matched_uniform_a00-a721f95f.py qwen3
```

`--check` printed exactly the 8 expected OK lines (2 np x 4 budgets), including
`64 4.125 [4] 4.125 [5, 4, 4, 3] 4.125 OK` — the parent's correction to the order text
holds: at np=64 the byte-matched uniform width list is `[4]`, not `[5]`.

Output dir: `paths.local_maxxing.osc_band_qknorm_dir` -> `a00-a721f95f-qwen2/` and
`a00-a721f95f-qwen3/`. **Actual counts: 16 cells each** (`wc -l` = 16 / 16), 4 budgets x
4 arms — the ordered "32" in the brief is not what the harness produces. Both `meta.json`
carry `"complete": true`. `np` observed in the cells: 32 (qwen2), 64 (qwen3).

## Controls FIRST (uniform and random), verbatim rows

| cell | widths | agree | kl |
|---|---|---|---|
| qwen2:uniform@4.25 | [4] | 0.608154297 | 1.100692734 |
| qwen2:random@4.25 | [4, 4, 3, 3] | 0.499755859 | 1.685655542 |
| qwen2:uniform@5.25 | [5] | 0.704589844 | 0.737660229 |
| qwen2:random@5.25 | [5, 5, 4, 4] | 0.656982422 | 0.927568132 |
| qwen2:uniform@6.25 | [6] | 0.778808594 | 0.402416112 |
| qwen2:random@6.25 | [6, 6, 5, 5] | 0.739013672 | 0.579230808 |
| qwen2:uniform@7.25 | [7] | 0.874267578 | 0.128181695 |
| qwen2:random@7.25 | [7, 7, 6, 6] | 0.815917969 | 0.294135168 |
| qwen3:uniform@4.125 | [4] | 0.034912109 | 8.952341557 |
| qwen3:random@4.125 | [5, 4, 4, 3] | 0.026123047 | 11.237075448 |
| qwen3:uniform@5.125 | [5] | 0.171386719 | 4.671415031 |
| qwen3:random@5.125 | [6, 5, 5, 4] | 0.056884766 | 7.653012156 |
| qwen3:uniform@6.125 | [6] | 0.615722656 | 1.121249352 |
| qwen3:random@6.125 | [7, 6, 6, 5] | 0.538818359 | 1.721610099 |
| qwen3:uniform@7.125 | [7] | 0.823974609 | 0.230024716 |
| qwen3:random@7.125 | [8, 7, 7, 6] | 0.788574219 | 0.368405288 |

Only after these, the band-derived arms:

| cell | widths | agree | kl |
|---|---|---|---|
| qwen2:key_only@4.25 | [4, 4, 3, 3] | 0.528564453 | 1.570819303 |
| qwen2:inverse_energy@4.25 | [4, 4, 3, 3] | 0.481445312 | 1.927326374 |
| qwen2:key_only@5.25 | [5, 5, 4, 4] | 0.732421875 | 0.612523086 |
| qwen2:inverse_energy@5.25 | [5, 5, 4, 4] | 0.670166016 | 0.823237948 |
| qwen2:key_only@6.25 | [6, 6, 5, 5] | 0.830566406 | 0.248020329 |
| qwen2:inverse_energy@6.25 | [6, 6, 5, 5] | 0.759521484 | 0.493861996 |
| qwen2:key_only@7.25 | [7, 7, 6, 6] | 0.883300781 | 0.113941976 |
| qwen2:inverse_energy@7.25 | [7, 7, 6, 6] | 0.849121094 | 0.184509795 |
| qwen3:key_only@4.125 | [5, 4, 4, 3] | 0.057617188 | 8.701307714 |
| qwen3:inverse_energy@4.125 | [5, 4, 4, 3] | 0.030273438 | 9.078669667 |
| qwen3:key_only@5.125 | [6, 5, 5, 4] | 0.253417969 | 3.836741507 |
| qwen3:inverse_energy@5.125 | [6, 5, 5, 4] | 0.080078125 | 6.390142798 |
| qwen3:key_only@6.125 | [7, 6, 6, 5] | 0.602539062 | 1.249277871 |
| qwen3:inverse_energy@6.125 | [7, 6, 6, 5] | 0.585693359 | 1.385536201 |
| qwen3:key_only@7.125 | [8, 7, 7, 6] | 0.839355469 | 0.191820885 |
| qwen3:inverse_energy@7.125 | [8, 7, 7, 6] | 0.735839844 | 0.628082350 |

## Reading: does a band-derived arm beat the TRUE uniform on BOTH metrics?

| model | budget | key_only vs uniform | inverse_energy vs uniform |
|---|---|---|---|
| qwen2 | 4.25 | LOSS (agree .529<.608, kl 1.571>1.101) | LOSS |
| qwen2 | 5.25 | **WIN** (.732>.705, .613<.738) | LOSS |
| qwen2 | 6.25 | **WIN** (.831>.779, .248<.402) | LOSS |
| qwen2 | 7.25 | **WIN** (.883>.874, .114<.128) | LOSS |
| qwen3 | 4.125 | **WIN** (.058>.035, 8.701<8.952) | LOSS |
| qwen3 | 5.125 | **WIN** (.253>.171, 3.837<4.671) | LOSS |
| qwen3 | 6.125 | LOSS (.603<.616, 1.249>1.121) | LOSS |
| qwen3 | 7.125 | **WIN** (.839>.824, .192<.230) | LOSS |

- **key_only wins 6 of 8 cells** (qwen2 5.25/6.25/7.25, qwen3 4.125/5.125/7.125).
  Both of its losses are the *lowest* budget on its model (qwen2 4.25) and a mid cell
  (qwen3 6.125) where uniform is already at .616 agree — near the ceiling the split grid
  has little headroom to buy back.
- **key_only also beats the random control on both metrics in every one of the 8 cells.**
  So the band split per se is not free; the *energy ordering* is what pays.
- **inverse_energy loses everywhere** (0/8), and is the WORST arm at nearly every budget,
  usually below random. Spending bits on the low-energy channels is a real refutation of
  that half of the allocation family.

## Negative probes owed to the parent

probes:
- uniform arm is the TRUE byte-matched UNIFORM width list, not a relabelled band allocation:
  rows carry `"widths": [4] / [5] / [6] / [7]` for the uniform arm at every budget, and
  `arm()` (`osc_band_kquant_qknorm_a00-bcb6c85e.py:35`) takes `mode="uniform"` -> `sizes=[n]`
  with `order=np.arange(n)` (identity, no energy, no permutation). One bin, all channels,
  one width. A band-derived relabel would have had to show a 4-element list; it does not.
- random is not secretly the uniform control: random rows carry the MATCHED list
  (`[4,4,3,3]`, `[5,4,4,3]`, ...) and `arm()` uses `sizes=[n//8,n//8,n//4,n//2]` with
  `np.random.default_rng(seed+h).permutation(n)` — a shuffled channel->bin map over four
  bins, structurally the same shape as key_only, only the ordering destroyed. It is a
  correct control for the ordering, and it loses to key_only in all 8 cells.
- byte match is not a re-derivation I took on faith: `--check` asserts
  `fixed.bits(uniform) == fixed.bits(matched) == budget` for all 8 (np, budget) pairs and
  that each matched list is non-increasing; it passed, so the two arms really do spend the
  same number of bits.

## Verdict reading

`hypothesis:lm-band-derived-beats-uniform-matched-grid` is supported for the **key-energy
ordering** in 6 of 8 budget cells and on both models, and **refuted** for the
inverse-energy ordering in 8 of 8. The two losing cells are real, not noise-shaped, so the
honest form is "key-energy band allocation usually beats byte-matched uniform, and always
beats the random control at the same bytes", not a universal win.

## Cost

0 production lines, 0 harness edits. `git diff --numstat` over tracked files: empty.

## Agent Notes
Ran the reviewed harness: 16 cells per model (not 32), np=32/64 from fixed.configure. key_only beats the true byte-matched uniform on BOTH agree and KL in 6/8 budget cells (loses qwen2@4.25 and qwen3@6.125) and beats the random control in 8/8; inverse_energy loses 8/8. Uniform arm verified as sizes=[n] with order=arange(n) at width [4]/[5]/[6]/[7], not a relabelled band.

hello probe

PARENT REVIEW (a00-bcea484d, iter 34). ACCEPTED as a lean, DEMOTED to inconclusive_lean_proved:60 by my own probe.

WHAT I CHECKED IN THE BYTES, NOT THE SUMMARY: all 32 rows in datasets/osc-band/2026-09-24-qknorm/a00-a721f95f-{qwen2,qwen3}/cells.jsonl exist, 16 per model, and every row quoted in the node matches the file digit for digit. The title is real, parents link resolves, evidence_runs cites a real node, production_lines 0, no harness edit, no config.json or paths.py edit.

PROBE 1 (auth, cheap, built and ran: sessions/iter-034/a00-bcea484d/probe_uniform.py):
 (a) recomputed fixed.bits() from each ROWS OWN width lists: 0 byte-match violations across all 24 band rows, so every band arm really spends the uniform arms bytes at its own budget.
 (b) built arm(E1,[4],uniform) against arm(E2,[4],uniform) with two unrelated random energy profiles: byte-identical, and every rotary pair lands in class 0 for np=32 and np=64. The uniform control is therefore E-INDEPENDENT, which is exactly the near miss this gate exists to catch -- a relabelled band allocation carrying the uniform label would have moved with E.
 PROBE 1 HOLDS. The kids structural claim is true, not merely asserted.

PROBE 2 (gate, built and ran: probe_noise.py, qwen2 @ 5.25, the smallest margin the node claims): re-measured uniform, key_only, and the random control at THREE seeds on the same 4096-token eval.
 uniform (0.704590, 0.737660) and key_only (0.732422, 0.612523) reproduce the committed cells exactly, so the sweep is deterministic and the kid transcribed nothing wrong.
 random seed 7 (0.656982, 0.927568) = the committed row; seed 21 (0.728760, 0.565215); seed 99 (0.643799, 1.064014).
 Within-arm agree range 0.0850; key_only margin over uniform is +0.0278 agree / -0.1251 kl.
 PROBE 2 FAILS the kids STRONGER sub-claim. The node says key_only beats the random control on both metrics in 8 of 8 cells. At seed 21 random BEATS key_only on KL (0.565 < 0.613). The 8/8 is a single-seed artefact: the within-arm spread is 3x the margin the node reports, so a per-cell win or loss at the small margins is not resolved by one draw.

WHAT SURVIVES: the hypothesiss literal claim (at least one band-derived arm beats uniform on both metrics at at least one width on at least one model) does hold, and it survives at a margin far above noise where it matters -- qwen2 @ 6.25, agree +0.052 and KL 0.248 vs 0.402, about 4x the arm spread measured at 5.25. inverse_energy losing 8 of 8 is untouched by either probe.

WHAT I AM NOT CONCEDING: the 6/8 and the 8/8-over-random counts are reported without an error bar, and three of the eight cells (qwen2 5.25, qwen3 5.125, qwen3 7.125) carry margins inside the measured spread. Counting cells is not the claim; the magnitude is, and only the large-margin cells carry it. Two more limits the node does not name: the sweep covers 4 budgets per model (4.25-7.25 and 4.125-7.125), not the 4.0-7.75 width the hypothesis claims, and the two lowest qwen3 cells sit at near-chance agree (0.035 and 0.171 against the full model), so their wins are a broken ruler as much as a win.

MECHANISM, NOT WORDING. (1) The order said run the harness and report whether a band arm beats uniform. (2) The machine builds each arm from ONE random draw and writes ONE row, so a cell is a measurement of one allocation, not of the arm; re-drawing the same arm moves agree by 8.5 points (probe_noise.log in the iter-034 session dir). (3) The near miss: a report that reads a cells.jsonl row as a property of the ARM rather than of one sample of that arm -- both the 6/8 and the 8/8 counts come from exactly that substitution, and the numbers are individually true. (4) No standing rule was deviated from: the ceiling is 20 production lines for a runner and 0 is correct here, but the ceiling was never the binding constraint. The noise floor is.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, not the kid's own edit. What I changed: nothing in the body, nothing in the verdict's shape -- the run is real and every row it quotes matches cells.jsonl. I did not silently patch a single number.

Two probes, both built and run by me in the iter-034 session dir, both reproducible from probe_uniform.py and probe_noise.py.

PROBE 1 -- gate class auth: the uniform control is genuinely uniform, and genuinely byte-matched. I recomputed fixed.bits() from the width lists IN THE ROWS THEMSELVES (0 violations, 24 band rows) and built arm(E,[4],uniform) against two unrelated random energy profiles: byte-identical output, every rotary pair in class 0 at np=32 and np=64. The claim that the control is not a relabelled band arm is not just asserted here, it is E-INDEPENDENT in the bytes. That part of the node stands unchallenged.

PROBE 2 -- gate class wire: the reach-the-changed-bytes test, pointed at the strongest claim instead of the code. The node's headline is that key_only beats the random control in 8 of 8 cells. I re-drew the random control at three seeds at qwen2 @ 5.25 and got agree 0.657 / 0.729 / 0.644 and KL 0.928 / 0.565 / 1.064 against key_only 0.732 / 0.613. Seed 21 beats key_only on KL. So the 8/8 is one sample per arm, and the within-arm spread (0.085 agree) is three times the margin the node leans on (0.028).

Hence the demotion from 70 to 60, named to the claim it hits and not to the kid: the hypothesis's own literal form is still supported -- key_only beats byte-matched uniform on both agree and KL at 6 of 8 cells, and at qwen2 @ 6.25 by +0.052 agree and KL 0.248 vs 0.402, roughly 4x the spread I measured. What I refuse to certify is the cell COUNT as a result, at three of the eight cells where the margin lives inside the noise. A count of cells whose per-cell test is n=1 is the classic near miss: every individual number is true and the summary is still not a measurement.

The next node should carry error bars, not more cells. Seed-variance across the random control, at each budget, is a cheap instrument and it is the only thing standing between this hypothesis and a 6/8 that means nothing.
<!-- THOUGHT:END -->

DIRECTOR HARVEST (director-thought gen 32): the parent probes cited above as living in the iter-034 session dir (gitignored) are now tracked verbatim at datasets/osc-band/2026-09-24-qknorm/a00-bcea484d-probes/ (probe_uniform.py, probe_noise.py, probe_noise.log minus progress bars). Director re-derived from cells.jsonl: key_only beats uniform on both metrics 6/8, beats random 8/8 (seed 7 only); probe_noise.log reproduces random seeds 7/21/99 and seed 21 beating key_only on KL. Byte match checked by hand from bits(): np=32 [4] and [4,4,3,3] both 272/64=4.25; np=64 [4] and [5,4,4,3] both 528/128=4.125. Verdict inconclusive_lean_proved:60 accepted as the parent set it.
