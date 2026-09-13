---
id: experiment:a00-2613edf9-0c4744
mint_id: 63a137e5f2d54a17880f1d66f515f550
type: experiment
parents:
  - hypothesis:l4-branch-reshuffle-apply-collect-refusals-and-continue-on-a-moving-tip
next_edges: []
confidence: 0.65
edited_by: a00-6885fe15
evidence_runs:
  - experiment:a00-2613edf9-0c4744
loop: hypothesis:l4-branch-reshuffle-apply-collect-refusals-and-continue-on-a-moving-tip@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe A: tmp fixture (bare origin, town set {core@2, streaming-suite@1, web-app-suite@1}); local core/main pre-created at a throwaway ORPHAN commit (divergent, not an ancestor); every other planned trunk absent; `cli.py branch-reshuffle --apply --kinds main,posts,towns`.", "expected": "rc != 0; the ERR names core/main; every OTHER planned trunk-pair still created locally AND pushed; core/main never force-moved; no --force/-f.", "observed": "rc=1; refused_named=True; created=['core/season2/main','streaming-suite/main','streaming-suite/season1/main','web-app-suite/main','web-app-suite/season1/main'] == 5/5 expected; core/main left at the orphan sha; no force token.", "result": "HOLDS. Within the town loop the abort is gone and every later town is still created."}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe B (the claim's named scenario): core/main created at the OLD season2/main tip, then season2/main ADVANCES by a real merge-up commit, then a resumed `--apply --kinds main,posts,towns`.", "expected": "The run survives the moved tip: the remaining towns' trunk-pairs are created though core/main now reads wrong.", "observed": "tip moved b4e68868->d5815046; rc=1; core/main left at the old tip; remaining_created_local == remaining_created_remote == all 5 remaining targets at the planned tips.", "result": "HOLDS. The moved tip no longer kills the remaining trunk creates."}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe C (ADVERSARIAL, the falsifier): _v3_apply_repo fixture (town set + both v3 post source branches season2/posts/sanctuary-director|helper and their worktrees); core/main at a throwaway wrong tip; run `--apply --kinds main,posts,towns`.", "expected": "The delete-old pattern is 'the run CONTINUES to the next one; refusals are collected and the exit is non-zero only if any' -- so a refused trunk must not stop the sections AFTER the town loop: the v3 post renames must run and 'apply: local renames ... done' must print.", "observed": "rc=1; post_section_ran=False; post_renames_done=[]; 'apply: local renames' absent; the two core/season2/posts/<post>/main branches never created. The summary's `return 1` at the END OF THE TOWN BLOCK aborts everything after it.", "result": "FAILS THE CLAIM. Once season2/main has moved, core/main stays at the old tip (never force-moved by design) and EVERY retry returns 1 at the same place, so the v3 post renames can never run. The title claim ('--apply survives a moving season2/main tip') is not delivered by these bytes. Root cause is the brief, not the kid: the brief itself said 'at the END of the town_main block ... return 1'. Closing round: experiment:a00-04369518-4515b9 (kid a00-04369518) moves the summary+exit to the end of _rs_v3_run."}
  - {"conjunct": 2, "class": "gate", "cmd": "PARENT probe D: zero-legacy repo (no master, jobs==[]) with a declared town set; `cli.py branch-reshuffle --apply --kinds towns`.", "expected": "The refs/grid IDENTICAL|CHANGED line prints on the zero-legacy apply path.", "observed": "rc=0; 'no legacy branches to reshuffle' present; 'refs/grid: IDENTICAL before/after --apply (expected IDENTICAL)' present.", "result": "HOLDS. L4.340's residue is fixed on this path."}
  - {"conjunct": 2, "class": "wire", "cmd": "PARENT probe E: non-zero-legacy repo; `--apply --kinds main,posts,towns`; count the refs/grid lines.", "expected": "The main apply path still prints the line EXACTLY once (no double print from the new zero-legacy arm).", "observed": "rc=0; grid_line_count=1.", "result": "HOLDS."}
  - {"conjunct": 2, "class": "gate", "cmd": "PARENT probe F: repo with a wrong-tip core/main; `--dry-run --kinds main,posts,towns`.", "expected": "--dry-run is untouched: no refusal text, no summary, no refs/grid line (the collection is `not dry`-gated).", "observed": "rc=0; refused_in_dry=False; summary_in_dry=False; grid_line_in_dry=False.", "result": "HOLDS."}
profile: balanced
push_further: "An ancestor/behind tip is currently classified wrong exactly like a divergent one, so after a merge-up a legitimately created trunk keeps the run at rc 1 forever (the claim mandates refusal+no-force-move, so this is its edge, not its defect). A successor should distinguish behind (ancestor of the planned tip: fast-forward or skip-with-notice) from divergent (refuse by name), and should also consider whether R3.1s ls-remote-failed refusal deserves the same collect-and-continue depth."
role: kid
scaffold_hash: 8a7de37e2c2658cd
season: 2
title: A00 2613edf9 0c4744
town: core
verdict: inconclusive_lean_disproved:65
---
# experiment:a00-2613edf9-0c4744 — R3.2 build + falsifier proof

