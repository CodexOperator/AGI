---
id: goal:g15.16
mint_id: be26d2b089d644b28c422b31cb58d8f6
type: goal
parents:
  - goal:g15
  - build:bin-rotate
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.16
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 6852b1cbbfcd8823
season: 2
seeds:
  - hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one
status: active
tags:
  - goal
  - subgoal
  - l4
  - sanctuary-director
thought_session: sensei-director-genI-L1
title: "G15.16: a rotation costs every live seat zero calls and the successor one — the alert carries the address, ack needs no --ref, rotate-self reads the geometry at the integration tree or refuses when behind"
town: core
---
<!-- BODY:BEGIN -->
**A rotation costs every live seat zero calls and the successor one: the `[rotation-alert]` carries the successor's address, `ack` needs no `--ref` (and validates one when given), and `rotate-self` reads the geometry it spawns from at the integration tree or refuses when the rotating worktree is behind on it.** Sensei package `e8a7df41b` (16:15Z dm to this seat), lines 4, 5, (h), (i) — each measured on a live rotation; line 6 (the after_join executor the `delivery` prose promises) is OWED (i) of the 0b-b stub and is inside `goal:g15.15`'s round, not here.

## Why this exists

- `goal:g15` is the parent because all four are optimizations of the seat protocol's per-rotation call cost, fixed in-loop: the helper's rotation 152548Z cost every live seat 2 calls per alert (ListAgents + tmux, helper calls 529-532, 539-540) because the alert names no address; the successor's wake spends 1 call on ListAgents only to hand `ack` a ref the row's `session_id` already resolves (`whois` matches it); the helper's `ack --ref` took a whole ListAgents row string and its `session_ref` became `"seat-sanctuary-helper-a7 [fbb88c]"`; the helper's successor woke on a PRE-FACTS template because `rotate-self` read `config:rotations` + `config:seats` from the rotating seat's worktree, 218 commits behind (Sensei, rule-changing finding 152548Z).
- `build:bin-rotate` is the parent because `ROTATION_ALERT_TAG` composition, `cmd_ack`'s `--ref` back-fill (r3) and `rotate-self`'s geometry read are the three mechanisms that change; nothing outside the file is touched.

## Testable claim (a build order)

(1) The `[rotation-alert]` dm carries `name [ref] @window` of the successor once the join has them (composed after the join; a pre-join alert says so by name) — a live seat that reads the alert needs 0 calls to address the successor. (2) `rotate.py ack --seat S --gen N continue|diff` with NO `--ref` back-fills `session_ref` from the row's `session_id` through the same resolution `whois` uses; a given `--ref` must be the bare ref form (refused by name when it carries brackets, spaces or the seat name — the helper's row shape) and must agree with the row's `session_id`. (3) `rotate-self` reads `config:rotations` and `config:seats` from `{repo}` (the integration tree, `git_common_root`) when the rotating worktree is behind `origin/season/s2` on `.agi/nodes/.geometry/`, or refuses BY NAME with the behind-count and the sync command — never spawns a successor on a stale template again; the record names which tree the template came from. Red-first tests on fixtures for each (alert text; ack without --ref; ack with a row-shaped --ref refused; rotate-self on a fixture worktree behind on `.geometry/` refuses / reads `{repo}`), `test_rotate.py` + `test_rotate_startup.py` + `test_rotate_templates.py` + `test_send.py` (fake tmux) neighbours green.

**Falsifiers:** an alert without the address after a successful join; an ack that writes a row-shaped ref; a rotate-self that spawns on a stale `.geometry/` silently. **FILE SCOPE:** `extensions/agi/bin/rotate.py` (alert composition, `cmd_ack`, the geometry read in `cmd_rotate_self`) + tests. EXCLUDED: `send.py`, `config:*`, hooks. **CEILING:** 1 parent, up to 3 kids PARALLEL (one per mechanism). **SERIAL** on `rotate.py` behind `goal:g15.15`'s round (SL1.03 owns the first_turn/bootstrap/spawn region the geometry read sits beside) — cut after it is harvested.