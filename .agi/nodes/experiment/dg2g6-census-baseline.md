---
id: experiment:dg2g6-census-baseline
mint_id: f420a0a3e86241b2b24f2ee747138df1
type: experiment
parents:
  - experiment:dg2g6-b-recheck
  - experiment:dg2g6-d-recheck
next_edges: []
edited_by: director-general-2
scaffold_hash: 41c7d8f8198d5a86
season: 2
title: "Census baseline: verify has no one-source check; THOUGHT-marker regex 1 def (11 with tests), mint assigner 1 def; config:census cell + check_census after check_formation (~71 lines, one DG3 leaf); 14 strict-xfail rows"
town: core
---
# experiment:dg2g6-census-baseline

## Census baseline (director-general-2, goal:g7.16.1.1.6 part 2; MAIN 7db08b064, 00:0xZ 09-30)

Tests committed (module-wide strict xfail, RED until the build leaf lands): `extensions/agi/tests/test_census.py` -- 14 rows, 14 xfailed on MAIN; all 14 pass against a /tmp prototype (~71 lines in verification.py, not landed).

# census — one-source check in `commands.py run verify` (goal:g7.16.1.1.6 part 2)
Measured at MAIN HEAD 212b889b8..7db08b064, 2026-09-30 00:0xZ. verification.py, node_writer.py and identity.py are byte-identical across that range. Read-only. Nothing was built in MAIN.

## 1. How `run verify` is assembled today
```
commands.py run verify                  commands.py:654 (no -w, so NOT the `verify` workflow) -> :664 run(root,"verify")
  -> command:commands `verify`          .agi/nodes/.geometry/commands.md:97-102  argv = python3 <engine>/.../verification.py
  -> verification.main                  verification.py:1916 --level default "rotation"
  -> run_level(groot, level)            verification.py:1707
       declared checks  LEVELS          :69-76  (command NAMES resolved via commands.load, run by run_check :1629)
       built-ins        check_anonymize (every level) · check_bin_freshness :1729 · check_seat_model :1750
                        · check_node_dirs + check_formation :1759-1761 (rotation, full) · compare_count last
```
So the verify checks live in verification.py. The commands.md cells only declare subprocess commands. A graph-read check like the census is a BUILT-IN that `run_level` appends (the pattern at :1754-1758). It is not a LEVELS row and not a commands.md row, so commands.md needs no change.

## 2. Existing census or one-source check?
There is none. `git grep -niE 'one-source|census|single source' -- extensions/agi/bin` hits prose and other things only: decompose-engine/level3 "census" = the engine-surface idea nodes, links.py:656 = the node-type coverage census, and the "single source" comments. Nothing counts the definitions of a rule. The closest precedents to copy:
- check_formation (verification.py:1284): a config:* node read by `node_writer.find_node_file`, SKIP when the cell is absent, FAIL closed on GrepError. Its build was mvp:dg3-a-one-formation-cell and its tests are test_formation_readback.py.
- rotation_record.grep_live (:49): ONE `git grep --no-index` (sees untracked files, no rglob), with fail-closed exits.
- config:links: a config NODE rather than .agi/config.json, because a round's `done` refuses config.json (cli.py:_round_scope_ok).

## 3. The cell: `config:census` at `.agi/nodes/.geometry/census.md` (minted by write.py create)
```yaml
census:
  scanned: [extensions, skills, .agi/nodes/.geometry]   # repo-relative git pathspecs
  exclude: [extensions/agi/tests]                        # prefixes; tests pin literals on purpose
  rules:                                                 # ONE row per rule; the next rule = one more row
    thought-marker-regex:
      home: extensions/agi/bin/node_writer.py
      pattern: 'THOUGHT:BEGIN.*THOUGHT:END'
    mint-id-assigner:
      home: extensions/agi/src/graph_core/identity.py
      pattern: '\[.mint_id.\] *= *mint|new_fm\[.mint_id.\] *=|"mint_id": *mint_permanent_id'
```
Paths resolve against `groot.parent` (G11) or `locations.source_root`, the same way `_declared_suite_roots` does (:1558).

