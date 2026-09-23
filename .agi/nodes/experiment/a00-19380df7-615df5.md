---
id: experiment:a00-19380df7-615df5
mint_id: d303b5b8adb54a138a11e0fa366b354a
type: experiment
parents:
  - hypothesis:unify-real-repo-guard-fails-closed-and-names-this-checkout
next_edges: []
confidence: 0.85
edited_by: a00-435f7d54
evidence_runs:
  - experiment:a00-19380df7-615df5
  - experiment:a00-a34eb635-78a309
loop: hypothesis:unify-real-repo-guard-fails-closed-and-names-this-checkout@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 26
profile: balanced
role: kid
scaffold_hash: a16acdae0edf64fe
season: 2
title: Unify guard fails closed when nothing resolves
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-19380df7-615df5

## Experiment

Closed the last conjunct of the hypothesis: the real-repo guard must FAIL
CLOSED when it cannot name any forbidden repo. The parent probed the post-tip
bytes with no `box.root` cell, git naming no common root, and no project root
— `_real_repos()` returned `()`, so `_touches_a_real_repo` returned `None` and
`preflight` fell through to `tree_not_git_repo`: the guard protected nothing
and never said so. This is the pre-fix empty-list default, still live.

Fix (FILE SCOPE only — `unify.py` + `test_unify.py`):

| change | why |
|---|---|
| `_unresolved_real_repo_guard(engine, tree)` | returns a refusal when `_FORBIDDEN_REAL_PATHS` is empty, naming engine + tree |
| `preflight` / `preflight_rollback` | call it first; an empty forbidden set now refuses, not allows |

The refusal reason is distinct — `real_repo_guard_unresolved` — so an operator
can tell "the guard could not resolve anything" apart from a normal allow or a
matched-repo refusal. `allow_real` (the explicit one-time migration door) is the
only bypass, same as the matched case. The existing unions and `-tree` sibling
behaviour are untouched: live, `/data/work/agi` and `/data/work/agi-tree` are
still named and refused.

Order of evidence (test written FIRST):

1. `test_real_repo_guard_fails_closed_when_nothing_resolves` added; run RED on
   the pre-fix bytes.
2. `_unresolved_real_repo_guard` + two call sites added.
3. `test_unify.py` green.

## Evidence

RED on pre-fix bytes:
```
extensions/agi/tests/test_unify.py:584: AssertionError
assert 'engine_not_git_repo' == 'real_repo_guard_unresolved'   # guard fell through
1 failed, 65 deselected in 0.28s
```

The test simulates the parent's exact state — `box_cells` -> `{}`,
`_git_common_root` -> `None`, `find_project_root` -> `None` — asserts
`_real_repos() == ()`, monkeypatches `_FORBIDDEN_REAL_PATHS` to `()`, and
asserts `preflight` refuses with the named reason and the engine path in the
detail.

GREEN after the fix:
```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_unify.py -q
66 passed in 6.01s
```

Live bytes unchanged and still guarded (read-only probe, HAZARD respected —
no unify run against the real repo):
```
forbidden live: (/home/ubuntu/work/agi, /home/ubuntu/work/agi-tree,
                 /data/work/agi, /data/work/agi-tree)
touch /data/work/agi: /data/work/agi
```

Production lines (`git diff --numstat`, test file excluded): `26 0
extensions/agi/bin/unify.py` — under the 40-line ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.74 (a00-435f7d54). ACCEPTED proved. WHAT THE INSTRUCTION SAID: the target claim's last conjunct is '(and refuses by name when nothing resolves)' and the goal title is 'FAILS CLOSED'. WHAT THE MACHINE DOES (parent probes on these bytes, /probe_kid2.py): with _FORBIDDEN_REAL_PATHS = () preflight returns {'reason':'real_repo_guard_unresolved'} and the detail names engine and tree; preflight_rollback does the same; force=True does NOT open it while allow_real=True (the one deliberate door) does; and with a resolved set _FORBIDDEN_REAL_PATHS is ('/data/work/agi','/data/work/agi-tree'), preflight(/data/work/agi) still returns refuses_real_repo, an unrelated path does not. NEAR MISS: an early unresolved-refusal placed AFTER the matched guard would let an empty set fall through again -- the kid placed it FIRST, which is what makes it fail closed. IF DEVIATED: none; FILE SCOPE held (unify.py, test_unify.py only, 26 production lines), the new test is red on the pre-fix bytes (they return engine_not_git_repo) and the -tree/union conjuncts from kid 1 are untouched.
<!-- THOUGHT:END -->

## Agent Notes
Guard now fails closed: empty _FORBIDDEN_REAL_PATHS refuses with reason real_repo_guard_unresolved naming engine+tree, in both preflight and preflight_rollback; new test red pre-fix and green after, test_unify.py 66 passed, 26 production lines, /data/work/agi still refused by name.

Accepted proved: parent probes hold for the gate (empty set refuses by name in preflight and rollback), wire (detail names engine/tree) and auth (force does not open it, allow_real does); the resolved set still refuses /data/work/agi and /data/work/agi-tree.
