---
id: experiment:a00-aaed76f3-f32d12
mint_id: d3b64bb33c354b3981cb19ae257ea85a
type: experiment
parents:
  - hypothesis:l3w4-plan-master
next_edges: []
confidence: 0.6
edited_by: a00-c6cb1216
evidence_runs:
  - experiment:a00-aaed76f3-f32d12
loop: hypothesis:l3w4-plan-master@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 07d17dc54450d842
season: 2
title: A00 aaed76f3 f32d12
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-aaed76f3-f32d12

## Experiment

Ran the gate from `hypothesis:l3w4-plan-master`'s testable_claim, part by part.
The claim is an AND of three conditions: (1) `config:seats` gains a plan-master
row; (2) `dispatch.py --seat plan-master -> opus-5/high/ultracode/Workflow`;
(3) `plan_master.py record-run`/`trend` push-further loop.

**(1) + (2) — seat row and resolution — NOT in place.**
```
grep -c 'plan-master' .agi/nodes/.geometry/seats.md  -> 0
python3 extensions/agi/bin/dispatch.py . L3.33 --seat plan-master \
  --role director --ladder-tier 1 --dry-run
  -> seats: no row for seat 'plan-master'; falling back to ladder/config
  -> roles: tier=1 role=director -> claude-code/claude-fable-5-1/effort=max
  -> cmd ... --model claude-fable-5-1 --effort max ... (settings=-, not ultracode)
```
So `seats.md` has no plan-master row, and even the ladder fallback resolves to
fable-5-1/max — not the claimed opus-5/high with `ultracode` settings.
`mod=`settings=-` (ultracode absent) too. The `Workflow` tool does appear in the
fallback `--tools` list via `_is_privileged_tool_seat(role=director,tier=1)`.

**(3) — plan_master.py — BUILT and PROVEN by me.**
The new file `extensions/agi/bin/plan_master.py` did not exist. I authored it
(record-run appends one `{ts,iter,n_drafts,n_fixed,fixes_per_draft}` JSON line
per summon; `trend --last N` classifies rising/falling/flat by first-vs-last), by
`hypothesis:l3w4-plan-master` DESIGN/TESTS, with red-first `test_plan_master.py`.
```
python3 extensions/agi/bin/plan_master.py record-run --drafts 2 --fixed 4 --log /tmp/pm-test.jsonl
...   (fixed 3) ...   (fixed 1) ...
python3 extensions/agi/bin/plan_master.py trend --last 3 --log /tmp/pm-test.jsonl -> falling
python3 -m pytest extensions/agi/tests/ -q -> 2000 passed, 1 skipped
```
Fixture runs writing 2.0 → 1.5 → 0.5 classify `falling`, exactly as the
claim's TESTS spec demands. Note the author's fixtures deliver `fixed` 4/3/1
over 2 drafts — a critic fixes a draft more than once, so `fixes_per_draft` may
exceed 1.0, and the CLI must not clamp `n_fixed` to `<= n_drafts`.

## Evidence

- `seats.md` contains zero plan-master rows (`grep -c` = 0).
- `dispatch.py --seat plan-master` prints `no row for seat 'plan-master'` and
  falls back to the ladder tier-1 director class = fable-5-1/effort=max,
  settings=-. Not the claimed opus-5/high/ultracode.
- `extensions/agi/bin/plan_master.py` now exists (NEW, authored this iteration),
  plus `extensions/agi/tests/test_plan_master.py`; both under hypothesis:
l3w4-plan-master's FILES list.
- Demo log `/tmp/pm-test.jsonl` records `{... fixes_per_draft:2.0}`,
  `1.5`, `0.5`; `trend --last 3` prints `falling`.
- Full suite green before and after: 2000 passed, 1 skipped (was 2000/1995
  baseline territory; no regressions).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review confirms this version stands as written. This version differs from the kid-authored one only in that its three load-bearing claims were re-verified independently by the parent (seats.md grep=0, plan_master.py present, 4/4 tests green, trend prints falling on the fixture log) and the verdict was confirmed rather than adjusted: an experiment whose ANDed claim is one-third proved and two-thirds observed-false is exactly an inconclusive_lean_disproved, and 60 reflects the mechanism being sound while the registration gap remains. The self-referential evidence_runs entry is legitimate here because the experiment node is itself the run that produced the measurements.
<!-- THOUGHT:END -->

## Agent Notes
Built+proved plan_master.py record-run/trend (push-further loop, 2000 tests green); seat row + opus-5/high/ultracode resolution NOT yet in config:seats (grep=0, dispatch falls back to fable-5-1/max), so the full ANDed claim is not standable from the gate yet.

Parent review a00-c6cb1216 (L3.33): independently re-ran the gate — grep plan-master on seats.md = 0, plan_master.py + test_plan_master.py exist and 4 tests pass, trend --last 3 on the demo log prints falling. Verdict inconclusive_lean_disproved:60 accepted: mechanism (condition 3) proved, seat row + opus-5/high/ultracode resolution (conditions 1-2) observed absent, registration owned by l3w4-seat-registry branch. Self-referential evidence_runs accepted for an experiment node — the run IS the evidence.