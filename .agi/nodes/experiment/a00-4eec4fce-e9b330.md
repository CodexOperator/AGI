---
id: experiment:a00-4eec4fce-e9b330
mint_id: 3f1c969b4dec48bf92f2028c85cb4d40
type: experiment
parents:
  - hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
next_edges: []
confidence: 0.55
edited_by: a00-4eec4fce
evidence_runs:
  - experiment:a00-4eec4fce-e9b330
line_ceiling: 40
loop: hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 20
profile: balanced
role: kid
scaffold_hash: 1a57234973da38ad
season: 2
title: "Arm B IFEval: 0.778189 strict, misses the 0.9x bar by 0.37pp inside the 0.4pp noise floor"
town: core
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-4eec4fce-e9b330 — score the 541-row arm B IFEval set

## Experiment

The parent verified that arm B generation finished: 541 rows in official order.
This round scored that file ONCE with the official Google harness and wrote the
IFEval row for arm B.

**1. File re-verified (cheap gate, ran first).**

```python
D="datasets/switch-rule/2026-09-21"
ip=[json.loads(l)["prompt"] for l in open(f"{D}/ifeval_input_data.jsonl") if l.strip()]
op=[json.loads(l) for l in open(f"{D}/armB_bonsai27b-ptq1.ifeval.responses.jsonl") if l.strip()]
assert len(op)==541 and [r["prompt"] for r in op]==ip
assert len(set(r["prompt"] for r in op))==541
assert all(set(r.keys())=={"prompt","response"} and r["response"] for r in op)
```

Output: `541 rows, exact official order, unique, nonempty -- OK`.

**2. Scored ONCE, official harness UNCHANGED.** The dispatch brief pointed at a
scorer venv in worktree `a00-9db255d9`, which no longer exists. The same scorer
+ venv are live at the engine root session dir (found by `find`), so no rebuild
and no re-fetch were needed:

```bash
cd /data/work/agi/.agi/sessions/iter-SWR.01/a00-559ee702/ifeval
../ifeval_venv/bin/python evaluation_main.py \
  --input_data=/data/work/agi/.agi/worktrees/a00-ec374f61/datasets/switch-rule/2026-09-21/ifeval_input_data.jsonl \
  --input_response_data=/data/work/agi/.agi/worktrees/a00-ec374f61/datasets/switch-rule/2026-09-21/armB_bonsai27b-ptq1.ifeval.responses.jsonl \
  --output_dir=/data/work/agi/.agi/worktrees/a00-ec374f61/.agi/sessions/iter-SWR-B.03/a00-4eec4fce/armB_score
```

Prompt-level and instruction-level aggregates recomputed from the harness's own
`eval_results_strict.jsonl` / `eval_results_loose.jsonl` (same reduction the
reference row uses; cross-checked: reference reduces to 470/541 = 0.868762 and
instruction-level 0.908873).

## Evidence

Arm B (Bonsai 2 27B PTQ1_0, no LoRA), 541/541 prompts, one run:

| metric | arm B | reference (deepseek-v4.1-flash) | rel. pct |
|---|---|---|---|
| strict prompt-level | **0.778189 (421/541)** | 0.868762 (470/541) | 89.57 % |
| loose prompt-level | 0.815157 (441/541) | 0.894640 | 91.12 % |
| strict instruction-level | 0.851319 (710/834) | 0.908873 | 93.67 % |

**Switch rule for arm B on IFEval: FIRES iff >= 0.9 x 0.868762 = 0.781886.**
Arm B is 0.778189, i.e. 421 of 541 vs the 423 needed — **does not fire**, short
by 0.37 pp. That shortfall is *smaller than the established ±0.4 pp langdetect
floor*: the harness calls `langdetect.detect()` unseeded
(`instruction_following_eval/instructions.py` L158, L1416, L1448), and the
reference itself re-scores at 469-472/541 across runs of the same file. So the
honest reading is "does not fire, and the margin is inside scorer noise", not a
clean miss. The floor is carried from prior rounds, not re-derived, and runs are
never averaged.

Against the HumanEval result (142/164 = 86.6 % = 92.2 % of ref, FIRES): arm B
clears one eval and misses the other, so arm B alone does not satisfy the
two-eval hypothesis. This is ONE arm on ONE eval — no mvp is minted here.

Deliverable: the arm B IFEval row and its switch verdict are written into
`datasets/switch-rule/2026-09-21/gap_table.md`, replacing the "IN PROGRESS"
prose.

## Restore

```
docker rm -f fork-bonsai      -> fork-bonsai
docker start llama-server     -> llama-server
curl :8080/v1/models          -> 200, 3 models
curl :8080/v1/chat/completions-> 200, chat.completion
no generator left             -> confirmed (no cmdline starts with python3 ifeval_gen_armB.py)
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Scores the file the parent verified rather than re-verifying generation again:
the 541-count gate is cheap and ran first, everything else was one harness run.
Chose the engine-root scorer copy over rebuilding the venv because it is the
same harness the reference row used (identical reduction confirmed by
re-deriving the reference's 470/541 and 0.908873 from its own results files),
and a fresh fetch would have introduced an unbidden second variable. Recorded
`inconclusive_lean_proved:55` rather than `disproved`: a 0.37 pp miss inside a
0.4 pp noise floor is not evidence of a real gap, but it is also not a fire.
<!-- THOUGHT:END -->

## Agent Notes
Arm B IFEval scored ONCE on all 541 prompts with the official harness: strict prompt-level 0.778189 (421/541), loose 0.815157, strict instruction-level 0.851319; threshold 0.781886, so does NOT fire — short by 0.37pp, inside the ±0.4pp langdetect floor. Row + verdict written to gap_table.md; fork-bonsai removed, llama-server restored.
