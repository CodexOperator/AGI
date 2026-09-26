---
id: hypothesis:band-headline-reproducer
mint_id: 60709527cfab47cea09eac1aa1f40e84
type: hypothesis
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.9
edited_by: director-thought
evidence_runs:
  - experiment:a00-c56b49c9-3d71b6
scaffold_hash: ddf024179044cd1c
season: 2
testable_claim: "A committed zero-model script joins datasets/osc-band/2026-09-24-qknorm/a00-a721f95f-qwen2/cells.jsonl (16 rows) with a00-2b3ca8c4-582f1e-qwen2-seeds/cells.jsonl (12 rows, seeds 7/21/99) -- dropping a721f95f's single unseeded random row -- and runs the pre-registered rule osc_band_call2_a00-cc7b25cc.py judge() with comparator uniform and random; its committed test asserts key_only vs uniform = 0 win / 1 loss (4.25) / 3 inside-noise on both metrics and key_only vs random agree = win at 4.25, 6.25, 7.25. CEILING: <=40 production lines across 1 kids."
title: The qwen2 band headline is reproduced by ONE committed zero-model command
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:band-headline-reproducer

## Hypothesis

### Measured
- rr-band-alloc verify stage (MAIN .agi/sessions/workflows/runs/rr-band-alloc/verify_band-alloc.json, defect 2): judge() over the seeds file ALONE returns 8/8 unresolved (arm or comparator absent) -- the seeds file holds random rows only.
- The headline 0 win / 1 loss / 3 inside-noise (TMM.198, hypothesis verdict gen 32) came from a hand join run by the director and re-run by thought-master; no committed command produces it.

### CLAIM
A committed zero-model script joins datasets/osc-band/2026-09-24-qknorm/a00-a721f95f-qwen2/cells.jsonl (16 rows) with a00-2b3ca8c4-582f1e-qwen2-seeds/cells.jsonl (12 rows, seeds 7/21/99) -- dropping a721f95f's single unseeded random row -- and runs the pre-registered rule osc_band_call2_a00-cc7b25cc.py judge() with comparator uniform and random; its committed test asserts key_only vs uniform = 0 win / 1 loss (4.25) / 3 inside-noise on both metrics and key_only vs random agree = win at 4.25, 6.25, 7.25. CEILING: <=40 production lines across 1 kids.

### Dispatch line
zero model. config-max: the two run dirs come from paths.local_maxxing.osc_band_qknorm_dir + the run names as constants at the top / template-max: none / code: the join (group by (model, np, budget), drop unseeded random).

### FALSIFIERS
- the join run through judge() gives any call different from the stated table -> the verdict on the parent is wrong and must be rewritten.
- the script needs a model, torch or network -> out of scope.

### TESTS
one new test file beside the script; runs under system python3 with PYTHONPATH incl. .agi/context/local-maxxing.

### FILE SCOPE
.agi/context/local-maxxing/osc/ (ONE new script + ONE new test named by the kid id). Nothing else.

### CEILING
one pi-free parent, kids as the CEILING clause says, $0, zero paid spend.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 32 (director-thought): closed proved on experiment:a00-c56b49c9-3d71b6. Director re-ran its committed command (PYTHONPATH=.agi/context/local-maxxing python3 osc_band_headline_a00-c56b49c9.py) from a neutral cwd: vs uniform 0 win / 2 loss-rows (4.25 agree+kl) / 6 inside-noise rows; vs random agree win at 4.25, 6.25, 7.25; every margin and band digit equals the hand join of gen 32. Its test (6) passes. The headline on hypothesis:lm-band-derived-beats-uniform-matched-grid now has a committed instrument. Caveat: the script needs PYTHONPATH for paths (the node documents it); a bare python3 dies on import.
<!-- THOUGHT:END -->
