---
id: goal:g7.31.1.2
mint_id: fb589b44ed9f46eaa6c0b4c4323bba0f
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.9
edited_by: director-belam
goal_id: G7.31.1.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 67eb4b9e47d1ff69
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - adapter
  - tmux
  - pane
thought_session: magic-pane-2026-09-21
title: "G7.31.1.2: Durable named tmux pane restart/reattach hold"
town: core
---
# goal:g7.31.1.2

## Why this exists

**Parent `goal:g7.31.1`.** Falsifiers on the parent were multi-headed. This leaf owns **durable named tmux pane hold** — kill the seat process; `restart` (or persistent-dispatch restart) reattaches to the **same** tmux pane name the seat keeps.

## Target end-state

- Adapter `restart` (or documented true impossibility) re-attaches to the same named tmux pane.
- Pane name is stable across adapter restarts; seat occupation is visible independently of process pid churn.
- Precursor to magic pane — durable hold first; magic UX later.

## Invariants

- One named pane per seat; no anonymous fire-and-forget for persistent grok seats.
- Restart goes through the same adapter/template seam as first spawn (`goal:g7.27` / `goal:g7.28`).
- Measured CLI argv shape is OOS here (`goal:g7.31.1.1`).
- Does not special-case `grok` inside `dispatch.py` / `rotate.py`.

## Falsifier

1. Kill the seat process; `restart` (or persistent-dispatch restart) reattaches to the **same** tmux pane name; `tmux list-panes` / capture shows the seat still there.

PROVISIONAL and UNMEASURED, ACT 2c (council: alive [decision] 11-06 19:49:54Z (A)(3) and 11-09 10:56:03Z; none of this is ever read as a pass of 1, which only the live kill + reattach run decides, on the owner's or belam's GO):
- grok-bot's resume proof is `session_id` (grok-bot.toml `[session] resume_proof`): heal resumes when the row carries an id, and logs 'resume proof PROVISIONAL (session_id present; UNMEASURED)' on every use.
- The session store's path is UNREAD: the help names the grok home `~/.grok` (doc:grok-bot-help-measured :175) and that sessions live 'under the target session directory' (:140-141), but no store was seen (belam's `~/.grok` read empty, 11-09). grok-bot.toml declares no `[session] store`, so heal's pre-launch read is UNREAD on every resume and the resume is launched.
- heal reads as uid `agi-reaper` (crons.md, `heal.py watch`), not the seat's uid: a store under the seat's home may be unreadable to it, and that also reads UNREAD, never 'absent'.
- A failed -r that keeps its process up (so the join reads the dead id back from its own argv) is invisible to the join alone; the first live run measures it once.
- A failed -r (2c-3, council 3/3 11:22Z-11:25Z 11-09, DG1's pick (b)): heal reads the pane join at the END of a 30 s window after its -r launch. `absent` or `no-pane` (the common exit: the launch-file bash ends with the harness and the window closes; the repo sets no remain-on-exit, the live tmux server's setting NOT read) = FAILED: the id leaves the row, the row keeps its dead pid (heal scans only pid > 0), NO in-pass fresh launch; the next heal cycle's ordinary spawn is the fresh launch (2b's new uuid, read back by the after-join pass). `ambiguous`, or a different pid at the end than at the launch = the id kept, pid EMPTY, nothing launched. On `absent` the failed window is still OPEN, so the row's window is written EMPTY (2c-4, R6): with its @id the next pass's (1b) would read the seat alive, a silent stall; empty, the next pass reaches _recover_seat and its same-name refusal, loud each pass, until the window closes (no window is killed). LIMIT (aio 11:46:05Z): that refusal holds for a NON-chain seat (it respawns under its own name); a chain seat (role prime_director) respawns as base-<gen+1>, a NEW name, so it would pass the refusal and open a SECOND window beside the failed one. Latent today: the one prime_director row is belam's, on claude-code, so the session_id path never reaches it. So a chain seat KEEPS its @id on an absent read (2c-5, sp's NIT): fail-closed, a stall, never a second window; its FAILED line says heal reads it alive until that window closes (alive's addition), so the stall is named once. Before any chain seat runs on a session_id-proof harness, it needs its own open-window check. The same-name refusal logs its own line each pass (2c-5, alive's NIT 1). NAMED, not changed (alive's NIT 2): a failed -r reads respawned False, so the pass's one launch slot stays unspent although a launch happened; a second seat can launch in the same pass. The dead id and what the join read are in heal's crash-recovery record, `resume_failed`; from the seat name: `python3 extensions/agi/bin/heal.py resume-failed --seat <seat>` (2c-5; `rotate.py status --record` skips crash-recovery records, so it never shows one). A refusal pass that rewrites the deduped detected record carries the prior `resume_failed` over (2c-5); the heal log's FAILED line keeps the id too. A row cell for it is one banked line for the owner's batch (council 10:56:03Z (C)). Which of no-pane / absent a live failed -r gives is read by the first live run.
- NOT YET (alive's NIT 1, at the touch that declares a `[session] store`): `~` in a store path expands in the home of heal's uid, not the seat's; resolve it against the seat's home then, with a row.

## Out of scope

- Measuring CLI flags / retiring stub argv (`goal:g7.31.1.1`).
- Magic-pane product chrome.
- Pane ↔ post/pin (`goal:g7.31.2`).

## Agent Notes

Split from `goal:g7.31.1` by director-belam (point) 2026-09-21 ET — multi-headed falsifier. Launch pi parent; diagram-max; batch-max; merge-up to Belam; blockers to owner only via director-belam.

**Related:** `goal:g7.28`, `goal:g7.31.1.1`.
