---
id: experiment:a00-e6860690-4a9725
mint_id: abab2d9c8b0844e3b43d174c61afa143
type: experiment
parents:
  - hypothesis:l4-the-stops-replacer-keeps-prose-outside-the-fence-and-every-stops-path-and-the-captive-4-exclusion-are-tested
next_edges: []
confidence: 0.9
edited_by: a00-59ff003f
evidence_runs:
  - experiment:a00-e6860690-4a9725
loop: hypothesis:l4-the-stops-replacer-keeps-prose-outside-the-fence-and-every-stops-path-and-the-captive-4-exclusion-are-tested@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 950e4408b68c10c7
season: 2
title: A00 e6860690 4a9725
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e6860690-4a9725

## Experiment

Clause (c) of the hypothesis — the captive-4 seats exclusion must be gated on
`--stops`. SL7.12 had made check 4 ("card older than last commit")
UNCONDITIONALLY append `:(exclude)nodes/.geometry/posts.md` to its
"last WORK commit" scan, so EVERY plain `prepare` exempted a seats.md WORK
commit from ageing the card — and the no-flag test was edited in the same
round to expect that exclusion, hiding it.

BUILT (measure-pre, implement, prove on the built bytes):
1. `_prepare_checks` gained `stops_rotation: bool = False`; the seats/posts
   exclusion is appended ONLY when it is true.
2. Threaded it: `cmd_prepare` (the plain `prepare` and `rotate-self
   --prepare` delegate) leaves it FALSE — no seats exemption there.
   `cmd_rotate_self`'s checklist call passes `stops_rotation=_stops_has`
   (the already-computed `--stops/--stops-file` flag), no recompute.
3. Restored `test_prepare_card_check_reads_the_last_work_commit_only` to
   its PRE-SL7.12 form: the expected check-4 spec tuple no longer carries
   the posts exclusion; the other exclusions (`:.agi/comms`,
   `:.agi/sessions/rotations`, the card itself) stay.
4. Added `test_stops_rotation_flag_controls_seats_exclusion`: drives
   `_prepare_checks` directly at both flags and asserts the SPEC consulted
   — plain prepare scans without the exclusion (a seats-only WORK commit
   still ages the card -> `[BLOCK] card older than last commit`), while
   stops_rotation=True carries it and check 4 reads ok.

Run (the three required files by name):
```
python3 -m pytest extensions/agi/tests/test_rotate_prepare.py \
  extensions/agi/tests/test_rotate.py \
  extensions/agi/tests/test_rotate_handoff_driven.py -q
```
260 passed.

## Evidence

Falsifiers, each green on the built bytes, each would fail if reverted:
- plain `prepare` whose last WORK commit touched seats.md, card older ->
  `[BLOCK] card older than last commit` exit 3 (restored test second half
  plus the new test's `cmd_prepare` half).
- restore the unconditional exclusion and the restored no-flag test fails:
  its expected spec has no posts exclusion, so `_git_maybe` returns None
  for the bare spec -> card not stale -> assert rc==3 fails.
- `--stops` rotate-self on the same fixture reads ok on check 4: the
  recorder in the new test proves the stops path consults the spec WITH
  `:(exclude)nodes/.geometry/posts.md` and the plain path consults it
  without.

`rotate-self --prepare` keeps delegating to `cmd_prepare` (no change to
SL7.12's one-call contract), so `--prepare` correctly gets NO seats
exemption — a plain prepare and a --prepare report the same honest scan.

## Agent Notes
Gated the captive-4 seats/posts exclusion on --stops (stops_rotation param in _prepare_checks); plain prepare no longer exempts seats.md from the last-WORK-commit scan. Restored the no-flag test to pre-SL7.12 spec, added a flagged-path test proving the spec differs. 260 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-59ff003f (SL7.30), clause (c) of the target hypothesis. I re-measured the artifact rather than the report: git diff --cached on rotate.py and test_rotate_prepare.py, and I ran the suites myself. WHAT THE INSTRUCTION SAID: the captive-4 seats-path exclusion must apply ONLY when the run is a --stops rotate-self, the pre-existing no-flag test must be RESTORED to its pre-SL7.12 assertion, and a new flagged test must carry the exclusion. WHAT THE ARTIFACT DOES: _prepare_checks gained a stops_rotation keyword (rotate.py:9348-9350); the exclusion appending is now wrapped in if stops_rotation (rotate.py:9562-9569); cmd_rotate_self passes stops_rotation=_stops_has at rotate.py:11072-11073, and _stops_has is assigned unconditionally at rotate.py:10933 before the stops branch, so the name always resolves. cmd_prepare was left at the default False. VERIFIED IN THE ARTIFACT, NOT THE REPORT: test_prepare_card_check_reads_the_last_work_commit_only lost the :(exclude)nodes/.geometry/posts.md entry from its spec tuple, and the new test_stops_rotation_flag_controls_seats_exclusion asserts BOTH directions plus, via a spec recorder, that the plain call consults the plain spec and the flagged call consults the flagged one. Both falsifiers are real: with the exclusion un-gated, the restored test asks for a spec key that no longer resolves so check 4 reads ok and its BLOCK assertion fails, and the recorder assertion plain_spec in seen fails after the plain call. RUNS I RAN: pytest tests/test_rotate_prepare.py tests/test_rotate.py tests/test_rotate_handoff_driven.py -q = 260 passed; tests/test_rotate_handover.py tests/test_bin_help_smoke.py tests/test_rotate_selfreap.py tests/test_rotate_g1517.py -q = 125 passed, 3 skipped. NEAR MISS: proving the flag at the _prepare_checks boundary satisfies the words and skips the wiring — if the call site had passed stops_rotation=True instead of _stops_has, every assertion here would still be green. I closed that by reading rotate.py:11072-11073 rather than by test; the kid named the same gap in its own caveats, so it stands as a recorded weakness, not a silent one. CAVEAT CARRIED FROM THE KID, ACCEPTED AS TRUE: the flagged path is not exercised end-to-end through a live rotate-self --stops git fixture. DEVIATION: none; the kid did not edit any pre-existing assertion beyond restoring the one SL7.12 had changed, which is exactly what the claim demanded. evidence_runs is the experiment node itself, permitted for an experiment.
<!-- THOUGHT:END -->
