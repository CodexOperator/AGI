---
id: hypothesis:mint-offers-storage-categories-from-config-cells
mint_id: 4bd1d330335142aebd7a5b34e6e38457
type: hypothesis
parents:
  - goal:g4.18.1.3
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: 4a56d56600042137
season: 2
tags:
  - engine
  - write
  - locations
  - g4.18.1
testable_claim: "(1) storage categories are config cells (2) one locations.py resolver numbers them and maps a pick + tail to (location, payload_ref), a custom path flagged (3) one CLI prints the list; one new cell = one new option, no code edit (assigned: director-engine)"
title: "the mint flow offers storage categories as a numbered list read from config cells, plus a flagged custom path (goal:g4.18.1.3; assigned: director-engine)"
town: core
---
# hypothesis:mint-offers-storage-categories-from-config-cells

## Measured
- A payload's base is already a NAME, never a path: `locations.payload_base` (extensions/agi/bin/locations.py:445) resolves `source_root` · `graph_root` · `repo_root` · any key under the config's `locations:` block; an unknown name is a hard error ([build].md "location" section). `write.py create --payload` stamps `location: source_root` (write.py ~2904).
- NO storage-CATEGORY list exists: the directory a post files a new payload under (engine code, tests, skills, .geometry config, schemas, context templates) is typed by hand into `--payload`; nothing offers the options, so a post can only guess the prefix.

## CLAIM
(1) the storage categories are CONFIG cells (one table, e.g. `mint.storage_categories.<key> = {location, prefix, label}`), seeded with the categories the owner names (engine code, tests, skills, .geometry config, schemas, context templates) (2) ONE resolver in locations.py returns them as a numbered list in cell order, and turns a pick (number or key) plus an optional path tail into `(location, payload_ref)`; a path outside every category is accepted and returned flagged `custom` (3) a one-line CLI prints the numbered list (the pane-side picker the draft flow of goal:g4.18.1.2 will call); adding one cell in a temp config adds one option with no code edit.

## Dispatch line
config-max: the category table IS the change -- a config cell, seeded by the kid via write.py/config edit in the round. template-max: none (the flow text rides goal:g4.18.1.2). code: the resolver + its CLI only, because no reader of such a table exists.

## FALSIFIERS
- a temp config with one extra category cell does not print one extra option (exit 0).
- `grep -nE '"(extensions|skills|\.agi)/' ` over the new resolver code finds a storage-path literal.
- a pick outside the list, or a custom path, raises instead of returning the flagged custom row.
- the resolver returns a location name `payload_base` refuses.

## TESTS
extensions/agi/tests/test_storage_categories.py (new; temp config only, tmp_path, never the live config written). Neighbourhood: test_locations*.py test_write*.py test_bin_help_smoke.py. Every pytest under `timeout 600`, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/bin/locations.py (the new resolver + CLI only) · .agi/config.json (the one new cell block) · extensions/agi/tests/test_storage_categories.py. NOT write.py (goal:g4.18.1.1 is under review there; the wiring into the mint flow rides goal:g4.18.1.2).

## CEILING
1 kid · <= 40 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude.

## CORRECTIVE DH.519 -- closes mur-director-engine-18 DH.510-k1 + k2 (accept_with_residue, verify died before returning)
BASE      CUT FROM season2/loops/hypothesis-mint-offers-storage-c-a00-a77d4234 tip 0c3d7766a. No merge. Never rebase.
1. locations.py:541-543 -- a non-dict storage category cell is skipped with `continue` and vanishes from the numbering -> refuse it BY NAME (a BAD row naming the cell, or a ValueError naming it), plus one test with a mistyped cell (DH.510 order 4, still NOT_MET).
2. locations.py:502 -- known_payload_locations admits every str KEY under locations: without checking its value, while payload_base:479-491 accepts only a non-empty str value -> admit only the names payload_base accepts; one test: a cell naming such a location is refused by name.
3. locations.py:1084-1088 -- main does not catch the ValueError raised at 583-588, so --storage-pick with a bad-location cell prints a traceback -> print the same ERR: line the other branches use and exit non-zero; one test through main.
4. experiment:a00-4bf392d4-1e7c8c is stale: verdict inconclusive_lean_disproved:45, probe-C (:18) and Still-open bullet 1 (:117-119) call the --storage-pick fall-through open, but 9f5816bdb fixed it -> RE-RUN the probe at the base, paste the output, set the verdict and bullets to what it shows (write.py only; never the thought verb over its THOUGHT).
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_storage_categories.py test_locations.py test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/locations.py (storage functions + their CLI branch only) · extensions/agi/tests/test_storage_categories.py · experiment:a00-4bf392d4-1e7c8c (write.py) · the kid's own node. NOT .agi/config.json.
CEILING   HARD CAP: 1 kid · net <= 15 production lines · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.519: mur-director-engine-18 DH.510-k1+k2 accept_with_residue (verify stage never returned): non-dict cell still silent (NOT_MET), location_ok over-accepts, CLI traceback, stale kid node a00-4bf392d4. Demoted as notes: two copies of the root names (by construction), parent prose in a kid THOUGHT. Ceiling breach (4 kids vs 1) and the round gate refusing config.json = findings rows, not corrective items.
<!-- THOUGHT:END -->
