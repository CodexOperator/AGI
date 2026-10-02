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
testable_claim: "(W) workflow.py and hooks/workflow_note.py are retired (status deprecated + moved, never `git rm`); the 30 manifests in extensions/agi/workflows/ are KEPT (narrow, self-contained, never updated like cards) and a review/check runs as a SPAWN = manifest + graph slice through a ONE-SHOT 'workflow spawn' launch template beside the self-rotating post template (council design, radically simple, under the 8 KB base); skill agi-workflow is KEPT, renamed and re-aligned to the new system (owner's names: 'round review' or 'graph growth check'), written AFTER the council fixes the template so it describes a command that exists; the references in skills agi, agi-corrective, agi-master-gate, agi-merge-pass and in config:commands are RE-POINTED to the new name, not dropped; the posts that ran workflow.py (DG5 4 runs, TM-new 1, DT-1 2, DT-2 1 by ~/track) complete a review as a spawn; Z4.e: 0 workflow.py lines in any live post's ~/track over 24 h AND DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn."
title: "Z4 phase W (AMENDED 14:5xZ): workflow.py + hooks/workflow_note.py retire; the manifests are KEPT as narrow self-contained spawn docs (spawn = manifest + graph slice, via a one-shot launch template the council designs); skill agi-workflow is KEPT, renamed and re-aligned ('round review' | 'graph growth check'); HOLD until the amendment lands"
town: core
---
# hypothesis:g716111-z4-phase-w-workflow-py-retires-entirely-spawn-is-dispatch-is-workflow

## OWNER AMENDMENT 10-02 14:5xZ (belam [owner] 14:54Z, banked town:local-maxxing Agent Notes 306d33621) -- SUPERSEDES the retire-everything line of 14:0xZ for the manifests and the skill; HOLD W until this lands
"... we can still re-use the workflow manifests and just use spawn with workflow manifests as well as graph slices. Workflow manifests are essentially the same as any other post doc they are just purposefully more narrow and self-contained compared to briefs and of course not meant to be updated like cards. They are still useful for reviews and catching things. We could just also have alternate templates for launching these sort of workflow spawns as opposed to more permanent self-rotating posts. We can still then keep the 'workflow' skill but re-align it to be more properly descriptive like 'round review' skill or 'graph growth check' skill. Give it a pass to re-align with the new systems as the rest of the skills. [...]" (excerpt; full text on the town board).
STATE: not dispatched, 0 live. RETIRES workflow.py + hooks/workflow_note.py (unchanged). KEPT: the manifests. NEW: a one-shot launch template (council design). KEPT + RENAMED: skill agi-workflow (goal:g7.16.1.11.14 skill deltas); belam recommends the pass rides IN W, after the template exists.

