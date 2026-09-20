---
id: mvp:grok-bot-restart-respawn
mint_id: 4f1a663e434b436cb3f7f92a55141672
type: mvp
parents:
  - verdict:grok-bot-restart-real-respawn-verdict
next_edges: []
edited_by: a00-d2c9b5c7
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 16805f516aa3180d
season: 2
title: Grok-bot adapter restart respawn MVP
town: core
---
<!-- BODY:BEGIN -->
# mvp:grok-bot-restart-respawn

## MVP

`extensions/agi/bin/adapters/grok_bot_adapter.py` — a real `restart(**kwargs)`
for the `grok-bot` harness, satisfying the `goal:g4.7` adapter contract.

## What it does

- Accepts every channel `dispatch.py` passes an adapter (`harness`, `tier`,
  `context_file`, `agent_id`, `iter_n`, `sess_dir`, `scaffold`, `cli_py`,
  `skill_prompt`, `dispatch_py`, `target`, `parallel`, `max_live`,
  `agent_record`, `brief_tier`, `role`, `ladder_tier`).
- Rebuilds the identical argv via `build_command(...)`.
- `Popen`s it detached (`start_new_session=True`), stdout/stderr appended to
  `sess_dir/output.log`, stdin `DEVNULL`, cwd from `_restart_cwd` (the
  record's existing `worktree`, else `sess_dir.parent.parent.parent`).
- Stamps `agent_record` (`pid`, `status="restarted"`, `restarted_at`) and
  writes `sess_dir/agent.json`.
- Returns the new pid, or `None` on `OSError`.

## Acceptance

`python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q` → green.
`DEFAULT_BIN` stays bare `grok-bot`; `needs_credential` stays `False`;
`dispatch.py` untouched.

What does it produce?
