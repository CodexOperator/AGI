---
id: goal:g15.18
mint_id: 0fb077a0ade04518bb3687ef26d2422e
type: goal
parents:
  - goal:g15
  - build:hooks-cc-session-start.sh
next_edges: []
confidence: 0.7
edited_by: sensei-director
goal_id: G15.18
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: cc7d6a665655c47f
season: 2
seeds:
  - hypothesis:l4-the-rotation-alert-hook-says-what-it-measures
status: active
tags:
  - goal
  - subgoal
  - l4
  - sanctuary-director
thought_session: sensei-director-genI-L1
title: "G15.18: rotation_alert.py says what it measures — UserPromptSubmit in the registration block, the band as a fraction of the threshold, window vs line by name, the seat's own rotate_at"
town: core
---
<!-- BODY:BEGIN -->
**`rotation_alert.py` says what it measures: the registration block names the event the Prime installed (UserPromptSubmit), the band line prints the band as a fraction of the threshold, the fraction line says window where it means window, and the line a seat is measured against is the seat's own `rotate_at`.** Prime, 16:22Z dm (owner-ordered): L4.94's rotation-reminder hook was INSTALLED 16:21Z under UserPromptSubmit; residue to fix in `extensions/agi/hooks/rotation_alert.py`.

## Why this exists

- `goal:g15` is the parent because these are bugfixes on a hook now LIVE for every session on the box, fixed in-loop; measured on this seat's own firing at 16:3xZ: `Approaching rotation (0.2098 of the line). Crossed band 18% of threshold.` — 0.2098 is of the WINDOW (0.446 of the line), and 18 = `int(0.40 × 0.47 × 100)`: the band printed as a fraction of the window under a label that says threshold (the Prime's "band 25% at 0.63 of threshold" is the same formula at the 0.55 band).
- `build:hooks-cc-session-start.sh` is the parent because the hook family under `extensions/agi/hooks/` is the mechanism; `rotation_alert.py` has no build node of its own yet (`level3.py` mints it at the next scan), and its registration block (`:11`, `:41-44`) prescribes `SessionStart` — the event that fires once at ~0 and can never escalate.

## Testable claim (a build order)

(1) The registration block prescribes `UserPromptSubmit` in the exact shape the Prime installed in `~/.claude/settings.json` (read the live file, copy the shape — never edit it). (2) `pct` (`:373`) prints `int(b_frac × 100)` — the band as a fraction of the threshold, as the text says; the fraction line prints both numbers by name: `X of the window = Y of the line`. (3) Verify the "first firing reports the LOWEST crossed band" report on the bytes: the loop (`:325-329`) picks the highest crossed band — if the report was the pct formula, say so in the verdict; if a path exists where a stale state file (`session_id` reuse) suppresses the higher band, fix it. (4) The line: read the seat's own `rotate_at` from its `config:seats` row when the seat is identifiable (AGI_SEAT once `goal:g15.15` lands; today the cwd = the row's `worktree`), fall back to `ladder.director_rotate_at`; this seat's row says 0.4 and the hook measured it against 0.47. (5) Tests in `test_rotation_alert.py`: registration text; pct at 0.63 × threshold prints 55; wording; seat-row threshold on a fixture worktree; the existing suite green.

**Falsifiers:** a firing whose printed band is not `b_frac × 100`; a registration block naming SessionStart; a seat with `rotate_at` 0.4 measured against 0.47. **FILE SCOPE:** `extensions/agi/hooks/rotation_alert.py`, `extensions/agi/tests/test_rotation_alert.py`. EXCLUDED: `~/.claude/settings.json` (the Prime's live install), `rotate.py`, `config:*`. **CEILING:** 1 parent, up to 2 kids. Disjoint from every other L1 round — cut now.

## Agent Notes
PRIME XI SL1#1 verdict line (6), fix-only, STILL OWED (L3 mints the brief): rotation_alert.py reads the seat row from the worktree own seats.md, so a rotate_at edited on season/s2 reaches a seat only at its next merge — read the integration-tree row (main checkout) or document the lag on the node; the row-worktree fallback at :145 is dead code; tests inherit AGI_SEAT from the runner env (env -u in the test); the docstring says SessionStart.
