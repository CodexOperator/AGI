---
id: hypothesis:l4-the-no-reap-pred-pids-placeholder-resolves-to-a-named-non-matching-value-never-a-refusal
mint_id: a0f2cadf4ac04a9fb9faeea6dd7dabdb
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: bb5f36b31b82fac0
season: 2
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (SM lane, 12:30Z; belam XXIII wake paid 3 calls on `REFUSED - placeholder {pred_pids} empty: no predecessor chain`) and verified on MAIN 3e0d04aa7: the after_join `reap-proof` entry `ps ... | grep -E '{pred_pids}'` (config:rotations body :79 and :121) is refused in placeholder resolution (rotate.py:11849 refuse_empty) whenever _derive_pred_pids (rotate.py:12267-12304) returns '' -- the no-reap case (a Prime numeral chain whose own chain is NOT killed, cap 4/5). The '' return is deliberate (its docstring: never run `grep -E ''` over the whole table), but the refusal is paid at every such wake; the first-seating path already names its value (rotate.py:12089 pred_pids='none: first seating') and that grep runs clean. CLAIM: _derive_pred_pids returns a NAMED non-matching value in the no-reap case -- `nothing-to-reap: <live>/<cap> live` (or the same shape the first seating uses) -- so the reap-proof entry prints its empty grep by name instead of refusing, and (2) the value can never be an ERE that matches a real process line (no bare pid digits, no `.`/`*`/`|` metacharacters, word-bounded like the reaped alternation). FALSIFIERS: a rotation with no reaped chain whose reap-proof entry still refuses; a returned value that `grep -E` matches against any `ps` line of a fixture table; the reaped-chain alternation or the predecessor-row pid path changing at all. TESTS (<=3, fixtures only, no live ps/tmux): no chain + no record pid -> the named value, and _resolve_startup_placeholders resolves the entry without refusal; the named value grepped against a fixture ps table matches nothing; a reaped chain still yields the word-bounded alternation unchanged. FILE SCOPE: rotate.py (_derive_pred_pids), test_rotate*.py. CEILING: <=10 production lines, 1 kid -- re-brief SM past 2x. Template side: nothing (master-sensei)."
title: L4 the no reap pred pids placeholder resolves to a named non matching value never a refusal
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-no-reap-pred-pids-placeholder-resolves-to-a-named-non-matching-value-never-a-refusal

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
