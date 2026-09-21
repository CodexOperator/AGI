---
id: experiment:a00-f067c356-b0ad80
mint_id: 2cc83c459b894596b0627a2755489784
type: experiment
parents:
  - hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit
next_edges: []
confidence: 0.7
edited_by: a00-19566029
evidence_runs:
  - experiment:a00-f067c356-b0ad80
line_ceiling: 120
loop: hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "sensei._audit_floors('floor_wake: abc\\nfloor_out: 7\\n') and _audit_floors('') at the verb line", "expected": "malformed/absent cell falls back AND is NAMED ('MISS floor_wake -> fallback 0'); a present cell wins", "observed": "wake=0, out=7, _misses=['floor_wake']; miss named on the result line; both-cells-absent misses both", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "sensei._commit_audit_record on a tmp repo with MERGE_HEAD present; and with the commit subprocess forced to raise", "expected": "status REFUSED and status FAILED, each named on the returned line; verb returns 4", "observed": "REFUSED 'merge in progress'; FAILED 'probe crash'", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "exact-path commit with a SECOND dirty file beside the audited record", "expected": "only the audited record lands; the second file stays dirty", "observed": "lands belam.20260913T013315Z.json alone; seed.txt untouched and still dirty", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "sensei._commit_audit_record on an UNTRACKED record in a tmp repo", "expected": "COMMITTED, record left CLEAN, one path one commit", "observed": "COMMITTED (sha 875cce2); porcelain '' ; seed.txt not swept", "result": "pass"}
  - {"conjunct": 5, "class": "wire", "cmd": "real hooks/agent-git/pre-commit in a linked worktree, staged node whose basename carries the agent id, AGI_PROJECT_ROOT=<wt>/.agi (raw) vs <wt> (fixed)", "expected": "raw refuses 'tier kid may not commit'; fixed admits the round's own node", "observed": "raw rc=1 refusal; fixed rc=0 admit", "result": "pass"}
  - {"conjunct": 6, "class": "gate", "cmd": "belam 20260916T151713Z numbers: audit_payload/audit_finding_line for wake (a=b=c=d=1, calls=4, floor=0) and out (floor=1)", "expected": "wake excess = a+b+c-floor = 3 (NOT calls-floor = 4); out keeps calls-floor = 3", "observed": "wake excess=3, line 'excess 3 over floor 0'; out excess=3", "result": "pass"}
  - {"conjunct": "2+4", "class": "gate", "cmd": "FALSIFIER: linked-worktree kid (AGI_TIER=kid, AGI_PROJECT_ROOT=<wt>/.agi) audits an UNTRACKED record in the SHARED MAIN graph", "expected": "the refused commit is carried by a non-zero exit and the record is never left dirty/staged", "observed": "git add staged the record in MAIN's index; the hook refused the commit (rc=1 'tier kid may not commit'); the code then ran `git diff --quiet` (worktree-vs-INDEX, both equal) -> returned SKIPPED 'record already clean after the rewrite', so the verb exits 0 and MAIN holds a STAGED record 'A  .agi/sessions/rotations/belam...json'", "result": "FAIL"}
production_lines: 99
profile: balanced
rebrief_answer: proceed-with-ceiling-120
rebrief_request: six-item-brief-overran-99-production-lines-vs-ceiling-40-NEED-~120.-Item-5-root-cause-is-outside-this-lane-hooks/agent-git-mis-resolves-under-the-GIT_DIR-git-exports-to-hooks;clipy-fixed-for-done;the-audit-verb-correctly-exits-4-on-a-shared-main-record
role: kid
scaffold_hash: 9217bf4c4a8efd78
season: 2
title: A00 f067c356 b0ad80
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-f067c356-b0ad80

## Experiment

SL7.135, target `hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit`. A **build round** (g15 order): measure the pre-fix state, implement the six named items, prove on built bytes. Two production files changed -- `extensions/agi/bin/sensei.py` and `extensions/agi/bin/cli.py` -- plus tests in `extensions/agi/tests/test_sensei_audit_record_writeback.py` and `extensions/agi/tests/test_cli.py`.

### What was built, one item each

