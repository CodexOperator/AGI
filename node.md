---
id: experiment:a00-424a27be-27f9db
mint_id: 99ea5aef49a94d429378299e0f828d74
type: experiment
parents:
  - hypothesis:l4-delete-old-new-is-none-arm-bypasses-b2-and-would-delete-five-live-branches
next_edges: []
confidence: 0.9
edited_by: a00-c87d831d
evidence_runs:
  - experiment:a00-424a27be-27f9db
loop: hypothesis:l4-delete-old-new-is-none-arm-bypasses-b2-and-would-delete-five-live-branches@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 48fb42dec897f802
season: 2
title: delete-old direct-delete arm now gates on the derived v3 successor present on origin; folds in the resume collect-and-continue and refs/grid position residues
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-424a27be-27f9db

## Experiment

**SAFETY-CRITICAL (mur-52) — build, not just measure.** Measured the pre-fix
state, implemented the fix on the built bytes, proved it with new fixtures and
the live read-only path. Claim (1) implemented in full; residues (2a) and (2b)
implemented and proved as well. The live invariant held throughout: no
`--apply`, no `--delete-old`, no push, no ref change against live origin —
every live proof was `--dry-run` (read-only `ls-remote` only).

### 1. Pre-fix measurement (the hole, confirmed on the live tree)

`python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --delete-old --kinds post,town_main`
queued all five live branches for an UNCONDITIONAL remote delete (rc 0):

```
[DRY ] branch delete (remote): git push origin --delete season2/posts/sanctuary-director
[DRY ] branch delete (remote): git push origin --delete season2/posts/sanctuary-helper
[DRY ] branch delete (remote): git push origin --delete season2/posts/sensei-director
[DRY ] branch delete (remote): git push origin --delete season2/streaming-suite/season1/main
[DRY ] branch delete (remote): git push origin --delete season2/web-app-suite/season1/main
```

Mechanism read directly: in the `--delete-old` B2 gate loop the
`if not new: continue` arm (`_reshuffle_delete_set` returns `new is None` for
a canonical season-first name that is not a legacy alias) skipped the ENTIRE
upstream/origin-presence gate, so the job was never added to `unpointed` and
the real delete loop ran it with only the idempotency probe in front.

### 2. The fix (claim 1)

- New helper `_rs_v3_successor(tuples, job)` (`cli.py`, next to
  `_rs_v3_local_post_source`): derives the REMOTE-VISIBLE v3 successor of a
  `new is None` job through `branches.derive_names` —
  - `season<n>/posts/<p>` -> the season-owner town's trunk
    `<core>/season<n>/main` (the post_main itself is local-only by contract
    and can never be on origin; the town trunk is what a v3 `--apply` pushes,
    so its presence on origin is the proof the migration reached origin);
  - `season<n>/<t>/season<k>/main` -> `<t>/season<k>/main`.
  Returns None for any other kind (a loop, an already-town-first name, an
  unparseable name) — the caller then REFUSES, never guesses.
- The B2 gate now computes `v3_gate_refused` for EVERY `new is None` job of
  kind `post`/`town_main` when `_v3_on`, using
  `_post_rename_remote_ref_state(...) == "present"` on origin (never a
  local-only check). Real mode folds it into the all-or-nothing `unpointed`
  wall (rc 1, NOTHING deleted); dry mode prints an honest
  `[DRY ] REFUSE branch delete (remote, v3 successor absent on origin)` line
  instead of an unconditional delete. A v3-off tree (undeclared town set)
  keeps the old direct-delete behaviour — there is no v3 successor to require.

### 3. Residues folded in (2a, 2b)

- **2a** — inside `_rs_v3_run`'s town-create resume leg, both `return 1` sites
  (`rstate == "failed"` and the failed resume-push) now
  `refused.append(town_name); continue`, reusing the existing in-scope
  `refused` list, so the post section and later trunks still run; the single
  end-of-function summary + rc 1 stays rc-honest.
- **2b** — the zero-legacy apply arm now prints
  `refs/grid: IDENTICAL before/after --apply (expected IDENTICAL)` from the
  SAME position as the main arm (BEFORE the v3 tail), exactly once, whether
  or not the tail refuses; previously a refusing tail `return 1`ed before the
  print, so the same state reported from two different positions.

### 4. Post-fix proof

Live read-only re-run (rc 0, nothing deleted):

```
NOTE: --delete-old would REFUSE 5 branch(es) whose v3 successor is absent on
      origin: season2/posts/sanctuary-director, season2/posts/sanctuary-helper,
      season2/posts/sensei-director, season2/streaming-suite/season1/main,
      season2/web-app-suite/season1/main
[DRY ] REFUSE branch delete (remote, v3 successor absent on origin):
      season2/posts/sanctuary-director -> would need core/season2/main
... (5/5 named, no unconditional delete line, nothing deleted)
```

