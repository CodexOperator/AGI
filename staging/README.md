# autoresearch-tree

Capillary DAG memory for fast LLM agent onboarding. A pi extension + skill that:

- Auto-injects an ASCII map of any project's research graph into every Claude Code session (SessionStart hook)
- Runs parallel pi subagents to extend the graph (idea → hypothesis → experiment → verdict → MVP → outcome → app_purpose)
- Provides a finite-state verdict taxonomy and longest-chain attractor for chain selection

## Install

```bash
pi install git:github.com/CodexOperator/autoresearch-tree
```

This registers the extension and skill via pi's standard `package.json` discovery (`pi.extensions` + `pi.skills`).

You can also install locally for development:

```bash
git clone https://github.com/CodexOperator/autoresearch-tree ~/autoresearch-tree
ln -sf ~/autoresearch-tree/extensions/autoresearch-tree/driver.sh ~/.local/bin/autoresearch-tree
```

## Use

In any project, drop an `autoresearch-tree.config.json` at the root. That marker turns the directory into an autoresearch-tree project. Then:

```bash
cd /path/to/project
autoresearch-tree --max-iters 5 --delay-mins 2
```

A new Claude Code session opened anywhere inside the project will receive an auto-injected ASCII map of the graph (top 80 lines of `context/INJECTION.md`).

## Two repos, two purposes

- **This repo** (`autoresearch-tree`): the engine. Graph core, renderers, embeddings, schema registry, driver, dispatch, heal, snapshot, render, the SessionStart hook, and the SKILL.md spec. Improvements to the method land here.
- **Your project repo**: the data. Nodes, kits, schemas, experiments, MVPs, verdicts, and any domain-specific `src/` modules your research produces.

Builder agents are told (`lib/agent-prompt.md`) to commit research output to the project and engine improvements to the plugin. The split is what makes the visualization+injection method portable: anyone who installs `autoresearch-tree` gets the same machinery, and engine improvements flow back through this repo.

## Layout

```
autoresearch-tree/
├── package.json                   ← pi.extensions + pi.skills declarations
├── extensions/autoresearch-tree/
│   ├── driver.sh                  ← orchestrator (max-iters, delay, smoke, no-heal)
│   ├── bin/
│   │   ├── snapshot-build-site.py ← build-site.md → nodes/<type>/<id>.md
│   │   ├── render-context.py      ← nodes/ → context/INJECTION.md (ASCII map)
│   │   ├── dispatch.py            ← spawn N parallel pi subagents per iter
│   │   ├── heal.py                ← timeout/kill hung agents, spawn healer
│   │   ├── zoom.py                ← BIG vs SMALL zoom context builder
│   │   └── cli.py                 ← agent done/status CLI
│   ├── lib/
│   │   ├── find-root.sh           ← walk-up project root detection
│   │   └── agent-prompt.md        ← shared rules for builder agents
│   ├── hooks/
│   │   └── cc-session-start.sh    ← Claude Code SessionStart auto-injection
│   ├── src/
│   │   ├── graph_core/            ← nodes, edges, graph, loader
│   │   ├── renderers/             ← ASCII, Mermaid, git-tree, git-diff
│   │   ├── embeddings/            ← Node2Vec + UMAP + similarity
│   │   └── schema_registry/       ← bracketed schema parsing + validation
│   └── tests/                     ← pytest suite for engine modules
└── skills/autoresearch-tree/
    └── SKILL.md                   ← skill manifest pi loads
```

## Project markers and config

A project becomes autoresearch-tree-aware via a single file at its root:

```json
{
  "agent_dispatch": {
    "claude_max_parallel": 5,
    "max_turns": 30
  },
  "agent_timeout_mins": 10,
  "delay_mins": 0,
  "max_iters": 1,
  "big_idea_vs_small_idea_split": 0.3
}
```

The driver auto-detects the root by walking up from `$PWD` until it finds `autoresearch-tree.config.json`.

Project-local script overrides are honored: if `<project>/bin/snapshot-build-site.py` exists it runs instead of the plugin's copy. This lets a project customize snapshotting without forking the plugin.

## How injection works

1. `SessionStart` hook runs when CC starts inside the project tree.
2. If `context/INJECTION.md` is older than 1 hour, the hook re-renders it using the plugin's `snapshot-build-site.py` + `render-context.py`.
3. First 80 lines of `INJECTION.md` go to stdout → CC injects as `additional_context`.
4. Outside any autoresearch-tree project the hook is a silent no-op.

`AUTORESEARCH_TREE_PROJECT_ROOT` env var overrides cwd-based detection if you need to drive it programmatically.

## Verdict taxonomy

Finite-state, no free-form strings:

```
proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
```

Plus `confidence: 0..1`, `evidence_runs`, `contradicts`, `supports`.

## Status

Early. The engine (graph + renderers + dispatch + heal) is functional and tested. Plugin discovery via `pi install` is unverified — the patterns it follows are the same ones pi-autoresearch's own extensions use, so it should work out of the box.

Pull requests welcome — particularly for new renderers, new schema types, or alternative attractor scoring functions.
