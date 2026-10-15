---
id: experiment:a00-dfe9f4d2-17b4e2
mint_id: 83ee251b16014d64abe386c543379625
type: experiment
parents:
  - hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration
next_edges: []
confidence: 0.85
edited_by: a00-0866334b
evidence_runs:
  - experiment:a00-dfe9f4d2-17b4e2
loop: hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fe3e44a1c976527e
season: 2
title: A00 dfe9f4d2 17b4e2
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-dfe9f4d2-17b4e2

## Experiment

CLAUSE (2) RECORDS of `hypothesis:l4-non-prime-genless-clauses-0-2-7-records-readers-migration`
(a g15 CLAIM = BUILD ORDER). Built on the already-landed clauses (0a)/(0b)/(0c)/(1);
those were not touched. FILE SCOPE honoured: `extensions/agi/bin/rotate.py`
(record + announce composition), the four named test files plus
`test_rotate_g1517.py`, and new assertions.

One predicate: `_seat_role(root, seat)` (rotate.py:4248) reads the seat's own
`config:seats` row role; every genless branch keys on `_is_prime_role` of its
result (`role is not None and not _is_prime_role(role)`). A `role=None`
(no row / direct unit caller) keeps today's gen shape byte-identical; the
guards are paired at `_is_prime_role(role)` spots.

### Step 2 — the announce text
- `_compose_announcement` (rotate.py:4791): new `role`/`seated_at`/`session_id`.
  NON-prime returns `[rotation-alert] <post> re-seated <ts> session <id8> |
  trigger: ... | handoff: ... | seq: ... | in flight: ...` — no `generation`
  substring. Prime path is the old string, byte-identical.
- `_compose_seating_announcement` (rotate.py:5286): non-prime replaces the
  `generation 0 -> N |` field with `re-seated <ts> session <id8> |`; the
  `--ask-diff` ack line routes through `_ack_call_args` for a non-prime post
  (`--post <p>`, never `--gen N`). Prime path unchanged.
- `_announce_rotation` (rotate.py:4982): seating branch passes
  `seating["role"]`, `seated_at`/`recorded_at`, and reads `window` when
  `window_id` is absent; rotation branch resolves `_seat_role(root, seat)`
  and passes `session_id` (row or caller-supplied). New `seated_at` /
  `session_id` params.

### Step 3 — the records
- `_seating_record` (rotate.py:5155): NON-prime -> `seated_at` (equal to
  `recorded_at`), `session_id`, `pid`, `ref`, and `window` (not `window_id`);
  NO `gen_before`/`gen_after`. Prime -> today's keys unchanged.
- `_rotate_self_record` (rotate.py:4593): new `role`. NON-prime drops the
  `b_generation` observation and adds top-level `seated_at`, and `window` /
  `session_id` / `pid` derived from the handover's `successor_window` and
  `join`. Prime unchanged.
- `_write_rotate_self_started` (rotate.py:4521): new `role`. NON-prime
  omits `gen_before`/`gen_after` (writes `seated_at`); this closes the
  in-progress surface so an interrupted non-prime rotation does not leak a
  gen. Prime unchanged.
- `_loop_record` (rotate.py:4661): new `role`; NON-prime adds `seated_at`
  (loop never carried gen keys).
- `_seating_record_exists` (rotate.py:5225): a genless record (no
  `gen_after`) for the seat now counts as this seating — a non-prime
  seating is keyed by the seat, not a gen, so the dual-announce gate still
  fires.
- `cmd_rotate_self` passes `role=role` to all 7 `_rotate_self_record` and 7
  `_write_rotate_self_started` calls (closeout uses `_co_role`) and supplies
  the record's `seated_at`/`session_id` to `_announce_rotation`.
- `cmd_loop` resolves `_loop_role = _seat_role(root, name) or role` and
  threads it through its 4 `_loop_record` calls.

### Step 4 — test migration (never reverting production code)
Migrated (gen-keyed non-prime assertions -> genless shape):
`test_rotate.py::test_rotate_self_writes_record_with_five_observations`,
`::test_rotate_self_interrupted_after_spawn_leaves_started_record`,
`::test_spawn_first_seating_emits_seating_alert_and_record`,
`::test_spawn_first_seating_default_ack_source_seating_wake_zero`,
`::test_spawn_first_seating_ask_diff_prints_exact_ack_line`;
`test_rotate_startup.py::test_first_seating_respawn_record_and_alert_carry_row_gen`,
`::test_first_seating_row_generation_zero_is_kept_as_zero`,
`::test_seating_base_block_checks_record_at_resolved_row_gen`.
New: `test_non_prime_rotation_record_is_genless`,
`test_non_prime_announce_is_genless_re_seated_session`,
`test_prime_seat_record_and_announce_keep_the_gen_shape`.
No unmigrated gen-keyed test file remains that this change breaks; the two
named falsifier files (`test_rotate_handover.py`, `test_rotate_recover.py`)
were already green unmodified.

## Evidence

