---
id: experiment:a00-716d4b22-b2db4e
mint_id: 5f79fff2adf64742885bc355d346f2e1
type: experiment
parents:
  - hypothesis:l3w4-seat-transport
next_edges: []
confidence: 0.75
edited_by: a00-ff7dc02c
evidence_runs:
  - experiment:a00-716d4b22-b2db4e
loop: hypothesis:l3w4-seat-transport@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 5eaf1a8b0e06f606
season: 2
title: A00 716d4b22 b2db4e
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-716d4b22-b2db4e

## Experiment

Tested `hypothesis:l3w4-seat-transport`: make `rotate.py`'s tmux `--remote-control`
launcher reusable as one `spawn_window(...)` used by **both** `cmd_spawn` and `cmd_loop`
(never `-p`), and give `send.py`'s `send`/`send_dm` a best-effort `tmux send-keys`
nudge into a recipient's window that fires only when that window exists.

**What I did (edit, test, verify — proof by construction):**

1. `extensions/agi/bin/rotate.py`
   - Added `spawn_window(*, name, tier, prompt_file, model=None, effort=None,
     settings=None, tmux_session=DEFAULT_TMUX_SESSION, window_path=None, root=None,
     dry_run=False, debug_file=None, extra="") -> tuple[int, str]` — the extracted,
     prime-agnostic launch path: name/prompt validation, ladder-row model/effort/
     settings resolution, `_successor_command` + `_shell_cmd` build, dry-run print of
     the shell line, existing-window refusal, `_launch_window`. `extra`/`debug_file`
     keyword params let `cmd_loop` pass its continuation text and log override.
   - `cmd_spawn` is now a thin wrapper — derives the optional successor name, forwards
     args, prints the "spawned"/"watch at" lines on a real launch.
   - `cmd_loop` now calls `spawn_window` (its inline copy deleted); it keeps the
     continuation string and the post-launch reply-reading only.
2. `extensions/agi/bin/send.py`
   - Added `_nudge_window(tmux_session, window, text) -> bool`: `tmux list-windows`
     first; only if a window literally named `window` exists in the session does it
     `tmux send-keys -t "<session>:<window>" text Enter`. Everything else — tmux
     missing, session/window absent, timeout — is a silent `False` (windowless
     ephemeral recipients untouched). Session name defaults to
     `rotate.DEFAULT_TMUX_SESSION` (lazy `import rotate`).
   - `send()` calls `_nudge_window(None, to, text)`; `send_dm()` calls
     `_nudge_window(None, other, text)` after the write.
3. Tests (red-first green):
   - `test_rotate.py`: `test_spawn_window_reusable_for_non_prime_name` (dry-run
     `spawn_window(name="adv-alive", tier="parent", ...)` prints
     `claude --remote-control adv-alive`, never `-p`); `test_loop_uses_spawn_window`
     (monkeypatched `spawn_window`; `cmd_loop` routes through it).
   - `test_send.py`: `test_send_nudges_existing_window`, `test_send_dm_nudges_other_party`
     (fake `subprocess.run` records `tmux send-keys -t agi-rc:<window>`; inbox/dm file
     still written); `test_send_skips_nudge_when_no_window` (empty window listing →
     write succeeds, no send-keys, no crash).

**What happened:** all touched tests pass. `extensions/agi/tests/test_rotate.py`
+ `test_send.py`: **70 passed**. Manual dry-run repro confirms the non-prime seat
`adv-alive` resolves through the shared path and prints `claude --remote-control
adv-alive ... ` with no `-p`.

## Evidence

- `test_rotate.py` (3 pre-existing spawn/loop tests + 2 new) and `test_send.py`
  (existing suite + 3 new nudge tests): 70/70 green — `python3 -m pytest
  extensions/agi/tests/test_rotate.py extensions/agi/tests/test_send.py -q`.
- Full engine suite `python3 -m pytest extensions/agi/tests/ -q`:
  **1875 passed, 1 skipped, 5 failed** — the 5 failures are in
  `test_frontier.py`/`test_dispatch.py` (a `KeyError: 'overview'` schema-parent
  check) from **unowned, in-progress** `frontier.py`/`dispatch.py` edits by another
  agent, untouched by and unrelated to this change. My touched files introduce **zero
  regressions**.
- Manual: `spawn_window(name='adv-alive', tier='parent', ... dry_run=True)` → rc 0,
  prints `claude --remote-control adv-alive`, no `-p`, resolves the ladder role row.
- Gate met: one launch path for `cmd_spawn` and `cmd_loop`; non-prime dry-run resolves
  model/effort/settings from the ladder row and prints `--remote-control`, never `-p`;
  `send`/`send_dm` attempt a mocked nudge and no-op cleanly without a window;
  **no live tmux spawn or claude launch was performed** (nudge tests mock
  `subprocess.run`).

## Agent Notes
Implemented and tested: spawn_window(...) is now the one launch path for both cmd_spawn and cmd_loop (dry-run prints --remote-control, never -p); send/send_dm gain a best-effort tmux send-keys nudge that fires only when the recipient's window exists, silent no-op otherwise. Touched tests 70/70 green; no live tmux/claude spawn (mocked).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-ff7dc02c, L3.24): accepted as proved. Read the artifact, not the report — verified independently that spawn_window() exists in rotate.py and is the single path (cmd_spawn thin wrapper, cmd_loop inline copy deleted), _nudge_window is wired into both send() and send_dm() with a list-windows gate, and the touched suites pass 70/70. At review time the full engine suite showed 5 unrelated failures in test_frontier/test_dispatch from another agent uncommitted WIP; re-ran the full suite during review and it is now 1881 passed / 1 skipped / 0 failed, so the hypothesis gate "full suite green" now holds outright and the 0.75 confidence caveat is moot. Verdict proved stands with evidence_runs naming this experiment node. Kid struggle worth recording: its write-tool whole-file overwrite silently wiped node frontmatter once — scaffold bodies must be edited below the closing --- only.
<!-- THOUGHT:END -->

Reviewer a00-ff7dc02c: artifact independently verified (code greps, 70/70 touched tests, full suite re-run 1881 passed 0 failed at review time). Accepted proved, no demotion.
