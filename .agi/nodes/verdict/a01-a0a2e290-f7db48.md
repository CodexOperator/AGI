---
id: verdict:a01-a0a2e290-f7db48
mint_id: 57583a5345544e6a99e05a1782dbfe9e
type: verdict
parents:
  - experiment:a00-1215e67e-de106f
next_edges: []
confidence: 0.65
scaffold_hash: 1f98ba978a218de4
title: A01 a0a2e290 f7db48
verdict: inconclusive_lean_disproved:65
---
# verdict:a01-a0a2e290-f7db48

## Verdict

inconclusive_lean_disproved:65

## Evidence

Independent review confirms the experiment's structural analysis of shape-2 viability for the full engine:

1. **`level3.py` L307** calls `git -C <engine_root> ls-files` — fails without a `.git/` directory (npm install breaks this).
2. **`grid.py` L79** `REF_NS = "refs/grid"` — grid.py has 17+ git call sites and depends on `refs/grid/*` branches existing in the git repo. npm install loses all refs.
3. **`locations.py` L185 `find_project_root()`** walks up from cwd for `.agi/` — correct behavior per `goal:g8.2`, not a skill-format problem. Inside a package tree the engine's own `.agi/` resolves only when cwd is inside the package.
4. **Existing hybrid deployment** (symlinks from `~/.claude/skills/agi` and `~/.local/bin/agi` into cloned repo) is morally equivalent to a git-installed pi package.
5. **Pi package format** (docs/packages.md, docs/skills.md) supports git sources natively — `pi install git:github.com/...`.

The decisive constraint is git availability, not skill-format structural limits. Git-installed packages preserve every mechanism; npm packages break the engine's git-dependent discovery and versioning. The hypothesis claimed shape 2 is categorically NOT viable — this is too broad. Shape 2 via git IS viable; the npm path is the real blocker. This refines rather than fully disproves the claim.

**Weakness:** The experiment's Method promised two concrete test packages. They were not built. The analysis is strong structural evidence but not empirical. A single `pi install git:... && driver.sh --smoke` from the installed package would convert this to `proved`.

## Primary evidence node

- `experiment:a00-1215e67e-de106f` — the structural analysis and mechanism-by-mechanism evaluation

## Confidence

0.65


## Agent Notes
Independent concurrence: shape-2 is viable via git (preserves level3/grid); npm breaks git-dependent mechanisms. Hypothesis claim was too broad — refined to npm-vs-git split. Method's test packages not built; structural analysis only.
