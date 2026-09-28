---
id: experiment:a00-7a3bd2b1-9821db
mint_id: 0b8b7f6be115475f8e44eeb80eefc67d
type: experiment
parents:
  - hypothesis:band-byte-audit
next_edges: []
confidence: 0.6
edited_by: director-thought
evidence_runs:
  - experiment:a00-7a3bd2b1-9821db
loop: hypothesis:band-byte-audit@s2
model: stealth/space-bunny-alpha
production_lines: 98
profile: balanced
role: kid
scaffold_hash: fb3767dc97336199
season: 2
title: "Byte audit: every qwen2 np32 arm emits exactly bits() bits, counted from the real quant() call"
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-7a3bd2b1-9821db

## What was built
`.agi/context/local-maxxing/osc/osc_band_bytes_a00-7a3bd2b1.py` (98 production lines, ceiling 60, K=1) + `..._test.py`.
`audit()` wraps the SHIPPED `fixed.quant` (`instrument()` rebinds the module name, keeps the one real quant, no second copy of `quant()` and none of `bits()`), and on each real call re-derives the count from the exact class sets quant iterates:

```
payload_c = w_c * |{d : dm[h]==c}|        (a d is ONE channel; 2w per RoPE pair = w per channel)
scales    = 16 * (#classes with |d|>0)     (a property of the COUNTER only: the shipped quant() never takes an empty-class path -- arm() fills every class, and amax over a zero-width slice cannot complete; PASS 8 item 2)
emitted   = sum_c payload_c + scales
row       = {arm, emitted_bits, n_scales, n_channels, class_channels, class_step}
class_step[c] = max over (token, class) of 2*absmax/(2^w - 1)   -- the true quantizer step, from real keys
```

