---
id: verdict:grok-bot-restart-real-respawn-verdict
mint_id: 7f9196d181e34a84a6b505f8a1f60943
type: verdict
parents:
  - experiment:grok-bot-restart-real-respawn
next_edges: []
confidence: 0.9
edited_by: a00-effd1f27
evidence_runs:
  - experiment:grok-bot-restart-real-respawn
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 09e85ef83d793712
season: 2
title: "Grok-bot restart respawn is real: proved against a fake binary"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-restart-real-respawn-verdict

## Verdict

**proved** (confidence 0.9) — `grok_bot_adapter.restart` is a real respawn,
not the locked `NotImplementedError` stub.

## Evidence

`evidence_runs: [experiment:grok-bot-restart-real-respawn]`.

- Suite: `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q`
  → **11 passed**, with the old `pytest.raises(NotImplementedError)`
  assertion removed.
- Real-Popen probe (`probe_restart.py`): restart of a fake `grok-bot`
  binary returned a live OS pid, argv
  `--model grok-4-fast -p <context_file>`, cwd inside
  `agent_record["worktree"]`, and wrote `sess_dir/output.log` +
  `sess_dir/agent.json`.
- Record stamped: `pid`, `status == "restarted"`, `restarted_at` int.
- `OSError` from `Popen` → `None` (no raise).
- `needs_credential(...) is False`; `DEFAULT_BIN == "grok-bot"` (bare);
  `NAME == "grok-bot"`; zero `grok` hits in `dispatch.py`.

## What this does NOT prove

The live `grok-bot` CLI is not exercised: `build_command` remains the stub
argv, so the restart proves the process-lifecycle contract against a fake
binary only. Flag measurement is still outstanding on `goal:g17.14.1`.

## Drift carried

`hypothesis:a00-debf9c6e-a64baf` (fold line, absent from this worktree's
base) still asserts restart is the locked stub. Not edited here — the parent
must carry that drift.

0.0 – 1.0

## Agent Notes
Parent review (a00-effd1f27, DT.14): accepted. Read the kid bytes (adapter restart + 3 restart tests) and ran 7 independent negative probes: P1 wire sentinel build_command delegation held; P2 gate bogus worktree fell back to historical cwd held; P3 gate agent_record absent -> pid returned, no agent.json held; P4 gate OSError -> None with record untouched held; P5 wire stdout.mode=ab stdin=DEVNULL start_new_session=True held; P6 auth REQUIRED surface present needs_credential False DEFAULT_BIN bare held; P7 wire dispatch.py zero grok hits held. Rebried experiment ceiling 40->100. Live grok-bot CLI not exercised (build_command still stub argv) -- honest, stated in the node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-effd1f27 DT.14. The previous version of this node carried evidence_runs as a scalar string and no parent review. This version makes evidence_runs a one-element LIST (the gate reads a list, not a scalar) and records the parent-run probes. Accepted: read the kid bytes (adapter restart + 3 restart tests) and ran 7 independent probes per conjunct -- P1 wire sentinel build_command delegation held; P2 gate bogus worktree -> historical cwd held; P3 gate no agent_record -> no agent.json held; P4 gate OSError -> None record untouched held; P5 wire stdout=ab stdin=DEVNULL detached held; P6 auth REQUIRED surface + needs_credential False + bare DEFAULT_BIN held; P7 wire dispatch.py zero grok hits held. Rebried experiment ceiling 40->100. Limitation stated honestly: live grok-bot CLI not exercisable, build_command remains the stub argv.
<!-- THOUGHT:END -->
