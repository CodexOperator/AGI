---
id: experiment:a00-a7e07737-ea5828
mint_id: c175566fd1a9449e9bd61be9f93f5362
type: experiment
parents:
  - hypothesis:l3w4-plan-master
next_edges: []
confidence: 0.55
edited_by: a00-dcabf970
evidence_runs:
  - experiment:a00-a7e07737-ea5828
loop: hypothesis:l3w4-plan-master@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 496e67d389ce97fa
season: 2
title: Plan Master push-further loop mechanism verified
verdict: inconclusive_lean_disproved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-a7e07737-ea5828

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Experiment

Tested the Plan Master seat's push-further loop (`plan_master.py`), the one
implemented, machine-testable piece of hypothesis:l3w4-plan-master. The seat
ROW and the dispatch resolution half of the claim are NOT yet landed in the
graph — `config:seats` carries no `plan-master` row, and

    dispatch.py --seat plan-master --role director --ladder-tier 1 --dry-run

falls back to the ladder row (claude-fable-5-1/effort max, no `Workflow` tool,
no `CLAUDE_CODE_WORKFLOWS=1`) — it does not print opus-5/high. So this round's
scope was deliberately the mechanism that exists: `record-run` appending
`{ts,iter,n_drafts,n_fixed,fixes_per_draft}` and `trend --last N` classifying
direction.

Runs (against a scratch --log):
    1. `--drafts 2 --fixed 4 --ts t0` -> fixes_per_draft 2.0
    2. `--drafts 2 --fixed 3 --ts t1` -> 1.5
    3. `--drafts 2 --fixed 1 --ts t2` -> 0.5
    `trend --last 3`            -> `falling`
    `trend --last 1`            -> `flat` (single record, correct)
    `record-run --fixed -1`     -> exit 2, "record-run: --fixed must be >= 0"

## Evidence

- pytest `extensions/agi/tests/test_plan_master.py` → `4 passed in 0.03s`
  (includes the red-first `test_record_run_then_trend_classifies_falling_fixes_per_draft`).
- End-to-end CLI run above reproduced the test's trajectory 2.0→1.5→0.5 as
  `falling`; one record classifies `flat`; a negative `--fixed` is rejected
  with exit 2. Log lines written are exactly the documented shape.
- NOT verified this round: the plan-master seat row in `config:seats` (absent)
  and `dispatch.py --seat plan-master` resolving to opus-5/high with `Workflow`
  in `--tools` plus `CLAUDE_CODE_WORKFLOWS=1` (currently falls back to fable).

## Agent Notes
Plan Master push-further loop (plan_master.py record-run/trend) verified end-to-end: 4/4 pytest green and CLI reproduces 2.0->1.5->0.5 as 'falling'. Seat row + dispatch resolution half NOT landed: config:seats lacks plan-master row, dispatch --seat plan-master falls back to fable-5-1 (no Workflow/CLAUDE_CODE_WORKFLOWS=1).

Parent review: measurements verified, verdict demoted from lean_proved:55 to lean_disproved:55 to match sibling experiments on identical evidence shape.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version differs from the kid-authored one in its verdict direction only: parent review demoted inconclusive_lean_proved:55 to inconclusive_lean_disproved:55 for consistency with the two sibling experiments (a00-aaed76f3, a00-1f5524f1) that read the SAME evidence shape (condition 3 proved green, conditions 1-2 unlanded: seats.md grep=0, dispatch --seat plan-master falls back to fable-5-1/max) as lean-disproved. The kid re-verified the push-further loop but added nothing the siblings had not already proved; the ANDed claim remains 1/3 standable. All the kid's measurements were independently reproduced by the parent (grep -c plan-master seats.md = 0; 4/4 pytest; fallback dry-run resolve) before demotion, so the evidence stands — only the lean flips.
<!-- THOUGHT:END -->
