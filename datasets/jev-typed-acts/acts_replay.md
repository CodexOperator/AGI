# acts_replay -- hypothesis:lm-jev-typed-acts-replay

MODEL=jev-1.13.0 (pinned); SEED=20260918; REPEATS=3; state = node BODY only, frontmatter stripped, cap 128k chars.
Corpus: 370 acts = 170 verdict + 200 experiment.

| question | recorded | agree | base | repeat-flip | ECE |
|---|---|---|---|---|---|
| q1 | 369 | 0.743 | 0.507 | 0.011 | 0.196 |
| q2 | 370 | 0.492 | 0.776 | 0.016 | 0.270 |
| q3 | 370 | 0.989 | 0.995 | 0.000 | 0.121 |
| q4 | 22 | 0.909 | 0.591 | 0.000 | 0.158 |
| q5 | 0 | 0.000 | 0.000 | 0.000 | 0.000 |

TypeSafe spend: $0.076246 = 1815381 input tokens x $0.042/Mtok (cap $0.50; output free per trove).
TYPESAFE_KEY len omitted; endpoint https://api.typesafe.ai/v1/systemone; no host/model/key id written.

## Data gates (named, not padded)

- merge-up-review.jsonl does not exist on this box; review decisions are not a structured corpus (only ~15 accept_with_residue occurrences across all rotation records). Rows here carry accept/demote labels derived from the recorded `demoted_from` field instead.
- rebrief answers: only 8-10 nodes carry `rebrief_request` in this checkout, not 50; q3 is scored on those records.
- Creation timestamps are absent from node files and `mtime` is uniform after checkout; `git log` is forbidden by the kid contract, so held-out is a seeded draw over the whole live corpus (seed above) rather than a literal post-2026-09-15 cut.

## Response health (1110 calls = 370 acts x 3 repeats)

| metric | value |
|---|---|
| HTTP 200 | 1110 / 1110 |
| response model id | jev-1.13.0 on every call |
| 403 / 422 / 429 / 529 | 0 / 0 / 0 / 0 |
| latency p50 / p95 | 0.633 s / 0.804 s |
| input tokens total | 1815381 |
| input tokens per act | 4906 (1110 calls / 370 acts = 3 repeats) |
| spend | $0.076246 = 1815381 x $0.042/Mtok, cap $0.50 (15 percent used) |

## Confusion, q1 verdict class (majority of 3 repeats, n=369)

| recorded | predicted | count |
|---|---|---|
| proved | proved | 139 |
| inconclusive_lean_proved | inconclusive_lean_proved | 103 |
| inconclusive_lean_proved | proved | 73 |
| inconclusive_lean_disproved | inconclusive_lean_disproved | 22 |
| inconclusive_lean_disproved | disproved | 7 |
| inconclusive_lean_proved | pending | 6 |
| pending | pending | 6 |
| disproved | disproved | 4 |
| inconclusive_lean_proved | inconclusive_lean_disproved | 4 |

All errors concentrate on the proved <-> inconclusive_lean_proved boundary:
73 lean-proved acts are called proved, and 4 lean-proved are called
lean-disproved. The six-word taxonomy collapses at the lean boundary.

## Confusion, q2 accept-vs-demote (n=370)

| recorded | predicted | count |
|---|---|---|
| accept | accept | 161 |
| accept | demote | 126 |
| demote | accept | 62 |
| demote | demote | 21 |

Majority baseline (always accept) = 0.776. jev = 0.492, i.e. WORSE than the
constant by 28 points. Demote precision = 21/147 = 0.14, recall = 21/83 = 0.25.
Over-prediction of demote is the failure: 126 of 223 accepted acts are called
demote. As a gate this would demote twice as much real work as it correctly
demotes.

## Falsifier check (OR -- any one trips)

| condition | measured | trips |
|---|---|---|
| any question top-1 < 0.60 | q2 = 0.492 | YES |
| ECE > 0.15 | q1 = 0.196 | YES |
| argmax flips > 5 percent of acts | q1 = 1.1 percent, q2 = 1.6 percent | no |
| spend > $0.50 per 1000 acts | $0.206 per 1000 acts | no |

FALSIFIER TRIPPED. q1 also misses the 0.75 success bar (0.743) and q4 is
scored on only 22 records. Repeat stability itself PASSES (1.1-1.6 percent
flips), so the endpoint is effectively deterministic; the failure is accuracy
and calibration, not nondeterminism.

## Leakage caveat (must not be read past)

State = node body only, but 1094 of 1473 corpus node bodies (74 percent)
literally contain their own `verdict:` word in the body text. q1 agreement
0.743 tracks that leakage rate almost exactly, so q1 is not evidence that jev
inferred the class -- it may be reading a word the body already prints, and
still missing it a quarter of the time. q2/q3/q4 labels have no such leak.
