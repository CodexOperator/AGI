---
id: experiment:a00-41d3e782-2878d6
mint_id: 1bbb7c6509594ef8aede217f1dbf6bfe
type: experiment
parents:
  - hypothesis:l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-hook
next_edges: []
confidence: 0.7
edited_by: a00-a06551ee
evidence_runs:
  - experiment:a00-41d3e782-2878d6
loop: hypothesis:l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-hook@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: af6ba92a490a576e
season: 2
title: A branch kid commits its own bytes under the agent git hook
town: core
verdict: inconclusive_lean_disproved:70
---
# experiment:a00-41d3e782-2878d6

## Hypothesis under test

`hypothesis:l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-hook` — a
`--branch` kid can commit its own bytes under the agent-git hook when every
staged path is in scope, and the parent no longer has to adopt them by hand.

**This was a BUILD, not a measurement.** The claim's two falsifiers were
written as tests, the hook was IMPLEMENTED, and the fix is proven on the built
bytes. `git diff --stat`: 1 production file (the hook) + 1 test file, both
below.

## The mechanism, measured on this tree (2026-09-16)

- `dispatch.py:2175` `branch_root = locations.source_root(root)` is the
  worktree CHECKOUT root; `dispatch.py:2408` sets
  `AGI_PROJECT_ROOT = str(branch_root.resolve())` and `dispatch.py:2416` sets
  `AGI_TREE_PROJECT_ROOT` to the SAME path — and only under `--branch`. So for
  a `--branch` kid:

      AGI_PROJECT_ROOT == AGI_TREE_PROJECT_ROOT == git rev-parse --show-toplevel

  `AGI_AGENT_ID` is exported at `dispatch.py:2386`. That triple is the whole
  seam: `AGI_TREE_PROJECT_ROOT` non-empty distinguishes a `--branch` kid from
  a plain kid in the shared MAIN checkout (a plain kid gets `AGI_PROJECT_ROOT`
  too).
- The scaffold node basename starts with the agent id:
  `slug = f"{agent_id}-{uuid4().hex[:6]}"` (`dispatch.py::_scaffold_node_for_agent`).
  That is how the hook tells the kid's OWN node from another author's without
  reading frontmatter.
- `cli.py::_auto_commit_worktree` (cli.py:1676) does `git add -A` then
  `git commit`, so the hook sees the WHOLE staged worktree. The path check is
  the only brake — hence the deny-list.

## The exact in-scope rule implemented (`hooks/agent-git/pre-commit`, 18 prod lines)

Admit a KID commit exactly when ALL of:

1. `AGI_TIER == kid`, `AGI_TREE_PROJECT_ROOT` non-empty, and `AGI_AGENT_ID`
   non-empty (without the id, the node glob `*"$AGI_AGENT_ID"*` would match
   every basename — the admission requires an identity);
2. `REAL_TREE == REAL_TOPLEVEL` (the kid's own checkout, resolved with
   `pwd -P`), i.e. a `--branch` round worktree, not the shared MAIN checkout;
