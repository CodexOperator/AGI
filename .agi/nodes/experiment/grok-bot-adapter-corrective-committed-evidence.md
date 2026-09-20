---
id: experiment:grok-bot-adapter-corrective-committed-evidence
mint_id: da2c6afae4524e8fb151b97587b9551e
type: experiment
parents:
  - hypothesis:a00-e0ab0dcc-d7d5f1
next_edges: []
edited_by: a00-e0ab0dcc
line_ceiling: 40
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 174
profile: balanced
rebrief_request: 174 production lines (adapter 162 + config 12) > 2x ceiling 80; overage inherent to re-adding committed bytes verbatim; request ceiling 180
role: kid
scaffold_hash: 3dddafedfbb98467
season: 2
title: "grok-bot adapter corrective: committed verbatim bytes, superset tests, real respawn probe"
town: core
---
# experiment:grok-bot-adapter-corrective-committed-evidence

## What was done

The corrective round for `goal:g17.14.1`: bring the committed DT.14/live-config
bytes forward verbatim, clear the three MUR residues, and produce honest
in-tree evidence. No re-design; no `dispatch.py` edit.

1. **Adapter (NEW, from `e554c440c`).**
   `git show e554c440c:extensions/agi/bin/adapters/grok_bot_adapter.py` ->
   `extensions/agi/bin/adapters/grok_bot_adapter.py`, 162 lines. The brought
   file's sha256 equals the committed blob's sha256
   (`66b7891f...10826081c`), so the bytes are verbatim.

2. **Config row (dependency of `goal:g17.14.2`, not authored here).**
   Inserted `harnesses.grok-bot` after `copilot-cli` in `.agi/config.json`,
   exactly as `ca330ac35` has it: `adapter: grok_bot`,
   `allowed_extra: [grok-4, grok-4-fast]`,
   `bin: /home/ubuntu/.npm-global/bin/grok-bot`,
   `models: {kid: grok-4-fast, parent: grok-4}`. JSON re-parses and the row
   resolves through `adapters.resolve`. **This is `goal:g17.14.2`'s
   deliverable**, carried only so the live-config tests can run.

3. **Superset test file (NEW).**
   Base `test_grok_bot_adapter.py` from `e554c440c` (restart tests), then
   appended the live-config block from `ca330ac35` (line 102 onward:
   `_project_root`, `live_cfg`, `test_live_config_grok_row_resolves`,
   `test_live_bin_cell_threads_through_to_argv`,
   `test_live_config_peers_still_resolve`,
   `test_dispatch_still_has_zero_grok_hits`). 246 lines; 15 tests; both sets
   present, `_project_root`/`live_cfg` exactly once. Residue R3 cleared.

4. **Committed real respawn probe (NEW, residue R1).**
   `extensions/agi/tests/probes/probe_grok_bot_restart.py` — no mocking: writes
   a throwaway shell script that echoes argv and sleeps, points the harness
   `bin` at it, calls `restart` through real `subprocess.Popen`, prints new
   pid, `is_alive`, argv seen, stamped record, `agent.json` and `output.log`
   existence, then kills the child. Real stdout captured to
   `extensions/agi/tests/probes/probe_grok_bot_restart.out` (15 lines).

## Results

**Adapter tests — green (15 passed):**

    $ PYTHONPATH=/tmp/pytestenv python3 -m pytest \
        extensions/agi/tests/test_grok_bot_adapter.py -q
    15 passed in 0.42s

**Adapter-suite regression — green (35 passed):**

    $ PYTHONPATH=/tmp/pytestenv python3 -m pytest extensions/agi/tests/test_adapters.py -q
    35 passed in 0.48s

**Probe output (real, committed):**

    NAME grok-bot
    DEFAULT_BIN grok-bot
    needs_credential False
    REQUIRED ['build_command', 'child_env', 'is_alive', 'restart', 'needs_credential']
    new_pid 1733710 is_alive True
    argv_seen --model grok-4-fast -p /tmp/grokprobe-xrjai2w1/context.md
    record {"id": "probe", "worktree": "/tmp/grokprobe-xrjai2w1", "pid": 1733710, "status": "restarted", "restarted_at": 1789887436}
    agent_json { ... "pid": 1733710, "status": "restarted" ... }
    output_log_exists True

A live pid and `is_alive True` are evidence a stub cannot produce.

**Zero `dispatch.py` edits:**

    $ grep -in grok extensions/agi/bin/dispatch.py
    (no output; exit 1)

## production_lines — measured honestly (residue R2)

Production paths are `extensions/**` and `.agi/config.json`; test files are
excluded. Because this round re-adds committed bytes, the number is large:

| production path | lines added | how measured |
|---|---:|---|
| `extensions/agi/bin/adapters/grok_bot_adapter.py` | 162 | `wc -l` (new file, untracked) |
| `.agi/config.json` | 12 | `git diff --numstat 18b3044cc -- .agi/config.json` -> `12  0` |
| **total** | **174** | 162 + 12 |

The DT.14 tip reported `12 0 .agi/config.json` + 84 adapter lines = 96, measured
from an uncommitted worktree diff; at the tip the config diff is EMPTY and the
adapter is `162 0` committed. 174 is the honest number against this branch's
actual bytes; test file (246) and probe (68+15) do not count.

## Ceiling checkpoint

Ceiling 40; 2x = 80. **174 > 80.** Per the round's checkpoint rule this node
carries a `rebrief_request`: the overage is inherent to re-adding the committed
adapter (162 lines) plus the carried `g17.14.2` config row (12 lines) — there
is no smaller honest version of "bring the committed bytes forward verbatim".
Requested ceiling: 180 production lines.
