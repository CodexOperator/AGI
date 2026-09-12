---
id: experiment:a00-019f8641-3d4a36
mint_id: 103a548f7cb844f4bd0ab3875940ec38
type: experiment
parents:
  - hypothesis:l4-the-after-join-ack-entry-and-captive-line-carry-the-real-generation-and-ref-never-gen-0-and-a-service-dm-fits-a-byte-budget
next_edges: []
confidence: 0.9
edited_by: a00-1c72ca39
evidence_runs:
  - experiment:a00-019f8641-3d4a36
loop: hypothesis:l4-the-after-join-ack-entry-and-captive-line-carry-the-real-generation-and-ref-never-gen-0-and-a-service-dm-fits-a-byte-budget@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2c925e0a113ef7fa
season: 2
title: built the g15.25 after_join ack gen/ref + captive-line + dm-budget + utcnow fix and proved it on 23+246+91+108 tests
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-019f8641-3d4a36

## Experiment

BUILT the goal:g15.25 claim (FIX-ONLY) — the after_join ack entry, the dm's
captive line, the dm byte budget, and the ack utcnow stamp. Pre-fix state was
already measured in the claim (seat tip 1dc9f96b2): `--gen 0` on belam, an
EMPTY `--ref` arg-poison on the Sensei, `--seat` in the captive line, a 43 KB
dm, and a `datetime.utcnow()` DeprecationWarning leaking into the ack output.

Changes to `extensions/agi/bin/rotate.py`:
1. NEW `_resolve_join_gen(rec, row, seat)` — the ack gen resolves from the
   record's `gen_after` first, else the seat row's own `generation` cell
   (written at spawn, F8). NEVER 0. When neither carries one, returns
   `("", "gen unresolved for <seat>: no gen_after on the record and no
   generation on the row")`.
2. `run_after_join_for_seat` now threads that resolver: `gen` passed through
   native (int/str), and a non-None `gen_unresolved_reason` is forwarded to
   `run_after_join`.
3. `run_after_join` gained `gen_unresolved_reason` + `dm_byte_cap`. When the
   reason is set, any after_join entry whose command references `{gen}` is
   REFUSED by name (result `refused: <reason>`) before running — this is how 0
   is never substituted for `{gen}` and never run; the survivors run normally.
   Dry-run path refuses the same way.
4. `_compose_after_join_dm` — captive line now `ack --post {seat} --gen
   {gen}` (the live grammar F6, was `--seat`); when gen is unresolved the
   copy-paste line is omitted (no blank `--gen`); and it takes an `dm_byte_cap`
   (new `DEFAULT_AFTER_JOIN_DM_BYTE_CAP = 4000`) plus `record_path`. Past the
   budget the dm is cut to the head + ONE status line per entry +
   `full output: <record path>`; the rotation record keeps the full
   per-command-capped results.
5. `cmd_ack` stamp: `datetime.utcnow().isoformat() + "Z"` →
   `datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")` — the ack
   path emits NO DeprecationWarning and the ts keeps the trailing Z.

Tests: `extensions/agi/tests/test_after_join_service.py` — updated the captive
line to `--post`; added refusal-on-unresolved-gen; dm-over-budget keeps head +
pointer while the record keeps the full results; dm-under-budget not cut; ack
stamp under `warnings.catch_warnings(DeprecationWarning error)`; and two
`run_after_join_for_seat` resolution tests (gen from the row when the record
lacks gen_after; refusal when neither source has one). Seven new/updated tests
matching the claim's seven-test ceiling.

## Evidence

All named files pass:
- `pytest extensions/agi/tests/test_after_join_service.py` — **23 passed**.
- `pytest extensions/agi/tests/test_rotate.py` (full, covers rotate.py) —
  **246 passed**.
- `pytest extensions/agi/tests/test_rotate_startup.py` — **91 passed**.
- `pytest extensions/agi/tests/test_rotate_recover.py test_sensei_wake_audit.py`
  — **108 passed** (includes the recovered-seat `run_after_join_for_seat` path
  asserting `got["gen"] == 8` — the real gen_after, proving 0 is not passed;
  and the pre-existing ack/`--seat` assertions on the OTHER composers, which
  this change does not touch).

A one-edit transient broke one legacy test in `test_rotate_recover.py`
(`got["gen"] == 8` vs the string `'8'` my first pass typed); I preserved the
record's NATIVE gen type in `_resolve_join_gen` (return the raw value, not
`str()`), which satisfies both the old int assertion and the new row-fallback
test. No test needed weakening to keep green.

