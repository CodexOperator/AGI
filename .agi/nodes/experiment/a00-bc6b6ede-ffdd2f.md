---
id: experiment:a00-bc6b6ede-ffdd2f
mint_id: 10feac89cd48427a9950e4f3d4677de5
type: experiment
parents:
  - hypothesis:c2-digital-kuramoto-flip-mode
next_edges: []
confidence: 0.95
edited_by: a00-08515464
evidence_runs:
  - experiment:a00-bc6b6ede-ffdd2f
loop: hypothesis:c2-digital-kuramoto-flip-mode@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3972bdc3f1f3e3e1
season: 2
title: A00 bc6b6ede ffdd2f
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bc6b6ede-ffdd2f

## Experiment

Kid B of hypothesis:c2-digital-kuramoto-flip-mode. ONE claim: the 8-nearest
flip-byte ring reproduces the all-flip K_c within 10% on the same seeds/grid
and reaches R(192) >= 0.9. Independent byte-neuron implementation from the
CLAIM spec (no Kid A code copied; Kid A read only for the shared conventions
and its K_c reference 115.96).

Script: `.agi/context/local-maxxing/c2/c2_kidB_ring.py` (ONE script, five
topologies, shared seeds/draws). Results: `c2_kidB_results.json` (825 rows).

Command:

```
~/.venv-lm/bin/python c2_kidB_ring.py --out c2_kidB_results.json
```

Inputs: N=256, sigma_I=10, seeds {0..4}, K_int = 0..256 step 8 (33 points),
4096 ticks, R averaged over the last 2048 ticks, driven by the same
`make_inputs` draw per (seed, sigma) reused across K and topology (paired).
Byte-neuron exactly per spec: m<-((m*205)>>8)+I+kick+n (n in {-1,0,+1}),
spike s = carry (acc>=256), reset = wrap, flip f = s^s[t-1],
I = round(N(80,10)) clipped [56,120]. Order parameter
`theta_i = 2*pi*(t-t_last)/(t_last-t_prev)` with the >3-period / <2-fire
exclusion and the <N/2-remain undefined rule; rate >= 0.98 flagged degenerate.

Topologies (kick read from the PREVIOUS tick's vector):
- `all_flip`  mean field, kick = floor(K_int*F/N), F = popcount(f)  (reference)
- `ring8`     kick_i = floor(K_int*popcount(byte_i)/8), byte_i = f at i+-1..i+-4
- `ring4`     same, i+-1..i+-2, /4
- `ring2`     same, i+-1, /2
- `spike`     all-flip mean field but using s in place of f (control)

Wall 157.5 s (ceiling 240 s). loadavg 4.57/3.80/3.38 -> 5.81/4.46/3.68;
MemAvailable 17,285,672 kB -> 16,742,720 kB; nproc 4; numpy 2.4.3.

## Evidence

Every number below is in `c2_kidB_results.json` (`claim`, `summary`, `box`).

| topo | K_c (5-seed mean) | K_c CV | R(0) | R(192) | rate(192) | plateau rate |
|---|---|---|---|---|---|---|
| all_flip | 115.96 | 0.43% | 0.0723 | 1.0000 | 0.6750 | 0.6989 |
| **ring8** | **114.68** | 0.38% | 0.0723 | **0.9919** | 0.6771 | 0.7015 |
| ring4 | 114.22 | 0.41% | 0.0723 | 0.9676 | 0.6765 | 0.7001 |
| ring2 | 113.24 | 0.61% | 0.0723 | 0.8673 | 0.6597 | 0.6686 |
| spike | 165.20 | 0.41% | 0.0723 | 1.0000 | 0.9935 | 0.9992 |

Claim checks:
- K_c ratio ring8/all_flip = **0.98899** -> within 10% = **true**
  (tolerance band 0.9..1.1; ring8 is 1.10% BELOW the all-flip switch).
- ring8 R(192) = 0.9919 >= 0.9, per seed [0.9918, 0.9932, 0.9890, 0.9905, 0.9950]
  -> **true** in 5/5 seeds.
- `all_conjuncts_hold` = **true**.

Information columns (NOT part of the claim):
- ring-2 K_c = 113.24 (0.61% CV) — still switches, and *below* the all-flip K_c,
  but its R(192) = 0.8673 < 0.9: a 2-bit wire locks at a lower order than the
  global field. ring-4 K_c = 114.22, R(192) = 0.9676 — between the two.
- Bits read per neuron per tick: ring-2 = 2, ring-4 = 4, ring-8 = 8, all-flip = N.
  So the owner's nearest-flip wiring reaches the same switch with 8/256 = 1/32
  of the all-flip read budget, and even 2 bits/tick still crosses 0.5.
- spike-mode K_c = 165.20 with plateau rate 0.9992 (> 0.98 degenerate): using
  the level instead of the flip moves the switch up 42.5% and locks only into
  the all-fire fixed point. The pilot's 166/1.000 is reproduced. This is the
  measured sense in which FLIP, not LEVEL, is the impulse that gives a
  non-degenerate lock.
- all-flip K_c = 115.96 equals Kid A's 115.96 to the digit on the same
  seeds/grid — the two independent implementations agree; the ring8 value
  matches the parent's pilot (114.7-115.9).

## Interpretation (for the parent's verdict, not a verdict itself)

Both conjuncts of the Kid B claim hold, so the parent's falsifier
"K_c(ring-8)/K_c(all-flip) > 1.25 or R(192) < 0.5 on the ring" does not fire.
`nearest-flip coupling` is viable wiring: the local byte carries the switch at
1/32 the all-flip read cost. The spike-mode column is the first measured
support for the flip-as-impulse reading: same accumulator, same reset, only
the read-out (flip vs level) changes, and the level variant only locks into
the degenerate all-fire state.

## Agent Notes
Kid B ring claim holds: ring8 K_c=114.68 vs all-flip 115.96 (ratio 0.9890, within 10%), ring8 R(192)=0.9919 in 5/5 seeds; ring4 114.22/R(192) 0.9676, ring2 113.24 but R(192) 0.8673<0.9 (2 bits/tick still switches, locks weaker); spike-mode K_c=165.20 at plateau rate 0.9992 (degenerate) -> flip not level is the impulse; all-flip K_c 115.96 == Kid A to the digit. 825 runs, wall 157.5s, numpy 2.4.3.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review TM.02: verified from the BYTES (c2_kidB_ring.py itself), not the kid report. Four negative probes. (1) gate: ring8 K_int=0 gives R=0.0723 <= 0.125 -- HOLDS. (2) wire: the ring coupling term neutralised in the KID OWN SOURCE ((K_int*cnt)//w -> *0) collapses R at K_int=128 from 0.6416 and at K_int=192 from 0.9919 to 0.0723, so the ring read reaches the accumulator -- HOLDS. (3) flip-specificity: mutating the ring source vector from f_prev to s_prev moves K_c from 114.685 to 166.061 (ratio 1.448), which is the same all-fire collapse the kid spike-mode control reports; the FLIP read is therefore load-bearing and the claim is stronger than a mere numeric coincidence --- if level-read had reproduced K_c within 10% the flip specificity would have been unproven. (4) cross-check: Kid B all_flip K_c=115.962 vs Kid A 115.96 (delta 0.002), so the two independent implementations agree. All four probes hold; verdict proved stands. Note ring2 also switches (K_c 113.24) but its R(192)=0.8673 < 0.9, so 8 bits/tick is the sparsest wiring that meets the claim R threshold.
<!-- THOUGHT:END -->
