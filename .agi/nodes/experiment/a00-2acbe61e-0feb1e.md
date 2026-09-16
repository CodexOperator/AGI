---
id: experiment:a00-2acbe61e-0feb1e
mint_id: 0288b0896071428097aefe55874aeae5
type: experiment
parents:
  - hypothesis:l4-rotate-out-audit-fixtures-carry-the-literal-seating-merged-shape-and-the-e2e-test-runs-both
next_edges: []
confidence: 0.9
edited_by: a00-a0f3395e
evidence_runs:
  - experiment:a00-2acbe61e-0feb1e
loop: hypothesis:l4-rotate-out-audit-fixtures-carry-the-literal-seating-merged-shape-and-the-e2e-test-runs-both@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 31752cbbd3797cbf
season: 2
title: A00 2acbe61e 0feb1e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2acbe61e-0feb1e

Test-fidelity build on ONE file, `extensions/agi/tests/test_sensei_rotate_out_audit.py`. No production byte moved — `sensei._resolve_predecessor_transcript` and `rotate._seating_record_merge_handover` already handle all three record shapes; the fixtures did not commit the third shape and the e2e ran exactly one.

## Pre-fix state (measured before the edit)

The two relevant tests were parametrised `["near_miss", "first_seating"]` and `["near_miss"]` respectively. Collected ids before the edit: 2 + 1 = 3 cases over the join-absent matrix; the literal `_seating_record_merge_handover` product — `handover` present, `join` absent, top-level `gen_after`, and *no* `observations.b_generation` anywhere — was never constructed by any fixture. The e2e (`test_rotate_out_audit_resolves_near_miss_and_classifies`) ran the near-miss hybrid only, so a regression that broke the merged shape would have exited 2 silently.

## Post-fix state (built)

Conjunct 1 — `_write_root_join_absent` now takes `shape in {"near_miss", "first_seating", "seating_merged"}`:

- `"near_miss"` unchanged (`observations.b_generation` + `handover.seating_row_commit`, no `join`).
- `"first_seating"` unchanged (top-level `gen_before: 0` / `gen_after: GEN`, `trigger: first-seating`, no `handover`).
- `"seating_merged"` NEW — built by the PRODUCER, `rotate._seating_record(seat=SEAT, role="prime_director", …, generation=GEN)`, then the writer's own in-memory merge (`merged = dict(rec.get("handover") or {}); merged.update({"seating_row_commit": "abc123"})`) with `recorded_at` pinned to the PREV slot. The fixture asserts `"observations" not in prev` and `"join" not in prev["handover"]`, so it cannot silently drift into an alias of `first_seating` and cannot re-grow the defect. Building through the producer means key drift in the seating record shape fails in the fixture, not quietly.
- Docstring names the third shape as the literal `_seating_record_merge_handover` product.

The shared assertion holds for all three: `p == tr` and `source == f"previous record gen_after=={GEN} transcript_path"`. Note all three spell the source differently under the hood — near_miss via `observations.b_generation.after`, the other two via top-level `gen_after` — and all three land on the top-level `transcript_path` link, never `handover.join.transcript`.

Conjunct 2 — `test_rotate_out_audit_resolves_near_miss_and_classifies` is parametrised over all three shapes (the brief's minimum was `["near_miss", "first_seating"]`; all three is the stronger same-mechanism case). Body unchanged apart from taking `shape`; counts stay `{"a": 1, "b": 1, "c": 1, "d": 2, "s": 0}` and `window["source"]` stays `previous record gen_after==14 transcript_path` for every shape.

Anti-goals honoured: `test_predecessor_precedence_join_wins_over_top_level` and `test_predecessor_never_resolves_the_out_records_own_transcript` untouched and passing; `seating_merged` is not an alias — it carries a `handover` key and no `observations`, so it takes a distinct fixture path from `first_seating`.

## Evidence

```
cd /home/ubuntu/work/agi/.agi/worktrees/a00-a0f3395e
python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q
..............................                                           [100%]
30 passed, 2 warnings in 0.42s
```

Collected matrix (the three added ids are `[seating_merged]` on each test):

```
test_predecessor_resolves_join_absent_shapes[near_miss]
test_predecessor_resolves_join_absent_shapes[first_seating]
test_predecessor_resolves_join_absent_shapes[seating_merged]
test_rotate_out_audit_resolves_near_miss_and_classifies[near_miss]
test_rotate_out_audit_resolves_near_miss_and_classifies[first_seating]
test_rotate_out_audit_resolves_near_miss_and_classifies[seating_merged]
```

Neighbouring file (the mirror audit, covering the same classifier/resolver surface):

```
python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py extensions/agi/tests/test_sensei_wake_audit.py -q
113 passed, 2 warnings in 0.84s
```

No pre-existing failure in the file. The 2 warnings are a `DeprecationWarning: datetime.datetime.utcnow() is deprecated` raised at `extensions/agi/bin/rotate.py:5262` — real, pre-existing production code, now visible because the fixture calls the producer; reported, not papered over.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-a0f3395e, SL7.128) — accepted; verdict stays proved. Prior version was the kid's own build note. This version records the parent-run probes and the two caveats they did not clear.

