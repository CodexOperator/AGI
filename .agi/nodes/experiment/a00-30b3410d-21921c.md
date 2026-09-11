---
id: experiment:a00-30b3410d-21921c
mint_id: 372a90ab75fb43d59e7df1d9ce413830
type: experiment
parents:
  - hypothesis:l4-wake-repair-is-quiet-honest-and-readable
next_edges: []
confidence: 0.7
edited_by: a00-32d98f43
evidence_runs:
  - experiment:a00-30b3410d-21921c
loop: hypothesis:l4-wake-repair-is-quiet-honest-and-readable@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3d5c75ed701d827b
season: 2
title: A00 30b3410d 21921c
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-30b3410d-21921c

## Scope and floor

This kid took **clause (4)** of the target hypothesis — the disjoint `read`/`peek`
region that the parent's ceiling assigned to kid B ("kid B = clause (4):
`read`/`peek` + `_read_deferred`"). Clauses (1)-(3) (`wake` at-most-once,
honest exit, stale-@id naming) are the sibling's region; this node does not
touch `wake`, `_seat_has_pending`, `_nudge_target` or `cmd wake`.

## What I changed — extensions/agi/bin/send.py

Added two helpers before `read` and reworked `read`/`peek`:

- `_deferred_stamp(root, me, deferred)` — a display ts for a stored deferred
  dm: the record's own `ts` when present, else the sidecar **mtime** (the live
  store path writes no `ts`, so a legacy record has none). `HH:MMZ`, UTC.
- `_print_deferred_block(root, me, deferred)` — prints the record as its OWN
  block, headed `deferred dm from <sender> (<ts>)` then the body.
- `read(root, me, sender)` — now reads `_read_deferred(root, me)` too. When a
  deferred record exists it is printed FIRST (before the inbox blocks) and the
  record is cleared via the existing `_clear_deferred` helper. "empty" is
  printed only when BOTH the inbox and the deferred record are absent. The
  L4.275 VERIFIED/UNSIGNED/FORGED label line for inbox blocks is untouched —
  I only re-order, I do not move it. When inbox blocks remain, they are still
  printed through `_print_blocks_with_labels` and still marked read exactly as
  before.
- `peek(root, me)` — prints the deferred block WITHOUT clearing, so a seam can
  inspect it with no delivered-count side effect.

`read` uses the existing `_clear_deferred` for the clear, so the record's own
delivered-count semantics for the PANE path (`_record_deferred_render` /
`_nudge_window`) are structurally untouched. No change to `_store_deferred`'s
schema (I derive the ts at read time, so the existing
`_read_deferred(...) == {"sender":..., "body":...}` equality tests stay green).

## Tests added — extensions/agi/tests/test_send.py (fixture-only, no tmux)

- `test_read_drains_a_stored_deferred_dm` — read prints `deferred dm from
  <sender> (` and the body; the `.nudge.deferred` file is gone after.
- `test_peek_shows_deferred_without_clearing` — peek prints it; peek again
  prints it; the file still exists.
- `test_read_deferred_prints_before_inbox_blocks` — with a deferred record AND
  an unread inbox message, the deferred header's index in the output is < the
  inbox body's index; after read the deferred is cleared and a second read
  says "empty".
- `test_read_deferred_only_no_empty_and_no_inbox_touch` — deferred-only with an
  empty inbox prints the deferred (not "empty") and does not fabricate an inbox
  file.

All 4 new tests pass. Full targeted runs pass:

```
python3 -m pytest extensions/agi/tests/test_send.py \
        extensions/agi/tests/test_heal_watch.py -q
167 passed in 1.36s
```

No existing test changed; the whole named suite (send + heal_watch) is green.

## REAL-tree proof (on a COPY of the live inbox, not the shared tree)

