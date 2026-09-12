---
id: experiment:a00-8550b79c-beff34
mint_id: 51df0f29d1b54c82b53bacab38e74d65
type: experiment
parents:
  - hypothesis:l4-the-after-join-record-names-the-sender-and-signature-the-send-returned-the-trim-keeps-the-captive-ack-line-and-the-cap-counts-bytes
next_edges: []
confidence: 0.8
edited_by: a00-ff3e0db1
evidence_runs:
  - experiment:a00-8550b79c-beff34
loop: hypothesis:l4-the-after-join-record-names-the-sender-and-signature-the-send-returned-the-trim-keeps-the-captive-ack-line-and-the-cap-counts-bytes@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e24a29ec04ebfbe6
season: 2
title: A00 8550b79c beff34
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8550b79c-beff34

## Experiment

goal:g15.25 FIX-ONLY build — hypothesis
`l4-the-after-join-record-names-the-sender-and-signature-the-send-returned-the-trim-keeps-the-captive-ack-line-and-the-cap-counts-bytes`.
MEASURED at post tip, then IMPLEMENTED, then proved on the built bytes.

Pre-fix measure (grep on base):
- `rotate.py` run_after_join set
  `dm_signed = (_sessions_dir(root)/"seats"/f"{sender}.key").is_file()` — key-FILE
existence, not the send's outcome (`send.py:244-254 _signing_key_for` returns
None on a malformed key, so a send with a key file present can still go
UNSIGNED). The record's dm_sender/dm_signed were written BEFORE the send ran.
- `_compose_after_join_dm` trim dropped the whole captive ack line on an
  over-budget dm and compared `len(full) > cap` (code points, not UTF-8 bytes).
- the cmd_rotate_self after_join dry-run plan printed `ack --seat` (line ~14347)
  while the live composer grammar is `ack --post`.

Changes (named files):
1. `send.py` — `send()` now returns the additive pair `(sender_used, signed)`
   (post-`_detect_sender` id actually written; signed = an envelope sig was
   actually written, i.e. a USABLE key — a present-but-malformed key reports
   unsigned). Every existing caller ignores the return.
2. `rotate.py` run_after_join — the dm is SENT FIRST and the record's
   `dm_sender`/`dm_signed` are recorded FROM the send's return, never from a
   key-file read; the default send closure returns `_send.send(...)`'s pair;
   an injected send_dm may return the same pair (or nothing: the record keeps
   the DECLARED sender, unsigned).
3. `rotate.py` `_compose_after_join_dm` — over budget, keeps the HEAD + ONE
   status line per entry + the CAPTIVE ack line (pinned), trims the MIDDLE
   with ONE marker line `… [trimmed N bytes] …`; the cap counts UTF-8 BYTES
   (`len(full.encode("utf-8"))`), so a 1000 two-byte-char body is over a
   1500-byte cap; docstring gains the policy sentence (the heal watch signs
   with the SEAT's key — the seat's own late rotation tail, same trust
   domain, performer named on the record; no heal key minted).
4. `rotate.py` cmd_rotate_self dry-run plan — prints `ack --post` (the ONE
   grammar).

Deviation recorded (a judgement call, per CLAUDE.md): the hypothesis's
parenthetical "every existing caller ignores the return" is false for
`send_dm` (``ask``/``report``/``escalate`` forward its return and the
`send --to` command calls `.resolve()` on it; tests assert the Path).
So `send_dm` was LEFT returning `Path`; only `send()` returns the pair —
which is what run_after_join's dm path actually uses. Changing send_dm's
return would have broken non-ignoring callers, violating "additive".

## Evidence

5 tests appended (<= 6), all green:
- test_after_join_service.py (3): (a) a fake send returning
  `(sender="heal", signed=False)` names the record's dm_sender/dm_signed FROM
  THAT RETURN even with a real on-disk seat key present (the falsifier);
  (b) an over-budget dm keeps head + status + the captive `ack --post` line,
  trims the middle with ONE `… [trimmed N bytes] …` marker, stays under the
  byte cap; (c) a 1000 two-byte-char body is over a 1500-byte cap (code-point
  count would keep it under).
- test_rotate.py (1, placed here — helpers `_write_seats_sheet` /
  `_rotate_self_args` / `fake_ladder` live in this module; the hypothesis
  listed (d) under test_after_join_service.py but it drives cmd_rotate_self):
  (d) the rotate-self dry-run plan prints only `ack --post` (no `ack --seat`
  on any printed `rotate.py ack` line).
- test_send.py (1): (e) send.send returns `(sender, signed)` on a signed
  fixture and `(sender, False)` on a key-file-present-but-malformed fixture.

Suite runs (named files, full suite green):
717 passed, 3 skipped — test_after_join_service test_send test_seatsig
  test_sensei test_heal test_bin_help_smoke test_write_self_row test_rotate
154 passed — test_heal_ack_rotation test_heal_watch test_rotate_tail
  test_rotate_handover test_write_master_sensei test_heal_seats
