---
id: experiment:a00-c5bff8fa-52aacb
mint_id: 63bd8cd4a3ef4391929ca6b4fbda68b6
type: experiment
parents:
  - hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin
next_edges: []
confidence: 0.85
edited_by: a00-6e5b8ea4
evidence_runs:
  - experiment:a00-c5bff8fa-52aacb
loop: hypothesis:l4-every-branch-name-derives-from-one-tuple-and-only-the-trunk-pair-per-level-reaches-origin@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 63c39aa047adccf8
season: 2
title: loop-prune + default-kinds delete-kind order (L4.332)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c5bff8fa-52aacb

## Experiment

Built on kids 1 & 2's artifacts (kid 2 EXCLUDED its own stderr `--kinds`
carve-out + the yolo loop-fix bug, so I cleanly re-landed here; the two
accepted kids shipped `branches.derive_names` + `_reshuffle_delete_set`).

### Task 1 — FIX the measured `_rs_delete_kind` segment-order defect (cli.py:2667)

Pre-fix, measured with the parent's exact probes on the built bytes:

    cli._reshuffle_delete_set(heads, {"post","town_main"})  # DEFAULT kinds
      -> ['core/season2/posts/p/main',
          'core/season2/posts/p/loops/L4.332/a00-x']        # a LOOP deleted
    cli._reshuffle_delete_set(heads, {"loop"}) -> []        # never by name

Both directions contradict the HOLD ruling. Cause: `_rs_delete_kind` tested
`"/posts/"` BEFORE `"/loops/"`, and every v3 loop branch `<town>/season<m>/
posts/<post>/loops/<round>/<agent>` CONTAINS `/posts/` (it lives under a
post), so it classified as "post" and the loop branch was unreachable.

FIX: `/loops/` is now tested BEFORE `/posts/`. No v3 loop shape lacks
`/posts/`, so segment ORDER is not segment precedence — loops-first still
resolves every shape. Post-fix probe:

    default kinds {post,town_main} -> ['core/season2/posts/p/main']  (loop gone)
    {loop}                          -> ['core/season2/posts/p/loops/L4.332/a00-x']

### Task 2 — `cli.py loop-prune` (new subcommand; dry-run DEFAULT, --apply to act)

(2a) MERGE-PATH search. Grepped rotate.py, cli.py, post_wire.py, dispatch.py,
season.py for any path that merges a loop branch into its POST branch. The
engine's ONLY loop merge is the SEASON-FIRST harvest — `_fd_next_commands`
prints `git merge --no-ff {branch}` at **rotate.py:11454** — which merges a
`season<n>/loops/<slug>-<agent>` loop into the SEAT branch (first-decision),
never a v3 town-first post main. NO code path anywhere touches the v3
town-first loop shape `<town>/season<m>/posts/<post>/loops/...` (grep for
`derive_names` and `/posts/.*/loops` across the four files: zero hits). So the
ONLY way a v3 town-first loop branch reaches its post main today is the
director's HAND MERGE → task branch (b): I shipped the `loop-prune`
subcommand with the exact rule.

(2b) Rule implemented in `extensions/agi/bin/cli.py`:
* `_v3_loop_post_main(name)` — recognises the v3 loop shape and DERIVES the
  post branch `<town>/season<m>/posts/<post>/main` through
  `branches.derive_names(town, m, post)["post_main"]` — the ONE shape source,
  never hand-spelled a second time.
* `cmd_loop_prune`: for each local+origin v3 loop branch, resolve its sha and
  the post main sha, then `git merge-base --is-ancestor <loop-sha> <post-sha>`.
  rc 0 → merged → may prune; rc 1 → unmerged → NEVER prune, named per branch;
  rc >1 / unresolvable ref → refuse by name, never guess.
* dry-run (DEFAULT) prints the plan and writes NOTHING (no `branch -d`, no
  `push --delete`, no ref change). `--apply` performs the deletes
  (`git branch -d` for a local, `git push origin --delete` for an origin leg
  — non-force, mirroring branch-reshuffle --delete-old), never --force/-f,
  never a master/remote-visible name.

## Evidence

