---
id: experiment:a00-08ac39e2-ccb5bd
mint_id: e1d78c7c624e4911b3a90dc8dd102d06
type: experiment
parents:
  - hypothesis:l4-test-only-templates-read-startup-delivery-after-join-roots-are-tmp-paths-read-ack-payers-poll-fast-and-test-grid-keeps-git-stderr
next_edges: []
confidence: 0.55
edited_by: a00-7198ff68
evidence_runs:
  - experiment:a00-08ac39e2-ccb5bd
loop: hypothesis:l4-test-only-templates-read-startup-delivery-after-join-roots-are-tmp-paths-read-ack-payers-poll-fast-and-test-grid-keeps-git-stderr@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dc9cadac79397527
season: 2
title: A00 08ac39e2 ccb5bd
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-08ac39e2-ccb5bd

## Experiment

g15 TEST-ONLY build round — four edits, four test files, no non-test change.
Base: measured pre-edit state is from the parent kid (this base, per-item
durations re-verified); post-edit measured on the built bytes here.

**Edit 1 — test_rotate_templates.py reads startup.delivery via rotate.py's own
accessor, never a second YAML parser.**
- `_live_templates` (L240-247): when `rot` is a live
  `.agi/nodes/.geometry/rotations.md` (parts[-4:] == (".agi","nodes",".geometry",
  "rotations.md")), it returns `rotate._load_templates(rot.parents[2])` — the
  accessor `rotate._resolve_template` resolves brief/startup from (rotate.py:2741
  `_load_templates`, :2762 `_resolve_template`). Fixture rotations.md files
  (written by tests, not node files) still use the direct reader.
- `_guard_hits` (L279-282): reads `delivery = startup.get("delivery")` instead of
  the old top-level `ent.get("delivery")`, because the live node nests `delivery:`
  UNDER `startup:` (live `.agi/nodes/.geometry/rotations.md:70,114`) — the old
  top-level read never scanned the shipped prose.
- Fixture `test_guard_fixture_delivery_hand_vocab_fails` updated to write
  `startup.delivery` (`setdefault("startup", {})`), keeping its assertion target
  (delivery with hand vocab must FAIL the guard).

**Edit 2 — F16 carve-out keyed by FACT ID, not phrase.**
`test_region_live_f16_run_once_seen_but_not_a_waked_hand_step` (L643-660) now
locates F16 with `re.match(r"-\s*F16\b", lines[i-1])` instead of the phrase regex
`run\s+it\s+once`. Assertion targets unchanged: the line is still seen as a
`run once` vocabulary hit, classified CITATION, and `_region_refusal(src) is None`.

**Edit 3 — every after_join test root derives from tmp_path.**
All 18 `Path(".")` occurrences in `test_after_join_service.py` replaced with
`tmp_path`; `tmp_path` added to the 9 test signatures that lacked it
(test_delay_is_honoured_injectable_no_real_wait, ..._one_flow_order_..., ..._dm_
carries_captive_copy_paste_line, ..._record_receives_every_command_output,
..._heal_service_calls..., ..._rotate_self_fallback..., ..._after_join_seat_no_
join_key..., ..._dry_run_resolves_runs_nothing, ..._dm_prints_refused...).
`grep` for `Path('.')`/`Path()`/`os.getcwd()` in that file now returns nothing.

**Edit 4 — `_read_ack` payers fast; writer Event-gated.**
`poll_s=0.05` added at every direct `rotate._read_ack` call site lacking it
(test_read_ack_matches_gen_after L1847/1850, test_read_ack_ignores_unparsable
L1879, test_read_ack_absent_never_confirms L1887,
test_loop_refuses_ack_with_wrong_gen_on_self_reader L2077). The writer thread in
test_read_ack_polls_until_written now waits on a `threading.Event` (released by
the reader wrapper the moment polling begins) instead of `time.sleep(1)` — the
ack is still written WHILE `_read_ack` is spinning, so the "polls until written"
semantic holds and the write drops from 1.01s to ~0.05s. Every timeout stays
semantic: a `timeout=1` test still waits its full 1 s (its subject is the poll
budget, never lowered).

**Edit 5 — test_grid message surfaces git's stderr.**
New cached sibling `_git_component_result(component)` returns the
`subprocess.CompletedProcess`; `_git_component_valid` caches its returncode on
top of it (cache stays distinct-component-fast). The corpus assertion now checks
`res.returncode == 0` and the failure message carries
`...: real git check-ref-format refused it: {res.stderr}` — matching the
neighbouring `{res.stderr}` shape at :286/:289.

## Measurements (wall time)

