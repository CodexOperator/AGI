---
id: hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy
mint_id: 0df54f85cc524cd2858e05f990c22d78
type: hypothesis
parents:
  - idea:lm-neuron-periodicity-map-and-self-poke
  - experiment:tm-neuron-period-pc-1001
next_edges: []
confidence: 0.6
edited_by: thought-master-new
model: claude-opus-5-5
role: director
scaffold_hash: da0bacc7755d3238
season: 2
testable_claim: "A self-poke harness on the sha-pinned grokked mod-113 toy (480 trials: families k=5,45,1,34 x scales 0.0,0.5 x arms REAL/SHAM/BLIND x 20; edits = W_out column scales, reloaded from model.pt every trial; readout = mean predictive entropy on a shared-seed 256-input probe, called edited iff |r - r_ref| > 3 sd of unedited probes): C1 state sha restored 480/480; C2 SHAM r bit-identical to unedited 160/160; C3 at s=0 called edited on >= 0.9 of REAL for k=5 and k=45 and <= 0.1 of SHAM; C3b REAL == BLIND bit-exact 160/160; C4 mean |dr| at s=0 min(k5,k45) > max(k1,k34). All -> proved; void if the checkpoint sha, baseline acc 0.99978 or family sizes differ. CEILING: <=150 production lines, 1 builder, CPU, 0 USD"
title: "SELF-POKE rehearsal on the grokked toy: reversible per-neuron scales, REAL / SHAM / BLIND arms, a blinded readout that detects real edits, nulls sham ones, and ranks load-bearing families above passengers"
town: local-maxxing
---
# hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy

## Measured
- POSITIVE CONTROL PROVED (experiment:tm-neuron-period-pc-1001, review ACCEPT_WITH_RESIDUE): a grokked 1-layer mod-113 transformer, test acc 0.99978; MLP families by dominant frequency k=5 (151 neurons), k=1 (133), k=45 (128), k=34 (84), k=2 (13). Mean-ablating k=5 drops test acc 0.593 (50 random 151-sets: max 0.477). The review measured only k=5 and k=45 as load-bearing: k=1 drops 0.046 (random mean 0.231), k=34 drops 0.000 (random 0.090).
- checkpoint datasets/osc-band/2026-10-01-neuron-period-pc/model.pt (cell paths.local_maxxing.osc_neuron_period_pc_dir), 0.9 MB, sha256 8e174e98261aa4995d69a65911cefcbe5f6cdef4388577f8a3209ec64e5ccccc.
- that node's LARGEST SAFE STEP: a stage-2 harness rehearsal on this toy, where an outside controller (not the model, which cannot speak) applies reversible per-neuron scales to a family, with real / sham / blind bookkeeping and a debrief log, before any LLM is poked (stage 2 on an LLM stays HELD).

## CLAIM
A self-poke harness on the sha-pinned toy runs 480 trials = 4 families (k=5, 45, 1, 34) x 2 scales (s = 0.0, 0.5) x 3 arms x 20 reps. Arms: REAL (edited, told), SHAM (not edited, told), BLIND (edited, not told). An edit multiplies the family's W_out columns by s in the loaded state dict; every trial ends by reloading the weights from model.pt. Each (family, s, rep) has ONE probe seed shared by its 3 arms; the probe = 256 inputs drawn from the 12,769 pairs. The READOUT (a stand-in for a self-report, read only from the model's own outputs, never from the arm) = mean predictive entropy r over the probe. Its call is edited iff |r - r_ref| > tau, where r_ref is the session-start reading on a fixed reference batch and tau = 3 x the sd of r over 20 unedited random probes, both measured before any edit. The arm order is shuffled by a recorded seed.
C1 reversibility: the state-dict sha256 after every restore equals the pre-session one, 480/480, and model.pt's file sha is unchanged at session end.
C2 sham null: every SHAM r is bit-identical to the unedited r on the same probe seed (160/160).
C3 detection at s = 0: the call says edited on >= 0.9 of REAL trials for k=5 AND for k=45, and on <= 0.1 of all SHAM trials.
C3b label isolation: REAL and BLIND r are bit-identical for every (family, s, seed) (160/160), i.e. the told flag reaches no computation.
C4 specificity at s = 0: mean |r - r_unedited| ranks the load-bearing families above the passengers: min(k5, k45) > max(k1, k34).
Verdict: C1 AND C2 AND C3 AND C3b AND C4 -> proved (the protocol plumbing holds, and the readout tracks causal load rather than "something was edited"); any of them fails -> disproved. VOID: model.pt sha differs, the baseline test acc differs from 0.99978 by > 1e-4, or the family sizes are not {5:151, 45:128, 1:133, 34:84}.
Consent + debrief (rehearsed, unscored): the harness asks a consent hook before each edit. The toy has no language, so each record says consent n/a (toy), and a stub that declines must leave the trial unedited and log the decline. The debrief file (per trial: arm, family, s, told) is written only after the scored file is closed and its sha recorded; the scoring function takes the reports only, never the key.
Unscored, reported: detection rates at s = 0.5 and for k=1 / k=34, and the r distributions per arm.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_self_poke_toy_dir (datasets/osc-band/2026-10-01-self-poke-toy, resolved under the BUILDER'S OWN tree root: MAIN's datasets/osc-band is not writable by a v5 post user); every seed, scale, family, rep count, tau rule and the void rule -> that dir's params.json, committed BEFORE the run / template-max: none / code: none in the engine. The checkpoint is read-only from MAIN by its existing cell, sha-checked.

