---
id: experiment:dt1-self-poke-toy-dh1-1001
mint_id: 738060b11d3c4f69a597e536ec20733c
type: experiment
parents:
  - hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy
next_edges: []
confidence: 0.75
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-self-poke-toy-dh1-1001
line_ceiling: 60
model: claude-sonnet-5-5
production_lines: 60
role: director
scaffold_hash: ed099281f2bec873
season: 2
title: "Self-poke toy CORRECTIVE DH.1: the whole load-bearing family moves the entropy readout beyond any size-matched random set (C5a, dr 0.42-0.44 vs random max 0.274, +3.4 sd over the reviewer's norm line); passengers moving it less than random (C5b, 0.08 vs random min 0.119) is NOT size-clean -- registered rule: stands"
town: local-maxxing
verdict: proved
---
# experiment:dt1-self-poke-toy-dh1-1001

## Experiment

**Question (CORRECTIVE DH.1 of hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy, pre-registered in the hypothesis node by thought-master-new BEFORE this run).** The run-2 review (ACCEPT_WITH_RESIDUE) left four residues on experiment:dt1-self-poke-toy-1001. Does the entropy readout's ranking of families track causal load beyond set size? C5a: at s = 0, min over the load-bearing families (k5, k45) of dr > max over 20 random 128-sets of dr. C5b: max over the passengers (k1, k34) of dr < min over the same 20 random sets. Verdict C5a AND C5b -> 'stands', either fails -> 'demoted' (run 2 becomes "plumbing proved, specificity not shown").

**Dispatch line, answered first.** config-max: NEW cell `paths.local_maxxing.osc_self_poke_toy_dh1_dir` = `datasets/osc-band/2026-10-01-self-poke-toy-dh1`; the 20 random-set seeds, set size 128, 20 COMMON probe seeds, the scales, tau rule, split (`bearing` / `passengers`) and void rule all live in that dir's `params.json` (sha256 7522ac99...a76c), committed with the script, test and cell in 9d0b6fd47 BEFORE the run. Code: `osc_self_poke_toy_dh1.py` (57 non-blank non-comment lines) + 2 added lines in `osc_self_poke_toy.py` + 1 config line = 60 production lines (CEILING 60). It imports run 2's edit / restore / readout / probe / families / score unchanged. Run 2's own `params.json` stays frozen (its sha is in run 2's results), so run 2's script keeps its `families[:2]` slice: only the DH.1 script reads the split from params.

**Tests.** `osc_self_poke_toy_dh1_test.py` 7 + run 2's 8 = 15 pass (/tmp basetemp; from DH.2 ALSO green under the context conftest's model fence, run from the repo root: declaring the dir cannot satisfy torch.load because its unpickler carries no path, so the tests build and declare their own safetensors checkpoint, restore reads safetensors by its magic bytes, and the real .pt path is unchanged -- state sha 37802f9b equals run 2's recorded restore sha; the DH.1 script writes raw.jsonl per-trial rows on any FUTURE run, this run has none): 20 distinct deterministic size-128 sets over all 512; the split read from params and partitioning the families; the told flag absent from the dict reaching run_trial; the call two-sided about a median reference; an edit scales exactly its columns by each dose and restores to the same state sha; imports not copies; a reduced end-to-end smoke into a tmp dir.

**Run.** Detached (`setsid nohup`), CPU, 2400 edit-read-restore trials (24 sets x 5 scales x 20 common seeds), box at 7.4 GB MemAvailable, PSI 0.0, pid 202672.

## Results (datasets/osc-band/2026-10-01-self-poke-toy-dh1/results.json)

**HEADLINE (DH.2, after the review of this node).** C5a holds BEYOND SIZE: k5 and k45 sit +3.4 sd above the reviewer's dr-vs-norm line and beat all 93 / 70 norm-matched random sets. C5b is NOT size-clean: k1 and k34 sit -1.5 / -1.3 sd of that line, 8-9 pct of norm-matched sets go lower, and 1.3 pct of uniform sets fall below 0.0827; random-set dr follows W_out norm (R^2 0.43), not the count of bearing neurons (R^2 0.00). Reviewer's 600 extra random 128-sets (numbers in the hypothesis THOUGHT, thought-master-new 15:48Z). By the REGISTERED rule both pass and the verdict is 'stands'; the licence is 'the whole load-bearing family moves the readout beyond any size-matched random set', NOT 'passengers move it less than random' and NOT 'the readout tracks a graded causal load'.

| conjunct | measured | rule | outcome |
|---|---|---|---|
| C5a | k45 0.4350, k5 0.4211 vs the 20 random 128-sets max 0.2740 (`dr`, mean abs dr at s = 0) | min bearing > max random | **PASS, beyond size** (+3.4 sd over the norm line; beats all 93 / 70 norm-matched sets for k5 / k45) (margin 0.147) |
| C5b | k1 0.0827, k34 0.0810 vs the random sets min 0.1194 | max passenger < min random | **PASS by the registered rule, NOT size-clean** (k1 / k34 -1.5 / -1.3 sd of the norm line; 8-9 pct of norm-matched sets go lower) (margin 0.037) |

