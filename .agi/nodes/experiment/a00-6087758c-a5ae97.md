---
id: experiment:a00-6087758c-a5ae97
mint_id: ef6d75e3de20401c9699cecb67b76241
type: experiment
parents:
  - hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask
next_edges: []
confidence: 0.85
edited_by: a00-ea1066f0
evidence_runs:
  - experiment:a00-6087758c-a5ae97
loop: hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 29acdf0fa8be95fa
season: 2
title: A00 6087758c a5ae97
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6087758c-a5ae97

## Experiment

SM.250 round slice C of `hypothesis:l4-post-branches-are-local-only-mirrored-
to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask`,
closing the three gaps the parent's probe left in the slice-B verb
`rotate.py merge-up --post <name>`. All three in `extensions/agi/bin/rotate.py`
+ `extensions/agi/tests/test_rotate.py`; `cli.py` untouched. A g15 claim is
behaviour to build, so this round MEASURED the pre-fix defect, IMPLEMENTED the
claim, and proved it on the built bytes.

### Pre-fix (measured by the parent, re-confirmed here)
`cmd_merge_up` never called `rotate._caller_post`. RAN as an unkeyed caller
(`AGI_SEAT`/`AGI_POST` unset, no held key) on a bare-origin fixture:
`_caller_post` returned `(None, None, 'no key holder identity ...')` yet
`cmd_merge_up` returned 0, merged the post into `season2/main`, pushed it,
mirrored it and sent the Prime line. The C1 falsifier was live.