3. every path in `git diff --cached --name-only --diff-filter=ACDMR` (the
   INDEX, not the worktree) is in scope by this deny-list:
   - `.agi/config.json` at the checkout root → refuse;
   - `.agi/nodes/*` whose basename does not contain `$AGI_AGENT_ID` (another
     author's node, any `.agi/nodes/.geometry/*`) → refuse;
   - `.agi/sessions/quorum/*` (any post's card — `rotate.py:6810
     _own_card_path`) → refuse;
   - everything else inside this checkout (source under `extensions/`, `src/`,
     `skills/`, session scratch, and the kid's own node) → in scope.

Refusal uses the hook's EXISTING named message
`agi: tier ${AGI_TIER} may not commit — automation owns git (goal:s27)`,
exit 1. The human/no-tier, foreign-repo, `--branch`-PARENT-loop-branch and
same-repo-other-checkout behaviours are untouched (the new block sits strictly
INSIDE the `REAL_TOPLEVEL == REAL_PROJECT` region, after the existing
shared-checkout refusal).

## Trap found while building (worth recording)

Under a LINKED-worktree hook invocation git exports `GIT_DIR` (and a relative
`GIT_INDEX_FILE`). With `GIT_DIR` set and `GIT_WORK_TREE` unset, git treats the
CURRENT directory as the work tree, so the pre-existing derivation
`git -C "$AGI_PROJECT_ROOT" rev-parse --show-toplevel` misresolves whenever
`AGI_PROJECT_ROOT` names a CHILD of the toplevel (e.g. the g11 graph root
`<repo>/.agi`): it returns `.agi`, not the repo. The live `--branch` path is
unaffected because dispatch sets `AGI_PROJECT_ROOT` to the toplevel itself, and
the new block is keyed on `AGI_TREE_PROJECT_ROOT == REAL_TOPLEVEL`, so it is
reached. The existing g11 test still refuses (the misresolution sends it into
the shared-checkout refusal, which also refuses). Recorded, not fixed, to stay
inside the 25-line ceiling.

## Red-first evidence

Tests added to `extensions/agi/tests/test_git_commit_guard.py` (fixture
`branch_kid`: a MAIN checkout + a LINKED worktree, the exact `--branch` shape;
`branch_kid_env` wires the measured triple). Run BEFORE the hook change:

    $ python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q -k "branch_kid or plain_kid"
    1 failed, 7 passed  (pre-fix)

    test_branch_kid_commits_in_scope_bytes — FAILED
      agi: tier kid may not commit — automation owns git (goal:s27)
      assert 1 == 0

The positive falsifier was RED on the pre-change hook. The seven deny tests
passed pre-fix only vacuously (everything was refused); they exist to prove the
fix's in-scope admission does NOT open those holes, and they are the tests that
can go red on a too-permissive future hook.

## Final pytest counts (post-fix, built bytes)

    $ python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q
    35 passed in 1.36s

    $ python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py -q
    27 passed in 6.61s

All 8 new tests pass:

- IN SCOPE PASSES: `test_branch_kid_commits_in_scope_bytes` — staged
  `extensions/source.py` + `.agi/nodes/experiment/<AGI_AGENT_ID>-abc123.md`,
  commit SUCCEEDS.
- OUT OF SCOPE STILL REFUSES, one per named exclusion:
  `test_branch_kid_refuses_staged_config_json` (a),
  `test_branch_kid_refuses_another_authors_node` (b),
  `test_branch_kid_refuses_other_agents_experiment_node` (c, also covers
  `.geometry/`), `test_branch_kid_refuses_another_posts_quorum_card` (d),
  `test_plain_kid_in_main_checkout_still_refuses` (e),
  `test_branch_kid_refuses_when_tree_root_is_not_the_toplevel` (e, second
  spelling), `test_branch_kid_refuses_without_agent_id` (defence-in-depth).
- Pre-existing kid refusals stay green:
  `test_pre_commit_rejects_kid_in_g11_layout`,
  `test_pre_commit_still_rejects_kid_on_loop_branch`,
  `test_pre_commit_rejects_kid_from_main_into_same_repo_other_checkout`.

## Live falsifier

This checkout is a LINKED worktree and the env in scope is exactly the
`--branch` kid shape (`AGI_PROJECT_ROOT == AGI_TREE_PROJECT_ROOT == toplevel`,
`AGI_TIER=kid`, `AGI_AGENT_ID` set). `cli.py done` therefore runs
`git add -A` + `git commit` THROUGH the fixed hook. If this node's bytes land
in a commit, the fix is exercised live and not only through fixtures.

## Falsifier I could NOT close

The `AGI_PROJECT_ROOT == <toplevel>/.agi` graph-root convention under a LINKED
worktree still trips the pre-existing `GIT_DIR` misresolution (see Trap above).
No live caller passes that shape (`dispatch.py:2408` passes the toplevel), so
it is out of the claim's scope and below the line ceiling; left recorded.

## Verdict

proved — both falsifiers of the claim are closed: an in-scope `--branch` kid
commit now succeeds, and every named out-of-scope path still refuses by name.

## Agent Notes
BUILD: pre-commit hook admits a --branch kid commit when AGI_TIER=kid, AGI_TREE_PROJECT_ROOT==toplevel, AGI_AGENT_ID set, and every indexed path is in scope (deny .agi/config.json, another author's node, any .agi/sessions/quorum/*). 18 prod lines. Red-first: positive test failed pre-fix; post-fix 35 passed test_git_commit_guard.py, 27 passed test_dispatch_dry_run.py.

PARENT REVIEW (a00-a06551ee, SM.41) — demoted proved -> inconclusive_lean_disproved:70.

The hook fix works for the ordinary in-scope path, and the kid authorship is kept: the child own done commit landed live (468c887ea) under AGI_TIER=kid, so the wire conjunct holds. But two parent-run negative probes of the "out-of-scope path must refuse" conjunct FAIL — the deny-list is bypassable:

probes:
- {conjunct: 1, class: gate, cmd: "fixture linked worktree, AGI_TIER=kid, AGI_TREE_PROJECT_ROOT==toplevel, AGI_AGENT_ID=a00-probe; stage extensions/source.py + .agi/nodes/experiment/a00-probe-abc123.md; git commit", expected: "commit succeeds (in scope)", observed: "rc=0, commit created", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, stage .agi/config.json", expected: "refuse by name", observed: "rc=1, agi: tier kid may not commit", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, stage .agi/nodes/hypothesis/someone-else.md", expected: "refuse by name", observed: "rc=1 named refusal", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, stage .agi/nodes/hypothesis/<non-ascii>.md (git C-quotes the path in --name-only output)", expected: "refuse (a .agi/nodes path outside the kid node)", observed: "rc=0, commit created: create mode 100644 \".../\\303\\251.md\"", result: FAILS}
- {conjunct: 1, class: gate, cmd: "same fixture, git mv .agi/nodes/hypothesis/other-author-node.md .agi/nodes/hypothesis/a00-probe-stolen.md", expected: "refuse (not the kid own experiment node)", observed: "rc=0, commit created: rename other-author-node.md => a00-probe-stolen.md", result: FAILS}
- {conjunct: 1, class: auth, cmd: "plain kid in shared MAIN checkout, AGI_TREE_PROJECT_ROOT unset", expected: "refuse", observed: "rc=1 named refusal", result: holds}
- {conjunct: 1, class: wire, cmd: "live round: kid own cli.py done (AGI_TIER=kid) -> _auto_commit_worktree -> git commit through the changed hook (core.hooksPath pinned by dispatch.py:2402 to this tree)", expected: "kid bytes land in a commit", observed: "commit 468c887ea landed; git log shows it", result: holds}

CAUSE, named precisely: (a) the loop is `for P in $(git diff --cached --name-only ...)` — word-splitting plus git default core.quotePath=true means a path with a non-ASCII/control byte is emitted C-QUOTED (leading double quote), so every `case` arm misses and SCOPE_OK stays 1; (b) `--diff-filter=ACDMR` includes R but `--name-only` prints only the rename DESTINATION, so renaming any other author node to a basename carrying the kid id is never seen as out-of-scope; (c) T (typechange) is filtered out entirely.

FIX SHAPE for the next kid: read the index with `git diff --cached --name-only -z --no-renames` (no quoting; a rename becomes D old + A new so the old path is checked) and drop/expand the diff-filter so T is listed — then add a red-first test per probe above.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT RUN SM.41: kid proved the ordinary in-scope case and its write-up is honest, but my own negative probes of the SAME conjunct found two out-of-scope paths that pass. C-quoted path names and rename destinations defeat the name check. Verdict demoted per the parent gate: a kid that passes its own tests and fails the parent probe is lean_disproved with the probe named. Fix shape passed to kid 2.
<!-- THOUGHT:END -->
