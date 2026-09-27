---
id: hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt
mint_id: 94b3853e1e714a548ce41199afc4e9c4
type: hypothesis
parents:
  - goal:g4.18.2
next_edges: []
edited_by: director-engine
scaffold_hash: 1f84fe93256bc5bc
season: 2
testable_claim: agent-prompt.md names parent (agi-dispatch, agi-node-write, agi-send, agi-verify) and kid (agi-node-write, agi-verify) skills by repo path; a test pins both lists and that every path exists; 0 bin lines
title: "Parents and kids on any harness are told their short skill set by path in the one agent prompt (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt

## Measured
extensions/agi/lib/agent-prompt.md (91 lines) is the ONE skill_prompt every adapter appends for every parent and kid (dispatch.py:844 -> claude_code_adapter.py:535-536, pi_adapter.py:108-109) and names NO skill. Seats get skills by the Claude Skill tool; a pi parent or kid has no Skill tool and is never told the skills/<name>/SKILL.md files exist. 10 skills live under skills/ (agi, agi-corrective, agi-dispatch, agi-goal, agi-merge-pass, agi-node-write, agi-rotate, agi-send, agi-verify, agi-workflow).

## CLAIM
agent-prompt.md carries ONE short section naming each tier's skill set by repo path, so a parent and a kid on ANY harness (claude-code or pi) are told which SKILL.md to read before which act: parent = agi-dispatch, agi-node-write, agi-send, agi-verify; kid = agi-node-write, agi-verify. A test pins that every named path exists under skills/ and that both tier lists are present.

## Dispatch line
config-max: none (the per-harness on/off + per-tier set cell is the NEXT round, the adapter-seam emitter) / template-max: THIS round is the template line -- the section in agent-prompt.md IS the change / code: none (0 production lines in bin/)

## FALSIFIERS
a named skill path that does not exist · a tier list missing · the section copying a skill's rules instead of naming its path · any bin/ change · the section over 12 lines

## TESTS
one new test (test_agent_prompt_skills.py): parse the section, assert both tiers present and every skills/<name>/SKILL.md path exists; plus test_claude_code_adapter.py test_decompose_engine.py test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)

## FILE SCOPE
extensions/agi/lib/agent-prompt.md (one new section only) · extensions/agi/tests/test_agent_prompt_skills.py (new) · build:lib-agent-prompt.md THOUGHT (write.py) · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 12 lines added to agent-prompt.md · <= 40 test lines · 0 bin/ lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version (director-engine, dispatch now per TMM.286). OWNER 05:48:37Z in the thought-master pane, verbatim: "Let’s do the doc for now then the code update. Make it go through cc adapter via templates or configs so it can be adapted to pi harness as well and also make sure parents and kids also get appropriate skills. Those can just be parent and kids also brief edits as they’re more limited in their skill needs." Sets judged: parent = agi-dispatch (spawn + judge kids), agi-node-write (every node), agi-send (the F31 rebrief dm), agi-verify (touched tests); kid = agi-node-write, agi-verify. agi-corrective, agi-rotate, agi-goal, agi-merge-pass, agi-workflow are seat flows, left out. The adapter-seam emitter (harnesses.<name>.skills cell) is the next round.
<!-- THOUGHT:END -->
