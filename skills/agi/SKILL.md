---
name: autoresearch-tree
description: >
  Capillary DAG memory for fast LLM agent onboarding. Idea → Hypothesis →
  Experiment → Verdict → MVP → Outcome chains with longest-chain-wins,
  mid-chain join, free-form branching, and a finite-state verdict taxonomy.
  Auto-injects an ASCII map of the research graph into every Claude Code
  session via SessionStart hook. Use when the user says "run autoresearch-tree",
  "extend the graph", "spawn parallel research agents", or "show me the research map".
category: software-development
---

# autoresearch-tree

Capillary DAG memory layer that captures research-and-build trajectories as
`Idea → Hypothesis(+) → Experiment → Verdict → MVP → Outcome → Bigger Outcome → App Purpose`
chains. Optimized for fast LLM agent onboarding: longest-chain-wins surfacing,
mid-chain join, free-form branching, structured verdict taxonomy.

## Install

```bash
pi install git:github.com/CodexOperator/autoresearch-tree
```

Pi auto-discovers the extension and skill via the repo's `package.json`
(`pi.extensions` + `pi.skills`). After install:

- The shell CLI `autoresearch-tree` is available (via the plugin's `driver.sh`)
- The Claude Code SessionStart hook auto-injects the project's research map

For local development, clone and symlink the driver:

```bash
git clone https://github.com/CodexOperator/autoresearch-tree ~/autoresearch-tree
ln -sf ~/autoresearch-tree/extensions/autoresearch-tree/driver.sh ~/.local/bin/autoresearch-tree
```

## How to Run

### From outside pi (shell)

A symlink at `~/.local/bin/autoresearch-tree` points to the driver. Run from
**inside any project tree** that contains `autoresearch-tree.config.json`:

```bash
cd <project>
autoresearch-tree --max-iters 5 --delay-mins 2
```

The driver walks up from `$PWD` to find the project root, so deep cwds work.

Useful flags:
- `--max-iters N` — total iterations (default 1)
- `--delay-mins M` — sleep between iters (default 0)
- `--smoke` — dry pass: snapshot + render + METRICs, no agent dispatch
- `--no-heal` — disable timeout monitor (debug)

Override project root explicitly:

```bash
AUTORESEARCH_TREE_PROJECT_ROOT=/path/to/project autoresearch-tree --smoke
```

### Recommended: launch inside tmux

For multi-hour runs you want to monitor across sessions, launch the loop in
a detached tmux session and a sibling monitor session:

```bash
cd <project>
# Worker session — runs the actual loop. Detached (-d), no terminal needed.
tmux new-session -d -s autoresearch-tree \
  "autoresearch-tree --max-iters 25 --delay-mins 2 |& tee /tmp/autoresearch-tree.log"

# Optional monitor session — split log tail + sessions/git watcher.
tmux new-session -d -s autoresearch-monitor -x 220 -y 50 \
  "tail -f /tmp/autoresearch-tree.log"
tmux split-window -h -t autoresearch-monitor \
  "watch -n 5 'ls -t <project>/sessions/ | head -10; echo ---; cd <project> && git log --oneline | head -10'"
```

Attach to either from anywhere:

```bash
tmux attach -t autoresearch-tree    # see live driver output, Ctrl-B D to detach
tmux attach -t autoresearch-monitor # see split log+session+git view
```

This survives shell exit, supports re-attach from any future shell, and lets
you peek without disturbing the loop. The worker session itself is fully
disposable — kill it with `tmux kill-session -t autoresearch-tree` to stop
gracefully (heal.py will SIGTERM agents, then SIGKILL).

### Fully detached (no tmux, fire and forget)

If tmux is unavailable, use `setsid` + `nohup` so the loop survives any
shell exit:

```bash
cd <project>
setsid nohup bash -c \
  'autoresearch-tree --max-iters 25 --delay-mins 2 > /tmp/autoresearch-tree.log 2>&1' \
  </dev/null >/dev/null 2>&1 &
disown
```

Tradeoff: there's no PTY to attach to — only the log file and the per-agent
session dirs to watch. If you may want to interact with the run later, prefer
tmux.

### Monitoring a live run

The driver writes:

- **Loop log:** stdout/stderr — METRIC lines, spawn events, iter summaries
- **Per-iter manifest:** `<project>/sessions/iter-NNN/manifest.json` — agent
  ids, pids, status, verdicts
- **Per-agent log:** `<project>/sessions/iter-NNN/<agent_id>/output.log`
- **Per-agent state:** `<project>/sessions/iter-NNN/<agent_id>/agent.json`
  (status: running/done/failed, verdict, confidence)
- **Commits:** agents commit to project git when work is done — `git log` is
  the authoritative record of what was produced
- **Injection:** `<project>/context/INJECTION.md` re-rendered every iter

Useful one-liners:

```bash
# Live loop progress
tail -f /tmp/autoresearch-tree.log

# Iter status across the project
grep -E "iter [0-9]+: 5 agents|status=" /tmp/autoresearch-tree.log

# How far along
ls <project>/sessions/ | grep -E "^iter-[0-9]+$" | sort -V | tail -5

# Verdict tally for the latest iter
python3 -c "import json; m=json.load(open('<project>/sessions/iter-NNN/manifest.json')); \
  [print(f\"{a['id']}: {a['status']} verdict={a.get('verdict','-')}\") for a in m['agents']]"

# What the agents committed
cd <project> && git log --oneline -20

# Kill the run if needed
pkill -f "autoresearch-tree --max-iters"
# or, if launched in tmux:
tmux kill-session -t autoresearch-tree
```

### Iter numbering caveat

The driver always runs `iter-001` through `iter-N` regardless of prior state.
Re-running over an existing project clobbers the per-agent session dirs
(`sessions/iter-NNN/`), but the actual research output (verdicts, nodes,
commits) is preserved in `nodes/` and git. To preserve session logs across
re-runs, archive the prior `sessions/iter-NNN/` dirs first:

```bash
for d in <project>/sessions/iter-0*; do
  mv "$d" "${d}-prevrun-$(date +%s)"
done
```

A future driver flag (`--iter-base`) would lift this constraint.

### From inside pi (skill)

When this skill is loaded, the pi agent invokes the same CLI via Bash:

```bash
$ autoresearch-tree --max-iters 1
```

Pi agents acting as **builders** (spawned by `dispatch.py`) get a zoom-targeted
context and a completion-CLI instruction injected into their system prompt.
They do NOT call `autoresearch-tree` themselves — they do the work and signal
done via:

```bash
$ python3 "$PLUGIN_ROOT/bin/cli.py" done <iter_n> <agent_id> \
    --verdict <state> --confidence <0..1> \
    --node-id <id> --parent <parent_id> --notes "<one-line>"
```

`$PLUGIN_ROOT` is exported into the agent's environment by `dispatch.py`.

## Two repos, two purposes

- **Plugin repo** (`autoresearch-tree`): the engine. `graph_core`, `renderers`,
  `embeddings`, `schema_registry`, driver, dispatch, heal, snapshot, render,
  hooks, this SKILL.md, and `lib/agent-prompt.md`. Engine improvements land here.
- **Project repo** (whatever you're researching): the data. Nodes, kits,
  schemas, experiments, MVPs, verdicts, and any domain-specific `src/` modules
  your research produces.

Builder agents (`lib/agent-prompt.md` rule #11) are told to commit research
output to the project and engine improvements to the plugin. The split is
what makes the visualization+injection method portable.

## Verdict Taxonomy (finite-state)

```
proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
```

N is integer 0..100. Plus per-verdict: `confidence` (0..1), `evidence_runs`,
`contradicts`, `supports`.

## Project Layout

The driver works in any directory tree shaped like:

```
<project>/
├── autoresearch-tree.config.json   # root marker + config
├── context/
│   ├── INJECTION.md                # auto-rendered each iter (≤200-line ASCII)
│   ├── schemas/[*].md              # bracketed-active node-type schemas
│   ├── kits/                       # cavekit specs (optional)
│   └── plans/build-site.md         # task graph (optional, used by snapshot)
├── nodes/                          # auto-generated frontmatter node files
└── sessions/iter-NNN/<agent>/      # per-agent run state + logs
```

Optional project-local script overrides (`<project>/bin/snapshot-build-site.py`,
`<project>/bin/render-context.py`) take precedence over the plugin's copies if
present — useful for project-specific snapshotting logic without forking the
plugin.

To bootstrap a new project: drop `autoresearch-tree.config.json` at the root.
Everything else is created on first run.

## Iteration Anatomy

1. `bin/snapshot-build-site.py` rebuilds `nodes/` from `context/plans/build-site.md`
   (skipped if no build-site present)
2. `bin/render-context.py` re-renders `context/INJECTION.md` (≤200-line ASCII)
3. METRIC lines emitted (`longest_chain_length`, `mvp_count`, `outcome_coverage`,
   `chain_branching_factor`, `node_count`, `edge_count`, `avg_chain_depth`)
4. `dispatch.py` spawns up to `agent_dispatch.claude_max_parallel` pi subprocesses:
   - Slot 0 → BIG zoom (whole graph)
   - Slot 1+ → SMALL zoom (top-attractor subtree, 2-hop bound)
5. `heal.py` polls every 30s; agents past `agent_timeout_mins` get killed +
   replaced with a healer subagent that diagnoses and patches
6. Agents signal completion via `cli.py done` → writes verdict node +
   marks `agent.json` `status=done`

## Big-Idea-vs-Small-Idea

Each iteration's first agent always explores BIG (broad context, fresh chain
or top-level fork). Remaining agents go SMALL (target = top attractor by
descendant count). Ratio configurable via `big_idea_vs_small_idea_split` in
`autoresearch-tree.config.json`.

## Auto-Injection (Claude Code SessionStart)

On every CC session start inside a project tree:

1. `hooks/cc-session-start.sh` walks up from `$PWD` to find `autoresearch-tree.config.json`
2. If `context/INJECTION.md` is older than 1 hour, re-renders silently
3. First 80 lines of `INJECTION.md` go to stdout → CC injects as `additional_context`
4. Outside any autoresearch-tree project the hook is a silent no-op

To register the hook globally, add to `~/.claude/settings.json` under
`hooks.SessionStart`:

```json
{
  "type": "command",
  "command": "/path/to/autoresearch-tree/extensions/autoresearch-tree/hooks/cc-session-start.sh",
  "timeout": 15,
  "statusMessage": "Building autoresearch-tree map..."
}
```

## Healing

If an agent's pid is alive but `status=running` past timeout, heal.py:
1. SIGTERM (2s grace) → SIGKILL the original
2. Spawn a HEALER pi subagent with the last 4 KiB of the original's log +
   diagnose-and-patch instruction
3. Healer commits a small fix and signals `pending` for the original agent_id
4. If pid is gone w/o completion → mark `failed` (no healer for ghost pids)

## Configuration

`autoresearch-tree.config.json` at project root:

```json
{
  "agent_dispatch": {
    "claude_max_parallel": 5
  },
  "agent_timeout_mins": 10,
  "delay_mins": 0,
  "max_iters": 1,
  "big_idea_vs_small_idea_split": 0.3,
  "metric_primary": "longest_chain_length",
  "metric_unit": "hops",
  "best_direction": "higher",
  "secondary_metrics": [
    "avg_chain_depth", "mvp_count", "outcome_coverage",
    "chain_branching_factor"
  ]
}
```

Pi uses its own default agent (`~/.pi/agent/settings.json`) — typically
`minimax/MiniMax-M2.7`. Provider/model are NOT overridden by the driver.

## See Also

- Plugin repo: https://github.com/CodexOperator/autoresearch-tree
- Cavekit (project spec): `<project>/context/kits/cavekit-autoresearch-tree-skill.md`
- Build site (task graph): `<project>/context/plans/build-site.md`
- Predecessor (frozen at iter 47): `~/.hermes/agi/`
- Sibling skills: `pi-autoresearch`, `autoresearch-create`, `autoresearch-finalize`