126 passed, 1 xfailed — test_sensei_wake_audit test_sensei_rotate_out_audit
  test_rotate_g1517 test_rotate_alert_two_tree test_rotate_prepare

Falsifiers checked:
- `dm_signed` no longer derived from the key file in run_after_join (grep:
  only `dm_signed = False` + the `_dm_ret` assignment remain).
- an over-budget dm now keeps the ack line (test b).
- the cap counts UTF-8 bytes (test c).
- the dry-run plan prints `--post` (test d).
- `_detect_sender` precedence untouched (out of scope).

Remaining `ack --seat` in rotate.py are the cmd_ack REFUSED line (2095), the
seating STARTUP alert body (4119), the successor ROTATION-CONTINUATION
instructions (14104/14117) and the s6.3 --ask-diff wake call (14560) — all
live-instruction/help lines governed by other ack hypotheses, each asserted
by existing tests (test_rotate.py:4369,4565,7915,7962; test_rotate_handover.py:1356),
and cmd_ack accepts both `--seat` and `--post` (parser: `--seat`, `--post`,
same dest), so prose may keep `--seat`. Only the DRY-RUN PLAN (the claim's
scope) is the one-grammar `--post`.

## Agent Notes
g15.25 FIX-ONLY built+proved: send() now returns (sender_used,signed); run_after_join records dm_sender/dm_signed FROM the send return (default closure returns the pair) never key-file; over-budget dm keeps head+status+captive ack line, trims middle with ONE marker, cap counts UTF-8 bytes; rotate-self dry-run plan prints ack --post. 5 tests appended, 1000-line suite green. Deviation: send_dm return left as Path (its callers consume it; additive would break).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW a00-ff3e0db1 (parent, SL7.99): accepted, verdict proved stands.

(1) WHAT THE INSTRUCTION SAID: the target hypothesis is a FIX-ONLY build order — "send.send / send_dm return (additively — every existing caller ignores the return) the sender actually used and whether the envelope was signed; run_after_join records dm_sender and dm_signed FROM THAT RETURN, never from the file system", plus trim-keeps-ack-line, UTF-8 byte cap, dry-run grammar, policy sentence; <=60 lines + <=6 tests.

(2) WHAT THE MACHINE ACTUALLY DOES, cited to file:line on the built bytes: rotate.py:11169-11173 `_dm_ret = send_dm(seat, dm)` then `dm_sender, dm_signed = _dm_ret` guarded by isinstance/len/str; the default closure at rotate.py:11159-11167 returns `_send.send(root, to, text, sender)`; send.py:2296 now returns `(from_id, sig_line is not None)` at send.py:2343; dm_sender/dm_signed are written to the record at rotate.py:11219-11220 AFTER the send. `_compose_after_join_dm` at rotate.py:10724 compares `len(full.encode("utf-8")) > cap`, and the trim at rotate.py:10753-10755 pins the ack line via `ack --post` with N byte-counted. The dry-run plan prints `--post` at rotate.py:14382. I ran the three touched test files myself: 612 passed.

(3) NEAR MISS: the plausible implementation that satisfies the words and loses the mechanism is to keep writing dm_sender/dm_signed from a key-file existence check and merely ADD the send's return as an extra field — the record would then still say "signed: yes" for a present-but-malformed key, and the falsifier test at test_after_join_service.py:2145 would catch it because it plants a REAL key on disk and asserts dm_signed is False. It does not: the key-file read is gone (grep dm_signed shows only the declared-sender fallback and the _dm_ret assignment).

(4) DEVIATION FROM THE LITERAL CLAIM, measured and accepted: the claim named send_dm as well as send.send; the kid left send_dm returning Path (send.py:3118) because its callers consume it — send.py:3185/3231/3247 forward it (ask/report/escalate) and the `send --to` CLI prints it at send.py:4275, and tests assert the Path. Changing it would violate "additively — every existing caller ignores the return", which is false for send_dm. The function run_after_join actually calls is send.send, so the mechanism the claim wanted (record names what the send returned) is fully delivered. This is a property of THIS case: the claim's parenthetical was wrong, not the implementation.

CAVEAT for the next reader: the default-closure path is exercised only through the stubbed `send` module (test_after_join_service.py:_stub_send returns the pair), so an end-to-end rotation whose real send() errored would fall back to the declared sender/unsigned — correct, but not directly asserted.
<!-- THOUGHT:END -->

PARENT REVIEW a00-ff3e0db1: accepted as proved. Verified on bytes (rotate.py:11159-11173, 10724/10753-10755, 14382; send.py:2296-2343) and re-ran the three touched test files: 612 passed. Recorded deviation accepted: send_dm left returning Path because send.py:3185/3231/3247/4275 consume it; the claim's 'every existing caller ignores the return' is false for send_dm, and run_after_join uses send.send, which now returns (sender_used, signed). File scope held: rotate.py, send.py, three test files only.
