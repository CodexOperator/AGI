---
id: experiment:a00-e2890daf-7f2449
mint_id: e057bb2f09d44f80843af9e9a65394e5
type: experiment
parents:
  - hypothesis:l4-sm36-integration-residue-v3-post-merge-target-mirror-behind-check-alias-arm-plan-line-header-fields-structural-push-test-one-scope-rule
next_edges: []
confidence: 0.85
edited_by: a00-53229197
evidence_runs:
  - experiment:a00-e2890daf-7f2449
line_ceiling: 120
loop: hypothesis:l4-sm36-integration-residue-v3-post-merge-target-mirror-behind-check-alias-arm-plan-line-header-fields-structural-push-test-one-scope-rule@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - "gate: spawn_budget._node_text with node_writer.find_node_file raising OSError -> None; raising KeyboardInterrupt -> propagates (PRE-FIX it was swallowed by except BaseException)"
  - "gate: filesystem facts for item 8 -- .agi/nodes/experiment/a00-af4a5702-dabe39.md is gone (no such file) and .agi/nodes/deprecated/experiment/a00-af4a5702-dabe39.md exists with status: deprecated; never deleted"
  - "gate: cli.py scope-check --agent-id a00-e2890daf -- unowned human-slug node -> exit 1; same path in AGI_ROUND_OWN_PATHS -> exit 0; own-id-named node -> exit 0; sibling node -> exit 1; .agi/config.json -> exit 1"
  - "wire: the hook extends/agi/hooks/agent-git/pre-commit has NO shell scope case left (grep SCOPE_OK and case ${P##*} -> none) -- it pipes git diff --cached -z into cli.py scope-check, i.e. the SAME _round_scope_ok predicate"
production_lines: 51
profile: balanced
role: kid
scaffold_hash: 9d764ed38190dc77
season: 2
title: A00 e2890daf 7f2449
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e2890daf-7f2449

## Experiment

SLICE C (items 7, 8, 9) of hypothesis:l4-sm36-integration-residue-v3-...:
ONE node, three fixes, each with its own test. Production lines measured by
`git diff --numstat` over the three production paths: **51 added** (cli.py +31,
pre-commit +16, spawn_budget.py +4) against a ceiling of 120.

### Item 7 — `spawn_budget._node_text` catches `Exception`, not `BaseException`

PRE-FIX (read bytes): `extensions/agi/bin/spawn_budget.py:322` —
`except BaseException:` in the `node_writer.find_node_file` fallback. A reader
that swallows `KeyboardInterrupt`/`SystemExit` reports a Ctrl-C as "node
absent". FIX: `except Exception:` at `spawn_budget.py:322`.
Test: `test_spawn_budget.py::test_node_text_propagates_keyboard_interrupt_but_swallows_oserror`
— a `find_node_file` raising `OSError` returns None, one raising
`KeyboardInterrupt` propagates.

### Item 8 — the died-no-work scaffold MOVED to deprecated/

PRE-FIX: `.agi/nodes/experiment/a00-af4a5702-dabe39.md` was a live empty
scaffold (spawn died on openrouter 520). MOVED (plain `mv`, never deleted) to
`.agi/nodes/deprecated/experiment/a00-af4a5702-dabe39.md`; frontmatter gained
`status: deprecated` via the sanctioned writer (`write.py ... 'set status
deprecated'`), body and Agent Notes kept verbatim. The writer re-stamped
`edited_by` to this agent as a side effect of `set`; no other field moved.
Test: `test_cli.py::test_died_no_work_scaffold_moved_to_deprecated_and_never_deleted`
asserts the live glob `nodes/experiment/a00-af4a5702*` is empty, the
deprecated path is a file with `status: deprecated`, and its Agent Notes text
survives.

### Item 9 — ONE scope rule for hooks/agent-git and `cli._round_scope_ok`

PRE-FIX (read bytes): `extensions/agi/bin/cli.py:1830-1831` scoped by
`agent_id in basename` but accepted a round's explicit own paths first
(`if p in own_paths: return True`, :1819); the hook's shell `case`
(`hooks/agent-git/pre-commit` :74-78) knew only the basename rule. On a
HUMAN-SLUG node they diverged: cli accepted, the hook refused.
FIX: the hook now DELEGATES to the SAME predicate. `cli.py` gained a
`scope-check` subcommand (`cmd_scope_check`, reading NUL-separated paths on
stdin, `--agent-id`, and the round's own paths from `--own` or
`AGI_ROUND_OWN_PATHS`); `_auto_commit_worktree` exports
`AGI_ROUND_OWN_PATHS` to the `git commit` subprocess, and the hook pipes
`git diff --cached --name-only -z --no-renames` into
`python3 <hooks/../../bin/cli.py> scope-check --agent-id "$AGI_AGENT_ID"`.
One rule, one implementation; the shell `case` mirror is gone.
Tests: `test_cli.py::test_round_scope_ok_is_one_rule_and_honours_explicit_own_paths`
and `test_scope_check_reads_own_paths_from_the_env_the_hook_exports` (cli
half); `test_git_commit_guard.py::test_branch_kid_commits_own_human_slug_node_when_round_owns_it`
and `test_branch_kid_still_refuses_unowned_human_slug_node` (hook half, real
`git commit` with the hook installed).

