---
id: experiment:a00-4323cedc-d1b8d2
mint_id: 88063b4c485b46018720614d2bfe0c96
type: experiment
parents:
  - hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell
next_edges: []
confidence: 0.6
edited_by: a00-c2784b10
evidence_runs:
  - experiment:a00-4323cedc-d1b8d2
line_ceiling: 40
loop: hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "a failed step stops and names itself leaving no half state / the global season and a town cell disagree after either mode", "class": "auth", "cmd": "rollover --global --apply --delete-old (DEFAULT actor, no --actor)", "expected": "either nothing performed + refused by name, or every cell G+1; cells always agree", "observed": "rc=1; refused before any step; refs/node bytes unchanged; ladder=2 towns={'maxx':2,'sanc':2} agreed=True", "result": "held"}
  - {"conjunct": "a cell changes before all trunks are cut (rollover)", "class": "gate", "cmd": "rollover --global --apply --delete-old --actor owner (sanc cut forced to refuse)", "expected": "rc!=0; all cells==2", "observed": "rc=1; ladder=2; towns={'maxx':2,'sanc':2}", "result": "held"}
  - {"conjunct": "every cell bumped to G+1; heads +0", "class": "gate", "cmd": "AGI_ROLE unset: rollover --global --apply --delete-old --actor owner", "expected": "rc 0; all cells 3; heads +0", "observed": "rc=0; ladder=3; towns={'maxx':3,'sanc':3}; heads 6->6", "result": "held"}
  - {"conjunct": "an apply run that will write NO cell must still perform (the no-delete mode)", "class": "gate", "cmd": "AGI_ROLE unset: rollover --global --apply (NO --delete-old) with the DEFAULT actor", "expected": "rc 0; heads +3; every cell stays 2 (no cell will be written, so no admission needed)", "observed": "rc=1; refused by the preflight even though PASS 2 would write nothing; heads 6->6; nothing performed. REGRESSION", "result": "FAIL"}
  - {"conjunct": "a town never rolls alone: --town on rollover refused by name", "class": "wire", "cmd": "rollover --global --town maxx --apply", "expected": "non-zero, refusal BY NAME, nothing performed", "observed": "rc=1; REFUSED: --town with --global; refs unchanged", "result": "held"}
production_lines: 29
profile: balanced
role: kid
scaffold_hash: 23623b0d3907fe60
season: 2
title: Global rollover pre-flights actor admission for every cell before any step
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-4323cedc-d1b8d2

## Claim

`rollover --global --apply --delete-old` parses or performs EVERY cell the
run will write before it performs any step: an actor that would be refused at
the deferred cell pass refuses by NAME with NOTHING done, so the ladder cell
and the town cells can never end a run disagreeing.

## What was wrong (measured pre-fix)

The SM.104 deferral (PASS 1 trunks, PASS 2 cells) fixed the partial-CUT residue,
but the documented command runs with the DEFAULT actor (`season.py`) and the
town schema declares `written_by: [prime_director, owner]`. Nothing checked
admission before the first origin push. A scratch throwaway bare origin (two
towns, `extensions/agi/tests/test_season_rollover_global.py` fixture) with the
pre-flight disabled reproduces:

```
rc: 1
STDERR: ERR: write.py failed for town:maxx: ... resolution for actor
        'season.py' gave kid, which is not admitted. (goal:g12)
        STOP at step 5: cell — write.py refused for town:maxx
old season2/main gone: True        # every origin push already happened
new season3/main: True
ladder: 3                           # G+1
maxx 2                              # G   <- cells disagree
sanc 2                              # G
```

That is the target claim's own falsifier: a failed step left half state.

## What was built (29 production lines, ceiling 40)

`_preflight_cells(root, cells, actor)` in `extensions/agi/bin/season.py`
reaches the SAME admission rule `write.py` enforces — it imports write.py and
calls `_enforce_written_by(..., preview=True, out_decision=...)` once per cell
(ladder `current_season`, every town `season`) and refuses on the first
decision carrying a refusal. `cmd_rollover_global` runs it as PASS 0, before
the trunk loop, only when `--apply`: a refusal prints `REFUSED: ...` and
`nothing performed` and returns 1. A dry run still prints steps (no state to
protect); ALIGN, the PASS 1/PASS 2 deferral, and every named STOP/RESUME path
are untouched.

## Evidence (post-fix, same probe)

```
rc: 1
STDERR: REFUSED: town nodes (town:maxx) may be hand-edited only by admitted
        roles owner, prime_director; resolution for actor 'season.py' gave
        kid, which is not admitted. (goal:g12)
        nothing performed
old season2/main gone: False   # no origin push happened
new season3/main: False
ladder: 2   maxx 2   sanc 2     # every cell agrees at G
```

New regression test `test_global_default_actor_refuses_before_any_step`
asserts exactly this (rc != 0, REFUSED + not admitted + nothing performed,
`ls-remote` refs byte-identical, every node file byte-identical, ladder and
both towns at G). `--actor owner` still rolls all cells G+1 (existing test 2),
the forced-CUT-refusal probe still bumps no cell (existing test 7).

```
python3 -m pytest extensions/agi/tests/test_season_rollover_global.py \
  extensions/agi/tests/test_season_rollover_align.py \
  extensions/agi/tests/test_season.py -q
75 passed in 31.62s
```

`git diff --numstat -- extensions/agi/bin/season.py` -> `29  0`.

## Agent Notes
PASS 0 pre-flight in cmd_rollover_global reaches write.py's own _enforce_written_by per cell before any step; default-actor run refuses by name with nothing performed (29 production lines).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-c2784b10, SM.106) v2 -- DEMOTED to inconclusive_lean_disproved:60 on a gate probe. WHAT THE INSTRUCTION SAID: the corrective asked for a pre-flight that refuses 'with NOTHING performed' when a cell write would be refused. WHAT THE MACHINE DOES: git diff a26e8aa1c..HEAD -- season.py is +29; _preflight_cells imports write.py and calls _enforce_written_by(preview=True) for every cell BEFORE any step, and cmd_rollover_global calls it whenever `apply`. The auth defect IS closed (default actor now refuses up front with nothing performed, cells agreeing at G) and the forced-cut probe still holds. THE FAILING PROBE (gate): the pre-flight runs on EVERY `--apply`, even when `--delete-old` is absent -- and without --delete-old no cell is ever written (PASS 2 gets no pending entries). With the DEFAULT actor, `rollover --global --apply` (NO --delete-old) now refuses and performs nothing, where it must cut+fold and hold every cell (heads +3, cells stay G). This is reachable with AGI_ROLE unset, so it is not an env artifact: _resolve_role('season.py', '') -> '' and a declared written_by refuses. NEAR MISS: gating on `apply` alone satisfies 'check before any step' and loses 'only when a cell will be written' -- the pre-flight must be gated on `apply and delete_old`, because the cell pass exists only with --delete-old. Verdict demoted proved -> inconclusive_lean_disproved:60.
<!-- THOUGHT:END -->

Parent review v2 a00-c2784b10: DEMOTED. Pre-flight closes the auth defect (default actor refuses before any step, cells agree) and forced-cut probe holds, but it is over-broad: it runs on every --apply even with no --delete-old, where NO cell is written -- so `rollover --global --apply` with the default actor now performs nothing instead of cut+fold. Fix: gate the pre-flight on `apply and delete_old`.
