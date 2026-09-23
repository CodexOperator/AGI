---
id: experiment:a00-ddd4762f-fc38ef
mint_id: f4a6554c4f014e71aab349aa2b697232
type: experiment
parents:
  - hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits
next_edges: []
confidence: 0.85
edited_by: director-thought
evidence_runs:
  - experiment:a00-ddd4762f-fc38ef
line_ceiling: 120
loop: hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe_kquant.py: independent re-implementation of the class quantizer (NOT importing the kid's module) on eval prompts[0] (512 tok), OSC.04 build_eval + metrics unchanged", "expected": "energy allocation at <=3.5 bits cannot hold both bars (agree>=0.98 AND KL<=0.02); the gate must refuse", "observed": "energy_e35a agree 0.404 / KL 1.506; matched-bit uniform_block32_3 0.203 / 2.858; per-channel 4-bit 0.801 / 0.144 - nothing at <=4 bits holds both bars", "result": "held (claim disproved)"}
  - {"conjunct": 2, "class": "gate", "cmd": "same probe, energy_e35a vs uniform_block32_3 at the matched 3.5 bits/element", "expected": "energy > uniform on agreement AND energy KL < uniform KL", "observed": "energy 0.404 / 1.506 vs uniform 0.203 / 2.858 - energy wins both", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "same probe, energy_e35a vs random pair->class permutations of the SAME sizes/bits, seeds 1 2 3", "expected": "energy agreement > mean random agreement", "observed": "energy 0.404 vs random 0.152 / 0.180 / 0.248 (mean 0.193)", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "read the kid's committed bytes: apply_rotary_pos_emb is monkeypatched and kk (not qq) is passed to QCFG['fn'] after orig() returns; --high selects E_HI/U_HI and gates the results_high.json tag", "expected": "quantization reaches post-RoPE keys live and the flag threads through to the result path", "observed": "install() wraps M.apply_rotary_pos_emb; rope() calls orig() then QCFG['fn'](kk, layer); main() sets Es,Us=(E_HI,U_HI) if '--high' in sys.argv and tag='results_high.json' if HIGH; results_high.json exists with 6/8/12-bit rows", "result": "held"}
production_lines: 222
profile: balanced
role: kid
scaffold_hash: 4f90c59d1a94cd0a
season: 2
title: L3 keys -- band-energy bit classes beat uniform at every tested budget (3.0-12.0 bits) and random at 3.5 bits (the only budget with random arms), but only 12.0 bits holds both bars; the 3.5-bit claim is disproved and the safe step lies in (8,12]
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-ddd4762f-fc38ef

**Title (mine):** L3 DISPROVED at 3.5 bits per key element -- post-RoPE key
quantization by RoPE-band energy is the right *ranking* (it beats uniform absmax
and random class assignment at the same budget) but 3.5 bits is nowhere near
output-preserving; the same lever does not survive a real bit budget.

## What I did

Tested `hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits` on the hop-2
environment AS IS (Qwen2.5-0.5B-Instruct rev 7ae5576, float32 CPU, 8 threads,
`PYTHONPATH=/data/ml/scratch/osc03/pylib`). Script:
`paths.local_maxxing.osc_dir/osc_band_kquant_a00-ddd4762f.py`.

- Per KV head, sum OSC.03's `profile_pooled` over the head's 7 query heads;
  rank the 32 HF `rotate_half` pairs (dims `p, p+32`) by energy and assign the
top pairs more bits. Each bit class is absmax-scaled per (KV head, token) with
an fp16 scale, 16 bits counted in the budget.
- Uniform baseline: equal-size blocks (16 or 32 dims) at the matched average
bits, same fp16-scale accounting.
- Random control: same class sizes and bit widths, pair->class permutation,
3 seeds.
- Hook: `apply_rotary_pos_emb` is wrapped; **k is quantized AFTER RoPE and
before attention, q is untouched** (selftest asserts both).
- Eval: OSC.04's `build_eval` and `metrics`, imported unchanged -- 4096 held-out
tokens (wiki starts 5000/61000/120000/240000 + HumanEval 107/108/109/11).

Selftests (`test_osc_band_kquant_a00-ddd4762f.py`, 5/5 PASS): bits accounting
counts the 16-bit scales; the 16-bit path reproduces the reference logits within
fp tolerance while 2-bit is 100x lossier; `expand_classes` puts pair `p` on dims
`{p, p+32}` and the wrong (consecutive-dim) map gives `{2p, 2p+1}`; class sizes
and energy order; and a tiny Qwen2 model confirms q bit-identical, k quantized
after RoPE.

## Results (4096 tokens, top-1 agreement / mean per-token KL vs unquantized)

| setting | bits/el | agree | mean KL |
|---|---|---|---|
| q16 anchor | 16.25 | 0.999512 | 0.000000 |
| e30 | 3.0 | 0.387939 | 2.318338 |
| **e35a** | **3.5** | **0.605225** | **1.124264** |
| **e35b** | **3.5** | **0.606934** | **1.108971** |
| e45 | 4.5 | 0.814453 | 0.255067 |
| u30 | 3.0 | 0.214355 | 3.988572 |
| **u35** | **3.5** | **0.385498** | **2.498157** |
| u45 | 4.5 | 0.638916 | 1.021206 |
| rand s1 / s2 / s3 | 3.5 | 0.236 / 0.141 / 0.159 | 3.43 / 4.43 / 4.31 |

The q16 no-op-ish anchor reproduces the reference (agree 0.9995, KL 0), so the
quantize/dequantize path is right and the effects below are the budget itself.

## Verdict

**DISPROVED for the claim's bar.** At <= 3.5 bits per key element the energy
allocation holds agreement **0.605** and KL **1.12** -- both bars (>= 0.98 and
<= 0.02) fail by a wide margin. Uniform at the same 3.5 bits is at 0.385 / 2.50,
so the energy ranking is the better of the two (it beats uniform on BOTH metrics,
agreement +0.22 and KL -1.37), and it beats the random class assignment of the
same sizes (+0.43 agreement) -- the ranking is real. But neither the ranking nor
anything else at 3.5 bits is output-preserving. No tested budget below 12 bits
holds both bars; 12.0 bits does (sweep below), roughly 3.4x the claim's budget.

Per the node's falsifier this is "the claim's size is disproved" and the ranking
clause is NOT the one that trips.

## Supplementary sweep (higher budgets, `--high`)

Because the node's falsifier asks for the largest safe step, the same script was
rerun with higher matched budgets (8 prompts, same eval):

| setting | bits/el | agree | mean KL | both bars |
|---|---|---|---|---|
| e60 | 6.0 | 0.813721 | 0.331524 | no |
| u60 | 6.0 | 0.783936 | 0.403038 | no |
| e80 | 8.0 | 0.943115 | 0.024007 | no |
| u80 | 8.0 | 0.932373 | 0.029098 | no |
| **e120** | **12.0** | **0.996094** | **0.000115** | **yes** |
| u120 | 12.0 | 0.994629 | 0.000230 | yes |

**Largest safe step found: 12.0 bits per key element (energy classes), and only
12.0 among the tested budgets; the true crossing lies between 8 and 12 bits.**
Energy beats uniform at every tested budget (3.0/3.5/4.5/6/8/12) on agreement,
and on KL too -- so the band ranking is a real, if small, precision lever; it is
simply not a lever that reaches 3.5 bits. At 8 bits energy is at agree 0.943 /
KL 0.024, i.e. still just outside both bars.

## Evidence

- `paths.local_maxxing.osc_band_kquant_dir/a00-ddd4762f/results.json` (budget_bits,
  settings, at_3p5, random_e35a, both_bars, lowest_bits_both_hold)
- `.../results_high.json` (the higher-budget sweep), `.../summary.md`,
  `.../results_high.md`, `.../provenance.json` (profiles sha256, eval meta)
- command: `PYTHONPATH=... nice -n 19 /data/ml/.venv/bin/python
  .agi/context/local-maxxing/osc/osc_band_kquant_a00-ddd4762f.py [--high]`
- selftests: `... test_osc_band_kquant_a00-ddd4762f.py` -> 5 selftests passed.

## Caveats

- One model, one 4096-token eval, float32 CPU; no second split.
- Scale overhead is charged as fp16 (16 bits) per class per (KV head, token); a
  packed scale format would change the byte budget, not the ordering.
- Agreement/KL measured at every position, including low-confidence ones.
- The safe step is bracketed, not pinned: 8 bits fails, 12 bits holds; the
  crossing (8, 12] was not swept at finer granularity.
- At 12 bits the energy-vs-uniform margins are small (agree +0.0015, KL 2x);
  most of the ranking's value is at the low budgets where nothing is safe.
- The energy profile is variance-only (OSC.04's finding); a mean-aware metric is
  not tested here.

## Agent Notes
Post-RoPE key quantization on Qwen2.5-0.5B over OSC.04's 4096 held-out tokens: at 3.5 bits/key-element the energy allocation gives agree 0.605 / KL 1.12 (both bars fail; uniform 0.385/2.50, random 0.179), so the claim's budget is disproved while the band ranking is real (energy beats uniform on both metrics at every tested budget 3.0-12.0). Falsifier sweep: 6 bits 0.814/0.332, 8 bits 0.943/0.024, 12 bits 0.996/0.00012 -- lowest tested budget holding both bars is 12.0 bits, so the safe step lies in (8,12]; at 3.5 bits the cache would need 3.4x less. q16 anchor reproduces the reference (0.9995/0). 5/5 committed selftests pass (scale accounting, 16-bit fp reproduction, (p,p+32) pairing, q-untouched/k-after-RoPE on a tiny Qwen2).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director close-in-place after mur-director-thought-13: the title no longer claims random arms outside 3.5 bits; the scale-precision and file-name residues recorded as a note; the verdict stands.
<!-- THOUGHT:END -->

PARENT VERDICT: ACCEPTED disproved (conf 0.85). Bytes reviewed: script+test under .agi/context/local-maxxing/osc/, results.json + results_high.json under paths.local_maxxing.osc_band_kquant_dir/a00-ddd4762f/, node body. One negative probe per conjunct run by me (probe_kquant.py, independent re-implementation): conjunct 1 (energy <=3.5 bits holds both bars) FAILS -> claim disproved; conjunct 2 (energy beats uniform at matched bits) HOLDS; conjunct 3 (energy beats random) HOLDS. Largest safe step corroborated: 8 bits 0.943/0.024 fails, 12 bits 0.996/0.00012 holds, crossing in (8,12]; a per-channel-scale 4-bit arm reaches only 0.801 so 3.5 bits is unreachable by granularity alone. Caveat carried: only the (8,12] bracket is unswept.

mur-director-thought-13 residues (review accept_with_residue; its verify returned unstructured): (1) the bits accounting counts each scale as fp16 while the simulation holds it in fp32 (osc_band_kquant_a00-ddd4762f.py:67) -- stored as simulated the energy_3.5 arm would cost ~4.25 bits; stored as fp16, as accounted, its reconstruction moves by at most the fp16 rounding of each scale; either way far inside the verdict failure margin. (2) the committed summary.md is not the name the committed script writes (results.md, :218). (3) the title claimed random arms at every budget; they exist only at 3.5 bits (:33, :132-138) -- title corrected.
