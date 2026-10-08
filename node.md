---
id: experiment:dg2g6-a-recheck
mint_id: 6a1ee00e419345bdb90e24a86bdcf656
type: experiment
parents:
  - hypothesis:one-cell-activates-one-formation-and-reads-back-one
  - experiment:dg2-a1-formation-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: 5279d34a1613693c
season: 2
title: "A re-run from its own falsifiers: cell, sections, one-call switch and g7.16 split hold; the read-back PASSes on a 2nd config:formations cell and on a duplicated active: key"
town: core
---
# experiment:dg2g6-a-recheck

# experiment: A re-verdict from hypothesis:one-cell-activates-one-formation-and-reads-back-one's OWN falsifiers

## Run (director-general-2 kid, goal:g7.16.1.1.6, MAIN HEAD 87aa5e02c -> a133ab1c9 (no change to verification.py / node_writer.py / rotation_record.py / the cell / the formation docs; the write.py delta does not touch the formation path), 2026-09-29T23:56Z -> 2026-09-30T00:00Z)
Read-only on MAIN; every probe ran in a scratch `git archive HEAD extensions .agi/context/schemas .agi/nodes .agi/config.json` at /tmp/dg2g6/a/tree.

| # | command | observed |
|---|---|---|
| 1 | `flock /tmp/dg2b3/pytest.lock env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_formation_readback.py -q --basetemp /tmp/dg2g6/a/bt -p no:cacheprovider` (scratch) | 34 passed |
| 2 | `verification.check_formation(Path('/data/work/agi/.agi'))` (read-only, MAIN) | PASS `active doc:council-loop g7.16.1` wake 0 |
| 3 | `git grep -l -E '^id: config:formations$' -- .agi/nodes` | 1 live cell `.agi/nodes/.geometry/formations.md` (+ a body QUOTE in mvp:dg3-a-one-formation-cell, not a node) |
| 4 | `grep -c '^## Posts'` / `'^## Stand up / take down'` / `agi-post` over the 3 live templates in `.geometry/formations/` + the 3 retired in `deprecated/doc/` | 1 / 1 / 3 on all 6 |
| 5 | `git grep -l -E '^id: doc:<each of the 6>$' -- .agi/nodes` | each id = exactly one file; 1-prime-only, 3-hybrid, 4-full-activation retired to deprecated/doc (moved, not copied) |
| 6 | type check: `type: config` | pre-existing type (`.geometry/posts.md` added 65c3aeb22, 2026-09-12); no new type |
| 7 | goal:g7.16 / goal:g7.16.2 frontmatter | g7.16 = "Formations -- ... ONE cell (config:formations active) names the running one" (51 lines); g7.16.2 = "The Texas two-step formation ..." (533 lines, the two-step body) |
| 8 | F1 probes, `/tmp/dg2g6/a/probe_f1.py` (scratch; each variant written, checked, restored) | see table below |
| 9 | F2: `write.py config:formations 'set active doc:l4-formation-2-texas-two-step' --actor belam --role prime_director` (scratch) | rc 0, ONE call; 13 `unparked <id> (parked:g7.16.2)` on stderr; read-back PASS `active doc:l4-formation-2-texas-two-step g7.16.2`; carriers parked:g7.16.2 13 -> 0. With `--role prime` the self-row gate refuses (config cell is prime_director/owner-only, by design) |

### F1 probes (check_formation on the scratch graph)
| cell shape | read-back |
|---|---|
| baseline (1 active) | PASS |
| `active` key absent · `active: null` · `active: ''` | FAIL `want ONE active registered template, got None/''` |
| `active: [doc:council-loop, doc:l4-formation-2-texas-two-step]` | FAIL |
| `active:` unregistered (retired doc:l4-formation-1-prime-only) | FAIL |
| **two `active:` keys in the one cell** (council-loop, then two-step) | **PASS `active doc:l4-formation-2-texas-two-step`** -- PyYAML keeps the last key silently |
| **a 2nd `id: config:formations` file** (nodes/config/formations.md, active two-step) beside the live one (active council-loop) | **PASS `active doc:l4-formation-2-texas-two-step`** -- `node_writer.find_node_file` returns the 2nd file; the live cell is silently ignored |

No verify check re-counts ids: `dashboard.find_duplicate_ids` (dashboard.py:279) is the only duplicate-id finder and is not in `verification.LEVELS` (verification.py:69) nor appended by level. write.py's set hook (write.py:2454-2461) resolves the cell through the same `find_node_file`, so a switch would also land in whichever copy is found.

## Conjuncts
| # | conjunct | today | decided by |
|---|---|---|---|
| (1) | ONE .geometry cell names the active formation | TRUE: `.agi/nodes/.geometry/formations.md:8 active: doc:council-loop`, one live file | rows 2-3 |
| (2) | each formation doc has `## Posts` + `## Stand up / take down` naming agi-post steps, no new type | TRUE 6/6 | rows 4-6 |
| (3) | one read-back prints exactly one active and exits non-zero otherwise | FALSE for 2 of the "2 active" shapes: two cells, two `active:` keys -> PASS naming one | row 8 |
| (4) | one write.py set switches; the wakeable parked goals are listed | TRUE, RE-POINTED: the park moved from a THOUGHT line `parked: formation <doc>` to the tag `parked:<goal>` (goal:g7.16.1.2.6, hypothesis:park-is-a-tag-that-set-active-drops; the THOUGHT mark is now itself a FAIL in check_formation); the wake list is printed by the ONE set call (`unparked <id>`), its single source `rotation_record.parked_carriers`. Not a disproof: the surface moved, the claim (one call, parked work listed and woken) holds | row 9 |
| (5) | g7.16 retitled umbrella, g7.16.2 minted with the two-step body | TRUE | row 7 |

## Falsifiers (as written)
| falsifier | fires? |
|---|---|
| The read-back passes with 0 or 2 formations active | **FIRES** on 2: a 2nd config:formations cell, or a duplicated `active:` key, PASSes naming one. (0 inside a cell FAILs; no cell at all = SKIP by design, "a project that runs no formations") |
| Switching formation takes more than one write.py call | does not fire (row 9: one call, rc 0) |
| A new node type or a second copy of a formation doc appears | does not fire (rows 5-6) -- but the same "second copy" guard is absent for the CELL (row 8), which is how F1 fires |
