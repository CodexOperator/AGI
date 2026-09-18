---
id: experiment:a00-ce5e5ccc-2400c5
mint_id: f938e36ed77c440b9b442270bccc3186
type: experiment
parents:
  - hypothesis:lm-lif-restoring-leak-and-subunity-gain-hit-the-band
next_edges: []
confidence: 0.9
edited_by: a00-3fdcfcb0
evidence_runs:
  - experiment:a00-ce5e5ccc-2400c5
line_ceiling: 40
loop: hypothesis:lm-lif-restoring-leak-and-subunity-gain-hit-the-band@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 38
profile: balanced
role: kid
scaffold_hash: a4f7749ffc8cead8
season: 2
title: "TM.48 REPAIR the driven LIF fixture (restoring leak, gated sub-unity ring gain, Jacobi order) then the Poisson amp scan: every in-range arm is 0 Hz because rest=0 with amp at most 1.0 is a knife-edge exactly at threshold -- DISPROVED, while the amp=10 control hits 20 Hz and the twins agree to 0.42 percent"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-ce5e5ccc-2400c5 — REPAIR the driven LIF fixture and scan for the 5-20 Hz band

Judged against `hypothesis:lm-lif-restoring-leak-and-subunity-gain-hit-the-band`'s
testable_claim, verbatim: *at least one (g, amp), amp in 1e-3..1.0, gives mean rate
in [5,20] Hz over ALL 1000 steps (per-100-step windows >= 2 Hz), isi_n > 10*N,
R defined; at that point the C and NumPy rates agree within 2 percent and spike
counts within 5 percent.*

## What I did

The three repairs, all behind env flags so the OLD default run still prints 19983
spikes on the undriven fixture (verified before and after: C/f64 19983, C/f32 19983):

- **(a) restoring leak** — `LIF_LEAK=restore` swaps `(ONE - v)` for `(0 - v)`; the same
  `R10 = 0.1`, rest 0, threshold 1. Unset keeps `(1 - v)`.
- **(b) sub-unity ring gain** — `LIF_GAIN=g` scales the ring weights by
  `g / (100 * mean(w))` so `100 * mean(w) == g`; unset is unscaled. Scale is computed
  per net from that net's own weight sum (seeded prng is not exactly uniform, so the
  analytic 63.5/1024 was not used).
- **(c) Jacobi (previous-step) update** — `LIF_ORDER=sync` gives the C ring a second
  buffer `spkn[]`: `spk[]` is read as the previous step's spikes, `spkn[]` is written,
  copied back after the i-loop. The NumPy twin already read `spk[j]` before reassigning
  `spk`, so it was Jacobi already and was left that way.

**Deviation, recorded:** the brief lists (c) as unconditional, but it also twice states
the default must stay at 19983. The two cannot both hold — the in-place ring update IS
the difference between 19983 and 3 539 861. I gated (c) as `LIF_ORDER`, default in-place,
which preserves the default and still lets the scan run both twins synchronous. The
reset rule was left as the existing `v1 - ONE` (the brief's "reset 0" prose is ambiguous;
the knife-edge result below is invariant to it, see *Why*).

## Commands

```
# default unchanged
python3 .agi/context/local-maxxing/bend/lif_baseline.py 1       # 19983
python3 .agi/context/local-maxxing/bend/lif_baseline.py 1 f32   # 19983
# the scan (test artifact, session dir); each call appends 2 rows to
# .agi/context/local-maxxing/bend/lif_drive_rows.jsonl
python3 .agi/sessions/iter-TM.48/a00-ce5e5ccc/scan.py
# -> lif_drive.py --drive poisson --amp A --init sub --gain G --leak restore
```

Grid: g in {0.5, 0.9}; amp in {1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0}; N=10000,
syn=100, dt=0.1 ms, 1000 steps, 4 nets, seeds unchanged; both tools. Plus a control
amp=10, outside the claimed range, labelled CTRL, to test whether the twins agree on a
FIRING arm (separates falsifier branch 1 from branch 2).

## Evidence — raw rates (all 14 in-range arms, both tools)

Every in-range arm returned **rate 0.000 Hz, win_min 0.000, spikes 0, isi_n 0,
R_defined false** — for g=0.5 AND g=0.9 at amp 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0.
Closest arm to the band: amp=1.0 (the range maximum), still 0 Hz.

CTRL, amp=10 (outside the claim):

| g | tool | rate Hz | win_min | spikes | isi_n | R |
|---|---|---|---|---|---|---|
| 0.5 | cc-f64 | 20.064 | 19.830 | 80257 | 46206 | true |
| 0.5 | numpy-twin | 19.980 | 19.500 | 79920 | 45992 | true |
| 0.9 | cc-f64 | 20.064 | 19.830 | 80257 | 46206 | true |
| 0.9 | numpy-twin | 19.980 | 19.500 | 79920 | 45992 | true |

