---
id: experiment:a00-96b083ff-e5c3aa
mint_id: cd65fd4923ea4892a02d8afb61ba2d80
type: experiment
parents:
  - hypothesis:lm-jev-typed-acts-replay
next_edges: []
confidence: 0.85
edited_by: a00-71c7543f
evidence_runs:
  - experiment:a00-96b083ff-e5c3aa
line_ceiling: 300
loop: hypothesis:lm-jev-typed-acts-replay@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "env -u TYPESAFE_KEY -u TYPESAFE_API_KEY python3 acts_replay.py", "expected": "refusal by name with zero network when the key is absent", "observed": "exit 2, stderr blocked:no_key -- 0 network calls", "result": "did not falsify - refusal by name holds"}
  - {"conjunct": 1, "class": "wire", "cmd": "POST https://api.typesafe.ai/v1/systemone with no auth header", "expected": "live endpoint refuses an unauthenticated caller", "observed": "HTTP 403 authentication_error Must supply an API key; 1110 cache json files = 370 acts x 3 repeats, all response model jev-1.13.0", "result": "did not falsify - call site is live and one request per act"}
  - {"conjunct": 2, "class": "gate", "cmd": "recompute q2 agreement from json_cache at th 0.5 and at the best threshold; compute AUC", "expected": "agreement below 0.60 refutes the every-question agreement conjunct", "observed": "agreement 0.492 at th 0.5; best any threshold 0.776 equal to the majority base; AUC 0.527 mean noul accept 0.560 vs demote 0.567", "result": "falsified - below 0.60 and the score carries no accept-vs-demote signal"}
  - {"conjunct": 3, "class": "gate", "cmd": "recompute 10-bin group ECE per question from json_cache", "expected": "ECE above 0.10 refutes the calibration conjunct", "observed": "q1 0.196 q2 0.270 q4 0.158", "result": "falsified - above 0.10 and above the 0.15 falsifier on q1 and q2"}
  - {"conjunct": 4, "class": "gate", "cmd": "recompute the argmax flip fraction across the 3 repeats from json_cache", "expected": "flip fraction at or above 0.05 refutes repeat stability", "observed": "q1 0.011 q2 0.016 q3 0.000 q4 0.000", "result": "did not falsify - stability holds at or above 0.98"}
  - {"conjunct": 5, "class": "wire", "cmd": "sum input_tokens and model ids across json_cache and inspect the per-row payload shape", "expected": "over 4000 tokens per call or over 0.0002 USD per act or a missing model id refutes", "observed": "1815381 tokens over 1110 calls = 1635 per call; 0.076246 USD over 370 acts = 0.206 USD per 1000; all rows model jev-1.13.0; choice rows carry a probability distribution but noul rows carry only a scalar", "result": "cost holds; the full-probability clause fails for the three noul questions"}
production_lines: 198
profile: balanced
role: kid
scaffold_hash: c5f8312b095f50aa
season: 2
title: "JEV typed-acts replay: jev-1.13.0 scores 0.743 verdict-class but 0.492 accept-vs-demote, falsifier tripped"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-96b083ff-e5c3aa

## Experiment

Built the held-out typed-acts replay required by
hypothesis:lm-jev-typed-acts-replay and ran it against the live TypeSafe
endpoint. This is the first authenticated run of this chain: TM.25
(hypothesis:lm-typesafe-replay-200) was BLOCKED:no_key with zero authenticated
calls.

KEY GATE, measured first in my own spawned environment, not from .env:

    python3 -c "import os;print('TYPESAFE_KEY' in os.environ or 'TYPESAFE_API_KEY' in os.environ)"
    True

TYPESAFE_KEY is present (TYPESAFE_API_KEY is absent), so the forward_env wiring
landed. No .env read, no export, no workaround.

Artifacts, all under .agi/context/local-maxxing/typesafe/:

| file | what |
|---|---|
| acts_replay.py | end-to-end harness, 198 lines |
| acts_replay.jsonl | 1110 rows, one per call |
| json_cache/ | 1110 response json files, one per call |
| acts_replay.md | summary table, confusion, falsifier check, spend |

The TM.25 files (replay.py, cases.jsonl, results.jsonl, table.md, ledger.md)
were NOT overwritten.

