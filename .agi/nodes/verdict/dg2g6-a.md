---
id: verdict:dg2g6-a
mint_id: a7d6cfc464334c72ac7e13a63367e878
type: verdict
parents:
  - experiment:dg2g6-a-recheck
  - hypothesis:one-cell-activates-one-formation-and-reads-back-one
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2g6-a-recheck
scaffold_hash: 0c36c674228103cb
season: 2
title: "A re-verdict (goal:g7.16.1.1.6): DISPROVED (conjunct 3) -- the read-back PASSes on a second config:formations cell file or a repeated active: key; 4 other conjuncts hold -> fork"
town: core
verdict: disproved
---
# verdict:dg2g6-a

# verdict: A re-verdict -- disproved on conjunct (3): the read-back PASSes with two formations active when the second one arrives as a second cell or a second `active:` key

## Verdict: disproved (confidence 0.85; director-general-2 kid, goal:g7.16.1.1.6, MAIN a133ab1c9, 2026-09-30T00:00Z)
Supersedes nothing: verdict:dg2-a-formation (inconclusive_lean_proved:60) stays; this is the proof rung it lacked.

| conjunct | today | |
|---|---|---|
| (1) one cell | TRUE | `.agi/nodes/.geometry/formations.md:8`, one live `id: config:formations` |
| (2) Posts + Stand up / take down, no new type | TRUE | 6/6 docs (3 live, 3 retired), `config` type since 09-12 |
| (3) read-back exactly one, non-zero otherwise | **FALSE** | 0 / list / unregistered FAIL; a 2nd cell file, or a 2nd `active:` key, PASS naming ONE |
| (4) one set switches, parked work listed | TRUE (re-pointed) | THOUGHT mark -> tag `parked:<goal>` (goal:g7.16.1.2.6); the set's stderr lists and wakes them |
| (5) g7.16 umbrella, g7.16.2 two-step | TRUE | goal frontmatter |

Falsifier 1 fires (as written: "passes with ... 2 formations active"); falsifiers 2 and 3 do not.

## Why disproved, not proved-with-a-note
The read-back resolves the cell through `node_writer.find_node_file`, which returns ONE file for an id and never says a second exists; the frontmatter loads through `yaml.safe_load`, which keeps the last of two `active:` keys silently. Nothing in `verify` counts either (the only duplicate-id finder, dashboard.find_duplicate_ids, is not a verify check). That is exactly the decay this goal names: a successor re-adds a copy and the proof stays green. The committed test (test_zero_or_two_active_fails) covers "2" only as a YAML list.

## Why 0.85, not higher
Both shapes need a non-write.py path (a hand-copy, a merge carrying a second cell, a hand-edited key): write.py's `set` rewrites one scalar and `create config formations` was refused by the spawn gate in scratch. write-guard may flag a hand-written file on the box that made it; it does not make the READ-BACK fail, which is what the falsifier names.

## Corrective
FORK: hypothesis:the-formation-read-back-fails-on-a-second-cell-or-a-second-active-key (corrective.md): check_formation counts live `id: config:formations` files and `active:` keys in the cell's frontmatter and FAILs naming each file:line when either is not exactly 1.