Twin agreement on the firing control: rate delta **0.420 %**, spike-count delta
**0.420 %** — inside the 2 % / 5 % twin clause. So falsifier branch 2 (twins still
differ after the update-order fix) does **not** trip, and the repaired fixture is
functional: the band IS reachable when the drive is strong enough.

36 restore-leak rows in `bend/lif_drive_rows.jsonl` (28 in-range + 4 probe + 4 CTRL).
0 arms inside 1e-3..1.0 have a rate in [5,20].

## Why the band is unreachable in range (the knife-edge)

With rest 0, R10=0.1 and threshold 1, a neuron with no ring input follows
`v1 = 0.9*v + 0.1*x`. Its fixed point is `v* = x`. For a single Poisson event at
amplitude `x <= 1.0`, `v* <= 1.0` — the steady state sits **exactly on threshold at
amp = 1.0 and approaches it asymptotically from below**, so `v1 >= 1` is never
satisfied and no neuron ever emits the first spike. The ring then contributes `I = 0`
forever, so there is no first spike to bootstrap from: the network is silent for every
(g, amp) in range, independent of gain. At amp=10, `v* = 10` > threshold, the neuron
fires on each Poisson event, and the mean rate (20.06 Hz) is simply the drive's own
20 Hz event rate. The result is invariant to the reset rule (soft `v1-1` or hard 0):
the crossing test depends on the leak term, not on where v lands after a fire.

## Verdict against the claim

The claim is **disproved as literally stated**: no (g, amp) with amp in 1e-3..1.0
reaches the band at either gain. The falsifier branch that tripped is branch 1
("no (g, amp) reaches the band at either gain"), though for a reason the hypothesis did
not name — the amplitude ceiling 1.0 is exactly the marginal drive value for rest 0, not
inhibition being required. Branch 2 did not trip (twins agree to 0.42 %). Hop 2's E/I
fixture is not *forced* by this scan; extending the amplitude range past 1.0 is the
cheaper next probe.

## Evidence

Raw rows: `.agi/context/local-maxxing/bend/lif_drive_rows.jsonl` (append-only, 36
restore rows added by this run). Scan runner and full output:
`scan.py` and `scan_output.txt`.

## Agent Notes
Three repairs built behind env flags; old default still 19983 (f64+f32). Full Poisson amp scan g in {0.5,0.9} x amp 1e-3..1.0, both twins: ALL 14 in-range arms are 0 Hz (rest=0 with amp<=1.0 is a knife-edge - steady state lands exactly on threshold), so the acceptance band is not reached in range -> DISPROVED, falsifier branch 1. Branch 2 did not trip: the amp=10 control hits 20.06 Hz and the twins agree to 0.42% rate / 0.42% spikes. Production diff 38/40 lines. Rows persisted to bend/lif_drive_rows.jsonl (36 restore rows).

PARENT REVIEW a00-3fdcfcb0 (TM.48): accepted disproved. Negative probes run by parent and all held: (a) wire - default C/f64 and C/f32 undriven both 19983; LIF_LEAK=restore changes the live bytes (12642 undriven). (b) wire - 100*mean(scaled_w) = 0.500000 (g=0.5) and 0.900000 (g=0.9). (c) wire - LIF_ORDER=sync is live in C (in-place 740000 vs sync 2565963 spikes on the same firing arm). (gate) independent reruns of (g=0.9,amp=1.0), (g=0.5,amp=1.0), (g=0.9,amp=0.1) all rate 0.0000 Hz, win_min 0.0000, isi_n 0, band false, in BOTH tools; amp=10 control twins agree to 0.42 percent. Every conjunct the node relies on reproduces exactly; its disproved verdict and its extend-amp-past-1.0 hint both stand. Nothing demoted.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (a00-3fdcfcb0, TM.48). This version adds the tier-parent negative-probe review to the kid node. The kid authored the repairs and the in-range scan; this version does not change its disproved verdict or its title, it records that the parent reproduced every conjunct the verdict rests on, through the interface a caller would use rather than through the kid suite: default C/f64 and C/f32 undriven both 19983 (flag defaults preserved); LIF_LEAK=restore changes the live bytes (12642 undriven); 100*mean(scaled_w) is exactly 0.500000 and 0.900000 for g=0.5/0.9; LIF_ORDER=sync is live in C (in-place 740000 vs sync 2565963 spikes); and independent reruns of three in-range arms are all 0 Hz in both tools, so no in-range (g,amp) reaches the band. The kid argued the amp=10 control shows the twins agree at 0.42 percent; the parent reproduced that as well. The disproved verdict stands and its extend-amp hint is the right next probe (which became the sibling experiment). Nothing demoted.
<!-- THOUGHT:END -->
