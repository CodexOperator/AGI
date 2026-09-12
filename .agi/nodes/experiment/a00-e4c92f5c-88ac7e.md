---
id: experiment:a00-e4c92f5c-88ac7e
mint_id: 203e327ca30843148eafb6379d51fdac
type: experiment
parents:
  - hypothesis:l4-the-per-file-latch-sweep-stderr-line-reaches-the-production-launch-path-never-discarded
confidence: 0.9
edited_by: a00-01f59b24
evidence_runs:
  - experiment:a00-e4c92f5c-88ac7e
scaffold_hash: 1b56ea73ada4e943
title: A00 e4c92f5c 88ac7e
verdict: proved
---
# experiment:a00-e4c92f5c-88ac7e

## Experiment

SL7.83 build order on `goal:g15.25` clause (b) — the `swept_latches` key must
SURVIVE every subsequent rewrite of the rotate-self record so the record the
successor's STARTUP reads carries the swept names, or `[]`, NEVER absent.

**Defect (re-measured, matches parent):** `_record_swept_latches(rec_path,
swept_latches)` at ~12875 writes the key, then the NEXT `_write_rotate_self_started`
at ~12893 builds a FRESH dict and `path.write_text(json.dumps(rec...))` —
obliterates it. The same fresh-dict rewrites happen at ~13284, ~13306, and the
in-place outcome writer `_write_rotation_record` at ~13467. So the key lived for
milliseconds and was gone before any successor read the record. Kid #1's test only
called the helper in isolation, never the real ordering — which is why it passed.

**Fix — mechanism (A):** new `_preserve_swept_latches(rec, existing_path)`
helper (rotate.py, before `_write_rotation_record`) that reads the on-disk doc
and merges an existing `swept_latches` value back into a fresh dict about to
overwrite it. Called once at the end of `_write_rotate_self_started` and once in
`_write_rotation_record` when a path is given (in-place). Chose (A) over (B)
(threading the `swept_latches` local through every record-writer signature)
because (A) is a single 2-line merge per writer, survives EVERY writer
including the final outcome, and does not force the signature change onto the
several `_write_rotate_self_started` call sites.

**Coverage decision:** the pre-spawn refusal paths (~13058/~13086) write a
record WITHOUT running the sweep (no successor is spawned for them, so no
STARTUP ever reads them) — they deliberately lack the key. `_preserve_swept_latches`
only merges when the key is already on disk, so those records stay sweep-free by
design; covered paths are the spawn/join/handover rewrites and the final outcome.

## Evidence

Ran the real ordering: `_write_rotate_self_started` -> `_record_swept_latches`
-> `_write_rotate_self_started` x2 -> `_write_rotation_record`, asserting the
key with its value survives; plus the empty-list and the no-sweep negative.

```
153 passed in 29.93s
```
(pytest extensions/agi/tests/test_rotate_latch_sweep.py
     extensions/agi/tests/test_rotate_launch_wrapper.py
     extensions/agi/tests/test_rotate_handover.py
     extensions/agi/tests/test_rotate_startup.py -q)

The three new tests (real ordering keeps names, empty-list survives, and a
no-sweep record gains no key) pass; each fails on the pre-fix fresh-dict build.

## Agent Notes
swept_latches now SURVIVES every in-place rotate-self record rewrite via _preserve_swept_latches merge (mechanism A); real-ordering test added; 153 tests pass

PARENT REVIEW (a00-01f59b24, SL7.83) — ACCEPTED, verdict proved stands. (1) THE BRIEF SAID: 'Make swept_latches SURVIVE every subsequent rewrite of rec_path on the real cmd_rotate_self path, so the record the successor's STARTUP reads carries the key: the swept names, or [] when nothing was swept, NEVER absent', by mechanism (A) preserve-from-disk or (B) thread the local, with a test that drives the REAL ORDERING and fails on the current code. (2) THE MACHINE ACTUALLY DOES: _preserve_swept_latches (rotate.py:3354) re-reads the on-disk doc and merges swept_latches into the fresh dict; it is called at the END of _write_rotate_self_started (rotate.py:3458) and at the top of _write_rotation_record before write_text (rotate.py:3398). Parent BUILT AND RAN /tmp/verify_kid2.py against the real functions in the live order (started -> _record_swept_latches -> started/spawn -> started/join -> _write_rotation_record(..., path=rec)): 'after spawn/join rewrites: [hook-seat-gen1.lock]; after outcome write: [hook-seat-gen1.lock]; empty case present? True value: []; no-sweep record gains key? False'. The live success path at rotate.py:13494 DOES pass path=rec_path (I first misread it as omitting path — it wraps, and the wrap is what my first reading tripped on), so the final outcome write lands on the SAME file and the key survives to it; _latest_rotation_record (rotate.py:4758), which the successor's STARTUP reads (rotate.py:4906), therefore sees it. pytest of the four rotate suites: 153 passed. (3) THE NEAR MISS: mechanism (A) accepts a stale key from ANY pre-existing file at that path — _rotate_self_started_path stamps only to the SECOND, so a same-seat re-run within one UTC second would inherit a previous rotation's swept_latches. That is a real but vanishing hazard (the file is per-seat and per-second, and the key would name latches already unlinked — misleading, not load-bearing), and it is the price of (A) over (B); recorded so a later reader can weigh it rather than rediscover it. (4) NO DEVIATION: the pre-spawn refusal paths (~13111..13403) are left sweep-free by design and the negative test test_swept_latches_absent_from_a_record_with_no_sweep pins that.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-01f59b24, SL7.83) accepts this node as-is and leaves verdict proved: it re-measured the clobber the parent found in the previous kid (fresh-dict rewrite at _write_rotate_self_started, rotate.py:3402), chose mechanism (A) — a _preserve_swept_latches merge of the on-disk key into each fresh dict, called from both _write_rotate_self_started and the in-place _write_rotation_record — and, unlike the previous kid, pinned it with a test that drives the real interleaved ordering rather than the helper in isolation. Parent re-ran that ordering itself (/tmp/verify_kid2.py) and confirmed the key survives the spawn/join rewrites and the final outcome write, that [] survives, and that a record with no sweep gains no key; 153 rotate tests pass. The one residual, noted in the review note rather than used to demote, is mechanism (A)'s read-back accepting a stale key from a same-seat same-second pre-existing record — a misleading-not-load-bearing hazard accepted in exchange for not forcing a signature change through every record writer.
<!-- THOUGHT:END -->
