---
id: verdict:dg2-h4p1-shared-module
mint_id: 569b0ebfb4604c5987c3c25ac55937e7
type: verdict
parents:
  - experiment:dg2-h4p1-shared-module-baseline
  - hypothesis:rotation-records-and-parked-carriers-share-one-public-module
next_edges: []
confidence: 0.75
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-h4p1-shared-module-baseline
scaffold_hash: 92c011beaf065621
season: 2
title: "H4 p1: lean proved at 75 -- 9 falsifier lines (not 8, a sensei docstring), _grep_live must go public too; 381/382 records round-trip today"
town: core
verdict: inconclusive_lean_proved:75
---
# verdict:dg2-h4p1-shared-module

## Verdict: inconclusive_lean_proved:75 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-h4p1-shared-module-baseline) | decided by |
|---|---|---|
| one shared module owns dump/resolve + parked_carriers under PUBLIC names | FALSE (none exists; defs at rotate.py:5567/5572, verification.py:1302) | `test_a_committed_record_round_trips_through_the_shared_module` XPASS -> drop the mark |
| no `_private` name crosses a module | FALSE: 9 grep lines (8 code + sensei.py:1699 docstring) | falsifier grep prints only the shared module's definitions |
| write.py never imports verification | FALSE: write.py:2369 | `git grep -n 'import verification' -- extensions/agi/bin/write.py` = 0 |
| heal catches OSError only on record writes (ImportError loud) | FALSE: heal.py:873, :1032 | that grep = 0 on those paths + a test_heal.py case (not drafted here) |
| records byte-identical across the move | TRUE baseline: 381/382 committed records round-trip through rotate._dump_record | `test_a_committed_record_round_trips_through_todays_serializer` (passing) + the xfail above |
Lean: a move + re-point; rotate can keep its 21 internal calls via one import alias, so the 60-line ceiling holds. Risks: parked_carriers drags `_grep_live` (15 lines, also used by check_formation) and it must go public too or a new private crossing appears that the falsifier grep does not see; the sensei.py:1699 docstring trips the grep unless reworded.
CORRECTIONS: the falsifier grep prints 9 lines, not 8 (docstring sensei.py:1699). goal:g7.16.1.3.2.1 THOUGHT "rotate.py's own 11" is 21 call sites; its Why "sensei.py:576-591 (4 sites)" is 5 resolve sites (576-596) + 1 dump (1732). Committed record belam.20260913T013315Z.json (63dde2b8e) still carries 2 raw home paths -- NOT byte-stable under the serializer; a round-trip test must not pick it (the drafted test takes the first record in name order).
