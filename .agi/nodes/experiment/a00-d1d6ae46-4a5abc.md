---
id: experiment:a00-d1d6ae46-4a5abc
mint_id: 52e05511baba4e018eb9a51e1ed7ef93
type: experiment
parents:
  - hypothesis:l3w4-hierarchy-one-source
next_edges: []
confidence: 0.85
edited_by: a00-d2e2165f
evidence_runs:
  - experiment:a00-d1d6ae46-4a5abc
loop: hypothesis:l3w4-hierarchy-one-source@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 672785ed71f3388f
season: 2
thought_session: SD.04
title: delete-duplicate-table zeroes class 6; render is frontmatter-only
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-d1d6ae46-4a5abc

## Experiment

Empirically tested the hypothesis's deletion leg — "duplicate prose tables in both
node bodies DELETED rather than re-derived" — without touching the live tree.
Built a throwaway mirror of the graph root in /tmp/hiroot
(copied `nodes/.geometry/{ladder,seats}.md`, the `sessions/` pin dir, and
`config.json`), then drove the already-built `hierarchy.py --check --root` and
`render --root` against it. Three measurements:

**M1 — baseline mirrors the live drift.** `hierarchy.py --check --root /tmp/hiroot`
→ exit 1, **10 violations**: 6 `orphan_pin` (belam-S1-L3-IX, belam-S1-L3-X,
dir-g1, dir-g15, dir-g16, liaison — that last a live owner-ordered seat with no
row, which only sanctuary-master may add) + 4 `body_table` (the duplicate
"Roles table (command ladder)" rows whose display labels `director (perpetual)`,
`liaison (owner)`, `parent (advisors)` disagree with the frontmatter `role`
values `director`, `liaison`, `parent`). Identical to the 10 violations
e66e7919 measured live — the mirror is faithful.

**M2 — deleting the duplicate table zeroes class 6 and nothing else.** Removed
only that prose table from the throwaway `ladder.md` BODY, replacing it with
one line pointing at `hierarchy.py render`. Re-ran `--check` → `body_table`
dropped **4 → 0**; the 6 genuine orphan pins were unchanged. The prose-vs-
declaration drift class the hypothesis says must be deleted is, in fact,
zeroed by the deletion, and the checker stays live on the real remaining
drift.

**M3 — the checker does not go permanently silent; render stays body-immune.**
Re-seeded a bogus `| 9 | bogus-role | … |` row into the throwaway ladder body:
`--check` fired it again (7 violations), and `hierarchy.py render --root`
printed the bogus role **0 times** (grep -c = 0) — the renderer reads
frontmatter only. Deleting the table is not masking; render never read it.

## Evidence

M1 exit=1, 10 violations (6 orphan_pin + 4 body_table, exact lines above).

M2 after deletion: exit=1, **6 violations, all orphan_pin**, zero body_table:
```
orphan_pin: belam-S1-L3-IX.meter has no seat row in config:seats
orphan_pin: belam-S1-L3-X.meter has no seat row in config:seats
orphan_pin: dir-g1.meter has no seat row in config:seats
orphan_pin: dir-g15.meter has no seat row in config:seats
orphan_pin: dir-g16.meter has no seat row in config:seats
orphan_pin: liaison.meter has no seat row in config:seats
hierarchy.py --check: 6 violation(s).
```

M3 after re-seeding a bad body row: exit=1, 7 violations, the bogus row flagged
as `body_table: roles prose row ['9', 'bogus-role', …]`; `render` grep for
`bogus-role` = 0.

Run on 2026-09-08 in a /tmp mirror; the LIVE tree was not modified (the actual
deletion on `ladder.md`/`seats.md` bodies and the `--check` wiring into
`commands.md` remain sanctuary-master/continue-pass work, and `liaison` still
needs a row only sanctuary-master may add).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SD.04: mirror methodology sound and evidence lines reproducible; deletion leg properly isolated. Note its "no write.py verb exists" claim was later falsified by a00-260a392b, which built body_patch — the mirror deferral was over-cautious, not wrong.
<!-- THOUGHT:END -->

## Agent Notes
Deletion leg evidenced on a /tmp mirror: removing the duplicate Roles table zeroed class-6 body_table 4->0, left 6 genuine orphan pins, re-seeded bad row still fires, render reads frontmatter only (bogus role appears 0x).