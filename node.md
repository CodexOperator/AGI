---
id: experiment:a00-4fc36918-6fffdf
mint_id: 1088344949b94c709c978cf75a30e9cf
type: experiment
parents:
  - hypothesis:l4-sensei-wake-audit-keys-on-the-session-not-gen-or-the-prime-ack-name
next_edges: []
confidence: 0.9
edited_by: a00-2f136117
evidence_runs:
  - experiment:a00-4fc36918-6fffdf
loop: hypothesis:l4-sensei-wake-audit-keys-on-the-session-not-gen-or-the-prime-ack-name@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "python3 /tmp/probe_sl7124_parent.py P1 — row names session A (aaaaaaaa-...), the ONLY rotation record on disk carries handover.join.session_id = B; call sensei.wake_audit(graph, seat, None, None) with --gen absent", "expected": "refuse by name, never fall back to 'latest' (the half-fix audits session B's transcript silently); exit 2, stderr names session aaaaaaaa, calls == []", "observed": "exit=2; stderr=\"ERR: cannot audit a wake for seat 'probe-poster': no rotation record for 'probe-poster' session aaaaaaaa; pass --transcript PATH or let the seat's rotation record name its session_log\"; calls=0", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 /tmp/probe_sl7124_parent.py P2 — one seat, two records (A older/T100000Z, B newer/T110000Z), two session-keyed ack FILES on disk; rewrite ONLY the row's session_id between the two runs and call sensei.wake_audit(graph, seat, None, None) each time", "expected": "the row's session id must thread LIVE to BOTH _latest_record and _hand_read_paths: row=A audits A's record and classifies A's session-keyed ack (b); row=B audits B's record and classifies B's ack; a helper tested in isolation but never threaded from the wake_audit call site fails this", "observed": "row=A: code=0, calls=[('b','record:probe-poster.20260911T100000Z.json')]; row=B: code=0, calls=[('d','record:probe-poster.20260911T110000Z.json')]; _hand_read_paths(...,SID_B) contains 'seats/probe-poster.ack.bbbbbbbb.json'", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "python3 /tmp/probe_sl7124_parent.py P3 — a PRIME row (role prime_director) deliberately carrying session_id = A, a legacy seats/<seat>.ack.json on disk, a session-keyed seats/<seat>.ack.aaaaaaaa.json also on disk, and TWO records (gen 12, gen 13 T110000Z, no session ids); call sensei.wake_audit(graph, seat, None, None)", "expected": "the prime must NOT be authorised onto the session path: rotate._ack_session_id == '', the LATEST record is audited, Read .ack.json is (b) and Read .ack.<sid8>.json stays (d), and the derived signal set carries the legacy name only", "observed": "rotate._ack_session_id=''; code=0; src=['...T110000Z.json','...T110000Z.json']; cats=['b','d']; paths=['seats/probe-poster.ack.json', ...] with no session-keyed entry", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 30eb2bcf7b6f12e4
season: 2
title: A00 4fc36918 6fffdf
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4fc36918-6fffdf

## What was done

BUILD ORDER, not a measurement. The pre-fix state was measured, then the
mechanism was implemented in the engine bytes, then the built bytes were
proved. Scope: `extensions/agi/bin/sensei.py` +
`extensions/agi/tests/test_sensei_wake_audit.py` (rotate.py untouched; its
half landed at 1c7072101).

## Evidence 1 — the pre-fix defect (measured, before the fix)

The 5 new tests in `TestSessionKeyedWakeAudit` were written first and run
against the unmodified tip:

```
$ python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py -q \
      -k "SessionKeyed"
5 failed, 62 deselected in 0.41s
```

The two load-bearing failures, verbatim:

