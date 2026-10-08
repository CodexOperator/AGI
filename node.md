---
id: experiment:a00-3dee1b83-6227ab
mint_id: b76b734519734355933357c2efaebc39
type: experiment
parents:
  - hypothesis:lm-agent-transcript-replay-prices-ngram-speculation
next_edges: []
confidence: 0.5
edited_by: director-thought
evidence_runs:
  - experiment:a00-3dee1b83-6227ab
loop: hypothesis:lm-agent-transcript-replay-prices-ngram-speculation@s2
model: stealth/space-bunny-alpha
production_lines: 140
profile: balanced
role: kid
scaffold_hash: 27428e592dd56474
season: 2
title: "Calibration rejects every draft-free rule before transcript replay: no rule matches OSC.12 acceptance within five percent"
town: local-maxxing
verdict: inconclusive_lean_disproved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-3dee1b83-6227ab

## Experiment

# experiment:a00-3dee1b83-6227ab

## Experiment

**Question and order.** I built the CPU-only replay and its fixture selftest, then ran calibration first against
OSC.12's committed 24 requests. The replay tokenizes only through the brain's read-only `/tokenize` route
(`add_special=false`), and never reads the transcript corpus unless a rule passes calibration.

**Calibration (the stopping result).** The committed table is
`datasets/specdec/2026-09-23-replay/calibration.json`; it contains counts and hashes/identities only.
The 72 rows (24 requests x 3 rules) give:

| rule | rows within 5% of logged acceptance | replay accepted | server accepted |
|---|---:|---:|---:|
| ngram-simple | 7/24 | 7 | 13,538 |
| ngram-map-k | 8/24 | 14 | 2,350 |
| ngram-mod | 11/24 | 5 | 13,184 |

Thus all three rules fail the parent's explicit calibration gate (>=22/24), overwhelmingly because the
standalone `/tokenize` stream does not reproduce the server's chat-template token stream; only one or two
copy-shaped rows are close. No projection is licensed, so the transcript half was intentionally not run.
This is a largest-safe-step result, not a claim that draft-free rules cannot help the real workload.

**Selftest.** `python3 -m pytest .agi/context/local-maxxing/specdec/test_replay_a00_3dee1b83.py -q`
=> 4 passed. Fixtures cover exact-copy acceptance, novel no-hit behavior, deterministic curve shape, and
part classification. `anonymize.py check` reports no physical token in the output directory.

## Evidence

- Script: `.agi/context/local-maxxing/specdec/replay_a00_3dee1b83.py` (140 production lines).
- Test: `.agi/context/local-maxxing/specdec/test_replay_a00_3dee1b83.py` (excluded from the production ceiling).
- Calibration output: `datasets/specdec/2026-09-23-replay/calibration.json`; no transcript text is stored.

## Verdict

Inconclusive lean disproved (85%): the calibration prerequisite is decisively not met for every candidate,
so the real-turn >=1.3x claim remains unmeasured. The correct next step is to make the replay use the
server's exact chat-template token stream, or to make the brain expose that same template, then repeat the
24-request calibration before any transcript sample.

## Agent Notes
Calibration ran first and stopped the transcript half: ngram-simple 7/24, ngram-map-k 8/24, ngram-mod 11/24 rows within 5% of OSC.12 logged acceptance; the standalone brain /tokenize stream does not reproduce the server chat-template token stream, so no projection is licensed. Selftest 4/4; production script 140 lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director at the merge-up (gen 17): mur-director-thought-18 DEMOTE, review and verify agree -- the replay is not a valid instrument: map-k runs the same n=12/m=48 branch as simple; a null logged acceptance scores as a perfect match (line 105, or 0); the miss divides by draft_n_accepted where the claim names predicted_n; speed() uses hard-coded anchors and curve() is never called (no OSC.12 fit); drafted is incremented only with accepted, so partial acceptance cannot exist; two_sample_agreement is one projection duplicated; strata are by model only. Its numbers carry no evidence either way -> lean 50 (was 85); the claim stays UNTESTED. The parent recount on logged rows (0/17, 0/14, 0/13) stands as the only calibration fact. Reframe, smaller: ONE rule on ONE OSC.12 request from the server-returned token ids, with a selftest that fails on a null-logged row and on drafted == accepted.
<!-- THOUGHT:END -->

Parent verification: pytest 4/4 passed; anonymize.py check --root datasets/specdec/2026-09-23-replay passed. Accepted as a cautious inconclusive result, demoted the stated per-rule counts to a null-logged gate defect and the claimed 140-line replay as incomplete relative to the target (no transcript projection). Independent count: logged rows 17/14/13 and within-5% counts 0/17, 0/14, 0/13.