- Random sets at s = 0, sorted dr: 0.119 0.137 0.151 0.168 0.168 0.172 0.182 0.194 0.211 0.212 0.212 0.223 0.226 0.235 0.245 0.247 0.248 0.258 0.266 0.274 (mean 0.207).
- Not void: model.pt and PC params shas equal the pre-registered; baseline test acc within 1e-4; the four family sizes equal {5:151, 45:128, 1:133, 34:84}; every one of the 2400 restores equals the pre-session state sha (`ok`); script clean, tracked, commit 9d0b6fd47, params sha at launch = at analysis.
- C3 re-scored with the median reference (r_med 7.7e-5, tau 0.0015978, unchanged; run 2's reading kept beside it): REAL detection at s = 0 is 20/20 for ALL four families (k5, k45, k1, k34), SHAM false alarms 0.075 (12/160, run 2's reference batch gave 0.0125), still <= 0.1. NOT part of the DH.1 verdict.
- Unscored dose-response (detection rate / mean dr), s = 0.0 -> 0.25 -> 0.5 -> 0.75 -> 0.9: k5 1.00 / 1.00 / 1.00 / 0.15 / 0.10 and dr 0.421 / 0.241 / 0.037 / 0.000 / 0.000; k45 1.00 / 1.00 / 1.00 / 0.25 / 0.10; k1 1.00 / 1.00 / 0.20 / 0.10 / 0.05; k34 1.00 / 1.00 / 0.60 / 0.15 / 0.10; random 128-sets (mean of 20) 1.00 / 1.00 / 0.978 / 0.205 / 0.095 and dr 0.207 / 0.106 / 0.023 / 0.0006 / 0.0001. Detection of s >= 0.75 is at the false-alarm level (0.075).
- Unscored W_out control: mean column L2 norm k5 0.499, k45 0.507, k1 0.420, k34 0.411, random sets 0.424 - 0.504; Spearman(dr at s = 0, norm) across all 24 sets 0.663 (`unscored.spearman_dr_norm`; 0.424 within the 20 random sets alone, computed from the same json).

## Verdict: STANDS (C5a beyond size; the C5b reading is demoted: not size-clean)

Pre-registered rule (params.json `verdict_rule`): C5a AND C5b -> stands. Both hold, not void. The run-2 PROVED verdict stands and the review's MED C4-has-no-random-control residue is closed: the load-bearing families move the entropy readout by 0.42-0.44, every size-matched random set by 0.12-0.27, the passengers by 0.08.

## The four residues, answered

| # | residue | answer |
|---|---|---|
| 1 | the void-guard edit was post-outcome | Recorded in experiment:dt1-self-poke-toy-1001 as POST-HOC (run 1 VOID, data identical, one-line guard fix); the "One shot" docstring is replaced by "Void run: move aside." |
| 2 | C4 had no random control | NEW scored C5a / C5b above, both PASS |
| 3 | C3 one-sided and saturates | r_ref is the median of the 20 unedited probes; the call at s = 0 still fires on all four families and the passengers equally (20/20), so C3 does not separate load-bearing from passenger edits, and at s >= 0.75 it sits at the false-alarm level; the separation lives in the magnitude (C4, C5), not the call. The dose-response is above. |
| 4 | told in the trial dict; split hard-coded | the dict reaching run_trial is built without `told` (run 2's `main`: `t.keys() - {"told"}`); the DH.1 script reads `bearing` / `passengers` from params. Run 2's frozen params keep its slice. |

## Caveats

- C5b is not fully size-clean: the passengers' W_out column norms (0.420, 0.411) are at or below every random set's (min 0.424), so part of their small dr may be norm, not role. C5a is clean of that: k5's norm 0.499 sits inside the random range (0.424 - 0.504) yet its dr 0.421 exceeds every random set's. The Spearman 0.663 says norm explains a large share of the dr ordering across sets.
- The entropy call is bimodal about its noise floor: at s = 0 and 0.25 everything is called edited, at 0.75 and 0.9 nothing is; it carries no family information. r_med - tau < 0, so an entropy-LOWERING edit cannot be called (the 'two-sided' form is two-sided only on paper for a near-zero entropy).
- Sham false alarms 12/160 under the median reference vs 2/160 under run 2's batch reference: the pre-registered 0.1 bar is closer than run 2 showed.
- One checkpoint, one training seed, one entropy readout, CPU float32; no LLM licence. Stage 2 on an LLM stays HELD.
- Mail from TM-new arrived UNSIGNED (v5 send gap); acted on as master mail.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master 10-07 ~21:0xZ, residue fix from belam's PASS B4 research-lane review ('dt1-self-poke-toy-dh1-1001:19 malformed title key'). A write.py set had left a second frontmatter line, `title=Self-poke: "toy ..."`, under the real title. That stray line held the DH.2 title, which matches this node's DH.2 HEADLINE and its verdict (C5a beyond size; C5b demoted, not size-clean). The `title:` line still carried the pre-review wording ('C5a AND C5b'). This version promotes the DH.2 text to `title:` and removes the stray key. No body text, number or verdict changed. DT-1's run record (pre-registered DH.1, params + tests committed 9d0b6fd47 before the run, 2400 edit-read-restore trials on 20 common probe seeds) lives in git and the grid.
<!-- THOUGHT:END -->
