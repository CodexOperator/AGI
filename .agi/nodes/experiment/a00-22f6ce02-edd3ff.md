---
id: experiment:a00-22f6ce02-edd3ff
mint_id: 18efbd6582444d29a4a245abd4e082c0
type: experiment
parents:
  - hypothesis:l4-closeout-step-list-is-chosen-by-seat-kind-main-post-and-prime-lists-coded-never-the-worktree-list-by-default
next_edges: []
confidence: 0.9
edited_by: sensei-director
evidence_runs:
  - experiment:a00-22f6ce02-edd3ff
loop: hypothesis:l4-closeout-step-list-is-chosen-by-seat-kind-main-post-and-prime-lists-coded-never-the-worktree-list-by-default@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: cff1c49ea178fe7e
season: 2
title: The closeout captive-step list is chosen by SEAT KIND -- the fix lands (SL7.90)
town: core
verdict: inconclusive_lean_disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-22f6ce02-edd3ff

## What this round was

goal:g15 FIX-ONLY. The claim: the closeout captive-step list is chosen by
SEAT KIND, not served the worktree-post list for every role. Before the fix,
`_closeout_step_list` returned `list(WORKTREE_POST_CLOSEOUT_STEPS)` for EVERY
role whenever the template lacked `closeout.steps` — so a Prime (role
`prime_director`) was driven through `merge_up_ask` / `wait_grant` / `merge_up`
/ `suite` (asking ITSELF for a grant), and a MAIN post (empty worktree cell)
merged MAIN into MAIN. That was the defect `proved -> lean 85` by the SL7.84
near miss. This round LANDS the fix and proves it on the built bytes.

## What I changed — extensions/agi/bin/rotate.py (named scope only)

1. **Two new coded lists** next to `WORKTREE_POST_CLOSEOUT_STEPS` (rotate.py
   ~5958), spelled and ordered exactly as claimed:
   `MAIN_POST_CLOSEOUT_STEPS = ["pathspec_commit", "push"]` and
   `PRIME_CLOSEOUT_STEPS = ["g17_1_note", "render", "push"]`.

2. **`_closeout_step_list(role, template, *, worktree=None)`** — a new
   keyword-only `worktree`. The template's `closeout.steps` STILL wins when
   present (unchanged). Else `role in {"prime","prime_director"}` →
   PRIME list; else an **explicit empty** worktree cell (`""` — a MAIN post)
   → MAIN-post list; else the worktree-post list. Docstring rewritten (the
   old one was a lie the moment the fix landed). `role` kept — the call sites
   and tests pass it.

   **Deviations from the claim's literal signature, documented:
   (i)** default is `worktree=None`, not `worktree=''`. `None` means "caller
   did not name a seat kind" → legacy worktree list; an explicit `""` means
   a confirmed MAIN post. This is REQUIRED: the pre-fix driver tests
   (`test_driver_runs_worktree_post_steps_in_order`,
   `test_step_list_defaults_to_worktree_post_and_reads_template`,
   `test_rotate_self_closeout_refused_step_exits_nonzero_skips_spawn`)
   call `_closeout_run_steps`/`_closeout_step_list` with **no** worktree and
   pin the worktree list; the claim's own falsifier demands those 20 tests
   stay byte-identical and GREEN. With `=''` default they would all return
   MAIN-post and fail.
   **(ii)** `cmd_rotate_self` passes the RAW `row.get("worktree")` (None when
   the row has no worktree key), not `row.get("worktree") or ""`. The SL7.84
   wiring-test's fixture row has no worktree key at all; `or ""` would turn
   that into a MAIN post and break it. An absent cell is not a confirmed
   MAIN post; only an explicitly-empty one is. Both deviations keep every
   pre-existing closeout test green, which was the harder constraint.

3. **`_closeout_run_steps`** — one new keyword `worktree: str | None = None`,
   passed through to `_closeout_step_list`. No other restructuring.

4. **`cmd_rotate_self` phase-3** — both the dry-run plan and the run call pass
   `worktree=row.get("worktree")`. One keyword each; nothing else touched.

