---
id: hypothesis:a00-39a02539-a46255
mint_id: 397b46fb92874f419467cc92f45c8f09
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.5
edited_by: season.py
scaffold_hash: c8a832c3c6c6d0a3
season: 1
thought_session: season
title: A00 39a02539 a46255
verdict: pending
---
# hypothesis:a00-39a02539-a46255

## Hypothesis

**Claim:** The three candidate distribution shapes in `goal:g8.1` (drop-in clone, skill package, real install) and the `bin/` directory retirement in `goal:s1` are **causally linked in both directions** — each shape enforces a different obligation on the entry-point layout, and conversely the entry-point layout (whether bin/ stays or is renamed) constrains which shapes are even viable. They cannot be decided independently, and `g8.1`'s "related and load-bearing: S1" is not a loose coupling but a hard dependency: picking a shape *is* the bin/ rename decision.

**The linkage:**

| Shape | bin/ can stay | bin/ must move | What forces the move |
|---|---|---|---|
| 1. Drop-in clone | yes | no | Nothing. The engine is a git checkout; `extensions/agi/bin/` as a flat script dir works fine (it already does). S1's rename is optional without a packaging constraint. |
| 2. Skill package | no | yes | The pi skill format loads a single `SKILL.md` entry point, not a directory of 15 scripts. To provide all entry points within a skill package, they must live somewhere discoverable — `extensions/agi/scripts/`, `extensions/agi/entry/`, or be restructured so `level3.py` and `bin/locations.py` resolve them. A flat `bin/` inside a skill has no standard resolution path. |
| 3. Real install | no | yes | PyPI / `uv tool install` requires `[project.scripts]` or `[project.gui-scripts]` in `pyproject.toml` mapping named entry points to Python callables. A flat `bin/*.py` directory does not appear in the installed package's `PATH` — pip does not copy arbitrary script directories into `site-packages/bin/`. Each `.py` file must be registered as an entry point, which requires renaming or wrapping every one. |

**If shape 1 is chosen → S1's rename is optional, and g8.1 and S1 are independent concerns.** The engine can stay a clone forever, bin/ stays as-is, and S1 only matters if GitNexus coverage of the engine's codebase is deemed worth the churn.

**If shape 2 or 3 is chosen → S1's rename is forced, and g8.1 and S1 are a joint decision.** Picking a non-clone shape before renaming bin/ means the packaging work has to invent a structurally different layout — effectively renaming bin/ during the packaging pass, which is more expensive than doing it deliberately as S1 proposes.

**What would prove it:** A concrete structural audit of each shape's entry-point requirements against the current `bin/` layout:

- **Shape 1 verifier:** `driver.sh --smoke` works unchanged. `git ls-files extensions/agi/bin/` returns 15 scripts; `level3.py` reads them fine. GitNexus indexing not required for the shape to function. No packaging work needed.
- **Shape 2 verifier:** Building a skill package from `skills/agi/` that discovers all 15 `bin/` scripts — either the skill package must duplicate the bin/ directory (bad, the sibling `a00-bad7df6a` already flags this), or restructure. If restructuring is needed to make the skill work, S1's rename is mandatory.
- **Shape 3 verifier:** Writing a minimal `pyproject.toml` that tries to include all 15 `bin/*.py` scripts as registered entry points. If `pyproject.toml` cannot accept `extensions/agi/bin/*.py` as-is (pip requires `package.module:function` format, not script paths), the rename is mandatory.

**What would disprove it:** Finding that a skill package (shape 2) or pip install (shape 3) can absorb the engine's current `bin/` layout without structural changes — e.g. a skill package imports `bin/*.py` files by relative path from its own `SKILL.md` entry point (possible because a skill is a directory tree, not a flat namespace), or a pip install uses `[tool.uv.scripts]` to point to `extensions/agi/bin/` as a script source dir without each file needing an entry-point declaration. If either shape absorbs the layout as-is, then the bin/ rename is a separate concern and g8.1's "related and load-bearing" note is simply a reminder rather than a dependency.

**Why this is distinct from all 10 sibling hypotheses under goal:g8.1:**

| Sibling | Focus | How this hypothesis differs |
|---|---|---|
| `a00-001de563` (hybrid split) | Engine=clone, integration=package as two layers | Does not examine the *entry-point layout dependency* of either layer on the other. Assumes clone keeps bin/, package gets its own entry points — doesn't test whether bin/ would need renaming for the package half. |
| `a00-23fc51e6`, `a00-4d063889`, `a01-0c63908f` (L9 pinning gap) | engine_commit field + drift check inside shape 1 | All stay within shape 1's clone assumption. None touch the bin/ rename question, which does not affect the pinning gap at all. |
| `a00-2bf7847c`, `a01-abd43b16`, `a01-c70bfcf6`, `a01-e3478ffd` | Empty scaffolds (budget errors) | No content to distinguish from. |
| `a00-bad7df6a` (shape 2 unviability) | Skill format cannot hold ~15 entry points + src/ + tests | Makes the skill-format claim but does not connect it to S1's rename — does not ask whether renaming bin/ would change the viability answer. |
| `a00-7e85b581` (shape 3 incompatibility) | Pip/uv install breaks three forkability invariants | Examines runtime invariants (git ls-files, root resolution, per-project versioning) but not the entry-point *packaging* requirement, which is a separate gate that must be passed before the runtime invariants even matter. |

This hypothesis uniquely bridges g8.1's shape question and S1's bin/ rename by testing the entry-point layout against each shape's packaging requirements, which no sibling has examined.

## Agent Notes
Bridges g8.1 shape decision and S1 bin/rename: each shape forces different obligations on entry-point layout (clone=optional, skill=forced, pip=forced) making them a joint decision not independent concerns. Testable via structural audit of each shape's packaging requirements against current bin/ layout. No experiment run.