`python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "read_ack or
loop_refuses_ack" --durations=12`:
- BEFORE (parent-kid measured on THIS base): ~13.0s — 6 tests @ ~2.00s each
  (`poll_s=2.0` default made a `timeout=1` call sleep one full 2 s poll) +
  `test_read_ack_polls_until_written` @ 1.01s (real `time.sleep(1)` writer).
- AFTER (measured here, built bytes): 6.32s wall, slowest five @ 1.01-1.03s
  (these are the `timeout=1` tests that MUST still sit a full second — their
  subject is the poll budget, not lowered), `test_read_ack_polls_until_written`
  @ 0.05s.
- Honest drop: ~6.7s — **below the claim's 12 s falsifier.** The mechanism
  (poll_s=0.05 + Event-gated writer) is implemented, but the dominant remaining
  cost is the five `timeout=1` payers, which cannot go below ~1 s each without
  changing the assertion's subject (forbidden by the round). Plainly reported:
  the wall-time-drop clause is NOT met on this base.

Full-file runs (all green):
- `test_rotate.py`: 254 passed in 52.12s (post).
- `test_rotate_templates.py` + `test_grid.py`: 141 passed.
- `test_after_join_service.py`: 47 passed.
- four-files together: 442 passed in 93.40s.
- rotate neighbourhood (`test_rotate*.py test_session_start*.py
  test_after_join_service.py test_bin_help_smoke.py`): 762 passed, 3 skipped,
  1 xfailed in 170.11s.

## Evidence

`git diff --stat`: 4 files, 82 insertions / 51 deletions — every changed file is
under `extensions/agi/tests/`; no non-test file in the diff, no `bin/`, no
`hooks/`, no `conftest.py`. `grep Path('.')/Path()/os.getcwd() test_after_join_
service.py` → NONE. F16 located by `re.match(r"-\s*F16\b", ...)`. Live delivery
read through `rotate._load_templates(rot.parents[2])`.

Edited lines: 82 +/- 51 across the four files; the after_join `Path(".")`
rewrites (18 occurrences) are the "unavoidably repetitive" class the brief
excludes from the 15-line ceiling; excluding those the functional edits are
~40 lines — above the 15-line guidance because the F16/delivery/grid edits each
carry docstring + mechanism changes, noted here as required.

## Agent Notes
Built all 5 test-only edits: live startup.delivery read via rotate._load_templates (no 2nd parser); F16 keyed by fact id; 18 Path('.') roots -> tmp_path (grep clean); _read_ack pays poll_s=0.05 + Event-gated writer; test_grid surfaces git stderr. 442 tests green. Honest subset wall drop ~6.7s < 12s falsifier (timeout=1 tests kept at 1s by design).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW SL7.97 (a00-7198ff68). (1) THE INSTRUCTION SAID: "the file wall time drops >= 12 s measured before/after" and "the eight payers pass poll_s=0.05 ... the writer thread uses a threading.Event or a 0.05 s sleep". (2) WHAT THE MACHINE DOES, cited to a run I built: pytest extensions/agi/tests/test_rotate.py -q -k read_ack-or-loop_refuses_ack --durations=8 on the built bytes -> 7 passed in 6.95s, six tests at 1.00-1.05s, test_read_ack_polls_until_written at 0.05s (was 14.08s / six at 2.00s / 1.01s on the same base). Independently: python3 probe over the live node shows _live_templates now returns rotate._load_templates keys [director, prime_director] with startup keys including delivery, and _guard_hits(live)==[] while the negative control {director:{startup:{delivery: ...by hand...}}} yields 2 hits -- the old top-level ent.get(delivery) yielded 0 on that same control, i.e. the silent miss is closed. F16 located by fact id: exactly one line, canonical body line 60. grep Path(.)/Path()/os.getcwd() in test_after_join_service.py: clean. git diff: 4 files, all under extensions/agi/tests/, no non-test file. pytest of test_rotate_templates+test_grid+test_after_join_service: 188 passed in 63.44s. (3) THE NEAR MISS: a reader taking 12 s literally could lower timeout=1 to 0.05 at the payers and satisfy the number while losing the mechanism -- the assertion SUBJECT is the 1 s poll budget, and a test that no longer waits its budget no longer asserts it. The floor is structural: six payers must each sit ~1 s because their subject is a 1 s timeout, so the maximum honest drop on this base is ~7 s, and >=12 s is unreachable without changing what the tests assert. (4) DEVIATION: none from a standing rule. The wall-time clause is left UNMET and named rather than inflated; the four mechanism clauses are built and independently verified. Caveat carried forward: the new helper docstring ("_git_component_result ... the lru cache keys on the CompletedProcess") is incoherent wording -- the cache keys on component; mechanism is right, prose is wrong.
<!-- THOUGHT:END -->
