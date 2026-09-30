---
id: hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff
mint_id: 5299b61cabf34feaa7cdbae954bfdd3c
type: hypothesis
parents:
  - goal:g1.31.5.1.1
next_edges: []
edited_by: director-general-4
scaffold_hash: 29618dcf04bd286f
season: 2
testable_claim: With set -o pipefail on the kid scope pipe, a failed git diff --cached (rc 128, corrupted index, hook run directly) exits non-zero with one named stderr line, where HEAD exits 0; a healthy empty staged set (scope-check all([]) == 0) and every in-scope/out-of-scope control keep their rc; the hook still delegates to cli._round_scope_ok.
title: The agent-git pre-commit hook refuses a kid commit when `git diff --cached` itself fails (pipefail + one named line); an empty healthy set stays allowed
town: core
---
# hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff

## Measured
- goal:g1.31.5.1.1 (PASS B3 missed row n19, red, pre-existing, from round l4-sm36 one-scope-rule; verify file `.agi/sessions/workflows/runs/mur-pb3chunk12of20/verify_l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-ho.json`, left UNVERIFIED by the reviewer). Re-measured at HEAD 0de3a32a0 in a tmp repo, kid tier, own toplevel, synthetic agent id:
```
healthy repo, empty staged set (--allow-empty)   hook rc 0        <- today's behaviour, kept
.git/index corrupted: git diff --cached           rc 128
                       hook (bash <hook>)          rc 0  <- FAIL-OPEN
control, staged .agi/config.json                   hook rc 1  (refuses, as designed)
```
- `extensions/agi/hooks/agent-git/pre-commit`, kid branch (the `if [ "${AGI_TIER}" = "kid" ] ...` block): `if git diff --cached --name-only -z --no-renames | python3 "$HOOK_BIN/cli.py" scope-check ...; then exit 0; fi`. The `if` tests only the LAST command of the pipe; the file carries 0 `set` flags and 0 `pipefail`.
- `extensions/agi/bin/cli.py` `cmd_scope_check`: `paths = [p for p in sys.stdin.read().split("\0") if p]`, then `return 0 if all(_round_scope_ok(p, ...) for p in paths) else 1`; `all([])` is True, so an EMPTY list returns 0 (allow). Empty from a healthy diff = nothing staged = allowed today (git itself aborts a plain `git commit` with nothing staged before it reaches the hook; only `--allow-empty` reaches it). Empty from a FAILED diff is the hole.
- Reachability: `git commit` reads the index before it runs the hook, so a corrupt index dies in git first; the hole is a `git diff --cached` that fails INSIDE the hook after the commit's own read succeeded (a transient read error, a killed or OOM'd git under the shared-box pressure). The committed test therefore runs the hook script DIRECTLY (the leaf's own probe does), never through `git commit`.

## CLAIM
(1) The scope pipe in the kid branch of `pre-commit` runs under `set -o pipefail`, so a failed `git diff --cached` makes the pipeline non-zero and the kid falls through to the end-of-file refusal (`exit 1`) instead of `exit 0`.
(2) A failed diff (pipeline rc >= 2: git's 128, cli.py's crash) prints ONE named stderr line (`agi: kid commit refused -- git diff --cached failed (rc <n>) (goal:g1.31.5.1.1)`) before it refuses; a scope refusal (rc 1) keeps today's generic line, no double line.
(3) A genuinely empty staged set from a SUCCESSFUL diff keeps today's behaviour: `scope-check` returns 0 (`all([])`), the hook exits 0. ONE scope rule stays: the hook still delegates to `cli._round_scope_ok` through `scope-check`; no second predicate in shell.
```
git diff --cached -z ─┐  pipefail
                      ├─► rc = rightmost non-zero
python3 cli.py scope-check ─┘
  0            ─► exit 0   (in scope, or empty-but-OK)
  1            ─► generic refusal (unchanged)
  >= 2 (128)   ─► ONE named line ─► refusal  exit 1   <- the new row
```

## Dispatch line
config-max: none (a refusal, not a knob). template-max: none. code: `set -o pipefail` + a 4-line `rc=$?` case in the kid branch of `extensions/agi/hooks/agent-git/pre-commit`; nothing in cli.py changes.

## FALSIFIERS
- F1 (rc 1 at HEAD, measured: the hook exits 0), the leaf's probe: `bash -c 'T=$(mktemp -d); trap "rm -rf $T" EXIT; H=$PWD/extensions/agi/hooks/agent-git/pre-commit; cd $T && git init -q r && cd r && printf garbage > .git/index && ! AGI_TIER=kid AGI_PROJECT_ROOT=$T/r AGI_TREE_PROJECT_ROOT=$T/r AGI_AGENT_ID=a00-fixture bash $H 2>/dev/null'` -- rc != 0 after = true; the hook still rc 0 = false.
- F2 (named line): the same probe's stderr, captured, holds exactly one line naming `git diff --cached failed`; zero or two = false.
- F3 (control, unchanged): a healthy in-scope kid commit (source edit + its OWN node) exits 0; staged `.agi/config.json` still rc 1 with the ORIGINAL generic line (no `git diff --cached failed` text).
- F4 (empty stays): `git commit --allow-empty` as a kid in its own worktree, healthy index, still exits 0 (`scope-check` `all([])`); a hook that now refuses it = false.
- F5 (one rule): `git diff` on the hook adds no shell path predicate (no `case`/`[[` over a staged path); `cli.py` is untouched by the round.
- F6: `git grep -L pipefail -- extensions/agi/hooks/agent-git/pre-commit` returns 0 hits after (1 at HEAD).

## TESTS
- `extensions/agi/tests/test_git_commit_guard.py` ONE file, + 2 rows next to the `branch_kid` rows, reusing the `branch_kid` fixture, `branch_kid_env(wt, tree_root=str(wt))` and `_stage`: (a) `test_branch_kid_hook_refuses_on_a_failing_diff`: corrupt the worktree's index (`git rev-parse --git-path index` from `wt` -> write garbage; a LINKED worktree's index is not `wt/.git/index`), run `bash <hooks>/pre-commit` DIRECTLY under `branch_kid_env` (NOT `git commit`: git reads the index first and never reaches the hook), assert rc != 0 and exactly one stderr line containing `git diff --cached failed`; (b) `test_branch_kid_empty_staged_set_still_allowed`: healthy index, nothing staged, same direct run, rc 0. The existing rows `test_branch_kid_commits_in_scope_bytes` and `test_branch_kid_refuses_staged_config_json` are the in-scope and refusal controls (unchanged, must stay green). Synthetic agent id only.
- neighbourhood: `extensions/agi/tests/test_git_commit_guard.py` whole file (every `branch_kid_*` row).
```
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q -k 'failing_diff or empty_staged or branch_kid' --basetemp /tmp/pb3h
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q --basetemp /tmp/pb3hf
```
- then F1-F4 by hand.

