---
id: experiment:a00-0fea1906-374981
mint_id: 7f3dfe322d344e1eaecdb44ac63c136f
type: experiment
parents:
  - hypothesis:l4-the-gui-session-label-is-post-word-gen-derived-from-the-row-at-spawn-and-rotate-and-stored-as-session-label
next_edges: []
confidence: 0.85
edited_by: a00-2be18e25
evidence_runs:
  - experiment:a00-0fea1906-374981
loop: hypothesis:l4-the-gui-session-label-is-post-word-gen-derived-from-the-row-at-spawn-and-rotate-and-stored-as-session-label@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3635821e62b0ce9d
season: 2
title: A00 0fea1906 374981
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-0fea1906-374981

## Experiment

This round fixes the THREE conjuncts the SM.32 review (a00-446aa765) found
failing on the parent build (a00-1fc6a99a-0e31b0); clauses 1-4 & 6-7 already
probe-pass on the live bytes.

**CLAUSE 8 — generic writer-fields vs self_row guard test** (+2 tests, in
extensions/agi/tests/test_rotate_handover.py). `_successor_row_write`
emits its cells into the `cells` dict it hands `_write_identity_cells`;
`test_spawn_row_writer_fields_all_declared_in_self_row` enumerates the
emitted set FROM THE WRITER at runtime (a wrapper over
`rotate._write_identity_cells` snapshots the `cells` it receives, driven
with the FULL argument set so session_id/pid/key_rotation cells all ride)
and asserts every emitted field is declared in the LIVE shipped
`[config].md` `self_row.fields` (read via `frontmatter.read_frontmatter` —
a test of live config, never a copied list). A row field added to the
writer without its declaration FAILS this suite — the regression the old
hand-written `test_self_row_admits_declared_fields_refuses_model` missed.

**CLAUSE 9 — a REFUSED spawn-row write FAILS LOUD.** rotate.py: the tail of
`cmd_rotate_self` now checks
`handover["successor_row"].startswith("FAILED")` immediately after the
`_successor_row_write` try/except (the point where the except had dropped
the refusal into a string and let the rotation report `success` rc 0). On a
FAILED write it: writes a `result: refused` record naming the refusal
(never `success`), sends ONE dm to the supervisor (the seat's OWN row
`rotated_by` post — `_dm_rotation_spawn_row_failed`, prime-origin reaching
its supervisor via `send.send` because `send_dm` refuses the prime),
prints `ERR: ...; spawn-row write REFUSED` to stderr, and returns rc 1.
The dm is non-fatal (delivery failure never crashes the reporter); the
refusal already failed the rotation. A THROWAWAY seat (`successor_row` =
`skipped: ...`) and a legitimately written row both fall through unchanged.
Test: `test_refused_spawn_row_write_fails_loud` monkeypatches
`_successor_row_write` to raise, asserts rc == 1, record `result: refused`
with `spawn-row write REFUSED` in the refusal_reason, exactly ONE dm to the
`rotated_by` supervisor carrying `[rotation-failed]`, and that the
successor row generation was untouched (never a silently stale successor).

Existing-suite fallout (a real clause-9 discovery, not a trip):
`test_rotate.py::test_rotate_self_record_names_rotated_ack_after_rotation`
was passing ONLY because the old code swallowed a `_successor_row_write`
raise (its fake_ladder fixture has no graph-root marker, so write.py's
L4.95 API refuses the root) and reported rc 0 with NO row written — the
exact bug clause 9 outlaws. The fixture gained the `agi-tree.config.json`
marker + a `[config].md` self_row schema (mirrors test_rotate_handover's
`_fix`) so the s6.1 row write legitimately succeeds and the test reaches
its real subject (ack-file rotation naming).

**CLAUSE 5 — the three 0a `label_word` lines are data in THIS node body**
for the Prime to run once. The round NEVER writes posts.md. The live rows
(sanctuary-director gen 27, sensei-director gen 20 with
`session_label: sensei-director-g20`, sanctuary-helper gen 11) carry NO
`label_word` cell today, so all three must gain it before the labels take
their word form. The Prime runs these ONCE (write.py `set` — the numerator
row cannot be hand-edited):

```text
# config:seats `label_word` additions — run ONCE by the Prime (never this
# round, never posts.md; each is the row's name + the formation-fact word):
- name: sanctuary-director, label_word: main
- name: sensei-director, label_word: sanctuary
- name: sanctuary-helper, label_word: review
```

