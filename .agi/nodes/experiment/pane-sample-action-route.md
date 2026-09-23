---
id: experiment:pane-sample-action-route
mint_id: fc9f1f69a65d436a832f568aa7c26662
type: experiment
parents:
  - hypothesis:a00-6f624b44-35fcfb
next_edges: []
edited_by: a00-6f624b44
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e5249def5ca1b012
season: 2
title: Sample write send dispatch workflow through the four named CLIs
town: core
---
<!-- BODY:BEGIN -->
# experiment:pane-sample-action-route

## Experiment

Runnable proof: `extensions/agi/tests/test_pane_sample_action_route.py` (new,
test-only, 0 production lines). It invokes the four named entry points under
`extensions/agi/bin/` as REAL subprocesses against a scratch tmp project
(`cwd=` the scratch, env scrubbed of every `AGI_*`/`PROJECT_ROOT` re-root), so
nothing touches this worktree's live `.agi/`.

Run:

    python3 -m pytest extensions/agi/tests/test_pane_sample_action_route.py -q
    ....                                                                     [100%]
    4 passed in 124.05s (0:02:04)

The same four commands, run verbatim against the same scratch fixture
(`/tmp/a00-sample-route-probe/sampleproj`), with their real output tails:

### (a) write.py — `extensions/agi/bin/write.py`

    cd /tmp/a00-sample-route-probe/sampleproj
    python3 extensions/agi/bin/write.py hypothesis:sample-route \
      'set title route sample lands through write.py' \
      --root /tmp/a00-sample-route-probe/sampleproj --actor a00-sample

    updated: hypothesis:sample-route

node file after (real):

    ---
    id: hypothesis:sample-route
    mint_id: cafebabe00000000000000000000abcd
    type: hypothesis
    edited_by: a00-sample
    scaffold_hash: deadbeef
    status: pending
    testable_claim: c
    title: route sample lands through write.py
    ---
    the sample body

The write CHANGED the file and recorded `edited_by` — the assertion is on
the observable effect, not returncode 0.

### (b) send.py — `extensions/agi/bin/send.py`

    python3 extensions/agi/bin/send.py send sample-parent \
      'sample body with no backticks or shell metacharacters' --from a00-sample

    /tmp/a00-sample-route-probe/sampleproj/.agi/sessions/inbox/sample-parent.md

inbox block (real tail):

    ---
    ts: 2026-09-23T08:11:52.836616+00:00
    from: a00-sample
    to: sample-parent

    sample body with no backticks or shell metacharacters

The body is ONE plain argv token (no backticks, no shell metacharacters) —
the argv-safe case the L4 message ruling allows. The block lands under the
SCRATCH project's `.agi/sessions/inbox/`, `from:` recorded.

### (c) dispatch.py — `extensions/agi/bin/dispatch.py`

    python3 extensions/agi/bin/dispatch.py \
      /tmp/a00-sample-route-probe/sampleproj 1 \
      --tier kid --target hypothesis:sample-route --harness pi --dry-run

real tail:

    roles: tier=0 role=kid -> pi/~deepseek/deepseek-v4-flash-latest/effort=-/thinking=-/settings=-
    season: ladder current_season=2
    aimed: 1 slot(s) at hypothesis:sample-route (level=small, strategy=extend_existing)
    [dry-run] slot=0 harness=pi tier=kid role=kid ladder_tier=0 level=small target=hypothesis:sample-route brief_tier=kid
      command: /usr/bin/python3 .../extensions/agi/bin/pi_trajectory.py --wrapper /home/ubuntu/.npm-global/bin/pi ... --provider openrouter --model '~deepseek/deepseek-v4-flash-latest' -p --mode json --append-system-prompt ...
      env: AGI_TIER=kid AGI_ROLE=kid AGI_LADDER_TIER=0 AGI_SEASON=2 AGI_LOOP=hypothesis:sample-route@s2 AGI_MODEL=~deepseek/deepseek-v4-flash-latest ... GIT_CONFIG_COUNT=1 CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1
      brief: tier=kid 63 lines; first 20:
    dry-run: nothing spawned, nothing written, no budget slot taken

`--dry-run` is the ONLY safe way to exercise the dispatch CLI in a sample: it
resolves every slot (target, tier, model, env, brief) and mints/spawns
nothing. A live `dispatch.py` spawns a paid agent.

### (d) workflow.py — `extensions/agi/bin/workflow.py`

    python3 extensions/agi/bin/workflow.py run review --harness pi --dry-run

real output (whole):

    [run-key] review
    [credential] inherited env (provisioning unavailable)
    [dispatch] global-checks :: role=global model=~deepseek/deepseek-v4-flash-latest effort=low
    [dispatch] review :: role=reviewer model=~deepseek/deepseek-v4-flash-latest effort=low
    [summary] workflow=review harness=pi stages=2 via dispatch.py kids

ONE workflow router (`workflow.py run`, `goal:g1.14`). No sixth route, no
parallel workflow invoker, no engine edit. The routers stay two, each with
its `--dry-run`.

## Evidence

- Test file: `extensions/agi/tests/test_pane_sample_action_route.py`.
- Scratch fixture: `sample_project` — `.agi/config.json`, ladder rows,
  `nodes/hypothesis/sample-route.md`, plus a symlink
  `extensions/agi/workflows -> <engine>/extensions/agi/workflows` so the ONE
  router's manifest resolves while every write stays in the scratch project.
- Isolation: every subprocess uses `cwd=sample_project` and `_child_env()`
  strips all `AGI_*` / `PROJECT_ROOT` keys, so the scratch graph is what
  resolves — never this worktree's live `.agi/`.
- Workflow note: the experiment node's schema (`[experiment].md`
  `allowed_parents`) refuses a `goal` parent, so it is parented to
  `hypothesis:a00-6f624b44-35fcfb`, which is itself under
  `goal:g7.31.3.2` — the chain is intact.
- Production lines: 0. `git diff --numstat` over tracked production paths is
  empty; the only new file is the test (test files are not production).

## THOUGHT

The sample is a test, not a script: the falsifier's word is "named CLIs, not a
parallel script", and the cheapest honest proof is a test that IS the sample
run shebanged into the suite. `--dry-run` covers both routers because a live
sample would spend money and neither router's live path is what the falsifier
names. The workflow symlink is a fixture convenience, not a route: it exists
because `_repo_root` discovers the registry by walking up from the project,
and a non-git tmp project has no engine above it.
