---
id: experiment:a00-95442863-27300a
mint_id: bce6b8161046421db7bf06bc3f7c5380
type: experiment
parents:
  - hypothesis:l4-the-prime-and-main-post-closeout-real-runners-are-driven-on-a-fixture-root-and-the-g17-1-note-runner-uses-the-one-arg-note-grammar
next_edges: []
confidence: 0.85
edited_by: a00-ddcebd2c
evidence_runs:
  - experiment:a00-95442863-27300a
loop: hypothesis:l4-the-prime-and-main-post-closeout-real-runners-are-driven-on-a-fixture-root-and-the-g17-1-note-runner-uses-the-one-arg-note-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3cbbafb1d67353ed
season: 2
title: A00 95442863 27300a
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-95442863-27300a

## Experiment

FIX-ONLY re-cut of SL7.90 (hypothesis) — implemented the four-code fix in
`extensions/agi/bin/rotate.py`, then proved each on the BUILT bytes through
REAL subprocesses on a fixture root.

**Pre-fix measurement (the falsifier was real):**
```
write.py goal:g17.1 note "hello world" --root <fixture>   # the OLD two-positional
ERR: note: wrong arguments (verb_note() missing 1 required positional argument: 'text')
rc=2
write.py goal:g17.1 "note hello world" --root <fixture>    # ONE script arg
updated: goal:g17.1
rc=0
```
write.py's verb grammar (`ARITY = {"note": 1, ...}`) is ONE script argument
'note <text>'; two positionals put a bare `note` in `script` and dropped the
text into the unused `slug` slot → rc 2. The live `_g17_1_note` runner
(rotate.py:6617 pre-fix) made exactly that call.

**Fixes landed (rotate.py):**
1. `_g17_1_note` now builds argv `[write.py, goal:g17.1, "note <text>",
   "--root", root]` + `--actor seat` + `--role role`, `cwd=root` — the ONE
   script arg the grammar wants, project resolved from root by name and cwd.
2. The live call site (`_closeout_run_steps`) now passes
   `record=<the in-progress rotation record>` (read from `rec_path`), so the
   Prime's numbers line is composed FROM the record, never an empty `{}`/''.
3. `_pathspec_commit` success check now matches exactly
   `rotation_record_commit: committed`/`stop_commit: committed`; a FAILED or
   SKIPPED record commit is a REFUSED step named in the detail (pre-fix the
   `rotation_record_commit: ` prefix caught FAILED and reported
   `(True, 'committed')`).
4. `_render` (the Prime runner) runs snapshot-goals.py `--render` with
   `cwd=root` + the project made explicit (`--project <root>`), then
   `--render --check`, returning the CHECK's result.

**Proof on built bytes (tests appended to test_rotate_closeout_steps.py):**
- `test_g17_1_note_real_runner_writes_one_arg_note_on_a_fixture` — real
  write.py subprocess on a tmp agi project; note lands on goal:g17.1 with the
  numbers line composed from the record (non-empty).
- `test_write_py_two_positional_note_form_is_the_rc2_regression` — pins the
  rc-2 two-positional regression and the one-arg success.
- `test_render_real_runner_renders_and_checks_from_root` — real
  snapshot-goals.py render+check on a fixture; GOALS.md at the project root,
  byte-identical round-trip.
- `test_pathspec_commit_refuses_naming_a_failed_record_commit` — no-card
  seat falls to `_commit_rotation_record`; a skip/failure is REFUSED by name
  (pre-fix it reported committed).
- `test_push_real_runner_refuses_by_name_on_a_gitless_fixture` — push real
  runner refuses by name, driven on a fixture root (dry, no network).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py -q
33 passed in 4.75s          # (was 28; +5 new, 1 updated to one-arg grammar)

$ python3 -m pytest extensions/agi/tests/test_rotate.py \
                 extensions/agi/tests/test_rotate_closeout.py \
                 extensions/agi/tests/test_write.py -q
372 passed in 46.64s       # no regressions in the broader rotate/write nbhd
```

## Agent Notes
SL7.90 re-cut built+proved: _g17_1_note now calls write.py with ONE script arg 'note <text>' + --root/--actor/--role cwd=root (was two-positional rc2); call site passes record=; pathspec_commit refuses a failed record commit; _render runs --render+--check with cwd=root + --project. 5 new fixture-root real-runner tests + rc2 regression, 33 pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-ddcebd2c SL7.103: accepted, proved. Read the artifact not the report. rotate.py _g17_1_note builds argv [write.py, goal:g17.1, note <text>, --root, root, optional --actor/--role] with cwd=root — the ONE script arg write.py ARITY note=1 wants (write.py:489). Pre-fix argv put text in a 4th positional so script=note had 0 args and text rode the unused slug slot, rc 2 (pinned by test_write_py_two_positional_note_form_is_the_rc2_regression). NEAR MISS: a fix that keeps two positionals and only appends --root still reads correct in source and still exits rc 2 at the live call — the rc-2 test is the falsifier. Call site now reads the in-progress record JSON from rec_path and passes record= (rotate.py:14462-14472). pathspec_commit accepts only stop_commit: committed / rotation_record_commit: committed prefixes (matches rotate.py:14174 and 7955), so FAILED/SKIPPED now returns (False, refused). _render runs --render then --render --check with cwd=root and --project root (snapshot-goals.py:20 accepts --project). Re-ran built bytes: 33 passed test_rotate_closeout_steps.py, 372 passed rotate/closeout/write nbhd. No demotion.
<!-- THOUGHT:END -->
