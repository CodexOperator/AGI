---
id: experiment:a00-7292064c-9ac113
mint_id: f2df22727ff240439c463a014e3b4a9b
type: experiment
parents:
  - hypothesis:l4-after-join-is-claimed-on-the-record-before-any-command-runs-one-perform-one-dm-per-record-and-a-join-resolved-gate-with-an-upper-bound
next_edges: []
confidence: 0.85
edited_by: a00-b8d150af
evidence_runs:
  - experiment:a00-7292064c-9ac113
loop: hypothesis:l4-after-join-is-claimed-on-the-record-before-any-command-runs-one-perform-one-dm-per-record-and-a-join-resolved-gate-with-an-upper-bound@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 24643102d3b9e6da
season: 2
title: A00 7292064c 9ac113
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7292064c-9ac113

## Experiment

Closed the TWO wedges the SL7.8x claim + JOIN-GATE cut left open (found by
reading its produced bytes), in `extensions/agi/bin/rotate.py` +
`extensions/agi/tests/test_after_join_service.py` (same file scope as SL7.88),
without touching 6.4 succ_ref, cmd_ack/_prepare_checks, or heal _watch re-exec.

### Fix A — the CLAIM WEDGE (no staleness bound on a dead claim)

a performer that claims, then dies before writing results, left `after_join`
truthy with NO results; `_claim_after_join` and the `run_after_join_for_seat`
pre-check both DEFERRED forever on it — a rotation's join/dm stranded. Added
`startup.after_join_claim_stale_s` (coded default
`DEFAULT_AFTER_JOIN_CLAIM_STALE_S = 300`). A claim older than the bound with
no `results` is STALE: the next performer logs a NAMED line
`after_join claim stale for <seat>: claimed by <performer> at <ts>` to stderr
and FALLS THROUGH to re-claim (overwrites the dead claim with its own) and
perform. A LIVE (fresh) claim still defers; a completed block (results)
never stale. Helper `_claim_is_stale` / `_claimed_at_age_s` / `_parse_utc_inst`
(read both the `+00:00` isoformat `_claim_after_join` writes and the `Z`
forms records/fixtures read). `run_after_join` passes stale_s from its
`startup`; `run_after_join_for_seat` now resolves the template UP FRONT so the
live-claim pre-check reads the same startup block.

### Fix B — the `age_s is None` WEDGE (unmeasurable age never performed)

a window_id record whose `recorded_at` did NOT parse gave `age_s None`, and
the join gate did `wait_s = age_s if age_s is not None else 0.0` then
`if wait_s < max_wait: return waiting` — so it returned `waiting` on EVERY
pass and was NEVER performed, the opposite of the hypothesis' "never left
unperformed forever". New rule (stated in the code comment): when the record
age is unmeasurable, anchor the upper bound on the CLAIM's age
(`_claimed_at_age_s` — the fresh instant a performer touched the record)
when a claim exists; with NO claim AND no measurable record age there is NO
anchor, so DO NOT wait — perform now with the named `join unresolved after
<n>s` refusals. A record of measurable age behaves exactly as before.

### Falsifier tests added (55 pass in test_after_join_service.py, +3)

1. `test_stale_claim_reclaimed_and_performed_once_with_named_line` — a stale
   claim (claimed_at 2020) is re-claimed and performed once, stderr carries
   the named stale line.
2. `test_fresh_claim_still_defers_no_stale_line` — a FRESH claim (now)
   still defers: no run, no dm, no stale line, live claim not overwritten.
3. `test_unparseable_recorded_at_not_wedged_performs_once` — a window_id
   record with UNPARSEABLE recorded_at is NOT wedged: performs once with the
   named `join unresolved after ...` refusal; a second pass is a no-op.

Also fixed the pre-existing `test_second_performer_deferred_by_live_claim`,
whose hardcoded `claimed_at 2026-09-12T09:00:00Z` is now STALE on the real
wall clock — re-claimed by Fix A — so it changed to a genuinely-fresh
`datetime.now()` claim (its assertion "live claim defers" was only true
within 300 s of that stamp).

## Evidence

```
python3 -m pytest extensions/agi/tests/test_after_join_service.py \
        extensions/agi/tests/test_rotate.py extensions/agi/tests/test_heal.py -q
318 passed in 42.15s
python3 -m pytest extensions/agi/tests/test_rotate_tail.py extensions/agi/tests/test_rotate_startup.py -q
119 passed in 3.34s
```

Seat-path (heal watch entry) sanity: a stale claim on `run_after_join_for_seat`
emits `after_join claim stale for s: claimed by watch at 2020-01-01T00:00:00Z`
and performs (`results` present), out.deferred is None.

Filtered run of the 4 claim/stale/unparseable tests: 4 passed, 51 deselected.

## Agent Notes
Closed both wedges in rotate.py: (A) dead-claim staleness bound startup.after_join_claim_stale_s=300 makes an unreponsed claim re-claimable with a named stale line; (B) unparseable recorded_at no longer waits forever (anchor on claim age, else perform with named refusals). 55+318+119 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.88 (verified on the bytes): the two wedges kid 1 left are closed. (A) `_claim_is_stale`/`_claimed_at_age_s`/`_parse_utc_inst` (rotate.py:9690-9735) make a claim older than `startup.after_join_claim_stale_s` (DEFAULT 300) re-claimable with a named stderr line, while a completed block (results) is never stale; `run_after_join_for_seat` falls through on a stale claim instead of deferring forever (10548-10563). (B) the join gate no longer treats an unmeasurable record age as age 0: it anchors on the claim age, else performs with the named refusal (10632-10660). I re-ran the suite: test_after_join_service+test_rotate+test_heal+test_rotate_tail+test_rotate_startup = 437 passed. Verdict proved accepted for THIS increment: the two sub-claims are built and falsifier-tested. WHAT THE INSTRUCTION SAID: "a claim whose claimed_at is older than the bound AND has no results is STALE and must be re-claimable ... a fresh claim still defers". NEAR MISS, stated as the counterfactual: the stale-claim re-claim is also a read-then-write — if two performers both read the SAME stale claim before either re-writes, both log stale and both perform, so the staleness bound narrows the dead-claim wedge but does not make re-claim atomic; the new tests are sequential and cannot see this. Not a reason to reject: the same non-atomicity already governs the fresh-claim path, and the bound is strictly better than the infinite defer it replaces. REMAINING GAP vs the hypothesis (not this node): a join:null record with no window_id is still not gated.
<!-- THOUGHT:END -->
