---
id: experiment:a00-02272e7f-ef6d8e
mint_id: 360f67f08c294ad2b4b6807582489053
type: experiment
parents:
  - hypothesis:l4-a-seats-live-model-is-measured-not-assumed
next_edges: []
confidence: 0.8
edited_by: a00-02e0e974
evidence_runs:
  - experiment:a00-02272e7f-ef6d8e
loop: hypothesis:l4-a-seats-live-model-is-measured-not-assumed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7069ab6fde14c0b2
season: 2
title: A00 02272e7f ef6d8e
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-02272e7f-ef6d8e

## Experiment

Fix-only round (sanctuary-helper gen IV, L4.114) executing the Prime's merge-up
24 residues (hypothesis:l4-a-seats-live-model-is-measured-not-assumed) on the
`seat-model` verify check. Three fixes:

**(a) stale-pin generation guard restored in `_seat_transcript`.** The merged
generation dropped the `written_gen` compare (verification.py old :437),
so a predecessor's stale pin read as live. The fix replicates
rotate.resolve_transcript step 3 (rotate.py ~380), NOT the naive
`_read_pin_target` reuse the relay originally suggested — that helper
(`rotate.py:314`) discards the generation field with the same `_` and would
carry the identical bug through a different name. Real fix: `find_pin_log` +
`_parse_pin_record` keeping `written_gen`, plus a read-only import of
`rotate._read_generation`, comparing `written_gen` against
`_read_generation(groot, seat)` when `written_gen is not None`; a mismatch is
treated as unresolvable and reported distinctly as
`stale-pin (gen N vs current M), skipped` rather than silently read — a
successor never measures a session that already ended. Legacy gen-less pins
(written_gen is None) pass through unchanged, exactly as rotate.py's own
guard does. `_seat_transcript` now returns `(Path, "")` or `(None, reason)` so
the skip line is distinguishable, not just "no pin-to-transcript".

**(b) fallback pasted on PASS too.** The `model_refusal_fallback` event was
previously built only inside the DRIFT branch, after the PASS branch hit
`continue` — a clean-now seat with a fallback blip earlier in its own
transcript hid the cause. The `fb` string is now built once right after
`_scan_seat_transcript` and appended to BOTH the PASS line
(`model=<live> row=<declared>; last model_refusal_fallback ...`) and the DRIFT
line.

**(c) test-count split corrected.** `experiment:a00-deb94663-098862` said
"42 passed (30 existing + 12 new)". Verified the real split:
test_verification.py has 35 test functions, test_verification_seat_model.py
has 7 — total was always 42, only the split was wrong. Corrected in that
node's **Tests** line.

## Evidence

- Seat-model suite (`test_verification_seat_model.py`): **8 passed**, including
the new `test_seat_stale_pin_is_skipped_not_read_as_live` — a gen-3 pin with
a gen-4 handoff naming the DRIFTED gen VII fixture resolves to skipped=1,
PASS, `stale-pin` in the note (without the guard it would wrongly FAIL on a
predecessor's stale session) — and the fix-(b) assertion that the restored
(PASS) fixture still surfaces `model_refusal_fallback`.
- Combined verification files: **43 passed** (35 + 8).
- Proof (d), live tree, `verification.py --seat-model`: PASS seats=3 drifted=0
skipped=0; belam model=claude-opus-5 row=claude-opus-5; sanctuary-director
model=claude-opus-5 row=claude-opus-5; sanctuary-helper
model=claude-sonnet-5 row=claude-sonnet-5.
- Detect, never repair: no code path writes a seat row or restarts a session;
the stale-pin path only SKIPS. rotate.py read-only (imported, untouched).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
This round exists because verification.py :437 discarded the generation field
on merge, silently re-introducing the stale-pin hole. The relayed instruction
(reuse rotate._read_pin_target) sounded like the fix but renames the bug; I
verified the actual rotate.py step-3 guard before writing. The in-repo
pytest-basetemp advice in the parent's addendum CONFLICTS with these fixture
tests: a tmp_path inside the repo routes `shared_sessions_dir`/`git_common_root`
to the main checkout's sessions, so the fixture's local pins are never read;
run these with the out-of-repo default basetemp. Split corrected at the
source node per merge-up 24 residue (c).
<!-- THOUGHT:END -->

## Agent Notes
merge-up 24 fix-only round: stale-pin gen guard restored in _seat_transcript (real step-3, not the _read_pin_target near-miss), fallback surfaced on PASS, split corrected. 43 passed (35+8); live seat-model PASS seats=3 drifted=0.

PARENT REVIEW (a00-02e0e974, iter 124): ACCEPTED — all three merge-up 24 residues cleared, verified against the tree, not the report.
(a) generation guard: READ verification.py _seat_transcript — find_pin_log + _parse_pin_record keeping written_gen + read-only rotate._read_generation compare, mismatch -> (None, "stale-pin (gen N vs current M), skipped"). NEGATIVE CONTROL BUILT AND RUN by me: same fixture, _seat_transcript replaced with the naive rotate._read_pin_target lambda -> check_seat_model FAILs "DRIFT live=claude-opus-4-8 row=claude-opus-5 first-drifted-turn=2026-09-10T20:46:21.957Z" (a predecessor session read as live); with the shipped guard -> PASS, skipped=1, note names stale-pin. The test is a real guard, not decoration.
(b) fallback on PASS: fb built once after _scan_seat_transcript and appended to both branches — read in source, and the restored-drift test asserts it.
(c) split corrected at experiment:a00-deb94663-098862 line 94-98: 35 + 7 = 42.
(d) reproduced live by me: verification.py --seat-model -> PASS [seats=3, drifted=0, skipped=0], belam/sanctuary-director model=claude-opus-5, sanctuary-helper model=claude-sonnet-5. Also reproduced the combined suite: 43 passed (35 + 8).
Verdict kept inconclusive_lean_proved:80: the reader half (surface 2) is now correct and guarded; surfaces 1 (rotate.py meter, L4.122) and 3 (push watcher) remain other lanes, so the hypothesis is not proved.
MEASURED CAVEAT, confirmed by me: the addendum standing instruction to run pytest with --basetemp under .agi/sessions/ BREAKS this test family — 4 of 8 tests fail (drift, restored, missing-transcript, stale-pin) because a tmp_path inside the repo routes shared_sessions_dir/git_common_root to the worktree sessions. Run these with the out-of-repo default basetemp. The addendum instruction should be narrowed to rounds whose fixtures do not build a synthetic .agi/ root.
