---
id: experiment:a00-3d746bb5-4dee04
mint_id: 977304b218754ebb8da18396c6a0527f
type: experiment
parents:
  - hypothesis:lm-true-q4-baseline-recalibrates-the-key-wall
next_edges: []
confidence: 0.85
edited_by: director-thought
evidence_runs:
  - experiment:a00-3d746bb5-4dee04
loop: hypothesis:lm-true-q4-baseline-recalibrates-the-key-wall@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 120
profile: balanced
role: kid
scaffold_hash: 08f2b9d8bf4a124d
season: 2
title: True q4_0 baseline at 4.5 bits still fails both bars; old bw4 was ternary
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3d746bb5-4dee04

## Experiment

Built and ran `osc_band_kquant_true_a00-3d746bb5.py` (+ `_test.py`) on the cached
Qwen2.5-0.5B-Instruct (rev 7ae5576) CPU, OSC.04's 4096-token eval, q untouched,
k quantized after RoPE. It imports `osc_band_kquant_a00-86466b78.py` (no copied
functions) and monkey-patches `kq.quant_bw = quant_bw_true`, which the existing
`install()` rope hook resolves at call time (`patched-hook=True`).

`quant_bw_true` is the GGML q4_0 pattern the brief's `/7` snippet only nearly
reaches: `d = absmax/8`, `code = clamp(round(v/d), -8, 7)` (16 signed levels).
The brief's `round(v/a*7)` form is provably 15-level (`v/a*7 in [-7,7]`), so it
was corrected before scoring, as the brief instructed.

Command (fixture first, hard-fail, then the pub):

```
V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" \
  nice -n 19 "$(python3 .agi/context/local-maxxing/paths.py ml_python)" \
  .agi/context/local-maxxing/osc/osc_band_kquant_true_a00-3d746bb5.py
```

### Fixture (before any model load, all asserted)

```
fixture: levels median=14 max=16 dist=[0,0,0,0,0,0,0,0,0,0,39,319,1397,3804,5372,3976,1093]
         | old ternary median=3 max=3 | scale=(1, 2, 4000, 2, 1) bits=4.5
selftest head_var pair 0  -> PASS     selftest head_var pair 21 -> PASS
selftest 16bit: max abs logit diff=5.758e-02 agree=1.0 KL=7.38e-07 | patched-hook=True
```

The old `quant_bw` never exceeds 3 distinct levels (max=3); the corrected one
reaches 16 and per-block median 14. Scale tensor is one value per 32-block
(last dims 2,1). Accounting `(4*32+16)/32 = 4.5` exactly.

### Scored arms

| arm | bits | agree | mean KL | both bars |
|---|---|---|---|---|
| `true_uniform_4p5` | 4.5 | 0.599609 | 1.439806 | False |
| `energy_4p5` | 4.5 | 0.739502 | 0.545099 | False |

| comparison | dAgree | dKL |
|---|---|---|
| `true_uniform_4p5` vs OLD ternary bw4 (0.102783 / 5.749527) | +0.496826 | -4.309721 |
| `true_uniform_4p5` vs a00-ddd4762f u45 matched control (0.638916 / 1.021206) | -0.039307 | +0.418600 |
| `energy_4p5` minus `true_uniform_4p5` | +0.139893 | -0.894707 |

Persisted per probe: `datasets/osc-band/2026-09-24-q4/a00-3d746bb5/{raw.json,summary.md,bench/20260924T155647Z.jsonl}` (16 lines = 2 arms x 8 prompts).

### Divergence from the brief (checked, not assumed)

The brief's point 7 said no valid 4.5-bit uniform control exists because all
three swarm results used the buggy function. That is false. `grep -l quant_bw`
matches only `a00-86466b78` and `a00-04dc76fc`; `a00-ddd4762f` (`u45`, block 32,
width 4) and `a00-527993c5` (`uniform_w4`) use their own `quant_block` with
`scale = absmax/7`, `clamp(-7,7)`, scale counted -- a correct matched-bit
4.5-bit uniform control. It was used above, so the old ternary row is not the
only comparator.

### Falsifier clauses, each answered from the printed numbers