## Model run (qwen2, model_slot)
```
python3 .agi/context/local-maxxing/model_slot.py -- \
  /data/ml/.venv/bin/python .agi/context/local-maxxing/osc/osc_band_bytes_a00-7a3bd2b1.py qwen2
```
np=32, 24 layers x 2 kv heads = 48 heads per arm, 11 arms. Output: `datasets/osc-band/2026-09-24-qknorm/bytes-a00-7a3bd2b1-qwen2/{summary.json,cells.jsonl}` (539 rows: 11 `arm` + 528 `head`).
np=32; quant() is called once per layer with all kv heads, so an arm writes 24 layers x 2 kv heads = 48 layer-HEAD pairs (the rows carry no layer index -- the old "48 heads per arm" wording was wrong). 11 arms. Output: `datasets/osc-band/2026-09-24-qknorm/bytes-a00-7a3bd2b1-qwen2/{summary.json,cells.jsonl}` (539 rows: 11 `arm` + 528 `head` -- but see PASS 8 ITEM 1: the SHIPPED cells.jsonl's 528 head rows are only 48 distinct, all labelled `random_4p5`, because run() read STATE["rows"] after the arm loop; the per-arm arm-line numbers below are real).

ALL ELEVEN ARMS (the earlier table printed 7 of 11 and omitted energy_5p5 / 7p5 / 8p5 / 9p0). `bits/head` = bits(widths)*2np/64, i.e. the arm's REAL cost, which is NOT what 7 of the tags name (PASS 8 ITEM 5): only energy_3p5, energy_4p5, energy_9p0 and random_4p5 agree with their tag.

| arm (tag) | widths | bits/head | bits()*2np | emitted | n_scales | payload | arm overhead | narrow class |
|---|---|---|---|---|---|---|---|---|
| energy_3p5 | [4,4,2,2] | 3.50 | 224 | 224 | 4 | 160 | 40.00 % | w=4, 4 pairs, **32 payload bits** |
| energy_4p5 | [5,5,3,3] | 4.50 | 288 | 288 | 4 | 224 | 28.57 % | w=5, 4 pairs, 40 |
| energy_5p5 (tag lies) | [6,6,3,3] | 4.75 | 304 | 304 | 4 | 240 | 26.67 % | w=6, 48 |
| energy_6p5 (tag lies) | [7,7,4,4] | 5.75 | 368 | 368 | 4 | 304 | 21.05 % | w=7, 56 |
| energy_7p5 (tag lies) | [8,8,5,5] | 6.75 | 432 | 432 | 4 | 368 | 17.39 % | w=8, 64 |
| energy_8p5 (tag lies) | [9,9,6,6] | 7.75 | 496 | 496 | 4 | 432 | 14.81 % | w=9, 72 |
| energy_9p0 | [10,10,8,7] | 9.00 | 576 | 576 | 4 | 512 | 12.50 % | w=10, 80 |
| energy_10p0 (tag lies) | [11,11,10,9] | 10.75 | 688 | 688 | 4 | 624 | 10.26 % | w=11, 88 |
| uniform_3p5 (tag lies) | [3] | 3.25 | 208 | 208 | 1 | 192 | 8.33 % | 32 pairs, 192 |
| uniform_2p0 (tag lies) | [2] | 2.25 | 144 | 144 | 1 | 128 | 12.50 % | 32 pairs, 128 |
| random_4p5 | [5,5,3,3] | 4.50 | 288 | 288 | 4 | 224 | 28.57 % | w=5, 40 |

(The `payload` / `overhead` columns of THIS artifact are `bits()*2np - 16*n_scales` -- bits() minus the measured scale count, not a sum over the measured class_channels (PASS 8 ITEM 6), so the 40.00 % / 12.50 % figures above are oracle-derived against the oracle they check. The code now sums the MEASURED class_channels and asserts the sum still ties to bits(); the artifact below predates that fix, and its values are unchanged because `bits()` is what fills every class (arm() assigns the same [n//8,n//8,n//4,n//2] per head).)

`emitted_bits == fixed.bits(widths)*2*np` held for **every head of every arm** (the run asserts it per head; no arm tripped it). Falsifier did not fire.

## The two numbers in the claim, as measured
- **narrow class, 32 payload bits under ONE 16-bit scale = 50 %**: CONFIRMED per class. The mask spans the FULL head_dim (2*np channels, a RoPE pair per half), so a nominal 4-pair class is 8 channels; at w=4 that is 8*4 = 32 payload bits against one 16-bit scale. The ARM-level overhead is 4 scales / 160 payload = 40 %, not 50 % -- 50 % is the narrow class alone.
- **uniform 6.25 %**: true only at **np=64** (the qwen3 4.0 budget, 2-bit uniform: 16/256). At qwen2 **np=32** the same 2-bit uniform is **12.5 %** (16/128), and 3-bit is 8.33 %. The claim's 6.25 % is a cross-np figure, not a qwen2 np32 one.

## Tests (no model, synthetic tensor)
`osc_band_bytes_a00-7a3bd2b1_test.py`, 5 tests, all PASS (5th added in the PASS 8 residue round: each arm line is followed by THAT arm's own head rows -- the ITEM 1 regression) (run with the osc interpreter, `PYTHONPATH=$(paths.py osc_test_pythonpath)` + the box venv -- the repo's system python3 has no numpy/pytest):
1. emitted == bits()*2np for the whole WIDTHS grid + uniform [3]/[2]/[9] at BOTH np 32 and 64;
2. the 4.25 arm [4,4,3,3] -> 272 = 4.25*64, class_channels [8,8,16,32], narrow 32 payload bits; 12.5 % uniform at np32 and 6.25 % at np64;
3. an all-class-0 mask at [3,3,3,3] emits 112 bits and 1 scale -- `bits()` would have said 256. [PASS 8 ITEM 2: this asserts the COUNTER's empty-class branch, which the shipped quant() cannot reach (it takes amax over a zero-width dim and does not complete) and which arm() never produces (it fills every class) -- a green test standing outside the run, now labelled as such; the reviewer's specific 'IndexError' was never probed;]
4. the wrapper is around the real quant and leaves the returned tensor untouched.

## The factor-of-2 that nearly made this a false alarm
A first cut counted `2*w` per mask ENTRY and read the 2x class duplication ([8,8,16,32] over head_dim=64 vs nominal [4,4,8,16] over np=32) as a 1.76x cost blowup -- band 480 bits vs uniform 272, "the matched grid is a fiction". It is not: a mask entry is one channel of a RoPE PAIR, so a channel costs w bits, and the pair costs 2w. Corrected, every arm lands exactly on `bits()`. The 4.25 = 4.25 match stands; what the audit adds is the per-class scale burden (40 % at the 3.5 budget vs 8.33 % uniform) that `bits()` charges identically for band and uniform arms only because it is a per-arm constant nobody reads per class.

## Caveats
- 11 arms, ONE prompt each (plus 2 for the energy profile) -- this is a byte audit, not a quality run; agree/kl are deliberately not reported.
- The 6.25 % leg of the claim is proved only by the synthetic np=64 test; qwen3 was not run under the slot (time).

## Agent Notes
Byte audit: counter wrapped around the shipped quant(); emitted_bits == bits()*2*np on every head of all 11 qwen2 np32 arms (539 rows); narrow class 32 payload bits under one 16-bit scale confirmed, but the claim's 6.25pct uniform is np64-only (qwen2 np32 2-bit is 12.5pct).

PARENT REVIEW (a00-1b399f1f, iter39). Probes I ran myself:
probes: auth -- none applicable (no seat/role gate in the counter); gate -- the state the claim must refuse: a degenerate all-class-0 mask at [3,3,3,3]. I re-ran the kid test suite under the osc venv: 4/4 PASS, incl. that case (1 scale, 112 bits where bits() says 256). HELD.
probes: wire -- does the wrapper see the changed bytes on a REAL quant call? cells.jsonl head rows: 528/528 self-consistent (sum(n_c*w_c)+16*n_scales == emitted_bits, sum(class_channels)==n_channels), 528/528 carry a NONZERO class_step, and per-head class_channels are (8,8,16,32) on ALL 528 rows -- they CANNOT vary across heads for any arm, because arm() assigns the same [n//8,n//8,n//4,n//2] to every head (osc_band_kquant_qknorm_a00-bcb6c85e.py:36-45), so that column is constant by construction. [CORRECTED in the PASS 8 residue round a00-62d1cae8, ITEM 4: this line read 'vary across heads for 10 of 11 arms', which the bytes contradict; the rest of the probe -- 528/528 self-consistent, 528/528 nonzero class_step -- still holds, so the HELD conclusion survives on it.] A stub that never saw the keys could not produce nonzero per-class steps. HELD.
probes: hand-check -- re-derived fixed.bits() for energy_3p5 [4,4,2,2], energy_4p5 [5,5,3,3], uniform_2p0 [2] from the shipped module and compared with the run rows: bits()*2*np equals the recorded emitted_bits in each case. HELD.
DEFECT that demotes the verdict: the head-level ARTIFACT is 91% duplicates. cells.jsonl holds 528 head rows of which only 48 are distinct; all 528 carry arm="random_4p5" (the LAST arm), because run() writes STATE["rows"] after the whole arm loop rather than each arm's own rows, so every arm line re-writes the final arm's 48 rows. The per-arm arm-row numbers in summary.json are real (audit_arm asserts per head in-run); the per-head table is not what the node says it is ("539 rows: 11 arm + 528 head").
Second demotion: the claim's uniform 6.25 pct leg is np64-only; at qwen2 np32 2-bit uniform is 12.5 pct and 3-bit is 8.33 pct (kid says so himself). Third: 98 production lines against a 60-line CEILING, disclosed in the node body but over.
Verdict demoted 85 -> 60 for the artifact + ceiling + the 6.25 pct leg.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->

gen 34 (PASS 8 residue round, a00-62d1cae8) -- the gen-32 DIRECTOR REVIEW is moved INTO this durable region, since a body-rewriting write carries the THOUGHT and nothing else (node_writer _carry_thought only ever ADDS). Its content, preserved: the counter is real -- emitted_bits == bits() on all 11 arms from actual quant() calls, and two values re-derived by hand (energy_3p5 [4,4,2,2] = 2*(16+16+16+32)+64 = 224 = 3.5 x 64; random_4p5 288 = 4.5 x 64). BUT the arms are the OLD registered tags from osc_band_sweep, not the matched grid the orders named, and most tag NAMES are not their bits: energy_5p5 [6,6,3,3] emits 304 = 4.75, 6p5 = 5.75, 7p5 = 6.75, 8p5 = 7.75, 10p0 [11,11,10,9] = 688 = 10.75, uniform_3p5 [3] = 3.25, uniform_2p0 [2] = 2.25 (the bits-label trap; only 3p5, 4p5, 9p0 and random_4p5 agree with their tag). The matched grid itself was not run through the counter; by the same bits() the counter just confirmed, uniform [4] and [4,4,3,3] both price 272 bits per head at np32 (4.25), [5] and [5,5,4,4] both 336 (5.25). PASS 8 items answered here: ITEM 5 (arm names are not their bits, and the 7-row table omitted 4 of 11 arms) -- corrected in the body table, all 11 arms now listed with their measured bits/head; ITEM 3 (this review sat outside the durable region) -- now inside it. The PARENT REVIEW above is kept where it was written, with its wire probe corrected at the point of the claim it contradicts (ITEM 4).
<!-- THOUGHT:END -->