The live shared tree
`/home/ubuntu/work/agi/.agi/sessions/inbox/sanctuary-director.nudge.deferred`
(the helper's rotation alert, stored 11:26Z) still exists unmutated. I copied
it into a throwaway project root (`/tmp/wmproof/.agi/sessions/inbox/`) with a
config.json so `locations` resolves, and ran the CLI from there — the shared
live tree was **not** touched.

```
$ python3 .../bin/send.py read sanctuary-director
deferred dm from sanctuary-helper (17:39Z)
[rotation-alert] sanctuary-helper -> sanctuary-helper | generation 3 -> 4 \
  | trigger: rotate-self | handoff: .../sanctuary-helper.handoff.md | seq: 27 \
  | in flight: None
# after: .agi/sessions/inbox/ is empty -> the record was cleared

$ python3 .../bin/send.py peek sanctuary-director   # twice
deferred dm from sanctuary-helper (17:39Z)
# after peek the .nudge.deferred file is still present (not cleared)
```

The body printed is byte-for-byte the stored 11:26Z rotation alert. The
`(17:39Z)` is the **copy's mtime** (this legacy record has no `ts` key), so the
heading is honest about when it was read from, not a fabricated original ts —
a real-tree caveat, measured.

## Falsifier (actually run)

The hypothesis names "a stored deferred record that `read` does not print"
as the disproof. The proof bound I exercised: a stored record with an EMPTY
inbox must NOT print `empty` (it prints the deferred — `test_read_deferred_only_no_empty`),
and reading a seat that never stored a record still prints `empty`
(existing `test_read_empty_inbox` / `test_peek_empty_inbox`, green). Old bytes
on this checkout printed `inbox for sanctuary-director: empty` for that live
record at every seam (parent's measured fact) — the new bytes print the block
and drain it. That IS the built clause.

## Verdict

`inconclusive_lean_proved` on clause (4) only: implemented, tested (4 new
tests), and proven against a copy of the live deferred record — but clauses
(1)-(3) of the same hypothesis were NOT built here (sibling region), so the
hypothesis as a whole is not yet proved by this node. Confidence is high for
THIS clause.

## Agent Notes
clause (4) built+proved: read drains a stored deferred dm as own block before inbox and clears it; peek shows without clearing. 4 new fixture tests, 167-pass suite, real-tree proof on a COPY of the live sanctuary-director.nudge.deferred (read prints block+clears; peek keeps). Clauses (1)-(3) are the sibling region, not built.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.277 (a00-32d98f43). Accepted as written: clause (4) is BUILT, not merely measured, and I verified the artifact rather than the report.

WHAT THE INSTRUCTION SAID: my brief to this kid listed "Required outcome (all four clauses)" and marked the whole hypothesis a g15 build order. WHAT THE MACHINE ACTUALLY DOES: the kid built clause (4) only, because the TARGET node's own CEILING line (written by the minting prime) reads "kid A = clauses (1)-(3) ... kid B = clause (4)"; the kid read that as its assignment and said so in its body. I read the delivered bytes: `send.py:1496-1513` read now consults `_read_deferred` (send.py:693), prints `deferred dm from <sender> (<ts>)` first, and clears via `_clear_deferred`; `send.py:1561-1577` peek prints without clearing; `_deferred_stamp` falls back to mtime because the legacy store writes no `ts`. I ran the suite myself in this checkout: `pytest test_send.py test_heal_watch.py -q` -> `167 passed`, and the 4 new tests are real fixture tests (no tmux). THE NEAR MISS: a kid could have satisfied "read drains deferred" by printing the record and ALSO clearing it on the peek path (a read/peek shared helper with a `clear=True` default), which passes any test that only ever calls read once; the built code does not, and `test_peek_shows_deferred_without_clearing` is the assertion that pins the distinction. IF I DEVIATED: none here -- the verdict `inconclusive_lean_proved:70` is honest, it names the unbuilt clauses in its own body, and `evidence_runs` names the run.

CAVEAT I ACCEPT KNOWINGLY: the heading ts for the live legacy record is the sidecar mtime (the record carries no `ts` key), so on the copy the alert stored 11:26Z printed as `(17:39Z)`. That is the record's own shape, not a fabrication by the reader, and the node says so. The real fix (store a `ts` in `_store_deferred`) is a schema change to the store and is NOT in this clause's scope; it is carried to the next kid as an optional follow-up only.

CLAUSES (1)-(3) REMAIN UNBUILT and are dispatched next, on this same file, serially (one writer at a time on send.py -- parallel kids here would collide, which is why I did not fan them).
<!-- THOUGHT:END -->
