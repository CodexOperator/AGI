---
id: hypothesis:a01-cca92e41-6de594
mint_id: d23110a3ce364e508f464f921d06179c
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.5
edited_by: season.py
scaffold_hash: 7971d24d53872220
season: 1
thought_session: season
title: A01 cca92e41 6de594
verdict: pending
---
# hypothesis:a01-cca92e41-6de594

## Hypothesis

**Claim:** shape 1 (drop-in clone) is sufficient as the sole distribution
shape for the engine. The pi integration layer (skill symlink, CLI symlink,
SessionStart hook) that the hybrid-split sibling
(`hypothesis:a00-001de563-9bd20a`) proposes to ship as a separate installable
package can instead be auto-provisioned from within the clone itself — a
self-registering `agi install` script inside the repo that sets up the two
symlinks and one hook entry. This eliminates the need for any package format
(skill or pip) to carry the integration layer.

**Why this matters:** `goal:g8.1` poses the three candidate shapes as mutually
exclusive and asks which one the engine should *be*. The hybrid-split sibling
answers "both: clone for engine code, package for integration" — which
doubles the delivery surface (two artifacts to maintain, two install paths).
If shape 1 can absorb the integration layer, the answer to g8.1's question is
simpler: shape 1 alone, with the package format adding nothing that an
install script inside the clone cannot do.

**What the integration layer actually is (from the engine's own tree):**

1. **Skill symlink:** `~/.claude/skills/agi → <engine>/skills/agi/SKILL.md`
   — a single symlink, set by `hooks/cc-session-start.sh`.
2. **CLI symlink:** `~/.local/bin/agi → <engine>/extensions/agi/driver.sh`
   — a single symlink, also set by the same hook.
3. **SessionStart hook:** one JSON entry in
   `~/.claude/settings.json` pointing at
   `<engine>/extensions/agi/hooks/cc-session-start.sh` — injected by
   `driver.sh --install` or `QUICKSTART.md` setup instructions.

All three are symlinks and a JSON key — none of them is a pip-installable
Python package, a skill package with dependencies, or anything a package
format buys. They are simple registration operations that any `install.sh`
inside the clone can perform.

**What would prove it:** a minimal `agi install` script (or a shell target in
`driver.sh` that is called once after cloning) registers the two symlinks and
the hook, and subsequently any project with a cloned engine resolves the
skill and the `agi` command exactly as it does today under the hybrid system.
Verifier: a fresh clone of the engine into a clean project, run `agi install`,
then `driver.sh --smoke` from inside that project resolves the skill and runs
without error. The verification is that no package installation step (`pi
install`, `npm install`, `uv tool install`) is needed — the clone's own
install step is sufficient.

**What would disprove it:**

1. **The symlinks or hook require a package manager to set up.** If
   registration depends on `pi` or `npm` CLI commands (e.g., `pi install`
   does something the symlinks cannot replicate), then the integration layer
   genuinely needs a package format. Counter-argument: `QUICKSTART.md`
   already documents the symlink setup as `ln -sf` commands, and
   `cc-session-start.sh` already sets up `~/.claude/skills/agi` from inside
   the clone — so the hook is already self-provisioning. If this works today,
   there is no package requirement.

2. **A pi skill package offers version pinning that the clone cannot match.**
   This is the core of the hybrid-split's argument: the package's version
   spec (`pi install user/agi@v1.2`) pins the integration layer, while the
   symlink always points at whatever HEAD is. Counter-argument: the engine
   version IS the integration layer version — they are one artifact (one
   commit). Pinning the engine commit (the L9 gap mechanism the siblings
   under this goal already explore) pins the integration layer as a free
   side effect. No separate package pinning is needed.

3. **The integration layer needs package-level features** — dependency
   declaration, post-install hooks, published versions on a registry. If
   a future requirement makes these necessary and the clone's install script
   cannot provide them (e.g., a Python dependency the integration layer has
   that the engine code does not), shape 1 would need the package format.
   Counter-argument: as of today, the integration layer has zero dependencies
   beyond what the engine clone already carries — it is `SKILL.md` text +
   shell hooks + symlinks. If it grows a dependency, that dependency is
   on the engine code, which the clone already provides.

**Why this is distinct from every living hypothesis under g8.1:**

- **Hybrid-split** (`a00-001de563`, pending): assumes the package IS needed
  for the integration layer. This hypothesis tests whether that assumption
  is false, which would convert the hybrid into shape-1-only.
- **L9 pinning gap** (`a00-23fc51e6`, `a00-4d063889`, `a01-0c63908f`): all
  three address the pinning sub-problem while assuming shape 1 as given.
  This hypothesis addresses shape 1's SUFFICIENCY, not a sub-problem within
  it — a different layer of the analysis.
- **Shape 2 not viable** (`a00-bad7df6a`, pending; experiment `a00-1215e67e`,
  leaning disproved 65): tests whether skill packages can hold the FULL
  engine. This hypothesis tests the opposite — whether the engine does not
  need a package at ALL, not even for the integration layer alone.
- **Shape 3 breaks forkability** (`a00-7e85b581`, pending): tests pip/uv
  install. This hypothesis is closer to "shape 1 or nothing" than to any of
  the shapes that need a packaging step.
- **Empty scaffolds** (`a00-2bf7847c`, `a01-abd43b16`, `a01-c70bfcf6`,
  `a01-e3478ffd`): no content to conflict with.

**Cost of being wrong:** If the integration layer does need a package (e.g.,
a future pi feature gate, or a registry requirement that symlinks cannot
satisfy), the answer to g8.1 shifts toward the hybrid-split or toward shape 2
for the integration half. But being wrong on this hypothesis still narrows
g8.1's outcome space from three contenders to two (clone vs. clone+package),
which is progress on the shape decision regardless.

<!-- THOUGHT:BEGIN -->
First version — fills scaffolded node a01-cca92e41-6de594 under goal:g8.1.
Tests a claim no sibling covers: whether shape 1 (drop-in clone) alone is
sufficient, by verifying the pi integration layer can be auto-provisioned
from within the clone rather than requiring a separate package format.
Distinct from the hybrid-split sibling which assumes a package is needed
for integration; from the L9 pinning siblings which assume shape 1 but
only address drift detection; and from the shape-2/shape-3 siblings which
test alternative shapes. No experiment run yet — verdict is pending.
<!-- THOUGHT:END -->

## Agent Notes
Shape 1 sufficiency hypothesis: tests whether drop-in clone alone can absorb the pi integration layer via self-registration, eliminating need for separate package format. No experiment run; distinct from all 11 siblings under g8.1.