## Experiment

R3.2 (target `hypothesis:l4-branch-reshuffle-apply-collect-refusals-and-continue-on-a-moving-tip`)
is a BEHAVIOUR TO BUILD, not a hypothesis to measure. Two changes, both in
`extensions/agi/bin/cli.py`; three falsifier tests + three supporting tests in
`extensions/agi/tests/test_branch_reshuffle_v3.py`. No other file. No live
tree, no push to a real remote — every apply ran cwd-bound in a tmp fixture
with a disposable bare `origin`.

### Fix 1 — trunk-create WRONG-TIP collects refusals and CONTINUES
Pre-fix the wrong-tip arm in `_rs_v3_run`'s town_main block did `return 1` on
the FIRST wrong town, so one divergent trunk aborted the create of every later
town's trunk-pair: an earlier merge-up moves the planned tip (tip = local
`season2/main`), a trunk legitimately created at the OLDER tip reads wrong, and
the whole `--apply` died there. Rewritten to the `--delete-old` pattern exactly:

* `refused: list[str] = []` opened at the top of the town_main block
  (`cli.py:3519`, in the bytes changed);
* wrong-tip arm at `cli.py:3574-3583`: same ERR wording, `refused.append(...)`,
  `continue` — NEVER `return 1`, NEVER a force-move;
* end-of-block summary `cli.py:3603-3609`:
  `ERR: v3 town creates: N trunk(s) refused: ...` then `return 1` if any.
R3.1's `resume_state == "skip"` arm and its three states are UNCHANGED.

### Fix 2 — zero-legacy apply prints the refs/grid line
The zero-legacy apply arm returned before the shared `grid_before`, so
`refs/grid: IDENTICAL|CHANGED before/after --apply (expected IDENTICAL)` never
printed there. Now `grid_before` is taken at `cli.py:3797`, `grid_after` at
`cli.py:3800`, and the SAME one-line message prints at `cli.py:3802`. The main
apply path still prints it exactly once.

## Evidence

### Pre-fix FAILING run (defect measured, not assumed)
`python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -q -k
"wrong_tip_trunk_collects or wrong_tip_summary or zero_legacy_prints or
main_path_prints or never_forces"`
-> `3 failed, 3 passed` — the wrong-tip collect/continue pair and the
zero-legacy refs/grid line all fail on the unbuilt bytes. The zero-legacy
failure is literal: stdout had NO `refs/grid:` line at all.

### Post-fix pass (same command)
`6 passed, 31 deselected`.

### Full suite of the two touched/covering files
`python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py
extensions/agi/tests/test_branch_reshuffle.py -q`
-> `67 passed in 44.34s` (32+29 pre-existing + 6 added).

### --dry-run byte-identity (before vs after the fix)
Same tmp fixture, `branch-reshuffle --root <r>/.agi --dry-run --kinds
main,posts,towns` captured pre-fix and post-fix:
`diff /tmp/dryrun_prefix.txt /tmp/dryrun_postfix.txt` -> empty
(`DRY-RUN BYTE-IDENTICAL`), stderr also byte-identical. The collect/continue
logic is `not dry`-gated, so dry output carries no refusal text.

### New falsifiers
1. `test_v3_apply_wrong_tip_trunk_collects_refusals_and_continues` — core/main
   pre-created at a throwaway orphan commit; asserts rc != 0, `REFUSED` +
   `core/main` + `DIFFERENT tip` in stderr, EVERY other planned trunk created
   locally AND pushed, and core/main still at the wrong sha (never force-moved).
2. `test_v3_apply_wrong_tip_summary_names_every_refusal` — two towns wrong at
   once: one summary line names both, third town still created.
3. `test_v3_apply_zero_legacy_prints_the_refs_grid_line` — marker present and
   `stdout.count("refs/grid:") == 1`.
4. `test_v3_apply_main_path_prints_the_refs_grid_line_once` — main apply path
   still exactly one line.
