---
id: experiment:a00-04369518-4515b9
mint_id: 44df264efaa34b998e200806dc1d51fa
type: experiment
parents:
  - hypothesis:l4-branch-reshuffle-apply-collect-refusals-and-continue-on-a-moving-tip
next_edges: []
confidence: 0.9
edited_by: a00-6885fe15
evidence_runs:
  - experiment:a00-04369518-4515b9
loop: hypothesis:l4-branch-reshuffle-apply-collect-refusals-and-continue-on-a-moving-tip@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe A: tmp fixture (bare origin, town set {core@2, streaming-suite@1, web-app-suite@1}); local core/main at a throwaway ORPHAN commit (divergent); every other planned trunk absent; `--apply --kinds main,posts,towns`.", "expected": "rc != 0; ERR names core/main; every OTHER planned trunk-pair created locally AND pushed; core/main never force-moved.", "observed": "rc=1; refused_named=True; created == expected == all 5 remaining targets; core/main left at the orphan sha; no --force/-f anywhere.", "result": "HOLDS."}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe C (the falsifier that demoted kid 1): _v3_apply_repo fixture (two v3 post source branches + worktrees); core/main at a wrong tip; `--apply --kinds main,posts,towns`.", "expected": "The delete-old pattern applied to the WHOLE job stream: the v3 post section still runs, both core/season2/posts/<post>/main exist, the closing line prints, rc != 0, core/main never force-moved.", "observed": "rc=1; post_section_ran=True; post_renames_done=['core/season2/posts/sanctuary-director/main','core/season2/posts/sanctuary-helper/main'] == expected; reached_apply_done_line=True; core/main still at the wrong sha.", "result": "HOLDS. Kid 1's demotion is closed by this kid's bytes."}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe B (the claim's named scenario): core/main created at the OLD season2/main tip, then season2/main ADVANCES by a real commit, then a resumed `--apply --kinds main,posts,towns`.", "expected": "The run survives the moved tip and creates the remaining tunnel trunk-pairs.", "observed": "tip moved 54351d68->7bcac0f3; rc=1; core/main left at the old tip; all 5 remaining targets created locally AND on origin at the planned tips; summary names core/main.", "result": "HOLDS."}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe G: two towns wrong at once (core/main and streaming-suite/main at a throwaway orphan commit); `--apply --kinds main,posts,towns`.", "expected": "ONE summary line naming both, rc != 0, the third town still created.", "observed": "rc=1; summary_lines=1; summary='ERR: v3 town creates: 2 trunk(s) refused: core/main, streaming-suite/main'.", "result": "HOLDS. No double summary."}
  - {"conjunct": 2, "class": "gate", "cmd": "PARENT probe D: zero-legacy repo (no master, jobs==[]) with a declared town set; `--apply --kinds towns`.", "expected": "The refs/grid IDENTICAL|CHANGED line prints on the zero-legacy apply path.", "observed": "rc=0; 'no legacy branches to reshuffle' present; 'refs/grid: IDENTICAL before/after --apply (expected IDENTICAL)' present.", "result": "HOLDS."}
  - {"conjunct": 2, "class": "wire", "cmd": "PARENT probe E: non-zero-legacy repo; `--apply --kinds main,posts,towns`; count refs/grid lines.", "expected": "Exactly one on the main apply path (no double print).", "observed": "rc=0; grid_line_count=1.", "result": "HOLDS."}
  - {"conjunct": 2, "class": "gate", "cmd": "PARENT probe F: repo with a wrong-tip core/main; `--dry-run --kinds main,posts,towns`.", "expected": "Dry-run gains no refusal text, no summary, no refs/grid line.", "observed": "rc=0; refused_in_dry=False; summary_in_dry=False; grid_line_in_dry=False.", "result": "HOLDS."}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe H (BOUNDARY, not a claim conjunct): origin REACHABLE and legacy jobs present, but the v3 create leg broken (local tip branch season2/streaming-suite/season1/main deleted so `git branch streaming-suite/main <tip>` fails rc != 0); `--apply --kinds main,posts,towns`.", "expected": "The closing 'apply: local renames + worktree re-points done' line may print only when it is TRUE -- it must NOT print when a v3 git command aborted before the post section.", "observed": "rc=1; v3_create_failed=True; post_section_ran=False; done_line_printed=True. The caller's `v3_rc = _rs_v3_run(...)` prints the line unconditionally, while the zero-legacy arm (unchanged `if _rs_v3_run(...): return 1`) does not -- the two arms disagree on the same state.", "result": "BOUNDARY, not a falsification of the claim (the claim's conjuncts all hold above). This kid's caller change was forced by the brief's own test spec ('apply: local renames ...' IS in stdout). Closing round: experiment:a00-502e9bea-e978df (kid a00-502e9bea) prints that line inside _rs_v3_run, gated on reaching the end of the job stream."}
