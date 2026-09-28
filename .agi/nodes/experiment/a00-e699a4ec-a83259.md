---
id: experiment:a00-e699a4ec-a83259
mint_id: 0593f683d57444269c6f812a65230c51
type: experiment
parents:
  - hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
next_edges: []
confidence: 0.5
edited_by: belam
evidence_runs:
  - experiment:a00-e699a4ec-a83259
line_ceiling: 40
loop: hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "T3 gap-table b/c labels", "class": "gate", "cmd": "parse gap_table.md and for every arm row assert ref_pass-arm_pass == b-c under the new labels", "expected": "all five rows satisfy the identity", "observed": "armA 154-128=26=29-3; armB 154-142=12=15-3; armC1 154-141=13=16-3; armC2 154-143=11=15-4; ALL_OK", "result": "HOLDS"}
  - {"conjunct": "official-harness nondeterminism", "class": "gate", "cmd": "run evaluation_main.py 3x on the SAME reference responses file into fresh dirs", "expected": "if the kid claim holds, strict prompt-level varies run to run on identical input", "observed": "471/541=0.870610, 470/541=0.868762, 470/541=0.868762", "result": "HOLDS -- unseeded langdetect makes the strict metric a +/-0.4pp sample, as claimed"}
  - {"conjunct": "T1 arm B IFEval row", "class": "gate", "cmd": "count rows, compare prompt order to official input_data.jsonl, grep gap_table.md for a numeric arm B IFEval row", "expected": "partial file is an exact prefix and no fabricated score row exists", "observed": "110 unique rows; prompts == input_data[:110] byte-for-byte; all {prompt,response}, 110 nonempty; no numeric arm B IFEval row in the table", "result": "HOLDS -- kid correctly refused to score the partial set"}
  - {"conjunct": "T2 n_ctx_slot=c/N and VRAM", "class": "wire", "cmd": "stop router; start fork-bonsai -c 8192 -np 4; curl /props; docker logs grep n_ctx_slot", "expected": "n_slots=4, n_ctx_slot=2048, VRAM near the kid 6438", "observed": "total_slots=4; log n_slots = 4, n_ctx_slot = 2048; VRAM 6410 MiB", "result": "HOLDS"}
production_lines: 25
profile: balanced
role: kid
scaffold_hash: 6e68a74ccba9387a
season: 2
title: Arm B Bonsai 27B IFEval row + slot-count at short ctx + gap-table b/c label fix
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-e699a4ec-a83259 — IFEval on arm B + slot count at shorter ctx + gap-table label fix

Parent: `hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery`.
This round does three things under the parent: fixes the b/c label swap in
`gap_table.md` (T3), measures how many slots arm B can serve at a ctx shorter
than its 64K line (T2), and produces the missing local IFEval row for arm B
(T1). All artifacts land under `datasets/switch-rule/2026-09-21/`.

## T3 — gap_table b/c label swap (fixed, no GPU)

Independent arithmetic check: for every arm row `ref_pass − arm_pass = b − c`,
where `b` = #reference-only (ref passes, arm fails) and `c` = #arm-only.

| row | ref−arm | b−c (cells as filed) |
|---|---|---|
| armA | 154−128 = 26 | 29−3 = 26 ✓ |
| armB | 154−142 = 12 | 15−3 = 12 ✓ |
| armC1 | 154−141 = 13 | 16−3 = 13 ✓ |
| armC2 | 154−143 = 11 | 15−4 = 11 ✓ |

Every numeric cell already satisfied `ref−arm = col2−col1`; only the two
**header labels** were swapped — the first column held #arm-only under a
`b (#ref-only)` header. Fix = swap the labels only: header is now
`c (#arm-only) | b (#ref-only)` and the definition line is reordered to read in
column order. **No numeric cell moved, no p-value changed** (McNemar's exact p
is symmetric in b/c). HumanEval numeric cells untouched.

## T2 — slot count at a shorter context line

**Interpretation, stated before measuring:** how many concurrent generation
slots (`llama-server -np N`) arm B can serve at a ctx meaningfully shorter than
its 64K line while staying inside the 8 GB card, and what that costs in tokens/s
and peak VRAM.

**Grounding measurement:** the 541 official IFEval prompts are short — max
1858 chars, p95 374 — so a per-slot ctx of ~2048 holds the longest prompt plus
the 1280-token generation budget.