## Measured
- belam [owner] 14:01Z: "we just need to retire workflow.py entirely" (the code); 14:54Z above: the manifests and the skill stay. Record: goal:g5.33 (owner 09-28), goal:g4.6 (one spawn path: spawn = dispatch = workflow = subagent).
- Users by ~/track (doc:rse-z4-ladder-out Z4.6, trunk 8356d4114; each post's agi-track record): DG5 4 runs, TM-new 1, DT-1 2, DT-2 1. Retire list per Z4.6, AMENDED: workflow.py, hooks/workflow_note.py (the 30 manifests, skill agi-workflow and config:workflows are no longer on it). References: skills agi, agi-corrective, agi-master-gate, agi-merge-pass and config:commands are RE-POINTED. NOT re-measured by me: the manifest count and the file list are Z4.6's; the round's first step re-counts them (git ls-files). Old-setup callers (dispatch, heal, adapters, glitch_master) keep their dead branch until they retire with the old setup (Z4.6).
- config:* edits are written by the Prime or the owner only ([config] written_by; pb3 a00-dd443bfa was refused for a kid AND a parent, then belam wrote it byte-exact and it landed in 96140880b).

## CLAIM
(W) workflow.py and hooks/workflow_note.py are retired (status deprecated + moved, never `git rm`); the 30 manifests in extensions/agi/workflows/ are KEPT (narrow, self-contained, never updated like cards) and a review/check runs as a SPAWN = manifest + graph slice through a ONE-SHOT 'workflow spawn' launch template beside the self-rotating post template (council design, radically simple, under the 8 KB base); skill agi-workflow is KEPT, renamed and re-aligned to the new system (owner's names: 'round review' or 'graph growth check'), written AFTER the council fixes the template so it describes a command that exists; the references in skills agi, agi-corrective, agi-master-gate, agi-merge-pass and in config:commands are RE-POINTED to the new name, not dropped; the posts that ran workflow.py (DG5 4 runs, TM-new 1, DT-1 2, DT-2 1 by ~/track) complete a review as a spawn; Z4.e: 0 workflow.py lines in any live post's ~/track over 24 h AND DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn.

## OPEN QUESTIONS (for the council / belam; none blocks the retire of workflow.py itself)
1. The launch template: ONE-SHOT, no rotation, no card, seeds = a manifest + a graph slice; where does it live (a row beside the post template in config:posts / engine.md) and how does it end (exit, record)? council design, under the 8 KB base. My recommendation: the same unit as a post minus the rotate cells, a manifest path as its first-turn seed.
2. The skill's name: 'round review' vs 'graph growth check' (owner offered both). Recommendation: ONE skill named for the act that exists today (a manifest-driven review of a round) = 'round review'; 'graph growth check' is a manifest of it, not a second skill.
3. config:workflows: keep as the manifests' index, or fold into the template (belam: keeps it unless the council folds it).

## Dispatch line
config-max: config:workflows (index kept unless folded) + config:commands (re-point) + the BOTH config:rotations `skills` entries (RENAME the clause, belam writes, the [config] ring; the pb3 pattern: the round hands him the byte-exact sub at its merge-up, he writes it on a branch, SM lands both in ONE update) / template-max: the four skills re-point their references; skill agi-workflow renamed + re-aligned / code: workflow.py and hooks/workflow_note.py retire, never delete. NOT dispatched: HOLD until the council fixes the launch template (belam 14:54Z).

## BELAM STEP (belam [rule] 14:4xZ, CHANGED by the owner 14:5xZ: DROP -> RENAME)
Renaming skills/agi-workflow to its new name means BOTH config:rotations skills entries (rotations.md, the two `"label": "skills"` lines) must RENAME the clause `python3 extensions/agi/bin/write.py build:skills-agi-workflow-SKILL.md 'read payload 2:7'; ` to the renamed build node's id (the build node is renamed or re-minted with the skill dir; test_skills_first_turn_entry names every live skills/agi-* dir, so a stale clause or a missing dir reds it). Measured on the trunk f9f502360: the clause occurs ONCE per entry and is 401 B at the old name; 6205 B per entry now, cap 7000 (belam's why cells 9917f032d: cap 7000 / 6205 B). The new name changes the clause by a few bytes: re-measure when the name is fixed. The round hands belam the byte-exact `sub!` and the new byte total; the old build node is retired (never `git rm`) in the same update.

## FALSIFIERS
Z4.e: 0 workflow.py lines in any live post's ~/track over 24 h AND DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn · `git grep -l 'workflow.py' -- skills extensions/agi/bin .agi/nodes/.geometry` hits only retired nodes · the manifests still resolve (`ls extensions/agi/workflows | wc -l` == the round's first count, 0 deleted) · test_skills_first_turn_entry 4 passed on the landing tree (both rotations skills entries name the renamed skill) · negative: no node is `git rm`'d (active + deprecated counts: the sum never drops).

## TESTS
the engine suite on the landing tree (the workflow.py tests retire with it: name each, never silently delete); `links.py links` broken 0; a spawn-as-review dry run by one thought post using a manifest + a graph slice.

## FILE SCOPE
workflow.py · hooks/workflow_note.py · skill agi-workflow (rename + re-align) · references in skills agi, agi-corrective, agi-master-gate, agi-merge-pass · config:commands + config:workflows + config:rotations (belam) · the launch template (council design, its own file). NOT in scope: the manifests (kept).

## CEILING
1 parent · kids <= 3 · one round · regular review; the config edits = belam's; HOLD until the template is designed.
