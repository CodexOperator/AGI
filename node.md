---
id: experiment:a00-001606b4-65fedb
mint_id: 7f90f41ff8e5493db3dd126559ff6b59
type: experiment
parents:
  - hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert
next_edges: []
confidence: 0.75
edited_by: a00-b1d92d36
evidence_runs:
  - experiment:a00-001606b4-65fedb
loop: hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1a88b91fcf8600ea
season: 2
title: A00 001606b4 65fedb
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-001606b4-65fedb

## Experiment

Region B — the KIND LOOPS half of hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert. NARROWED first cut: the dry-run loop PLAN only (merged -> would-prune line, unmerged -> NOT pruned, legacy -> HELD BY NAME); no rename of derivable legacy loops, no apply of the loop plan.

Edits to `extensions/agi/bin/cli.py` (branch-reshuffle region only):
- `_LEGACY_LOOP_RE` — the legacy-loop shape regex (`loop/<slug>-<agent>@s<N>` or `season<N>/loops/<slug>-<agent>`); distinct from the existing `_V3_LOOP_RE` (never a second v3 shape regex — the v3 classification reuses `_v3_loop_post_main` exactly).
- `_rs_v3_loops_plan(repo) -> int` — the KIND LOOPS plan. For every branch (local + origin legs from the existing `_loop_refs`) that is a v3 loop shape recognized by the EXISTING `_v3_loop_post_main`, classify by the EXISTING loop-prune rule reusing `_loop_refs`/`_loop_sha`:
  * merged (`git merge-base --is-ancestor <loop-sha> <post-sha>` rc 0) -> `[DRY ] loop prune: <name>` (a plan; never pruned in this cut)
  * unmerged (rc 1) -> `unmerged: <name> -> NOT pruned: <post>` (named, never pruned)
  * rc > 1 / unresolvable ref -> `REFUSE: <name> -> <reason>` on stderr and the plan returns 1 (rc-honest; never a guess)
  Every OTHER loop branch (legacy shapes `_v3_loop_post_main` returns None for) is printed `HELD BY NAME: <name>` with a one-line reason that its post/round are not derivable from a single town tuple in this cut (the narrowing of the target's "rename when derivable from the session record" clause is recorded, not silently dropped). No push line is ever emitted for a loop; no loop is mutated even under --apply.
- `_rs_v3_run` internal kinds guard now includes `"loop"`; a `--kinds ...loops` section emits the loop plan; the three call-site guards (`no legacy jobs` early-return, the dry PLAN section, and the apply tail) include `"loop"` so `--kinds loops` actually reaches the plan.

Tests added to `extensions/agi/tests/test_branch_reshuffle_v3.py`:
- `_v3_loops_repo(tmp_path)` — `_v3_repo` plus a v3 post_main, a MERGED v3 loop (branch at the post_main's own commit => ancestor), an UNMERGED v3 loop (a divergent fork commit, not an ancestor), and two LEGACY loop branches.
- `test_v3_loops_plan_merged_unmerged_held_by_name` — asserts (a) merged -> `[DRY ] loop prune: <name>`, (b) unmerged -> `unmerged: <name> -> NOT pruned: <post>` and the branch survives, (c) legacy loops -> `HELD BY NAME`, no push/delete of a v3 loop name.
- `test_v3_loops_dry_run_writes_nothing_changes_no_ref` — `--dry-run --kinds main,posts,towns,loops` leaves `git for-each-ref` byte-identical and the sessions dir free of plan JSON (the WAIT/EVIDENCE for the dry-run-writes-nothing clause).

## Evidence

Suite: `python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_branch_reshuffle_v3.py -q`
-> `48 passed` (was 46 before this cut; the two new loop tests added). test_cli.py has no branch-reshuffle coverage (`-k kinds|reshuffle|dry_run|delete|v3` -> 19 deselected), so the two reshuffle files are the whole cli-change surface.

Real-tree dry-run (from this round's worktree, NOT --applied, nothing written):
`python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --kinds main,towns,posts,loops`

The KIND LOOPS plan on the live tree:
```
  v3 loop plan (dry-only; never mutates a loop in this cut):
HELD BY NAME: loop/hypothesis-harvest-table-subcomm-a00-26e81f42@s2 (legacy loop; its post/round are not derivable from a single town tuple in this cut — rename deferred, never touched)
HELD BY NAME: season2/loops/hypothesis-l4-the-meter-hook-lat-a00-59a0a441 (legacy loop; its post/round are not derivable from a single town tuple in this cut — rename deferred, never touched)
...
```
Counts: 454 branches HELD BY NAME (all legacy `loop/*@s2` + `season2/loops/*`), 0 merged v3 loops, 0 unmerged v3 loops, 0 REFUSE. This is correct: the live tree still carries only legacy loop branches (v3 town-first loop branches do not exist until the v3 apply runs), so merged/unmerged v3 classification is exercised by the tmp fixture, and everything the live tree does have is named HELD BY NAME and never touched. The live `season2/loops/hypothesis-l4-the-meter-hook-*` heads cited by the node are correctly HELD.

The dry-run WRITES NOTHING: the loop plan emits no push/delete, the code writes the plan file only under --apply or an explicit --plan-out (Region A invariant, unchanged), and the fixture test proves refs and sessions dir stay byte-identical.

## Verdict justification

The dry-run KIND LOOPS PLAN lands and is fixture-proven (merged-unmerged-legacy classification exact, nothing written, no mutation). BUT the full hypothesis sentence has two halves that this cut does NOT build: (1) renaming unmerged DERIVABLE legacy loops to their v3 post loop home (deliberately narrowed to HELD BY NAME here — the session-record derivation is a future cut), and (2) applying the loop plan / the whole v3 apply (Region A landed apply for main/towns/posts; loop apply is not built). So the claim is not fully proved; it is a strong, measured-lean_proved.

## Agent Notes
Region B: dry-run KIND LOOPS plan lands in cli.py (_rs_v3_loops_plan reusing _v3_loop_post_main/_loop_refs/_loop_sha: merged->[DRY] loop prune, unmerged->NOT pruned named, rc>1/unresolvable->REFUSE+exit1, legacy loop/*@s2 + season<N>/loops/*->HELD BY NAME, no push line, never mutates even under --apply). Fixture-proven in test_branch_reshuffle_v3.py (_v3_loops_repo merged/unmerged/legacy + write-nothing byte-identical). Live dry-run: 454 HELD, 0 merged/unmerged/refuse. 48 pass. NOT built: rename of unmerged derivable legacy loops and loop apply -> lean.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (L4.334): accepted lean_proved:75, NOT proved. (1) WHAT THE BRIEF SAID: region B narrowed to the dry-run KIND LOOPS plan -- merged loop -> a would-prune line, unmerged -> NOT pruned and named, rc>1/unresolvable ref -> REFUSE + exit 1, every legacy loop branch (loop/<slug>-<agent>@sN or seasonN/loops/<slug>-<agent>) -> HELD BY NAME and never touched; --dry-run still writes nothing; fixture test; real-tree dry-run pasted. (2) WHAT THE MACHINE ACTUALLY DOES: cli.py:3125 _rs_v3_loops_plan reuses the EXISTING _v3_loop_post_main for the v3 shape and the EXISTING _loop_refs/_loop_sha plus the same git merge-base --is-ancestor probe that cmd_loop_prune uses, with a new _LEGACY_LOOP_RE for the legacy shapes only; _rs_v3_run and its three call-site guards now include loop. The parent re-ran the broad touched surface (branch_reshuffle, branches, branch_spelling_grep, towns, no_literal_town, cli, crons, crons_mirror): 255 passed in 27.06s. (3) THE NEAR MISS: a plan that pruned in dry mode, or that classified an unmerged loop as mergeable, would satisfy the words and lose the "never pruned while unmerged" rule; the fixture asserts the unmerged branch SURVIVES and the merged one is named. A second hand-written v3 loop regex would have satisfied "classify loops" and lost the one-shape-source rule; the code reuses _v3_loop_post_main. (4) DEVIATION DECLARED AND ACCEPTED: the "rename an unmerged loop when post and round derive from the round session record" half is deliberately narrowed to HELD BY NAME, because that derivation is data-dependent and was not in the kid budget; the node records the narrowing rather than hiding it. (5) WHY 75 AND NOT PROVED: the loop plan never mutates even under --apply, and the derivable-legacy-loop rename is unbuilt, so the target KIND loops sentence is only half built. The live dry-run showed 454 branches HELD, 0 v3 loops, 0 REFUSE -- correct, because v3 loop branches do not exist until the v3 apply runs.
<!-- THOUGHT:END -->
