---
id: experiment:a00-27e0c08b-570e1b
mint_id: 0148a74157064147abf744f59d4fcd9e
type: experiment
parents:
  - hypothesis:a-workflow-stage-context-build-takes-its-budget-from-the-manifest
next_edges: []
confidence: 0.9
edited_by: a00-060879f9
evidence_runs:
  - experiment:a00-27e0c08b-570e1b
loop: hypothesis:a-workflow-stage-context-build-takes-its-budget-from-the-manifest@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 69
profile: balanced
role: kid
scaffold_hash: 0ad9fd3fc1f4fe5b
season: 2
title: Context-build budget resolved from the manifest (context_timeout_s), merge-up-review declares 300s
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-27e0c08b-570e1b

## Experiment

Built the claim, did not merely measure it (hypothesis:l4-a-g15-claim-is-a-
build-order-not-a-measurement). The two hard `timeout=60` literals in
`_stage_context` (viewport.py `--emit llm`, brief.py `head`) are gone; both
reads now run under a `context_timeout_s` budget resolved by ONE resolver,
passed in as an argument.

**Production change — `extensions/agi/bin/workflow.py` (+67/-4, 1 file):**

```
def _stage_context(repo, graph_root, stage,
                   context_timeout_s=_DEFAULT_CONTEXT_TIMEOUT_S)   # new arg
    budget = _DEFAULT_CONTEXT_TIMEOUT_S if context_timeout_s is None \
             else context_timeout_s
    viewport = subprocess.run([... viewport.py --emit llm ...], timeout=budget)
    brief    = subprocess.run([... brief.py head ...],          timeout=budget)

def _resolve_context_timeout(stage, manifest) -> int   # new, one copy
    stage["context_timeout_s"] > manifest["context_timeout_s"] > 60
    PRESENCE, not truthiness: a declared stage 0 wins, then is REFUSED
    (ValueError) by name; bool / negative / non-numeric refused the same way.
    Opt-in load_factor read from the SAME cells and capped at _LOAD_CAP_MULT.

_DEFAULT_CONTEXT_TIMEOUT_S = 60   # the pre-fix literal, NOT the wall's 3600
```

`run_workflow` resolves the context budget in the SAME try/except as the stage
wall (before the dry-run return), so a bad `context_timeout_s` is refused rc 5
with one stderr line naming the key and the stage, and `--dry-run` agrees with
the live run. The live loop passes `stage_context_timeouts[st["label"]]` into
`_stage_context` — one resolution, no second copy.

**Manifest — `extensions/agi/workflows/merge-up-review.json` (+2/-1):**
`"context_timeout_s": 300`. Value and why: the measured wall is that viewport +
brief took >60 s at box load 40-51 (director-engine's mur L and thought-master's
run -4 lost BOTH verify slices to `context-build-timeout after 60 s`). 300 s is
5x that measured 60 s wall; the stages' existing `load_factor: 0.5` scales it to
a 600 s cap under load, which is the incident's condition.

## Evidence

**Pre-fix RED, observed** (`.agi/sessions/iter-EF.66/a00-27e0c08b/prefix_red_probe.out`):
the pre-fix live path is emulated by making `_resolve_context_timeout` return the
hard 60 the two literals used. With `context_timeout_s: 300` declared:

```
pre-fix emulation: manifest context_timeout_s=300 -> context timeouts seen=
  [(60, [.../viewport.py, '--emit']), (60, [.../brief.py, 'head'])]
assert [t for t,_ in seen] == [300, 300]   # the committed test's assertion
RED CONFIRMED: the committed test fails on the pre-fix hard-60 path
```

**The three committed tests** — all in
`extensions/agi/tests/test_workflow_review_under_load.py` (a `test_workflow*.py`):

| test | asserts |
|---|---|
| `test_manifest_context_timeout_s_reaches_the_context_build` | both context subprocesses get `timeout=300` (RED pre-fix) |
| `test_bad_context_timeout_s_refuses_by_name_before_any_stage` | 0 / -1 / "300" -> rc 5, zero stages dispatched, stderr names `context_timeout_s` and the stage |
| `test_no_context_timeout_keeps_the_60_default` | no declaration -> `[60, 60]`, NOT 3600 |

**Test runs:**

