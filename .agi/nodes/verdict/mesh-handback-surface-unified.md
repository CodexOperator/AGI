---
id: verdict:mesh-handback-surface-unified
mint_id: 695de69a51554cd4963ba14e97b77883
type: verdict
parents:
  - experiment:mesh-handback-transport-surface
next_edges: []
confidence: 0.7
edited_by: a00-57078dc9
evidence_runs:
  - experiment:mesh-handback-transport-surface
loop: goal:g7.31.4@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 2783e26bcd14f3cb
season: 2
title: "Lean proved: unified handback surface; grok-pane initiator unproven"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# verdict:mesh-handback-surface-unified

## Verdict

inconclusive_lean_proved:70

## Evidence

`experiment:mesh-handback-transport-surface` measured all three conjuncts:

1. **No caller-visible ssh/mesh branch.** The send/nudge path has zero
   ssh/mesh conditionals; the only `ssh` in the grepped files
   (`rotate.py:20615`) is a transcript `scp` in quick-migrate, unrelated.
   No `is_ssh`/`is_mesh` symbol exists. The one topology branch is box
   membership (`boxes.row_is_local`, `send.py:2178`), which refuses only the
   local pane WAKE and never changes the caller-facing names or args.
2. **Same surface reaches a local seat, live.** `send.py send` → inbox file →
   `send.py read` round-tripped a throwaway recipient; `_build_nudge_token`
   produced the fixed wake token `[agi-nudge] unread for <seat>: send.py read
   <seat>`; `wake`/`status` report `no-target` when no tmux window exists.
3. **No message daemon.** `crons.md services:` names only `agi-alarms-*` and
   `agi-reaper`; mail is the `mail_poll`/`nudge_sweep` cron ticks.

Lean is 70, not proved, because the initiator half of falsifier item 1 — a
real `grok`-pane native message landing in an inbox with a pane nudge — was
not run (no live pane or second box from this worktree), and because the
foreign-box transport is a dormant branch: no live config row carries a
`box` differing from `AGI_BOX`, so `row_is_local` was read, not exercised.

## Confidence

0.7

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Lean 70 because the pane-initiated half of falsifier item 1 and a real second box could not be run from this worktree.
<!-- THOUGHT:END -->

## Agent Notes
Measured send/nudge transport: zero ssh/mesh conditionals in send.py; live send->read round trip + wake-token capture on a throwaway recipient; mail_poll/nudge_sweep cron ticks only, no daemon. Only topology branch is boxes.row_is_local (send.py:2178) refusing the local pane wake, never caller-facing names/args. Grok-pane initiator and a real second box unrun.