* cli.py `_rs_delete_kind`: `/loops/` now precedes `/posts/` (L4.332 comment).
* cli.py: `_V3_LOOP_RE`, `_v3_loop_post_main`, `_loop_refs`, `_loop_sha`,
  `cmd_loop_prune`, and the `loop-prune` parser entry.
* extensions/agi/tests/test_branch_reshuffle_v3.py — the DISCRIMINATING
  default-kinds tests (kid 2's suite ran all four kinds and could not see
  the default): `test_delete_default_kinds_never_take_a_v3_loop` and
  `test_delete_named_loops_kind_takes_the_v3_loop`.
* extensions/agi/tests/test_cli_loop_prune.py (NEW, 4 tests) — a real fixture
  repo with a BARE origin: merged loop pruned by --apply (local + origin),
  unmerged loop kept (branch existence AND per-branch output line), dry-run
  byte-for-byte unchanged (ref count + branch list + tree digest
  before/after), never --force/-f, and every remote-visible name survives
  (asserted with `branches.is_remote_visible` over the surviving refs).

Summary lines (task's exact command):

    python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
      extensions/agi/tests/test_branch_reshuffle_v3.py \
      extensions/agi/tests/test_cli.py -q
    -> 58 passed in 41.00s

    python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
      extensions/agi/tests/test_branch_reshuffle_v3.py \
      extensions/agi/tests/test_cli.py \
      extensions/agi/tests/test_cli_loop_prune.py -q
    -> 62 passed in 80.03s

No --apply / no prune / no push against the live repo; all mutations ran in
tmp-path fixtures. branches.py, the readers, crons and .agi/nodes/* (beyond
this node) untouched.
<!-- BODY:END -->

## Agent Notes
Fixed _rs_delete_kind /loops/-before-/posts/ (default-kinds delete-set defect) with discriminating tests; shipped cli.py loop-prune (dry-run default, --apply) pruning a v3 town-first loop branch iff merged into its derive_names post main. 62 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6e5b8ea4, L4.332, kid 3/4). ACCEPTED, verdict kept proved — this kid closed the defect I gave it and did not reproduce it. I re-ran both probes myself: `_rs_delete_kind` now returns "loop" for core/season2/posts/p/loops/L4.332/a00-x and "post" for core/season2/posts/p/main; `_reshuffle_delete_set(heads, {"post","town_main"})` — the DEFAULT --kinds set — now returns only core/season2/posts/p/main, and `{"loop"}` returns only the loop head. That is the HOLD ruling honoured in both directions, and the kid added the DISCRIMINATING test I asked for (a test that names all four kinds cannot see the default — that is why kid 2 missed it). `pytest test_branch_reshuffle.py test_branch_reshuffle_v3.py test_cli.py test_cli_loop_prune.py -q` = 62 passed. I read test_cli_loop_prune.py:153-218 and every assertion is real: merged loop gone local AND origin, unmerged loop present AND named per-branch as "unmerged: <b> -> NOT pruned", dry-run `before == after` on the tree digest, no `--force`/`-f`, every surviving name passes branches.is_remote_visible. MERGE-PATH FINDING accepted after I checked the cite myself: rotate.py:11454 is real — `print(f"git merge --no-ff {branch}")` under `verb == "harvest"` — and it merges a SEASON-FIRST loop into the seat branch, so no code path merges a v3 town-first loop into its post main; the director's hand merge is the only one, which is exactly the condition the claim gives for shipping `cli.py loop-prune` instead. The rule is `git merge-base --is-ancestor <loop-sha> <post-sha>`, rc 0 prunes and rc 1 names-and-keeps, which is the claim verbatim. NEAR MISS I checked for: a second hand-spelled v3 loop shape beside the grammar — `_v3_loop_post_main` derives the post through `branches.derive_names(...)["post_main"]` (probed: core/season2/posts/sanctuary-director/loops/L4.332/a00-x -> core/season2/posts/sanctuary-director/main, and a season-first loop returns None), so the ONE tuple stays the source. Caveat carried forward, not a demotion: `loop-prune` exists because no automated v3 harvest path exists — when one is written it must call the same rule rather than grow its own; that is a note for the rename round, not a failure here. NEXT: kid 4 takes the readers + the hand-spelled-shape grep test.
<!-- THOUGHT:END -->
