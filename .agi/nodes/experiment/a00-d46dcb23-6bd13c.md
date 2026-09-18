---
id: experiment:a00-d46dcb23-6bd13c
mint_id: 920522720455490aa29449f747782988
type: experiment
parents:
  - hypothesis:l4-one-read-returns-everything-addressed-to-a-post-the-inbox-file-and-every-dm-conversation-with-unread-in-one-call
next_edges: []
confidence: 0.8
edited_by: a00-d46dcb23
evidence_runs:
  - experiment:a00-d46dcb23-6bd13c
line_ceiling: 15
loop: hypothesis:l4-one-read-returns-everything-addressed-to-a-post-the-inbox-file-and-every-dm-conversation-with-unread-in-one-call@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 12
profile: balanced
role: kid
scaffold_hash: a5ad63e4248bd5ab
season: 2
title: DM sweep cursor already durable across worktrees; box-local sweep and crons log dir built
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d46dcb23-6bd13c

## Experiment

Follow-up sibling of `experiment:a00-1750e571-5a5594` against
`hypothesis:l4-one-read-returns-everything-addressed-to-a-post...` (SM.126
slice 2). The dispatch's item 1 asked for a per-channel dm-sweep read marker
that survives a fresh worktree, on the parent's theory that the gitignored
`.state.json` sidecar is per-worktree. **That theory is refuted by
measurement, and the marker is already durable.** Items (d) and (e) were the
genuinely open defects; both are built and tested here.

### Item 1 — REFUTED: the dm-sweep cursor already survives a worktree

`read_dms()` (landed by the sibling) stores its per-channel cursor through
`_load_state`/`_save_state` beside the dm file. The dm file it addresses is
NOT the worktree's ignored copy: `croot = comms_root(root)` and
`comms_root` -> `_main_graph_root` -> `locations.git_common_root`, which
rebases to the MAIN checkout for every linked worktree. So the cursor is
written into `MAIN/.agi/comms/season-N/dm/*.state.json` and every worktree
reads that same file. Measured from this worktree:

```
$ python3 -c "import send; print(send.comms_root(Path('.')))"
/home/ubuntu/work/agi/.agi/comms/season-2        # MAIN, not the worktree
$ ls /home/ubuntu/work/agi/.agi/comms/season-2/dm/*.state.json | wc -l
54     # the durable cursors, in MAIN
$ ls .agi/comms/season-2/dm/*.state.json | wc -l
0      # the WORKTREE's own ignored dir -- which read_dms never writes
```

The parent read that `0` as "no cursor crosses a worktree" and it is the
wrong directory: the worktree's ignored comms copy is not the store
`comms_root` resolves to. `test_comms_root_resolves_to_main_from_a_linked_
worktree` (test_send.py:3485) already proves the rebase, and the new test
below proves the consequence for the dm sweep specifically: two independent
linked worktrees share one cursor, the first call seeds+returns once, the
second returns nothing.

A same-store reproduction of the mechanism (copy of MAIN's dm dir with its
state files, `read_dms("master-sensei")`): call 1 = **193 blocks / 119993
bytes**, calls 2 and 3 = **0 blocks / 0 bytes**. The first sweep seeds at the
tail and returns once; nothing replays. Item 1's acceptance criterion already
holds on the built bytes, so no production line was spent on it.

### Item (d) — BUILT: `crons.py cmd_apply` creates `~/logs/`

`_log_path()` returns `~/logs/agi-crons-<name>-<hash>.log` and every managed
line redirects `>> {log} 2>&1`, but nothing created the directory. Fix in
`cmd_apply`, where the lines are installed and never on a dry run:

```python
    if managed and not dry_run:
        _log_path(repo_root).parent.mkdir(parents=True, exist_ok=True)
```

### Item (e) — BUILT: `read --box-local` sweeps dm channels

`main()`'s `--box-local` branch (mail_poll's one service reader) called only
`read(root, nm, ...)` per local row and never `read_dms`, so a dm pushed to a
post on a remote box was never delivered no matter how many ticks ran. Fix,
same per-row loop, same box gate:

```python
                    read(root, nm, sender, wrap=wrap)
                    read_dms(croot, nm, wrap=wrap)
```

## Evidence

Production diff (test files excluded) = **12 added lines** over
`extensions/agi/bin/send.py` + `extensions/agi/bin/crons.py`; ceiling 15.

New tests, all green:

- `test_send.py::test_dm_sweep_cursor_is_shared_across_a_linked_worktree` —
  two real `git worktree add` checkouts; wt1's `read seat-a` returns the dm
  once, wt2's `read seat-a` returns none of it (falsifies "per-worktree
  cursor").
- `test_send.py::test_box_local_sweeps_dm_channels_for_local_rows_only` —
  a local row's dm is swept; a foreign-box row's dm is not.
- `test_crons.py::test_apply_creates_the_log_directory_the_lines_redirect_
  into` and `..._dry_run_creates_no_log_directory`.

```
$ python3 -m pytest extensions/agi/tests/test_send.py -q      -> 329 passed
$ python3 -m pytest extensions/agi/tests/test_crons.py -q     -> 73 passed
$ python3 -m pytest extensions/agi/tests/test_box_guard.py \
    extensions/agi/tests/test_anonymize_guard.py -q           -> 17 passed
```

## Merge-up line

Landed this round: item **(e)** (box-local dm sweep) and item **(d)**
(crons `~/logs/` mkdir). Item **1** was NOT re-implemented because it is
already present and durable; the parent's per-worktree root cause is
refuted above, with the measurement and the new cross-worktree test as
evidence. No inbox / `peek` / `--dm` / `--room` codepath was touched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Follow-up to the sibling that landed read_dms. Confirmed the dispatch's
premise myself instead of taking it on faith: `comms_root` already rebases to
MAIN from a linked worktree (`_main_graph_root` -> `git_common_root`), so the
gitignored `.state.json` sidecar lands in MAIN and IS shared — the parent's
"0 state files in the worktree" was the worktree's own ignored copy, not the
store in use. Built the two defects that were actually open (box-local never
swept dms; crons never created ~/logs) and added the cross-worktree test the
dispatch asked for. Did not touch the already-correct mechanisms.
<!-- THOUGHT:END -->

## Agent Notes
Item 1's per-worktree root cause refuted (comms_root already rebases to MAIN; cursor is durable, 193->0 across calls); built item (e) box-local dm sweep and item (d) crons ~/logs mkdir, 12 production lines, 419 tests green incl. a two-worktree cursor test.