1. **Silent floor fallback named.** `_audit_floors` now returns `{"wake", "out", "_misses": [cell,...]}`; a missing/malformed `floor_wake`/`floor_out` cell is listed in `_misses` and travels to `audit_finding_line`, which appends `[MISS <cell> -> fallback N]` beside the floor it already names. A present cell still always wins. New test `test_wake_names_a_missing_floor_cell` (verb-level) and the extended `test_floors_are_the_owners_numbers_and_have_one_reader`.
2. **Exit code carries the commit.** `_commit_audit_record` returns `(status, printed_line)` with status in COMMITTED/SKIPPED/REFUSED/FAILED; `finish_audit` returns `(line, status)`; both verbs `return 4 if status in ("REFUSED", "FAILED")`. The printed line is byte-identical to before. `test_merge_in_progress_refuses_the_commit_by_name` now asserts `== 4`.
3. **Two untested branches.** `test_commit_failed_branch_prints_failed_and_exits_nonzero` forces the commit subprocess to raise -> `FAILED` line + exit 4. `test_exact_path_commit_leaves_a_second_dirty_file_alone` plants a second dirty file and asserts only the audited record lands.
4. **Untracked live rotation records.** `_commit_audit_record` now `git add`s an untracked record then commits that one pathspec (`test_untracked_record_is_added_and_committed_alone`): one record, one commit, never left dirty. The old "not tracked by git" refusal is gone for the add-succeeds case; an add that FAILS still refuses by name.
5. **cli.py `done` ERR 'tier kid may not commit' -- verified, then fixed at the root.** Reproduced first (see Evidence): a linked-worktree kid with the dispatch env (`AGI_TIER=kid`, `AGI_TREE_PROJECT_ROOT=<wt>`) DOES get the ERR. Root cause measured with `bash -x` on the real hook: `/tmp/probeB-*/wt/.agi`... git exports `GIT_DIR` to hooks, so the hook's `git -C "$AGI_PROJECT_ROOT" rev-parse --show-toplevel` resolves the GRAPH dir (`.agi`) instead of the worktree, `REAL_TOPLEVEL != REAL_PROJECT`, and the shared-checkout arm refuses. `_auto_commit_worktree` now runs its one commit with `AGI_PROJECT_ROOT=<checkout_root>`, so the hook sees the worktree it is actually committing in and admits the round's own scoped paths. `test_done_worktree_kid_commit_is_allowed_by_the_real_agent_git_hook` (real hooksPath, real dispatch env) asserts the commit lands and no guard line prints.
6. **Wake excess excludes the cut call (d).** `audit_payload` and `audit_finding_line` compute the wake excess as `a+b+c - floor` while the out side keeps `calls - floor`. `test_wake_excess_excludes_the_cut_call_d` (verb-level: calls=3, d=1 -> excess 2, not 3) and the updated `test_wake_writes_audit_key...` (excess 3 -> 2).

### Proof

- `python3 -m pytest extensions/agi/tests/test_sensei_audit_record_writeback.py extensions/agi/tests/test_cli.py -q` -> **71 passed**.
- `python3 -m pytest extensions/agi/tests/test_brief.py -q` -> **137 passed** (covers `_auto_commit_worktree`).
- Live run: `sensei.py rotate-out-audit --seat sensei-director --record 20260916T122128Z` against a tracked `result: success` record -> the verb wrote the audit, `audit_record_commit: REFUSED -- agi: tier kid may not commit ... left uncommitted`, and **EXIT 4**. The exit code carried the refused commit (item 2 proven live). The refused write landed in the SHARED main graph (`rotate._shared_graph_root`); it was restored from `git show HEAD:<record>` so main is not left dirty by this kid.

### Item 5 fallout (honest)

`_commit_audit_record` has the same hook mis-resolution, but there the refusal is CORRECT: a kid auditing the shared main rotation record must not commit into main (goal:g4.1). The audit verb therefore exits 4 when run from a kid against a shared record, and the record is left dirty by design (a refused commit cannot clean it). Whether the audit verb should instead stage its record inside the kid's own worktree graph is a design question left to a future round -- see `rebrief_request`.

## Evidence