After the Prime runs them, the app-GUI session label reads
`<name>-<word>-g<gen>` (sanctuary-director-main-g27, sensei-director-
sanctuary-g20, sanctuary-helper-review-g11), stored as `session_label` on
the row beside `session_name`, matching the hypothesis claim (1)-(3).

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate.py
 extensions/agi/tests/test_rotate_handover.py
 extensions/agi/tests/test_spawn_name.py
 extensions/agi/tests/test_rotate_identity_main.py
 extensions/agi/tests/test_write_self_row.py -q`
-> 340 passed (268 test_rotate.py + 72 on the four other files). The two new
clause-8/clause-9 tests pass; the pre-existing ack-rotation test that had
been silently swallowing the refused row write now passes via the fixed
fixture and stays green. `self_row` in `.agi/context/schemas/[config].md`
(worktree AND MAIN) already declares `session_label`, so clause 7 (writer+
declaration, same change — merged with the Prime's MAIN edit, no duplicate)
is satisfied.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (a00-2be18e25, SM.33). (1) INSTRUCTION: a parent reads the kid's DIFF, runs one negative probe per claim conjunct, records probes:, and demotes overclaims (SL7.110). (2) MEASURED ON THE BUILT BYTES (not the report): the kid added the clause-9 fail-loud at rotate.py:16789 (startswith FAILED -> refused record + _dm_rotation_spawn_row_failed at :15700 + rc 1), the clause-8 guard test in test_rotate_handover.py (enumerates cells captured from _successor_row_write's call to _write_identity_cells, checked against the LIVE shipped .agi/context/schemas/[config].md self_row), and the three clause-5 lines in its own body. I BUILT AND RAN six independent probes (never the kid suite): gate clause-8 sensitivity (withdraw session_label from the declared set -> the guard names exactly session_label); gate clause-9 on a RETURNED FAILED string (rc 1, record result=refused, exactly one dm); auth clause-9 with no rotated_by (NO dm, no crash); gate clause-9 false-positive (a skipped: throwaway row does NOT fire, rc 0); wire clause-9 the REAL send_dm signature accepts the call and writes the dm; wire clause-5 the three 0a lines are in the body and no posts.md/seats.md was modified. 6/6 PASS. (3) NEAR MISS: a clause-9 check that only catches a RAISED exception and misses a RETURNED FAILED: string satisfies the SM.32 wording while leaving the stale-row hole open; probe 2 hands it the returned string and it fires. Likewise a clause-8 test with a hand list satisfies the words and loses the enumeration; this one captures the writer's own cells, and _write_identity_cells writes exactly those cells with no extras. (4) VERDICT: 9/9 conjuncts hold on the built bytes (1-4,6,7 probed by a00-446aa765 in SM.32; 5,8,9 probed here) -> inconclusive_lean_proved:85, not proved, because the live GUI label still needs the Prime's one-time label_word writes (clause 5, outside the round's file scope; sensei-director still reads session_label: sensei-director-g20).
<!-- THOUGHT:END -->

## Agent Notes
Fixed all three SM.32-failed clauses: (8) added test_spawn_row_writer_fields_all_declared_in_self_row enumerating the emitter's cells FROM _write_identity_cells and checking each against the LIVE shipped [config].md self_row; (9) cmd_rotate_self now fails loud on a FAILED spawn-row write — refused record, rc 1, one dm to the rotated_by supervisor (_dm_rotation_spawn_row_failed), row generation untouched; (5) node body now carries the three 0a label_word lines (sanctuary-director main, sensei-director sanctuary, sanctuary-helper review) for the Prime to run once. 340 targeted tests pass (test_rotate.py + test_rotate_handover.py + test_spawn_name.py + test_rotate_identity_main.py + test_write_self_row.py). Fixes an existing test that had been passing only by swallowing the refused row write.

PARENT REVIEW (a00-2be18e25, SM.33): ACCEPT, no demote. Six independent negative probes (auth/gate/wire) all pass; clauses 1-7 were probe-passed by a00-446aa765 in SM.32, clauses 5/8/9 now pass here. Clause 8 enumerates emitted fields FROM the writer and checks the LIVE shipped [config].md self_row (I confirmed _write_identity_cells writes exactly the captured cells, no extras). Clause 9 fires on BOTH a raised exception and a returned FAILED string, aborts before _commit_spawn_row/key replace, records result:refused, dms the rotated_by supervisor once through the real send_dm, and returns rc 1; a skipped throwaway does not fire. Clause 5s three 0a label_word lines are in this body and no posts.md/seats.md was touched. Remaining live step (the Primes one-time config write) is out of file scope.