Commands (repo root = this checkout):

    python3 -m pytest extensions/agi/tests/test_rotate.py \
      extensions/agi/tests/test_rotate_handover.py \
      extensions/agi/tests/test_rotate_recover.py \
      extensions/agi/tests/test_rotate_startup.py \
      extensions/agi/tests/test_rotate_g1517.py \
      extensions/agi/tests/test_after_join_service.py -q
    -> 537 passed (baseline before the change: 534 passed; +3 new tests)

    python3 -m pytest extensions/agi/tests/test_rotation_alerts.py \
      extensions/agi/tests/test_rotate_alert_two_tree.py \
      extensions/agi/tests/test_sensei_rotate_out_audit.py \
      extensions/agi/tests/test_sensei_wake_audit.py \
      extensions/agi/tests/test_heal_watch.py \
      extensions/agi/tests/test_rotate_closeout_steps.py \
      extensions/agi/tests/test_rotate_latch_sweep.py \
      extensions/agi/tests/test_rotate_verb.py \
      extensions/agi/tests/test_rotate_identity_main.py -q
    -> 242 passed, 1 xfailed

    python3 -m pytest extensions/agi/tests/test_rotate_autopsy.py \
      extensions/agi/tests/test_rotate_closeout.py \
      extensions/agi/tests/test_rotate_complete.py \
      extensions/agi/tests/test_rotate_copilot_harness.py \
      extensions/agi/tests/test_rotate_first_decision.py \
      extensions/agi/tests/test_rotate_handoff_driven.py \
      extensions/agi/tests/test_rotate_launch_wrapper.py \
      extensions/agi/tests/test_rotate_legal_hint.py \
      extensions/agi/tests/test_rotate_next.py \
      extensions/agi/tests/test_rotate_prepare.py \
      extensions/agi/tests/test_rotate_selfreap.py \
      extensions/agi/tests/test_rotate_tail.py \
      extensions/agi/tests/test_rotate_templates.py \
      extensions/agi/tests/test_rotate_verb_resolvers.py \
      extensions/agi/tests/test_send.py \
      extensions/agi/tests/test_spawn_name.py -q
    -> 548 passed

Net line counts: rotate.py +98 net (135 ins / 37 del), test_rotate.py +71
net, test_rotate_startup.py -2 net.

## Residues (named, not hidden)
- The FIRST-SEATING BOOTSTRAP (`_first_seating_run`) still writes
  `generation:` and `gen N` telemetry for a non-prime seat. That is the
  bootstrap doc, not a rotation/seating RECORD or the announce; clause (2)
  does not name it. Left for the clause-(7) READERS kid or a follow-up.
- `_seat_role` resolves the row by the seat NAME. A non-prime seat whose
  live window is a chain name (`belam-S1-L4-<n>`) with its row under another
  name resolves `None` and keeps the legacy gen announce. Live non-prime
  seats are plain-named, so this is latent, not live.
- `_compose_announcement` / `_compose_seating_announcement` called DIRECTLY
  with no `role` still produce the gen shape (backward-compatible by
  design); production always reaches them through `_announce_rotation`,
  which resolves the role.

## Agent Notes
Clause (2) RECORDS built: non-prime rotation/seating/started/loop records are genless (seated_at+session_id+pid+window, no gen_before/gen_after) and the announce reads '[rotation-alert] <post> re-seated <ts> session <id8>'; prime shape byte-identical. 537 passed on the 6 named test files (+3 new), plus 242+548 across the alert/heal/sensei/rotate readers.

PARENT REVIEW (a00-0866334b, SM.243): accepted. Bytes read: one predicate _seat_role(root,seat) + _is_prime_role gates every branch. _compose_announcement and _compose_seating_announcement emit for a NON-prime seat the genless line "[rotation-alert] <post> re-seated <ts> session <id8>" and never the substring "generation"; _seating_record and _rotate_self_record/_write_rotate_self_started omit gen_before/gen_after and carry seated_at + session_id + pid + window for non-prime, while the prime branch keeps gen_before/gen_after and window_id byte-identically. All _rotate_self_record call sites pass role=role; the rotation announce resolves role via _seat_role. PARENT PROBES (all PASS): (wire/gate) _compose_announcement with role=director returns re-seated <ts> session <id8> with NO "generation"; with role=prime_director returns the exact "generation 21 -> 22" line; (gate) _seating_record role=director -> {seated_at, window, pid, session_id}, no gen keys; role=prime_director -> {gen_before:0, gen_after, window_id}; (gate) _rotate_self_record role=director -> keys {pid, seated_at, session_id, window} and NO observations.b_generation; role=prime_director keeps observations.b_generation {before,after}; role=None (legacy) keeps gen. Suite: test_rotate.py + test_rotate_handover.py + test_rotate_recover.py + test_rotate_startup.py + test_after_join_service.py + test_rotate_g1517.py = 537 passed. CAVEATS: only test_rotate.py and test_rotate_startup.py were migrated (the other two named files pass unchanged — their gen refs are prime or role-less fixtures); a row-less THROWAWAY seat (role=None) still emits the gen line, which the clause does not cover because a throwaway is not a post.
