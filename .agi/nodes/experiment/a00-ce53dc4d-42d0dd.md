---
id: experiment:a00-ce53dc4d-42d0dd
mint_id: 7bf1b108cff74ee7a7da2e10ae8fd2f3
type: experiment
parents:
  - hypothesis:l4-reshuffle-apply-gates-on-origin-new-and-both-delete-old-flags-honour-dry-run
next_edges: []
confidence: 0.9
edited_by: a00-de4869f3
evidence_runs:
  - experiment:a00-ce53dc4d-42d0dd
loop: hypothesis:l4-reshuffle-apply-gates-on-origin-new-and-both-delete-old-flags-honour-dry-run@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7893ca2302ec2b78
season: 2
title: A00 ce53dc4d 42d0dd
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ce53dc4d-42d0dd

## Experiment

KID B (L4.320, region B) — implement both `--delete-old` flags honouring
`--dry-run`, and gate branch-reshuffle's delete on upstream=origin/<new>.
KID A had already landed region A (the `--apply` upstream gate, fixture -u
seeding, master add-only); I built on it and touched none of it.

### Changes to `extensions/agi/bin/cli.py`

**(B1) `cmd_branch_reshuffle` reads `args.dry_run`** (`dry = bool(args.dry_run)`).
The `--delete-old` block now: needs no green-suite stamp when dry (`--dry-run`
bypasses the stamp gate so the real-tree preview works), prints each delete as
`[DRY ] branch delete (remote): git push origin --delete <old>` and runs NONE
(`if dry: continue`), and returns 0 with `dry-run: nothing changed`. A dry pass
never reaches the real delete loop nor the B2 gate.

**(B2) `--delete-old` is gated upstream=origin/<new>.** Before the real delete
loop, every non-master job's `j["new"]` branch must read
`_post_rename_upstream(repo, new) == f"origin/{new}"`. Any that read unset or
the carried `origin/<old>` are refused BY NAME (sorted) and NOTHING is deleted
(all-or-nothing, non-zero). master stays add-only (never a gate target, never
a delete). The gate is skipped only for `--dry-run` (which previews, deletes
nothing).

**(B3) `_post_rename_delete_old` honours `--dry-run`.** New `dry_run` param;
`cmd_post_rename` passes `bool(args.dry_run)`. Prints each delete as
`[DRY ] ...` and runs none, needs no green upstream gate, returns 0 with
`dry-run: nothing changed`. Real delete keeps its upstream gate.

**(B4) `_post_rename_delete_old` collects refusals, is resumeable.** Instead of
`return 1` at the first un-pointed branch, it gathers ALL unpointed names,
deletes what IS gated green, lists the refusals, and returns non-zero only
when any were refused. A branch whose remote ref is already gone is skipped
(via `_post_rename_ls_remote`), so a second run deletes only what remains and
exits 0 when nothing remains.

### Tests (`extensions/agi/tests/test_branch_reshuffle.py`,
`extensions/agi/tests/test_post_rename.py`)

The four pre-existing branch-reshuffle delete tests ran `--delete-old` without
`--apply` first; under B2 that is now a correct all-or-nothing refusal, so I
added `_apply_kinds`/`_apply_all` helpers (migrate first, then delete) and
re-targeted assertions. The post-rename `..._deletes_nothing` test changed
meaning under B4 (green `a` IS deleted now), so it was rewritten, and I added
B1/B3/B4-specific tests:

- `test_delete_old_refuses_by_name_and_deletes_nothing_when_unpointed` (B2
  falsifier — see below)
- `test_delete_old_dry_run_prints_zero_runs` (B1)
- `test_delete_old_dry_run_prints_and_runs_none` (B3)
- `test_delete_old_is_resumeable_second_run_exits_zero` (B4)
- `test_delete_old_refuses_names_branch_and_deletes_nothing` (B4 collect+delete-green)

### Proof (from the parent worktree a00-de4869f3)

    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py -q
    ..................../...  19 passed
    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_post_rename.py -q
    .......................  23 passed
    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli.py -q
    .................../...  19 passed
    $ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_post_rename.py extensions/agi/tests/test_cli.py -q
    61 passed

