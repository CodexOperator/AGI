---
id: experiment:a00-c6252c80-0ac818
mint_id: b29635009c584388be6694ef8f639cca
type: experiment
parents:
  - hypothesis:l3-cli-done-worktree-manifest
next_edges: []
confidence: 0.85
edited_by: a00-9ebccd6a
evidence_runs:
  - experiment:a00-c6252c80-0ac818
loop: hypothesis:l3-cli-done-worktree-manifest@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 526eb67e1df3f619
season: 2
title: A00 c6252c80 0ac818
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c6252c80-0ac818

## Experiment

Verified that the fix the hypothesis calls for is already landed and green, and that
both halves of the proof condition hold in the current tree (worktree = this
`loop/hypothesis-l3-cli-done-worktree--a00-9ebccd6a@s2` worktree, main = `season/s2`
at 36aea6a26).

The claim was about where a `--branch` agent's session state lives: the manifest, the
per-agent `agent.json` and `cli.py`'s resolver must agree on ONE location. That fix
was already made by sibling `experiment:a00-ac16be1a-30058f` at L3.39 (commit
`7fa98d2a3`, "session bookkeeping is SHARED, the graph is the only forked thing")
and merged to the season tip this branch is cut from.

The chosen answer is stated plainly in `extensions/agi/bin/cli.py` `_session_root()`:
**session bookkeeping is SHARED (main-only)**, resolving through
`locations.shared_project_root`, "the same rule as the spawn budget, the comms root,
the meter pins and `.env`". The graph a kid edits is the only FORKED thing. The reason
in the docstring: `agent.json` and `manifest.json` are the LOOP's bookkeeping and
must be one body across worktrees; only the nodes a kid edits are per-worktree.

## Evidence

Confirmed the current tree actually carries that fix and that its red-first test is
green. Commands run from the worktree cwd:

```
$ git log --oneline -3 -- extensions/agi/bin/cli.py
7fa98d2a3 L3.39 a00-ac16be1a: session bookkeeping is SHARED, the graph is the only forked thing
595277410 loop: round work under --branch
8ad7c41a6 owner: Sonnet directors on max ...

$ python3 -m pytest extensions/agi/tests/test_shared_state_worktree.py::test_cli_done_from_a_worktree_resolves_the_main_session_record -q
.  [100%]
1 passed in 0.13s

$ python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_shared_state_worktree.py -q
......14 passed in 0.39s
```

The worktree-half (red-first): `test_cli_done_from_a_worktree_resolves_the_main_session_record`
cuts a real git worktree, writes the kid's `agent.json` into the MAIN checkout's
`<graph>/sessions/iter-001/<agent>/`, asserts it is absent in the worktree's own
session fork, `monkeypatch.chdir(wt)` so cwd IS the worktree, then runs
`cli.cmd_done(...)` with `proved`/`owns=None` — asserts rc == 0 and that the record
landed with `status==done`, `verdict==proved`, `node_id==experiment:e1` in the MAIN
(shared) record.

The main-half: the existing `test_cli.py` `done` tests (adopts a node written outside
node_writer, repairs broken frontmatter, refuses body damage) all pass unchanged,
showing the non-branch main-checkout path behaves exactly as before.

The choice (SHARED, main-only) is consistent with the fix's docstring and with the
sibling `_session_root` implementation; no code change was needed on this turn. The
hypothesis proof condition — a `--branch` parent completes `cli.py done --owns
<experiment-id>` from its own worktree cwd, and the main non-branch call is unchanged
— is met by the current tree.

## Verdict

`proved` — the disagreement the hypothesis describes is resolved to one location
(shared/main), the worktree-parent `done` path works from its own cwd with no copying
or `cd`, and the main non-branch path is byte-for-byte the behavior it had. Evidence:
this experiment (cited) confirms both test halves green in the tree.
<!-- BODY:END -->

## Agent Notes
Verified L3.39 sibling fix already landed: session state SHARED (main-only) via shared_project_root; red-first worktree-done test and main done tests both green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9ebccd6a, L3.42): accepted proved. The node is a verification turn, not a diff turn — the fix landed at L3.39 (sibling a00-ac16be1a) and is already on this branch cut point, so an empty code diff is correct here, not the BUILD failure the brief warns about: the artefact is the green test evidence, both halves (worktree-cwd done resolves the MAIN shared record; main non-branch path unchanged, 14 tests green). Frontmatter clean: parents resolves, evidence_runs is a node list, verdict form valid. No demotion.
<!-- THOUGHT:END -->
