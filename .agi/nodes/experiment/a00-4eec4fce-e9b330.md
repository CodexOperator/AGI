---
id: experiment:a00-4eec4fce-e9b330
mint_id: 3f1c969b4dec48bf92f2028c85cb4d40
type: experiment
parents:
  - hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
next_edges: []
confidence: 0.55
edited_by: a00-ec374f61
evidence_runs:
  - experiment:a00-4eec4fce-e9b330
line_ceiling: 40
loop: hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "armB IFEval strict score is a real measured row", "class": "wire", "cmd": "parent-independent re-run of the unchanged official evaluation_main.py on the same 541-row file, then reduce follow_all_instructions", "expected": "strict within the +/-0.4pp langdetect floor of the kid 0.778189, i.e. 0.7742-0.7822", "observed": "Accuracy: 0.778189; independent reduction 421/541 = 0.7781885 -- exactly the kid number on this run", "result": "HOLDS"}
  - {"conjunct": "no fabricated score; row honestly does not fire", "class": "gate", "cmd": "read the arm B IFEval row in gap_table.md, compare 421 to the 423 needed at 0.9*0.868762=0.781886; confirm no numeric arm B IFEval row existed before this round", "expected": "row = 0.778189 (421/541) and 421 < 423 -> does not fire; the row was absent pre-round", "observed": "row present at 0.778189; threshold 0.781886; 421<423; parent probe at 11:38Z found no numeric arm B IFEval row and no eval_results_*armB* file", "result": "HOLDS"}
  - {"conjunct": "hardware restore", "class": "wire", "cmd": "docker ps; curl :8080/v1/models; pgrep for the generator cmdline", "expected": "fork-bonsai gone, llama-server up and answering 200 with the 3 models, no generator left", "observed": "only llama-server Up (healthy); :8080 /v1/models returns Qwen3.5-35B-A3B-Q3_K_M, Qwen3.5-9B-Q4_K_M, bonsai; no process whose cmdline starts python3 ifeval_gen_armB.py", "result": "HOLDS"}
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
Parent review SWR-B.03 (a00-ec374f61), accepted, no demotion. (1) The brief said arm B IFEval fires iff >= 0.9 x 0.868762 = 0.781886, and required one scoring run with the official unchanged harness. (2) What I ran, not what the node says: an independent re-run of evaluation_main.py on the same 541-row file returned strict prompt-level Accuracy 0.778189 and my own reduction of eval_results_strict.jsonl gave 421/541 follow_all_instructions -- exactly the kid number, 421 < 423, so it does not fire by 0.37pp, inside the established +/-0.4pp unseeded-langdetect floor. gap_table.md carries the matching row; fork-bonsai is gone and :8080 answers with the 3 models. (3) Near miss: a node could have reported fired by rounding 421/541 to 0.78 and comparing loosely to 0.7819, or by averaging several scoring runs until one crossed the threshold; the kid did neither, it kept the one run and named the miss inside the noise band. (4) The kid relocated the scorer to /data/work/agi/.agi/sessions/iter-SWR.01/a00-559ee702 because the worktree path in the brief had been reaped; I verified that copy is the one the reference row used (re-derives 470/541 and 0.908873 from its own results), so the relocation is not a second harness. Verdict kept at inconclusive_lean_proved:55 although the point estimate sits below the bar: the honest reading is a boundary sample, not a clean miss, and the label is the kid observation -- not a rule violation. What the round proves: arm B fires on HumanEval (92.2 pct rel) and misses on IFEval (89.57 pct rel), so arm B alone does not satisfy the two-eval hypothesis; C1/C2 IFEval are still unmeasured and the master decides the next chunk.
<!-- THOUGHT:END -->

## Agent Notes
Arm B IFEval scored ONCE on all 541 prompts with the official harness: strict prompt-level 0.778189 (421/541), loose 0.815157, strict instruction-level 0.851319; threshold 0.781886, so does NOT fire — short by 0.37pp, inside the ±0.4pp langdetect floor. Row + verdict written to gap_table.md; fork-bonsai removed, llama-server restored.

PARENT REVIEW SWR-B.03 (a00-ec374f61): ACCEPTED, verdict unchanged at inconclusive_lean_proved:55, no demotion. Three parent-run probes hold: (wire) independent re-run of the official harness returns strict 0.778189, 421/541, exactly the kid number; (gate) gap_table.md row matches 0.778189 vs threshold 0.781886, 421<423, does NOT fire by 0.37pp inside the +/-0.4pp noise floor, and no numeric row existed pre-round; (wire) fork-bonsai removed, llama-server restored and answering 200 with 3 models, no generator left. Scorer relocated to the engine-root session copy because the worktree in the brief was reaped -- verified same harness the reference used. RESULT: arm B fires on HumanEval (142/164, 92.2pct rel) and misses IFEval (89.57pct rel); arm B alone does not satisfy the two-eval hypothesis.
