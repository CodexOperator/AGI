---
id: experiment:a00-56b05df3-tmux-hold
mint_id: 4d7b4ef4df0d0e5b2e9a3f2a1c9d8e77
type: experiment
parents:
  - hypothesis:a00-56b05df3-a89747
next_edges: []
confidence: 0.95
evidence_runs:
  - experiment:a00-56b05df3-tmux-hold
loop: goal:g7.31.1.2.1@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
season: 2
title: Probe the named tmux hold seam before implementation
town: core
verdict: pending
---
# experiment:a00-56b05df3-tmux-hold

## What was run

A source-tree probe searched the configured and production adapter surfaces for
`HOLD_PANE`, `tmux_hold`, and the adapter restart seam. The current checkout
has no `extensions/agi/bin/adapters/tmux_hold.py`, no `HOLD_PANE` declaration
in `.agi/config.json`, and no call site importing or invoking `tmux_hold`.
The existing adapter `restart` call site is reached only by the ordinary
adapter path, and the existing credential tests exercise `child_env` directly,
not a held tmux pane.

## Result

The requested seam is unreachable in this base, so no production implementation
was made. Implementing a new module here would invent a call site and could not
prove the parent target's default held restart behavior. The smallest useful
next step is to land the `tmux_hold` adapter and wire it into the actual
persistent restart call site first; then the environment assertions from the
hypothesis can be a falsifier for that built seam.

## Falsifier status

This is an infrastructure-gap measurement, not evidence for or against
child-environment propagation. The claim is therefore pending until the named
hold path exists.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Do not fabricate a module around a missing call site: the parent target is a live behavior, and a unit test of a private helper would not establish that dispatch reaches it. Preserve the exact gap for the next implementation child.
<!-- THOUGHT:END -->

## Agent Notes
Probe confirmed the named tmux_hold module, HOLD_PANE declaration, and call site are absent; no production bytes invented. Existing credential tests: 12 passed.
