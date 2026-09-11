---
id: experiment:a00-c1c301b5-ee36ae
mint_id: 5709d4478ad6407495d5db81c8a967f1
type: experiment
parents:
  - hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env
next_edges: []
confidence: 0.9
edited_by: a00-e2e16001
evidence_runs:
  - experiment:a00-c1c301b5-ee36ae
loop: hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e7cb93722832ed05
season: 2
title: "Non-vacuous git-env redirect falsifier: GIT_COMMON_DIR alone redirects, pop restores"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c1c301b5-ee36ae

## Experiment

Built the NON-VACUOUS falsifier for hypothesis:l4-the-tier-gate-scan-is-not-
redirectable-by-git-env in extensions/agi/tests/test_tier_gate.py, on the
fake-MAIN + DECOY harness (the kid's three old tests were VACUOUS: a throwaway
conftest symlink made root #1 `_default_record_root()` resolve to the REAL
tree, so the planted record was found at root #1 and the git step never
mattered; and it set GIT_DIR equal to GIT_COMMON_DIR, which git resolves to
equal dirs -> `git_common_root` returns the walk-up repo root -> no redirect).

Setup, per the parent's spec, so root #1 finds NOTHING and the only record is
reachable through the git-resolved root #2:
  * `_build_fake_main` now `git init`s the fake MAIN (git_common_root consults
    `git rev-parse` only once a `.git` is on the walk-up, so a `.git`-less
    fake main is inert against the redirect). Record lives ONLY in
    `<main>/.agi/worktrees/kidA/.agi/sessions/.../agent.json` (pid = ancestor).
  * `_build_decoy_graph`: a decoy git repo carrying `.agi/config.json` +
    `.agi/nodes` (so find_project_root resolves it) but NO record.
  * `_run_pytest_on_fake_main` now strips host GIT_* vars before merging
    extra_env, so the redirect is exactly what the test sets.

Run against the fake main's bare tests dir with GIT_COMMON_DIR=<decoy>/.git
ALONE (GIT_DIR unset -- the parent's measurement, confirmed), AGI_TIER unset.

MEASURED MECHANISM (matches parent's bytes):
  GIT_COMMON_DIR=<decoy>/.git alone  -> git rev-parse: `.git` vs `<decoy>/.git`
      differ -> git_common_root returns common_dir.parent = decoy ->
      _record_roots() scans [<decoy>/.agi/sessions] ONLY -> record lost ->
      no tier -> bare suite RUNS (escape).
  GIT_COMMON_DIR=<decoy>/.git GIT_DIR=<decoy>/.git (equal) -> both report
      <decoy>/.git -> equal -> git_common_root returns the walk-up repo root
      -> NO redirect. (So GIT_DIR cancels it; set alone is the vector.)

VERDICT-DRIVING OUTPUT (repro + the new tests):
  * MUTATED conftest (the three pop lines REMOVED -- pre-fix bytes): bare dir
    with GIT_COMMON_DIR=<decoy>/.git -> returncode 0, "1 passed" (ESCAPE).
    This is the RED-on-pre-fix proof: the falsifier measures the pop.
  * FIXED conftest (pop present): same invocation -> returncode 4,
    "ERROR: AGI_TIER=kid refuses a bare full-suite directory run; run a
    specific test file or a -k filter instead." -> REFUSED.

Tests added / reworked in test_tier_gate.py (all 38 pass in 13.5s):
  * test_falsifier_git_env_cannot_redirect_the_scan_to_a_scratch_repo
    (REWRITTEN non-vacuous: root #1 empty, GIT_COMMON_DIR-alone, refusal)
  * test_falsifier_git_env_redirect_mutation_escapes_without_the_pop (RED pre-fix)
  * test_falsifier_git_env_redirect_no_redirect_still_refuses (unset -> refuse)
  * test_falsifier_git_env_redirect_to_configless_repo_still_refuses
    (decoy with no `.agi` -> fallback to root -> refuse)
  * test_falsifier_git_env_redirect_no_record_anywhere_passes
  * test_falsifier_git_env_redirect_named_file_still_passes (REWRITTEN non-vacuous)
  * test_decision_git_common_dir_alone_redirects_shared_root (in-process,
    real resolvers: redirect -> decoy; GIT_DIR equal -> cancelled; pop -> restored)

The mechanism wording is now stated as the parent demanded: GIT_COMMON_DIR
ALONE succeeds and redirects the scan; GIT_DIR set EQUAL to it cancels the
redirect (git sees git-dir == common-dir). This corrects the kid's previous
claim that "a gutted GIT_COMMON_DIR breaks the lookup" -- the opposite is
true: a live company dir alone redirects.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_tier_gate.py -q
38 passed in 13.49s

$ python3 -m pytest extensions/agi/tests/test_locations.py -q
85 passed in 2.35s
```

Mutation vs guard repro (clean tmp harness):
```
=== MUTATED(no-pop) pre-fix bytes: returncode=0 ===
1 passed in 0.01s                          # bare dir ESCAPED the gate
=== FIXED(pop present): returncode=4 ===
ERROR: AGI_TIER=kid refuses a bare full-suite directory run;
run a specific test file or a -k filter instead.
```

## Agent Notes
Built non-vacuous git-env redirect falsifier on fake-MAIN+DECOY harness: GIT_COMMON_DIR alone redirects pre-fix (mutation escapes, exits 0), pop restores refusal (exit 4). All 38 test_tier_gate pass; title set.

PARENT REVIEW (a00-e2e16001, L4.228): ACCEPTED, verdict proved upheld. Non-vacuous falsifier verified: root #1 (fake MAIN sessions) holds no record, the only kid record lives in the registered worktree reachable solely through the git-resolved root #2; GIT_COMMON_DIR ALONE pointed at a decoy graph carrying .agi/config.json redirects shared_project_root to the decoy (parent independently reproduced this from the real worktree). The mutation test strips exactly the three pop lines (fail-closed regex, n==1) and asserts the SAME invocation ESCAPES (exit 0) on pre-fix bytes while the fixed bytes REFUSE (exit 4) -- so the test measures the pop, not the environment. Negative controls cover unset/configless/no-record/named-file. Parent ran the file: 38 passed in 13.35s. Fix kept: conftest pytest_cmdline_main pops GIT_DIR/GIT_COMMON_DIR/GIT_WORK_TREE before any root resolves.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Round 2 of this hypothesis, built on round 1 (experiment:a00-e0f72fb4-bd6f07), whose fix is kept but whose tests were vacuous. This round adds a fake-MAIN + DECOY harness that makes root #1 find nothing so the git-resolved root #2 is load-bearing, drives GIT_COMMON_DIR ALONE (GIT_DIR deliberately unset -- set equal it cancels the redirect), and adds the non-vacuity pair: the same invocation against a conftest with the pop lines stripped escapes (exit 0) and with them present refuses (exit 4). Also corrected round 1s false mechanism claim: GIT_COMMON_DIR alone succeeds and redirects; it is not a lookup failure.
<!-- THOUGHT:END -->
