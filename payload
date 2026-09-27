---
name: agi-dispatch
description: >
  Drive a goal through dispatched parents and judge what comes back: decompose, dispatch a
  parent with the exact tier/role flags, the spawn bound, the behind-origin refusal, kid
  rebriefs, and season.py judge (continue | adjust | done). Use whenever a director spawns
  a parent or kid, or judges a parent's report against its plan node.
---

# agi-dispatch — decompose ▸ dispatch ▸ judge

Source of truth: `dispatch.py -h` · `season.py judge -h` · `spawn_budget.py status`. A director JUDGES; it never does kid work.

## 1 · The loop
```
goal:gX ──decompose──▶ goal:gX.a  goal:gX.b          write.py create goal … (skill agi-goal)
                          │          │
                       parent     parent             dispatch.py (below)
                          │          │
                       outcome    outcome
                          └────┬─────┘
            season.py judge <outcome-id> --against goal:gX      → continue | adjust | done
```
Nest rather than widen; sketch the leaves first; spawn parents ONLY against sketched leaves.

## 2 · Dispatch a parent
```bash
python3 extensions/agi/bin/dispatch.py <project_root> <iter_n> --tier parent \
  --role parent --ladder-tier 0 --detach --target <goal-or-hypothesis-id> [--dry-run]
```
- `--role parent --ladder-tier 0` is DELIBERATE: `--role` defaults to `kid`, so a bare `--tier parent` resolves
  the tier-0 KID row and spawns the parent on the wrong model (hypothesis:l3w1-tier0-director-brief).
- Exit 3 = your post is behind `origin/season2/main`: that refusal IS the behind check (F9) — no hand fetch + rev-parse.
- `--push-further` re-dispatches at `--target` from its `push_further` text; refused at an overview/vision/moral node.
- Bound: `spawn_budget.py status` (live agents vs the tree-wide cap); `provisioning.py status` (per-spawn keys).
- A director dispatches from ITS OWN worktree; ≤ 8 live parents, ≤ 5 kids each.

## 3 · Kids and rebriefs (F31)
A parent that answers a kid's `rebrief_request` in-node dms its director the answer line
(kid id, N/C, proceed-with-N | cut) BEFORE the kid resumes. A kid past 2× its budget with no such dm in your
inbox = self-authorised: cut it. A kid's work is the kid's — brief, do not steer.

## 4 · Judge
`season.py judge <report-id> --against <plan-id> --actor <post>` stamps the alignment:
`continue` (keep going) · `adjust` (reword the plan node) · `done` (close the plan, mint the outcome).
Judge against the plan node's PARENT (the lens this tier sees through), from the report AND the bytes.
Reviews of a round run BY NAME on pi (skill `agi-workflow`), never inline.
