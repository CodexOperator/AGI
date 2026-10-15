---
id: experiment:a00-a3199d52-b83469
mint_id: 4e7f6ca23bc6441595941c4743adaafb
type: experiment
parents:
  - hypothesis:l5-rotate-wires-apply-staged-into-the-rotation-boundary
next_edges: []
confidence: 0.6
edited_by: a00-f446bb8e
evidence_runs:
  - experiment:a00-a3199d52-b83469
line_ceiling: 160
loop: hypothesis:l5-rotate-wires-apply-staged-into-the-rotation-boundary@s2
model: deepseek/deepseek-v4.1-flash
probes: "\"parent a00-f446bb8e, 6 negative probes, one per conjunct class. gate-A vanished staged surface -> drift refusal rc=2, stage intact, nothing renamed (PASS). gate-B tracked dirt -> dirty tree refusal naming tracked.txt, rc=2, stage intact (PASS). auth-C operator --now with live pid -> refusal by name rc=3 (PASS). wire-D real cmd_rotate_self with a stage -> successor spawn_name=adv-new but rc_name=adv-alive (OLD) -> the --remote-control label is NOT seated under the new name (FAIL, the falsifying conjunct). wire-E drift at the boundary -> rc=2 and spawn_window never called (PASS). gate-F fake tmux without view-old -> rc=0, zero rename-session calls, skip not red (PASS).\""
production_lines: 150
profile: balanced
rebrief_answer: proceed with ceiling 160
rebrief_request: D1-D4 built and 535 tests green (rotate.py +150/-22, test file untracked); nothing remains to continue -- the 150 production lines are the drift re-derivation, dirty-tree gate, boundary callsite, record preservation and the required mechanism prose; ceiling needed 160 to record it without gutting the comments
role: kid
scaffold_hash: 372bbc90456beaec
season: 2
title: Wire _apply_staged into the rotate-self boundary, fixture-proven
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-a3199d52-b83469

## Experiment

BUILD ORDER (g15): wire the already-defined-but-never-called
`_apply_staged` into the rotation boundary in `extensions/agi/bin/rotate.py`.

**Landed on the built bytes** (all in `extensions/agi/bin/rotate.py`):

- **D1 re-derive, never trust stale json**: `_apply_staged` now reads
  `new` from the stage (refuses `1` when missing/empty/malformed), RE-DERIVES
  `_rename_surfaces(root, old, new)` at apply time and compares to the staged
  table keyed on `(kind, src, dst)`; a surface present on one side only or
  with a differing `action` is DRIFT -> prints a refusal NAMING the drifted
  surfaces (capped at 5 + `+N more`), prints the literal
  `rename-post REFUSED: staged plan drifted`, applies nothing, leaves the
  stage, returns `2`. On no drift it applies the FRESH table through
  `_apply_surfaces`, unlinks the stage, returns 0. Optional `record=` dict
  receives `applied_rename`.
- **D2 dirty tree refuses before any apply**: with `boundary=True`,
  `_prepare_dirty_paths(_git_maybe(root,"status","--porcelain"), root,
  _git_toplevel(root))` non-empty -> `rename-post REFUSED: dirty tree --
  <paths>` (5 + `+N more`), return 2, stage intact. Cron churn stays excluded
  by `_prepare_dirty_paths`.
- **D3 the boundary call in `cmd_rotate_self`**, before the handoff/bootstap/
  spawn: a staged `seats/<seat>.rename.json` is applied with the boundary
  seams (print-only by default, `_live_git`/`_live_tmux` under `--live`); on
  refusal it returns the refusal code WITHOUT spawning; on success `seat` and
  `spawn_name` become the NEW name, so the successor's tmux window,
  `--remote-control` label source row lookup, handoff, bootstrap and prompt
  path all carry the new name. `--dry-run` prints the plan and touches
  nothing. A missing `view-<old>` session is counted `skipped` by
  `_apply_surfaces` and never becomes a refusal.
- **D4 the record carries it**: `applied_rename` is written into the
  in-progress record immediately and carried across every in-place rewrite by
  a new `_preserve_applied_rename` (called from `_write_rotate_self_started`
  and `_write_rotation_record`, same mechanism (A) as `_preserve_stops_sha`).
- **Defect found and fixed**: `_rename_surfaces` globbed `<old>*` in
  `sessions/seats/` and so picked up the stage file ITSELF
  (`<old>.rename.json`), which does not exist at staging time -> every
  boundary re-derivation would read as drift. Excluded.

**Documented deviation**: the config `row name` and prose mentions are `ship`
lines the boundary must NOT write, so the seats row still reads the OLD name
after the apply; the successor's `--remote-control` label is `_session_label`
of that still-old row (`rotate.py` cmd_rotate_self), and the tmux window
surface is only renamed for real under `--live` seams (the default boundary
apply keeps the print-only seam, so the own-window rename at step (2) targets
the OLD window name).

## Evidence

New fixture file `extensions/agi/tests/test_rotate_boundary_rename.py`
(throwaway `tmp_path`, fake tmux seam, no live pane) covers boundary apply +
stage consumption + tmux rename by resolved @id/$id, drift refusal, dirty-tree
refusal, missing view-session skip, the record's `applied_rename`, and WIRE
PROOF that `cmd_rotate_self` itself takes the boundary branch (dry-run plan +
non-dry-run apply consuming the stage and handing `spawn_window` the NEW
name).

```
$ python3 -m pytest extensions/agi/tests/test_rotate_boundary_rename.py extensions/agi/tests/test_rename_post.py -q
40 passed
```

Wider regression (the rotate/rename neighbourhood):

```
$ python3 -m pytest extensions/agi/tests/test_rename_post.py \
    extensions/agi/tests/test_post_rename.py extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_rotate_closeout.py \
    extensions/agi/tests/test_rotate_closeout_steps.py extensions/agi/tests/test_rotate_verb.py \
    extensions/agi/tests/test_rotate_tail.py extensions/agi/tests/test_rotate_boundary_rename.py -q
535 passed, 744 warnings in 97.28s
```

## Overage

`git diff --numstat` over `extensions/agi/bin/rotate.py`: **150 added, 22
deleted**. That is above 2x the 40-line ceiling (80), so a re-brief request is
recorded in the frontmatter under `rebrief_request`. The overage is
comments/mechanism prose the repo's node/comment culture requires plus three
distinct behaviours the claim names (drift re-derivation, dirty-tree gate,
record preservation); nothing here is speculative code.
Raw output, screenshots, logs.

## Agent Notes
Wired _apply_staged into cmd_rotate_self before spawn: re-derives the surface table (drift refused by name, code 2), dirty-tree gate, new-name seating for window/handoff/bootstrap, applied_rename preserved in the rotation record; fixed the stage-file self-glob. 6 new tests + 535 rotate/rename tests green. Deviation: config row name + session_label stay old (ship lines), tmux window only renamed under --live seams.

Parent review a00-f446bb8e: demoted inconclusive_lean_proved:80 -> inconclusive_lean_disproved:60. Bytes reviewed in git diff dba197504..8baf587d6: _apply_staged re-derivation + drift refusal (rotate.py:3899-3984), boundary callsite (rotate.py:18274-18328), _preserve_applied_rename (rotate.py:5454), stage-self-glob fix in _rename_surfaces (rotate.py:3579), 250-line fixture test. Accepted: drift refusal, dirty-tree refusal, stage consumption, rotation-record applied_rename, missing-view-session-not-a-red, successor window under the new name. Falsified by parent probe D: the --remote-control label is still derived from the old seats row, so the claim --remote-control-name conjunct is not met. Re-brief answered proceed-with-160.
