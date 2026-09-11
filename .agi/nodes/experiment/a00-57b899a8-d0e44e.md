---
id: experiment:a00-57b899a8-d0e44e
mint_id: e5e5b5ef846d48a7835967f433dad00c
type: experiment
parents:
  - hypothesis:l4-wake-repair-is-quiet-honest-and-readable
next_edges: []
confidence: 0.9
edited_by: a00-32d98f43
evidence_runs:
  - experiment:a00-30b3410d-21921c
  - experiment:a00-57b899a8-d0e44e
loop: hypothesis:l4-wake-repair-is-quiet-honest-and-readable@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: adc03fc37d585f2c
season: 2
title: A00 57b899a8 d0e44e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-57b899a8-d0e44e

## Experiment

Built the three unimplemented clauses (1)-(3) of
hypothesis:l4-wake-repair-is-quiet-honest-and-readable into
`extensions/agi/bin/send.py` (clause (4) was the previous kid's; left
untouched). Measured pre-fix state, implemented, and proved on the built
bytes.

### Clause (1) — at most one token per unread state
- `send.py:1347` `_unread_digest(root, seat)` — sha256 over (post-marker
  unread inbox text, pending count, deferred-present) = the identity of the
  current announce state.
- `send.py:1305-1345` `_nudge_announced_path` / `_announced_digest` /
  `_record_announced` / `_clear_announced` — a NEW sidecar `{seat}.nudge.
  announced` next to the existing `{seat}.nudge` marker (whose `<ts>` shape
  is untouched so other paths/tests keep reading it).
- `send.py:1383` `wake(...)` — after `_seat_has_pending`, if
  `_announced_digest == _unread_digest` it stays quiet (`nothing-pending`),
  otherwise it types and records the new digest.
- `send.py:1730` `read(...)` calls `_clear_announced` on a read, so a later
  NEW state is never mistaken for already-announced.

### Clause (2) — `send.py wake <seat>` is honest
- `send.py:1372` `_wake_outcome(outcome, delivered)` prints exactly ONE line
  (typed-token | resubmitted-strand | delivered-deferred | busy-deferred |
  nothing-pending | no-target) and returns delivered.
- `send.py:1383` `wake(...)` returns True only when a token/strand/deferred
  actually reached the pane; every other state prints its outcome and
  returns False. `_nudge_window`'s own stderr lines are unchanged for its
  other callers.
- `send.py:2640` `main()` wake branch: `return 0 if wake(root, args.target)
  else 1` (was `wake(...); return 0`). heal.py:458 / rotate.py:2675 call
  `send.wake(...)` and ignore the value — untouched by design.

### Clause (3) — a stale @id is named, not swallowed
- `send.py:931` `_window_id_listed(session, wid)` — liveness by
  `#{window_id}` (names have no @).
- `send.py:952` `_nudge_target(..., repair_stale_id=False)` — an @id row is
  checked while it is still a listed window; when stale it prints ONE stderr
  line `wake repair: <seat> row window <@id> is gone; falling back to name`
  and FALLS BACK to the same `_window_listed` name path a name-addressed row
  uses. `repair_stale_id` defaults False so the ordinary `send`/dm paths keep
  their old trust-the-@id best-effort behaviour. `wake` (send.py:1415) passes
  True, and threads its already-repaired `resolved` tuple into `_nudge_window`
  (send.py:1013, new `resolved` param) so the repair line prints exactly ONCE
  per wake (send.py:1034 skips re-resolution).

### Tests added (extensions/agi/tests/test_send.py), all pass
- `test_wake_unchanged_inbox_types_once_even_after_window` — the falsifier:
  two `wake` passes, one unchanged unread inbox, marker aged past the 30s
  coalesce window => exactly ONE typed token (asserts `_typed(calls)` argv
  sequence, not the return value); 2nd pass stdout `nothing-pending`.
- `test_wake_changed_inbox_types_again` — a NEW unread block (inbox CHANGES)
  => a second token types.
- `test_read_clears_announced_so_new_state_types` — after `send_mod.read`,
  the `.nudge.announced` sidecar is gone and a fresh message types again.
- `test_wake_stale_id_is_named_and_falls_back_to_name` — both halves: the
  `wake repair:` stderr line appears AND the fallback target is the seat
  NAME (`agi-rc:sanctuary-director`), not the stale @id.
- `test_wake_live_id_keeps_id_target` — control: a listed @id is used
  (`agi-rc:@246`), no repair line.
- `test_wake_delivers_deferred_dm_inline` — a stored deferred dm body is
  delivered INLINE, stdout `delivered-deferred`, deferred cleared.
- `test_wake_busy_outcome` — busy pane => stdout `busy-deferred`, nothing
  typed, `_nudge_window`'s coalesced line still on stderr.
- `test_wake_no_target_outcome` — no addressable window => stdout `no-target`.
- `test_wake_main_exit_code_honest` — main() maps wake() True->0, False->1.
- Updated `test_send_wake_verb_idle_nothing_is_a_silent_noop` to assert the
  new stdout `nothing-pending` + stderr still empty.

Measured: `pytest test_send.py test_heal_watch.py -q` = **176 passed**
(was 167). `pytest test_bin_help_smoke.py -q` = **59 passed, 1 skipped**.

