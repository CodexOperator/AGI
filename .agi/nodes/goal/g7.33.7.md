---
id: goal:g7.33.7
mint_id: 5e24ca245f234d0fafa63c26a640e1fc
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.8
edited_by: director-engine
goal_id: G7.33.7
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 7370177cd7803728
season: 2
seeds:
  - hypothesis:lm-grid-storage-trunk-is-config-declared
  - hypothesis:lm-grid-storage-trunk-code-fix-remaining-literal-sites
  - hypothesis:lm-grid-storage-trunk-migration-for-local-maxxing
  - hypothesis:lm-grid-commit-configured-trunk-lifts-branch-blind-refusal
status: active
tags:
  - local-maxxing
  - engine
title: "G14.14.7: GRID STORAGE TRUNK BY CONFIG -- grid.py ref namespace (today one hardcoded constant, REF_NS = refs/grid at grid.py:84) becomes config-declared so crons.py:548-549 branch-blind refusal is fixed by configuration, not a hardcoded override (owner 01:5xZ 09-21 on goal:g14, supersedes G14.14.6 first item)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.14.7

## Agent Notes
Source. Transcribed from the goal g14.14 body (owner 01:5xZ 09-21 on goal g14, verbatim there: let us have a way to trunk the grid into any arbitrary branch storage trunk via config or template use). Supersedes G14.14.6's first item now that a configured trunk removes the branch-blind refusal; --allow-branch stays as the explicit override for an unconfigured tree.

Commits to. Verified against source, not assumed: grid.py defines ONE constant, REF_NS = refs/grid at grid.py line 84, and nine call sites derive from it (FETCH_SPEC/PUSH_SPEC at lines 102-103, node_ref/legacy/session_ref at 299/303/307, mint_ref at 453, the ready/log lines at 681/683/965) -- already a single resolver in code, just not yet config-driven. crons.py lines 547-549 hardcode the grid_sync command as one literal string, including refs/grid/*:refs/grid/* on line 549, a SECOND spelling of the same namespace outside grid.py entirely. (a) add grid.storage_trunk to .agi/config.json, default value refs/grid so every existing project round-trips unchanged; (b) REF_NS resolves from config.storage_trunk (fallback refs/grid), so all nine existing call sites pick it up for free -- no second resolver added; (c) crons.py's cmd template uses grid.py's own PUSH_SPEC instead of re-hardcoding the literal on line 549; (d) tests: a tree with storage_trunk=refs/grid/t1/ records versions there and refs/grid/ stays untouched; the default tree is byte-identical to today; grid.py versions reads back from the configured trunk.

Invariants. Kids write the fix, parents review, the director batches and orders. The kid pins existing behaviour with the engine suite first (python3 -m pytest extensions/agi/tests -q) before changing REF_NS. Default behaviour (no storage_trunk configured) must be byte-identical to today -- this is the falsifier with the most weight, since refs/grid/* already holds real history that must keep resolving.

Falsifiers. The round is falsified if a tree with no storage_trunk configured resolves anything other than refs/grid (a silent behavior change for every existing project), or if crons.py still hardcodes a namespace literal anywhere after the fix (the second-spelling gap reopened), or if the fix breaks the engine suite (demote, never merge).

Done when. The hypothesis lands a verdict against its own falsifiers: default tree byte-identical, a configured trunk isolates its versions, crons.py has one spelling, engine suite green. Migration for this box (storage_trunk=refs/grid/local-maxxing/ then grid.py migrate-refs or a documented re-seed) happens AFTER the round lands, not as part of it.

First chunk, minted next: hypothesis:lm-grid-storage-trunk-is-config-declared, the whole round (a) through (d) as one testable claim, per the goal g14.14.7 body describing ONE round rather than independent lettered items.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
renumber g14.14.7 -> g7.33.7 to align the town with core's 09-21 goal re-arrangement (owner GO on core; owner 09-23 asked the two teams be aligned): the parent g14.14 became g7.33 on core; mint_id preserved; Prime core-sync 09-23
<!-- THOUGHT:END -->