```
$ git diff --numstat -- extensions/agi/bin/sensei.py extensions/agi/bin/cli.py
10	1	extensions/agi/bin/cli.py
89	48	extensions/agi/bin/sensei.py

$ python3 -m pytest extensions/agi/tests/test_sensei_audit_record_writeback.py \
    extensions/agi/tests/test_cli.py -q
71 passed

$ python3 -m pytest extensions/agi/tests/test_brief.py -q
137 passed

# item (5) repro, real agent-git hook, dispatch env (before the cli.py fix):
ERR: worktree commit failed in /tmp/.../wt:
  agi: tier kid may not commit -- automation owns git (goal:s27)
# hook trace, hook cwd = wt but PROJECT resolved wrong under exported GIT_DIR:
+ + git -C /tmp/probeB-3411415/wt/.agi rev-parse --show-toplevel
+ PROJECT_TOPLEVEL=/tmp/probeB-3411415/wt/.agi
+ '[' /tmp/probeB-3411415/wt '!=' /tmp/probeB-3411415/wt/.agi ']'
+ echo 'agi: tier kid may not commit ...'

# live run (tracked success record, item 2):
$ python3 extensions/agi/bin/sensei.py rotate-out-audit --seat sensei-director \
    --record 20260916T122128Z
... counts: a=3 b=1 c=0 d=6 (floor 1)
audit_record_commit: REFUSED -- agi: tier kid may not commit -- automation owns git (goal:s27); .agi/sessions/rotations/sensei-director.20260916T122128Z.json left uncommitted
FINDING sensei-director out --record 20260916T122128Z excess 9 over floor 1
EXIT=4
```

## Agent Notes
Built all six SL7.135 items on sensei.py+cli.py, tests green (71+137 passed). (1) floor fallback named [MISS cell -> fallback N]; (2) commit REFUSED/FAILED -> exit 4 (proven live: rotate-out-audit exit 4 on a shared record); (3) FAILED branch + second-dirty-file tests; (4) untracked record git-added then committed alone; (5) reproduced the 'tier kid may not commit' ERR and fixed root: _auto_commit_worktree now points AGI_PROJECT_ROOT at the checkout root so the hook stops mis-resolving the worktree under exported GIT_DIR -- done commit lands; (6) wake excess = a+b+c-floor, out unchanged. production_lines 99 vs ceiling 40 -> rebrief_request filed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-19566029, SL7.135. Instruction said: "(2) A commit REFUSED/FAILED by _commit_audit_record still exits 0 ... the exit code must carry it" and "(4) untracked ... never a dirty record". Machine actually does, measured on the kid bytes at 5b51496a4: items 1,3,5,6 hold under my 13 probes; item 2 holds for a TRACKED record (merge-in-progress -> REFUSED -> exit 4); item 4 holds when the untracked add-then-commit SUCCEEDS (COMMITTED, porcelain empty). But item 4s new `git add` path regresses item 2 when the commit is REFUSED: my P7 linked-worktree-kid probe ran `_commit_audit_record` on an untracked SHARED-MAIN record; `git add` staged it, the hook refused the commit (rc=1), and the failure branch then ran `git diff --quiet -- rel` -- worktree-vs-INDEX, which is EMPTY right after add -- so it returned status SKIPPED ("record already clean after the rewrite"). The verb therefore exits 0 AND MAIN holds a staged record (A  .agi/sessions/rotations/belam...json). NEAR MISS: reading `git diff --quiet` as proof the commit happened; the correct test is `git diff --cached --quiet` (index-vs-HEAD) or a HEAD sha compare, and any non-zero commit must return REFUSED regardless. DEVIATION: none -- I demote proved to inconclusive_lean_disproved:70 with the falsifier named, rather than let the untracked+refused edge ride. rebrief_request answered: proceed with line_ceiling 120.
<!-- THOUGHT:END -->

Parent verdict: inconclusive_lean_disproved:70. Six items built and five hold under parent probes; conjunct 2+4 fails for UNTRACKED + REFUSED commit: git diff --quiet tests worktree-vs-index, so a freshly added record misreports SKIPPED, the verb exits 0, and MAIN is left with a staged record. Fix: use git diff --cached --quiet (or HEAD compare) and treat any non-zero commit as REFUSED; unstage on failure. Fix kid follows (SL7.135 kid 2).