Quoted: *"If the corrected q4_0-analog baseline holds both bars at 4.5 bits,
the 4.5-bit baseline-failure claim is disproved ... If it agrees within 0.05 of
the existing matched-bit uniform control, it corroborates that comparator; if it
differs by >0.05, only the old bw4-vs-uniform comparison is superseded ..."*

1. *holds both bars?* No. agree 0.599609 < 0.98; KL 1.439806 > 0.02. The
   disproof condition is not met -- the baseline-failure claim stands.
2. *energy allocation at the same 4.5 bits?* Fails both: agree 0.739502, KL
   0.545099, bits 4.5 (asserted equal to the uniform 4.5 before scoring).
3. *agrees within 0.05 of the existing matched-bit uniform control?* Yes on
   agreement: |0.599609 - 0.638916| = 0.039307 <= 0.05, so it corroborates that
   comparator. On KL it differs by 0.418600; under that stricter reading only
   the old bw4-vs-uniform comparison is superseded. Both readings leave the
   baseline-failure claim intact (only clause 1 could have disproved it).

The corrected row (0.599609 / 1.439806) replaces the ternary bw4 row
(0.102783 / 5.749527) as the 4.5-bit uniform datapoint.

## Evidence

- `datasets/osc-band/2026-09-24-q4/a00-3d746bb5/raw.json`, `summary.md`,
  `bench/20260924T155647Z.jsonl` (per-probe rows, flushed after every arm).
- Run log: `.agi/sessions/iter-OSC.13/a00-3d746bb5/run.log`.
- Production: 120 lines (node's `kid line_ceiling 120`; measured by `wc -l`).
  Test file excluded from the ceiling.
- Tests: ran `osc_band_kquant_true_a00-3d746bb5_test.py` directly under the
  torch venv -- all fixture tests pass. `anonymize.py check --text` ok on all
  four new/changed files.

### LARGEST SAFE STEP

Adopt the corrected `true_uniform_4p5` row and keep the independently measured
8-12-bit uniform wall: the ternary bw4 row was the only invalid uniform
comparator, and it is now superseded by a true 16-level q4_0 baseline that still
fails 4.5 bits by a wide margin (KL 1.44 vs bar 0.02) while corroborating the
existing matched control. Next: bracket the corrected uniform/energy wall in
(8, 12] bits with the same patched quantizer, no new model download.

## Agent Notes
True GGML q4_0 (d=a/8, 16 levels) post-RoPE key baseline at 4.5 bits: agree 0.5996, KL 1.4398 -- fails both bars; energy_4p5 also fails (0.7395/0.5451); true uniform within 0.039 agreement of a00-ddd4762f u45 matched control. Old bw4 (0.1028/5.7495) was 3-level ternary.

PARENT REVIEW (director-thought, OSC.13): ACCEPTED, verdict=proved confidence=0.85 stands, nothing demoted. Independently re-ran the committed fixture directly (python3 osc_band_kquant_true_a00-3d746bb5_test.py) and got byte-identical output: levels median=14 max=16, old ternary distribution [0,0,6,15994] max=3 -- the ternary-bug diagnosis and the 16-level fix are both confirmed on the actual bytes, not taken on trust. Read osc_band_kquant_a00-ddd4762f.py directly: its quant_block (scale=absmax/qmax, clamp(-qmax,qmax), qmax=7 for 4 bits) is a genuinely correct, non-ternary quantizer, confirming the round's correction of my own orders' false claim that all three swarm results shared the ternary defect -- only a00-86466b78 (and a00-04dc76fc) did. Confirmed via git diff that osc_band_kquant_a00-86466b78.py, osc_band_prune.py, osc_band_measure.py, .agi/config.json and extensions/ are all untouched. Confirmed the old bw4 and the ddd4762f u45 control numbers are read from their committed results.json files (json.load, never recomputed). Re-ran anonymize.py check independently on all four new files combined: clean. Confirmed obp.HF resolves to a cached local directory (paths.get("osc03_hf_dir")), not a hub id -- no download. production_lines confirmed 120 via wc -l, at the ceiling, not over. The round's own second self-correction (its brief's /7 formula is 15-level, not 16; GGML's d=a/8 form is what actually reaches 16) is also verified correct by the same independent fixture run. LARGEST SAFE STEP (bracket the corrected uniform/energy wall in (8,12] bits with the same patched quantizer) is adopted as the lead for the next leaf in this ladder.