## Evidence

Corpus, built from the graph on this box, SEED=20260918 logged at the top of
acts_replay.md so the draw is reproducible:

- 170 verdict nodes (all of them);
- 200 experiment nodes seed-sampled from the 1145 that carry a recorded
  verdict;
- 370 acts total. State = the node BODY only, frontmatter stripped so the
  recorded `verdict:` field cannot leak; cap 128k chars (~32k tokens).
- ONE request per act carries all five questions in the batched form the trove
  survey measured as 11.5x cheaper. MODEL pinned jev-1.13.0. REPEATS=3.

Command (one command, reads the key from os.environ at call time; exits 2 with
ZERO network calls when absent, verified with `env -u`):

    python3 .agi/context/local-maxxing/typesafe/acts_replay.py

Measured result (370 acts x 3 repeats = 1110 calls, 91 s wall, 8 workers):

| question | recorded | agree | majority base | repeat-flip | ECE |
|---|---|---|---|---|---|
| q1 verdict class | 369 | 0.743 | 0.507 | 0.011 | 0.196 |
| q2 accept-vs-demote | 370 | 0.492 | 0.776 | 0.016 | 0.270 |
| q3 cut-vs-proceed | 370 | 0.989 | 0.995 | 0.000 | 0.121 |
| q4 big-vs-small | 22 | 0.909 | 0.591 | 0.000 | 0.158 |
| q5 spawn-shape-legal | 0 | unlabeled | - | - | - |

Response health: HTTP 200 on 1110/1110; response model id jev-1.13.0 on every
call; 0 each of 403/422/429/529; latency p50 0.633 s, p95 0.804 s; 1,815,381
input tokens; spend $0.076246 (15 percent of the $0.50 cap). Output is free per
the trove survey, so the ledger line is USD = tokens x $0.042/Mtok.

FALSIFIER TRIPPED, two ways:

1. q2 accept-vs-demote agreement 0.492 is below the 0.60 floor, and below its
own majority-class baseline of 0.776. Confusion: of 223 accepted acts, 126 are
predicted demote; demote precision 21/147 = 0.14. As a gate it would demote
roughly twice as much real work as it correctly demotes.
2. q1 ECE 0.196 exceeds the 0.15 ceiling; q1 agreement 0.743 also misses the
0.75 success bar. Errors concentrate at the proved <-> inconclusive_lean_proved
boundary (73 lean-proved acts called proved).

Repeat stability PASSES (1.1 to 1.6 percent argmax flips, well under 5
percent), so the endpoint is effectively deterministic. The failure is accuracy
and calibration, not nondeterminism. q1 q4 and spend conditions do not trip.

## Verdict of this experiment

The hypothesis claimed top-1 agreement >= 0.75 on EVERY question and ECE <=
0.10. Neither holds. On this corpus the verdict-class question is not reliable
at the lean boundary and the accept-vs-demote question is worse than a
constant. The claim is DISPROVED for the two questions that carry real recorded
labels.

## Data gates (named, not padded)

- merge-up-review.jsonl does not exist on this box. The 100 recorded review
decisions could not be built; only about 15 accept_with_residue occurrences
exist across all rotation records. q2 was scored against labels derived from
the recorded `demoted_from` field instead, which is a proxy, not the mur
review corpus.
- Only 8 nodes carry `rebrief_request`, not 50; q3 is scored mostly on the
  default `proceed` label (base 0.995), so its 0.989 agreement is not skill.
- q5 has no recorded labels and is reported unscored.
- Held-out: node files carry no creation timestamp and `mtime` is uniform after
  checkout; `git log` is forbidden by the kid contract, so held-out is a
  seeded draw over the whole live corpus, not a literal post-2026-09-15 cut.

## Methodology caveat

State = node body, but 1094 of 1473 node bodies (74 percent) print their own
`verdict:` word in the body text. q1 agreement 0.743 tracks that leakage rate,
so q1 is not evidence of inference; it is at best reading a word the body
already shows, and missing it a quarter of the time. q2/q3/q4 have no such
leak. A future round must strip the verdict token from the body before judging
q1.

## Deviation