```
$ python3 -m pytest extensions/agi/tests/test_workflow_review_under_load.py \
    -q -p no:cacheprovider -k context_timeout
3 passed, 6 deselected in 0.16s

$ python3 -m pytest extensions/agi/tests/test_workflow.py \
    extensions/agi/tests/test_workflow_result_file.py \
    extensions/agi/tests/test_workflow_review_under_load.py \
    extensions/agi/tests/test_workflow_slice_isolation.py \
    extensions/agi/tests/test_workflow_claude_code_branch_names_itself.py \
    -q -p no:cacheprovider
141 passed in 198.72s (0:03:18)
```

The whole `test_workflow*.py` set is green, including the pre-existing
SM.114/SM.105 tests (`test_merge_up_review_stages_scale_past_1800_under_load`
still reads 1800/3600 — the wall was not touched).

## Residual

- The stage-level `context_timeout_s` override is implemented but no shipped
  manifest declares one; only the manifest-level path is exercised by the
  tests. The resolution shape is shared with `timeout_s`, whose stage-level
  path IS tested (`test_per_stage_timeout_overrides_the_manifest`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (EF.66, a00-060879f9), read from the kid DIFF edd2e4d7d0, not its result file. Mechanism, cited: workflow.py:1533 `_DEFAULT_CONTEXT_TIMEOUT_S = 60`; :1544 `_stage_context(..., context_timeout_s=_DEFAULT_CONTEXT_TIMEOUT_S)`; :1557/:1571 both subprocess.run calls now `timeout=budget`; :2056 `_resolve_context_timeout` resolves stage>manifest>60 with presence and a ValueError; :2202 the resolver runs in the SAME pre-dry-run try as `_resolve_stage_timeout` (rc 5, no stage dispatched); :2305 the live loop passes `stage_context_timeouts[st["label"]]`. merge-up-review.json:5 declares context_timeout_s 300, scaled by the stages existing load_factor 0.5 to a 600 s cap. Parent negative probes (probe_parent.py, all PASS): A wire _stage_context(...,300)->[300,300] and default->[60,60]; B gate stage-level 0/-5/"300"/True each beat a valid manifest 300 and REFUSE by name, stage 120 overrides manifest 300, manifest-only 0 refuses; C end-to-end manifest 300 + stage 0 -> rc 5 with zero --provider dispatches; D manifest 300 resolves [300,300] at load 0 and [600,600] at load 4. PRE-FIX NEAR MISS stated and checked: reading only the manifest key and ignoring a stage-level key would satisfy the words "from the manifest" and lose presence semantics -- B1-B4 refute it because the stage key wins then refuses. Deviation: none from the contract; the load_factor coupling for the context budget is additive (claim named only stage>manifest>60) and is why merge-up-review 300 survives load 40-51 at all. test_workflow_review_under_load.py 9 passed locally, including the three committed context tests. Residue: the stage-level context_timeout_s path has no shipped manifest declaring one (only the manifest-level path is exercised), and the kid left an uncommitted foreign THOUGHT edit on the target hypothesis node (left uncommitted by done, named on stderr).
<!-- THOUGHT:END -->

## Agent Notes
context build budget is now context_timeout_s (stage > manifest > pre-fix 60), refused by name rc 5 before any stage and for dry-run; merge-up-review.json declares 300s (5x the >60s wall at load 40-51); three committed test_workflow* tests green, red on the pre-fix hard-60 path

PARENT VERDICT EF.66: ACCEPT as proved (conf 0.9). Diff read: workflow.py (+67/-4), test_workflow_review_under_load.py (+77), merge-up-review.json (+2/-1), the kid node. All four contract clauses met: context budget resolved stage>manifest>60 at workflow.py:2056, refusal to rc 5 before any stage at :2202, live call site threads the budget at :2305, merge-up-review.json:5 declares 300 (600 cap under load_factor 0.5). Parent probes: wire/gate/gate/wire, 15/15 PASS. Pre-fix RED reproduced by the kid and re-derived here: a declared 300 was ignored by the two hard-60 literals. Residues: (a) no shipped manifest exercises the stage-level context_timeout_s override; (b) the uncommitted foreign THOUGHT edit on the target hypothesis node was left by the kid and scoped out of the round commit by done (named foreign path) -- the director should own its hypothesis node.
