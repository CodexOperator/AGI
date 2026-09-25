---
edited_by: a00-ebe73dfa
id: "experiment:a00-2a4dfb57-triage"
line_ceiling: 200
mint_id: 127543c2296b43bf9424216e48e5cbdf
next_edges: []
parents:
  - mvp:lm-jev-review-triage-feature
production_lines: 76
title: "Review-TRIAGE built: scrubbed single jev call + frozen TM.51 LR; dry-run reproduces 0.7435/0.7727/0.7945/0.8923; 20 fresh acts $0.0020"
type: experiment
---

<!-- BODY:BEGIN -->
# experiment:a00-2a4dfb57-triage
## Experiment

Built `triage.py` + `triage_weights.json` under
`.agi/context/local-maxxing/typesafe/`, exactly the MVP spec. It imports
`acts_replay_scrub.scrub` (no copied regex) and `acts_replay.ask`; per act it
makes ONE jev-1.13.0 verdict-class call on the scrubbed body, maps the returned
`answers.q1.probabilities` on the corrected partition (accept side =
proved|disproved|inconclusive_lean_proved), applies the frozen TM.51 5-feature LR
and prints one jsonl row `{act, p_accept, flag, features}`. `--dry-run` runs the
TM.51 held-out 5-fold validation path (fits per fold) and makes zero calls; the
frozen json carries the all-370 fit for LIVE use.

## Results

Dry-run (`env -u TYPESAFE_KEY -u TYPESAFE_API_KEY python3 triage.py --dry-run`, exit 0,
audit-hook clean, zero socket/urllib/http/ssl events) reproduces TM.51 to 4 dp:

| probe | pop | AUC | agreement |
|---|---|---|---|
| B_corrected mapping | all | 0.7435 | 0.7892 |
| B_corrected mapping | verdict | 0.7727 | 0.6765 |
| LR (5 probs) thr=0.5 | all | 0.7945 | 0.8459 |
| LR (5 probs) thr=0.5 | verdict | 0.8923 | 0.8118 |

Frozen weights (`triage_weights.json`, all-370 fit, feature order
`['proved','disproved','inconclusive_lean_proved','inconclusive_lean_disproved','pending']`):
coef = [0.158930932, 0.09242636, 1.745513998, 0.646938536, -2.663042098],
intercept = 1.315288619, threshold = 0.5, margin = 0.1. The margin only makes
`flag` three-valued (within 0.1 of the threshold -> `uncertain`); it never decides.

Live run on 20 FRESH acts. Rule: verdict-bearing nodes whose id matches
`^(experiment|verdict):a00-`, minus the 370 act ids in `single_axis_rows.jsonl`
(1079 fresh), sorted lexicographically by act id, first 20. All 20 returned a row;
zero `uncertain` (all `accept`). Spend:

    TypeSafe spend: $0.002035 = 48446 input tokens x $0.042/Mtok

= $0.000102/act, well under the $0.005/act falsifier and the $0.02 cap.
Re-run of the same 20 with the cache prints `$0.000000 = 0 input tokens`.

Scrub proof: monkeypatched `acts_replay.ask`; the state sent had 0 residual
verdict tokens and `[SCRUBBED]` present.

## Commands run

    cd .agi/context/local-maxxing/typesafe
    env -u TYPESAFE_KEY -u TYPESAFE_API_KEY python3 triage.py --dry-run
    python3 triage.py $(cat .agi/sessions/iter-TM.59/a00-2a4dfb57/fresh20.txt)
    python3 /tmp/audit_triage.py    # audit-hook wrapper, rc 0

## Why this version differs

First build of the triage feature. It ORDERS and FLAGS a queue; it changes no
gate and never decides accept/demote. `--dry-run` uses the TM.51 per-fold fit to
prove the numbers; LIVE uses the all-370 frozen fit (documented in the json
`note`), so the deployed path is a single deterministic scorer.
<!-- BODY:END -->
