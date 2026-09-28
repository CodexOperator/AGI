---
id: hypothesis:skills-load-per-harness-per-tier-from-one-config-cell
mint_id: 75b7d8016cd44ce98b4432650c62524d
type: hypothesis
parents:
  - goal:g4.18.2
  - hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt
next_edges: []
edited_by: director-engine
scaffold_hash: bb896ebca4ddecb8
season: 2
testable_claim: harnesses.<name>.skills tier sets drive the skill segment both adapters append; a pi parent and a pi kid carry exactly their tier set; a new skill enters a tier by the cell only; the emitter is startup-gate admitted; agent-prompt.md skill lines retire
title: "Skills load per harness and per tier from one config cell through the adapter seam; pi parents and kids get their limited set (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:skills-load-per-harness-per-tier-from-one-config-cell

## Measured
Seats see skills through the Claude Skill tool; parents and kids get ONE skill_prompt file (extensions/agi/lib/agent-prompt.md, dispatch.py:844) appended by claude_code_adapter.py:535-536 and pi_adapter.py:108-109. After DH.526 that file names each tier's set in prose -- a second source the moment a skill is added. No harness cell decides whether skills load or which. The startup gate admits only python3 extensions/agi/bin/*.py producers (shell readers refused, measured 05:4xZ), so the seat-side index needs an engine emitter too (TMM.284).

## CLAIM
ONE config cell per harness, harnesses.<name>.skills = {on, tiers: {seat, parent, kid}} with each tier a list of skill names, decides the skill index every adapter appends: the claude_code and pi adapters both build the skill segment from it (name + first description line per skills/<name>/SKILL.md, <= 150 chars a line, folded '>' and inline descriptions both read); a pi parent's and a pi kid's built prompt carry EXACTLY their tier set; a new skill enters a tier by editing the cell only; the same emitter, called as python3 extensions/agi/bin/<emitter>.py --tier seat, is admitted by the startup gate (rotate._producing_refusal(cmd) is None) so the Prime can swap doc:draft-skills-first-turn's ten clauses for one call; DH.526's agent-prompt.md skill lines RETIRE in this round (one source: the cell).

## Dispatch line
config-max: harnesses.<name>.skills in .agi/config.json (on + the three tier lists) -- the cell is the whole rule / template-max: the segment's one-line format lives next to the cell, never in code / code: the emitter + one call in each adapter's skill_prompt build (the resolver that does not exist)

## FALSIFIERS
a tier list in code · a skill name hardcoded anywhere but the cell · the adapters building different segments for the same tier · a pi prompt missing its tier set or carrying another tier's · agent-prompt.md still naming skills · the emitter refused by the startup gate · a new skills/<dir> needing a code edit to reach a tier

## TESTS
new test: a folded and an inline SKILL.md fixture; the cell's tier sets drive a pi parent's and a pi kid's built prompt exactly; a new fixture skill added to one tier by the cell only appears there; rotate._producing_refusal on the emitter cmd is None · plus test_claude_code_adapter.py test_pi_adapter*.py test_adapters_spawn_cwd.py test_dispatch.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp)

## FILE SCOPE
extensions/agi/bin/<one new emitter>.py · extensions/agi/bin/adapters/claude_code_adapter.py + pi_adapter.py (the skill_prompt build only) · .agi/config.json (harnesses.*.skills only) · extensions/agi/lib/agent-prompt.md (retire DH.526's lines) · extensions/agi/tests/<one new test> · build node for the new emitter (write.py create build) · the kid's own node

## CEILING
HARD CAP: 2 kids (1: cell + emitter + test, 2: adapter wiring + agent-prompt retirement) · <= 60 production lines · <= 120 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. BASE: cut from the DH.526 loop tip once 526 clears its mur.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version (director-engine; TMM.284 re-scoped by TMM.286 + TMM.287). OWNER 05:48:37Z, verbatim: "Let’s do the doc for now then the code update. Make it go through cc adapter via templates or configs so it can be adapted to pi harness as well and also make sure parents and kids also get appropriate skills. Those can just be parent and kids also brief edits as they’re more limited in their skill needs." OWNER 05:53:36Z, verbatim: "Once the code is live make the pi parents and kids use it as well instead with their more limited set of commands." QUEUED behind DH.526 (it retires 526s lines, so it is cut from 526s cleared tip).
<!-- THOUGHT:END -->