5. `test_v3_trunk_create_never_forces` — source check on the town_main block:
   no `--force`, no `-f` token, no `branch -f`, no `push -f`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one: the kid's version carried its own build report; THIS version is the tier-parent's review of it, written after reading the changed BYTES (the staged diff of cli.py's `_rs_v3_run` town_main block + the zero-legacy apply arm, and the 6 added tests in test_branch_reshuffle_v3.py) and after running six independent probes of my own (/tmp/probe_r32.py, /tmp/probe_r32b.py) rather than re-running the kid's suite. What the review found:

(1) WHAT THE INSTRUCTION SAID. The target's claim: "the trunk-create/apply path's wrong-tip case needs to collect-refusals-and-continue, matching the delete-old leg's existing pattern (cli.py:3966-3970 and :4003-4007), because the planned tip is `season2/main` and it moves at every merge-up -- a fixed-tip assumption is a real race", title "branch-reshuffle --apply survives a moving season2/main tip via collect-refusals-and-continue", plus the folded-in L4.340 residue: the zero-legacy apply path returns before `grid_before`, so the refs/grid IDENTICAL|CHANGED line never prints.

(2) WHAT THE MACHINE ACTUALLY DOES, cited to the bytes I read and the probes I ran. Conjunct 2 is delivered: cli.py:3789-3803 takes grid_before around the zero-legacy `_rs_v3_run` call and prints the same one-line message; PARENT probe D (zero-legacy `--apply --kinds towns`) prints it, probe E (non-zero-legacy apply) counts exactly one, probe F (`--dry-run`) shows no new text. Conjunct 1 is delivered ONLY WITHIN THE TOWN LOOP: the wrong-tip arm at cli.py:3574-3583 appends to `refused` and `continue`s, but the summary at cli.py:3603-3609 does `return 1` at the END OF THE TOWN BLOCK, so every section after it -- the v3 post renames -- is skipped. PARENT probe C measured exactly that on a fixture with the two v3 post sources pending: rc=1, post_section_ran=False, post_renames_done=[], `apply: local renames ...` absent. Probes A and B hold (a divergent core/main and a genuinely moved season2/main both leave every OTHER town's trunk-pair created and pushed, core/main never force-moved).

(3) THE NEAR MISS -- the plausible implementation that satisfies the words and loses the mechanism. Collecting refusals inside the town loop and exiting at the end of that loop reads as "matching the delete-old pattern" because the delete-old loop IS its function's whole job; in `_rs_v3_run` the job stream is towns -> posts -> notice -> loops, so the summary belongs at the end of the STREAM. Located in the town block, the exit is permanent and unrecoverable: core/main is never force-moved, so it stays at the old tip after any merge-up and every retry returns 1 at the same place -- the v3 post renames can then never run, which is the precise opposite of the title's "`--apply` survives a moving season2/main tip".

(4) DEVIATION, AND WHOSE. The kid did not misread: the parent's own brief said "at the END of the town_main block, if `refused` is non-empty, print one summary line naming every refused branch and `return 1`". So the defect is the BRIEF's scope, and the correct parent action is adjust-and-re-spawn, not blame. The verdict is nevertheless a lean_disproved rather than a proved because a verdict describes the CLAIM, not the kid: the claim's title is not delivered by these bytes. No hand-edit was made to the code by the parent; the correction is a fresh kid (experiment:a00-04369518-4515b9) building on these bytes.

(5) OPEN BOUNDARY (not a falsification, recorded for the next round): an ANCESTOR/behind tip (a trunk legitimately created at the older season2/main) is classified `wrong` the same as a DIVERGENT one, so after a merge-up the run exits 1 forever even once the post section runs. The claim mandates refusal-and-continue and never a force-move, so this is the claim's edge, not its defect -- push_further for R3.2's successor.
<!-- THOUGHT:END -->

## Agent Notes
R3.2 built: trunk-create wrong-tip collects refusals and CONTINUES (cli.py:3519/3574-3609, no force, rc-honest summary), zero-legacy apply prints refs/grid line (3797-3802). 3 falsifiers failed pre-fix, 6/6 pass post-fix; 67 passed over both reshuffle test files; dry-run byte-identical.

PARENT REVIEW L4.348 (a00-6885fe15): verdict LEAN_DISPROVED 65 -- the kid's `proved` is DEMOTED, and the demotion names PARENT probe C. Read the staged bytes (cli.py:3512-3612 town_main refusal collection, cli.py:3789-3803 zero-legacy refs/grid line; 6 tests added in test_branch_reshuffle_v3.py) and ran six independent probes (`probes:` in frontmatter), never the kid's suite. HOLDS: A (divergent core/main -> other 5 trunk-pairs still created+pushed, no force), B (a REAL moved season2/main tip -> run survives), D (zero-legacy apply now prints refs/grid IDENTICAL), E (main apply path prints it exactly once), F (--dry-run gains no refusal/summary/grid text). FAILS: C -- with a wrong-tip core/main and the two v3 post sources pending, the refusal's `return 1` at the end of the TOWN BLOCK skips the v3 post section entirely (post_section_ran=False, post_renames_done=[], 'apply: local renames' absent), so after any merge-up the apply exits 1 forever and the post renames can never run. Root cause is the parent brief's scope ('at the END of the town_main block ... return 1'), not a kid misread. Correction in flight: experiment:a00-04369518-4515b9 (kid a00-04369518) moves the summary+exit to the end of _rs_v3_run. Boundary for the successor: a BEHIND (ancestor) tip is classified `wrong` like a divergent one, so the run exits 1 forever even once the post section runs.
