---
id: experiment:a00-9d6cbbf0-63bfec
mint_id: ee6fe5e95ca8418389d77b3cfa64ece9
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.99
edited_by: a00-0b5cc10b
evidence_runs:
  - experiment:a00-9d6cbbf0-63bfec
  - experiment:a00-a7060fdc-f436eb
  - experiment:a00-e416bc28-0c9d1b
  - experiment:a00-6f40fad2-eca451
  - experiment:a00-72273745-0d44f3
loop: hypothesis:lm-band-derived-beats-uniform-matched-grid@s2
model: stealth/space-bunny-alpha
production_lines: 43
profile: balanced
role: kid
scaffold_hash: 6f2639b44f92e418
season: 2
title: Exact non-increasing allocator search with blocked harness
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-9d6cbbf0-63bfec

## Experiment

Implemented a fresh allocator script and test. `search(np, tag)` enumerates integer widths, filters on the authoritative `fixed.bits()`, and requires `w0 >= w1 >= w2 >= w3`; paired `[a,a,b,b]` solutions are preferred before minimum gap. The script imports the existing `arm`, `bits`, `install`, and `forward` implementation unchanged and persists each cell to an append-only JSONL file with widths, bits, agreement, and KL.

The test covers all nine tags for both np=32 and np=64 and checks exact accounting (0.01 tolerance), non-increasing direction, and the np=32 4.5-bit cross-check. All 3 tests pass.

## Harness check and stopping decision

The required Qwen2.5 check ran with `widths=[13,13,10,10]` (authoritative result: 11.75 bits, not 7.75). Actual held-out metrics were `agree=0.99462890625`, `kl=0.00011305001919481583`; expected was `0.991699/0.000489`. The mismatch is material, so the sweep was correctly not launched. No 72-cell result is claimed; all sweep cells remain pending.

Search output (paired-shape preference):

- np=32: 4.0 `[3,3,3,3]`, 4.5 `[5,5,3,3]`, 5.0 `[4,4,4,4]`, 5.5 `[6,6,4,4]`, 6.0 `[5,5,5,5]`, 6.5 `[7,7,5,5]`, 7.0 `[6,6,6,6]`, 7.5 `[8,8,6,6]`, 7.75 `[9,9,6,6]`.
- np=64: 4.0 `[5,5,3,3]`, 4.5 `[4,4,4,4]`, 5.0 `[6,6,4,4]`, 5.5 `[5,5,5,5]`, 6.0 `[7,7,5,5]`, 6.5 `[6,6,6,6]`, 7.0 `[8,8,6,6]`, 7.5 `[7,7,7,7]`, 7.75 `[8,8,7,7]`.

## Evidence

- `test_osc_band_derived_a00-9d6cbbf0.py`: `3 passed`.
- Production script: 43 lines; test: 13 lines (under the 150-line production ceiling).
- Anonymize check: `ok`.

## Status

Pending, blocked by the required harness mismatch. The next run should diagnose the harness discrepancy before measuring the random-control sweep.

## Agent Notes
Exact non-increasing search and 18-combination test pass; required Qwen2.5 harness check mismatched (actual 0.99462890625/0.00011305001919481583 vs expected 0.991699/0.000489), so sweep was not launched and all 72 cells remain pending.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said to prove the allocator and run the full grid. The machine evidence is incomplete: the fresh search script does enumerate non-increasing integer widths and uses fixed.bits(), but the required Qwen2.5 harness result is a material mismatch (0.99462890625/0.00011305001919481583 versus 0.991699/0.000489), and the script therefore correctly refuses to launch the 72 cells. The near miss is to accept the unit test as proof while silently ignoring the held-out harness mismatch. Independent parent probe: pytest collection in this checkout fails before tests with ModuleNotFoundError: numpy, so the claimed 3-pass result is not independently re-derived here; this supports pending rather than a stronger verdict. No deviation from the review rule.
<!-- THOUGHT:END -->

Parent review: accepted the pending experiment as a correctly blocked result; demoted no prior evidence. probes: auth=not applicable; gate=required Qwen2.5 harness mismatch blocks sweep; wire=pytest collection could not reach the changed module because numpy is unavailable in the parent environment, so live wire verification is unresolved. Grid completeness is not claimed: 0/72 cells, pending diagnosis.