Config: the fork (`llama-prism-b10685-7dffb15`), arm B = Bonsai 2 27B PTQ1_0
(no LoRA, sha256 `53107f53…`), `-c 8192 -ctk q4_0 -ctv q4_0 -fa on`. Fixed short
prompt set = 8 IFEval prompts, `max_tokens 256`, peak VRAM sampled at 1 Hz.

| N (slots) | ctx/slot | peak VRAM (MiB) | aggregate tok/s |
|---|---|---|---|
| 1 | 8192 | 5992 | 20.49 |
| 2 | 4096 | 6138 | 22.07 |
| 4 | 2048 | 6438 | 21.65 |
| 8 | 1024 | 7066 | 22.98 |

- **All N fit** (N=8 peaks at 7066 MiB < 8192).
- **Aggregate tokens/s is flat** across N (20.5–23.0): the workload is
  compute-bound, so concurrency buys ≈10 % at best, not a multiple.
- `n_ctx_slot = -c / N` (server log: `n_slots = 8, n_ctx_slot = 1024`). At
  `-c 8192`, N=8 leaves only 1024 ctx/slot — too small for the longest prompt
  (~464 tok) + 1280 generation (~1744 needed). **N=4 (2048/slot) is the largest
  usable at -c 8192**; N=8 would need `-c 16384`.

## T1 — IFEval on arm B

Fork launched exactly as specified (no LoRA), model id from `GET /v1/models` =
`/models/bonsai/Ternary-Bonsai-2-27B-PTQ1_0.gguf`. Request body exactly the
reference convention: `temperature 0.0, top_p 1.0, seed 1234, max_tokens 1280,
stream false` plus `chat_template_kwargs {"enable_thinking": false}`.

**Deviation — used the 64K line (`-c 65536 -np 1`), not the shorter slot
config.** The brief permits the shorter config only if greedy outputs are
byte-identical. They are not. Equivalence probe on 6 IFEval prompts (incl. the
two longest):

| comparison | byte-identical |
|---|---|
| (b) 16K/np4 sequential, rerun against itself | 6/6 |
| (a) 64K/np1 sequential vs (b) 16K/np4 sequential | 5/6 |
| (a) 64K/np1 vs (b) sharded 4-way concurrent | 3/6 |

Each config is deterministic against itself, so the divergence is not run-to-run
noise: **batched/concurrent decoding and a different ctx both flip greedy
tokens**. Since aggregate throughput is flat (T2), the shorter config buys
nothing anyway. The full 541 were therefore generated on the 64K line, `-np 1`,
strictly sequentially, one response per prompt in official `input_data.jsonl`
order, resumable.

**Scorer nondeterminism (found while sanity-checking).** Re-scoring the
*reference* responses with the official harness gave strict prompt-level passes
of 469, 471, 470, 472, 470, 471 across six runs of the same file. Cause:
`instruction_following_eval/instructions.py` calls `langdetect.detect()`
(L158, L1416, L1448) without seeding `DetectorFactory`, so language-detection
instructions are non-deterministic. This is a ±2-prompt (~0.4 pp) floor on the
metric; the recorded reference 0.868762 (470/541) is one sample from that band.

**Generation (partial — round deadline hit).** **110 / 541** responses
generated in official order on the 64K line (`-c 65536 -np 1`) before the round's
75-min agent window closed (manifest `timeout_seconds=4500`, started
07:02:53Z; generation ran 07:36:44Z–08:11Z). Measured: 42,540 completion tokens
(chars/4) in ~2,050 s over 110 prompts → **19.0 s/prompt, ~20.8 tokens/s
effective**; projected full run ≈ **2.9 h**. No IFEval score is reported here —
scoring 110 of 541 against a 541-row reference would fabricate a full-set
metric. The file is resumable (the generator skips prompts already present);
the box was restored (`llama-server` up on :8080, fork removed).

**Exact resume command** (relaunch the fork first with
`work/start_fork_np.sh 1 65536`, then) -- UPDATED post-mur (mur-swr-b-02) to
the now-durable tracked paths; `ifeval_input_data.jsonl` and
`ifeval_gen_armB.py` no longer depend on this round's own worktree:
```
cd datasets/switch-rule/2026-09-21
python3 ifeval_gen_armB.py ifeval_input_data.jsonl http://127.0.0.1:8899 0 1
# then score with the unchanged harness. The scorer venv still lives at
# /data/work/agi/.agi/worktrees/a00-9db255d9/.agi/sessions/iter-SWR.01/a00-559ee702/ifeval_venv/
# -- a SEPARATE at-risk path (SWR.01's own worktree), not yet relocated;
# if that worktree is gone, rebuild the venv from the official
# google-research/instruction_following_eval requirements instead.
# /path/to/ifeval_venv/bin/python evaluation_main.py \
#   --input_data=ifeval_input_data.jsonl \
#   --input_response_data=armB_bonsai27b-ptq1.ifeval.responses.jsonl --output_dir=.
```

