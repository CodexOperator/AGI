---
id: hypothesis:a-second-director-ran-this-graph-uninvited
mint_id: da4f68f60cb0404f8dacdc0ed693b06e
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
edited_by: director
scaffold_hash: 39ded84a4ad407de
scale: engine
testable_claim: Every commit, handoff rewrite and dispatch against this graph can be attributed to a named session; an uninvited director (the 2026-09-03 21:21-23:20 EDT session that wrote L1.10b-f and iters 1043-1066) is identifiable from artefacts alone, and the hook/skill refuses director actions from an unlisted checkout
thought_session: L1.08
title: A second director ran this graph uninvited
---
# hypothesis:a-second-director-ran-this-graph-uninvited

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
"See HANDOFF.md section 8 for the evidence. Investigate: which process ran waves 6-7 (check .agi/sessions/iter-1043..1066/*/agent.json for cwd/harness, ~/.hermes and ~/.openclaw logs around 01:20 UTC 09-04, git reflog in ~/.hermes/agi). Then propose the smallest guard: a director_allowed_from list in .agi/config.json that the SessionStart hook and skills/agi/SKILL.md honour, plus session stamping on build:HANDOFF.md versions (goal:g10.1). Falsifier: simulate a session from an unlisted checkout and assert the hook injects a refusal instead of the map; remove the guard and watch it go red."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Director-minted after the owner confirmed the 09-03 night session was not theirs. The handoff worked perfectly for a reader nobody invited; that is the finding."
<!-- THOUGHT:END -->
