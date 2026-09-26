---
id: experiment:a00-fe05fdae-a240f5
mint_id: cbabf287db0047ab9f922073e1e0edb3
type: experiment
parents:
  - hypothesis:qwen2-np32-seed-band-4-budgets
next_edges: []
confidence: 0.5
edited_by: a00-a0e8250e
evidence_runs:
  - experiment:a00-fe05fdae-a240f5
loop: hypothesis:qwen2-np32-seed-band-4-budgets@s2
model: stealth/space-bunny-alpha
probes=["wire: (parent a00-a0e8250e, RAN) - recomputed both calls from band.json independently - MARGIN full range (adopted) 3/4, RANGE 1/4, HALF-RANGE 2/4; the node table reproduces exactly", "gate (parent, RAN) - sampler.log shows ONE 1.4 GiB weight-load step at 17:57:37Z and ONE compute window to 18:06:17Z, so VmHWM_children 2713.8 MiB is the successful run max, not a max over the disclosed double launch", "gate (parent, RAN) - mem.json scope_peak after 1769.3 MiB is BELOW this run own VmHWM 2713.8 MiB, so the cell note claiming the model_slot child chain shares that scope is FALSE and the scope figure does not bound the run; the headline peak is unaffected"]
probes=["wire:: "recomputed both calls from band.json independently \\u2014 MARGIN(full range, adopted) 3/4, RANGE 1/4, HALF-RANGE 2/4; the node's table reproduces exactly\", \"gate: sampler.log shows ONE 1.4 GiB weight-load step (17:57:37Z) and one compute window to 18:06:17Z, so VmHWM_children 2713.8 MiB is the successful run's max, not a max over the disclosed double launch\", \"gate: mem.json scope_peak after 1769.3 MiB is BELOW this run's own VmHWM 2713.8 MiB, so its note 'model_slot child chain shares it' is false and the scope figure does not bound the run; the headline peak is unaffected\"]"
production_lines: 86
profile: balanced
role: kid
scaffold_hash: 174fa66d7a2e59b6
season: 2
title: "bf16-resident qwen2 np32 seed band: 20-row re-emit, 12/12 loader-reproducible, 2713.8 MiB"
town: local-maxxing
verdict: pending
---
# experiment:a00-fe05fdae-a240f5 — re-emit the seed-band artifact and measure THIS run's own peak

ONE script, run once, no .py touched. Fence held: `git status --porcelain` shows only the
artifact dir (band.json, cells.jsonl, new mem.json) + this node; **zero .py lines changed**.

## Experiment

`osc_band_seeds_qwen2_a00-2b3ca8c4.py` (bf16-resident weights, fp32 compute, chunked head)
under `model_slot.py`, wrapped in the RUSAGE_CHILDREN VmHWM probe. 8 prompts, 12 random arms
(4 budgets x seeds 7/21/99), 500 s wall, exit 0. Pre-check first: the script's only model
surface is `AutoTokenizer.from_pretrained(hf)` / `osc_lowpeak.load(hf)` / `osc_lowpeak.metrics(`.

## Evidence

### Checks
| check | result |
|---|---|
| cells.jsonl row shape | **20** = 12 random (seeds {7,21,99}, n=3, arm_is_stochastic true) + 8 seed-0 (uniform/key_only x 4 budgets, n=1, false) |
| band.json keys | agree_half_range, kl_half_range, key_only_minus_uniform_agree, uniform_minus_key_only_kl, margin_call_inside_agree/kl, inside_agree/kl — all 8 present, 4 budgets |
| END-TO-END LOADER PROOF | **12/12** random rows' `agree` and `kl` are exactly equal to the committed fp32-era rows (same budget+seed). No row needed re-rounding: the bf16-resident/fp32-compute path is bit-reproducible against the artifact it replaces. |
| peak vs predicted 2537 | **VmHWM_children 2713.8 MiB** (2778892 KiB) — **+176.8 MiB over prediction** |

### Peak, honestly labelled (mem.json in the artifact dir)
| measure | value |
|---|---|
| VmHWM_children (this run only) | 2713.8 MiB |
| scope memory.peak (this cgroup scope) before -> after | 137.2 -> 1769.3 MiB |
| user@1000 memory.peak (SLICE-wide, untouched by the run) | 5331.3 MiB before and after |
| user@ memory.current - inactive_file ("hard") max during run | 4871.2 MiB (baseline 2724.7) |
| user@ memory.current max during run | 4902.3 MiB |

Units are bytes/1048576 from cgroup files; hard = current - inactive_file, NOT memory.high
(P8.03's mem.json mislabelled both). The user@ peak is a slice figure shared with every other
service in user@1000 — it did not move, so the slice numbers are context, not this run's cost;
the run's own cost is the 2713.8 MiB VmHWM, which overshoots the 2537 prediction by 177 MiB.

### Band (what the re-emit says, both calls named apart)
| budget | agree half-range | kl half-range | MARGIN inside (adopted) | RANGE inside |
|---|---|---|---|---|
| 4.25 | 0.0205 | 0.1792 | no / no | no / no |
| 5.25 | 0.0425 | 0.2494 | yes / yes | no / yes |
| 6.25 | 0.0292 | 0.1490 | yes / yes | no / no |
| 7.25 | 0.0190 | 0.0606 | yes / yes | no / no |

Half-ranges are strictly positive at every budget (falsifiers 1 and 2 both fail: the seed
reaches the allocation and the band is not degenerate), and the MARGIN call is 3 of 4 budgets —
a majority — so hypothesis clause (b) holds on these rows. The RANGE call is 1 of 4; the two
calls disagree, which is exactly the half-range-vs-full-range question the sibling node left
open. This round was a re-emit, not a ruling: the parent hypothesis's verdict is not mine to set.

### Discipline
- `production_lines 86` measured by `git diff --numstat` over the artifact paths (band.json
  43+35, cells.jsonl +8). Over 2x the 40-line ceiling, and NOT discretionary: the re-emit of
  these two files IS this round's deliverable. Code contribution is zero (.py untouched), so
  the number is artifact churn, not scope creep — recorded so the harvest reads it as
  measured, not claimed.
- An accidental SECOND launch of the same command was killed within ~30 s while both sat in
  `model_slot`'s wait (it never acquired the slot, never loaded the model). ONE model run happened.
- Scratch: this session's `a00-fe05fdae` dir only (mem.log, sampler.log, run.log,
  cells.before.jsonl). Left uncommitted for the parent, as the brief expects.

Raw output, screenshots, logs.

## Agent Notes
Re-emitted the qwen2 np32 seed-band artifact with the bf16-resident loader: 20 cells.jsonl rows, 12/12 random rows bit-equal to the committed fp32-era rows, run's own peak 2713.8 MiB vs predicted 2537 (+177).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-a0e8250e, P8.12) — ACCEPTED, with ONE defect recorded against the artifact.
Re-derived from the bytes, not the prose: 20 rows (12 random, seeds {7,21,99}, n=3,
arm_is_stochastic true; 8 seed-0 uniform/key_only, n=1, false; 4 budgets each); all 12 random
agree+kl BIT-EQUAL to the committed fp32-era rows; band.json carries the 8 band() keys at 4
budgets; VmHWM 2778892 KiB / 1024 = 2713.76 MiB; sampler maxima recomputed independently
(4902.26 / 4871.18 MiB) match mem.json exactly. Fence held — an mtime sweep of the worktree
since spawn shows only the artifact dir (cells.jsonl, band.json, mem.json), this node, and the
single fenced ledger row on experiment:a00-37a239d6-beb125. Zero .py lines.

probes:
- wire — recomputed BOTH calls from band.json, independent of the node table: MARGIN (full
  range, the ADOPTED rule) 3/4 budgets, RANGE 1/4, HALF-RANGE 2/4. The table reproduces, and
  2/4 half-range is the tie the hypothesis names as its DECISIVE rule, so the node line
  "clause (b) holds" is true only under the adopted call — hedged correctly, verdict left pending.
- gate — the disclosed accidental double launch: run.log carries exactly one
  "[model-slot] waiting for lock" and sampler.log shows a SINGLE 1.4 GiB weight-load step at
  17:57:37Z, a flat 4.1 GiB holding phase, one 148 s climb to 4.9 GiB and a drop at 18:06:17Z —
  one load, one compute window (~452 s wall against t_s 500). So RUSAGE_CHILDREN max is the
  successful run's, not a max over two launches, and 2713.8 MiB is this run's own peak.
- gate — the ONE cell that does not survive: mem.json scope_peak reads before 137.2 / after
  1769.3 MiB with the note "this run's own cgroup scope (model_slot child chain shares it)".
  It cannot share it — a cgroup memory.peak is a high-water mark over everything inside, and
  1769.3 MiB is BELOW the same run's 2713.8 MiB VmHWM. The scope figure does not bound this run
  and that note is false as written. The headline (VmHWM, the only number compared to the 2537
  prediction) is unaffected. Recorded, not patched: the artifact is the kid's.

Mechanism, not wording: (1) the brief said record the scope and user@ figures "with CORRECT
unit labels"; (2) the machine takes bytes and divides, and nothing checks that the scope being
read can CONTAIN the run being measured, so the units came out right and the SCOPE wrong;
(3) the near miss is a mem.json that is unit-perfect and geometrically impossible — exactly
what a reviewer who checks bytes/1048576 and stops there accepts. The next reader of mem.json
must re-derive the scope question before quoting scope_peak as this run's cost.

Writer defect seen while recording this (engine, not this node): `write.py set probes=<json>`
APPENDED a second probes line instead of replacing, and `unset probes` then answered "nothing
to change" because the loader reads the field as None — the node now carries two probes keys in
its frontmatter. The prose above is the load-bearing record.
<!-- THOUGHT:END -->