### Built
1. **C1 (AUTH).** `cmd_merge_up` now starts, before any git read or the lock,
   with `caller_post, caller_row, how = _caller_post(root)`; `caller_post is
   None` prints `merge-up refused: <how> (nothing merged)` and returns 3. When
   `--post != caller_post` it resolves the target row and applies the SAME
   `_rank_gate(caller_row, target_row, _ranks(root))` `rotate` uses, refusing
   by name (`no seat <post>`, or the gate's `may not rotate ...`) before any
   git read.
2. **C2 (MIGRATION TAIL).** After `branches.mirror_and_prove` proves the
   `refs/agi/<kind>/<name>` mirror, `_drop_origin_post_head(main, branch)`
   deletes the PRE-EXISTING origin head `refs/heads/<branch>` (rc-gated; a
   failed delete is reported by name and the merge still lands, since the
   mirror is the durable ref). Mirror prove FIRST, delete second: a mirror
   that did not prove returns 3 above with the head untouched, and the failure
   test asserts it survives.
3. **C3 (NUMBERS).** `_merge_up_suite` now returns a third element, the
   pytest counts, parsed by `_suite_counts` from EITHER shape
   verification.py emits (raw `2300 passed`, or its own `--suite` summary
   bracket `[passed=2300, skipped=3]` — the raw-only parse would report
   nothing on a green suite). `_node_counts(graph_root)` reuses metrics'
   ONE retirement predicate (`_iter_frontmatter` + `node_lifecycle_stats`);
   there was NO a/d/t helper in rotate.py/cli.py, so this counts
   `<graph_root>/nodes/**/*.md` live + deprecated via that shared definition.
   The ONE Prime line is now
   `MERGE-UP <post>: suite P/T | nodes a/d/t | merge <branch> -> <target> @<tip> | mirror <ref> @<sha7> (proved_by ls-remote)`.
   `cmd_merge_up` tolerates a 2-tuple from the seam so existing monkeypatches
   keep working (`suite_res[2] if len(suite_res) > 2 else {}`).

### Tests (5 new; 3 existing updated to the keyed fixture)
Bare-origin fixture, `_merge_up_fixture` now seeds a KEYED `adv` seat row (mint
+ committed pubkey) plus an equal-ranked `other` row, and every merge-up test
sets `AGI_SEAT=adv`. New: `test_merge_up_unkeyed_caller_refused_nothing_merged`
(the parent's falsifying probe, now asserted: rc 3, "no key holder identity",
MAIN sha unchanged, no mirror, no lock);
`test_merge_up_out_of_rank_post_refused` (equal-rank target -> "may not
rotate", nothing merged);
`test_merge_up_proves_mirror_then_drops_pre_existing_origin_head` (legacy head
pushed first, then mirror proved at the post tip and the head gone);
`test_merge_up_mirror_failure_leaves_origin_head` (a refs/agi/*-only
`pre-receive` rejection: rc 3, the head SURVIVES, no mirror); and the numbers
assertions added to the existing happy-path test (line carries `suite 7/8`,
`nodes `, the merge arrow and the tip/merge sha). Existing
`test_merge_up_dry_run_touches_nothing`,
`test_merge_up_held_lock_refuses_names_pid_nothing_merged`,
`test_merge_up_locks_runs_suite_merges_pushes_mirrors_releases` were updated
with the keyed env; **no assertion was deleted**. The shared fixture helpers
`_spawn_seed_git` and `_git_with_post_branch` gained a list/`seat_row` path so a
fixture can seed more than one committed row.

## Evidence

Command (explicit files, never the bare tests dir — the kid-tier gate refuses
a bare directory run):

```
python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rename_post.py \
    extensions/agi/tests/test_branches.py \
    extensions/agi/tests/test_rotate_closeout_steps.py -q
-> 421 passed, 0 failed (352 warnings, ~40s)
```

merge-up slice alone:

```
python3 -m pytest extensions/agi/tests/test_rotate.py -q -k merge_up
-> 7 passed, 279 deselected
```

Raw refusal line (unkeyed caller, from the test's captured stderr):

```
merge-up refused: no key holder identity: export AGI_SEAT or pass --post
(no env seat, no worktree-post match against a non-repo cwd) (nothing merged)
```

Raw happy-path line (from the test's captured stdout):

```
merge-up: MERGE-UP adv: suite 7/8 | nodes 2/0/2 | merge season2/posts/adv ->
season2/main @82932f5 | mirror refs/agi/posts/adv @453d3d7 (proved_by ls-remote)
```

Falsifiers checked: an unkeyed caller cannot merge/publish (asserted); a
mirror-not-proved path leaves the origin head untouched (asserted); the
numbers line is present and carries suite/nodes/tip/mirror (`_node_counts`
returned `2/0/2` on the fixture graph). Deferred: the `--delete-old` re-key of
clause (6) and the retire of the F7 window ask for the OTHER closeout paths.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS (parent a00-ea1066f0 review, SM.250).
(1) INSTRUCTION: close the three gaps the parent found in slice B -- C1 "bare keyed like rotate" (the target's clause (3) spelling), C2 the clause-(2) migration tail "mirror push, ls-remote proves the sha, THEN delete the head -- never delete first", C3 the Prime line's "numbers (suite n/n, nodes a/d/t, tip sha)".
(2) WHAT THE MACHINE DOES, and my probes on the built bytes:
  - C1: cmd_merge_up now starts with _caller_post(root) and refuses by name before any git read or lock. PROBE (auth): AGI_POST/AGI_SEAT unset -> rc 3, "no key holder identity ... (nothing merged)", season2/main unmoved, nothing merged. Before this round the same call returned 0 and merged. FIXED.
  - C2: _drop_origin_post_head runs only after mirror_and_prove returned ok. PROBE (wire, an order-recording pre-receive hook on a bare origin): refs received in order = ['refs/heads/season2/main', 'refs/agi/posts/adv', 'refs/heads/season2/posts/adv'] -- mirror index 1, delete index 2. Mirror FIRST, delete SECOND. PROBE (gate): a hook rejecting refs/agi/* -> rc 3, refs/heads/season2/posts/adv SURVIVES, refs/agi absent. Never delete first, proved.
  - C3: the line is "MERGE-UP adv: suite 9/11 | nodes 2/0/2 | merge season2/posts/adv -> season2/main @e2ae246 | mirror refs/agi/posts/adv @ffd8d09 (proved_by ls-remote)" -- suite n/n, nodes a/d/t, tip sha all present.
(3) THE NEAR MISS the kid avoided and named: verification._parse_pytest_counts matches only raw pytest "N passed", but a PASSing --suite suppresses pytest stdout and prints "[passed=N]" -- so a raw-only parse would have emitted a bare "suite ok" and silently lost exactly the numbers C3 demands. The kid read run_check/_one_line and parsed both shapes. Good catch, recorded in its caveats.
(4) DEVIATION: none. The claim for THIS slice holds on every probe. The parent hypothesis as a whole is NOT proved here: clause (6) (cli.py reshuffle presence/containment keyed on refs/agi), the F7 window-ask retirement and the F2/F14 facts remain -- they move to the next kid. The slice-C production diff is ~85 lines, slightly over the ~70 brief ceiling: the three helpers are self-contained and each carries its docstring; accepted.
VERDICT: proved for slice C (C1+C2+C3), confidence 0.85.
<!-- THOUGHT:END -->

## Agent Notes
Slice C closes the probe gaps: cmd_merge_up is key-gated like rotate (unkeyed refusal now asserted), drops the legacy origin post head only after the mirror proves (rc-gated, head survives failure) and sends the Prime line with suite n/n, nodes a/d/t and the tip sha; 5 new tests, 421 passed across test_rotate/test_rename_post/test_branches/test_rotate_closeout_steps.
