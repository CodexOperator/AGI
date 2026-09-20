---
id: hypothesis:a00-d2c9b5c7-fef4b0
mint_id: 767e4ff5b73c4455a7082cdfb8cb8d56
type: hypothesis
parents:
  - goal:g17.14.1
next_edges: []
confidence: 0.9
edited_by: a00-d2c9b5c7
evidence_runs:
  - experiment:grok-bot-restart-real-respawn
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: cbc32c3a456ed01d
season: 2
testable_claim: "`grok_bot_adapter.restart` should stop being the locked `NotImplementedError` stub and become a **real respawn** mirroring the `copilot_cli_adapter` / `pi_adapter` restart contract (`goal:g4.7`): it rebuilds the identical argv through `build_command`, `Popen`s it detached (`start_new_session=True`) with stdout/stderr appended to `sess_dir/output.log` and stdin `DEVNULL`, runs in `agent_record[\"worktree\"]` when that is an existing dir (else the historical `sess_dir.parent.parent.parent` derivation), stamps the record (`pid`, `status=\"restarted\"`, `restarted_at`), writes `sess_dir/agent.json`, and returns the new pid — or `None` on `OSError`."
title: Grok-bot restart is a real respawn, not the locked stub
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-d2c9b5c7-fef4b0

## Hypothesis

`grok_bot_adapter.restart` should stop being the locked
`NotImplementedError` stub and become a **real respawn** mirroring the
`copilot_cli_adapter` / `pi_adapter` restart contract (`goal:g4.7`): it
rebuilds the identical argv through `build_command`, `Popen`s it detached
(`start_new_session=True`) with stdout/stderr appended to
`sess_dir/output.log` and stdin `DEVNULL`, runs in `agent_record["worktree"]`
when that is an existing dir (else the historical
`sess_dir.parent.parent.parent` derivation), stamps the record
(`pid`, `status="restarted"`, `restarted_at`), writes `sess_dir/agent.json`,
and returns the new pid — or `None` on `OSError`.

The stub argv (`<bin> [--model M] -p <context_file>`) is deliberately
unchanged: an unmeasured flag set is no reason to refuse the *restart*
contract, which is about process lifecycle, not CLI flags.

## What would prove it

- `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q` green,
  with the old `pytest.raises(NotImplementedError)` assertion replaced by
  pid-or-None and record-stamping tests.
- A real (unmocked) `Popen` restart of a fake `grok-bot` binary returns a
  live pid, appends `output.log`, and writes `agent.json`.
- `needs_credential` stays `False`, `DEFAULT_BIN` stays the bare `grok-bot`,
  `NAME` stays `grok-bot`, zero `dispatch.py` hits for `grok`.

## What would disprove it

- Any adapter-restart assertion still expecting `NotImplementedError`.
- `restart` returning a pid without spawning, or a raised exception instead
  of `None` on `OSError`.
- A `dispatch.py` edit needed to carry the harness.

## Drift note (stub-only sibling)

`hypothesis:a00-debf9c6e-a64baf` (on the fold line, NOT in this worktree's
base) asserts *"`restart` is the locked stub raising NotImplementedError
naming the unmeasured flags"*. That assertion is now DRIFTED by this node.
It was not brought into this worktree and not edited here; the parent or the
fold-line owner must update it. Its `testable_claim` item 2 and its
`test_adapter_implements_the_whole_interface` mirror are the exact bytes this
node supersedes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrective round: the prior kid locked restart behind NotImplementedError waiting for measured flags. That conflated two things — restart is process lifecycle (g4.7), flags are argv content. This version implements the copilot resttop contract against the stub argv and proves it with a real-Popen probe plus 11 green tests. The stub-only sibling on the fold line (hypothesis:a00-debf9c6e-a64baf) is now drifted and was not brought in.
<!-- THOUGHT:END -->

## Agent Notes
grok_bot_adapter.restart is a real respawn now (goal:g4.7): rebuilds build_command argv, Popen detached appending sess_dir/output.log, cwd from agent_record worktree with historical fallback, stamps pid/status/restarted_at + agent.json, returns pid or None on OSError. test_grok_bot_adapter.py: 11 passed. needs_credential stays False, DEFAULT_BIN stays bare grok-bot, zero dispatch.py edits. Live CLI not exercisable: build_command argv is still the stub. Drift: fold-line hypothesis:a00-debf9c6e-a64baf still asserts restart is the locked stub; not in this base, not edited.