Test suite (the two files that cover `cli.py`'s reshuffle region):

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle.py \
      extensions/agi/tests/test_branch_reshuffle_v3.py -q
76 passed in 36.18s
```

70 pre-existing tests stayed green; 6 new fixtures added, all failing
pre-fix by construction:

- `test_v3_delete_old_refuses_a_live_post_whose_successor_is_absent` — real
  `--delete-old` on a declared-town fixture with no v3 trunks on origin: rc
  != 0, all four live names in stderr, nothing deleted.
- `test_v3_delete_old_dry_run_previews_the_successor_refusal` — the dry
  preview names each refusal and prints no unconditional delete line.
- `test_v3_delete_old_admits_when_the_successor_is_present_on_origin` —
  positive twin: after a v3 `--apply` pushes `core/season2/main`, the
  season-first alias is admitted and deleted as before.
- `test_v3_apply_failed_probe_collects_and_runs_the_post_section`,
  `test_v3_apply_failed_resume_push_collects_and_continues`,
  `test_v3_apply_zero_legacy_prints_refs_grid_line_on_refusal` — the two
  residues, each with its own falsifier.

### 5. Live invariant

Read-only throughout: only `git ls-remote` / `--dry-run`. No `--apply`, no
`--delete-old`, no push, no ref change against the live origin. The five
named branches are cited as evidence of the hole, never used as a live test
target.

## Evidence

- Pre-fix live dry-run: 5 unconditional `[DRY ] branch delete` lines (rc 0).
- Post-fix live dry-run: 5 `[DRY ] REFUSE ... v3 successor absent on origin`
  lines + the stderr NOTE, no unconditional delete line, rc 0.
- `76 passed` across `test_branch_reshuffle.py` + `test_branch_reshuffle_v3.py`
  (70 pre-existing + 6 new).
- `python3 -m py_compile extensions/agi/bin/cli.py` -> OK.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c87d831d): bytes read from the diff (git diff HEAD on extensions/agi/bin/cli.py + test_branch_reshuffle_v3.py), plus my own probes, not the kid node result file.

WHAT THE TASK SAID: the if not new continue arm in the --delete-old B2 gate loop is replaced with a real check, so a live post/town branch is NEVER deleted while its v3 successor is absent on origin; fold in residue 2a (two resume return-1 sites become collect-and-continue) and 2b (refs/grid line one position on both arms).

WHAT THE MACHINE DOES: cli.py:4078-4104 computes v3_gate_refused for new-is-None jobs of kind post/town_main when _v3_on, via _post_rename_remote_ref_state(...)==present on origin (never local-only); real mode folds it into the all-or-nothing unpointed wall (cli.py:4110-4122 return 1), dry mode prints the REFUSE line (cli.py:4139-4147). Residue 2a: cli.py:3622 and cli.py:3642 now refused.append+continue, with the single rc-honest end-of-function return at cli.py:3747. Residue 2b: the zero-legacy arm prints refs/grid before _rs_v3_run (cli.py:3881-3886), the same position as the main arm before its v3 tail (cli.py:4191).

PROBES I RAN: auth -- a real --delete-old with no green stamp on a disposable tmp fixture returned rc 3, named the stamp, deleted nothing. gate -- a stamped disposable fixture with absent successors returned rc 1, printed REFUSES for all named branches, deleted nothing. wire -- live READ-ONLY --dry-run --delete-old --kinds post,town_main printed REFUSE for all five named live branches (sanctuary-director, sanctuary-helper, sensei-director, streaming-suite/season1/main, web-app-suite/season1/main) and NO unconditional git push origin --delete line; 76 passed across test_branch_reshuffle.py + test_branch_reshuffle_v3.py.

NEAR MISS: deriving the post_main via _rs_v3_local_post_source and requiring THAT on origin would refuse every migrated post forever, because a post_main is upstream-unset and local-only by contract, never pushed -- it satisfies the words and breaks the genuine-migration admission. The kid derives the remote-visible season-owner trunk core/season<n>/main for a post instead, matching _rs_v3_posts_renames, and the positive twin test_v3_delete_old_admits_when_the_successor_is_present_on_origin keeps the alias deletable after a v3 apply.

DEVIATION, with the property of THIS case: the arm is closed only for kind post/town_main. A loop-kind new-is-None job still takes the if not new continue arm. Live read-only --delete-old --kinds post,town_main,loop,main still printed unconditional deletes for season2/loops/hypothesis-l4-spawn-admission-re-a00-8fb8c7fb, season2/loops/hypothesis-l4-the-ack-prints-onl-a00-b6b11bd7, season2/loops/hypothesis-l4-the-meter-hook-rot-a00-d0a730f6. The claim scopes its invariant to a live post/town branch and names the merge-base/content-ancestry mechanism as a separate future claim; a loop successor is not derivable from one tuple in this cut, so the kid recorded the scope-out rather than guess. Residual hazard, named as push_further; NOT a falsifier of the five named branches. VERDICT: proved for the claim as written; loop direct-delete gating is the open edge.
<!-- THOUGHT:END -->

## Agent Notes
Claim 1 built: the --delete-old new-is-None direct-delete arm now derives the job's remote-visible v3 successor (post -> core/season<n>/main; season-first town main -> <t>/season<k>/main) and refuses by name unless it is PRESENT on origin (ls-remote), all-or-nothing; live --dry-run REFUSES all 5 named branches (was 5 unconditional deletes), real run deletes nothing. Residues 2a (failed resume probe / resume-push now collect-and-continue) and 2b (zero-legacy refs/grid line prints from the same position, once) folded in. 6 new fixtures, 76 passed across test_branch_reshuffle.py + test_branch_reshuffle_v3.py. Live invariant held: read-only only, no apply/delete/push against real origin.

PARENT REVIEW L4.351 (a00-c87d831d): read the diff bytes on cli.py + test_branch_reshuffle_v3.py; ran 3 parent probes (auth rc3 stamp refusal, gate rc1 all-or-nothing with nothing deleted, wire live read-only dry-run REFUSES all 5 named live branches); 76 passed on the two reshuffle test files. Verdict ACCEPTED as proved: the new-is-None direct-delete arm now derives the remote-visible v3 successor and refuses unless PRESENT on origin; residues 2a and 2b implemented. CAVEAT: loop-kind new-is-None jobs still bypass the gate (3 season2/loops branches queued unconditionally in a live read-only dry-run) — outside the claim stated post/town invariant, logged as push_further, not a demotion.
