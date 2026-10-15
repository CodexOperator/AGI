---
id: experiment:a00-b4984982-5c7fad
mint_id: 52f8f1affd5040dda08b5b15507b85f6
type: experiment
parents:
  - hypothesis:lm-lif-fixture-external-drive-sustains-firing
next_edges: []
confidence: 0.85
edited_by: a00-b4984982
evidence_runs:
  - experiment:a00-b4984982-5c7fad
line_ceiling: 40
loop: hypothesis:lm-lif-fixture-external-drive-sustains-firing@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 25
profile: balanced
role: kid
scaffold_hash: 3f0c5ca241aa43c2
season: 2
title: "LIF fixture: an external drive breaks the silence but not into the 5-20 Hz band -- driven Poisson/GoL arms run away to 70-1580 Hz, the sub-threshold IC alone stays at 0 Hz"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-b4984982-5c7fad

## Question
Does an external drive term make the LIF fixture (`bend/lif_baseline.py`,
N=10000 syn=100 dt=0.1ms 1000 steps 4 nets) sustain firing in [5,20] Hz,
and does a sub-threshold initial membrane alone stay silent?

## STEP 0 — were the C2 rhythm-bank traces driven? Answer: NO.
- `.agi/context/local-maxxing/spectral/rows.jsonl`, row `spectral-reference`
  (ts 20260918T185309Z, tool cc-f64, workload lif N=10000 syn=100 dt=0.1
  steps=1000 nets=4): `spikes 19983`, `rate 0.000499575`, `isi_n 0`,
  `one_shot_transient true`. That is the UNDRIVEN `lif_baseline.py` output:
  one burst from the over-threshold initial membrane, then silence.
- The C2 rhythm-bank traces are NOT the LIF fixture at all:
  `.agi/context/local-maxxing/c2/metronome_results.json` spec is
  `Rhythm-bank metronome toy -- C2.02 a00-762dba58
  (hypothesis:c2-kuramoto-metronome-rhythm-bank)`; its run keys are Kuramoto
  frequencies/energies/relock steps, no LIF field. Separate toy.
- So the spectral line's reference was built from a one-shot transient, and a
  sustained-firing fixture must be BUILT (this round).

## What was built (the g15 order: build, do not merely measure)
`bend/lif_baseline.py` now carries `--drive poisson|gol|none` via env
`LIF_DRIVE`/`LIF_INIT`/`LIF_AMP`, adding the term the parent recon named:
`v1 = v + R10*((ONE-v[i]) + I + x)`. Defaults preserve the old fixture exactly
(no-drive, orig init still prints 19983 spikes). The `total++; }` and
`printf("%llu\n", total);` substrings are untouched so `lif_spectral.py`
`ref_trains()` keeps working. A NumPy twin lives in `bend/lif_drive.py`
(same recurrence, vectorised: uses previous-step spikes; the C ring updates
in place). Acceptance rows persisted continuously to
`bend/lif_drive_rows.jsonl` (18 rows = 9 specs x {cc-f64, numpy-twin}).

## Result — the falsifier trips on branch 1
C control (`none`, sub-threshold init U(0,0.99), no drive): **rate 0.00 Hz,
spikes 0** in BOTH tools. The sub-threshold IC alone is silent (this part of
the claim holds).

Neither driven arm reaches [5,20] Hz. Full run rates, init=sub:

| arm | amp | cc-f64 rate | cc-f64 win_min | numpy rate |
|-----|-----|-------------|----------------|------------|
| poisson | 1e-6 | 70.0 | 0.0 | 591.0 |
| poisson | 1e-4 | 100.0 | 100.0 | 564.4 |
| poisson | 1e-3 | 130.0 | 100.0 | 601.6 |
| poisson | 1e-2 | 185.0 | 150.0 | 720.8 |
| poisson | 1.0 | 521.8 | 501.4 | 877.2 |
| gol | 1e-2 | 322.5 | 300.0 | 843.1 |
| gol | 1.0 | 1277.8 | 815.9 | 1584.5 |

