---
id: experiment:a00-ccab16ad-03d9b3
mint_id: cf4171d333544e9aa94f19c93acd7f51
type: experiment
parents:
  - hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer
next_edges: []
confidence: 0.75
edited_by: a00-ccab16ad
evidence_runs:
  - experiment:a00-ccab16ad-03d9b3
line_ceiling: 45
loop: hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 45
profile: balanced
role: kid
scaffold_hash: 7c68f27df788b29a
season: 2
title: SM.123 slice 4 -- fixes the five mur residues on the migrate receive path (worktree identity, fork threshold, stage compat, crash-free tick, scp path deferred)
town: core
verdict: inconclusive_lean_proved:78
---
<!-- BODY:BEGIN -->
# SM.123 slice 4 -- the five mur-sm-123-s2-c3 residues, fixed on the round's own bytes

## Experiment

Slice 3 is on HEAD (merged cb10774d4): the box-scoped two-live guard, the
non-numeric-pid skip, the fork-without-session-id refusal, and
`transcript_from_registry_dict` for the transcript path all hold. Do not
rebuild them. This round answers the five NEW residues mur found on top.

1. **R1 target worktree identity (FIXED).** `_migrate_seat` created
   `root/worktrees/<post>` (bare post name) and its returned cells omitted
   `worktree`, so a moved post kept the SOURCE box's stale cell,
   `_seat_worktree_cwd` resolved nowhere, the post read as MAIN and the NEXT
   rotation silently ran in MAIN. Now the seating uses the REAL convention
   `<main>/.agi/worktrees/post-<seat>` (`_fd_seat_worktree`,
   `.agi/nodes/.geometry/posts.md` rows) and returns
   `"worktree": ".agi/worktrees/post-<post>"` so `_write_identity_cells`
   overwrites the stale cell. New test
   `test_receive_marks_the_moved_post_as_a_worktree_never_main` drives the
   REAL `git worktree add` through `cmd_migrate_receive` and asserts the
   captured cells carry the cell, the row is NOT a main post
   (`bool(row) and not row["worktree"].strip()` is False), and
   `_seat_worktree_cwd` resolves the directory.

2. **R2 the fork threshold can now choose fork end to end (FIXED, option a).**
   `_migrate_default_mode` returns fork on a low meter, but `cmd_migrate`
   refused any fork without `--session-id`, and the meter is only the chooser
   when `--mode` is omitted (which has no `--session-id`). Chosen fix: the
   **auto-mode path supplies the post's own live session id** -- the thing a
   fork exists to resume -- from `_migrate_row(...).session_id`. An explicit
   `--mode fork` still refuses by name when no id is available. The node's
   `testable_claim` is unchanged because the claim (conjunct 3: fork chosen
   on a low meter) is now true as written; tested by
   `test_auto_mode_fork_supplies_the_posts_own_session_id` and
   `test_auto_mode_fork_with_no_session_id_anywhere_is_refused`.

3. **R3 stage-absent compat on receive (FIXED).** The slice-1 writer's
   `_KEYS` had no `stage`; `parse_record` required it, so an un-upgraded
   source box's record would be silently dropped. `parse_record` now reads a
   stageless record as `request`; `verify_record` parses the RAW frontmatter
   (`_parse_fm`) and chooses the canonical key order by whether `stage` is
   present, so a legacy-signed record still verifies while a STAGED record
   can never verify under the legacy order (otherwise a `seated` ack could
   relabel as `request`). Zero live records exist today, so this is a
   forward-compat guard, not a data migration. Tested by
   `test_a_stage_absent_record_is_read_as_a_request_and_verifies`.

4. **R4 the receive tick is crash-free (FIXED).** `subprocess.run(argv,
   cwd=str(wt))` raised `FileNotFoundError` when `git worktree add`
   (check=False) left the worktree absent, aborting the WHOLE tick. The
   `_migrate_seat` call is now wrapped: an `OSError` skips THIS record by
   name and the tick lives for the next. Tested by
   `test_receive_skips_a_record_it_cannot_seat_without_killing_the_tick`
   (record `p` raises, record `q` still seats).

5. **R5 fork transcript scp path (DEFERRED, named).** See Boundary.

Measured production lines: `git diff --numstat` over the two production
paths = 23 added (migrate_channel.py) + 22 added (rotate.py) = **45**, at the
45-line ceiling. No test file lines are counted.

## Evidence

All commands were run in this worktree on branch
`season2/loops/hypothesis-l4-quick-migrate-one--a00-f2f90804`, over the
round's OWN production bytes (`extensions/agi/bin/rotate.py`,
`extensions/agi/bin/migrate_channel.py`). Unlike the slice-3 residue, nothing
here depends on a config or geometry file this round cannot commit: the round
carries both production files, and every assertion reads tmp trees or the
live rotations node (already committed at e60e19e4d).

```
$ python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q
27 passed in 1.09s

$ python3 -m pytest extensions/agi/tests/test_crons.py \
    extensions/agi/tests/test_crons_mirror.py extensions/agi/tests/test_send.py \
    extensions/agi/tests/test_bin_help_smoke.py -q
493 passed, 4 skipped in 39.72s

$ git diff --numstat -- extensions/agi/bin/rotate.py extensions/agi/bin/migrate_channel.py
23	7	extensions/agi/bin/migrate_channel.py
22	6	extensions/agi/bin/rotate.py
```

The complicit config residue on this feature -- `migrate_fork_below` in
`.agi/nodes/.geometry/rotations.md` -- was landed by the director at
e60e19e4d (`git show HEAD:...rotations.md | grep -c migrate_fork_below` = 1),
so `test_live_rotations_node_declares_the_fork_threshold` is now green from
committed bytes, not a dirty worktree.

## Boundary

R5 (deferred, third pass): the fork transcript `scp` source path
(`_migrate_copy_transcript`, `rotate.py` ~20497) assumes the source and target
worktree absolute paths are identical, so a source box rooted elsewhere
copies nothing. Fixing it means carrying the source cwd in the record (a
`_KEYS` change, which moves the signed canonical) or a dedicated
source-cwd field; it is out of a 45-line round and is NOT fixed here.
Tracking: this line is the third consecutive disclosure, per
mur-sm-123-s2-c3 review D3.

Forward compat note: `stage` is in the current writer's `_KEYS`, so once both
boxes run this module no stageless record is produced; R3 only covers the
rolling-upgrade window.

## Agent Notes
SM.123 slice 4: R1 worktree identity fixed (.agi/worktrees/post-<seat> + worktree cell returned, real-git test asserts NOT main), R2 auto-mode fork supplies the post's own session_id (explicit --mode fork still refuses by name), R3 stage-absent record read as request with legacy-order signature verification, R4 receive tick skips an OSError seating by name and lives, R5 scp source-cwd path named and deferred a third time with a Boundary tracking line. Production lines 23+22=45 at ceiling. test_migrate_channel.py 27 passed; crons+crons_mirror+send+bin_help_smoke 493 passed/4 skipped.