**Falsifier for B2:** in `test_delete_old_refuses_by_name_and_deletes_nothing_when_unpointed`,
after a full `--apply` the test sabotages `season2/posts/post-a`'s upstream
back to `origin/seat/post-a@s2` and asserts `--delete-old` returns non-zero and
`assert "origin/seat/post-a@s2" in origin` (all-or-nothing: nothing deleted).
Remove the B2 gate, and the delete loop runs for the well-pointed branches —
`origin/seat/post-a@s2` IS deleted even though its branch was never pointed at
the new name, so `"origin/seat/post-a@s2" in origin` FLIPS to `not in`. That
is the assertion that flips when B2's gate is removed.

**REAL-TREE DRY-RUN PASTE** (read-only; both printed `[DRY ]` and changed
nothing; `git ls-remote --heads origin | wc -l` in parens):

    # branch-reshuffle --dry-run --delete-old  (11 before -> 11 after)
    branch-reshuffle (season=2): 5 legacy branch(es)
    [DRY ] branch delete (remote): git push origin --delete seat/sanctuary-director@s2
    [DRY ] branch delete (remote): git push origin --delete seat/sanctuary-helper@s2
    [DRY ] branch delete (remote): git push origin --delete seat/sensei-director@s2
    [DRY ] branch delete (remote): git push origin --delete town/streaming-suite@s2
    [DRY ] branch delete (remote): git push origin --delete town/web-app-suite@s2
    dry-run: nothing changed

    # post-rename --dry-run --delete-old  (11 before -> 11 after)
    [DRY ] branch delete (remote): git push origin --delete seat/sanctuary-director@s2
    [DRY ] branch delete (remote): git push origin --delete seat/sensei-director@s2
    [DRY ] branch delete (remote): git push origin --delete seat/sanctuary-helper@s2
    dry-run: nothing changed

Neither `--apply` nor a `--delete-old` without `--dry-run` was run against the
real tree.

## Evidence

Same content as above; the full transcript of the two real-tree dry-runs ended
`dry-run: nothing changed` with `git ls-remote --heads origin` counting 11 both
before and after each. The three named pytest files pass (61 tests, 0 failures).

THOUGHT: KID A's region-A gate was already the `== origin/<old>` fixture seed;
I did not touch region A. The one ambiguity worth recording: B1 (dry-run
brackets) and B2 (upstream gate) interact — I chose dry-run to bypass BOTH the
stamp gate and the upstream gate so a real-tree read-only preview can never be
blocked by a gate and always prints its `[DRY ]` lines. B2 gates only the real
delete, which is the behaviour the brief's real-tree paste demands (both paste
commands must print `[DRY ]` and exit cleanly on a live tree that is not
gated-green).

## Agent Notes
region B: both --delete-old flags honour --dry-run ([DRY ] print, zero run, real-tree 11->11); branch-reshuffle delete gated upstream=origin/<new> (all-or-nothing refuse-by-name); post-rename delete collects refusals + resumeable. 61 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-de4869f3, L4.320). (1) The brief said: BOTH --delete-old flags must honour --dry-run; reshuffle --delete-old must be gated on EVERY renamed upstream == origin/<new>; post-rename --delete-old must collect refusals and be resumeable. (2) Measured on the built bytes: cmd_branch_reshuffle reads `dry = bool(args.dry_run)` (cli.py:2664); the real delete is gated by a pre-pass collecting every non-master `j["new"]` whose `_post_rename_upstream(repo, new) != f"origin/{new}"`, refusing by name all-or-nothing (cli.py:2756-2775), while the dry path prints `[DRY ] branch delete (remote): ...` and `continue`s before any subprocess (cli.py:2790-2800); _post_rename_delete_old takes dry_run, skips already-absent remotes via _post_rename_ls_remote, collects refusals instead of aborting (cli.py:2326-2382). Real-tree read-only paste: `git ls-remote --heads origin | wc -l` was 11 both before and after each command. I re-ran the three named files myself: 61 passed. (3) Near miss: letting --dry-run reuse the real pass changes NOTHING because the flag would gate only the stamp, not the subprocess; the check that matters is that no `subprocess.run(["git","push","origin","--delete",...])` is reachable while `dry` is true -- it is not. (4) Deviation: KID B chose dry-run to bypass the upstream gate too, so a live-tree preview is never blocked; correct for a read-only preview, but it means the paste cannot distinguish gate present from gate absent -- that distinction rests on the fixture tests, not the real-tree paste. Weakness: the B2 falsifier is asserted from a pasted sabotage transcript, and B4's "delete what is green" changes the meaning of a previously-passing test, which a later reader should re-check against the original intent.
<!-- THOUGHT:END -->
