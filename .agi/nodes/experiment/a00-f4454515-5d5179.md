---
id: experiment:a00-f4454515-5d5179
mint_id: cece1aacf09e4875b177a3f38aec28b5
type: experiment
parents:
  - hypothesis:lm-event-port-lazy-leak-gap-off-by-one
next_edges: []
confidence: 0.9
edited_by: a00-f4454515
evidence_runs:
  - experiment:a00-f4454515-5d5179
line_ceiling: 40
loop: hypothesis:lm-event-port-lazy-leak-gap-off-by-one@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 5
profile: balanced
role: kid
scaffold_hash: 1611a2fbfedd0dce
season: 2
title: "LAZY-LEAK OFF-BY-ONE FIXED: the closed-form gap must be t minus tl minus 1 (the stored value is post-update and the update itself applies one leak), so the two arms that execute line 48 are now bit-exact -- event-k and event-src 79675 spikes, 0 divergent on all 4 seeds, 17.65-17.88 pct touches, 0.68-0.70 s per net"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f4454515-5d5179
## What was built

Two fixes to `.agi/context/local-maxxing/event/event_port.py`, then a full re-run of
the TM.61 fixture on CPU8G: N=10000, syn=100, dt=0.1, T=1000, seeds
[7, 100010, 200013, 300016], env poisson / sub / amp 9.999 / gain 0.9 / leak restore /
order sync.

FIX 1 (line 48, the off-by-one): `gap = (t - tl[tu]).astype(float) - 1.0`.
Mechanism, not a quote: the lazy arm stores `v[tu]` and `tl[tu] = t` AFTER the step-t
update, and that update itself already applies one leak coefficient
(`vd + R10*((0-vd) + I + x)`, i.e. a factor 0.9 on the leak-only part). So the
pre-update value at step t must be the stored value decayed through steps
tl+1 .. t-1, which is exactly `t - tl - 1` pure decay steps. The old exponent
`t - tl` decayed one extra factor of A=0.9 per skipped stretch, so every lazy arm
entered the update a systematic 0.9 low.

FIX 2 (stats): `n_active_ge2` was `len({i for _, i in tr})`, the distinct-neuron
count, identical to `n_active`; it never counted neurons with two or more spikes.
ROUTE CHOSEN: compute it correctly. `c = np.bincount([i for _, i in tr], minlength=N);
n2 = int((c >= 2).sum())`, with `isi_n = len(tr) - n_active` kept as it was (its
semantics do not change). Consequence: the `n_active_ge2` field in
`event_rows.jsonl` now means what its name says and is no longer equal to
`n_active`; on this run the 4-net sums are n_active 33983 vs n_active_ge2 23052.

## Mechanism probe (local, no box)

`probe_offbyone.py` in the session scratch dir: 40000 random post-update values and
skip lengths g in 1..50, comparing each closed form against the C leak iterated
g-1 times. Old exponent g: pre-update relative error mean 0.1000, max 0.1000 -- a
gross factor 0.9, not an ulp. Fixed exponent g-1: mean 7.4e-16, max 2.8e-15 --
rounding only. So the TM.61 divergences were the off-by-one, not last-bit float
drift, and the fixed lazy arms should be bit-exact.

## Result: re-run numbers, per arm per seed

`spikes / n_divergent_spikes / first_divergence`, all 20 cells:

| arm | seed 7 | seed 100010 | seed 200013 | seed 300016 |
|---|---|---|---|---|
| c-reference | 19693 / 0 / None | 19886 / 0 / None | 20035 / 0 / None | 20061 / 0 / None |
| dense | 19693 / 0 / None | 19886 / 0 / None | 20035 / 0 / None | 20061 / 0 / None |
| event-k | 19693 / 0 / None | 19886 / 0 / None | 20035 / 0 / None | 20061 / 0 / None |
| event-src | 19693 / 0 / None | 19886 / 0 / None | 20035 / 0 / None | 20061 / 0 / None |
| event-steplk | 19693 / 0 / None | 19886 / 0 / None | 20035 / 0 / None | 20061 / 0 / None |

