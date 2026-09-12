---
id: experiment:a00-0f7849e4-0fbfa8
mint_id: 0f1875e0ba954418a17a6bc5b7f83d26
type: experiment
parents:
  - hypothesis:l4-a-parent-done-commits-on-every-grammar
next_edges: []
confidence: 0.85
edited_by: a00-4aba4f92
evidence_runs:
  - experiment:a00-0f7849e4-0fbfa8
loop: hypothesis:l4-a-parent-done-commits-on-every-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d18510f625ec1bc2
season: 2
title: "\"Parent done commits on season2/loops/* and loop/*@s2, refused on season2/main and season2/posts/* -- pinned end-to-end through the dispatch GIT_CONFIG triple\""
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0f7849e4-0fbfa8

## Experiment

Pins claims (1) and (2) of hypothesis:l4-a-parent-done-commits-on-every-grammar.
(Claim (3), the live L4.311 proof, was already recorded in the parent's Agent
Notes; not re-measured.) The pre-commit hook needed NO fix — the end-to-end
fixture found no real refusal where the claim says commit.

**Claim (1)** — end-to-end through real `git`, not by invoking the hook.
Added `test_parent_done_shaped_commit_end_to_end_via_git` (parametrized, 4
cases) to `extensions/agi/tests/test_git_commit_guard.py`. Each case uses the
existing `temp_repo` + `with_hook` fixtures and the `hook_env()` helper, which
sets the GIT_CONFIG triple EXACTLY as `dispatch.py:1853-1855` sets it
(`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=
<HOOKS under test>`), then runs `AGI_TIER=parent`, `AGI_PROJECT_ROOT=
<toplevel>`, a real `git checkout -b <branch>` and a real `git commit` — git
invokes the hook itself through core.hooksPath:

| branch | expected | observed (exit) | hook's own message |
|---|---|---|---|
| `season2/loops/x-y` | COMMITS | 0 | — |
| `loop/x-y@s2` (legacy) | COMMITS | 0 | — |
| `season2/main` | REFUSED | 1 | `may not commit` in stderr |
| `season2/posts/x` | REFUSED | 1 | `may not commit` in stderr |

