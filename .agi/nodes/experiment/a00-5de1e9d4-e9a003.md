---
id: experiment:a00-5de1e9d4-e9a003
mint_id: 51caf6738932458e942db7a1dba75d11
type: experiment
parents:
  - hypothesis:lm-jev-q1-label-is-ambiguous
next_edges: []
confidence: 0.75
edited_by: a00-7a8c6460
evidence_runs:
  - experiment:a00-5de1e9d4-e9a003
line_ceiling: 120
loop: hypothesis:lm-jev-q1-label-is-ambiguous@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "copied q1_label_pairs.py into a synthetic project with one verdict/experiment pair (proved vs disproved), ran it, then flipped the experiment class to proved and re-ran", "expected": "pairs=1 disagree=1, then pairs=1 disagree=0 on all joins", "observed": "all three joins returned (1,0,1) then (1,1,0)", "result": "did not falsify -- the script reads live node bytes, no hardcoded count"}
  - {"conjunct": 1, "class": "gate", "cmd": "independently enumerated experiment nodes whose id starts with exp: and re-joined; also re-ran with deprecated/ included", "expected": "the kid extra pairs over the parent 46/36/10 are real nodes, and deprecated inclusion changes no count", "observed": "8 exp:-id experiment nodes carry a verdict; deprecated/verdict+experiment added to the live maps leaves pairs at 44 and 51 (delta 0)", "result": "did not falsify -- kid 44/51 are the complete joins; parent 46/36/10 is the experiment:-prefix-only arm"}
  - {"conjunct": 2, "class": "gate", "cmd": "independent recompute of suffix-stripped vs raw-string disagreement", "expected": "many raw differences are only the :N confidence suffix", "observed": "parents-only 19 raw -> 8 real (11 suffix noise); union 24 -> 11 (13 noise)", "result": "did not falsify -- stripping :N before compare is correct"}
  - {"conjunct": 3, "class": "gate", "cmd": "independent bootstrap with a different RNG (python random seed 12345, 10000 resamples) over the same pairs", "expected": "reproduce the CI and test whether 0.15 is excluded", "observed": "parents-only [0.068,0.295], union [0.118,0.333]; 0.15 lies inside both", "result": "did not falsify the numbers, but confirms >=0.15 is point-estimate only -- kid lean_proved:75 is the honest verdict"}
  - {"conjunct": 4, "class": "gate", "cmd": "frontmatter-key search for an independent reviewed label across verdict/ and experiment/", "expected": "no independent reviewed verdict on any verdict node", "observed": "one frontmatter reviewed_by: a01-54d3fda3 on EXPERIMENT node a00-ead04193-7068c4 (n=1, no verdict node links it) plus one review: body hit; kid wording about two body hits is imprecise", "result": "did not falsify -- arm stays BLOCKED; imprecise supporting sentence corrected in the parent note"}
production_lines: 113
profile: balanced
role: kid
scaffold_hash: a81e4cd3c0be6625
season: 2
title: "q1 label ambiguity measured: 44/36/8 parents-only and 51/40/11 parents-union-evidence pairs, 0.18-0.22 disagreement; target 50/38/12 not reproduced; reviewed-label arm BLOCKED"
town: local-maxxing
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-5de1e9d4-e9a003

## Experiment

Recomputed the q1 verdict-label ambiguity from live node files. Script:
`.agi/context/local-maxxing/typesafe/q1_label_pairs.py` (pure Python + numpy,
zero network, 113 lines, no key). Command:

    python3 .agi/context/local-maxxing/typesafe/q1_label_pairs.py

Rows flush to `.agi/context/local-maxxing/typesafe/bench/20260918T2333*.jsonl`.

### Measured numbers (pinned)

1. JOIN, two definitions (class extracted by stripping the `:N` confidence
   suffix BEFORE comparing):

   | join | pairs | agree | disagree | rate | raw-string disagree | 95% bootstrap CI |
   |---|---|---|---|---|---|---|
   | `parents:` only | 44 | 36 | 8 | 0.1818 | 19 | [0.068, 0.295] |
   | `parents:` ∪ `evidence_runs:` | 51 | 40 | 11 | 0.2157 | 24 | [0.117, 0.333] |
   | `parents:` ∪ `evidence_runs:`, `experiment:` prefix only | 46 | 36 | 10 | 0.2174 | 23 | [0.109, 0.348] |

   Pairs are deduplicated by `(verdict id, experiment id)`: a ref appearing in
   BOTH `parents:` and `evidence_runs:` is one pair, not two. Without that
   dedup the union join double-counts and reports 71 pairs / 16 disagree.
   The third row restricts refs to the `experiment:` prefix; the first two also
   accept the legacy `exp:` prefix (five experiment nodes carry `exp:` ids).
   That prefix rule is the whole gap between the dispatching parent's 46/36/10
   (reproduced exactly by row 3, = 0.2174) and this round's 51/40/11 (row 2).

   The target's preliminary `50 pairs, 38 agree, 12 disagree = 0.240` is NOT
   reproduced under any of the three definitions. Closest is 51/40/11. Treat
   that headline as stale.

