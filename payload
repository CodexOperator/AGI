---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Commit-Message Style Conventions

Captured for cavekit-git-remote R6 (commits on the unified repo should match observable conventions). Source: last 10 commits from each origin repo.

## `~/.hermes/agi/` (master) — destination repo

Style: descriptive freeform, often metric-oriented or iter-tagged. No fixed prefix. Sentence case. May include parenthetical metrics.

Examples:
- `Prune ideas.md: mark hooks/scripts/ASCII done, update current best to iter 47 (1665 nodes, 1700 edges, 72 lines)`
- `ASCII renderer now shows hook_reference/script_reference/pipeline nodes (+17 lines). Added build_script_bridges(): script→pipeline cross-type edges (+55 edges). Primary stays at noise floor 0.04ms. Graph richer AND better visualized.`
- `Parse hooks/ (3 hooks) + scripts/ (~40 Python CLI tools with function/class children): +235 nodes, +184 edges. Primary metric unchanged at 0.03ms noise floor. lru_cache warm load absorbs additional parsing overhead entirely.`
- `iter-44: parse_templates creates template_stage nodes with rich YAML metadata`
- `Pre-compute hub reachability matrix: O(1) reachability queries`
- `docs: mark pipelines/templates done, update current best node count to 1430`

Patterns observed:
- Often leads with a verb or noun phrase describing the change
- Rich body lines with metrics, file references, performance notes
- Occasional `iter-NN:` or `docs:` prefix but not required
- Multiple sentences acceptable, periods used

## `~/autoresearch-tree/` — origin being folded in

Style: type-prefixed conventional-commits-like (`type(scope): subject`). Lowercase prefixes. Imperative.

Examples:
- `feat(bridge): add autoresearch-tree-bridge pi extension — refreshes INJECTION.md per agent turn during autoresearch-create loops`
- `engine: scaffold+verdict pipeline — driver pre-creates node skeletons, agents fill body, cli.py done updates verdict`
- `agent-prompt: add 'web not cathedral' philosophy — one small node per iteration, linking is the work`
- `engine: scrub ANTHROPIC_*/CLAUDE_CODE_* env vars before spawning pi (was leaking CC subscription quota)`
- `engine: fix metrics emitter to import graph_core from PLUGIN_ROOT/src not PROJECT_ROOT/src`
- `skill: add tmux/detached launch patterns + monitoring section + iter numbering caveat`
- `initial: autoresearch-tree plugin (engine + skill + hooks)`

Prefixes seen: `feat(scope):`, `engine:`, `agent-prompt:`, `skill:`, `initial:`.

## Recommendation for the unified repo

Since the canonical destination is `~/.hermes/agi/`, the unified history follows agi's freeform descriptive style. Commits introduced by the fold may carry an explicit prefix to make folded work locatable in `git log`:

- `fold:` prefix for commits that perform the autoresearch-tree → agi merge, file moves, and renames (e.g., `fold: move engine bin/ into extensions/agi/bin/`).
- Subsequent post-fold work returns to agi's freeform style.

The subtree merge itself (T-007) preserves the original conventional-commits-style messages from autoresearch-tree's history — those stay verbatim in the merged history.
