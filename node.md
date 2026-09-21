---
id: experiment:a00-ad0adb1e-403a0b
mint_id: f7140a7c85c043ba83fd58dfab449e0c
type: experiment
parents:
  - hypothesis:l4-the-meter-telemetry-key-resolves-to-a-measured-fraction-or-a-labelled-estimate-never-blank
next_edges: []
confidence: 0.85
edited_by: a00-bbb6f27a
evidence_runs:
  - experiment:a00-ad0adb1e-403a0b
loop: hypothesis:l4-the-meter-telemetry-key-resolves-to-a-measured-fraction-or-a-labelled-estimate-never-blank@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 57c76bc44bdc91e2
season: 2
title: A00 ad0adb1e 403a0b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ad0adb1e-403a0b

## Experiment

BUILD fix-only round on goal:g15.25 SL7.71. Pre-fix state MEASURED: both
rotation templates (director + prime_director, 4bad592ec + fb9e86652) list
`meter` in `telemetry`, so every bootstrap write ran `_derive_bootstrap_fact`
against a switch with no `meter` branch and rendered
`SKIPPED: no handover derivation for meter` for every seat. No pre-fix test
asserted that string (grep found none), so replacing it was safe.

Implemented the `meter` branch in `_derive_bootstrap_fact` (rotate.py:7416)
with three descending cases, the claim's exact shape:
  (a) the pinned successor transcript (the seat pin `<sessions>/<seat>.meter`
      -> transcript) has assistant usage -> the MEASURED fraction exactly as
      rotate.py meter prints it: `0.NNNN (used/window tokens)
      source=claude-code transcript (pinned) threshold=0.47`.
  (b) no usage but the caller supplies the successor's composed first-input
      byte count (`meter_first_input_bytes` kwarg, threaded through
      `_write_bootstrap` -> `_derive_bootstrap_fact`) ->
      `est. N tokens = first input <bytes>/4 (head + brief + STARTUP)` --
      labelled, never a bare number (P6).
  (c) neither (pre-spawn, transcript not answered yet, no bytes) -> None with a
      NAMED join-only reason; `meter` added to BOOTSTRAP_JOIN_ONLY_FACTS so the
      pre-spawn record writes `pending: resolved after join` (never blank,
      never SKIPPED), and `_fill_bootstrap_join_facts` now fills the measured
      fraction in place once the successor transcript carries its first
      assistant turn.

MEASURED which case is real (the hypothesis asked): on the live rotation the
pin write precedes the bootstrap write, so the successor transcript exists
but usually carries NO assistant usage yet -> the real pre-spawn outcome is
case (c) (join-only -> `pending: resolved after join`), and the post-join
`_fill_bootstrap_join_facts` (SL7.54's seam) fills the measured fraction. The
est. case (b) is implemented and tested but the pre-spawn rotate-self caller
currently supplies no byte count, so it stays the caller-opt-in path.

## Evidence

Three tests appended to test_rotate_startup.py, all green:
  test_meter_fact_measured_fraction_exactly_as_meter_prints  (case a)
  test_meter_fact_estimate_from_composed_first_input_bytes   (case b)
  test_meter_fact_join_only_pending_then_filled              (case c)

$ python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q -k meter
  3 passed, 88 deselected

Suite regressions checked (files that touch the bootstrap / join-fill facts I
changed, incl. BOOTSTRAP_JOIN_ONLY_FACTS):
  test_after_join_service.py + test_heal_ack_rotation.py + test_rotate_tail.py
    50 passed
  test_rotate_startup.py + test_rotate_handover.py
    134 passed

Representative asserted values (from the tests):
  measured : "0.0010 (1000/1000000 tokens) source=claude-code transcript
              (pinned) threshold=0.47"
  est.     : "est. 1000 tokens = first input 4000 bytes/4 (head + brief +
              STARTUP)"
  pre-spawn: telemetry["meter"] == "pending: resolved after join"
  post-join: telemetry["meter"].startswith("0.0020 (2000/1000000 tokens)")

The three falsifiers are all avoided on the built bytes: a bootstrap block
never reads SKIPPED for meter; a bare unlabelled number never appears (est.
carries `est.`); a transcript with usage prints the measured fraction, never
an estimate; and the join-only path leaves no `pending:` behind after the
join (rewritten with the measured fraction).

## Agent Notes
meter telemetry key now resolves in _derive_bootstrap_fact: measured fraction from pinned transcript, est. N tokens from composed first-input bytes/4, else join-only pending filled by _fill_bootstrap_join_facts; 3 tests green + 184 regression tests pass

## Agent Notes
meter telemetry key resolves in _derive_bootstrap_fact (measured fraction / est. N tokens from composed first-input bytes/4 / join-only pending filled post-join); FIX-ONLY build, 3 tests green, 184 regression tests pass

PARENT ACCEPT: meter resolves measured/est./join-only-pending, never SKIPPED; verified independently (292 tests green across 5 files); proved kept, confidence 0.85; est. byte-count caller is still opt-in, follow-up worth one node if rotate-self should pass it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-bbb6f27a: instruction said goal:g15.25 FIX-ONLY, kid must IMPLEMENT the meter branch, not merely reproduce it. Machine check: rotate.py:7493 now has key == "meter" (measured / est. / join-only), meter added to BOOTSTRAP_JOIN_ONLY_FACTS at :7573, all three _write_bootstrap call sites (9050, 12417, 13012) pass join_pending=set(BOOTSTRAP_JOIN_ONLY_FACTS), and _fill_bootstrap_join_facts computes overrides["meter"] (:9578). I re-ran the bytes myself: test_rotate_startup.py -k meter 3 passed; test_rotate_startup.py+test_rotate_handover.py 134 passed; test_rotate.py+test_after_join_service.py+test_rotate_tail.py 289 passed. NEAR MISS: a branch that only relabels the SKIPPED string would have satisfied the words and left pre-spawn blocks still non-resolving; the join_pending wiring is what actually makes it never-blank. Deviation from the claim text: the est. case is caller-opt-in because rotate-self passes no first-input byte count yet (kid said so); the pre-spawn real outcome is join-only pending, which the claim explicitly permits.
<!-- THOUGHT:END -->
