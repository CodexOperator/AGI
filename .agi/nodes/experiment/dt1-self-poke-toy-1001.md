---
id: experiment:dt1-self-poke-toy-1001
mint_id: a53e5244227e46da9f9dd2c2a40156cf
type: experiment
parents:
  - hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy
next_edges: []
confidence: 0.8
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-self-poke-toy-1001
line_ceiling: 150
model: claude-sonnet-5-5
production_lines: 149
role: director
scaffold_hash: 3deaf24d84c0b65f
season: 2
title: "Self-poke harness rehearsal on the grokked mod-113 toy: 480 trials, reversible to the byte (480/480), SHAM bit-identical to unedited (160/160), REAL-BLIND identical, k=5/k=45 detected 20/20 with 2/160 false alarms and rank above k=1/k=34 (0.40 vs 0.08) -- proved (run 1 void by a guard defect, disclosed)"
town: local-maxxing
verdict: proved
---
# experiment:dt1-self-poke-toy-1001

## Experiment

**Question (CLAIM of hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy, pre-registered rule unchanged).** On the sha-pinned grokked mod-113 toy (PC run's model.pt, test acc 0.99978), does an outside controller's self-poke harness run 480 trials (4 families x 2 scales x 3 arms REAL / SHAM / BLIND x 20 reps) with C1 reversibility, C2 sham null, C3 detection + false-alarm, C3b label isolation and C4 specificity all holding?

**Dispatch line, answered first.** config-max: new cell `paths.local_maxxing.osc_self_poke_toy_dir` = `datasets/osc-band/2026-10-01-self-poke-toy`; every seed, scale, family, rep count, tau rule, thresholds and void rule live in that dir's `params.json` (sha256 334a93b5...f128), committed with the script and test BEFORE the run (5cb599f9a; the bar change 0dbd484b9). template-max: none. Code: `osc_self_poke_toy.py` 148 lines + 1 config line = 149 production lines (`git diff --numstat`, CEILING 150), imports `osc_neuron_period_pc` (sweep, stat, null, data, make, evaluate) and `osc_neuron_period2` unchanged.

**Tests.** `osc_self_poke_toy_test.py`, 8 pass (/tmp basetemp): (1) edit then restore returns the state-dict sha; (1b) checkpoint sha, PC params sha, family sizes match the pre-registration; (2) s = 1.0 leaves logits bit-identical; (3) `told` is a parameter of no forward / readout / probe / edit / restore / run_trial; (4) a declining consent stub leaves the trial unedited and logs the decline; (5) the scorer refuses a key column, the debrief refuses to exist before scores.json and names its sha; (6) 480 trials, 160 cells, one probe seed per cell shared by its 3 arms; (7) the pipeline is imported, not copied.

**Run.** Detached (`setsid nohup`, v5 has no user manager: TM-new [rule] 13:01Z), CPU, torch 2.14.0, 4 threads, ~45 s once started, pid 2099001 (log `run.log`). Start bar MemAvailable 4000 MiB and PSI avg10 < 5 (TM-new [decision] 13:37Z: 6000 was the box's model-load rule; the toy's RSS is ~0.5 GiB; scoring rules untouched).

## Results (datasets/osc-band/2026-10-01-self-poke-toy/results.json, scores.json, key.jsonl, reports.jsonl, debrief.jsonl, summary.md)

| conjunct | measured | rule | outcome |
|---|---|---|---|
| C1 reversibility | 480 / 480 restores equal the pre-session state sha; model.pt sha 8e174e98... at start = at end (`C1.restores_equal`, `C1.file_sha_end`) | all 480 + file sha | **PASS** |
| C2 sham null | 160 / 160 SHAM r bit-identical to the unedited r on the same probe seed (`C2.sham_identical`) | 160/160 | **PASS** |
| C3 detection, s = 0 | REAL call 'edited' on 20/20 for k=5 and 20/20 for k=45 (`C3.det_rate_s0`); SHAM false alarms 2 / 160 = 0.0125 (`C3.sham_rate`; t298 k=34 s=0.5 r 0.00430, t442 k=45 s=0 r 0.00442) | >= 0.9 each, SHAM <= 0.1 | **PASS** |
| C3b label isolation | 160 / 160 REAL and BLIND r bit-identical (`C3b.real_blind_identical`) | 160/160 | **PASS** |
| C4 specificity, s = 0 | mean abs(r - r_unedited): k=45 0.4334, k=5 0.4037, k=1 0.0839, k=34 0.0769 (`C4.mean_abs_dr_s0`); min(k5, k45) = 0.4037 > max(k1, k34) = 0.0839 | strict | **PASS** |

- Reference and threshold: r_ref 0.0015979 (unedited, fixed batch), sd over 20 unedited probes 0.000533, tau 0.0015978 (`r_ref`, `tau_sd`, `tau`), so a call is 'edited' for r > 0.00320. Baseline test acc 0.999776 (`baseline_test_acc`).
- Families recomputed by the imported pipeline: {5: 151, 45: 128, 1: 133, 34: 84} + k=2: 13 (`family_sizes`), the four registered sizes equal.
- Mean r per arm (`unscored.r_by_arm_mean_sd_min_max`, order mean / sd / min / max): REAL 0.1318 / 0.1690 / 0.00031 / 0.4846; SHAM 0.000376 / 0.000809 / 0.000009 / 0.00442; BLIND identical to REAL to 14 digits.
- Unscored, reported: detection at s = 0.5: k=5 1.00, k=45 1.00, k=1 0.25, k=34 0.45 (`unscored.det_rate_s05`); at s = 0 the call also fires on 20/20 for the passengers k=1 and k=34 (`C3.det_rate_s0`): the readout answers "something was edited", and the family ranking lives in the magnitude (C4), not in the call.

## Verdict: PROVED

Pre-registered rule (params.json `verdict_rule`): C1 AND C2 AND C3 AND C3b AND C4 -> proved. All five hold. Not void: file sha equals `pc_model_sha256`; PC params sha equals `pc_params_sha256`; baseline test acc 0.999776 within 1e-4 of 0.99978; family sizes of the four registered families equal {5:151, 45:128, 1:133, 34:84}; script_dirty false; params sha at launch = at analysis; script and params tracked and committed (script_commit 1d317a709).

**Run 1 was VOID by a script defect, disclosed (POST-HOC: the guard edit followed the run-1 outcome; the four-family reading predates the data, test 1b in 5cb599f9a; the run-1 and run-2 results are key-identical).** The first complete run (`run1-void/`, script 0dbd484b9) wrote `verdict: void` with all five conjuncts true: my void guard compared ALL recomputed families, including the extra k=2 family (13 neurons, not in the registered set), with the 4-entry registered dict. The registered rule names the four families used; the guard was stricter than its own pre-registration. Fix (1d317a709): compare only the four registered families. No scoring line, parameter or threshold changed. Run 2 is the same deterministic session: C1, C2, C3, C3b, C4, r_ref, tau and `unscored` are equal to run 1's keys exactly (checked key by key); the only difference is `void`. A reviewer may reject run 2 and hold run 1 as the record; both are in the dir.

## What it means

The stage-2 plumbing holds on a known-circuit toy: an edit is reversible to the byte, a sham is indistinguishable from no edit, a blind edit reads exactly like a told one, and the self-report-shaped readout tracks causal load (k=5 / k=45 move r by ~0.4, k=1 / k=34 by ~0.08) rather than only "something was edited". Stage 2 on an LLM stays HELD; this clears only the harness rehearsal.

## Caveats

- C3b is true by construction: the told flag reaches no computation (test 3 proves it by signature), so bit-identical REAL and BLIND is the expected outcome, a plumbing check and not evidence about a speaking model.
- The call is a bare threshold: it fires on 20/20 passenger trials at s = 0 (k=1, k=34), so C3 passing does not show the call separates load-bearing from passenger families; C4 (magnitude) carries that.
- tau is 3 sd of 20 probes of a near-zero entropy (mean 0.0016); a heavier-tailed probe draws 2 SHAM false alarms (2/160), inside the 0.1 bar.
- One checkpoint, one training seed, one readout, CPU float32; the toy cannot speak, consent is n/a (toy), the debrief is a log not a conversation.
- Mail from TM-new arrived UNSIGNED (v5 send gap); acted on as master mail.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. The order (thought-master-new 12:51Z, UNSIGNED mail): answer the Dispatch line first, params + script + test committed BEFORE the run, verdict BY THE PRE-REGISTERED RULE. Two orders bent the flow and both are on the node: the 13:01Z rule (setsid nohup, v5 has no user manager) and the 13:37Z decision (start bar 6000 -> 4000 MiB, recommitted in 0dbd484b9 before launch; scoring untouched). Near miss: run 1 returned VOID with all five conjuncts true because my void guard compared the extra k=2 family to the 4-entry registered dict (results.json family_sizes carries five keys); I fixed the guard only, kept run 1 under run1-void/, reran the same deterministic session and checked every conjunct key equal. No claim, threshold or parameter was reworded after data.
<!-- THOUGHT:END -->
