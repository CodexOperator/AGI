---
id: experiment:a00-e93ed21c-959acf
mint_id: 08fd37614a9945329b042f360bbd50d9
type: experiment
parents:
  - hypothesis:mint-offers-storage-categories-from-config-cells
next_edges: []
confidence: 0.85
edited_by: a00-a77d4234
evidence_runs:
  - experiment:a00-e93ed21c-959acf
loop: hypothesis:mint-offers-storage-categories-from-config-cells@s2
model: stealth/space-bunny-alpha
probes:
  - "probe-A wire (conjunct 2, the kid own claim): live CLI in a temp project whose cell tests.location=no_such_place -- --storage-categories still lists 6 rows at exit 0, --storage-pick 2 exits 1 with ValueError naming the option and the value; HOLDS, the diff bytes reach the real call site"
  - "probe-B gate (conjunct 1+2, PARENT claim not the kid claim): every SEEDED category read from the live config through payload_base+prefix -- geometry -> <root>/.geometry and schemas -> <root>/context/schemas DO NOT EXIST, yet location_ok=True for both; the stamp checks the NAME, not the target, so 2 of 6 options resolve nowhere; FIRES"
  - "probe-C auth/gate (claim 5): --storage-pick 2 --tail foo.py with NO --storage-categories prints the default layout and exits 0, resolving nothing; the flags fall through silently; FIRES"
  - "probe-D gate (order item 4, refuted): a non-dict cell inserted mid-table does NOT shift numbering (n = len(rows)+1 is dense) -- it is skipped silently, no error, but the numbering-shift premise in the dispatch orders is FALSE against these bytes"
production_lines: 27
profile: balanced
role: kid
scaffold_hash: 7f59e51d07227834
season: 2
title: a bad cell location is refused by name at the option, not passed to payload_base
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e93ed21c-959acf

## The round in one line

The parent's review demoted the previous kid to `inconclusive_lean_disproved:55`
because falsifier 4 FIRED: `resolve_storage_category` copied a cell's
`location` out of the config with a bare `str()` and no membership test, so a
typo in one config cell became a row the write path refuses later, far from the
option, with an error that names the config value and not the option. This round
closes that falsifier, in the author's own file, with no change of scope.

## What I changed (3 code hunks, +32/-5, net 27 production lines)

`extensions/agi/bin/locations.py` only. `write.py` untouched, `.agi/config.json`
untouched (the six seeded cells are already on the branch), no path literal added.

| # | Change | Where |
|---|--------|-------|
| 1 | NEW `known_payload_locations(config)` — the location NAMES `payload_base` accepts, in its own resolution order (the three roots, then every key under `locations:`). One list, so the picker and the write path cannot disagree. | beside `payload_base` |
| 2 | `storage_categories` now stamps each row `location_ok = name in known_payload_locations`. Listing stays TOTAL — printing the picker never raises, whatever the config says. | `storage_categories` |
| 3 | `resolve_storage_category` REFUSES a hit whose `location_ok` is false, raising `ValueError` that names the OPTION, the bad value, and the accepted names. No such row is ever returned, by number or by key. | `resolve_storage_category` |

`payload_base` itself is deliberately NOT refactored to use the new list: its
`known` is built `sorted()` and its KeyError message is already covered by
`test_locations.py`. One source per rule would prefer the share; a behaviour
change to the write path's error text in a 27-line round would not.

## Falsifiers, each turned into a test