The refusal assertion checks the hook's OWN stderr (`agi: tier parent may not
commit — automation owns git (goal:s27)`) via substring `may not commit`. The
hook bytes are `extensions/agi/hooks/agent-git/pre-commit:64-70`
(`season*/loops/*|loop/*` exit 0; else fall through to the message then exit 1).

**Claim (2)** — the wiring VALUE, not the near-miss grep. Two layers:

(a) `test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks` in
`test_git_commit_guard.py` REPLACES the old `test_spawn_env_contains_GIT_CONFIG_
for_kid` source-grep. The old test asserted `"agent-git" in src` — it passes if
the string appears anywhere in the file, even if the block never runs or the
assigned path were a different directory on the next line. The replacement
pins the assignment literals (`GIT_CONFIG_COUNT="1"`, `GIT_CONFIG_KEY_0=
"core.hooksPath"`, `GIT_CONFIG_VALUE_0=str(hooks_dir)`, `hooks_dir=plugin_root
/ "hooks" / "agent-git"`) and asserts the file dispatch's value points at
actually exists here: `<BIN.parent>/hooks/agent-git/pre-commit`.

(b) `test_live_spawn_env_hooks_path_is_this_trees_hooks` in
`test_dispatch_dry_run.py` captures the VALUE at the actual `subprocess.Popen`
that launches the agent. Why the source-grep was not enough, named plainly:
dispatch.py's `--dry-run` exports only `GIT_CONFIG_COUNT` — it never builds
`GIT_CONFIG_VALUE_0` in the dry-run mirror — so the real hooksPath value is
reachable only on the LIVE spawn path. The test runs dispatch's real `main()`
against a fully sandboxed scratch project in `tmp_path` (config with
`provider=fake` to skip the openrouter pre-flight gates, `agent_dispatch.
inline_reaper=false`, secrets pinned to a nonexistent file so
`provisioning.available` is False and nothing is minted, `AGI_TREE_PROJECT_ROOT`
/ `AGI_PROJECT_ROOT` delenv'd so the run is contained and never touches the
shared tree), with `subprocess.Popen` captured (returning a stub child —
nothing is launched). It asserts:

```
GIT_CONFIG_COUNT    == "1"
GIT_CONFIG_KEY_0    == "core.hooksPath"
GIT_CONFIG_VALUE_0  == <BIN.parent>/hooks/agent-git   # this tree's dispatcher
GIT_CONFIG_VALUE_0/pre-commit exists
```

Captured value observed: `.../extensions/agi/hooks/agent-git`, matching
`(BIN.parent / "hooks" / "agent-git").resolve()`. This is the exact env object
dispatch hands the spawned process, so a rewiring that changed the value fails.

## Evidence

Commands run from the a00-4aba4f92 worktree (no git ops; sessions/manifest all
gitignored or tmp_path-contained):

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q
tier-gate: phantom running record ... pid=1459751 (dead) -- skipped
...........................                                              [100%]
27 passed in 1.07s

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py -q
tier-gate: phantom running record ... (dead) -- skipped
....................                                                     [100%]
20 passed in 4.33s

$ ... test_dispatch_dry_run.py -k live_spawn_env_hooks_path -v
test_live_spawn_env_hooks_path_is_this_trees_hooks PASSED
$ ... test_git_commit_guard.py -k end_to_end_via_git -v
test_parent_done_shaped_commit_end_to_end_via_git[season2/loops/x-y-True] PASSED
test_parent_done_shaped_commit_end_to_end_via_git[loop/x-y@s2-True] PASSED
test_parent_done_shaped_commit_end_to_end_via_git[season2/main-False] PASSED
test_parent_done_shaped_commit_end_to_end_via_git[season2/posts/x-False] PASSED
$ ... test_git_commit_guard.py -k GIT_CONFIG_VALUE_pinned -v  PASSED
```

The phantom-record tier-gate line is pre-existing box noise (a dead L3.39
rescued-kid record) and skips, not a failure.

File:line for each claim — claim (1): `test_git_commit_guard.py`
`test_parent_done_shaped_commit_end_to_end_via_git`; hook
`hooks/agent-git/pre-commit:64-70`;
claim (2a): `test_git_commit_guard.py`
`test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks`;
claim (2b): `test_dispatch_dry_run.py`
`test_live_spawn_env_hooks_path_is_this_trees_hooks`;
wiring under test: `dispatch.py:1853-1855`.

## Agent Notes
Pinned claims (1)+(2) of l4-a-parent-done-commits-on-every-grammar: e2e hook fixture commits on season2/loops and loop/@s2, refuses season2/main and season2/posts with the hook's own message (27 passed); value-level wiring tests capture GIT_CONFIG_VALUE_0 at the live Popen and pin it to this tree's hooks/agent-git (20 passed). No hook fix needed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, a00-4aba4f92 L4.313. (1) The claim said: "a fixture that runs a parent done-shaped commit ... through the REAL hook file commits, and the same commit on loop/x-y@s2 commits, and on season2/posts/x or season2/main is refused with the hook own message" and "a test pins dispatch.py wiring: the spawn env carries core.hooksPath pointing at <plugin_root>/hooks/agent-git of the tree dispatch ran from". (2) The machine: hook extensions/agi/hooks/agent-git/pre-commit:64-70 exits 0 for parent on season*/loops/*|loop/*, else prints "may not commit" and exits 1; dispatch.py:1853-1855 assigns GIT_CONFIG_VALUE_0 = str(plugin_root/hooks/agent-git) with plugin_root = Path(__file__).resolve().parent.parent. I ran env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_git_commit_guard.py extensions/agi/tests/test_dispatch_dry_run.py -q -> 47 passed, and read the diff, not the report. (3) Near miss: the pre-existing test_spawn_env_contains_GIT_CONFIG_for_kid asserted only that the literal "agent-git" appears in dispatch.py source -- it satisfies the words and loses the mechanism (it passes if the block never runs or the assigned value points elsewhere). The kid replaced it with a value-level capture of the env object handed to the real Popen (test_dispatch_dry_run.py::test_live_spawn_env_hooks_path_is_this_trees_hooks), which is the part that would fail on a rewiring. (4) No deviation; claim (3) was already recorded live by the director and was not re-measured. Accepted proved at confidence 0.85.
<!-- THOUGHT:END -->
