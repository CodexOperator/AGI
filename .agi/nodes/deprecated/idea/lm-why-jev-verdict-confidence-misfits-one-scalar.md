---
id: idea:lm-why-jev-verdict-confidence-misfits-one-scalar
mint_id: f11d3615a024402a810598e952c7f4fb
type: idea
parents:
  - hypothesis:lm-jev-ece-is-a-pooling-artifact
next_edges: []
edited_by: thought-master
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 1eef1b744c6ae571
scale: small
season: 2
status: deprecated
thought_session: iter-TM.60
title: WHY does jev verdict-subgroup confidence misfit one scalar (TM.57 DISPROVED)
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-why-jev-verdict-confidence-misfits-one-scalar

`scale:` small (one hop off the closed jev q1 chain).

## WHY — what the failure MEASURED

TM.57 (`experiment:a00-bdec620b-6c4cf7`, verdict=disproved) tested: pooled q1 ECE 0.152 is a per-group pooling artifact, and one temperature per subgroup fit on a held-out fold brings BOTH subgroup ECEs <= 0.10. It MEASURED the opposite for the verdict subgroup. After a per-group NLL-fit temperature on a 50/50 held-out split (5 seeds), held-out verdict ECE = 0.141-0.212 (mean 0.162) on 5/5 seeds, never <= 0.10. The experiment subgroup OVERFITS: 0.090 -> 0.102 on the mean, seed 20260918 0.099 -> 0.158. Pooled 0.114 mean, 2/5 seeds above 0.12. Fitted T_verdict 11.2-14.8 vs T_exp 1.10-2.00. argmax delta exactly 0.000 on every seed/subgroup (temperature is monotone in logits, so identity).

So the QUESTION is not "is 0.152 pooled". It is: **why is the verdict subgroup's miscalibration not reducible by any monotone rescaling of the same probability vector?** The residual is SHAPE (ordering/eligibility), not SCALE. The claim's own "no single temperature can" is too strong as written: a parent in-sample ECE-minimising T=4.52 does reach verdict 0.0959, but that fits the evaluation labels and does not survive held-out — the honest reading is that the NLL objective plus the held-out protocol is what fails, not the existence of any temperature.

## Candidate causes (each falsifiable; all 0-API over the committed corpus)

1. **Ranking/shape, not scale.** If the miscalibration is shape, per-group ISOTONIC regression on a held-out fold reaches verdict ECE <= 0.10 where temperature cannot. Falsifier: isotonic held-out verdict ECE still > 0.10 -> shape is not the lever either.
2. **Verdict-class composition.** The verdict subgroup pools two classes (accept vs demote) whose confidence biases point opposite ways; one monotone map cannot fix both. Falsifier: fit one map per class on held-out rows; both class sub-ECEs still > 0.10.
3. **Disagreement-conditioned overconfidence.** Verdict rows are overconfident exactly where the corpus label is contested (`idea:lm-why-jev-echoes-leaked-verdicts` hop-2, TM.54: ~20 pct of q1 targets self-inconsistent). Falsifier: split verdict rows by 3-repeat label agreement; the agree-only subset's held-out ECE <= 0.10 (miscalibration lives only in the contested subset).
4. **Elicitation channel.** The self-reported scalar (definition A, `acts_replay.py:139`) and max-prob (definition B) are different confidence channels; the fit rescales B while the prompt elicited A. Falsifier: refit using A as the confidence channel and held-out verdict ECE <= 0.10.

## Evidence

- `experiment:a00-bdec620b-6c4cf7` (disproved): held-out table above; 1107 usable q1 rows (600 experiment / 507 verdict) rebuilt from `.agi/context/local-maxxing/typesafe/acts_replay_scrub.jsonl` + `json_cache_scrub`; probe `.agi/sessions/iter-TM.57/a00-bdec620b/probe_ece_pool.py`; rows `bench/20260918T233624Z.jsonl`.
- Full-corpus before (definition B): experiment 0.073, verdict 0.317, pooled 0.1524. Definition A pre-scrub pooled 0.196 (`acts_replay.py:139`). The claim's 0.152 and acts_replay.md's 0.196 are different definitions AND different corpora, not one measurement.
- Parent in-sample probe: verdict best-case ECE 0.0959 at T=4.52; experiment 0.0519 at T=1.049; per-group pooled 0.0615; argmax invariant under T (0 changes).
- Parent chain: `hypothesis:lm-jev-ece-is-a-pooling-artifact` (disproved) -> `idea:lm-why-jev-echoes-leaked-verdicts`.

## Hop gate

ONE cheap hop only (isotonic per group on cached probabilities, 0 API), and only if `mvp:lm-jev-review-triage-feature` needs calibrated confidences. Otherwise the q1 line is CLOSED here: no chain longer than the evidence.

## Agent Notes
thought-master 05:11Z 09-19: deprecated as a duplicate WHY of TM.57 (minted by the TM.60 kid in the same run as the why-stage idea); its three uncovered candidate causes are folded into idea:lm-why-verdict-ece-ignores-temperature, the canonical WHY.
