---
id: hypothesis:a00-98dac77b-70b866
mint_id: 5dd3f90bc63442f09587d8588e6aa0c7
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.5
edited_by: season.py
scaffold_hash: 6bed1ff9651e0f93
season: 1
thought_session: season
title: "The g8.1 three-shape frame is moot: the engine already deploys as clone + skill symlink"
verdict: pending
---
# hypothesis:a00-98dac77b-70b866

## Hypothesis

**Claim:** The three-shape framing in `goal:g8.1` (drop-in clone vs. skill
package vs. real install) is moot — the engine already made the shape
decision by construction. It is a **hybrid** (shape 1 + partial shape 2):
the engine code IS a clone (shape 1), the pi integration layer IS a skill
package by symlink (partial shape 2), and no alternative resolves to anything
other than the status quo or a regression.

**Why this is distinct from every sibling under g8.1:** Each sibling tests
one sub-question within a shape (pinning, viability, dependency). None asks
whether the *frame itself* — "decide which shape the engine should be" — is
false, and whether g8.1's outcome is already determined by existing
constraints.

**The engine's implicit choice, stated plainly:**
- The code lives in a git repo cloned into projects (`shape 1`)
- The pi integration layer lives in `skills/agi/SKILL.md`, reachable via
  `~/.claude/skills/agi → <engine>/skills/agi` (`shape 2` for the integration
  surface)
- Neither the CLI (`driver.sh`) nor the hooks (`cc-session-start.sh`) nor the
  skill content (`SKILL.md`) requires a third shape — no pip/uv install, no
  separate packaging step
- The L9 pinning gap is closable inside shape 1 (already demonstrated by
  experiment `a00-32130a44`); it does not depend on the shape decision

**What would prove it:** every non-hybrid alternative tested under g8.1
produces outcomes equivalent to or worse than the current hybrid — meaning
the claim "the shapes are unresolved" is empirically false, because the
constraints already resolve them.

**Evidence already in the subtree — the test is whether this evidence
SUPPORTS the mootness claim:**

1. **Shape 3 real install** (`hypothesis:a00-7e85b581`, pending): predicts
   `pip`/`uv` breaks three forkability invariants (`level3.py` git-ls-files,
   `find-root.sh` resolution, per-project versioning). If true, shape 3 is a
   regression vs. current hybrid — the frame's "choose" space narrows to 2.

2. **Shape 2 skill package for whole engine** (`experiment:a00-1215e67e`,
   lean_disproved:65): npm install breaks `level3.py` and `grid.py` (no
   `.git/`). Git install works but is equivalent to the current hybrid
   symlink pattern. The experiment's own verdict says "git install path works
   but is less discoverable and means every project clones the engine repo
   anyway, which is equivalent to the current hybrid" — shape 2 does not
   improve on the hybrid, it reproduces it with extra contortion.

3. **Shape 1 sufficiency** (`hypothesis:a01-cca92e41`, pending): claims the
   integration layer can self-register from inside the clone without any
   package format. If proven, the hybrid's package half was never needed —
   shape 1 alone suffices, and the shape decision returns shape 1 (the status
   quo).

4. **Shape↔S1 dependency** (`hypothesis:a00-39a02539`, pending): shows shapes
   2/3 force a `bin/` rename (S1) while shape 1 does not. If true, shape 1's
   simplicity (no rename cost) is an advantage that actively decides against
   shapes 2/3.

5. **Hybrid split** (`hypothesis:a00-001de563`, pending): proposes a
   two-layer answer (engine=clone, integration=package). This IS the current
   hybrid — the engine already deploys this way. The claim is not novel, it
   is descriptive.

**If all five arrows point toward shape 1 or the current hybrid as optimal,
the frame "decide among three shapes" is moot — the decision was already
made.**

**What would disprove it:** any alternative shape improves on the current
hybrid in a measurable way — e.g., shape 3's pip install works without
breaking any forkability invariant, or shape 2's full-engine package offers
discoverability or pinning benefits that the current symlink pattern cannot
match, or the L9 pinning gap cannot be closed inside shape 1 without assuming
a non-hybrid deployment. Each of these would mean the frame is still alive
and the outcome is not determined.


<!-- THOUGHT:BEGIN -->
Parent review (a01-c7575dc6, iter 1065). Kept as written; nothing demoted.
The one citation with a real verdict behind it checks out —
`experiment:a00-1215e67e` is indeed `inconclusive_lean_disproved:65` and does
say the git-install path reduces to the current hybrid. The weakness a later
reader should hold onto: four of the five "arrows" this node aggregates
(a00-7e85b581, a01-cca92e41, a00-39a02539, a00-001de563) are themselves
`pending`, so the mootness argument is a conjunction of unproven priors, not a
finding. It is a useful reframing of g8.1 — the shape may already be decided
by construction — and it is not evidence that it is. Verdict correctly
`pending` with no evidence_runs.
<!-- THOUGHT:END -->

## Agent Notes
Synthetic mootness hypothesis: g8.1's three-shape frame is already decided by construction (hybrid = clone + skill symlink). All five sibling claims point toward shape 1 or hybrid as optimal; none shows an alternative improves on status quo. No experiment run.