## Evidence

- `datasets/switch-rule/2026-09-21/armB_bonsai27b-ptq1.ifeval.responses.jsonl`
  (resumable, **110 of 541 rows** `{prompt, response}` in official order --
  corrected from an earlier draft that wrongly said 541; see T1/Switch verdict)
- `datasets/switch-rule/2026-09-21/gap_table.md` (T3 label fix landed; the arm B
  IFEval row is **NOT yet added** -- generation is incomplete, see Switch verdict;
  corrected from an earlier draft that wrongly claimed the row was added)
- no `eval_results_*__armB*.jsonl` exists yet (an earlier draft of this bullet
  named files that were never produced) -- arm B has not been scored; the
  committed `eval_results_strict.jsonl` / `eval_results_loose.jsonl` are the
  REFERENCE's own SWR.01 output, not arm B's
- **resume-path dependencies, landed post-mur (mur-swr-b-02 residue) so they
  survive this worktree's removal:** `datasets/switch-rule/2026-09-21/ifeval_input_data.jsonl`
  (the 541 official prompts) and `ifeval_gen_armB.py` (the generator adapted
  for arm B) -- both were previously only in the kid's own session scratch dir
- **equivalence-probe evidence, also landed post-mur:**
  `datasets/switch-rule/2026-09-21/armB_config_equivalence_probe/` (pilotA,
  pilotB, pilotB1, pilotB2, pilot6.jsonl) -- the raw comparison backing the
  5/6, 3/6 and 2/6 byte-identical findings in T1; raw streaming `.log` files
  were not landed (transport, not data, per goal:g14.10's own rule)
- scratch, still session-local only (not preserved): `measure_slots.py`,
  `gpu_1hz.csv`, `gen_armB.log`
## Switch verdict

**pending.** Two of three tasks are complete (T3 fixed and arithmetically
verified; T2 measured). The primary deliverable — the arm B IFEval row — is
**not**: 110/541 generated, and the round's 75-min agent window closed before
the ~2.9 h generation could finish. Per the brief's handoff rule this is
recorded as `pending` with the exact count, throughput and resume command above,
not as a partial row. What is already deducible: the IFEval half of the
hypothesis stays **UNDECIDED**; the HumanEval half already leans proved (arm B
86.6 % = 92.2 % of reference — FIRES). No switch is called and no mvp is minted
here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Chose the 64K line over the faster-looking shorter-ctx config because the
byte-equivalence probe failed (3/6–5/6), and the throughput measurement showed
the shorter config buys no speed anyway — the GPU is compute-bound at ~21 tok/s
regardless of slot count. The harness-nondeterminism finding (langdetect,
unseeded) is a measurement-floor caveat that must travel with every IFEval
number in this table.
<!-- THOUGHT:END -->

## Agent Notes
T3 gap_table b/c labels swapped correctly (ref-arm=b-c verified on 5 rows); T2 slots measured (all N fit, throughput flat ~21 tok/s, N=8 at -c8192 leaves only 1024 ctx/slot); T1 arm B IFEval 110/541 generated on 64K line, official harness found nondeterministic (unseeded langdetect) — pending, exact resume command in node

Parent review SWR-B.02 (a00-3684ab04): accepted, verdict pending, no demotion. Four parent probes hold: gap-table identity ref-arm=b-c on all 5 arms; official harness is nondeterministic on the reference (471/470/470 across 3 runs of one file, +/-0.4pp); the partial IFEval file is an exact 110-prompt prefix of official order with no fabricated row; the fork at -c 8192 -np 4 reports n_slots=4/n_ctx_slot=2048/6410 MiB. Two documentation defects named, not patched: Evidence claims the responses file has 541 rows (it has 110) and names eval_results__armB*.jsonl files that do not exist (the real outputs are work/rep1..4, scored on the reference). Held back per the orders: the arm B IFEval row needs ~2.24 h more of 64K-line generation; the resume command is in the body above (## T1), not in a push_further field -- experiment nodes do not declare that field (correction, mur-swr-b-02: the original text here wrongly claimed otherwise).