```
>  assert _cats(counts) == {"a": 1, "b": 0, "c": 0, "d": 0, "s": 0}
E  AssertionError: assert {'a': 0, 'b':..., 'd': 1, ...} == {'a': 1, ...}
E    Differing items: {'d': 1} != {'d': 0}; {'a': 0} != {'a': 1}
```
(record selection: the LATEST record — the other session's transcript — was
audited, so the row's own session-keyed post audited as missing/wrong)

```
>  assert calls[0]["cat"] == "b"      # the row's OWN session-keyed ack
E  AssertionError: assert 'd' == 'b'
```
(a session-keyed ack read classified (d) real work — which CUTS the wake
window — because `_hand_read_paths` spelled only `seats/<seat>.ack.json`)

## Evidence 2 — the built bytes (after the fix)

```
$ python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py \
      extensions/agi/tests/test_sensei.py \
      extensions/agi/tests/test_sensei_rotate_out_audit.py -q
104 passed in 0.65s
```
plus the shared-mechanism neighbours (rotate handover/tail/selfreap, which own
their own `_latest_record`):
```
$ python3 -m pytest ...test_sensei_wake_audit.py test_sensei.py \
      test_sensei_rotate_out_audit.py test_rotate_handover.py \
      test_rotate_tail.py test_rotate_selfreap.py -q
203 passed, 396 warnings in 37.04s
```
All green. `rotate_out_audit` still drives `_hand_read_paths`/`_latest_record`
through their defaults and did not move.

## Changed bytes (sensei.py, ~62 lines net, <=120 ceiling)

1. `_record_matches_session(rec, session_id)` (sensei.py:594) — reads
   `handover.join.session_id`; full match, or an 8-char-prefix match either
   way (the ack is spelled `session_id[:8]`), with an 8-char floor so a
   truncated/blank id matches nothing.
2. `_latest_record(root, seat, gen=None, session_id=None)` (sensei.py:638) —
   a non-empty `session_id` narrows selection to the matching record, latest
   by filename order among matches; the `gen`/`latest` arms are byte-identical
   when `session_id` is empty (same loop, `session_id` is an extra filter).
3. `_resolve_wake_transcript(..., session_id=None)` (sensei.py:677) threads it
   and names the session in the refusal when no record matches.
4. `_hand_read_paths(entries, facts, seat, session_id="")` (sensei.py:897) adds
   `seats/<seat>.ack.<session_id[:8]>.json` when non-empty, and keeps
   `seats/<seat>.ack.json` UNCONDITIONALLY.
5. `wake_audit` (sensei.py:1180-1193) resolves `session_id =
   rotate._ack_session_id(root, seat)` — the same identity path
   `rotate._ack_path` writes with — and passes it to both.
6. `--gen` stays `default=None`; no new CLI flag; argparse surface unchanged.

## The four conjuncts, each against bytes

(a) **record by session, --gen optional and never required for a non-prime
post** — `test_record_selected_by_row_session_not_latest`: one seat, two
records (`handover.join.session_id` + `handover.join.transcript` to two real
transcripts), the row names session A and A's record is the OLDER one. With
`gen=None` the audit reads A's transcript (`whois` -> F2, source
`20260911T100000Z.json`), not B's LATEST `true`. `_latest_record`'s session
arm does the selection.

(b) **two session-keyed acks select the matching session** —
`test_two_session_keyed_acks_selects_the_matching_session`: two ack FILES on
disk (`seats/<seat>.ack.aaaaaaaa.json`, `...bbbbbbbb.json`) and two by-hand
Read calls. The row's OWN session-keyed ack path classifies **b**; the OTHER
session's ack path still classifies **d**. No `--gen` anywhere.

(c) **Prime legacy `.ack.json` still resolves** —
`test_prime_legacy_ack_and_latest_record_unchanged`: a prime row
(`role: prime_director`, so `rotate._is_prime_role` -> `rotate._ack_session_id`
returns "") has its `.ack.json` read classify **b**, and with no `--gen` the
LATEST record is audited (`20260911T110000Z.json`) — byte-identical to before.
`_hand_read_paths(..., "")` still contains `seats/<seat>.ack.json`.

(d) **documented fallback, never a silent re-key** —
`test_nonprime_row_without_session_id_falls_back`: a non-prime row with NO
`session_id` audits the LATEST record and its derived signal set carries the
legacy name only (exactly one `seats/<seat>.ack.*` entry). Plus
`test_hand_read_paths_adds_session_keyed_ack_only_when_given`, which pins the
mechanism directly: `""` -> legacy only; `"abcdef1234567890"` -> both.