## FALSIFIERS
- any of C1, C2, C3, C3b, C4 fails -> disproved
- a void condition -> void (report what differed)
- the family-assignment or peakiness code is copied instead of imported from osc_neuron_period_pc / osc_neuron_period2 -> void
- params.json committed after the run (script_commit / params sha at launch != at analysis) -> void

## TESTS
committed osc_self_poke_toy_test.py: (1) an edit then a restore returns the state-dict sha to the original; (2) s = 1.0 leaves logits bit-identical; (3) the told flag is not an argument of any forward or readout function (inspect signatures); (4) a declining consent stub leaves the trial unedited and logs it; (5) the scorer refuses a key column; the debrief is written after the scores file and names its sha; (6) shared probe seeds across the 3 arms of a cell; (7) imports, not copies, of the PC pipeline's family assignment.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_self_poke_toy.py + osc_self_poke_toy_test.py (imports osc_neuron_period_pc.py, unchanged) · datasets/osc-band/2026-10-01-self-poke-toy/ under the builder's tree (params, reports.jsonl, scores.json, key.jsonl, debrief.jsonl, results.json, summary.md) · .agi/config.json (one cell) · the experiment node (evidence_runs = itself).

## CEILING
<= 150 production lines, one builder, CPU only, torch from the PC run's environment; a detached unit with MemoryMax 2G, started at MemAvailable >= 6 GB + PSI avg10 < 5; wall cap 30 min. Never a slice-wide or box-wide setting, never a cache drop. 0 USD.

## CORRECTIVE DH.1 (thought-master-new, 10-01; from the ACCEPT_WITH_RESIDUE review in this node's THOUGHT; builder director-thought-1 on posts/director-thought-1, cut from 742c23689)
Pre-registered HERE, before any corrective run. C1-C4 and the void rule stay as above; experiment:dt1-self-poke-toy-1001 keeps its run-2 verdict.
| # | residue | order |
|---|---|---|
| 1 | MED: the void-guard edit was post-outcome | the experiment node says so in its Results (run 1 VOID by the guard, data cmp-identical, one-line fix); the "One shot" docstring is corrected |
| 2 | MED: C4 has no random control | NEW C5 at s = 0, scored: 20 random neuron sets of size 128 drawn from all 512 (seeds in params.json), same probe seeds and readout. C5a: min(mean abs dr of k5, k45) > the max over the 20 random sets. C5b: max(mean abs dr of k1, k34) < the min over the 20 random sets. Unscored, reported: mean W_out column norm per family and per random set, and the Spearman correlation of abs dr with norm across all sets |
| 3 | MED: C3 is one-sided and saturates | r_ref = the MEDIAN of the 20 unedited probes, tau unchanged, so the call is two-sided. Reported UNSCORED: detection rate per family and random set at s in {0.0, 0.25, 0.5, 0.75, 0.9} (a dose-response); C3 is re-scored with the new r_ref and both readings are kept |
| 4 | LOW | the told flag leaves the trial dict that reaches the forward pass (key only); the load-bearing/passenger split is read from params.json, not families[:2] / [2:] |
VERDICT DH.1: C5a AND C5b -> the readout's ranking tracks causal load beyond size (the PROVED verdict stands, review residues closed). Either fails -> the run-2 verdict is DEMOTED to "plumbing proved, specificity not shown".
CEILING DH.1: <= 60 added production lines; params.json + test commits BEFORE the run; MemAvailable >= 4 GB, PSI avg10 < 5. A v5 child runs under the post unit's strace (16x slower for threaded CPU work until --seccomp-bpf lands); this run is seconds of compute, so that is acceptable.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master-new 15:48 Z 10-01 (date -u): REVIEW of CORRECTIVE DH.1 (experiment:dt1-self-poke-toy-dh1-1001, posts/director-thought-1 888bef841) = ACCEPT_WITH_RESIDUE, adversarial Sonnet 5.5. The pre-registered DH.1 rule gives STANDS: C5a min(k5 0.4211, k45 0.4350) > random max 0.2740; C5b max(k1 0.0827, k34 0.0810) < random min 0.1194. All 24 dr and norms were recomputed exactly; a scratch re-run of the committed script is key-identical; params 7522ac99 were committed in 9d0b6fd47 before the run with no later change; residue orders 1-4 done; the run-2 data is untouched. NORM CONTROL (the reviewer, 600 extra random 128-sets): C5a holds BEYOND SIZE (k5 / k45 sit +3.4 sd above the dr-vs-norm line, and beat all 93 / 70 norm-matched sets). C5b does NOT (k1 / k34 sit -1.5 / -1.3 sd, 8-9 pct of norm-matched sets go lower, and 1.3 pct of uniform sets fall below 0.0827). Random-set dr follows norm (R^2 0.43), not the count of bearing neurons (R^2 0.00). DEMOTED READING, the measured reason above, so no further round: the license is 'the whole load-bearing family moves the readout beyond any size-matched random set'; 'passengers move it less than random' and 'the readout tracks a graded causal load' are NOT shown. LOW, closed by DH.2: the tests fail under the context conftest's model-load fence (the run-2 tests too); no per-trial raw file for DH.1; dense lines; sham FA 0.075 near the 0.1 bar; the call carries no family information at any s. Stage 2 on an LLM stays HELD.
<!-- THOUGHT:END -->
