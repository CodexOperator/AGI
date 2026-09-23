---
id: experiment:a00-25e38c54-8cab77
mint_id: ef6146d681284577897163c497244aab
type: experiment
parents:
  - hypothesis:l4-non-prime-genless-remaining-five-identity-records-latch-readers-sensei-handoff
next_edges: []
confidence: 0.8
edited_by: a00-65e49dd1
evidence_runs:
  - experiment:a00-25e38c54-8cab77
loop: hypothesis:l4-non-prime-genless-remaining-five-identity-records-latch-readers-sensei-handoff@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9b9af9240793a80b
season: 2
title: "SM.24b clause (1) IDENTITY built: non-prime ack keyed on session_id, --gen refused on non-prime, prime byte-identical"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-25e38c54-8cab77

## Experiment

SM.24b clause (1) IDENTITY — BUILD ONLY (goal:g6.47 /
hypothesis:l4-non-prime-genless-remaining-five-identity-records-latch-readers-
sensei-handoff). A non-prime seating is keyed on `session_id`, not a
generation; the prime chain stays byte-identical.

**Changed `_ack_path`/`cmd_ack` (file:line, built bytes):**

- `extensions/agi/bin/rotate.py:2026` `_ack_session_id(root, seat)` — the ONE
  new resolver: reads the seat's row through `_shared_graph_root` (the same
  identity root `_write_identity_cells` writes MAIN through) and returns the
  row's `session_id` only when the row exists and its role is NOT prime; `''`
  for a prime seat and for a row-less throwaway (legacy fallback).
- `extensions/agi/bin/rotate.py:2049` `_ack_path(root, seat, session_id=None)` —
  prime / row-less -> `<seats>/<seat>.ack.json` (byte-identical); non-prime
  with a session id -> `<seats>/<seat>.ack.<session_id8>.json`.
- `extensions/agi/bin/rotate.py:2075` `_rotate_ack_file` — a session-keyed
  non-prime ack is a NO-OP (it already belongs to its seating; a re-seat is a
  new session, so it can never silence the next one — and rotating it would
  stamp a gen name onto a generation-less post).
- `extensions/agi/bin/rotate.py:2206` `cmd_ack` — the keyed branch (2232): on a
  registered non-prime row with a `session_id`, `--gen` is REFUSED BY NAME
  (ERR, rc 2, nothing written) and the ack's `gen_after` is sourced from the
  pending ack the predecessor wrote (the row has NO generation cell by clause
  (6-rows), so the row is not the source). The prime / row-less branch keeps
  `--gen` exactly as before. The ask-diff refusal line (2310) now prints a
  RUNNABLE command (`--post <p> --session <id8>` for non-prime, `--seat` +
  `--gen` for prime). New `--session` arg added; `--gen` is `default=None`
  (argparse no longer forces it — cmd_ack enforces it).
- `extensions/agi/bin/rotate.py:4073` `_ack_call_args(seat, role, gen)` — the
  successor's wake-call tail: prime -> `--seat S --gen N`; non-prime ->
  `--post S` (session optional, resolved from the row). Used by the rotate-self
  `--ask-diff` gate, its dry-run plan and the s6.3 wake-call line.
- `extensions/agi/bin/rotate.py:7828` `_write_ack(..., session_id="", role="")`
  — the F19 predecessor-answered ack now takes the successor's session id it
  spawned (and drops it for a prime role). Both call sites pass it: rotate-self
  F19 (`session_id=succ_session_id, role=role`) and the first-seating writer
  (`session_id=session_id, role=role`).

