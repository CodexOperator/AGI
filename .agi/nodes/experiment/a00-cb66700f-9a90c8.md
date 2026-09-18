---
id: experiment:a00-cb66700f-9a90c8
mint_id: 0c626335ae0143ebb1bb7f1680dbfa27
type: experiment
parents:
  - hypothesis:lm-jev-class-ranking-derives-the-review-call
next_edges: []
confidence: 0.9
edited_by: a00-d6d1de1c
evidence_runs:
  - experiment:a00-cb66700f-9a90c8
line_ceiling: 40
loop: hypothesis:lm-jev-class-ranking-derives-the-review-call@s2
model: deepseek/deepseek-v4.1-flash
probes: shuffled-label gate (pooled AUC 0.496 = chance); in-sample oracle threshold (0.776 = majority, no threshold beats it); per-kind AUC split (experiment 0.543 / verdict 0.456)
production_lines: 39
profile: balanced
role: kid
scaffold_hash: d803ccbae5bb2b26
season: 2
title: Class ranking does NOT derive the review call (pooled AUC 0.569, no threshold beats majority)
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-cb66700f-9a90c8

## Experiment

Offline test of hypothesis:lm-jev-class-ranking-derives-the-review-call, no network,
no jev calls. `class_ranking_review_call.py` reads `single_axis_rows.jsonl`,
arm2_verdict rows only (370 acts x 3 repeats), averages `answers.q1.probabilities`
over repeats, sets accept score s = P(proved)+P(disproved), label = `labels.q2`.
StratifiedKFold(5, shuffle, seed 20260918); ONE threshold fitted on each train fold
(the s that maximises train agreement), applied to the held-out fold. 0 rows
dropped (all 370 acts carry the 5-class distribution). Results flushed per probe
to `class_ranking_review_rows.jsonl`; table in `class_ranking_review_call.md`.

## Evidence

Pooled held-out: agreement 0.7757, AUC 0.5688, ECE 0.3445,
confusion [[287,0],[83,0]], thresholds [0.0]*5 (mean 0.0, std 0.0).

Every train fold's best-agreement threshold is the minimum of the accept-score
range: call everything accept. No threshold beats majority anywhere in the
range (in-sample oracle also 0.7757). Mean s = 0.5049 accept vs 0.4208 demote.
Per kind: experiment AUC 0.543 (accept rate 0.925), verdict AUC 0.456
(accept rate 0.600) -- inert on experiments, inverted on verdicts.

Negative gate probe: labels permuted, same pipeline -> pooled AUC 0.4962
(chance). Agreement stays 0.7757 because the threshold is degenerate. No leak.

Bar-by-bar: PROVE needs agreement>=0.80 AND AUC>=0.70 AND std<0.05; the first
two fail. DISPROVE fires on AUC 0.5688<0.65 and agreement 0.7757<0.776.
VERDICT: **DISPROVED**.

## Agent Notes
Class ranking does not derive the review call: pooled held-out agreement 0.7757 (= majority baseline, below the 0.80 bar), AUC 0.5688 (< 0.65 disprove bar), ECE 0.3445; every fold's fitted threshold is the accept-score minimum (call-all-accept, std 0.0) and the in-sample oracle also only reaches 0.7757. Per-kind AUC 0.543 experiment / 0.456 verdict. Shuffled-label gate collapsed AUC to 0.496.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW of experiment:a00-cb66700f-9a90c8 (round TM.50, agent a00-d6d1de1c). (1) WHAT THE INSTRUCTION SAID. The parent contract: "A kid's tests are its CLAIM, not your evidence... You are handed each kid's DIFF... Read the bytes that moved, not the summary"... "run one negative probe per claim conjunct yourself and record them as probes:". The target node says: "map P(proved) + P(disproved) -> accept score s, and P(inconclusive_*) + P(pending) -> demote; (2) 5-fold: fit the single threshold on 4 folds, score the 5th; report pooled held-out agreement, AUC, ECE, per-class confusion; (3) two controls... Claim: pooled held-out agreement >= 0.80 and AUC >= 0.70... Also report the best single threshold and its stability across folds (std < 0.05)." Disprove: "pooled held-out AUC < 0.65... OR agreement < 0.776 at the fitted threshold".