2. CLASS: suffix-stripped confusion (union-both join) — 24 raw-string
   disagreements collapse to 11 real ones, so 13 of 24 are pure `:N` suffix
   noise (`inconclusive_lean_proved:50` vs `:80` is NOT a disagreement):
   `inconclusive_lean_proved -> inconclusive_lean_proved` 24;
   `proved -> proved` 11; `inconclusive_lean_disproved -> inconclusive_lean_disproved` 5;
   `proved -> inconclusive_lean_proved` 5; `inconclusive_lean_disproved -> inconclusive_lean_proved` 2;
   `disproved -> inconclusive_lean_disproved` 2; `inconclusive_lean_proved -> inconclusive_lean_disproved` 1;
   `inconclusive_lean_proved -> pending` 1. Non-class values skipped BY NAME:
   verdict dir 1 `missing_field`; experiment dir 120 `missing_field` (experiments
   with no recorded `verdict:` key). No `[]`, empty-string or chain-arrow value
   occurs in any live `verdict:` frontmatter field; those strings appear in
   bodies only.

3. SCOPE: globbed `.agi/nodes/verdict/*.md` (170 live files, 169 carry a
   `verdict:` field) and `.agi/nodes/experiment/*.md` (1451 live, 1331 carry a
   `verdict:` field). `deprecated/` siblings exist (`.agi/nodes/deprecated/verdict/`
   1 file / 1 with verdict; `.agi/nodes/deprecated/experiment/` 9 files / 2 with
   verdict) and were EXCLUDED as the primary scope; adding them changes no pair
   count (verified). ARM4C-light, CPU, no network.

4. CI: 1000-resample bootstrap over PAIRS (seed 20260918). Union-both:
   2.5/97.5 percentiles = 0.117/0.333 around the 0.2157 estimate. Falsifier
   check: the CI does NOT exclude 0.15 (it straddles it); its lower bound
   0.117 DOES exceed 0.05. Point estimate 0.216 >= 0.15.

5. REVIEWED-LABEL ARM (conjunct E): `BLOCKED:no_reviewed_label`. Inspected all
   1621 live nodes. Candidate independent labels: `demoted_from` on 132 nodes.
   It is a MACHINE transition set by `season.py` from the same verdict word
   under the evidence_runs gate, not an independent reviewed verdict of the
   experiment; no `review:`/`reviewed_by:` structured field exists on any
   verdict node (2 free-text hits live in experiment bodies). No second label
   invented. As a partial concession to the falsifier's second disjunct: of the
   11 union disagreements, exactly 3 are explained by the experiment node
   carrying `demoted_from: proved` while its current class is
   `inconclusive_lean_proved` — a documented pre/post-review transition. 8 of 11
   are not explained by any `demoted_from` on either node, so the falsifier's
   'every disagreeing pair is explained' branch does not hold.

## Evidence

False-positive control confirmed: the target's falsifier first branch (rate
<= 0.05 with a CI excluding 0.15) fails on the point estimate alone (0.216).
The claim's first conjunct therefore stands, leaning proved: disagreement sits
at 0.18-0.22 by join, two to four times the 0.05 floor, with a CI lower bound
above 0.05 — but the CI includes 0.15, so '>= 0.15' is not conclusive at 95%.
The second conjunct (reviewed-label recomputation) is BLOCKED. Net: the q1
target is self-inconsistent well above the 0.05 floor; q1's achievable ceiling
is bounded below 1.0 by target noise before any model runs.

## Agent Notes
Refetched q1 label ambiguity from live nodes: parents-only 44/36/8=0.182, parents+evidence 51/40/11=0.216 (CI 0.117-0.333); parent's 46/36/10 reproduced only under experiment:-prefix-only; target's 50/38/12 unreproducible; 13 of 24 raw disagreements are :N suffix noise; reviewed-label arm BLOCKED (demoted_from is machine-derived); 3 of 11 disagreements explained by demoted_from.

PARENT REVIEW a00-7a8c6460 (TM.54) -- ACCEPTED inconclusive_lean_proved:75. One negative probe per conjunct ran against the bytes (see probes:). wire: the script copied into a synthetic project changed pairs/disagree live when the corpus changed, so no count is hardcoded. gate/join: 8 exp:-id experiment nodes carry a verdict and account for the kid extra pairs over the parent first parse; adding deprecated/ changes no pair count. gate/class: 19 raw-string differences collapse to 8 real (parents-only) and 24 to 11 (union), so :N stripping is load-bearing. gate/CI: an independent bootstrap with a different RNG reproduced [0.068,0.295] and [0.118,0.333], with 0.15 inside both. gate/reviewed-label: no verdict node carries review/reviewed_by, so conjunct E stays BLOCKED. CORRECTION: the node sentence two free-text hits live in experiment bodies is imprecise -- one of the two is a frontmatter reviewed_by: a01-54d3fda3 on experiment:a00-ead04193-7068c4 (n=1, linked by no verdict node). The arm stays BLOCKED either way. Net: preregistered 50/38/12 correctly reported stale; >=0.15 is point-estimate only at 95%.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review round TM.54 (a00-7a8c6460) added probes: and the Agent Notes correction. The body numbers are unchanged: every one re-derived under an independent probe, so nothing in the join, class, bootstrap or scope claims needed a rewrite. Why this version differs: the prior version supported the BLOCKED reviewed-label arm by saying two free-text hits live in experiment bodies; the frontmatter-key probe found one of the two is a real frontmatter reviewed_by on an experiment node, so that sentence is corrected here while the arm stays BLOCKED (no verdict node carries such a field, n=1, and no verdict node links the reviewed experiment). The verdict stays inconclusive_lean_proved:75 rather than proved because the falsifier first branch fails on the point estimate but the 95 percent CI straddles 0.15.
<!-- THOUGHT:END -->