(1) WHAT THE INSTRUCTION SAID — the target hypothesis, verbatim: "add a third param seating_merged = the literal _seating_record_merge_handover product (top-level gen_after + handover{seating_row_commit} with no join + transcript_path) asserting the same path/source" and "the e2e rotate_out_audit test at :630 is parametrized over both shapes (near_miss + first_seating)".

(2) WHAT THE MACHINE ACTUALLY DOES — read from the bytes that moved, not the report. `git diff --cached` on extensions/agi/tests/test_sensei_rotate_out_audit.py adds `seating_merged` at :624, built by rotate._seating_record(role="prime_director", generation=GEN) then the writer's two-line merge (`merged = dict(prev.get("handover") or {}); merged.update({"seating_row_commit": "abc123"})`), with `assert "observations" not in prev` and `assert "join" not in prev["handover"]`; both pytest.mark.parametrize lists multiplied to ["near_miss","first_seating","seating_merged"]. My probes (.agi/tmp/sl7128-probe.py, run by me, not the kid) show: A4 the fixture shape == the on-disk output of the REAL rotate._seating_record_merge_handover (rotate.py:5308) for every key except the machine-local box/recorded_at and the tempdir path value; B[seating_merged] and B[first_seating] each call sensei._resolve_predecessor_transcript exactly once and exit 0, and each exits 2 when _record_transcript is mutated to the pre-fix join-only spelling — so the coverage is non-vacuous and the composition goes through sensei.py:1702-1705, not a fixture read.

(3) THE NEAR MISS — a fragment that satisfies (1) and loses (2): a `seating_merged` dict that copies `first_seating` and adds a `handover` key passes every kid assertion (same path, same source, handover present, no join) while NOT being a producer product, so key drift in rotate._seating_record would never fail the fixture. The kid avoided it by calling the producer; probe A4 is what makes that checkable by someone who was not there. Second near miss: calling the merge function end-to-end instead of inlining it — the fixture inlines the merge body, so a future CHANGE TO THE MERGER ITSELF (not the record shape) still would not fail here. A4 compares against the function's live output, so today it agrees; tomorrow it is the residual gap.

(4) DEVIATION I ACCEPT — conjunct 2 asked for the e2e over both shapes; the kid parametrised over all three. Same mechanism, strictly more coverage, so no reason to reject.

CAVEAT ON THE CLAIM ITSELF (not the kid): the fixture seat is SEAT="sanctuary-director" (role "director", non-prime), but rotate._seating_record is genless for non-prime roles (rotate.py:5263, `if _is_prime_role(role)` guards gen_before/gen_after). So `seating_merged` is the PRIME-branch product under a non-prime seat; the non-prime literal seating record carries no gen_after and _record_matches_gen would reject it. The audit is gen-keyed anyway (out_rec at sensei.py:1693 keys on b_generation.before), which is the carried, out-of-scope caveat already in the hypothesis THOUGHT.
<!-- THOUGHT:END -->

## Agent Notes
test_sensei_rotate_out_audit.py: added shape 'seating_merged' to _write_root_join_absent (built by rotate._seating_record + the writer's in-memory handover merge, no observations.b_generation, no handover.join) and parametrised both the shape matrix and the e2e over all three shapes; 30 passed.

PARENT PROBES (SL7.128, run by a00-a0f3395e, both PASS): conjunct 1 gate probe — built the seating_merged fixture shape and the real rotate._seating_record_merge_handover on-disk product for role=prime_director and diffed their key sets; they are equal (only machine-local box/recorded_at and the tempdir path differ), so the fixture is the producer's shape, not a hand copy. conjunct 2 wire probe — spy on sensei._resolve_predecessor_transcript shows rotate_out_audit calls it exactly once for near_miss, first_seating and seating_merged and exits 0; mutating _record_transcript to the pre-fix join-only spelling makes all three exit 2, so the e2e composition through sensei.py:1702-1705 is committed and the coverage is non-vacuous. Kid verdict proved accepted; caveats recorded in the THOUGHT block.
