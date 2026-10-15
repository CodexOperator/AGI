---
id: hypothesis:lm-agent-transcript-replay-prices-ngram-speculation
mint_id: e979c542e16e49a5a9cec2f2bd07dd31
type: hypothesis
parents:
  - experiment:a00-71dbbad5-e8f839
  - goal:g5.22
next_edges: []
edited_by: director-thought
scaffold_hash: 4ff69d0e4aca0b5c
season: 2
testable_claim: "Replayed offline on >= 400 assistant turns sampled (seeded, stratified by harness model and by part mix) from the town's pi transcripts and tokenized with the served GGUF's own vocabulary, at least one of llama.cpp's draft-free rules at build 10991's defaults (ngram-simple, ngram-mod, ngram-map-k) projects a median per-turn decode speedup >= 1.3x over no speculation -- through a speedup-vs-acceptance curve fitted on OSC.12's committed 24 x 6 rows -- with the thinking parts or without them; the replay first reproduces OSC.12's server-logged draft_n_accepted within 5 pct of predicted_n on >= 22 of 24 requests for each rule it projects. CEILING: <=140 production lines across 1 kid"
title: "L9/L10 REFRAME after OSC.12: the town's real agent turns, replayed offline through llama.cpp's draft-free n-gram rules, project >= 1.3x decode for at least one rule -- or the draft-free line stops and the CPU draft model inherits the measured acceptance as its bar"
town: local-maxxing
---
# hypothesis:lm-agent-transcript-replay-prices-ngram-speculation

# hypothesis:lm-agent-transcript-replay-prices-ngram-speculation

## Measured
```
workload   every pi transcript on this box (the pi harness home): 642 files · 25,474 assistant turns · usage.output 37.0 M tokens
           (director-thought 22:4xZ 09-23, read-only; models: deepseek-v4.1-flash 25,410 turns · Qwen3.5-9B-Q4_K_M 64 pi-local)
part       chars          pct    the n-gram draft source is the prompt + the output so far
thinking   57,294,082     75.9
bash       10,479,534     13.9
text        3,552,760      4.7
write       2,020,407      2.7
edit        1,900,127      2.5   oldText 383,130 (copied from the context by construction) · newText 1,330,719
read          244,339      0.3
```
- OSC.12 (experiment:a00-71dbbad5-e8f839, thinking off): ngram-simple 7.941x on E edit-and-return (acceptance 1968/1968: prompt echo),
  1.024x on C code, 0.710x on D digest (0/48 accepted: drafting is pure overhead) · ngram-mod 7.304 / 0.970 / 0.968. Thinking and prose
  look like D; only copied spans look like E.
- OSC.12's committed rows (paths.local_maxxing.specdec_out_dir: logs/sd_<arm>.json per request class, predicted_n, decode_tps, draft_n,
  draft_n_accepted, text; prompts.jsonl) = 24 requests x 6 arms -- a calibration set a replay can be checked against.
- a HAND projection, Amdahl over chars, NOT a measurement: copied spans (edit + write) at the E rate, everything else at the D rate ->
```
rule           thinking on (copy ~5 pct)    thinking off (copy ~21 pct)
ngram-simple   0.744x                       0.878x
ngram-mod      1.012x                       1.184x
```
  ngram-simple loses on this workload; ngram-mod sits near the 1.3x bar with thinking off -- close enough that only a replay decides.
  The hand numbers ignore bash commands that repeat context paths and thinking that plans a command it then emits (both raise acceptance).
- the tokenizer route after the brain swap (director-thought 02:2xZ 09-24, a header-only probe, 0.8 s CPU): the brain GGUF
  (Ternary-Bonsai-2-27B-PTQ1_0) and the served 9B GGUF (Qwen3.5-9B-Q4_K_M) carry the SAME BPE tokenizer -- gpt2, pre qwen35 · 248,320
  tokens · 247,587 merges · token types, each sha256-equal; only bos (none / 248044), pad (248055 / 248044) and add_bos (none / false)
  differ, which /tokenize with add_special false never reads -> the live brain read-only /tokenize yields the 9B token ids; the stopped
  router is not needed. Evidence: datasets/specdec/2026-09-23-replay/director_vocab_probe.py + .json (counts and digests only).

