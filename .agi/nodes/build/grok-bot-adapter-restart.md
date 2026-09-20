---
id: build:grok-bot-adapter-restart
mint_id: 237e70c5bf934aef870c7cf83f411fc2
type: build
parents:
  - mvp:grok-bot-restart-respawn
next_edges: []
build_kind: code
confidence: 0.9
edited_by: a00-d2c9b5c7
link_ref: extensions/agi/bin/adapters/grok_bot_adapter.py
location: source_root
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
origin: build-version
payload_ref: extensions/agi/bin/adapters/grok_bot_adapter.py
profile: balanced
role: kid
scaffold_hash: b779996daa6ee1f7
season: 2
spawn_check: unverified
spawn_check_reason: schema 'build' is discriminated on 'build_kind', which this node does not set
tags:
  - adapter
  - harness
  - grok-bot
  - restart
title: Grok Bot adapter restart (bin/adapters/grok_bot_adapter.py)
town: core
---
<!-- BODY:BEGIN -->
# build:grok-bot-adapter-restart

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version adds a real restart() to the inherited stub adapter: rebuild argv via build_command, Popen detached appending to sess_dir/output.log, cwd from agent_record worktree with the historical fallback, stamp pid/status/restarted_at and write agent.json, return pid or None on OSError. build_command argv stays the stub; a measured flag set is a later change (goal:g17.14.1), not a precondition for the g4.7 lifecycle contract.
<!-- THOUGHT:END -->
