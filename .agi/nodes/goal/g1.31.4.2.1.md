---
id: goal:g1.31.4.2.1
mint_id: af8e530e1bae43769ee69665a8fc2922
type: goal
parents:
  - goal:g1.31.4.2
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.2.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: e55a06406729a3bc
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - rotate
  - copilot
  - harvest
title: "G1.31.4.2.1: harvest prints the git-listed branch from one reader, copilot hooks + spawn line are true, rotate status lists every post window"
town: core
---
# goal:g1.31.4.2.1

## Why this exists
goal:g1.31.4.2: the DG5 half (rotate/spawn code) of the council's LANES ruling (goal:g1.31 body, LANES block), 5 PASS B3 items from 3 rounds, all open at HEAD ff09c6101:
- `l4-the-window-reply-and-harvest-or-cut-are-captive-steps` #40 #42 (`.agi/sessions/workflows/runs/mur-pb3chunk9of20/verify_l4-the-window-reply-and-harvest-or-cut-are-captive-steps.json`) — harvest line takes the LLM label; duplicate harvest reader.
- `l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi` #31 #32 (`.agi/sessions/workflows/runs/mur-pb3chunk6of20/verify_l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-cla.json`) — hooks parity unmet; false post-spawn message.
- `l3w0-rotate-roles` #45 (`.agi/sessions/workflows/runs/mur-pb3retry20s/verify_l3w0-rotate-roles.json`) — status misses belam-* windows.

## Target end-state
- `first-decision`'s harvest answer prints `git merge --no-ff <r["branch"]>`, the name from `git branch --list`; a label that differs from the row's branch, or an answer count != row count, is refused by name — no `branch = label or r["branch"]` (rotate.py:17597), no silent `zip(rows, answers)` truncation (rotate.py:17592). (#40)
- ONE harvest-row reader: `first-decision` (`_fd_rounds` rotate.py:17471, `_fd_seat_agent_ids` :17409, worktree convention :17402) reuses `cmd_harvest_table` (rotate.py:21642, convention :22100) or both share one helper; the stale "harvest-table ... is NOT in this tree" comment (rotate.py:17271) is gone. (#42)
- The copilot-cli post-spawn line (rotate.py:2628-2631) names the shipped `--remote` mode (extensions/agi/templates/harness/copilot-cli.toml:23 `const = "--remote"`) instead of "(copilot has no remote-control mode)"; a committed test pins the string. (#32)
- Copilot hooks parity (hypothesis conjunct 5): the SessionStart map injection and the UserPromptSubmit meter line are registered in copilot's documented `hooks` config (`sessionStart`, `userPromptSubmitted`) by the copilot seat build (templates/harness/copilot-cli.toml · bin/adapters/copilot_cli_adapter.py) and proven on a fixture — or, on the claim's fallback branch, the meter is read from the CLI's own session log / `--usage-output-file`; today neither is wired (`git grep -n 'usage-output-file\|userPromptSubmitted' -- extensions/` = 0 hits; experiment a00-440ab5ac-e53139.md:162-164 "NOT wired"). (#31)
- `rotate.py status` lists the windows of the post session (`DEFAULT_TMUX_SESSION = "agi-rc"`, rotate.py:104) — incl. every belam-* window — not only sessions named `agi-master*`/`belam*` (filter rotate.py:3797-3799; docstring :3636, module doc :37-38); a committed test fakes tmux and covers the branch. (#45)

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Every harvest/cut line stays PRINTED, never run (test_rotate_first_decision.py:255 stays green).
- Tests fake tmux and the copilot binary; none touches a live pane or spends a premium turn.

## Falsifier
1. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q -k "harvest_label_mismatch or copilot_hooks_registered or status_lists_windows_in_post_session"` passes with >= 3 tests (exit 5, none collected, today), and `test_rotate_first_decision.py` stays green.
2. Negative: `git grep -n 'copilot has no remote-control\|label or r\["branch"\]\|is NOT in this tree' -- extensions/agi/bin/rotate.py` returns zero hits.

## Out of scope
goal:g1.31.4.2.2 (verification.py window + P6 meter, DG6) · goal:g1.31.4.1 · goal:g1.31.4.3 · goal:g1.31.4.4 · goal:g1.31.4.5 · goal:g1.31.4.6 · goal:g1.31.4.7 · copilot #30 (stale quoted argv, NODE lane) · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-5** (council LANES ruling, goal:g1.31: DG5 = rotate/heal/spawn/dispatch).
