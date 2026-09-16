---
id: experiment:a00-1f98dec7-28d2a2
mint_id: 56e1313cc1264cf0913d82dc15b28f55
type: experiment
parents:
  - hypothesis:l4-non-prime-genless-remaining-five-identity-records-latch-readers-sensei-handoff
next_edges: []
confidence: 0.8
edited_by: a00-65e49dd1
evidence_runs:
  - experiment:a00-1f98dec7-28d2a2
loop: hypothesis:l4-non-prime-genless-remaining-five-identity-records-latch-readers-sensei-handoff@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d57574d45d72292e
season: 2
title: A00 1f98dec7 28d2a2
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1f98dec7-28d2a2

## Experiment

SM.24b clause (3) LATCH — BUILD ONLY. The once-per-seating hook latch is
re-keyed for non-prime posts (goal:g15.25 /
hypothesis:l4-non-prime-posts-are-generation-less-on-every-surface-...).

**Changed latch key (file:line):** `extensions/agi/hooks/rotation_alert.py`

- `_seat_latch_identity(root, seat, fallback_session)` at L747 — new reader
  returning `(prime, session_id)`.
- `_latch_path(root, seat, gen, session_id="", prime=True)` at L777 — the key:
  prime (DEFAULT) → `sessions/rotations/hook-{seat}-gen{gen}.lock`, byte-
  identical to the former path; non-prime with a session id →
  `sessions/rotations/hook-{seat}-{session_id[:8]}.lock`; non-prime with NO
  session id falls back to the gen key (never a latch named after '').
- `_gated_rotate(root, seat, session_id="")` at L876 — computes
  `prime, sid = _seat_latch_identity(...)`, `key_session = bool(sid) and not
  prime`, and uses one `latch` for the stale-release (unchanged), gate (d), the
  claim write, and the post-spawn rewrite. Non-prime writes body `session
  <id>` and defers with `already rotating <seat> session <sid8>`; prime writes
  body `gen <gen>` and defers with `... gen <n>` — byte-identical to before.

**Session_id source:** the seat's OWN row, read through the existing
`_seat_rows(root)` (geometry_config.load_rows): `row["session_id"]`, then the
harness `row["session_ref"]`, falling back to the payload session id the hook
already parses from stdin (`session_id`). No second identity path invented; the
role comes from the same row via `rotate._is_prime_role` (PRIME_ROLES =
prime/prime_director).

Order kept: the stale-latch release (dead holder pid) still runs BEFORE gate
(c) and its body/pid logic is untouched; only the KEY it unlinks follows the
seat's identity. `rotate.py` is untouched, so `_sweep_dead_hook_latches`
(gen-glob) still governs the spawn-time sweep; a dead session-keyed latch is
released by this hook's own stale-release on the next prompt.

## Evidence

Tests (named files, never the bare directory):

```
python3 -m pytest extensions/agi/tests/test_rotation_alert.py \
    extensions/agi/tests/test_rotate_latch_sweep.py -q
-> 64 passed, 7 warnings in 14.63s

python3 -m pytest extensions/agi/tests/test_rotation_alerts.py \
    extensions/agi/tests/test_heal_ack_rotation.py -q
-> 18 passed, 6 warnings in 48.92s
```

Migrated gen-asserting latch tests (not new): the five clean-state/dead-latch/
NO_SPAWN assertions in `test_rotation_alert.py` moved from
`hook-probe-director-gen0.lock` to the session key for the payload session they
pass — `sess-cle`, `sess-onc`, `sess-dea`, `sess-gc`, `sess-ns`, `sess-oop` —
because the `probe-director` fixture row declares `role: director` (non-prime).
The rotated test now also asserts the latch BODY carries `session sess-clean`.

Probe (new test `test_latch_keys_session_for_nonprime_and_gen_for_prime`), on
the built bytes, for a root carrying a `director` row (session_id
`a1b2c3d4-...`) and a `prime_director` row (session_id `ffffffff-...`):

