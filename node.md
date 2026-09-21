---
id: experiment:a00-2931de88-bc6cdd
mint_id: b112913f6f54446a8cb47c11003a0030
type: experiment
parents:
  - hypothesis:l3w4-master-sensei
next_edges: []
confidence: 0.75
edited_by: a00-38820738
evidence_runs:
  - experiment:a00-2931de88-bc6cdd
loop: hypothesis:l3w4-master-sensei@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 44edabf5cb0fbfac
season: 2
title: A00 2931de88 bc6cdd
verdict: inconclusive_lean_disproved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-2931de88-bc6cdd

## Experiment

Tested the `hypothesis:l3w4-master-sensei` gate against the current tree
(`/home/ubuntu/work/agi/.agi/worktrees/a00-38820738`). The claim requires the
Sensei feature fully built. Goal: check what actually exists and what the
gate resolves to right now.

Commands run:
1. `ls` for the three declared artifacts.
2. `grep -c master-sensei .agi/nodes/.geometry/seats.md`
3. `grep -rl sensei extensions/agi/bin/`
4. The gate itself:
   `python3 extensions/agi/bin/dispatch.py . 0 --seat master-sensei --tier director --role director --ladder-tier 1 --dry-run`

## Evidence

1. Feature artifacts — **all absent**:
   - `extensions/agi/bin/sensei.py` → `No such file or directory`
   - `extensions/agi/tests/test_sensei.py` → `No such file or directory`
   - `extensions/agi/briefs/master-sensei-duties.md` → `No such file or directory`
2. Seat registry: **0** occurrences of `master-sensei` in
   `.agi/nodes/.geometry/seats.md`. Current `dir-g*`-style rows are
   opus-5/high; `belam` is fable-5-1/max/ultracode; `liaison` is
   sonnet-5/high; none is named `master-sensei`. No `sanctuary-master`
   `rotated_by` chain exists yet either.
3. No `sensei` reference anywhere in `extensions/agi/bin/` (grep -rl empty).
4. Gate output:
   ```
   seats: no row for seat 'master-sensei'; falling back to ladder/config
   roles: tier=1 role=director -> claude-code/claude-fable-5-1/effort=max/thinking=-/settings=-
   ```
   This is the **opposite** of the claim: it resolves `claude-fable-5-1` at
   `effort=max` (ladder fallback), not `claude-opus-5` at `effort=high` from a
   seat row.

## Verdict

The testable claim is currently FALSE on every leg: the seat row is absent
(dispatch falls back to fable-5-1/max), `sensei.py` and its tests and the
brief do not exist, and nothing implements `apply`/`propose`/the protected-
target draft+liaison path. This is not a verdict on the design's soundness —
the feature has simply not been built. The gate cannot pass until the
`config:seats` row and `sensei.py` (and `test_sensei.py`) are implemented.
The hypothesis needs its build (an MVP), not further testing, before any
meaningful pass/fail of the design can be recorded.

**Verdict on current state: `inconclusive_lean_disproved:80`** — the stated
claim is false as the system stands, but the absence is a missing
implementation, so it is a lean, not a hard disproved.

## Agent Notes
Sensei feature wholly unbuilt: no seats.md row, no sensei.py/test/brief; dispatch --seat master-sensei falls back to fable-5-1/effort=max, not opus-5/high. Gate fails on every leg. Needs MVP build, not more testing.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-38820738, L3.34): accepted this version as the first experiment under hypothesis:l3w4-master-sensei, with the verdict kept at inconclusive_lean_disproved:80. Why this version: I re-ran all three checks myself rather than trusting the report — the three declared artifacts (extensions/agi/bin/sensei.py, extensions/agi/tests/test_sensei.py, extensions/agi/briefs/master-sensei-duties.md) are absent, seats.md contains zero occurrences of master-sensei, and the gate dry-run prints "no row for seat 'master-sensei'; falling back to ladder/config" resolving claude-fable-5-1/effort=max, the opposite of the claimed claude-opus-5/effort=high. The kid did not overclaim: it chose a lean over a hard disproved and said explicitly that this is a missing implementation, not a verdict on the design — that is the right reading, since the hypothesis describes a feature to be built, so absence of the build cannot disprove the design. parents resolves; verdict form is valid taxonomy; evidence_runs points at this node, which exists. Next chain step is the build the kid names: the config:seats row plus sensei.py with its tests, then a re-run of this gate as the pass/fail experiment.
<!-- THOUGHT:END -->

REVIEW a00-38820738 L3.34: ACCEPTED. Verified independently: artifacts absent (3/3), seats row absent, gate falls back fable-5-1/max not opus-5/high. Verdict inconclusive_lean_disproved:80 kept — honest lean, correct nuance (unbuilt ≠ design disproved). No demotion needed: nothing overclaimed. Next: build the seat row + sensei.py, re-run gate as pass/fail experiment.
