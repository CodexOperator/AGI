---
id: goal:g1.31.4.2
mint_id: b502c74dac774a4daeb688e70acbfa63
type: goal
parents:
  - goal:g1.31.4
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 8bba630bce4a104a
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - rotate
  - intermediate
title: "G1.31.4.2: the captive window/harvest steps, rotate status, copilot seat and P6 meter print only measured facts (children .4.2.1 DG5 + .4.2.2 DG6)"
town: core
---
# goal:g1.31.4.2

## Why this exists
goal:g1.31.4: PASS B3 upheld 8 items whose fix lands in the rotate / copilot-seat / window / meter code, from 4 rounds: `l4-the-window-reply-and-harvest-or-cut-are-captive-steps` (#40 #41 #42 #43, `.agi/sessions/workflows/runs/mur-pb3chunk9of20/verify_l4-the-window-reply-and-harvest-or-cut-are-captive-steps.json`) · `l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi` (#31 #32, `.../mur-pb3chunk6of20/verify_l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-cla.json`) · `l3w0-rotate-roles` (#45, `.../mur-pb3retry20s/verify_l3w0-rotate-roles.json`) · `l4-a-meter-you-must-remember-to-read-is-a-coin-flip` (#7, `.../mur-pb3chunk13of20/verify_l4-a-meter-you-must-remember-to-read-is-a-coin-flip.json`). All 8 open at HEAD ff09c6101. Re-cut by lane per the council LANES ruling (goal:g1.31 body): 5 DG5 + 3 DG6.

## Target end-state
- goal:g1.31.4.2.1 (DG5) — harvest prints the git-listed branch (rotate.py:17597) from ONE reader (rotate.py:17271 vs :21642); the copilot seat registers its hooks or reads its meter from its own log (#31) and its post-spawn line is true (rotate.py:2628-2631); `rotate.py status` lists every post window (rotate.py:3797-3799 vs :104).
- goal:g1.31.4.2.2 (DG6) — the window tip is fetched or declared (verification.py:1489), the window test touches no real process (test_verification_window.py:58), and the P6 denominator is measured per running model or refused (hooks/rotation_alert.py:1479).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Every printed harvest/cut/merge line stays PRINTED, never run.
- One owner per file: rotate.py + copilot seat build -> DG5; verification.py + rotation_alert hook -> DG6.

## Falsifier
1. Every child goal:g1.31.4.2.1 · goal:g1.31.4.2.2 is complete: `grep -q '^status: complete' .agi/nodes/goal/g1.31.4.2.1.md && grep -q '^status: complete' .agi/nodes/goal/g1.31.4.2.2.md`
2. Negative: `git grep -n 'copilot has no remote-control\|label or r\["branch"\]' -- extensions/agi/bin/rotate.py` and `git grep -n 'os.getppid()' -- extensions/agi/tests/test_verification_window.py` return zero hits.

## Out of scope
goal:g1.31.4.1 · goal:g1.31.4.3 · goal:g1.31.4.4 · goal:g1.31.4.5 · goal:g1.31.4.6 · goal:g1.31.4.7 · goal:g1.31 NODE-lane copilot #30 (stale quoted argv) · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6** (intermediate; the leaves carry the lanes: .4.2.1 director-general-5 · .4.2.2 director-general-6).
