---
id: goal:g1.31.4.2.1.3
mint_id: 227ea9be7e8a4acda0a2009fcc8ed425
type: goal
parents:
  - goal:g1.31.4.2.1
next_edges: []
confidence: 0.7
edited_by: director-general-5
goal_id: G1.31.4.2.1.3
goal_kind: subgoal
origin: goals-doc
model: stealth/space-bunny-alpha
role: director
scaffold_hash: 80d0dd96af49240c
season: 2
seeds: []
status: active
tags:
  - engine
  - meter
title: "G1.31.4.2.1.3: every transcript reader (parse_usage_from_cc_transcript, the log_path reads) is UNKNOWN under an unreadable or looping path, through ONE shared guard"
town: core
---
# goal:g1.31.4.2.1.3

## Why this exists
parent goal:g1.31.4.2.1 — the same mur `mur-posts-director-general-5-4` (pin4). Leaf B, verbatim (the line numbers are MUR-TIME lines, not lines at the current tip: rotate.py is 23,338 lines now and `parse_usage_from_cc_transcript` is defined at `rotate.py:587`; find a call site by name, not by number): the OTHER transcript readers are unguarded — `parse_usage_from_cc_transcript` at `rotate.py:12673` and `:15332`, plus reads on `log_path` at `:1465` / `:1474`. The leaf fixed ONE reader (the meter pin); these are the same defect at the sibling call sites, and the verifier ruled them outside the leaf's claim so they need their own row.

## Target end-state
No caller of `parse_usage_from_cc_transcript` (and no read of `log_path`) can raise on an unreadable or looping path: each such read is wrapped, reports UNKNOWN for that reader, and leaves the rest of the status output intact.

## Invariants
- One guard shape for all transcript readers — a helper, not four inline try blocks (the mur's config-max note: one source per rule).
- A `RuntimeError` from `Path.resolve()` on a symlink loop is caught wherever an `OSError` is (MEASURED py3.12.3: a real `a->b->a` loop raises `RuntimeError('Symlink loop')`, NOT `OSError`).

## Falsifier
1. For each of the four named sites, a test drives it against (a) a mode-000 transcript dir and (b) a real symlink loop, and asserts no raise + UNKNOWN printed; the suite is green.
2. Negative: delete the shared guard — exactly the tests naming those sites red, and the pin-leaf tests stay green (name the seam per test, the mur-3 lesson).

## Out of scope
goal:g1.31.4.2.1.2 (leaf A, `find_pin_log`'s `is_dir()`) · granting any uid access to another seat's transcripts: DECLINED by belam 18:14, the CLI half is the whole remedy.

## Agent Notes
Assigned to **director-general-5**.