## Evidence

5 new tests (ceiling 6). Files changed: `extensions/agi/bin/sensei.py`,
`extensions/agi/tests/test_sensei_wake_audit.py`. No other file touched; no
git command was run.

## Agent Notes
wake-audit now keys a non-prime post's record AND ack on the row's session_id: _record_matches_session + _latest_record(session_id=) + _hand_read_paths adds seats/<seat>.ack.<sid8>.json while always keeping .ack.json; wake_audit resolves via rotate._ack_session_id. Pre-fix 5 new tests failed (wrong record audited; own session ack read classified d -> window cut); post-fix 104 passed on the 3 required files, 203 with the rotate neighbours. 5 tests, ~62 net lines, sensei.py only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2f136117), SL7.124, target hypothesis:l4-sensei-wake-audit-keys-on-the-session-not-gen-or-the-prime-ack-name. Kid's verdict ACCEPTED as proved; no demotion. Read the changed bytes (git diff --cached over sensei.py + test_sensei_wake_audit.py), not this node's own report.

(1) INSTRUCTION, quoted from the target's testable_claim: "sensei.py wake-audit resolves a non-prime post record and ack by the post SESSION key -- ack seats/<post>.ack.<session_id8>.json (rotate.py:2239-2256, landed 1c7072101) and the record whose handover.join.session_id matches -- with --gen optional and never required for a non-prime post; a fixture with two session-keyed acks and two records for one post selects the matching session, and the Prime legacy .ack.json still resolves."

(2) WHAT THE MACHINE ACTUALLY DOES, read from the bytes and then BUILT AND RAN. `_record_matches_session(rec, session_id)` (sensei.py:594) reads `handover.join.session_id`; `_latest_record(root, seat, gen=None, session_id=None)` (sensei.py:638) narrows to the matching record when session_id is non-empty and is byte-identical when it is ""; `_resolve_wake_transcript(..., session_id=None)` (sensei.py:677) threads it and names the session in the refusal; `_hand_read_paths(..., session_id="")` (sensei.py:897) adds `seats/<seat>.ack.<session_id[:8]>.json` and keeps `seats/<seat>.ack.json` UNCONDITIONALLY; `wake_audit` (sensei.py:1180-1193) resolves `rotate._ack_session_id(root, seat)` -- the SAME identity path rotate._ack_path writes with -- and passes it to both. argparse `--gen` stays default=None. I ran /tmp/probe_sl7124_parent.py (exit 0, 12/12 assertions): P1 auth -- a row naming session A with only a session-B record on disk REFUSES by name (exit 2, "no rotation record for 'probe-poster' session aaaaaaaa", calls=0); P2 wire -- rewriting ONLY the row's session_id flips the audited record AND the classified ack (row=A -> T100000Z + own ack (b); row=B -> T110000Z + other ack (d)); P3 auth -- a prime row carrying a session_id anyway keeps `.ack.json` (b), keeps the session-keyed ack read at (d), and still audits the LATEST record.

(3) THE NEAR MISS, stated as a counterfactual. A kid that adds `_record_matches_session` and the session-keyed ack signal but never threads the row's session id from `wake_audit`'s call site satisfies every helper-level unit test and loses the mechanism: the audit keeps auditing "latest" and keeps classifying a session-keyed ack read as (d), which CUTS the wake window -- the exact defect the claim names. P2 is the probe that kills it, because it changes only the row and requires both the record selection and the ack signal to move. It moved.

(4) DEVIATION FROM A STANDING RULE: none. Residual recorded, NOT a demotion: passing an explicit `--gen N` alongside a session-keyed non-prime post ANDs the two filters, so a caller who supplies a bogus generation on a generation-less post gets a named refusal -- the claim only requires that `--gen` be optional and never required, which holds.

The probe gate's own reading found no numbered CLAIM items in the target (its testable_claim has no `(1) (2) (3)` enumeration), so `_claim_conjunct_numbers` returns [] and the code gate would not have fired; I recorded the three probes anyway, one per conjunct I read out of the prose (record-by-session / ack-by-session-and-threaded / prime-legacy), in the node's `probes:` field.
<!-- THOUGHT:END -->