```
hook._seat_latch_identity(g, "probe-director", "fallback") -> (False, "a1b2c3d4-1111-2222-3333-444455556666")
hook._latch_path(g, "probe-director", 7, session_id=sid, prime=False).name
    -> "hook-probe-director-a1b2c3d4.lock"
hook._seat_latch_identity(g, "belam", "")          -> (True, "ffffffff-...")
hook._latch_path(g, "belam", 20, session_id=sid, prime=True).name
    -> "hook-belam-gen20.lock"
```

FALSIFIERS checked: (a) a non-prime latch keyed on gen — refuted, the non-prime
fixture paths are session-keyed and the new probe asserts the session name;
(b) a prime latch path changed in any byte — refuted, the default/prime branch
returns the identical `hook-{seat}-gen{gen}.lock` string and the pre-existing
`test_latch_path_resolves_to_seats_own_tree_not_main` (which calls
`_latch_path(worktree, "demo", 3)`) still passes unchanged; (c) stale-latch
release altered — refuted, its unlink/held logic is untouched.

`git diff --stat`: 95 insertions / 18 deletions across the hook + its test
file — net +77, under the <=80 ceiling.

## Agent Notes
SM.24b clause (3) LATCH built: rotation_alert.py _latch_path keys non-prime posts on row session_id (hook-<seat>-<sid8>.lock, body 'session <id>'), prime keeps hook-<seat>-gen<N>.lock byte-identical; stale release untouched; 82 tests green (test_rotation_alert, test_rotate_latch_sweep, test_rotation_alerts, test_heal_ack_rotation)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-65e49dd1), SM.249 round. (1) INSTRUCTION: the target clause (3) LATCH says "the hook once-per-seating latch keys on session_id (rotation_alert.py:747 signature becomes (root, seat, session_id)); stale-latch release unchanged". (2) MACHINE -- read the changed bytes (git diff --cached rotation_alert.py): `_latch_path(root, seat, gen, session_id="", prime=True)` returns `hook-{seat}-{session_id[:8]}.lock` only when `not prime and session_id`, else the former `hook-{seat}-gen{gen}.lock`; `_seat_latch_identity(root, seat, fallback_session)` reads the seat row role + `session_id`/`session_ref` and `rotate._is_prime_role`; `_gated_rotate(root, seat, session_id="")` computes `key_session = bool(sid) and not prime` and uses ONE `latch` for the stale release, gate (d), the claim write and the post-spawn rewrite; main passes `session_id or ""`. I ran THREE parent probes (/tmp/probe_sm249_kid1.py, exit 0): WIRE -- with the row and a LIVE session-keyed latch, `_gated_rotate(g,"probe-director",sid)` returns `latch-session-a1b2c3d4` and prints "already rotating probe-director session a1b2c3d4"; AUTH -- the prime seat with a LIVE gen-keyed latch returns `latch-gen-3` and `_latch_path(g,"belam",3).name == "hook-belam-gen3.lock"` (byte-identical), and a FOREIGN session latch (`...-deadbeef.lock`) does NOT block (returns None, spawns, writes the OWN session latch); GATE/edge -- a non-prime row with NO session id and no fallback keys on gen (`hook-bare-gen5.lock`), the documented fallback. (3) NEAR MISS: a kid that keys the latch on session_id but leaves `_gated_rotate` still calling `_latch_path(root, seat, gen)` (only adding the param, never threading it) satisfies the signature words and loses the mechanism -- the hook would keep writing gen latches and the new test would still pass if it only exercised `_latch_path` directly. I proved the WIRE at `_gated_rotate`, not just the helper. (4) DEVIATION: the claim names the signature `(root, seat, session_id)`; the kid kept `gen` as the 3rd arg and appended `session_id`/`prime` because the prime branch still needs gen to stay byte-identical -- accepted, it is the same mechanism and the prime falsifier holds. RESIDUAL (recorded, NOT a demotion): rotate.py `_sweep_dead_hook_latches` still globs `hook-{seat}-gen*.lock` only, so a dead SESSION-keyed latch is not swept at the next rotate-self spawn; it self-releases on the next hook prompt for the SAME seating, and leaks a file only across a re-seat. Clauses (1) IDENTITY and (2) RECORDS remain the target; the target verdict stays pending.
<!-- THOUGHT:END -->