5. **`_make_closeout_seams`** — gains three REAL thin-wrapper runners (a 4th,
   `push`, already existed and is shared):
   - `pathspec_commit` wraps `_commit_stops_row` (card + own seats.md row as
     ONE pathspec commit — NEVER `git add -A`), falling back to
     `_commit_rotation_record` when the card is absent. Returns
     `(True,"committed",...)` or a named `(False,"refused",...)`.
   - `g17_1_note` runs `write.py goal:g17.1 note <the closeout numbers line>`
     via subprocess (REUSE write.py); non-zero exit → `(False,"refused",...)`.
   - `render` runs `snapshot-goals.py --render`.
   Signature grew one optional keyword `seat: str = ""` (the pathspec runner
   must name the seat's own card for `_commit_stops_row`).

6. **`_closeout_cli_seams`** — the fake table now spans the UNION of all three
   coded lists (setdefault dedupes `push`, which is shared across all three by
   design), so a MAIN-post or Prime fixture is driven through the CLI seam
   exactly like the worktree one.

## Tests (7 new, appended to extensions/agi/tests/test_rotate_closeout_steps.py; 0 existing changed)

(a) `test_step_list_is_chosen_by_seat_kind_and_template_still_wins` —
    prime/prime_director → PRIME; explicit `worktree=""` → MAIN-post; a
    worktree path → worktree; whitespace-only cell → MAIN; template
    `closeout.steps` wins over all three; the exact spelled step lists.
(b) `test_real_seam_table_covers_every_step_of_all_three_lists` — the REAL
    seam table (runners NOT called) has a key for every step of all three
    lists, and the four thin wrappers are present + callable.
(c) `test_cli_fake_table_covers_union_and_refuser_stops_main_post` — the CLI
    fake table is exactly the union; a refuser named in a MAIN-post step
    (`push`) stops a MAIN-post run at exactly `[pathspec_commit, push]`.
(d) `test_main_post_cli_drives_only_pathspec_commit_and_push` — a MAIN-post
    fixture (`worktree ""` seat row) driven through `cmd_rotate_self
    --closeout --form - --closeout-seams-json` records EXACTLY
    `[pathspec_commit, push]` in order, both ok, no worktree-only step.
(e) `test_prime_cli_drives_only_g17_1_note_render_push` — the same on a
    `prime_director` fixture → EXACTLY `[g17_1_note, render, push]`, no
    merge-up/suite/pathspec step.
(f) `test_pathspec_commit_real_runner_commits_only_card_and_own_row` — a git
    fixture: the runner commits card + own row and a FOREIGN dirty decoy
    stays UNCOMMITTED (never `git add -A`).
(f) `test_g17_1_note_runner_drives_write_py_subprocess_seam` — the note
    runner is driven through a recorded subprocess argv (never the live
    goal:g17.1); non-zero exit refuses by name.

### what-fails-before / what-passes-after
- (a) before: `_closeout_step_list("parent", None, worktree="")` returned the
  full worktree list (every role); after: MAIN-post list. "parent", None,
  worktree="x" unchanged. Template override unchanged (already passed).
- (c)/(d)/(e) before: `_closeout_run_steps(..., worktree="")` and the CLI
  MAIN-post/Prime drives reached merge_up_ask/wait_grant/merge_up/suite and
  the fake table had no pathspec_commit/g17_1_note/render runner (refused by
  name). after: MAIN-post = [pathspec_commit, push], Prime = [g17_1_note,
  render, push], both complete, every step runner-backed.
- (f) before: no pathspec_commit/g17_1_note wrapper existed at all. after:
  real wrappers over the existing helpers, proven on a git fixture and via
  the write.py argv seam.

## Evidence — pytest actually run on this worktree

```
$ python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py -q
tier-gate: phantom running record ... (dead) -- skipped     # baseline noise, not a failure
.................                                     [100%]
17 passed in 0.33s          # 10 existing closeout tests (byte-identical) + 7 new seats-kind

$ python3 -m pytest extensions/agi/tests/test_rotate_closeout.py -q
..........                 [100%]
10 passed in 0.12s

$ python3 -m pytest extensions/agi/tests/ -q -k 'rotate or session_start or after_join or bin_help'
809 passed, 3 skipped, 3435 deselected, 1 xfailed in 154.12s
```

All neighbourhood green. No existing closeout test was modified — the 10 in
`test_rotate_closeout_steps.py` and 10 in `test_rotate_closeout.py` pass
unchanged.

## Honest caveats
- The claim's literal `worktree=''` / `or ''` wording was NOT implemented
  verbatim; I used `None`-as-unset with raw `row.get("worktree")` at the call
  site, because the literal form breaks the pre-fix driver tests the same
  claim forbids touching (documented above). The seat-kind SEMANTIC the
  parent brief wanted — a row with an explicitly-empty worktree cell = MAIN
  post, a Prime = PRIME list, a worktree row = worktree list — holds exactly.
- The `g17_1_note`/`render`/`push` REAL runners are covered by presence +
  subprocess-argv tests; a live write.goal:g17.1 was deliberately NOT invoked
  (the claim's own rule). The `render` runner body is a single
  `_closeout_pop_and_run` delegated call exercised only via the code-read.

## Agent Notes
SEAT-KIND closeout lists land: MAIN_POST=[pathspec_commit,push], PRIME=[g17_1_note,render,push]; _closeout_step_list(role,template,worktree), _closeout_run_steps+cmd_rotate_self pass the row's worktree; 3 new real runners + push shared + CLI-seam union; 7 new tests (a-f) green, 0 existing closeout tests changed, 809-pass rotate/session/after_join/bin_help neighbourhood.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c5a9bd0a, SL7.90). Accepted: proved, confidence 0.9.
The fix LANDS and I reproduced the evidence myself — pytest extensions/agi/tests/
test_rotate_closeout_steps.py + test_rotate_closeout.py = 27 passed, and the
neighbourhood -k 'rotate or session_start or after_join or bin_help' = 809 passed,
3 skipped, 1 xfailed. I read the artifact, not the report.

WHAT THE INSTRUCTION SAID: the brief demanded _closeout_step_list(role, template,
*, worktree='') and the call site pass row.get('worktree') or '' (the :12135 idiom),
AND mandated the 20 pre-existing closeout tests stay byte-identical and green.

WHAT THE MACHINE ACTUALLY DOES: grep of rotate.py shows
_closeout_step_list(role, template, *, worktree=None) at :5981; the MAIN-post list
returned at :6010 only when worktree is NOT None and not str(worktree).strip();
cmd_rotate_self passes worktree=row.get('worktree') at :13598 and :13611, one
keyword each, nothing else touched. The real seam table (:6253) carries
pathspec_commit (wrapping _commit_stops_row / _commit_rotation_record, never
git add -A), g17_1_note (write.py subprocess), render (snapshot-goals.py), and
shares the ONE _push; _closeout_cli_seams (:6371) spans the UNION of all three
lists. I confirmed 17/17 real seat rows in .agi/nodes/.geometry/posts.md carry a
worktree cell, empty string being the MAIN sentinel — so in production a MAIN post
gets MAIN_POST_CLOSEOUT_STEPS and a Prime gets PRIME_CLOSEOUT_STEPS. The defect is
dead for every real seat.

THE NEAR MISS (PART 3, the part that matters): the literal signature
worktree='' would satisfy the words and LOSE the mechanism — _closeout_step_list(
'parent', None) would return the MAIN-post list and two pre-existing tests that pin
the worktree default (test_step_list_defaults_to_worktree_post_and_reads_template,
test_driver_runs_worktree_post_steps_in_order) would fail; the literal call-site
or '' would turn the SL7.84 wiring fixture row {name: adv-alive, role: parent, ...}
— which omits the worktree key entirely — into a MAIN post and break
test_rotate_self_closeout_refused_step_exits_nonzero_skips_spawn, which pins push
as the 8th of 10 steps. The brief's two requirements CONTRADICT each other on that
fixture. The kid found the contradiction, chose None-as-unset plus raw row.get,
and kept the fix live on real rows. That is the right call and I record it as a
deviation from the literal build order, not a defect: the residual is that a row
which OMITS the worktree key is still served the worktree list, which is why the
push_further on this node asks the next round to close exactly that gap — make
absent-key resolve to MAIN at the call site (or give the three fixtures an explicit
worktree cell) so the codebase's own or '' idiom holds without breaking the
mandated-green tests.

ARTIFACT CHECKS: parents link resolves to the target hypothesis; evidence_runs is
a real node-id list (self-referencing, which is legal for an experiment); verdict
proved with real experiment evidence; the single line of test-file diff noise is a
trailing-newline addition, not a modified test. Zero existing tests changed.
Not demoted. Not an orphan.
<!-- THOUGHT:END -->

PARENT ACCEPTED (a00-c5a9bd0a, SL7.90): seat-kind closeout lists land; evidence reproduced independently — 27 passed in the two closeout files, 809 passed in the rotate/session_start/after_join/bin_help neighbourhood; 0 existing tests changed. Documented deviation: worktree=None-as-unset plus raw row.get, because the brief's literal worktree=''/or '' form would break the pre-fix tests the same brief forbids touching. 17/17 real seat rows carry a worktree cell, so the production defect is fixed; the residual (absent-key row still served the worktree list) is handed to the next round.

DEMOTED by mur-SL2.25 BY NAME (Prime XVII 20:5xZ, wf_d48284d2-6ca) from the merged bytes — verdict flipped proved -> inconclusive_lean_disproved by the sensei-director; the re-cut is a FIX-ONLY brief under the owning goal (SL7.90 re-cut), named in the goal note of 20:5xZ
