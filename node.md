---
id: hypothesis:g141-h-five-skills-say-what-is-true-write-py-is-the-old-setups-writer-and-workflow-py-is-legacy
mint_id: b1419ec401e44dabb8a21e218aeeb59f
type: hypothesis
parents:
  - goal:g1.41
next_edges: []
confidence: 0.8
edited_by: director-general-1
scaffold_hash: 76171befa0582e8b
season: 2
testable_claim: "(H) five skills stop teaching two things the owner overruled, and invent no replacement: (H1) skills/agi-goal, agi-dispatch and agi-corrective each name write.py as the OLD setup's node writer (a post whose row has engine.v 4 edits node files with plain Write/Edit and agi-turn commits, owner 10-01 23:3xZ) and none says write.py is 'the only writer'; (H2) skills/agi, agi-workflow, agi-corrective and agi-dispatch each mark the workflow.py route LEGACY with the owner order (retire it, 10-02 14:01Z) and goal:g5.33, and none calls it 'the only sanctioned' route; the routing itself is unchanged because agi-master-gate still runs every mur through the live workflow.py"
title: "G1.41 H (skills): five skills carry the owner's two overrulings -- write.py is the old setup's writer (engine.v 4 posts use plain Write/Edit), workflow.py is LEGACY until goal:g5.33 replaces each job -- as labels, not reroutes"
town: core
---
# hypothesis:g141-h-five-skills-say-what-is-true-write-py-is-the-old-setups-writer-and-workflow-py-is-legacy

## Measured
- The residue (goal:g1.41 TESTS + SKILLS): skills/agi/SKILL.md:59 says workflow.py run is "**The only sanctioned workflow dispatch route**"; agi-workflow (description + body) teaches `workflow.py` by name; agi-corrective:103 and agi-dispatch:48 send every re-mur through `workflow.py run merge-up-review --harness pi-free`. Owner 10-02 14:01Z (via belam, verbatim in doc:radically-simple-engine around :2136): "we just need to retire workflow.py entirely and stop wasting time on it". agi-goal:13 ("write.py (the only writer)"), agi-dispatch:16 + :61 and agi-corrective:71-81 teach write.py as the writer; owner 10-01 23:3xZ (doc:unified-head :54): a post whose row has engine.v 4 reads with plain Read/cat/grep/git + sect and writes node files with plain Write/Edit, agi-turn signs the commit. skills/agi-node-write/SKILL.md already carries that banner in its description ("OLD SETUP ONLY").
- WHY H2 IS A LABEL: the retirement is goal:g5.33 (active, job by job: "a manifest retires only after its replacement runs"), and skills/agi-master-gate/SKILL.md:148-161 says the master's mur runs read .agi/sessions/workflows/runs/mur-*/verify_R-EFnn.json and "import MAIN's LIVE workflow.py (3 runners)". workflow.py is still the live mur runner today (extensions/agi/bin/workflow.py exists at trunk). A skill that said "do not use it" or named a dispatched-round replacement for mur would break the gate or invent a flow.
- Sizes are not railed (skills are not engine pieces). .claude/skills/* are committed symlinks into skills/: edit skills/ only.

## CLAIM
(H) five skills stop teaching two things the owner overruled, and invent no replacement: (H1) skills/agi-goal, agi-dispatch and agi-corrective each name write.py as the OLD setup's node writer (a post whose row has engine.v 4 edits node files with plain Write/Edit and agi-turn commits, owner 10-01 23:3xZ) and none says write.py is "the only writer"; (H2) skills/agi, agi-workflow, agi-corrective and agi-dispatch each mark the workflow.py route LEGACY with the owner order (retire it, 10-02 14:01Z) and goal:g5.33, and none calls it "the only sanctioned" route; the routing itself is unchanged because agi-master-gate still runs every mur through the live workflow.py.

## Dispatch line
config-max: none / template-max: a one-line banner per skill (the wording is the same sentence in each, quoted from agi-node-write's description for H1) / code: none.

## FALSIFIERS
Greps at the tip, each one line of output: `git grep -n -E 'only sanctioned workflow dispatch route|\(the only writer\)' -- skills` prints 0 lines (trunk: 2) · `grep -c 'engine.v 4' skills/agi-goal/SKILL.md skills/agi-dispatch/SKILL.md skills/agi-corrective/SKILL.md` each >= 1 (trunk: 0 0 0) · `grep -c 'LEGACY' skills/agi/SKILL.md skills/agi-workflow/SKILL.md skills/agi-corrective/SKILL.md skills/agi-dispatch/SKILL.md` each >= 1 AND each of those four files names `g5.33` · NEGATIVE (no invented route): `git diff <cut>..<tip> -- skills | grep '^+' | grep -c -E 'dispatched round|dispatch.py run'` is 0 for the H2 banners, and `git grep -c 'workflow.py run' -- skills/agi-master-gate/SKILL.md skills/agi-merge-pass/SKILL.md` is unchanged (the live route stays documented where it is used). Mutants: a banner without g5.33 · a banner that removes the routing line · agi-goal untouched.

## TESTS
a new skills-truth.t.sh (shell) holding the greps above, no network; the links check (links.py links 0 broken) and test_skills*.py if any (named in the report).

## FILE SCOPE
skills/agi/SKILL.md · agi-workflow · agi-corrective · agi-dispatch · agi-goal (SKILL.md each; NEVER the .claude symlinks, NEVER agi-master-gate / agi-merge-pass: they describe the live route) · the test file (DG2) · the round's experiment node.

## CEILING
1 parent (goal:g1.41) · kids <= 1 (DG5, claude-code Sonnet) · <= 12 added lines per skill (a TWO-operand numstat <cut>..<tip before the paste commit>) · no code · no paid agent run beyond the builder.

## DG1 NOTE (BANKED for the owner, not a blocker)
Whether to move mur OFF workflow.py now is goal:g5.33's schedule, not this round's. Options: (a) keep the label only (this round); (b) build the dispatched-round mur and flip agi-master-gate + agi-merge-pass in ONE landing. Recommendation (a) now, (b) as g5.33's next job, because SM's gate depends on the live runner today. A skill that says "retired" while the master's gate runs on it would be a false green.

## DG1 RULING that landed (SM mur, 8502309d65: RH1)
The first H round labelled four skills and missed the `agi` skill's own copy of the write.py rule (four unlabelled claims). RH1 (9be5ada623) labels them as the OLD setup's (owner 10-01 23:3xZ) as a banner under the section heading and in three lines. Labels only; the HEADING TEXT is unchanged on purpose: extensions/agi/bin/rolslice.py matches it verbatim (a rename would drop the section from the kid / parent / director slices).
