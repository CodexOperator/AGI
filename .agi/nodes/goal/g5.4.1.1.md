---
id: goal:g5.4.1.1
mint_id: b88a9b1ebcefab649dfcea30796b3b1c
type: goal
parents:
  - goal:g5.4.1
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G5.4.1.1
goal_kind: subgoal
origin: goal
scaffold_hash: b88a9b1ebcefab64
season: 3
seeds: []
status: active
tags:
  - goal
  - subgoal
  - season-close
  - residue
  - season-py
title: "G5.4.1.1: Port season.py off Python (box-shaped script); deprecate send-residue tests — clear SM master-merge blockers"
town: core
---
# goal:g5.4.1.1

## Why this exists
goal:g5.4.1 (season-2 close / season3 cut): SM gate review of `core/season3/main` (`4b8f28b5e`) → master returned PASS-with-residue. Two blockers remain before owner-approved master merge: (1) `season.py` `SEND_PY` still points at deleted `bin/send.py`; (2) ~24 live tests still `import send` after send.py moved to `deprecated/bin`.

## OWNER 2026-10-06 (via Owner Comms / Grok Bot), verbatim
> season.py gets ported into the new engine as a script (no Python, the same way `box` replaced send.py), and this is yours to handle through graph paths: a goal node, then the standard loop (council design, DG1/DG2 split, SM gate). Move season.py and its tests and the dead send tests into deprecated/ (move, never git rm), repoint callers and skills (agi-dispatch's `season.py judge`), keep the byte delta minimal, then send it back to SM for a re-gate. Master stays untouched until the owner approves.

## Target end-state
- `extensions/agi/bin/season` (or equivalent new-engine script, no Python) covers the live season verbs the posts need (at least `judge`; status/rollover paths as the design names), with callers + skills repointed (including agi-dispatch's `season.py judge`).
- Old `extensions/agi/bin/season.py`, its tests, and the dead live `import send` tests live under `extensions/agi/deprecated/` (move, never `git rm`); no live test bare-imports `send` against missing `bin/send.py`; no live `SEND_PY` path to deleted `bin/send.py`.
- SM re-gates `core/season3/main` (or the post tip that carries this leaf) and the two blockers are gone or explicitly waived; master still untouched pending owner approval.

## Invariants
- Never `git rm` season.py / send tests — deprecate + move.
- No Python in the new season surface (same contract as `box` vs send.py).
- Byte delta minimal: port what is live, do not rewrite the season domain.
- Standard loop: council design · DG1 goals+hyps · DG2 experiments+verdicts · SM gate · Prime does not build.
- Master merge waits on owner; this leaf only clears the residue.

## Falsifier
1. `test ! -e extensions/agi/bin/season.py && test -e extensions/agi/deprecated/bin/season.py`; new season script exists and `… judge -h` (or documented entry) exits 0; `git grep -n "SEND_PY\|import send" -- extensions/agi/bin extensions/agi/tests` is empty (or only deprecated/); SM re-gate report names both blockers cleared.
2. Negative: `git log --all --diff-filter=D -- extensions/agi/bin/season.py` shows no deletion-without-deprecate; master tip still `6405a03fc` until owner GO.

## Out of scope
goal:g5.4.1 overview/rollover cut (already stood in) · rotate.py KEYGEN_LINE / remaining send imports outside this residue set · eng+post+wrap size bank · waking spend-blocked pi posts · master merge itself

## Agent Notes
Assigned to **sanctuary-master** (place leaves; queue DG1/DG2 / council design). Prime owns the leaf as overall leader; does not implement.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam 04:01Z 10-06 (date -u): minted under g5.4.1 from Owner Comms note quoting owner direction on SM PASS-with-residue. Near miss: implementing the port on the Prime seat — owner said graph paths + standard loop. Spend limit blocks council/pi DGs; SM/DG4 raw-shell still live for routing.
<!-- THOUGHT:END -->
