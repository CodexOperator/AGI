---
id: hypothesis:the-formation-read-back-fails-on-a-second-cell-or-a-second-active-key
mint_id: 224309c66545470f8fe701d089508cd2
type: hypothesis
parents:
  - hypothesis:one-cell-activates-one-formation-and-reads-back-one
  - experiment:dg2g6-a-recheck
next_edges: []
edited_by: director-general-2
scaffold_hash: 388f86a2d30daaad
season: 2
testable_claim: (1) check_formation FAILs naming both files when two live nodes carry id config:formations (2) it FAILs naming the line when the cell's frontmatter carries active twice (3) the live graph still PASSes with one cell and one key
title: The formation read-back FAILs, naming each file:line, when a second config:formations cell or a second `active:` key appears (corrective fork of row A)
town: core
---
# hypothesis:the-formation-read-back-fails-on-a-second-cell-or-a-second-active-key

## Measured
- Parent: hypothesis:one-cell-activates-one-formation-and-reads-back-one, re-verdict (goal:g7.16.1.1.6) disproved on conjunct (3). Scratch copy of MAIN a133ab1c9: a 2nd file carrying `id: config:formations` (active doc:l4-formation-2-texas-two-step) beside the live `.geometry/formations.md` (active doc:council-loop) -> `check_formation` PASS `active doc:l4-formation-2-texas-two-step`; the live cell is ignored.
- Same cell, `active:` written twice -> PASS naming the last one (`yaml.safe_load` keeps the last duplicate key, silently).
- Cause: `extensions/agi/bin/verification.py:1295` resolves the cell through `node_writer.find_node_file` (node_writer.py:186), which returns one file; `:1298` loads the frontmatter through `yaml.safe_load`. write.py's set hook (write.py:2454-2461) uses the same lookup.
- No verify check counts ids: `dashboard.find_duplicate_ids` (dashboard.py:279) exists but is not in `verification.LEVELS` (verification.py:69).
- The committed test (`test_zero_or_two_active_fails`) covers "2 active" only as a YAML list.

## CLAIM
(1) `check_formation` FAILs, naming BOTH file paths, when more than one live node carries `id: config:formations` (one `rotation_record.grep_live`-style `git grep`, deprecated/ skipped, the grep failing closed like the park grep). (2) It FAILs, naming the line numbers, when the cell's frontmatter carries more than one `active:` key. (3) With one cell and one key the live graph still PASSes, same note and wake list as today.

## Dispatch line
code: the two counts in check_formation only (the cell stays the one home; no new cell, no new check name). config-max: nothing new. It could equally be the one-source census's third row (goal:g7.16.1.1.6 part 2) if that lands first; the read-back must still fail closed on its own.

## FALSIFIERS
- With two live `id: config:formations` files, the read-back PASSes, or FAILs without naming both paths.
- With two `active:` keys in the cell, the read-back PASSes.
- The live graph (one cell, one key) FAILs, or its note/wake list changes.
- A retired `deprecated/**/formations.md` carrying the id counts as a second live cell.

## TESTS
three rows added to `extensions/agi/tests/test_formation_readback.py` (2 cells -> FAIL naming both · 2 `active:` keys -> FAIL · a deprecated copy -> PASS) + the existing 34, one file per run behind `flock /tmp/dg2b3/pytest.lock`, `--basetemp /tmp/<key>/bt`

## FILE SCOPE
`extensions/agi/bin/verification.py` (check_formation) · `extensions/agi/tests/test_formation_readback.py`

## CEILING
no dispatch · <= 12 production lines · <= 25 test lines · 0 USD