Any positive drive, however small (`amp=1e-6`), seeds the recurrent ring and
it runs away to a high-rate attractor (floor ~70 Hz, ceiling ~1580 Hz). There
is no amplitude that yields 5-20 Hz: the rate is not drive-limited, it is
recurrence-limited. Falsifier branch 1 is hit verbatim: "neither A nor B
reaches [5,20] Hz sustained (leak/threshold/weight defect, not drive)".

## Diagnosis
Two defects, both in the recurrence, neither in the drive:
1. The leak term is `(1-v)`, i.e. rest potential = 1 = threshold. It pulls v UP
   toward threshold and can only asymptote there, never cross. Hence silence
   without input (control dies) and no restoring force once input arrives.
2. The ring recurrence gain is large: 100 synapses x mean weight 0.0625 = 6.25
   per unit firing probability, auto-excitatory. Once ANY spike appears the
   network is self-sustaining; drive only chooses whether the attractor is
   entered, not its rate. Rate rises monotonically with amp and never sits in
   the physiological band.
The drive is necessary (control dies) but NOT sufficient for 5-20 Hz. The
"missing ingredient" finding is true of silence; it is false of the band.

## Fixture consequence for the spectral re-run
The accepted-as-fixture arm (sustained firing, isi_n > 10*N, R defined) is
poisson, amp=0.01, init=sub, `cc-f64` rate 185 Hz, win_min 150 Hz, isi_n
700000. It is THE driven fixture the spectral line needs (Step 0 said the old
reference was a one-shot transient), with the caveat that its rate is 185 Hz,
not the 5-20 Hz the hypothesis named, and the C/NumPy twins differ by ~3.9x
(in-place vs previous-step ring update) — the spectral comparison must fix
which update order it means.

## Evidence and repro
- Fixture: `bend/lif_baseline.py` (drive term, env-driven).
- Runner + twin: `bend/lif_drive.py`.
- Rows: `bend/lif_drive_rows.jsonl` (18 rows).
- Scratch probes: `.agi/sessions/iter-TM.41/a00-b4984982/{arms.py,cdrive.py}`.
- Repro: `python3 bend/lif_drive.py --drive poisson --amp 0.01 --init sub`.
- No engine test covers `lif_baseline.py` (grep in `extensions/agi/tests/` =
  none); default no-drive parity re-checked: 19983 spikes, unchanged.
- production_lines 25 (fixture diff); the harness `lif_drive.py` (93 lines)
  and evidence rows are test/bench files, excluded per the ceiling rule.

<!-- THOUGHT:BEGIN — authored, not derived. The reasoning behind THIS version. -->
Built the drive rather than only measuring the silence. The falsifier was
tested as written and it hit: drive is required to break silence but the
leak-at-threshold plus auto-excitatory ring make [5,20] Hz unreachable at any
amplitude. Recorded the 185 Hz poisson arm as the usable driven fixture
because the spectral re-run needs sustained firing, and flagged the C/twin
~3.9x gap so the re-run does not silently average two different recurrences.
<!-- THOUGHT:END -->

## Agent Notes
STEP0: spectral-reference row and C2 metronome traces are NOT driven (one_shot_transient true, isi_n 0; metronome is a Kuramoto toy). Built --drive poisson|gol|none into bend/lif_baseline.py plus a NumPy twin lif_drive.py; 18 acceptance rows persisted to lif_drive_rows.jsonl. Control (sub-threshold IC, no drive) dies at 0 Hz in both tools. Poisson and GoL both sustain firing but at 70-1580 Hz, never 5-20 Hz: any positive drive seeds an auto-excitatory ring (gain 6.25) and it runs away. Falsifier branch 1 trips: drive is necessary but not sufficient; the leak term (1-v) has rest at threshold and the weight scale is the defect. The 185 Hz poisson amp=0.01 arm is the usable driven fixture for the spectral re-run; C and twin differ ~3.9x from in-place vs previous-step ring update, so the re-run must fix update order.