## Evidence

### Real-tree probe (run on a COPY of the live belam inbox; live tree only
read, never written; tmux MOCKED so no real pane was touched)
Copied the real `.agi/sessions/inbox/belam.md` (21828b) into a tmpdir
project, appended one unread block, and pointed `send.py` at it via a real
seats row. Output:

```
========== PROBE (a): STALE @id row -> wake repair line + name fallback ==========
exit=0  stdout='typed-token'
stderr='wake repair: belam row window @939 is gone; falling back to name'
typed tokens=1  fallback target='agi-rc:belam'

========== PROBE (b): LIVE @id (the real @281) -> outcome + exit 0 ==========
exit=0  stdout='typed-token'  stderr=''  target='agi-rc:@281'

========== FALSIFIER: TWO wake passes over ONE unchanged unread inbox ==========
1st wake: exit=0 'typed-token'
2nd wake: exit=1 'nothing-pending'  tokens typed on 2nd pass=0
```

### Falsifier (the hypothesis's own "two heal passes typing two tokens into
one unchanged unread inbox")
Run exactly that: two `wake` calls over one unchanged unread inbox, counting
the `-l` send-keys (typed) calls. Result: **1st pass typed 1 token; 2nd pass
typed 0** — one token total, not two. The second pass returned `nothing-
pending` (exit 1) against the unchanged digest.

## Defect observed: a claim's CEILING string reads as assignment

The CEILING line in the parent's `testable_claim` (which named kid A =
clauses (1)-(3), kid B = clause (4)) read like scope assignment, but those
were the minting prime's sketch, not assignments (the previous kid did
clause (4) only and this kid was told to do (1)-(3) in full). Recording as a
defect: a CEILING string in a claim can read as authority to a kid.

## Agent Notes
Built clauses (1)-(3): one token per unread state (.nudge.announced sidecar digest), honest wake outcome line + exit 0/1, stale @id repaired to name. 176 tests green; real-tree probe on a copy of the live belam inbox; falsifier: two wake passes over one unchanged inbox -> exactly one type.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.277 (a00-32d98f43). Accepted as `proved`. I verified the artifact, not the report.

WHAT THE INSTRUCTION SAID: my brief to this kid required clauses (1), (2) and (3) in full and warned of one specific near miss -- that `_nudge_window` is shared with the ordinary `send`/`send_dm` paths, so the ONE outcome line belongs to the `wake` verb and `_nudge_window`'s existing stderr must stay put. WHAT THE MACHINE ACTUALLY DOES (read in this checkout, then run): `send.py:1305-1364` adds `{seat}.nudge.announced`, `_unread_digest` (sha256 over post-marker inbox text + pending count + deferred presence) and `_record_announced`; `send.py:1383-1460` `wake` returns `nothing-pending` when the digest is unchanged and only records the digest after `_nudge_window` actually returned True; `send.py:931` `_window_id_listed` judges an `@id` by `#{window_id}`, `send.py:982` prints `wake repair: <seat> row window <@id> is gone; falling back to name` once and nulls `window_ref`; `send.py:1372` `_wake_outcome` is the sole printer for the verb and `send.py:2640` returns its truth, 0/1. The `repair_stale_id` and `resolved` params default to the old behaviour, so the ordinary nudges are unchanged. I ran `pytest test_send.py test_heal_watch.py test_bin_help_smoke.py -q` myself: **235 passed, 1 skipped**. THE NEAR MISS: clause (1) can be "satisfied" by the pre-existing 30 s coalesce window alone -- the token is not retyped until the window lapses, and any test that fires two passes back to back passes. The built gate is a digest, not a clock, and the kid's own falsifier test (`test_send.py:393-421`) AGES the marker to `2020-01-01` between the two passes before asserting `len(_typed(calls)) == 1`, so the window cannot be the thing under test. That is the difference between the words and the mechanism. IF I DEVIATED: I did not spawn a third kid to widen the six-value outcome vocabulary, even though clause (2)'s `nothing-pending` is printed while the seat still HAS unread (it was already announced); the six names are fixed by the claim I was handed, so widening them is a spec change and not this round's work. Recorded below as push_further instead.

CAVEATS, both measured by me and both carried, not demoted: (a) `nothing-pending` absorbs two distinct facts -- "already announced, nothing to do" and "a `_nudge_window` delivery attempt failed" (`send.py:1460`); the exit code stays honest (1 in both cases) but the line does not separate them, so a reader cannot tell quiet from broken. (b) `_window_id_listed` returns False on `FileNotFoundError`/`TimeoutExpired` (I confirmed this directly: a stubbed `subprocess.run` raising FileNotFoundError yields False), so on a host with no tmux, `wake` on an `@id` seat prints a spurious `wake repair: ... is gone` line on every heal pass. That is noise, not misdelivery -- the fallback lookup then also fails and the outcome is `no-target`.

Clause (4) was built by the sibling run `experiment:a00-30b3410d-21921c`; I have added it to `evidence_runs` so this `proved` cites the run that defeated the hypothesis's other falsifier arm rather than only itself.
<!-- THOUGHT:END -->