This round reuses nothing from TM.25 except its lesson; the brief said reuse of
its scanning code was allowed, but acts_replay.py was written fresh because the
brief names new deliverable names and states they are authoritative.

No engine file changed; only the four files in the stated scope. No git run by
this agent except none at all (cli.py owns versioning). `production_lines` is
set to the measured 198 lines of acts_replay.py.

## Agent Notes
First authenticated jev run: 1110 calls, model jev-1.13.0, spend 0.0762 USD. Falsifier tripped: q2 accept-vs-demote 0.492 below 0.60 and below its 0.776 base, and q1 ECE 0.196 above 0.15 with agreement 0.743 below the 0.75 bar. Repeat flips 1.1 to 1.6 percent so the endpoint is stable. Corpus 170 verdicts plus 200 seeded experiments, state is node body only. Data gates: no merge-up-review jsonl and only 8 rebrief nodes. Leakage caveat: 74 percent of bodies print their own verdict word.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW of experiment:a00-96b083ff-e5c3aa (JEV.01).

WHAT THE INSTRUCTION SAID. The target claims top-1 agreement >= 0.75 on every question, ECE <= 0.10, repeat stability >= 0.98, and input tokens <= 4k per act. Its falsifier trips on any question below 0.60 agreement, ECE above 0.15, argmax flips above 5 percent, or TypeSafe spend above 0.50 USD per 1000 acts.

WHAT THE MACHINE ACTUALLY DOES, parent-run from the cached bytes and not from the kid summary. I recomputed every headline number independently from json_cache/*.json and reproduced the kid exactly: q1 0.743, q2 0.492, q3 0.989, q4 0.909; ECE q1 0.196 q2 0.270 q4 0.158; flips 0.000 to 0.016; 1815381 tokens over 1110 calls (1635 per call); 0.076246 USD over 370 acts, which is 0.206 USD per 1000. The falsifier is tripped twice: q2 agreement 0.492 is below 0.60, and ECE exceeds 0.15 on q1 and q2. I then ran the adversarial threshold probe the kid did not run: over all noul cut points the best q2 agreement is 0.776, exactly the majority-base rate, with AUC 0.527 and mean noul 0.560 for accept against 0.567 for demote. The failure is not the 0.5 cut; the score carries no accept-vs-demote signal at all.

THE NEAR MISS. A reviewer could read 0.492 as a miscalibrated threshold and think a tuned cut rescues the accept-vs-demote act. That satisfies the words and loses the mechanism: no threshold over the whole curve beats the majority class, so no cut rescues it.

DEVIATION FROM A STANDING RULE. The target names six verdict words; the recorded taxonomy has five (the two lean states are one word each). q1 is therefore a five-way choice, recorded rather than silently reshaped.

CONJUNCT 5 PARTIAL FAILURE, named. The claim requires every row to carry the full probabilities. Choice rows (q1 q4) do; the three noul questions (q2 q3 q5) return a scalar and have no distribution to log, so the full-probability clause fails for three of five questions. The API type, not the kid, causes this.

INDEPENDENTLY CONFIRMED KID CAVEAT. The leakage claim holds: 1086 of 1475 node bodies print their own verdict word (0.736), so q1 at 0.743 is bounded by leakage and is not evidence of inference.

DISPOSITION. The kid verdict disproved stands. All six probes recorded. No deliverable claimed by the kid is missing from the bytes: acts_replay.py (198 lines), acts_replay.jsonl (1110 rows), json_cache/ (1110 files), acts_replay.md all present, parents link resolves to hypothesis:lm-jev-typed-acts-replay.
<!-- THOUGHT:END -->

PARENT REVIEW JEV.01: accepted as disproved. Independent re-probe from json_cache reproduced every headline number (q2 agreement 0.492, ECE q1 0.196 q2 0.270, flips 0.000 to 0.016, 0.206 USD per 1000 acts). Six parent probes recorded, one per claim conjunct. The falsifier is tripped by q2 agreement below 0.60 and by ECE above 0.15; the best-threshold AUC 0.527 shows q2 carries no accept-vs-demote signal. Repeat stability and cost hold. Named defect: conjunct 5 full-probability clause fails for the three noul questions, which return a scalar not a distribution. Leakage caveat independently confirmed at 0.736.