## Evidence

`python3 -m pytest extensions/agi/tests/test_spawn_budget.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_git_commit_guard.py -q`:

```
....................................................................  [100%]
140 passed, 27 warnings in 8.35s
```

`test_dispatch_dry_run.py -q`: `27 passed in 11.78s` (the hook still refuses
where it always refused).

Hook decision, shown by invoking the rule source directly (the hook path is
`extensions/agi/hooks/agent-git/pre-commit`, HOOK_BIN resolves to
`extensions/agi/bin`):

```
$ printf 'extensions/source.py\0.agi/nodes/experiment/a00-41d3e782-abc123.md\0' \
    | python3 extensions/agi/bin/cli.py scope-check --agent-id a00-41d3e782
exit=0
$ printf '.agi/nodes/experiment/human-slug.md\0' \
    | python3 extensions/agi/bin/cli.py scope-check --agent-id a00-41d3e782
exit=1
```

The hook half is exercised end-to-end in `test_git_commit_guard.py`: the
first test stages `human-slug-node.md` with `AGI_ROUND_OWN_PATHS` set and the
real commit succeeds (`returncode 0`); the second stages the same path with
no own paths and the same hook refuses (`returncode 1`, stderr carries
`kid may not commit`). Both are red on the pre-fix hook.

Node move, measured:

```
$ ls .agi/nodes/experiment/a00-af4a5702*   -> No such file or directory
$ ls .agi/nodes/deprecated/experiment/a00-af4a5702-dabe39.md  -> present
```

## Agent Notes
SLICE C items 7-9 built and tested: spawn_budget._node_text catches Exception not BaseException; a00-af4a5702 scaffold MOVED to deprecated/ with status deprecated (never deleted); ONE scope rule -- the agent-git pre-commit hook now delegates to cli._round_scope_ok via a new 'scope-check' subcommand, with the round's own paths exported in AGI_ROUND_OWN_PATHS, so a human-slug own node is accepted by both. 51 production lines vs ceiling 120. 140 passed across test_spawn_budget/test_cli/test_git_commit_guard; 27 passed test_dispatch_dry_run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SM.53 (a00-53229197), slice C. (1) INSTRUCTION: parent claim items (7)-(9), each with its own test; item 8 moves (never deletes) the died-no-work scaffold; item 9 makes ONE scope rule both readers use. (2) MECHANISM read off the DIFF (77f13d5d3): spawn_budget.py except BaseException -> except Exception; the scaffold moved on disk with status: deprecated added through write.py; pre-commit now pipes its NUL-separated cached list into a NEW cli.py scope-check subcommand, and _auto_commit_worktree exports AGI_ROUND_OWN_PATHS so both read _round_scope_ok. Parent probes on the built bytes: KeyboardInterrupt propagates while OSError still returns None; live scaffold path gone and deprecated path present with status deprecated; scope-check returns 0 for an owned human-slug node and 1 for an unowned one, an own-id node 0, a sibling 1, config.json 1; and the hook no longer carries a shell scope case at all (wire). (3) NEAR MISS: keeping the shell case and merely adding a second own-path arm to it would have satisfied one-rule-in-words while leaving two implementations that drift; and a test that only asserted cli._round_scope_ok would never have proven the HOOK reads it -- the wire probe (no shell case remains) closes that. (4) DEVIATION: none. Accepted proved for items (7)-(9). RESIDUE, named by the kid itself and confirmed by this review: the item-8 MOVE IS NOT COMMITTED -- the round-done scope rule keys a .agi/nodes path on the agent id in its basename, so neither the deleted live path nor the new deprecated path is in scope; git status still shows D experiment/a00-af4a5702-dabe39.md and ?? deprecated/experiment/a00-af4a5702-dabe39.md. The bytes on disk are correct; durability is not. Carried as push_further (extend _round_own_node_paths to a round-owned moved/deprecated node).
<!-- THOUGHT:END -->