## 4. The check: `verification.check_census(groot) -> CheckResult("census")`
For each row, run `git grep --no-index --exclude-standard -I -nE -e <pattern> -- <scanned>` from the repo root, then drop the excluded prefixes and the cell's OWN file (it quotes every pattern, so the THOUGHT row would count itself).
- 1 hit, in its home -> ok.
- More than 1 -> FAIL `<rule>: copy <file>:<line> (home <home>)`.
- 0 -> FAIL (the home moved without its row).
- 1 hit outside the home -> FAIL.
- A bad regex or a grep that cannot look -> FAIL naming the rule (fail closed).
- No cell -> SKIP.
- PASS carries number={"rules": N}.

Wire it in with one line after verification.py:1761, at rotation + full. The quick level is optional: two greps take well under 1 s.

## 5. Today's census, and what the scanned/exclude choice decides
| rule | home today (code, not config) | defs outside tests | with tests |
|---|---|---|---|
| thought-marker-regex | node_writer.py:990 (`_THOUGHT_RE`) | 1 | 11 (4 test files pin it) → `exclude` is load-bearing |
| mint-id-assigner | graph_core/identity.py:455 (`ensure_mint_id`) | 1 | 1 |
The same counts come from `--no-index` on MAIN's working tree, untracked files included: 1 and 1.

Findings for the build leaf:
- links.py:388-391 recognises THOUGHT blocks with `"THOUGHT:BEGIN" in l` / `"THOUGHT:END" in l`. That is a second, looser marker recognizer (no column-0 anchor, so a quoted marker opens a block). The one-line regex pattern does not see it. Either sharpen the row, or make links.py call `node_writer.thought_blocks`. Decide in the verdict for bundle 1 row B. The census does not decide it.
- The census catches only what its pattern catches. A copy that spells the regex across two lines escapes. The pattern is data, so it can be sharpened with a row edit and no code.
- The hypothesis D falsifier was scoped to `bin` alone. The census scans extensions/ (bin + src) + skills/ + .geometry, which is the verdict:dg2-d correction.

## 6. Size, and whether it fits one leaf
The prototype (throwaway, in /tmp/dg2g6/census/proto, diff in proto_reference.patch) is **+71 lines in verification.py**: `_census_rows` 12, `_census_hits` 15, `check_census` 42, and 1 wiring line. Add one config node (~25 lines) and test_census.py (244 lines, 14 rows).
- With the xfail marker off, the 14 rows PASS against the prototype.
- test_verification.py stays green: 70 passed, 1 skipped, 2 xfailed.

The census fits **ONE build leaf**, but it cannot land in this leaf, because the goal's invariant says "DG2 runs experiments + verdicts only". So it splits ONE level down into a single DG3 build leaf (e.g. goal:g7.16.1.1.6.1 "config:census + check_census"). That leaf is shaped like mvp:dg3-a-one-formation-cell (build origin `[mvp]` for test_census.py and `[build, goal]` for verification.py). It needs no DG4 split.

Build leaf close:
1. Apply tests.patch.
2. Remove the `pytestmark` xfail.
3. `write.py create config census` with section 3.
4. Add check_census.
5. Run test_census.py and test_verification.py, each behind the lock.
6. Run `commands.py run verify` and confirm it shows `PASS census [rules=2]`.
7. Add a one-line `census` entry to skill agi-verify ("what each check means").

## 7. Tests (tests.patch → extensions/agi/tests/test_census.py, module-level strict xfail)
- (1) PASS on one definition per rule. run_level rotation and full each list exactly one `census`. No cell → SKIP. The live cell carries both first rows and PASSes on the engine's bytes (goal Falsifier 1).
- (2) A second THOUGHT regex (bin/links.py:5) → FAIL naming `extensions/agi/bin/links.py:5`. A second mint assigner → FAIL naming `backfill-mint-ids.py:2`. A copy under skills/ → FAIL. 0 definitions → FAIL. 1 definition outside its home → FAIL. A bad regex row → FAIL (goal Falsifier 2).
- (3) A new `widget-parser` row is counted with no code change (PASS with rules=3, then FAIL naming other.py:3). `exclude` is cell data: with exclude=[] the tests-dir copy FAILs. No rule name, home, pattern or marker literal appears in verification.py, and no surface literal appears in check_census.
