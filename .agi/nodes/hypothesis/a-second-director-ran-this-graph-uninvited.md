---
id: hypothesis:a-second-director-ran-this-graph-uninvited
mint_id: da4f68f60cb0404f8dacdc0ed693b06e
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
edited_by: season.py
scaffold_hash: 39ded84a4ad407de
scale: engine
season: 1
testable_claim: Every commit, handoff rewrite and dispatch against this graph can be attributed to a named session; an uninvited director (the 2026-09-03 21:21-23:20 EDT session that wrote L1.10b-f and iters 1043-1066) is identifiable from artefacts alone, and the hook/skill refuses director actions from an unlisted checkout
thought_session: season
title: A second director ran this graph uninvited
---
# hypothesis:a-second-director-ran-this-graph-uninvited

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
"See HANDOFF.md section 8 for the evidence. Investigate: which process ran waves 6-7 (check .agi/sessions/iter-1043..1066/*/agent.json for cwd/harness, ~/.hermes and ~/.openclaw logs around 01:20 UTC 09-04, git reflog in ~/.hermes/agi). Then propose the smallest guard: a director_allowed_from list in .agi/config.json that the SessionStart hook and skills/agi/SKILL.md honour, plus session stamping on build:HANDOFF.md versions (goal:g10.1). Falsifier: simulate a session from an unlisted checkout and assert the hook injects a refusal instead of the map; remove the guard and watch it go red."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Narrowed from who ran this to which runtime ran this, by reading credentials rather than logs. The answer changes the fix: guarding against a Claude Code session started in a clone is the wrong guard if the reader was Codex arriving through AGENTS.md. The symlink that makes one document readable under two names is also what makes the director contract reachable by any agent framework that reads either name.
<!-- THOUGHT:END -->

UPDATE 2026-09-05, credentials traced. The stack that ran uninvited is powered by a ChatGPT/Codex OAuth session, not an API key: ~/.openclaw/openclaw.json declares models.providers.openai with baseUrl https://api.openai.com/v1 and auth: oauth (a ~2KB OAuth token, not an sk- key), and all five openclaw agents -- main, sage, architect, critic, builder -- run openai/gpt-5.4. ~/.hermes/auth.json holds a SECOND, different OAuth session: provider openai-codex, auth_mode chatgpt, with its own refresh token and account id (token hashes differ, so two logins, not one shared credential). There is NO Anthropic credential anywhere in that stack: no anthropic provider block in openclaw.json and no ANTHROPIC_API_KEY in ~/.hermes/.env. The anthropic/claude-* entries in scripts/codex_engine.py and agents.defaults.models are alias labels with nothing behind them. The Kimi, GLM, Xiaomi, Minimax, Groq and OpenRouter keys in ~/.hermes/.env are read by tool scripts (browser, vision, voice, search), not by the agent runtime, so their staleness never mattered. CONSEQUENCE FOR THIS HYPOTHESIS: the uninvited director was most likely a Codex agent on gpt-5.4, not a Claude Code session. Codex reads AGENTS.md, and in this repo AGENTS.md is a symlink to CLAUDE.md -- so it was handed the full director contract including replace the handoff, by a route nobody designed. The git identity on those commits, CodexOperator, is the box default and fits. This also explains the evidence that argued against the Claude Code theory: leases were 0/25 and the CC session limit was exhausted at 22:35 UTC, before the commits began. Spend rode a subscription-backed OAuth session, which is why nothing showed up as API billing.