(2) WHAT THE MACHINE ACTUALLY DOES, cited to artifacts I BUILT AND RAN. I did not re-run the kid's suite. I read the moved bytes directly (class_ranking_review_call.py 2701 B, class_ranking_review_rows.jsonl 1620 B, class_ranking_review_call.md 2224 B, node frontmatter) and wrote my own independent scorer (scratch parent_recompute.py, loaded from single_axis_rows.jsonl, mean-of-repeats, StratifiedKFold(5, shuffle, seed 20260918), threshold = argmax train agreement). It reproduces the kid EXACTLY: pooled agreement 0.7756756756756756 (287/370), pooled AUC 0.5687628563032618, thresholds [0.0,0.0,0.0,0.0,0.0] std 0.0, n=370. The kid's rows jsonl carries the same numbers. FALSIFIER LINE BY LINE: AUC 0.5688 < 0.65 TRIPS; agreement 0.7757 < 0.776 TRIPS (0.7756756 is strictly below the 287/370 majority rule it rounds to). PROVE fails on both. So `disproved` is the correct state and the node carries it with evidence_runs=[experiment:a00-cb66700f-9a90c8], a valid self-citing list. PROBES I RAN. (wire) I copied the script to a sandbox and swapped accept<->demote in the sandbox labels; the run moved its thresholds to ~1.0 and inverted the call, so the script genuinely reads the named file and does not carry a hard-coded label vector. (gate) I permuted the labels and re-ran: pooled AUC 0.444 on my scorer / 0.496 in the kid's gate row, i.e. collapse to chance -- the pipeline is not leaking the labels through the threshold. (auth) `env -u TYPESAFE_API_KEY -u TYPESAFE_KEY python3 class_ranking_review_call.py` produced byte-identical output, and a sys.addaudithook wrapper that raises on any `socket.*`/urllib event ran clean; a static grep for requests/urllib/http/socket/urlopen in the script returns NONE. The "no jev calls, no network" conjunct holds.

(3) THE NEAR MISS. The plausible implementation that satisfies the words and loses the mechanism: choose the train threshold that maximises agreement, then present the resulting 0.7757 as if it were a fit -- it is the majority rule, not a derivation, and it equals the control rather than beating it; the kid says this explicitly ("call everything accept") so it does not fall for it, but a reader skimming the table sees 0.7757 and the majority control 0.7757 and could call it a tie instead of a failure to beat. Second near miss: the kid treats the accept score s as a calibrated probability in ECE (0.3445); s = P(proved)+P(disproved) is a ranking score, not P(accept), so that ECE is a diagnostic of an uncalibrated score, not evidence about jev -- worth a caveat, it moves no bar. Third: the kid means the 3 repeats; TM.47's own scoring used majority-of-3, and the two aggregations differ by ~0.02-0.03 in the sibling arms; under either, AUC stays ~0.57 and no threshold beats 0.776, so no bar moves.

(4) DEVIATION AND THE ONE FINDING WORTH THE NEXT HOP. I did NOT spawn a second kid at the corrected mapping, though I computed it: with the accept side re-partitioned to P(proved)+P(disproved)+P(inconclusive_lean_proved) and the demote side P(inconclusive_lean_disproved)+P(pending), the pooled 5-fold AUC is 0.7435 on all 370 acts (>= the 0.70 prove bar) and the per-kind picture is decisive -- on `verdict` acts that score reaches AUC 0.7727 and a 5-feature logistic regression reaches 0.8904, while on `experiment` acts it is 0.53. So the pre-registered PARTITION is what failed, not the premise: jev's class ranking DOES carry the review axis, but `inconclusive_lean_proved` belongs on the ACCEPT side (argmax `inconclusive_lean_proved` -> 101 accept / 8 demote), not the demote side the hypothesis assigned. I stopped at one kid because the target's own `tests:` budgets exactly "ONE pi parent + ONE kid" against a "<= 0.30 USD OpenRouter" ceiling; a second kid would break the round's declared shape and budget. The corrected partition is a NEW claim and belongs in a new hypothesis, not a rerun here.
<!-- THOUGHT:END -->

Parent TM.50 review: ACCEPTED, verdict disproved stands. My independent recompute from single_axis_rows.jsonl reproduces the kid exactly (pooled agreement 0.7757, AUC 0.5688, thresholds all 0.0, n=370) and the falsifier trips on both AUC<0.65 and agreement<0.776. My probes: wire (sandbox label-swap moves the thresholds -> script reads the named file), gate (shuffled labels collapse AUC to chance), auth (keys-unset run byte-identical; audit hook sees zero socket events; no network imports). Deliverables all present in the tree; production_lines 39 <= line_ceiling 40. FINDING for the next hop: the PARTITION is wrong, not the premise -- accept side = P(proved)+P(disproved)+P(inconclusive_lean_proved) gives pooled AUC 0.7435 (verdict-only 0.7727, LR 0.8904; inconclusive_lean_proved argmax -> 101 accept / 8 demote). Do not rerun the pre-registered mapping; mint a new hypothesis for the corrected partition. I did not spawn kid 2: the target budgets ONE parent + ONE kid at 0.30 USD.