profile: balanced
push_further: "A BEHIND (ancestor) tip is still classified wrong exactly like a divergent one, so after a merge-up the run stays at rc 1 forever once the post section has run; the claim mandates refusal+no-force-move so this is its edge, not its defect. A successor should distinguish behind (ancestor of the planned tip: fast-forward or skip-with-notice) from divergent (refuse by name)."
role: kid
scaffold_hash: 1cfae6d854bebcc8
season: 2
title: A00 04369518 4515b9
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-04369518-4515b9

## Experiment

Extend the R3.2 bytes the prior kid landed (a00-2613edf9): move the
wrong-tip refusal summary + non-zero exit from the END OF THE TOWN BLOCK to
the END OF `_rs_v3_run`, so a refused trunk no longer blocks the sections
that FOLLOW it (v3 post renames, v3 main notice, dry-only loop plan).

Scope: `extensions/agi/bin/cli.py` + `extensions/agi/tests/test_branch_reshuffle_v3.py`.
No live apply; every run is a tmp fixture with a disposable bare origin.

### What changed (byte-level)

* `refused: list[str] = []` is now declared ONCE early, after the
  `town_declared` INERT guard and before the `if "town_main" in kinds` block
  (cli.py:3520). It was previously declared inside the town block.
* the town block still appends the wrong town and `continue`s; the per-refusal
  `ERR: branch-create <town> REFUSED: ...` in the loop is unchanged (cli.py:3582).
* the `if refused: ... return 1` summary was REMOVED from the end of the town
  block and re-added at the very END of `_rs_v3_run`, just before `return 0`
  (cli.py:3671-3674). Same wording, same rc.
* every OTHER `return 1` in `_rs_v3_run` is untouched: real `git branch` /
  `git push -u` rc failures, R3.1's ls-remote `"failed"` refusal, and the v3
  loop-plan rc.
* caller (`cmd_branch_reshuffle`, the main apply tail): the old
  `if _rs_v3_run(...): return 1` swallowed the closing
  `apply: local renames + worktree re-points done;` line on a refusal. Now
  `v3_rc = _rs_v3_run(...)`; the closing line prints, then `return v3_rc`
  (cli.py:4180-4183) -- the refusal is still rc-honest (1) and a real git
  failure is still 1, but the report of the v2 renames/re-points that DID
  complete above is not suppressed.
* the zero-legacy `refs/grid:` line the prior kid added is untouched.

### Falsifier added

`test_v3_apply_wrong_tip_trunk_still_runs_the_post_section` -- `core/main` at
an orphan wrong tip, run `--apply --kinds main,posts,towns`, assert rc != 0,
the summary names `core/main`, `[APPLY] branch rename (local, v3)` and
`apply: local renames + worktree re-points done;` are in stdout, both
`core/season2/posts/<post>/main` branches exist, and `core/main` is still at
the wrong sha.

## Evidence

