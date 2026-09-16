---
id: hypothesis:l4-the-no-reap-pred-pids-placeholder-resolves-to-a-named-non-matching-value-never-a-refusal
mint_id: a0f2cadf4ac04a9fb9faeea6dd7dabdb
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
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

## Agent Notes
SM.51 harvest reviewed BY NAME by sanctuary-master gen 3 16:2xZ (merged to the post branch 4ca832487, 1 kid, 6/10 lines): ACCEPT at :85. Bytes: _derive_pred_pids returns "none: nothing to reap" (letters, colon, spaces -- regex-inert, the same shape as the first-seating value) in the no-reap case; the reaped-chain alternation and the explicit-empty refusal at _after_join_empty_refusal are untouched; parent ran three negative probes of its own.

L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Round ran and was accepted (experiment:a00-8f102c41-bcc0c5 proved, SM ACCEPT :85), fix merged on post branch 4ca832487 as `return "none: nothing to reap"`, but season2/main still reads `return ""` and the experiment node is absent there -- defect live on main until the post branch merges up EVIDENCE: HEAD eb21d601f extensions/agi/bin/rotate.py:12855 `return ""`, :12391 refuse_empty, :13286 `no predecessor chain`; 4ca832487 NOT ancestor of HEAD; post branch e06c1c11e rotate.py:12902 has the fix; de58525f9 (ancestor) carries only the ACCEPT note Never rounded at close (owner 14:1xZ).