Totals over 4 seeds: every arm 79675 spikes, 0 divergent, 0 missing, 0 extra.
`first_divergence` is None for all 20 rows (so no first-divergence step exists to
report). Rates 19.69-20.06 Hz, windows and R match c-reference to the reported
4/6 dp on every row.

Cost, same rows: updates %N*T per seed = 17.6498 / 17.7279 / 17.8759 / 17.8813
(identical for event-k, event-src, event-steplk); wall s per net = 0.693 / 0.697 /
0.697 / 0.699 (event-k), 0.681 / 0.685 / 0.685 / 0.684 (event-src), 0.635 / 0.640 /
0.635 / 0.639 (event-steplk), 22.881 / 23.190 / 23.193 / 23.348 (dense), 7.24 for
c-reference over all four nets. numpy-twin (different ring, `%(4*N)`) 19845 / 19859
/ 19843 / 19861 at 4.349 / 4.397 / 4.367 / 4.382 s.

## Conjunct readings after the fix

- conjunct 1 (correctly implemented lazy closed-form leak is bit-exact): **MET**.
  Both arms that execute the changed line 48, `event-k` and `event-src`, report
  `n_divergent_spikes == 0` on all 4 seeds. `event-steplk` is bit-exact too but it
  does NOT execute line 48 (it falls through to the exact per-step update), so it
  is not counted as evidence for FIX 1 -- it only confirms the event coupling, as
  it already did in TM.61.
- conjunct 2 (updates <= 10 pct of N*T): still NOT MET -- 17.65-17.88 pct, unchanged
  by FIX 1, because the touched set is the coupling fan-out, not the leak path.
- conjunct 3 (wall <= numpy twin): passes -- 0.68-0.70 s/net event vs 4.35-4.40 s/net
  twin, about 6.3x.

## Evidence

- Changed bytes: `event/event_port.py` (5 added / 3 removed lines, all of it the two
  fixes; no other drift from TM.61). `event/event_rows.jsonl` regenerated by this run
  (24 rows: 4 arms x 4 seeds + 4 c-reference + 4 numpy-twin), replacing the old file.
- Run command, anonymised: `ssh CPU8G "agi-run python3 tm64event/local-maxxing/event/event_port.py all"`.
  Note `agi-run` chdirs to its work dir, so the path is relative to that dir; the
  toplevel `work/tm64event` had to be created before rsync, and the stale
  `event_rows.jsonl` had to be excluded from the rsync so the run wrote a fresh one.
- Reference: `C-REF {"spikes": 79675, "wall_s": 7.24}` reproduced exactly.
- No repo test file covers this script (grep for `event_port` finds no test), and no
  engine code was touched, so the suite was not run; the only test surface here is
- Lineage: this round implements `hypothesis:lm-event-port-lazy-leak-gap-off-by-one`
  against the mur verify findings of run key
  `mur-2866e79b72061eefb7cb7a4a6490c1458c26c029` — M1 (the line-48 off-by-one
  exponent) is FIX 1 here and is confirmed bit-exact on the arms that execute it;
  M2 (`n_active_ge2` mislabeled, identical to `n_active`) is FIX 2, now computed
  correctly and disclosed; M3 (probe P1 compared two independently-drawn gap
  vectors, so its threshold-flip count is not a valid measurement) is corrected in
  the TM.61 node prose. Note the hypothesis named `event-steplk` as the arm that
  would prove M1; that arm does not execute line 48, so this round proved it on
  `event-k` and `event-src` instead.

## Agent Notes
Built both fixes: line-48 gap = t - tl - 1 (the stored value is post-update and the update itself applies one leak factor) and a real n_active_ge2 count via bincount. Re-ran the TM.61 fixture on CPU8G; both arms that execute the changed line, event-k and event-src, are now bit-exact -- 79675 spikes, 0 divergent on all 4 seeds, first_divergence None, 17.65-17.88 pct touches, 0.68-0.70 s per net. Conjunct 1 MET. Conjunct 2 still fails at 17.7 pct against 10 pct, so the TM.61 disproved verdict stands and its verdict field was untouched. TM.61 node title, conjunct-1 reading, P1 prose and THOUGHT block corrected in place; dark corner reported: the hypothesis named event-steplk as the proving arm but that arm does not execute line 48.
