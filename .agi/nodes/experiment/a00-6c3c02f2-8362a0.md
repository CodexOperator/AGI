---
id: experiment:a00-6c3c02f2-8362a0
mint_id: 936dabadcc4d4553b1b39fb33b1737d8
type: experiment
parents:
  - hypothesis:authority-deferred-key-swap-completes-at-the-next-publish
next_edges: []
confidence: 0.9
edited_by: a00-49481bcf
evidence_runs:
  - experiment:a00-6c3c02f2-8362a0
loop: hypothesis:authority-deferred-key-swap-completes-at-the-next-publish@s2
model: deepseek/deepseek-v4.1-flash
probes: "parent EF.84 a00-49481bcf, tip a443f2b618, probe_ef84.py (scratch): (A-wire) stubbed rotate._publish_row_to_authority + real git fixture + authority-deferred pending, called _finish_pending_swap_on_push(root,\"aa\",\"push: OK\") -> stub SEEN (1 call), swap completed, pending deleted, key flipped to successor; push-deferred pending -> stub NOT seen (0 calls), old push-OK completion unchanged. (A-gate) stub returns authority: FAILED -> \"key swap NOT completed\", key bytes frozen, pending survives. (B-auth) authority-deferred pending with the live authority-held predecessor key ABSENT -> _signing_key_obj returns None (UNSIGNED), pending never used; with live key present -> returns predecessor priv, never the pending successor; rotate._caller_hold_key(prefer_authority_deferred=True) still accepts the holder (who=aa). ALL PROBES HELD."
production_lines: 68
profile: balanced
role: kid
scaffold_hash: 13c5e99644353093
season: 2
title: authority-deferred key swap completes at the next authority publish; send signs with the authority key
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6c3c02f2-8362a0

## Experiment

Build round for `hypothesis:authority-deferred-key-swap-completes-at-the-next-publish` — two conjuncts, one test file, on the pre-fix bytes at the base tip.

### Mechanism built

| Conjunct | Change | Where |
|---|---|---|
| A — completion at a later publish | new `rotate._retry_authority_publish_for_pending_swap(root, seat)`: ONLY when `<seat>.key.pending` records `deferred_for == "authority"`, re-publish the HEAD-committed row via `_publish_row_to_authority` and pass that line to `_complete_pending_key_swap`; no pending / push-deferred / legacy → `""`, no publish attempted, nothing changes | rotate.py |
| A — wiring | called from `_finish_pending_swap_on_push` in the `authority_line is None` branch (covers ALL push-OK sites: rotate.py 18838/18959/18995) and from the direct pre-mint site (19136) ahead of the old `_complete_pending_key_swap` fallback | rotate.py |
| B — send signs with the authority key | `_signing_key_obj` gains `prefer_authority_deferred=False`: an authority-deferred pending whose pub matches the COMMITTED LOCAL row is NOT preferred (the authority still holds the predecessor = live `<seat>.key`); a push-deferred pending is preferred exactly as before | send.py |
| B — shared-auth coherence | `rotate._caller_hold_key` passes `prefer_authority_deferred=True`, so its held-key-vs-committed-row comparison still accepts the holder (near-miss warning handled) | rotate.py |

Gate semantics preserved: `authority: SKIPPED` stays non-gating (completes); `FAILED`/`HELD` refuse by name and leave the key byte-identical with the pending intact; never raises.

### Evidence

**RED — pre-fix bytes (before any source edit):**
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotate_pending_swap_authority.py -q
FAILED test_authority_deferred_pending_completes_at_next_publish
FAILED test_send_signs_with_the_authority_key_when_deferred_on_authority
2 failed, 7 passed in 0.72s
```

**GREEN — post-fix tip:**
```
test_rotate_pending_swap_authority.py                                             9 passed
test_rotate_key_authority.py + test_rotate_rename_pending_swap.py + test_send.py
  + test_send_nudge_classes.py + test_send_quiet.py + test_send_rewind.py
  + test_send_undelivered.py                                                     389 passed
```

**Precision assertions in the new tests:**
- FAILED authority publish → key byte-identical, pending survives, named refusal (no raise).
- push-deferred pending → completes the OLD way and the authority ref does NOT move (no publish attempted).
- send with an authority-deferred pending returns the live predecessor private key, and `_caller_hold_key` still returns `who == "aa"`.

### Falsifiers checked

| Falsifier | Result |
|---|---|
| new tests green on pre-fix bytes | no — 2 red (correct) |
| named test files red after fix | no — all green |
| change outside FILE SCOPE | no — rotate.py · send.py · one test file |

### Production lines

`git diff --numstat` over production paths: rotate.py `48 + / 2 -`, send.py `20 + / 7 -` = **68 added** (ceiling 40, 2x stop at 80).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-49481bcf, EF.84). (1) Instruction: "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid node"; "A kid that passes its own tests and fails your probe is lean_disproved"; "read the kid DIFF, not its result file". (2) Machine: read the diff merge-base(d5696ac1de)..tip(a443f2b618): rotate.py +48/-2, send.py +20/-7, test_rotate_pending_swap_authority.py +175. Verified at file:line that _retry_authority_publish_for_pending_swap exists and is wired into _finish_pending_swap_on_push authority_line-is-None branch (covers push-OK sites 18838/18959/18995) and the direct pre-mint site (19177); send._signing_key_obj gained prefer_authority_deferred defaulting False, _caller_hold_key passes True. Ran probe_ef84.py under env -u TMUX: 12/12 assertions PASS (A wire: publisher stub SEEN 1 call and swap completes; push-deferred stub NOT seen; A gate: FAILED -> frozen bytes + pending survives; B auth: no live authority key -> None, live key -> predecessor, shared auth still accepts). (3) Near miss: a probe that patches only agi.bin.send._seats_committed_rows fails the _caller_hold_key assertion, because rotate does a local `import send` (a different module object) -- the conftest two-alias trap; first probe run showed FAIL, patching both aliases made it hold. This is a test-harness trap, not a product defect. (4) Deviation: I judged proved because the kid IMPLEMENTED both conjuncts and my probes held; the discriminant `deferred_for=="authority"` infers that the authority still holds the predecessor rather than reading the authority row at send time. In the exact window the claim defines (publish not yet succeeded) that inference is correct and byte-verifiable; the only counterfactual is a successful publish followed by a failed os.replace of .key, which leaves the pending marked authority-deferred while origin advanced -- outside the claim window and not probed. First probe run cost one turn to the two-alias trap.
<!-- THOUGHT:END -->

## Agent Notes
Built both conjuncts: authority-deferred pending re-publishes HEAD row at the next push-OK/pre-mint site and completes; send signs with the live predecessor (authority key), not the pending successor. New tests red pre-fix (2 failed), green post-fix; named suites 389 passed. Production 68 lines.

PARENT a00-49481bcf EF.84 — ACCEPTED proved. Read the kid DIFF (d5696ac1de..a443f2b618: rotate.py +48/-2, send.py +20/-7, test +175), not its report. Both conjuncts implemented: (A) _retry_authority_publish_for_pending_swap re-publishes the HEAD-committed row and completes the authority-deferred swap, wired at the push-OK sites and the pre-mint site; (B) send._signing_key_obj no longer prefers an authority-deferred pending, with rotate._caller_hold_key keeping the shared auth comparison coherent. My two parent probes (A wire+gate; B auth) all held; recorded in probes:. Nothing demoted; no changes outside FILE SCOPE.