### 1. Pre-change FAILING run of the falsifier (measured)

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -q \
    -k wrong_tip_trunk_still_runs_the_post_section
E       AssertionError: ...
E       assert '[APPLY] branch rename (local, v3)' in
        '...v3 town creates (3 towns):\n  [APPLY] branch create (v3): git branch core/season2/main ...
         ...v3 main: season<n>/main stays ...'
E       stderr tail: 'ERR: v3 town creates: 1 trunk(s) refused: core/main'
1 failed, 37 deselected
```

Pre-fix the post section NEVER RAN: the town block's `return 1` aborted the
whole function, so on a moved `season2/main` tip the v3 post renames could
never happen on any retry (core/main stays at the old tip and is never
force-moved). The migration could never complete.

### 2. Passing run after the change

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py \
    extensions/agi/tests/test_branch_reshuffle.py -q
68 passed in 43.37s
```

(`test_v3_apply_refuses_a_trunk_at_wrong_tip` -- rc == 1 + REFUSED/core/main
in stderr -- still passes; the other wrong-tip collection tests still pass.)

### 3. --dry-run byte-identity on the SAME fixture (before vs after bytes)

Pre-change `cli.py` reconstructed in-place as `cli_before_tmp.py` (temp copy,
deleted after); both run against one identical `_v3_apply_repo` fixture:

```
kinds='main,posts,towns' identical=True rc_before=0 rc_after=0
kinds='towns'            identical=True rc_before=0 rc_after=0
kinds='posts'            identical=True rc_before=0 rc_after=0
kinds='main'             identical=True rc_before=0 rc_after=0
```

Byte-identical stdout+stderr+rc: the refusal collection lives inside the
`not dry and has_origin` path, so no `--dry-run` may gain a summary or an ERR.

### 4. Line numbers of the moved bytes

| byte | line |
|---|---|
| `refused: list[str] = []` (early, whole-stream collection) | cli.py:3520 |
| per-refusal `ERR: branch-create <town> REFUSED:` (unchanged) | cli.py:3582 |
| ONE summary + `return 1` (was end of town block) | cli.py:3671-3674 |
| caller `v3_rc = _rs_v3_run(...)` + closing line + `return v3_rc` | cli.py:4180-4183 |

### 5. No force-move anywhere

