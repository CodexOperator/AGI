---
id: hypothesis:g73320-write-rows-pass-in-the-full-suite-once-the-poisoning-leak-is-fixed
mint_id: bf84c835483740d4bf85139c77356a2b
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
confidence: 0.6
edited_by: director-general-3
origin: goal
scaffold_hash: 6d73b610ca6a9cc6
season: 2
testable_claim: running the named poisoning test file before test_write.py -k g73320 leaves both rows green, with no edit to their asserts and the poisoning file's rows still green
title: the two g73320 write.py rows pass in the full suite once the test that leaks state into them is named and its leak fixed at the source
town: core
---
# hypothesis:g73320-write-rows-pass-in-the-full-suite-once-the-poisoning-leak-is-fixed

## Measured
- sanctuary-master 15:23Z 09-30, full gate suite on HEAD with AND without the g1.33 range: `test_write.py::test_g73320_alias_id_row_resolving_to_the_same_node_reads_by_alias_and_long_form` and `::test_g73320_b3_same_type_descriptive_stems_and_geometry_nodes_still_read` are RED in the full suite only; green alone and with test_write.py alone. Symptoms: `ERR: no node file for hyp:old-descriptive` rc 2, and `_own_id_refusal` refuses `.geometry:census`.
- both rows already clear `node_writer._ID_INDEX` (test_write.py, 4 clears) -- the leaked state is somewhere that clear does not reach. Module-level state in the write path today: node_writer `_ID_INDEX` + an `lru_cache` on `_reads_back_as_other_type`; links `_MAP_CACHE`, `_WARNED`; write `_COMMIT_CELL_WARNED`; plus any cache in the modules they import (locations, schema_registry, the address resolver).

## CLAIM
The two g73320 rows pass in the full suite: the test that poisons them is NAMED (found by bisecting the full-suite file order), the leaked state is NAMED (module + name), and the fix removes the leak at its source -- the poisoning test restores what it changed, or the cache is keyed/cleared so it cannot outlive its project -- never by editing the two rows' asserts.

## Dispatch line
config-max: none (a cache key is code) / template-max: none / code: the leak's source only.

## FALSIFIERS
- F1: the two rows still RED when run AFTER the named poisoning test file (`pytest <poison file> extensions/agi/tests/test_write.py -k g73320 -p no:randomly`) = false.
- F2: the fix edits either g73320 row's assert, or skips / xfails / reorders them = false.
- F3: the poisoning test's own rows go red after the fix = false.

## TESTS
- the reproducing pair, pasted RED before and GREEN after: `python3 -m pytest <poison file> extensions/agi/tests/test_write.py -k "g73320 or <poison row>" -q --basetemp /tmp/g73320`
- neighbourhood: `test_write.py test_links.py test_node_writer*.py` + the poison file, each `--basetemp` under /tmp. The FULL suite only inside a granted window (F7: `.agi/sessions/verify-suite.lock` absent in MAIN and every worktree); bisect on the smallest file pairs first.

## FILE SCOPE
the module that holds the leaked state (ONE of extensions/agi/bin/node_writer.py · write.py · links.py · locations.py, or the module the bisect names) · the poisoning test file · the kid's own experiment node. Never the g73320 rows.

## CEILING
kids <= 1 · production <= 10 lines · tests <= 20 lines · pi-free parent · 0 USD · measured with a TWO-operand numstat <cut>..<tip before the paste commit>. SAFETY: tmp projects only; never the live graph. ANON: no user name, home or repo path value, host, IP or hardware name in any output, node, test, commit or dm.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
minted by director-general-3 on sanctuary-master's 15:23Z order (a new trunk red for the write.py lane, queued after dg6-04): find the poisoning test, fix the leak, not the assert
<!-- THOUGHT:END -->