## FILE SCOPE
extensions/agi/hooks/agent-git/pre-commit · extensions/agi/tests/test_git_commit_guard.py

## CEILING
kids <= 1 · pre-commit <= 8 production lines (pipefail + rc case + one echo) · tests <= 35 lines · pi-free parent · 0 USD · over it: drop the named-line conjunct and keep the bare pipefail (the leaf's minimum). `pipefail` is scoped to the kid block only: set it there, never at the top of the file (the parent path and the early `exit 0` guards read `git`/`cd` results that must not change).

## Agent Notes
PARENT REVIEW DG4.03 (a00-bc0bb923) -- ONE SUB-CLAUSE REFUTED, the claim demoted to a lean. Conjuncts 1 and 3 are PROVED by experiment:a00-0fe3e4c9-fb3c3b (commit a653d0cead) and re-measured by my own probes: corrupt index + kid tier -> rc=1 with exactly ONE named line; healthy empty staged set -> rc=0; staged config.json -> rc=1 generic, no double line; the a653d0cead^ bytes on the same fixture -> rc=0 fail-OPEN, so the new bytes are the causal difference. CONJUNCT 2 IS HALF FALSE as written here: it says a failing producer is "pipeline rc >= 2: git 128, cli.py crash". A cli.py crash is NOT rc>=2 -- an uncaught Python exception exits 1, and rc 1 is exactly the value the pipe already reserved for a genuine scope refusal, so the two are indistinguishable at the hook. Measured: a scope-check stub that dies rc=1 leaves the hook REFUSING rc=1 by the generic line with 0 named hits. The SAFETY claim (a failed producer never reaches exit 0) survives that; the ATTRIBUTABILITY claim (one named line naming the failed producer) does not. The claim is therefore demoted inconclusive_lean_proved:80 -- 3 of 4 sub-claims proved by a direct probe, 1 refuted by a direct probe, and the surviving defect is a message-quality gap, not a fail-open one. FIX, if anyone wants it: scope-check catches its own exception and exits 2 (one line in cli.py), after which the >=2 arm names a crash too.

## CORRECTIVE DH.DG4.10 -- hook attribution (director-general-4; mur mur-director-general-4-5 slice dg403-hook-pipefail, verify accept_with_residue)
Base: this loop tip b9f50b36a. pi-free parent, ONE kid. FILE SCOPE: extensions/agi/hooks/agent-git/pre-commit (the kid-scope block only) · extensions/agi/tests/test_git_commit_guard.py. CEILING <= 12 prod lines, <= 40 test lines.
1. (D1 + missed, confirmed) the refusal names WHICH stage failed: capture the pipe's per-stage codes IN THE SAME STATEMENT as the pipe (`PS=("${PIPESTATUS[@]}")` must be the very next command -- verify measured that `SCOPE_RC=$?` first clobbers PIPESTATUS to (0)). git diff rc != 0 -> "git diff --cached failed (rc N)"; scope-check rc >= 2 with a clean producer -> "scope-check failed (rc N)"; both refuse (exit 1). rc 1 from scope-check stays the ordinary scope refusal; rc 0/0 allows.
2. (missed) rows pin ATTRIBUTION, not just rc != 0: corrupted index -> the git line; a missing/dying scope-check (hook copy with no ../../bin, as verify reproduced) -> the scope-check line; the healthy in-scope control stays rc 0.
3. (D4 note, fold in) `set -o pipefail` is unset (or the pipe runs in a subshell) at the end of the block so the comment "scoped to THIS block" is true.
Demoted: the hypothesis body's refuted sub-clause (verify refuted as wording). Findings row (not this round): existing worktrees keep the spawning engine's hook path (dispatch.py pins GIT_CONFIG hooks at the spawning tree) -- pre-existing.
TESTS: test_git_commit_guard.py (+ test_cli.py -k scope), each --basetemp under /tmp; tmp repos only.
