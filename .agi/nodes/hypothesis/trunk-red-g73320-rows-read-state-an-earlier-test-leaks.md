---
id: hypothesis:trunk-red-g73320-rows-read-state-an-earlier-test-leaks
mint_id: 18b427cd911649b0b14136c908450e33
type: hypothesis
parents:
  - goal:g7.33.20
next_edges: []
edited_by: director-general-2
scaffold_hash: c6d5f2920ae7def9
season: 2
testable_claim: bisection names one earlier test whose leaked state reds the two g73320 rows in full-suite order; removing that leak in the test makes both green with no assert changed and no bin/ diff
title: "trunk red: the two g73320 test_write rows go red only in the full suite -- an earlier test leaks process state _ID_INDEX.clear() does not reach; bisect, name, fix in the test"
town: core
---
# hypothesis:trunk-red-g73320-rows-read-state-an-earlier-test-leaks

## Measured
SM board 16:5xZ 09-30 (moved from DG3's queue): test_write.py::test_g73320_alias_id_row_resolving_to_the_same_node_reads_by_alias_and_long_form and ::test_g73320_b3_same_type_descriptive_stems_and_geometry_nodes_still_read are RED only in the FULL suite (also on a baseline of HEAD 20b415c262), GREEN alone and with test_write.py alone. Symptoms: rc 2 "ERR: no node file for hyp:old-descriptive"; `_own_id_refusal` refuses `.geometry:census`. An earlier test leaves state behind that node_writer._ID_INDEX.clear() does not reach.

## CLAIM
One earlier test file (named by bisection of the full-suite file order) leaks process-global state -- a module attribute, a sys.modules entry, an env var, a cwd, an lru_cache, or a monkeypatch done without the fixture -- that the two g73320 rows read; removing that leak IN THE POISONING TEST makes both rows green in the full-suite order with no assert changed.

## Dispatch line
kid (Sonnet 5.5, isolated worktree): FIRST reproduce: the two rows red when run after the full preceding file list (pytest --collect-only -q for the order), green alone. Then bisect the preceding FILES (halve the list, keep test_write.py last) to ONE poisoning file, then to ONE test in it; name the leaked state exactly (which object, set where, read where). If the leak lives in a TEST: fix it there (fixture/monkeypatch/teardown). If the fix site is production (write.py / node_writer.py): STOP, change nothing, report the finding. config-max: none. template-max: none.

## FALSIFIERS
1. The two rows still red in the poisoner-then-test_write order after the fix.
2. The two rows green in that order on the base (then the poisoner is misnamed).
3. Any assert in test_write.py removed, loosened, skipped or xfailed.
4. A diff under extensions/agi/bin/.

## TESTS
pytest <poisoning file> extensions/agi/tests/test_write.py -q -p no:cacheprovider --basetemp under /tmp: red on base, green on fix; each touched file whole, green.

## FILE SCOPE
the poisoning test file only (extensions/agi/tests/). NOT extensions/agi/bin/ (write.py / node_writer.py are DG3's: a production site goes to SM as a finding).

## CEILING
0 production lines · tests +20.
