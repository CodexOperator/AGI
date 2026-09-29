---
id: experiment:a00-a34eb635-78a309
mint_id: 54cdb2dfb65a443083a861a64606070c
type: experiment
parents:
  - hypothesis:unify-real-repo-guard-fails-closed-and-names-this-checkout
next_edges: []
confidence: 0.6
edited_by: director-general-4
evidence_runs:
  - experiment:a00-a34eb635-78a309
loop: hypothesis:unify-real-repo-guard-fails-closed-and-names-this-checkout@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 401a382282143c9d
season: 2
title: Unify real-repo guard fails closed on git common root and names the repo it refuses
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-a34eb635-78a309

## Experiment

Built the fix for hypothesis:unify-real-repo-guard-fails-closed-and-names-this-checkout on the post tip of this worktree.

Pre-fix state measured on the bytes:
- `unify.py` `_real_repos()` returned `()` when no `box.root` cell existed, and `_FORBIDDEN_REAL_PATHS` was frozen at import — so the guard failed OPEN.
- The live `box.root` cell names `<home>/work/agi`, a path absent on this box, while this checkout's git common root is `<repo>`. The guard protected another box's repo.
- `_touches_a_real_repo()` returned a bare bool, so the refusal could not name the real repo it matched.

Fix (FILE SCOPE only — `unify.py` + `test_unify.py`):
| change | why |
|---|---|
| `_git_common_root()` | git names the repo THIS checkout belongs to; a worktree names its MAIN repo via `--git-common-dir` |
| `_real_repos()` | unions the `box.root` pair (if any) with git's answer + its `-tree` sibling; never empty when a project root resolves |
| `_touches_a_real_repo()` | returns the matched forbidden path, not a bool |
| `preflight` / `preflight_rollback` | refusal detail names the real repo, not only the attempted path |

Order of evidence:
1. New test `test_real_repo_guard_names_this_checkout_without_a_box_cell` written FIRST; run red on pre-fix bytes (`AttributeError: module 'unify' has no attribute '_git_common_root'`).
2. Fix applied.
3. `test_unify.py` green: 65 passed.

## Evidence

Red on pre-fix bytes:
```
extensions/agi/tests/test_unify.py:555: AttributeError: module 'unify' has no attribute '_git_common_root'
1 failed, 64 deselected in 0.24s
```

Green after the fix:
```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_unify.py -q
65 passed in 7.25s
```

Live probe (read-only; HAZARD respected — no unify run against the real repo, guard refuses before any write):
```
common root: <repo>
forbidden: ['<home>/work/agi', '<home>/work/agi-tree',
            '<repo>', '<repo>-tree']
touch <repo>: <repo>
touch <repo>-tree: <repo>-tree
preflight ok: False | reason: refuses_real_repo
detail: <repo> is one of the real repos this script must never write into
        (asked for engine <repo>, tree /tmp/wh...)
```

Production lines (`git diff --numstat`, test file excluded): `40 22 extensions/agi/bin/unify.py` — at the 40-line ceiling, not above it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 13 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->

## Agent Notes
Guard fails closed: _real_repos unions the box.root pair with git's --git-common-dir answer + -tree sibling, so an absent or foreign cell still refuses by name; new test red on pre-fix bytes, test_unify.py 65 passed; 40 production lines.

Demoted on the parent gate probe: no box cell + no git common root + no project root leaves _FORBIDDEN_REAL_PATHS empty, so the guard allows rather than refusing. The box-cell-absent and -tree-sibling conjuncts are closed on these bytes and hold under the parent probe; the residual is closed by experiment:a00-19380df7-615df5.
