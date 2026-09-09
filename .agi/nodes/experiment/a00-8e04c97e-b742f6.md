---
id: experiment:a00-8e04c97e-b742f6
mint_id: bf77d5393e26432585d7ee4399027a21
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.7
edited_by: a00-8e296aa5
evidence_runs:
  - experiment:a00-8e04c97e-b742f6
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3fdd8edcae6f859c
season: 2
title: A00 8e04c97e b742f6
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-8e04c97e-b742f6

## Experiment

SD.08 KID-2 slice: built the **per-role SKILL.md slice mechanism** (owner's "different roles also would be shown different parts of the skill.md … command structure, hierarchy, and how everyone plays their part — the biggest one any role needs to know"). Did NOT touch `skills/agi/SKILL.md`, `.agi/context/INJECTION.md` or `rotate.py` (other owners this iteration).

**New artefact: `extensions/agi/bin/rolslice.py`** + `extensions/agi/tests/test_rolslice.py`. Mechanism, per the hypothesis's own rule (no second role description):

1. Resolves the role against the machine-readable hierarchy (`hierarchy.load_seats` / `load_ladder`) and **fails loudly** on an unknown role — a slice can never drift from what dispatch resolves (verified `test_unknown_role_fails_loud`).
2. Injects `hierarchy.render()` — THE chart — into every slice, so each role carries "how everyone plays their part" from the same machine-readable source every other renderer reads.
3. Selects SKILL.md sections by a machine-readable `CORE` + `ROLE_SECTIONS` map. CORE (CLI, Safety rails, Verdict taxonomy, Three tiers, Choosing a runtime) reaches every role; protocol sections reach only the roles that run them (Iteration protocol -> parent & kid, Director economics/HANDOFF/COMPLETE/git grid -> director).
4. `--measure` counts slice tokens with tiktoken o200k so before/after is real numbers.

**Measured per-role, slice tokens + impact on the full prompt total** (baseline from the corrected a00-0f527d4c measurement: SKILL 13180 + INJECTION 8406 = 21586 static prefix; per-role totals kid 22734 / parent 24657 / director 24690 / prime 25450 / liaison 24258):

| role | slice tok | =% SKILL | total before | total after | total cut |
|---|---|---|---|---|---|
| kid | 4703 | 36% | 22734 | 14257 | **37.3%** |
| parent | 5153 | 39% | 24657 | 16630 | **32.6%** |
| director | 8134 | 62% | 24690 | 19644 | 20.4% |
| prime_director | 8136 | 62% | 25450 | 20406 | 19.8% |
| liaison | 8134 | 62% | 24258 | 19212 | 20.8% |

Slice alone cuts total prompt 20-37% per role. The director bucket is fatter because it legitimately owns HANDOFF/COMPLETE/git-grid — the comprehension-wins metric over raw token count.

**MUST-NOT-LOSE check:** every SKILL.md safety marker survives the leanest (kid) slice (verified `test_must_not_lose_markers_are_in_skill_slices`: Never create / grid.py checkout / node count / safety / prayer / kill). The key-floor rule and kill-by-PID procedure live in HANDOFF.md + the successor briefs, NOT SKILL.md, so they are structurally out of scope for this slice — not at risk.

**Slice discipline:** touched ONLY `rolslice.py` (new) + `test_rolslice.py` (new) + this node. Moves 3/4/5 and the INJECTION.md graph-stream restructure are separate slices.

## Evidence

```
SKILL.md full 13180 tok ; slices: kid 4703 (36%) / parent 5153 (39%) / director 8134 (62%)
pytest extensions/agi/tests/ -q  ->  2209 passed, 1 skipped  (rolslice tests included)
05 passed in 0.12s   (rolslice suite alone)
```

Slice assembly output extracts the hierarchy chart + role sections; full run:
`/home/ubuntu/work/agi/tmp/venv/bin/python extensions/agi/bin/rolslice.py --all --measure --root .agi`
(venv has tiktoken+yaml; base python lacks tiktoken — same env note as the sibling measurement rounds).

## Agent Notes
Per-role SKILL slice mechanism built (rolslice.py + test). Slice = hierarchy.render chart + CORE sections (CLI, safety rails, verdict taxonomy, three tiers) + role protocol sections from a machine-readable map; unknown role fails loud. Measured (tiktoken o200k): kid slice 4703 tok (36% of SKILL) cuts total 37.3%; parent 5153 (39%) cuts 32.6%; director 8134 (62%) cuts 20.4%; prime/liaison ~same as director. Suite green 2209 passed. This covers the SKILL.md half of the 21586 static prefix (13180); the INJECTION.md half (8406, the graph-stream) is a separate slice — per-role totals above assume INJECTION unchanged, so the full 70-90% still needs that slice. Safety markers verified present in the leanest slice.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8e296aa5), accepted. Verified directly, not from the report: rolslice.py + test_rolslice.py exist, rolslice suite passes (5/5) re-run by me. parents resolve, verdict format valid, evidence self-named (legitimate for an experiment). Mechanism honors the no-second-role-description rule (hierarchy.load_seats/load_ladder source, loud failure on unknown role — the right failure mode). Numbers plausible against the corrected baseline; honest that 70-90% of TOTAL is not reached by this slice alone. One caveat: the slice is built but not yet WIRED into brief.py assembly, so the measured savings are potential, not landed — wiring is the next kids job. Verdict lean_proved:70 fair for mechanism-built-and-measured.
<!-- THOUGHT:END -->

## Agent Notes
Per-role SKILL slice mechanism built (rolslice.py+test): hierarchy.render chart + CORE sections + role protocol sections, fails loud on unknown role. Slice cuts total prompt kid 37.3%/parent 32.6%/director 20.4% (tiktoken o200k). Suite green 2209 passed. Covers SKILL half of 21586 static prefix; INJECTION graph-stream slice separate.