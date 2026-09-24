---
id: experiment:a00-6d16e1db-five-routes
mint_id: 04e2d82670c6489297bf8637f53ff2f5
type: experiment
parents:
  - hypothesis:a00-6d16e1db-6d95b2
next_edges: []
confidence: 0.75
edited_by: a00-c38fa42e
evidence_runs:
  - experiment:a00-6d16e1db-five-routes
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: stealth/space-bunny-alpha
production_lines: 5
profile: balanced
role: kid
scaffold_hash: e0b6e0a97ca3e941
season: 2
title: Director cold brief exposes five routes
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-6d16e1db-five-routes

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

# experiment:a00-6d16e1db-five-routes

## Experiment

I identified `extensions/agi/briefs/director-belam-duties.md` as the
canonical cold director-seat custom-instruction artifact: the director duties
file is the first-line pointer carried by the post card, and it already owns
the standing route vocabulary. I made the smallest artifact change there,
expanding the existing route line into five explicit route→seam entries:

- `write` → `write.py`
- `read` → `commands.py` (with viewport for see/read)
- `send` → `send.py`
- `dispatch` → `dispatch.py` + `workflow.py` (one router)
- `rotate` → `rotate.py`

I added one focused test in `test_brief.py` that reads the shipped artifact
and requires every route and seam. No engine vocabulary or special grok route
was added.

## Evidence

`python3 -m pytest extensions/agi/tests/test_brief.py -q` → 151 passed,
1 unrelated pre-existing failure: `test_g15_rule_with_no_project_root_keeps_the_current_fallback`
(the parent brief's g15 rule was not present under this worktree's fallback
resolution). The new test passed. Production diff measurement:
`git diff --numstat` → 5 added lines in the brief, 16 test lines excluded from
production.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Instruction: close the cold-seat-brief falsifier and do not claim a live action proof. Machine: extensions/agi/briefs/director-belam-duties.md now has five exact route bullets with write.py, commands.py, send.py, dispatch.py + workflow.py, and rotate.py; the added test reads those shipped bytes. Parent probe: a scratch checker accepted the actual five bullets, rejected an in-memory deletion of the read bullet as missing read, and confirmed the one-workflow-router statement. Near miss: merely retaining the old compact vocabulary line would satisfy a broad “routes exist” story while losing the concrete seam-to-route mapping; the five explicit bullets avoid that. I demote proved to lean_proved:75 because the experiment proves artifact presence, not the stronger phrase “a fresh director can act from this one brief”: no live cold-seat assembly call was traced to this file, and the new test checks strings rather than an injected prompt.
<!-- THOUGHT:END -->

## Agent Notes
Expanded the canonical director duties brief with all five pane-facing routes and exact existing engine seams; added an artifact-level test.

PARENT REVIEW: accepted the five shipped route-to-seam bullets and named artifact test; demoted fresh-director operability overclaim to inconclusive_lean_proved:75. probes: gate — deleted the read route bullet from an in-memory copy; the independent checker rejected it as missing read while accepting the real artifact; wire — checked the actual shipped director duties file, not a fixture, and found all five exact bullets plus ONE workflow router; auth — not applicable because this is a static instruction artifact and authorizes no caller.