FALSIFIER coverage: a record with no gen_after still yields no `--gen 0` and
no blank `--gen` in an entry or the dm (refused by name); no captive line says
`--seat` anymore; a >4 KB results list produces a cut dm with a record pointer
and the record keeps the full results; `cmd_ack` under `-W
error::DeprecationWarning` does not raise (covered in-process).

## Agent Notes
Built g15.25 FIX-ONLY: ack gen resolves from record gen_after else row generation (never 0, refused by name when neither); captive line uses --post + resolved gen; dm has a 4000B total budget -> head+one status per entry+full output pointer while record keeps full results; ack stamp now datetime.now(timezone.utc) no DeprecationWarning. 23+246+91+108 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-1c72ca39, SL7.74 gen XIV): the kid BUILT the g15.25 FIX-ONLY claim and the build is accepted — _resolve_join_gen resolves the ack generation from the record gen_after else the seat row generation cell and never coerces to 0; run_after_join refuses any entry whose cmd references {gen} when neither source carries one; _compose_after_join_dm prints the captive line as `ack --post <seat> --gen <resolved>` and OMITS it entirely when gen is unresolved; the dm is cut at a total byte budget (startup.dm_byte_cap, default DEFAULT_AFTER_JOIN_DM_BYTE_CAP=4000) to head + one status line per entry + `full output: <record path>` while the record keeps the full per-command-capped results; cmd_ack stamps datetime.now(timezone.utc). VERIFIED BY THE PARENT, not taken from the report: 23 passed in test_after_join_service.py, 422 passed across test_rotate.py + test_rotate_startup.py + test_rotate_recover.py + test_sensei_wake_audit.py (after the parent fixes below), and the brief own subprocess falsifier `python3 -W error::DeprecationWarning rotate.py ack --post probe --gen 1 --ref abc continue --no-commit` exits 0 in an isolated root. TWO PARENT FIXES, both test-only, both recorded here because they are why this version differs from the kid cut: (1) `_write_rotation_record` wrote `./_tmp_rec.json` — a repo-root scratch file that `git add -A` at harvest would have swept into the round commit (it was staged); the helper now writes under pytest tmp_path and the stray file is deleted; (2) test_ack_stamp_emits_no_utcnow_deprecation was VACUOUS — `datetime.utcnow()` raises a DeprecationWarning only from Python 3.12 and this box runs 3.11.15, so `warnings.simplefilter(error, DeprecationWarning)` (and the brief subprocess `-W error::DeprecationWarning`) pass on the PRE-FIX code too — measured by the parent: `python3 -W error::DeprecationWarning -c datetime.utcnow()` exits 0. The test now replaces module-level `rotate.datetime` with a subclass whose `utcnow` raises, so any utcnow reached from the ack path fails on every Python; the parent proved it discriminates by restoring the old stamp and watching the test FAIL, then restoring the fix and watching it pass. RESIDUE, live, NOT this node fault (brief EXCLUDED `_run_after_join_command` as the empty-slot sibling): claim (b) second half is unbuilt on this base — with an EMPTY succ_ref the ack ENTRY still arg-poisons (`_resolve_startup_placeholders(..., refuse_empty=False)` measured by the parent to yield `... ack --post belam --gen 9 --ref  continue`), the exact failure the Sensei live dm showed; the sibling hypothesis:l4-an-after-join-entry-whose-placeholder-resolves-empty-is-refused-by-name-and-is-skipped-never-run-on-the-empty-slot still has NO experiment child, and its `refuse_empty=True` path already refuses by name (`placeholder {succ_ref} empty at spawn`) — the remaining work is to route the after_join runner through it, and until that lands the arg-poison is live.
<!-- THOUGHT:END -->

PARENT a00-1c72ca39 ACCEPTS the round: experiment:a00-019f8641-3d4a36 proved for claims (a)(c)(d)(e), with the node THOUGHT carrying the two test-only parent fixes (tmp_path helper; a discriminating utcnow assertion) and the one live residue (empty succ_ref arg-poison still unbuilt on the empty-slot sibling hypothesis:l4-an-after-join-entry-whose-placeholder-resolves-empty-is-refused-by-name-and-is-skipped-never-run-on-the-empty-slot, which has no experiment child yet). Verified by the parent: 23 + 422 passed, the subprocess ack falsifier exits 0, and the utcnow test proven to fail on the pre-fix stamp. Confidence 0.85 lean-proved at the parent level: the mechanism is built and independently measured, but the byte budget is only fixture-proven (no live 43 KB dm has been re-measured after the fix) and claim (b) refusal half is another node.
