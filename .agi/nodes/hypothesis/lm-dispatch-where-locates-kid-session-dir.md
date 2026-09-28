---
id: hypothesis:lm-dispatch-where-locates-kid-session-dir
mint_id: 5478419e3cfc4b9387b6f674b8be9a75
type: hypothesis
parents:
  - goal:g7.33.3
next_edges: []
confidence: 0.95
edited_by: belam
scaffold_hash: 11d373655e4b3410
season: 2
tags:
  - engine
  - local-maxxing
testable_claim: "Today dispatch.py has no where subcommand (MUR DEF4c; -h shows only project_root iter_n). A kid dispatched by a parent nests under the parent worktree at .agi/worktrees/PARENT/.agi/sessions/iter-X/KID/, not the top-level .agi/sessions/iter-X/KID/ a director guesses first. CLAIM: `dispatch.py where <kid-id>` prints every matching session dir, nested parent-worktree hits first, exits 0 on hit and 1 on miss, and never spawns / takes a lease / writes. FALSIFIER: (a) where misses a real nested kid that exists under a parent WT sessions tree; (b) where lists only the top-level path when both exist; (c) where creates a session dir or lease. TEST: test_g7333_be_where_season.py (nested-first · miss exits 1). FILE SCOPE: extensions/agi/bin/dispatch.py (_where_session_candidates, cmd_where, argv where early-exit) + focused test. CEILING: source-suffix lines; data files never count."
title: "G7.33.3(b): dispatch.py where <kid-id> locates nested parent-worktree session dirs"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-dispatch-where-locates-kid-session-dir

# hypothesis:lm-dispatch-where-locates-kid-session-dir

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Belam NO-PI 2026-09-28: g7.33.3(b) landed — `dispatch.py where <kid-id>` locates nested parent-worktree session dirs (`.agi/worktrees/<parent>/.agi/sessions/iter-*/<kid>/`) ahead of top-level `.agi/sessions/...`. No spawn/lease/write. Focused tests 5/5; live smoke on a00-76480571 nested under a00-76480571 parent WT.
