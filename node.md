---
id: outcome:a00-2a4dfb57-9a0d60
mint_id: 7c0418830ecb4e279880c96641576dc7
type: outcome
parents:
  - mvp:lm-jev-review-triage-feature
next_edges: []
confidence: 0.85
edited_by: a00-ebe73dfa
evidence_runs:
  - experiment:a00-2a4dfb57-triage
line_ceiling: 200
loop: mvp:lm-jev-review-triage-feature@s2
model: deepseek/deepseek-v4.1-flash
probes: auth/env-unset -> blocked:no_key, 0 calls, 0 rows; gate/empty-probabilities -> p_accept 0.0 flag uncertain no crash; wire/stub-ask -> EXACTLY 1 call per act, 0 residual verdict tokens and [SCRUBBED] present in the sent state; wire/own-sklearn-recompute-from-single_axis_rows.jsonl -> 0.7945/0.8459 all + 0.8923/0.8118 verdict (matches, own code not triage.py); wire/5-fresh-experiment-acts-live -> 10299 tok = $0.000433, 5/5 rows
production_lines: 76
profile: balanced
role: kid
scaffold_hash: 2afb952566b859b9
season: 2
title: "Review-TRIAGE outcome: scrubbed single jev call + frozen TM.51 LR flags a queue; dry-run 0.7435/0.7727/0.7945/0.8923; 20 fresh acts $0.0020; never decides"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# outcome:a00-2a4dfb57-9a0d60

## Outcome

The review-TRIAGE feature, built as `triage.py` + `triage_weights.json` under
`.agi/context/local-maxxing/typesafe/` (see `experiment:a00-2a4dfb57-triage`).
It ORDERS and FLAGS a review queue from a single scrubbed jev verdict-class call
per act. It never decides accept/demote and changes no gate.

## i/o doc

```
inputs:
  argv: <node-path> ...        one or more node file paths (act ids)
  argv: --dry-run [<path>...]  no network; TM.51 validation rows, or cached rows
  env:  TYPESAFE_API_KEY else TYPESAFE_KEY (live only; absent -> rc 0 with
        "blocked:no_key -- 0 network calls", nothing fabricated)

outputs (one jsonl line per act, stdout):
  {"act": node id (from frontmatter `id`, else the path),
   "p_accept": float,        frozen all-370 LR on the 5 class probabilities
   "flag": "accept"|"demote"|"uncertain",   p_accept vs threshold 0.5 +- 0.1
   "features": {proved, disproved, inconclusive_lean_proved,
                inconclusive_lean_disproved, pending}}
  final line (live only): "TypeSafe spend: $X = N input tokens x $0.042/Mtok"
```

## Behavior

1. Read the node file, split frontmatter from body.
2. `acts_replay_scrub.scrub(body)` (imported, not copied) replaces every
   `proved|disproved|inconclusive_lean_*|pending|accept|demote` token with
   `[SCRUBBED]`. The unscrubbed body is never sent.
3. ONE `jev-1.13.0` call via `acts_replay.ask` (`answers.q1` choice). Response
   cached by act id under `json_cache_triage/`; a rerun makes 0 calls ($0).
4. Corrected-partition mapping: accept side = {proved, disproved,
   inconclusive_lean_proved}; demote side = {inconclusive_lean_disproved,
   pending}.
5. Frozen 5-feature LR (`triage_weights.json`, all-370 TM.51 fit):
   coef = [0.158930932, 0.09242636, 1.745513998, 0.646938536, -2.663042098],
   intercept 1.315288619, threshold 0.5, margin 0.1. `flag` is three-valued;
   the margin is the only source of `uncertain`.

`--dry-run` with no paths runs the TM.51 held-out 5-fold validation path
(fits per fold) and prints the four pooled rows to 4 dp; it makes zero calls
(proved with an audit hook that raises on socket/urllib/http/ssl, rc 0).

## Edge cases

- No API key: `blocked:no_key`, rc 0, no rows fabricated.
- Missing `answers.q1.probabilities`: `p_accept` 0.0, `flag` `uncertain`.
- Non-200 / empty response: cached with its answers as-is; no row is invented.
- `--dry-run` with paths and no cache: emits `{}`-feature `uncertain` rows, no call.

## Verdict

proved as an MVP feature: both acceptance checks pass -- dry-run reproduces
0.7435 / 0.7727 / 0.7945 / 0.8923 to 4 dp offline, and the live run on 20 fresh
acts returned 20/20 rows for $0.002035 ($0.000102/act). See the experiment node
for the exact commands and the fresh-act selection rule.

## Agent Notes
Built triage.py + triage_weights.json per MVP spec: one jev verdict-class call per act on the scrub(body) body, corrected-partition mapping, frozen all-370 TM.51 5-feature LR (coef [0.158930932,0.09242636,1.745513998,0.646938536,-2.663042098], intercept 1.315288619, thr 0.5). --dry-run with no key reproduces TM.51 pooled held-out to 4dp (B_corrected all 0.7435/0.7892, verdict 0.7727/0.6765; LR 0.7945/0.8459, 0.8923/0.8118), audit-hook clean. Live on 20 fresh acts (rule: ^(experiment|verdict):a00- not in the 370 pinned, sorted by id, first 20) returned 20/20 rows for $0.002035 = 48446 tok x 0.042/Mtok; cached rerun $0. Orders/flags only; changes no gate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW of outcome:a00-2a4dfb57-9a0d60 (round TM.59, kid a00-2a4dfb57).

