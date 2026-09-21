---
id: experiment:a00-2ad441ce-8a5a40
mint_id: 5ff2443ed4474216948028e9fa23c9b9
type: experiment
parents:
  - hypothesis:l4-the-first-seating-tests-stub-the-pushed-seats-seam-and-a-none-miss-is-not-pinned-for-the-process
next_edges: []
confidence: 0.9
edited_by: a00-cfbba4e5
evidence_runs:
  - experiment:a00-2ad441ce-8a5a40
loop: hypothesis:l4-the-first-seating-tests-stub-the-pushed-seats-seam-and-a-none-miss-is-not-pinned-for-the-process@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d0c149bbb0e400a1
season: 2
title: A00 2ad441ce 8a5a40
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2ad441ce-8a5a40

## Experiment

Tested, then built, the claim that the four `test_first_seating_*` tests stub
the pushed-seats seam (no real suite fetch reaches origin), the two
`send._pushed_seats` stubs clear the memo, and a None fetch miss is not
pinned for the whole process.

**Pre-fix measurement (falsifier reproduced):** injected a fake `git` into
PATH that logs each invocation (exits 128 on `fetch`) and ran the four
first-seating tests:

```
GITCALL:fetch origin season2/main      ×4
GITCALL:fetch origin season/s2         ×4
```

8 real `git fetch origin` attempts per file run; each test got the
worktree-fallback row and passed only because the fake exit made the pushed
ref unreachable — violating SL7.46's "no suite test reaches origin" and
SL7.54's fetch memo.

**Fix (rotate.py, `_prime_pushed_seats`):** a None miss is no longer
memoized on its first occurrence. The next build in the process RETRIES the
real fetch once; only a SECOND consecutive miss for the same `(root, ref)`
pins None (so a genuinely-dead pushed ref is fetched at most twice per
process, not on all five values-build sites). Added `_PUSHED_SEATS_MISSES`
counter (mirrors `_PUSHED_SEATS_FETCHED_ONCE`), cleared by
`_prime_rows_fetch_clear`.

**Fix (tests):** `_fs_prime_pushed_patch(monkeypatch)` clears the memo and
stubs `rotate._prime_pushed_seats`; `_fs_director_first_turn(root,
monkeypatch)` calls it, so all four `test_first_seating_*` run hermetically.
`_prime_dual_source_rows` and the fallback test now call
`rotate._prime_rows_fetch_clear()` first (memo can no longer shadow the
stub). Added `test_prime_pushed_seats_none_miss_retries_once_then_pins` and
`test_first_seating_family_reaches_no_origin_fetch` (counter asserts 0).

**Post-fix verification:** same fake-git PATH — 0 fetch calls, 11 seam tests
pass; full `test_rotate_startup.py` 84 passed; `test_rotate_recover.py` +
`test_after_join_service.py` 40 passed.

## Evidence

```
pre-fix (fake git exits 128 on fetch): GITCALL fetch origin season2/main ×4,
  season/s2 ×4  →  8 origin fetches across the family
post-fix (same fake git): NO FETCH CALLS; 11 seam tests green
pytest test_rotate_startup.py -q                    → 84 passed
pytest test_rotate_recover.py test_after_join_service.py -q → 40 passed
test_prime_pushed_seats_none_miss_retries_once_then_pins:
  miss1 → fetch (return None, not memoized); miss2 → fetch (not memoized);
  miss3 → no fetch (pinned None): fetch_calls == 2 ✓
test_first_seating_family_reaches_no_origin_fetch:
  send._pushed_seats reached 0 times across the three seat shapes ✓
```

A g15.25 claim, built and proven on the built bytes (FIX-ONLY round).
<!-- BODY:END -->

## Agent Notes
Pre-fix: 8 real git fetch origin across the 4 test_first_seating_* tests; _fs fixtures now stub rotate._prime_pushed_seats, the 2 send._pushed_seats stubs clear the memo, and _prime_pushed_seats retries a None miss once before pinning on 2nd consecutive miss. Post-fix: 0 fetches, 84+40 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-cfbba4e5, SL7.59): accepted as proved. Verified on the parent base by running the four first-seating tests plus the two new seam tests under a PATH-shimmed fake git that exits 128 on any fetch and logs every call — 7 passed, 0 fetch calls (the Prime measured 8 across the family pre-fix; the kid reproduced that before fixing). Full test_rotate_startup.py 84 passed in 2.42s. Read the artifact, not the report: _PUSHED_SEATS_MISSES skips memoizing the first miss and pins on the second for the same (root, ref); _prime_rows_fetch_clear clears both dicts; the _fs_* fixture clears the memo then stubs rotate._prime_pushed_seats; the two send._pushed_seats stubs (_prime_dual_source_rows, the fallback test) clear the memo first. All three claims in the testable_claim hold; file scope respected (rotate.py _prime_pushed_seats + the test file); exclusions untouched. Caveat carried: the two-miss pin rule means a genuinely-dead pushed ref still costs exactly 2 fetches per process, and a success after a first miss behaves correctly because success memoizes into _PUSHED_SEATS_FETCHED_ONCE so the miss counter is never re-read for that key.
<!-- THOUGHT:END -->
