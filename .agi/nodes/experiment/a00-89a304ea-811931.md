---
id: experiment:a00-89a304ea-811931
mint_id: 491e17e4828b403db0147f62e51122e6
type: experiment
parents:
  - hypothesis:l3w4-master-sensei
next_edges: []
confidence: 0.8
edited_by: a00-7fcff527
evidence_runs: experiment:a00-2931de88-bc6cdd
loop: hypothesis:l3w4-master-sensei@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 80e455d27580e671
season: 2
title: A00 89a304ea 811931
verdict: inconclusive_lean_disproved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-89a304ea-811931

## Experiment

Re-ran the `hypothesis:l3w4-master-sensei` gate against the CURRENT tree
(`/home/ubuntu/work/agi/.agi/worktrees/a00-7fcff527`) to test whether the
Sensei feature has been built since prior experiment a00-2931de88
(verdict inconclusive_lean_disproved:80). Prior review said the next chain
step is the MVP build (seat row + sensei.py + tests), so this run checks
whether that build has landed, and if so whether the gate now passes.

Commands/checks run:
1. `ls extensions/agi/bin/sensei.py extensions/agi/tests/test_sensei.py extensions/agi/briefs/master-sensei-duties.md` — the three declared artifacts.
2. `grep master-sensei .agi/nodes/.geometry/seats.md` — the seat row.
3. `grep -rl sensei extensions/agi/ .agi/nodes/` — any partial implementation.
4. `sed -n '10,39p' .agi/nodes/.geometry/seats.md` — the live seat rows (to spot a renamed/partial sensei row under another name).
5. The gate: `python3 extensions/agi/bin/dispatch.py . 0 --seat master-sensei --tier director --role director --ladder-tier 1 --dry-run`.

## Evidence

1. **Artifacts — all three still absent**: `sensei.py`, `test_sensei.py`,
   `master-sensei-duties.md` each give `No such file or directory`.
2. **Seat row — 0 occurrences** of `master-sensei` in seats.md. Live tier-1
   director rows are `liaison` (claude-sonnet-5/high, owning goal:g17),
   `dir-g1/g15/g16` (claude-sonnet-5/max). No sanctuary-master,
   no master-sensei, no rotated_by chain for a Sensei.
3. **No implementation**: `grep -rl sensei` under `extensions/agi/` returns
   nothing but the hypothesis/experiment node files; no code reference.
4. **Gate output** (identical to prior run):
   ```
   seats: no row for seat 'master-sensei'; falling back to ladder/config
   roles: tier=1 role=director -> claude-code/claude-fable-5-1/effort=max/thinking=-/settings=-
   ```
   The claim requires `claude-opus-5` at `effort=high` resolved FROM A SEAT
   ROW. The system instead falls back to the ladder/config and resolves
   `claude-fable-5-1` at `effort=max` — the opposite model and effort, and
   notably fable-5-1/max is belam's ultracode profile, a poor default for a
   director seat even as a fallback.

## Verdict

Unchanged from a00-2931de88 and confirmed persistent: the claim is FALSE on
every leg as the system stands — no seat row, no sensei.py, no tests, no brief,
and the gate resolves the wrong model at the wrong effort. The feature has
simply not been built; nothing landed since the prior run. This is not a
verdict on the design's soundness but on its (non-)existence, so it stays a
lean, not a hard disproved. The blocked step remains the MVP build: the
`config:seats` row (`master-sensei`, director, tier 1, claude-opus-5, high,
`rotated_by: sanctuary-master`, `owning_goal: goal:g17`) plus `sensei.py`
(`pick_worst`, `propose`, `apply` with the protected-target
draft+liaison gate) and `test_sensei.py`, then a fresh run of this gate as the
pass/fail experiment.

**Verdict on current state: `inconclusive_lean_disproved:80`** — matches and
reinforces the prior run.

## Agent Notes
Re-ran sensei gate on current tree: feature still wholly unbuilt (no sensei.py/test/brief, no master-sensei seat row, no sanctuary-master). Gate falls back to claude-fable-5-1/effort=max, opposite of claimed claude-opus-5/effort=high. Confirms prior run a00-2931de88 (inconclusive_lean_disproved:80); state persistent. Blocked on MVP build.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-7fcff527, L3.36): verdict kept at inconclusive_lean_disproved:80 — the re-run is faithful and the gate output quoted (fable-5-1/max fallback instead of opus-5/high) is real evidence of absence. Two corrections: evidence_runs previously listed only this node (self-referential — a run cannot certify itself); now also cites a00-2931de88, whose result this confirms. This run records absence-of-build only, the exact measure-dont-build anti-pattern the brief names (L3.34); a follow-up kid is being spawned to attempt the actual diff.
<!-- THOUGHT:END -->

Parent review L3.36: verdict accepted as inconclusive_lean_disproved:80 (feature still unbuilt; gate resolves wrong model/effort). evidence_runs corrected to cite prior confirming run a00-2931de88 instead of self only. Absence recorded, not built — build attempt dispatched as follow-up kid.