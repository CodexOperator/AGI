---
id: hypothesis:l3w4-seat-transport
mint_id: e3f4a86b0fa24391a9c92c2f89828ffc
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-III
scaffold_hash: 647fe42ef1218764
season: 2
testable_claim: rotate.py's cmd_spawn and cmd_loop both route through one new spawn_window(...) function that launches any named seat via `claude --remote-control` in tmux (never `-p`), and send.py's send/send_dm call `tmux send-keys` to nudge a recipient's tmux window when it exists while leaving windowless (ephemeral) recipients unchanged.
thought_session: L3.21
title: Spawn and nudge perpetual seats
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-seat-transport

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAIM
`rotate.py`'s tmux `--remote-control` launcher generalises from a prime-only primitive into one reusable `spawn_window(...)` any named seat calls; `send.py`'s `send`/`send_dm` gain a best-effort `tmux send-keys` nudge into the recipient's window, firing only when that window exists, leaving windowless (ephemeral) recipients untouched.

WHY
Owner (2): "Belam, quorum, and owner director-kid liaison all have remote sessions just in case." Owner (1): the four "are live in perpetuity," and Belam "spawns advisors who keep acting on his behalf" — addressable, not one bounded turn. Director gloss, same section: "perpetual seats cannot run as `claude -p` (one bounded turn, unaddressable)... `send.py send --to <seat>` writes the inbox and types a one-line nudge into the seat's tmux window... Ephemeral parents/kids stay fire-and-forget."

FILES
extensions/agi/bin/rotate.py :: cmd_spawn (L782), cmd_loop (L864), _successor_command (L620), _build_claude_command (L601), _shell_cmd (L751), _launch_window (L763), load_role (L443), DEFAULT_TMUX_SESSION
extensions/agi/bin/send.py :: send (L308), send_dm (L399), send_room (L410, untouched), _detect_sender (L111)
extensions/agi/bin/adapters/claude_code_adapter.py :: build_command (L505) — always `-p` (L562)
extensions/agi/bin/adapters/pi_adapter.py :: docstring (L18) — pi stays non-interactive
extensions/agi/briefs/prime-director-successor.md — only per-role prompt file today; content is a neighbour brief's
extensions/agi/tests/test_rotate.py :: test_spawn_dry_run, test_spawn_refuses_existing_window
extensions/agi/tests/test_send.py :: project fixture (L26)

DESIGN
1. Extract `cmd_spawn`'s body (name validation, tmux_session/prompt_file, `load_role`, `_successor_command`, `_shell_cmd`, dry-run/existing-window check, `_launch_window`) into `spawn_window(*, name, tier, prompt_file, model=None, effort=None, settings=None, tmux_session=DEFAULT_TMUX_SESSION, window_path=None, root=None, dry_run=False) -> tuple[int, str]`. `cmd_spawn` becomes a thin wrapper; `cmd_loop` calls it too instead of its own inline copy — `name`/`tier` were already parameters, nothing prime-specific to strip.
2. `send.py`: `_nudge_window(tmux_session, window, text) -> bool` runs `tmux send-keys -t f"{tmux_session}:{window}" text Enter` via `subprocess.run(capture_output=True, timeout=5)`, catching `FileNotFoundError`/`TimeoutExpired` like `_launch_window`. `DEFAULT_TMUX_SESSION` via a local `import rotate` (mirrors rotate.py's own local `import brief`). Called from `send()`/`send_dm()` after the write, `window = to` / `other`; silent False when the window is absent.

TESTS (red-first)
- test_spawn_window_reusable_for_non_prime_name: `spawn_window(name="adv-alive", tier="parent", prompt_file=<tmp>, dry_run=True)` prints `claude --remote-control adv-alive`, never `-p`.
- test_loop_uses_spawn_window: monkeypatch `rotate.spawn_window`; `cmd_loop` calls it.
- test_send_nudges_existing_window / test_send_dm_nudges_other_party: fake `subprocess.run` records `tmux send-keys -t agi-rc:<window>`; file still written.
- test_send_skips_nudge_when_no_window: fake `list-windows` empty; write succeeds, no send-keys attempted, no crash.

GATE
`spawn_window` is the one launch path for `cmd_spawn` and `cmd_loop`; a dry-run for a non-prime name/tier resolves model/effort/settings from the ladder row and prints `--remote-control`, never `-p`; `send.py send --to <name>` and plain `send.py send <name>` attempt a mocked nudge, no-op cleanly with no window; full suite green; no live tmux or claude spawn.

NOT IN SCOPE
The seat registry (`l3w4-seat-registry`); per-seat prompt bodies; busy-pane detection; the pi harness (fire-and-forget); who reaches the prime, `send_dm`'s gap (`l3w4-quorum-reviews`).

SOURCE
`.agi/context/l3-command-ladder-brief.md`, final section "Owner text 2026-09-07 ... perpetual seats, the quorum as reviewer, the owner liaison" — owner verbatim (1) and (2), and the "Director gloss ... Transport change required" paragraph.