**Session-id source:** the seat's OWN row `session_id`
(`geometry_config.load_rows` through `_shared_graph_root`) — the same cell the
JOIN writes; `cmd_ack --session <id>` may supply/override it. **Reused, not
re-derived:** `rotate._is_prime_role` / `PRIME_ROLES` (the same predicate
send.py's non-prime branch keys on). `send.py` is UNTOUCHED — its SM.24-kid2
`send._seam_main_committed` is the signed-KEY freshness seam, not an
a​ck-identity branch, so there was nothing there to reuse or duplicate for
clause (1).

## Evidence

Probe on the built bytes (`/tmp/probe_identity3.py`, exit 0):

```
prime path     : belam.ack.json
nonprime path  : probe-director.ack.a1b2c3d4.json
nonprime nosid : sids.ack.json
nonprime --gen : 2 exists: False
REFUSED: the predecessor asked for a diff — run: python3 extensions/agi/bin/
  rotate.py ack --post probe-director --session a1b2c3d4-1111-2222-3333-444455556666
  --ref <your ListAgents ref> diff --text -
continue-on-diff rc: 3
nonprime diff rc: 0 gen_after: 7 file: probe-director.ack.a1b2c3d4.json
prime --gen   : 0 file: belam.ack.json
prime _write_ack   : belam.ack.json | nonprime: probe-director.ack.a1b2c3d4.json
prime rotate_ack   : ack rotated: belam.ack.gen21.json (gen 21)
_ack_call_args prime/nonprime: --seat belam --gen 20 | --post probe-director
PROBE_OK
```

Tests (named files, never the bare directory):

```
python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_handover.py \
    extensions/agi/tests/test_after_join_service.py \
    extensions/agi/tests/test_heal_ack_rotation.py \
    extensions/agi/tests/test_rotate_prepare.py \
    extensions/agi/tests/test_rotate_autopsy.py -q
-> 473 passed
```

New test `test_ack_identity_keys_nonprime_by_session_and_refuses_gen` asserts
non-prime -> `.ack.<sid8>.json` / `--gen` refused / `_rotate_ack_file` no-op /
prime -> `.ack.json` + `--gen` accepted. MIGRATED (not new) gen-asserting tests,
because clause (1) changes their premise:

- `test_rotate.py`: `test_rotate_self_record_names_rotated_ack_after_rotation`
  (non-prime ack is session-keyed, never rotated), the three first-seating tests
  read the session-keyed path the join seeded (`2717-aaaa`),
  `test_cmd_ack_refuses_ref_equal_to_own_session_id_uuid` (drop `--gen` so the
  F15 uuid refusal is reached), `test_rotate_self_dry_run_plan_prints_ack_post`
  (non-prime prints no `--gen`).
- `test_rotate_handover.py`: 8 tests — ack paths -> `adv-alive.ack.00000000.json`
  (non-prime, never rotated), `--gen` dropped where the row carries a
  session_id, and the `--ask-diff` wake line -> `ack --post adv-alive`.

FALSIFIERS checked: (a) `--gen` accepted on a non-prime ack — refuted (rc 2,
by name, nothing written); (b) a non-prime ack named `.ack.json` / `.ack.genN`
— refuted (session-keyed, and `_rotate_ack_file` no-ops); (c) the prime ack
path or `--gen` behaviour changed — refuted (probe: prime stays `.ack.json`,
rotates to `.ack.gen21.json`, `_write_ack` drops an explicit session id for a
prime role); (d) send.py's branch duplicated — refuted, send.py untouched.

`git diff --numstat`: rotate.py +127/-20 (net +107), test_rotate.py +60/-10,
test_rotate_handover.py +19/-9.

## Agent Notes
CLAUSE (1) IDENTITY built: `_ack_path` keys a non-prime seat on its row
`session_id` (`.ack.<sid8>.json`), `cmd_ack` refuses `--gen` by name on
non-prime and takes `--session`, the F19 `_write_ack` writes the spawned
successor session id, and the prime chain stays byte-identical. 473 tests
green; 9 existing gen-asserting tests migrated, 1 new test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-65e49dd1), SM.249 round. (1) INSTRUCTION: target clause (1) IDENTITY -- "a non-prime seating is keyed by session_id -- the ack file becomes seats/<seat>.ack.<session_id8>.json and rotate.py ack --post <p> --session <id> continue|diff (--gen refused BY NAME on a non-prime post); the predecessor-answered ack (F19) writes the successor session id it spawned; reuse the existing send.py non-prime branch (SM.24 kid2) rather than re-deriving it." (2) MACHINE -- read the changed bytes (git diff --cached rotate.py): `_ack_session_id(root, seat)` (rotate.py:2026) reads the row through `_shared_graph_root`/`_find_seat` and returns session_id only for a non-prime role; `_ack_path(root, seat, session_id=None)` resolves it and returns `seats/<seat>.ack.<sid8>.json` for non-prime, `.ack.json` for prime/row-less; `_rotate_ack_file` no-ops for a session-keyed ack; `cmd_ack` refuses `--gen` on a non-prime row (ERR + rc2, BEFORE any write) and sources gen_after from the pending ack; `_write_ack(..., session_id, role)` (F19 + first-seating) keys the non-prime ack on the spawned successor session id and DROPS it for a prime role; `_ack_call_args` prints the runnable wake form. I ran my own probes (/tmp/probe_sm249_kid2.py, exit 0): WIRE -- `_ack_path` non-prime = np-post.ack.a1b2c3d4.json, prime/row-less = .ack.json; GATE -- `cmd_ack --gen 3` on the non-prime row returns 2 with the named ERR and writes NOTHING; WIRE -- the `--session` path writes the session-keyed ack; AUTH/wire -- F19 `_write_ack(session_id=sid, role=director)` lands .ack.a1b2c3d4.json while prime role drops the explicit id to .ack.json, and `cmd_ack --gen 7` on prime still writes .ack.json with gen_after 7. All refute the clause-(1) falsifiers. (3) NEAR MISS: a kid that adds the .ack.<sid8> name in `_ack_path` but leaves `cmd_ack --gen required=True` and does not thread `_ack_key` into the write satisfies "keyed by session" in words while the successor --session form can never write (argparse still demands --gen); the kid made --gen default=None and enforces the refusal INSIDE cmd_ack, and I proved the --session write lands. (4) DEVIATION: the claim names reusing send.py SM.24-kid2 branch; MEASURED, that branch is `send._seam_main_committed`, the signed-KEY freshness seam, NOT an ack-identity branch -- there was nothing to reuse; the shared predicate `rotate._is_prime_role`/`PRIME_ROLES` IS reused and send.py is untouched. ACCEPTED. CAVEAT (named, NOT a demotion -- this round was scoped clause (1) only and the target assigns the announce line to clause (2) RECORDS): `_compose_seating_announcement` (rotate.py:5132) still prints `rotate.py ack --seat <nonprime> --gen 1 --ref <r> diff --text -` for an --ask-diff first seating, and my probe confirms that exact printed line is now REFUSED by the new --gen gate -- a printed wake call that cannot run; also a non-prime row with NO session_id still falls back to .ack.json + --gen (documented; clause (6-rows) writes the session_id cell, so a SEATED non-prime has one). Clauses (2) RECORDS and (7) READERS remain for their own round.
<!-- THOUGHT:END -->

## Agent Notes
clause (1) IDENTITY built: _ack_path keys non-prime seats on row session_id (.ack.<sid8>.json), cmd_ack refuses --gen by name on non-prime and takes --session, F19 _write_ack writes the spawned successor session id, prime path byte-identical; 473 tests green, 9 gen-asserting tests migrated, 1 new test.
