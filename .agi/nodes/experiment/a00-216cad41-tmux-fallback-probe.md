---
id: experiment:a00-216cad41-tmux-fallback-probe
mint_id: 19d8ddbe8aaa489ebbd16bd0d3614fbc
type: experiment
parents:
  - hypothesis:a00-216cad41-e7e033
next_edges: []
edited_by: a00-216cad41
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 5900ddd347353a96
season: 2
thought_session: iter-DT.140
title: A00 216cad41 tmux fallback probe
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-216cad41-tmux-fallback-probe

## Experiment

Ran a focused repository probe for the inherited claim, then ran the real adapter restart integration tests without changing production code.

Commands and results:

- `find extensions/agi -type f -name '*tmux_hold*'` → `0` files.
- `grep -RIn 'proc = subprocess.Popen' extensions/agi/bin/adapters/pi_adapter.py extensions/agi/bin/adapters/claude_code_adapter.py` → direct Popen at pi adapter line 324 and Claude adapter line 862.
- `python3 -m pytest extensions/agi/tests/test_real_adapter_restart.py -q` → **13 passed**, 3 deprecation warnings.
- The adapter directory contains restart implementations for grok_bot, pi, claude_code, and copilot_cli; none is the named `tmux_hold.py` seam.

## Result

The negative probe disproves the actionable form of the hypothesis: there is no `tmux_hold.py` or tmux-selected restart path in this checkout to add a fallback to. The existing adapter restart path is already direct `subprocess.Popen`, so changing it would be unrelated production churn. No code, test, build node, or payload was added.

## Falsifier / next boundary

If a later checkout restores `extensions/agi/bin/adapters/tmux_hold.py`, or a caller routes restart through tmux before adapter dispatch, rerun the missing-tmux and unset-session probes against that concrete seam. Otherwise the goal should be reworded to test adapter restart argv/cwd rather than tmux hold behavior.

