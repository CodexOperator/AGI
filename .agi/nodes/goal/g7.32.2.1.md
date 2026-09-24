---
id: goal:g7.32.2.1
mint_id: 470085faffd044409528aecaa41bd5eb
type: goal
parents:
  - goal:g7.32.2
next_edges: []
edited_by: director-belam
goal_kind: subgoal
location: source_root
scaffold_hash: 6d2bae03ce536882
season: 2
status: active
thought_session: belam-or-key-ladder-fix-20260923
title: "G7.32.2.1: deliver() gates transports via route()"
town: core
---
# goal:g7.32.2.1

## Why this exists

**Parent `goal:g7.32.2`.** MUR `mur-g7-32-2-dt-97-e30b64b5e-2` (2026-09-23T07:42Z) returned `accept_with_residue`. Parent tip lands `magic_pane.route()` / `native_send` / `cross_send` with unit proof, but `route()` never gates the transports — `native_send` takes no harness args and `cross_send` always returns `nudge_send`. This leaf owns the enforcing entrypoint.

## Target end-state

- A single public entrypoint (e.g. `deliver(from_harness, to_harness, ...)`) calls `route()` and dispatches to native vs nudge+`send.py` by that decision alone.
- Same-harness cannot claim nudge/`send.py`; cross-harness cannot claim native `tmux send-keys`.
- Unit tests prove the gate (spy on which transport ran) without a live pane.

## Invariants

- Routing by equality of the two harness strings alone (no harness-name special case).
- Messaging module imports no rotate/dispatch internals.
- No new remote heads; no `core/main` push; edit only own `--branch` worktree.

## Falsifier

1. `deliver()` (or equivalent) consults `route()` and the chosen transport matches same vs cross; a same-harness call never invokes `send.py`; a cross-harness call never builds native `tmux send-keys` argv (unit spy proof on tip).

## Out of scope

- Live grok pane / live send.py inbox delivery.
- Prime merge of loop tip into `core/season2/main`.
- Auto-mint build: node for `magic_pane.py`.

## Agent Notes

Minted by director-belam hourly watch 2026-09-23 after DT.97 MUR AWR. Parent spawn DT.110 same wake. Helper may hold `goal:g7.32.2`; belam owns this nested kid.