| Falsifier | Test | Result |
|---|---|---|
| 4. the resolver returns a location name `payload_base` refuses | `test_bad_cell_location_is_refused_by_name_not_passed_through` (asserts the raise, and that the message names both the option and the value), `test_no_row_of_any_table_carries_a_name_payload_base_refuses` (the property: every row's `location_ok` is exactly membership, and any row the resolver DOES return resolves through `payload_base`) | closed |
| 1. a temp config with one extra category cell does not print one extra option | `test_one_extra_cell_adds_one_option` (previous round, still green) | holds |
| 2. a storage-path literal in the resolver | `test_resolver_carries_no_storage_path_literal` (greps the source of all three functions now) | holds |
| 3. a pick outside the list, or a custom path, raises | `test_custom_path_is_flagged_never_raised`, `test_pick_outside_the_table_is_flagged_custom_not_raised` | holds |

New: `test_a_declared_locations_cell_makes_a_bad_cell_acceptable` — the fix is
CONFIG, not code: a cell naming `docset` is un-validatable until `locations.docset`
is declared, and accepted after. One config edit, no code edit, which is the
hypothesis's own claim about the table.

## Evidence

```
$ timeout 600 python3 -m pytest extensions/agi/tests/test_storage_categories.py -q
14 passed in 0.15s

$ timeout 600 python3 -m pytest extensions/agi/tests/test_locations.py \
    extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_write.py -q
296 passed, 6 skipped in 8.67s

$ python3 extensions/agi/bin/locations.py --storage-categories | head -3
1  engine_code  source_root  extensions/agi/bin  (engine code)
2  tests  source_root  extensions/agi/tests  (tests)
3  skills  source_root  skills  (skills)

$ # live config, one cell's location mutated to a name payload_base refuses
REFUSED: storage category 'tests' declares location 'no_such_place', which
payload_base does not accept. Use one of: source_root, graph_root, repo_root,
comms_root, pi_home, claude_home.

$ git diff --numstat -- extensions/agi/bin/locations.py .agi/config.json
32	5	extensions/agi/bin/locations.py
```
Test file +47 lines, excluded from the production count. Production lines: **27**
(net), against the 40 ceiling and the 80 the previous round was flagged for.

## Still open (not mine, recorded for the parent)

- The category table is still read by nobody: the picker is inert until
  goal:g4.18.1.2 wires it into the mint flow.
- `payload_base`'s own `known` list duplicates `known_payload_locations`
  (sorted, not insertion order). One source per rule says share it; it is a
  behaviour change to the write path's error text and belongs to whoever owns
  `payload_base`, not to a 27-line patch under it.

## Agent Notes
Closed the hypothesis falsifier 4 the parent review saw fire: known_payload_locations(config) is the one name list, storage_categories stamps location_ok per row, resolve_storage_category refuses a bad cell location by naming the option (3 hunks, +32/-5, 27 production lines); 14 storage-category tests, 296 neighbourhood green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW of DH.510 (a00-a77d4234), reading git diff 3d470e290..9f6e018a4, not the result file.

(1) WHAT THE INSTRUCTION SAID: "COMMIT the kid edits", "any byte outside FILE SCOPE = cut the kid", and seven numbered defects; kid briefs carry a 40-line production ceiling.

(2) WHAT THE MACHINE ACTUALLY DOES: the diff is three files -- locations.py +32/-5, test_storage_categories.py +47, its own node. Every byte is inside FILE SCOPE; no config.json edit, no write.py edit, no path literal. known_payload_locations() at L493 is the one name list; storage_categories stamps location_ok at L525; resolve_storage_category raises by name at L556. I ran the live CLI in a temp project with a cell mutated to no_such_place: the list still prints 6 rows at exit 0, --storage-pick 2 exits 1 naming tests and no_such_place. The claim the node titles itself on HOLDS, and I am not the one who wrote it.

(3) THE NEAR MISS: a stamp called location_ok reads like a guarantee and is only a membership test in the accepted-names list. Nothing checks the directory the row points at. I ran every seeded cell through payload_base+prefix: geometry -> <root>/.geometry and schemas -> <root>/context/schemas do not exist, both stamped ok=True. A reader who trusts the stamp believes 6/6 options are usable; the machine says 4/6. Same for the CLI: --storage-pick 2 --tail foo.py with no --storage-categories prints the default layout and exits 0 -- resolved nothing, refused nothing. The fix closes the name and leaves the target and the flag-pair open.

(4) IF YOU DEVIATE FROM A STANDING RULE: dispatch order item 4 ("a non-dict cell shifts numbering") is FALSE against these bytes and I refute it rather than order it fixed -- n is len(rows)+1, dense, so a skipped cell shifts nothing; it is merely silent, which is not the defect that was ordered. Ordering a fix for a defect that does not exist would have cost a line and taught the graph a false mechanism.

VERDICT: the node own claim is proved and its evidence_runs name itself; I keep it. The PARENT hypothesis is not proved: conjunct 2 (a pick maps to a real location) fails for 2 of 6 seeded cells, and conjunct 3 fails for a bare --storage-pick. Residue is carried to the next kid on this branch. 27 production lines against a 40 ceiling, and the title is the kid own words.
<!-- THOUGHT:END -->
