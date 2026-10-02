---
id: hypothesis:g716111-z4-phase-w-workflow-py-retires-entirely-spawn-is-dispatch-is-workflow
mint_id: 9f5ad37a45a34ad2bdf657799a4dfede
type: hypothesis
parents:
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 2f455ccbe3eaf24d
season: 2
testable_claim: "(W) workflow.py is retired entirely, in ONE round: status deprecated + moved (never `git rm`) for workflow.py, the 30 manifests in extensions/agi/workflows/, skill agi-workflow, config:workflows and hooks/workflow_note.py; the references in skills agi, agi-corrective, agi-master-gate, agi-merge-pass and in config:commands are dropped; the posts that ran it (DG5 4 runs, TM-new 1, DT-1 2, DT-2 1 by ~/track) complete a review as a spawn (agi-kid / engine.kid) instead; Z4.e: 0 workflow.py lines in any live post's ~/track over 24 h AND DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn."
title: "Z4 phase W: workflow.py retires entirely in ONE round (spawn = dispatch = workflow = subagent): workflow.py, the 30 manifests, skill agi-workflow, config:workflows, hooks/workflow_note.py go; four skills + config:commands drop their reference; the v5 users' reviews become spawns"
town: core
---
# hypothesis:g716111-z4-phase-w-workflow-py-retires-entirely-spawn-is-dispatch-is-workflow

## Measured
- belam [owner] 14:01Z (verbatim on goal:g7.16.1.11.15): "we just need to retire workflow.py entirely and stop wasting time on it". Record: goal:g5.33 (owner 09-28) and goal:g4.6 (one spawn path): spawn = dispatch = workflow = subagent.
- Users by ~/track (doc:rse-z4-ladder-out Z4.6, trunk 8356d4114; each post's agi-track record): DG5 4 runs, TM-new 1, DT-1 2, DT-2 1. Retire list per all-is-one's Z4.6: workflow.py, the 30 manifests in extensions/agi/workflows/, skill agi-workflow, config:workflows, hooks/workflow_note.py; references to drop: skills agi, agi-corrective, agi-master-gate, agi-merge-pass, config:commands. NOT re-measured by me: the 30 and the file list are Z4.6's count; the round's first step re-counts them (git ls-files). Old-setup callers (dispatch, heal, adapters, glitch_master) keep their dead branch until they retire with the old setup (Z4.6).
- config:* edits are written by the Prime or the owner only ([config] written_by; pb3 a00-dd443bfa was refused for a kid AND a parent): the round hands belam the byte-exact config:workflows / config:commands edits.

## CLAIM
(W) workflow.py is retired entirely, in ONE round: status deprecated + moved (never `git rm`) for workflow.py, the 30 manifests in extensions/agi/workflows/, skill agi-workflow, config:workflows and hooks/workflow_note.py; the references in skills agi, agi-corrective, agi-master-gate, agi-merge-pass and in config:commands are dropped; the posts that ran it (DG5 4 runs, TM-new 1, DT-1 2, DT-2 1 by ~/track) complete a review as a spawn (agi-kid / engine.kid) instead; Z4.e: 0 workflow.py lines in any live post's ~/track over 24 h AND DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn.

## Dispatch line
config-max: config:workflows + config:commands + the BOTH config:rotations `skills` entries (belam writes, the [config] ring; the pb3 pattern: the round hands him the byte-exact edits at its merge-up, he writes them on a branch, SM lands both in ONE update; belam 14:4xZ) / template-max: the four skills drop the workflow.py references / code: retire, never delete. NOT dispatched yet: a design round for the council first (belam 14:01Z: council re-cuts B/C, HOLD any phase-B round).

## BELAM STEP (belam [rule] 14:4xZ, in W's orders)
Retiring skills/agi-workflow means BOTH config:rotations skills entries (rotations.md, the two `"label": "skills"` lines) must DROP the clause `python3 extensions/agi/bin/write.py build:skills-agi-workflow-SKILL.md 'read payload 2:7'; ` -- test_skills_first_turn_entry names every live skills/agi-* dir, so a dead clause or a missing dir reds it. Measured on the trunk f9f502360 (each entry run through `/bin/sh -c`, stdout+stderr): the clause occurs ONCE per entry; 6205 B now -> 5804 B after the drop (the clause = 401 B); byte_cap 7000 stays (5804 <= 7000). The round hands belam: `sub!` deleting that one clause in both entries, byte_cap unchanged, with the build node build:skills-agi-workflow-SKILL.md retired (never `git rm`) in the same update.

## FALSIFIERS
Z4.e: 0 workflow.py lines in any live post's ~/track over 24 h AND DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn · `git grep -l 'workflow.py' -- skills extensions/agi/bin .agi/nodes/.geometry` hits only retired nodes · test_skills_first_turn_entry 4 passed on the landing tree (both rotations skills entries drop the agi-workflow clause) · negative: no node is `git rm`'d (active + deprecated counts: the sum never drops).

## TESTS
the engine suite on the landing tree (the workflow tests retire with it: name each, never silently delete); `links.py links` broken 0; a spawn-as-review dry run by one thought post.

## FILE SCOPE
workflow.py · extensions/agi/workflows/*.md|js manifests · skills/agi-workflow · hooks/workflow_note.py · references in skills agi, agi-corrective, agi-master-gate, agi-merge-pass · config:workflows + config:commands (belam). Nothing else.

## CEILING
1 parent · kids <= 3 · one round · regular review; the config edits = belam's.
