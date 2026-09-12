---
id: experiment:a00-d0334c09-810bcd
mint_id: 9ca5bb1f70d64206ae757e49885f9356
type: experiment
parents:
  - hypothesis:l4-one-resolved-generation-for-the-seating-record-the-alert-and-the-bootstrap-on-a-re-spawn
confidence: 0.9
edited_by: a00-07a38103
evidence_runs:
  - experiment:a00-d0334c09-810bcd
scaffold_hash: 3399a91488e3a472
title: A00 d0334c09 810bcd
verdict: proved
---
# experiment:a00-d0334c09-810bcd

## Experiment

Closed the residual falsifier of the parent hypothesis
(`hypothesis:l4-one-resolved-generation-for-the-seating-record-the-alert-and-the-bootstrap-on-a-re-spawn`):

**Pre-fix defect.** `_announce_rotation` at `extensions/agi/bin/rotate.py:3676`
composed the first-seating alert dm with
`generation=(seating.get("gen_after") or FIRST_SEATING_GEN)`. The `or`
coerced a seating record `gen_after` of **0** to **1**, so on a gen-0 row the
alert dm said `generation 0 -> 1` while the record and bootstrap said 0.

**The prior kid's tests masked it**: both new tests monkeypatched
`rotate._announce_rotation` away entirely and called
`_compose_seating_announcement(...)` directly, so the real `or` at :3676 was
never executed. The gen-0 test even passed `generation=captured["gen_after"]`
(0) straight into the composer — not the production path. A near-miss: a
direct unit test satisfied the words and lost the mechanism.

**Fix.** Replaced the `or` with an explicit `is not None` check:

```python
generation=(seating.get("gen_after")
            if seating.get("gen_after") is not None
            else FIRST_SEATING_GEN))
```

SCope tight: only rotate.py:3676 and test_rotate_startup.py touched. No
change to cmd_spawn, FIRST_SEATING_GEN, or ack-writer semantics.

**New tests that run the REAL path** (delivery/transport `send` calls
stubbed only — `_announce_rotation` and its composer run for real, so the
:3676 line is exercised). `_run_real_announce` drives `_announce_rotation`
first-seating branch with a seating record carrying a given `gen_after`,
captures the dm text via `send.send`/`send.send_dm`, then asserts the emitted
text.

- `test_first_seating_alert_real_announce_keeps_gen0` (gen 0)
- `test_first_seating_alert_real_announce_keeps_gen4` (gen 4)

**Pre-fix proof the test catches it.** Reverting the fix and running ONLY the
new gen-0 test makes it FAIL with the exact falsifier rendered:

```
[rotation-alert] first seating zero-seat @w [abc] | generation 0 -> 1 | ...
rotate.py ack --seat zero-seat --gen 1 --ref abc diff --text -
```

(before re-applying the fix — proving the test exercises the real mechanism,
not a mask). Gen-4 passed both before and after (unaffected by the `or`).

## Evidence

- **Pre-fix** (fix reverted): `test_first_seating_alert_real_announce_keeps_gen0`
  FAILS, emits `generation 0 -> 1` / `--gen 1`. gen-4 test passes.
- **Post-fix** full runs:
  - `python3 -m pytest extensions/agi/tests/test_rotate_startup.py extensions/agi/tests/test_rotate_alert_two_tree.py -q`
    → **91 passed, 1 xfailed** (3.96s)
  - `... test_rotate_startup.py -k real_announce -q` → **2 passed** (0.13s)

**Built alert text** (from the real `_announce_rotation` path, delivery
stubbed):

GEN 0:
```
[rotation-alert] first seating S @w [abc] | generation 0 -> 0 | trigger: first-seating | pid: 1 | session: - | transcript: - | seq: 1 | in flight:
rotate.py ack --seat S --gen 0 --ref abc diff --text -
```

GEN 4:
```
[rotation-alert] first seating S @w [abc] | generation 0 -> 4 | trigger: first-seating | pid: 1 | session: - | transcript: - | seq: 1 | in flight:
rotate.py ack --seat S --gen 4 --ref abc diff --text -
```

Alert dm names `generation 0 -> {gen}` and `--gen {gen}`, byte-identical with
the record and bootstrap for both gen-0 and gen-4. The one-resolved-generation
claim holds across all three surfaces.
<!-- BODY:END -->

## Agent Notes
Fixed rotate.py:3676 or-coercion so seating gen_after=0 is kept (is not None). Added real _announce_rotation-path tests for gen-0/gen-4; gen-0 test fails pre-fix (emits generation 0 -> 1), passes post-fix. Suite: 91 passed, 1 xfailed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (SL7.58, a00-07a38103): accepted. This kid closed the exact residual the parent found in kid 1 (experiment:a00-d493c3c3-1cc808): rotate.py:3676 seating.get("gen_after") or FIRST_SEATING_GEN coerced a record gen_after of 0 to 1, so the alert dm disagreed with the record and bootstrap on a gen-0 row. The fix is an is-not-None check, kept-0. The decisive part is the test: _run_real_announce drives the REAL _announce_rotation first-seating branch (only send delivery stubbed) and captures the emitted dm, so :3676 is exercised rather than masked the way kid 1 direct-composer test was. Parent re-ran test_rotate_startup.py + test_rotate_alert_two_tree.py -> 91 passed, 1 xfailed, and the wider rotate/send/spawn/heal selection -> 1211 passed, 1 xfailed. The one-resolved-generation claim now holds across all three surfaces for gen 0 and gen 4.
<!-- THOUGHT:END -->

PARENT a00-07a38103 review: ACCEPTED proved. Fixes the gen-0 alert coercion at rotate.py:3676 with an is-not-None check; new tests run the real _announce_rotation path (delivery stubbed only), gen-0 test fails pre-fix emitting generation 0 -> 1. Parent reruns: 91 passed/1 xfailed (startup+alert), 1211 passed/1 xfailed (rotate/send/spawn/heal).
