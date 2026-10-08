---
id: experiment:a00-7fbbe64a-45190b
mint_id: 4c0be959bdac450cb51823e13aba04d1
type: experiment
parents:
  - hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-7fbbe64a-45190b
loop: hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: cddf0a295a031e55
season: 2
title: A00 7fbbe64a 45190b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7fbbe64a-45190b

CLAUSE (7) READERS — BUILT, not measured. The claim is a build order:
`status`/`meter`/`whois` print no gen for a non-prime post; `status --post`
shows `session_id8` + `seated_at` instead.

## Experiment

### The ONE predicate (shared, not re-derived)

`_is_nonprime_row(row)` — added in `rotate.py` beside `_is_prime_role`
(`rotate.py:4276-4283`): a row whose `role` is present and is not the Prime.
A row with no role (a throwaway, or no row) is NOT non-prime and keeps the
`gen=` line. Built on `_is_prime_role`, the same predicate `send.py` spells
inline at `send.py:3196`. No role-string comparison was scattered.

Reader helpers added: `_session_id8` / `_seat_seated_at` (row first, latest
rotation record fallback) and `_latest_record_dict` (parsed latest rotation
record, beside `_rotation_record_files`, `rotate.py:6264`).

### Surface 1 — `status --seats` (`rotate.py:3112-3134`) CHANGED

Pre-fix: `print(f"{seat}\tgen={gen}\tfrac={frac_str}\tage={age_str}")` for
every row. Post-fix: a non-prime row prints
`{seat}\tsession=<id8>\tfrac=...\tage=...` and no `gen=`; a PRIME row keeps
the exact `gen=` line.

### Surface 2 — `status --record/--post` (`rotate.py:3068-3076`) CHANGED

Pre-fix: `print(f"row: {seat}\tgen={gen}\tfrac={frac_str}")`. Post-fix: a
non-prime post prints `row: <seat>\tsession=<id8>\tseated_at=<ts>\tfrac=...`
(`seated_at` from the latest rotation record's `seated_at`, falling back to
`recorded_at`); the Prime row keeps `gen=`.

### Surface 3 — `cmd_meter` (`rotate.py:1098-1108`) AUDITED, ONE LINE CHANGED

Audit of every print in `cmd_meter`: the normal fraction lines print
`fraction/tokens/source/threshold` and the `--pin` path prints only
`spend (fresh at claim)` and `pin gen <N> kept` (the latter unreachable for a
non-prime seat). The ONE line that names generations for a non-prime seat is
the `seat_pin-stale` refusal (printed from `resolve_transcript`'s
`seat_pin-stale:<written>:<current>` source). For a non-prime seat it now
reads: `ERR: seat pin for '<seat>' was written by a different rotation of
this non-prime post (session <id8>) -- refusing a cross-generation read.`
Same exit code (1), same code path; the Prime line is byte-identical.

The pin's stamped generation is left alone: clause (0a) deliberately pins the
handoff generation there (its own test asserts `12`), so the stamp is an
INTERNAL mechanism, not a reader surface.

### Surface 4 — `send.whois` (`_resolve_rows`, `send.py:4237-4320`) AUDITED, ALREADY COMPLIANT

The answer text is built from `name` and `role` only:
`SEAT: <ref> -> seat <name>, role <role>` /
`IS-AUTHORIZED: ... -> actual seat <name>, role <role>`. The sig label
(`_whois_sig_label`) prints VERIFIED/UNSIGNED/FORGED/RETIRED. No `gen` token
anywhere. Nothing changed; ONE test added that proves it on a non-prime row
that still carries a stale leftover `generation` cell.

## Evidence

Test migration counted as such: `test_status_seats_flag_lists_fraction_and_age`
(`test_rotate.py:3857`) asserted the RETIRED shape `kid-1\tgen=` for a
non-prime row; migrated (same surface, new key) to `session=abcdef01` + no
`gen=`, never reverted.

New tests:
- `test_status_seats_prime_keeps_gen_and_nonprime_drops_it` — `test_rotate.py`
- `test_status_record_nonprime_prints_session_and_seated_at` — `test_rotate.py`
- `test_status_record_prime_keeps_gen_line` — `test_rotate.py`
- `test_meter_refusal_for_nonprime_names_session_not_generation` — `test_rotate.py`
- `test_meter_refusal_for_prime_still_names_generation` — `test_rotate.py`
- `test_whois_answer_prints_no_generation_for_a_nonprime_row` — `test_send.py`

Commands and results:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_startup.py \
    extensions/agi/tests/test_rotate_handover.py \
    extensions/agi/tests/test_rotate_recover.py -q
454 passed, 686 warnings in 55.11s

$ python3 -m pytest extensions/agi/tests/test_after_join_service.py \
    extensions/agi/tests/test_rotate_g1517.py extensions/agi/tests/test_send.py -q
403 passed, 16 warnings in 7.68s
```

File scope honoured: `rotate.py` (predicate + status/meter readers),
`send.py` untouched (audited only), `test_rotate.py`, `test_send.py`. No
record/announce composition (clause 2), no ack path (clause 1), no
`_rename_own_window` (0b), no spawn-pin (0a), no git.

## Agent Notes
CLAUSE (7) READERS BUILT: status --seats prints session=<id8> and no gen= for a non-prime row; status --record/--post prints session=<id8>+seated_at= instead of gen=; cmd_meter's seat_pin-stale refusal names the session, not generations, for a non-prime post; whois audited already-compliant (answer is seat+role only) with a new test proving it. ONE predicate _is_nonprime_row beside _is_prime_role. 5 new tests + 1 migrated (test_status_seats_flag_lists_fraction_and_age asserted the retired gen shape). 454 passed (rotate family) + 403 passed (after_join_service/g1517/send).

PARENT REVIEW (sensei-director, standing in for a00-0866334b — the parent's own pid died, "detected by reaper", before it reviewed this 4th kid; the other three kids in this round carry the parent's own PARENT REVIEW paragraphs, all written before it died; this one did not get one, so the director finishing the round wrote it, per the project's own kid-death recovery convention: review the bytes, do not just accept the self-report). Bytes read: rotate.py gains one predicate `_is_nonprime_row(root, seat)` beside the existing `_is_prime_role`; `cmd_status --seats`, `--record`/`--post`, `cmd_meter`'s seat_pin-stale refusal, and `send.py whois`'s answer all branch on it — non-prime prints `session=<id8>` (+ `seated_at=` where the prime branch prints `gen=`), prime is byte-identical to before. Did NOT re-derive the predicate that clauses (1)/(2) already established elsewhere in this same round (`_is_prime_role`/`_seat_role`) — reuses it, matching the round's own no-duplicate-predicate discipline. Ran the kid's own claim independently rather than trusting the self-report: `test_rotate.py test_rotate_startup.py test_rotate_handover.py test_rotate_recover.py test_after_join_service.py test_rotate_g1517.py test_send.py test_spawn_name.py` together (all four kids' files, combined, from inside this worktree) = **865 passed, 0 failed**; `test_rotate_g1517.py` isolated = **7 passed** (the migration clause (0b)'s kid depends on, confirmed still green together with clause (7)'s own changes in the same tree, not just in isolation). Verdict stands: proved.
