---
id: goal:g1.31.4.2.2
mint_id: 3e5c03e8ba384a599fad40b432a9a44c
type: goal
parents:
  - goal:g1.31.4.2
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.2.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: b8e7919df6533abd
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - verification
  - window
  - meter
title: "G1.31.4.2.2: the window tip is fetched or declared, window tests touch no real process, the P6 meter denominator is measured per model or tagged unmeasured"
town: core
---
# goal:g1.31.4.2.2

## Why this exists
goal:g1.31.4.2: the DG6 half of the council's LANES ruling (goal:g1.31 body, LANES block: verification.py + rotation_alert hook), 3 PASS B3 items from 2 rounds, all open at HEAD ff09c6101:
- `l4-the-window-reply-and-harvest-or-cut-are-captive-steps` #41 #43 (`.agi/sessions/workflows/runs/mur-pb3chunk9of20/verify_l4-the-window-reply-and-harvest-or-cut-are-captive-steps.json`) — window tip never fetched; window test probes the real process.
- `l4-a-meter-you-must-remember-to-read-is-a-coin-flip` #7 (`.agi/sessions/workflows/runs/mur-pb3chunk13of20/verify_l4-a-meter-you-must-remember-to-read-is-a-coin-flip.json`) — P6 denominator trusted, not measured (verdict held at inconclusive_lean_proved:85).

## Target end-state
- `render_window`'s tip is either fetched before `rev-parse origin/<branch>` (verification.py:1489) or printed as the unfetched local ref with its age, and the docstring (verification.py:1449-1451) names which; the hypothesis THOUGHT declares the deviation if unfetched. (#41)
- `test_verification_window.py` touches no real process: no real `os.getppid()` in the fixture lock (:58, :72, :230, :247, :259, :279); `verification.PROC` and `_pid_alive` (verification.py:844) are faked in every row, incl. `test_window_lock_held_when_fixture_lock_exists` (:68). (#43)
- The P6 meter's denominator is established for the RUNNING model, not the single ladder cell `director_context_tokens: 1000000` (`.agi/nodes/.geometry/ladder.md:21`, read at extensions/agi/hooks/rotation_alert.py:1479); a model with no `context_tokens_by_model` row falls back to the ladder window every post already reads, tagged `unmeasured:<model>` ON the meter line next to the fraction, and raises ONE open finding naming the risk (a real window below the ladder value under-reports f, so the post rotates LATE), closed when that model's row lands; the refusal (rotation_alert.py:1486-1496) stays only for window <= 0 -- so "do not quietly assume 1M" holds: the assumption is never silent. (#7)

## Invariants
- A residue is closed by a reviewed round, never by a note.
- The meter never prints a fraction without its window's provenance: over an unmeasured denominator it falls back to the ladder window, tagged `unmeasured:<model>` on the same line; it refuses only at window <= 0 (P6).
- Tests never signal, read /proc of, or walk the parent chain of a real process.

## Falsifier
1. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_verification_window.py extensions/agi/tests/test_rotation_alert.py -q -k "window_tip_fetch or denominator_per_model"` passes with >= 2 tests (exit 5, none collected, today), and both files stay green (test_rotation_alert.py: 58 at the review).
2. Negative: `git grep -n 'os.getppid()' -- extensions/agi/tests/test_verification_window.py` returns zero hits.

## Out of scope
goal:g1.31.4.2.1 (rotate.py harvest/status/copilot, DG5) · goal:g1.31.4.1 · goal:g1.31.4.3 · goal:g1.31.4.4 · goal:g1.31.4.5 · goal:g1.31.4.6 · goal:g1.31.4.7 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6** (council LANES ruling, goal:g1.31: verification.py + rotation_alert hook are DG6).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Restated to match the build, per the council ruling (alive convening, 05:4xZ 09-30; self-perpetuating, all-is-one, alive agree): the fail-closed wording (title, end-state #7, P6 invariant) became fall back + unmeasured tag on the meter line + ONE open finding naming the late-rotation risk. Reason: the rc-4 refusal prints no fraction, so the post never rotates by meter.
<!-- THOUGHT:END -->