`test_v3_trunk_create_never_forces` still passes: the town block carries no
`--force` / `-f`, and the falsifier re-asserts `core/main` is still at the
wrong sha after the run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one: the kid's version carried its own build report; THIS version is the tier-parent's review of it, written after reading the changed BYTES (the staged diff of cli.py: cli.py:3510-3674 `_rs_v3_run` -- `refused` declared once early, the summary+`return 1` moved to the end of the function, and cli.py:4172-4183 the caller's `v3_rc = _rs_v3_run(...)` + closing line + `return v3_rc`; plus the one new falsifier in test_branch_reshuffle_v3.py) and after running eight independent probes of my own (/tmp/probe_r32.py, /tmp/probe_r32b.py, plus P7b/P8), not the kid's suite.

(1) WHAT THE INSTRUCTION SAID, and what the machine does. The instruction was to move the wrong-tip refusal summary + non-zero exit from the end of the town block to the END OF `_rs_v3_run`, so a refused trunk no longer blocks the v3 post section; to leave every OTHER return 1 alone; and to keep --dry-run byte-identical. The bytes do exactly that: `refused: list[str] = []` at cli.py:3520 (declared once, before the town block), the per-refusal ERR + `refused.append(...)` + `continue` at cli.py:3582, and the single summary + `return 1` at cli.py:3671-3674 after the loop section. PARENT probe C -- the probe that demoted kid 1 -- now HOLDS: with core/main wrong and both v3 post sources pending, rc=1 and post_renames_done == both core/season2/posts/<post>/main, post_section_ran=True.

(2) THE OTHER PROBES, all HOLD. A (divergent core/main; every other town still created+pushed; never force-moved), B (a REAL moved season2/main tip: the resumed apply creates all 5 remaining targets locally and on origin), G (two wrong towns -> exactly ONE summary line naming both), D (zero-legacy apply prints refs/grid IDENTICAL), E (main apply path prints it exactly once), F (--dry-run gains no refusal text, no summary, no refs/grid line).

(3) THE NEAR MISS, measured and then fixed by a third kid. The kid's new falsifier required `apply: local renames + worktree re-points done;` in stdout on the REFUSAL path, and the caller's old `if _rs_v3_run(...): return 1` swallowed it there -- so the kid changed the caller to `v3_rc = _rs_v3_run(...)`, print the line, `return v3_rc`. That shape prints the line UNCONDITIONALLY, so PARENT probe H (origin reachable, legacy jobs present, the local tip branch season2/streaming-suite/season1/main deleted so `git branch streaming-suite/main <tip>` fails) shows rc=1, post_section_ran=False and done_line_printed=True -- a line claiming work that did not happen -- while the zero-legacy arm, left as `if _rs_v3_run(...): return 1`, does not print it. Same state, two arms, two reports. H is a BOUNDARY OF THE IMPLEMENTATION, not a falsification of the claim (the claim's two conjuncts hold), so this node stays proved.

(4) DEVIATION, AND WHOSE. The kid's deviation from "every OTHER return 1 stays where it is" is a CALLER change, not an `_rs_v3_run` change, and the kid is right that the instruction was scoped to `_rs_v3_run`. The force behind it was the parent's own brief, whose test spec demanded that line in stdout on the refusal path. The correction is a fresh kid (experiment:a00-502e9bea-e978df): print the line inside `_rs_v3_run` where it is true, gated on `not dry`, and delete the print from both callers so the arms agree. The parent changed no code.

(5) VERDICT: proved, not demoted. The kid's own falsifier failed pre-change (measured, with the E-line assertion named) and passes after; my eight probes are the evidence and every claim conjunct holds. This node is the one that satisfies the belam `--apply` gate's R3.2 half, provided the third kid's correctness-of-report fix lands in the same round.
<!-- THOUGHT:END -->

## Agent Notes
Moved the wrong-tip refusal summary + rc from end of town block to end of _rs_v3_run (cli.py:3520 decl, 3671-3674 summary); a refused trunk no longer blocks the v3 post section. Falsifier test_v3_apply_wrong_tip_trunk_still_runs_the_post_section FAILED pre-fix, passes after; 68 passed over test_branch_reshuffle_v3.py + test_branch_reshuffle.py; dry-run byte-identical on same fixture for 4 kind sets.

PARENT REVIEW L4.348 (a00-6885fe15): verdict ACCEPTED -- kid's `proved` NOT demoted. Read the staged bytes (cli.py:3510-3674, 4172-4183; 1 new falsifier) and ran eight independent probes (`probes:` in frontmatter), never the kid's suite. HOLDS: A (divergent core/main -> all 5 other trunk-pairs created+pushed, no force), B (a REAL moved season2/main tip -> run survives), C (the probe that demoted kid 1: post_section_ran=True, both core/season2/posts/<post>/main created, rc=1), D (zero-legacy apply prints refs/grid IDENTICAL), E (main path prints it exactly once), F (--dry-run gains no refusal/summary/grid text), G (two wrong towns -> ONE summary naming both). BOUNDARY: H -- with origin reachable but the v3 create leg broken, rc=1, post_section_ran=False and the caller STILL printed 'apply: local renames + worktree re-points done', while the zero-legacy arm does not; the two arms disagree on the same state. Not a claim falsification (the claim's conjuncts hold); correction in flight: experiment:a00-502e9bea-e978df prints that line inside _rs_v3_run where it is true and deletes it from both callers. This node satisfies the belam `--apply` gate's R3.2 half; the gate should read it together with the third kid's node.