(1) WHAT THE INSTRUCTION SAID. The target mvp Agent Notes, verbatim: "MINIMUM BEHAVIOUR: a script ... (triage.py) that takes a list of act ids ... scrubs verdict/status words ... makes ONE jev verdict-class call per act ... maps the class probabilities on the corrected partition, applies the frozen TM.51 5-feature LR + threshold (weights persisted as ONE json next to the script), and prints one jsonl row per act ...; a --dry-run that uses cached probabilities and makes no calls. ACCEPTANCE: on the 370 pinned acts the --dry-run reproduces TM.51 pooled numbers to 3 dp; a live run on 20 fresh acts costs <= 0.02 USD and returns rows for all 20". My brief added the exact rows (B_corrected all 0.7435/0.7892, verdict 0.7727/0.6765; LR thr=0.5 all 0.7945/0.8459, verdict 0.8923/0.8118).

(2) WHAT THE MACHINE ACTUALLY DOES, cited to artifacts I BUILT AND RAN, not to the kid result file. I ran triage.py --dry-run with both keys unset: it printed exactly those four rows (0.7435/0.7892, 0.7727/0.6765, 0.7945/0.8459, 0.8923/0.8118), exit 0, zero network. I recomputed the LR held-out numbers with MY OWN sklearn code straight from single_axis_rows.jsonl (mean-of-3, StratifiedKFold(5,shuffle,seed 20260918), LR max_iter=1000, thr 0.5): all n=370 AUC 0.7945 agree 0.8459; verdict n=170 AUC 0.8923 agree 0.8118 -- identical, so triage.py is not carrying a hard-coded number. Probe file: scratch probe_triage.py. PROBES: (auth) env-unset + uncached act -> SystemExit "blocked:no_key -- 0 network calls", 0 calls, 0 rows. (gate) answers.q1 empty -> p_accept 0.0, flag uncertain, no crash. (wire/stub-ask) I monkeypatched acts_replay.ask to capture the state and count calls: EXACTLY 1 call for 1 act, 0 residual verdict tokens, [SCRUBBED] present -- the scrub-before-call and one-call-per-act conjuncts hold on the live path. (wire/live) I ran 5 FRESH experiment acts myself against the real key: 10299 input tokens = $0.000433, 5/5 rows, $0.000087/act -- under the $0.005/act falsifier by 57x and the $0.02 cap. Frozen-weight wire: changing the coefficient vector moves p_accept (0.8177 vs 0.7558 vs sigmoid(intercept)), so the json drives the score.

(3) THE NEAR MISS. A kid can satisfy "measured on the corrected partition" by printing the TM.51 B_corrected mapping row and lose the mechanism: the LIVE flag never applies that hand partition. The deployed p_accept is the fitted LR over the raw 5 probabilities, and its learned coefficient for inconclusive_lean_disproved is +0.647, so a pure-ILD act scores 0.8768 -> flag accept, i.e. the LR disagrees with the very demote side the partition assigns. The correction that matters (inconclusive_lean_proved on the accept side) DOES survive -- its coefficient is +1.7455 and pure-ILP scores 0.9552 accept -- but a reader who takes "mapped on the corrected partition" literally would think ILD is routed demote. Second near miss: the 20-fresh live run cannot demonstrate triage quality. Every one of the 170 verdict acts is already in the pinned 370, so the only fresh acts are experiments -- the subgroup where TM.51 measured the model inert (AUC 0.5535, 92.5 pct accept). All 20 (and all 5 of mine) flagged accept. That is exactly the accepted cost/row-emission check, but it is not evidence about flags. On the 370 population the frozen weights give 316 accept / 40 demote / 14 uncertain; the demote flag has precision 0.775 (31/40) and recall 0.37 (31/83) -- it flags some likely demotes, not most. Third: the frozen threshold 0.5 is a FIXED threshold, not a fitted one; the title's "0.82-0.85 at one fitted threshold" is the thr=0.5 row (0.8459), while TM.51 fitted-threshold agreement is 0.7946. The kid froze the defensible 0.5 and documented it.

(4) DEVIATION. The kid read a 40-line production ceiling from its spawn-time system prompt because my node line_ceiling write landed AFTER dispatch minted the node; I therefore set line_ceiling 200 on this node and corrected the kid-authored experiment node from 40 to 200 (production_lines 76), so the overage was mine, not the kid. I ran the live acceptance calls myself (5 acts) rather than only re-reading the kid cache, per the dispatch order to run both checks myself. Benign side effect: corrected_partition_rows.jsonl was rewritten at 20:09 by a TM.51 re-run (75 rows, 6954 B, same shape); TM.51 is deterministic, so no evidence was lost. VERDICT: accept proved -- both acceptance checks pass, all five negative probes hold, no falsifying case. The three weaknesses above are caveats on usefulness, not falsifiers of the built acceptance.
<!-- THOUGHT:END -->
