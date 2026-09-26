---
id: experiment:a00-9608da10-ec05af
mint_id: 5d33d95ac551412c9b98fa167ca2ce0e
type: experiment
parents:
  - hypothesis:l4-suite-green-on-main-the-18-reds-after-h2-and-rc-propagation-are-fixtures-that-learn-the-resolver-plus-one-no-repo-predicate-fix
next_edges: []
confidence: 0.9
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: director-engine
evidence_runs:
  - experiment:a00-9608da10-ec05af
line_ceiling: 15
loop: hypothesis:l4-suite-green-on-main-the-18-reds-after-h2-and-rc-propagation-are-fixtures-that-learn-the-resolver-plus-one-no-repo-predicate-fix@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f66ca17a70950b27
season: 2
title: "L4 suite green: dedicated no-git-path predicate test added; parent CLASS D reason corrected"
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-9608da10-ec05af

## Experiment

Closed the two deliverable gaps that demoted the parent round
(experiment:a00-25355804-78e3b9) to inconclusive_lean_proved:80. Parent had
already turned the 18 reds green and verified the core with its own full-suite
run (`verification.py --level rotation --suite`: RESULT PASS, 5326 passed / 16
skipped, table==footer). This round did TEST-ONLY and NODE-REWORD work — no
production change (0 production lines, `git diff --numstat` on locations.py +
verification.py).

## Gap 1 — the claim's dedicated no-git-path predicate test (tests only)

The parent's diff carried only the summary-parser test; the predicate
`is_live_checkout(no-repo) is False` was exercised only indirectly by the
heal_watch test + a parent probe, not by its own named test. Added a dedicated
test to `extensions/agi/tests/test_suite_live_checkout.py`:

```python
def test_no_git_path_is_never_the_live_checkout(tmp_path):
    """The claim's dedicated no-repo predicate test: a path with NO enclosing
    git repo must read FALSE (never LIVE), while the real engine checkout
    reads True. Covers the regression that could label a gitless /tmp basetemp
    LIVE and trip the H2 refusal."""
    import tempfile
    gitless = Path(tempfile.mkdtemp())  # fresh dir under /tmp, no repo
    assert locations.is_live_checkout(gitless) is False
    assert locations.is_live_checkout(LIVE) is True
```

First draft also asserted `git_common_root(gitless) is None` — WRONG: that
helper returns the path itself unchanged for a gitless dir (its no-repo
fallback), never None, so the assertion failed. Dropped it; the claim needs
only the predicate's True/False behaviour. Test green.

## Gap 2 — corrected the parent's CLASS D node reason

The parent node claimed "the two prior landings put one hit in workflow.py".
Git-blame (parent's own finding) shows the season2/main comment PREDATES the
landings (present at 982257cdd, added in the season2/main merge c67b973f8), so
blaming the landings was false. Re-worded that section in place via write.py
`replace body 57:69`: the hit is pre-existing (not introduced this round), the
re-pin into the pinned inventory STAYS exactly as a legitimate re-triage, and
the attribution no longer blames the landings. Pinned inventory unchanged.

## Result

Both deliverable gaps closed. All 18 reds remain green (parent's full-suite
run), the newly-added dedicated no-repo predicate test is green, and the
parent's CLASS D reason now tells the truth.

## Evidence

Run command (each file set):
```
python3 -m pytest extensions/agi/tests/test_suite_live_checkout.py \
  extensions/agi/tests/test_suite_live_checkout_worktree.py \
  extensions/agi/tests/test_heal_watch.py -q \
  --basetemp $(mktemp -d /tmp/agi-sm80-bt.XXXXXX) -p no:cacheprovider
```
Result: 75 passed, 12 warnings in 4.76s (includes the new
`test_no_git_path_is_never_the_live_checkout`).

Single-test confirm:
```
python3 -m pytest extensions/agi/tests/test_suite_live_checkout.py -q \
  --basetemp $(mktemp -d /tmp/agi-sm80-bt3.XXXXXX) -p no:cacheprovider \
  -k no_git_path
```
Result: 1 passed, 9 deselected in 0.08s.

Production line count (allowed `git diff --numstat` on locations.py +
verification.py): 0 net lines. Test-only round, well under the 15-line
ceiling.

## Agent Notes
Added the dedicated no-git-path predicate test the claim's TESTS required
(assert is_live_checkout(gitless)==False and is_live_checkout(LIVE)==True) to
test_suite_live_checkout.py; 75 passed across live_checkout×2 + heal_watch, and
the new test alone passes. Corrected the parent experiment node's CLASS D
reason (write.py body replace): workflow.py comment PREDATES the landings, so
the re-pin stays as a legitimate re-triage but no longer blames the landings.
0 production lines changed — this round was test + node-reword only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 7 residue (hypothesis:pass7-0926-residue-batch, test_brief.py:829): evidence_runs was the scalar form the brief example moved away from; rewritten as the one-item list of the SAME id. No evidence added or removed, verdict unchanged.
<!-- THOUGHT:END -->

## Agent Notes
Closed the two deliverable gaps that demoted the parent claim to inconclusive_lean_proved:80. (1) Added the claim's dedicated no-git-path predicate test to test_suite_live_checkout.py (is_live_checkout(gitless)==False, is_live_checkout(LIVE)==True); 75 passed across live_checkout x2 + heal_watch, new test green. (2) Corrected parent's CLASS D reason via write.py: workflow.py comment PREDATES the landings (982257cdd / merge c67b973f8), re-pin stays as legitimate re-triage but no longer blames the landings. 0 production lines (test + node-reword only).

PARENT REVIEW (a00-107fc3a7): ACCEPT. This continuation closes the two gaps that demoted kid1 (experiment:a00-25355804-78e3b9) to inconclusive_lean_proved:80. Gap 1 (the claim's required no-git-path predicate test): ADDED test_no_git_path_is_never_the_live_checkout asserting is_live_checkout(gitless)==False and is_live_checkout(LIVE)==True; I re-ran it green (3 passed with heal_watch + conftest_gate, --basetemp /tmp). Gap 2 (CLASS D node reason): the reword landed on kid1's node via write.py -- git-blame confirms the season2/main comment PREDATES the landings (present at 982257cdd, merge c67b973f8), so the node no longer falsely blames the landings; the pinned-inventory re-triage itself stays legitimate. 0 production lines this round -- test + node-reword only, as ordered. PROBES: (1) wire -- test_no_git_path is_live_checkout==False on a fresh gitless /tmp dir, LIVE==True (HOLDS). (2) auth -- in-repo basetemp still refused (base full-suite H2 guard green, exit 3 named line) (HOLDS). Verdict proved stands.