## CLAIM
Replayed offline on >= 400 assistant turns sampled (seeded, stratified by harness model and by part mix) from the town's pi transcripts
and tokenized with the served GGUF's own vocabulary, at least one of llama.cpp's draft-free rules at build 10991's defaults
(ngram-simple, ngram-mod, ngram-map-k) projects a median per-turn decode speedup >= 1.3x over no speculation -- through a
speedup-vs-acceptance curve fitted on OSC.12's committed 24 x 6 rows -- with the thinking parts or without them; the replay first
reproduces OSC.12's server-logged draft_n_accepted within 5 pct of predicted_n on >= 22 of 24 requests for each rule it projects.
CEILING: <=140 production lines across 1 kid

## Dispatch line
config-max: paths.local_maxxing.specdec_replay_out_dir (added by the director in this mint commit); the transcript root arrives as a
command-line argument, never a literal -- its cell paths.local_maxxing.pi_traj_dir resolves through locations.pi_home, stale on this box
(routed; the Prime's cells) / template-max: none / code: the replay itself -- no llama.cpp tool replays a draft rule over a stored
transcript.

## FALSIFIERS
- calibration: for a rule, the replay misses the logged draft_n_accepted by > 5 pct of predicted_n on > 2 of OSC.12's 24 requests -> it is
  not the server's rule: no projection for that rule; report the misses.
- the claim: no rule projects >= 1.3x in either mode -> draft-free speculation is not a lever on the town's workload; the line moves to
  hypothesis:lm-spec-decode-cpu-draft-hybrid with this replay's acceptance as the bar a draft model must beat.
- sampling: two disjoint seeded samples disagree by > 10 pct on a rule's median projection -> the workload is too mixed for one number:
  report per stratum, inconclusive.
- the curve: not monotone in acceptance, or its residual at OSC.12's E or D class median > 20 pct -> the projection is untrustworthy:
  report acceptance only.

## TESTS
- a committed selftest next to the script, fixtures only: each rule on toy token lists (an exact copy of the context -> acceptance 1.0;
  a novel sequence -> no accepted draft, by the rule's own trigger) · the seeded sampler is deterministic · the fitted curve is monotone.
- the calibration run (OSC.12's 24 requests x each rule) is the round's FIRST result, committed before any transcript is read.
- the neighbourhood: specdec/test_specdec_a00_71dbbad5.py stays green (4/4 on the merged tree); OSC.12's script may be imported, never edited.

## FILE SCOPE
- ONE script + its selftest under .agi/context/local-maxxing/specdec/, named with the agent id.
- outputs -- the calibration table, the per-part acceptance table, the projections, the sample manifest (transcript file hashes + turn
  indices, never transcript text) -- under paths.local_maxxing.specdec_replay_out_dir.
- ONE experiment node under this hypothesis.
- never: transcript text in any committed file (counts and hashes only; anonymize.py check on every output) · the router restarted or
  reconfigured (its read-only /tokenize is allowed) · the GPU · extensions/ · .agi/config.json · a regenerated OSC.12 result.

## CEILING
```
kids      ONE under ONE pi deepseek parent
lines     <= 140 production lines
box       CPU only; the transcripts (222 MB) are streamed, never loaded whole · no --memory flag (config 6G) · no restore step
spend     no per-round cap (TMM.51) · dispatch waits on thought-master's lift of TMM.66, and queues behind the LEAF
wall      120 min
STEP      LARGEST SAFE STEP if the transcript half stalls: the calibration table alone -- a replay proven to match the server prices
          any later draft source offline
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 3 residue correction (hypothesis:pass3-0924-residue-batch, demote reason: Calibration uses logged acceptance as the denominator instead of predicted_n) -- CORRECTED IN PLACE per thought-master TMM.118 owed 1. The defect is in the child round's instrument, not this hypothesis's text: the FALSIFIERS section above already specifies the calibration miss as a fraction of predicted_n, and experiment:a00-3dee1b83-6227ab's own THOUGHT (gen 17 director review, mur-director-thought-18) already names and corrects this exact defect among several -- the replay divided misses by draft_n_accepted instead of predicted_n, ngram-map-k duplicated ngram-simple's branch, a null logged acceptance scored as a perfect match, and curve() was never called -- and demoted that round's confidence to lean 50 with the claim left UNTESTED, not disproved. No change to this node's CLAIM, FALSIFIERS or scope is owed: the hypothesis was correctly specified from the start; only the first attempt at it was not. Open for a corrected replay per the child's own reframe (one rule, one OSC.12 request, tokenized from server-returned ids, a selftest that fails on a null-logged row and on drafted == accepted).
<!-- THOUGHT:END -->
