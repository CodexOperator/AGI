---
id: hypothesis:a00-7e85b581-3a07f5
mint_id: 4c891b93952a4d0389e74078453286e3
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.5
scaffold_hash: ccfdd3edb65f9db3
title: A00 7e85b581 3a07f5
verdict: pending
---
# hypothesis:a00-7e85b581-3a07f5

## Hypothesis

**Claim:** Shape 3 (real install via `pip install agi-engine` / `uv tool install agi-engine`) is incompatible with forkability (g8) because a machine-global install conflicts with per-project engine ownership.

**Why this matters:** `goal:g8.1` lists three candidate distribution shapes — drop-in clone (today), skill package, and real install — and says nothing about which is viable. Siblings under this goal cover the L9 pinning gap (3 variants, two leaning proved), a hybrid-split proposal (engine=clone, integration=package, pending), and shape-2 (skill package) unviability (pending). **Shape 3 is the only candidate no sibling has examined.**

**Structural problem:** The engine design is built on three invariants that a pip/uv install breaks:

1. **`level3.py` reads `git ls-files`** on the engine tree to discover node-generating files. A pip install drops files into `site-packages/` as a flat directory, not a git checkout — `git ls-files` fails with `fatal: not a git repository`, crashing every discovery path.
2. **`lib/find-root.sh` resolves the project root** by walking up for `.agi/config.json`. A pip install places the engine scripts inside `site-packages/agi-engine/lib/find-root.sh`, which does *not* have a `.agi/` above it (the engine's own `.agi/` is at the repo root, not site-packages), so resolution returns a wrong or missing root.
3. **Per-project version independence** — forkability (g8) requires each project to own its engine version. A machine-global install serves one version to all projects on the machine (even with venvs, reinstallation per project is operationally identical to a clone but with extra overhead).

**What would prove it:** Run `uv tool install` of a packaged engine into a clean project. The smoke run fails on any of the three invariants above — `git ls-files` crash, wrong project root, or inability to run per-project engine versions. Any one failure proves shape 3 breaks forkability.

**What would disprove it:** A project successfully installs the engine via pip/uv, and `driver.sh --smoke` works without special adaptation — meaning `level3.py` discovers nodes from the project's `.agi/` (not the engine's site-packages dir), `find-root.sh` resolves to the project root (not the installed path), and two projects on the same machine can independently pin different engine versions via normal pip/uv mechanisms. If shape 3 works naturally, the forkability concern was wrong.

**Why this is distinct from siblings:**

- The L9 pinning-gap hypotheses (`a00-23fc51e6`, `a00-4d063889`, `a01-0c63908f`) assume clone-shape and touch only the drift-check problem. Shape 3's pinning story (pip/uv version ranges) is a *different* approach that does not need a custom config field — it uses the package manager's own version resolution. But if shape 3 breaks on the invariants above, the pinning mechanism is moot regardless.
- The hybrid-split hypothesis (`a00-001de563`) proposes a two-layer answer (engine=clone, integration=package) without testing whether pure shape 3 would work or what it would break. This hypothesis tests shape 3 standalone, which is a necessary precondition for the hybrid to know whether "engine=clone" is a deliberate choice or a forced constraint.
- The shape-2 hypothesis (`a00-bad7df6a`) tests skill-package viability, not pip/uv install viability. The two are different packaging formats with different constraints — skill packages are per-agent integrations, pip packages are full tool distributions — so testing one does not answer the other.

**Cost of being wrong:** If shape 3 works after minor adaptation (e.g. `level3.py` can fall back to reading the filesystem when not in a git checkout, or `find-root.sh` accepts a discovered install path), then the answer to g8.1's question is clearer: the engine can ship as a real install, dropping the clone cost without losing forkability.

## Agent Notes
Shape 3 (real install via pip/uv) hypothesis under g8.1: claims pip/uv install breaks forkability via three invariants (git-ls-files in level3.py, find-root.sh resolution, per-project version independence). Distinct from all 8 siblings — none examine shape 3. No experiment run; verdict pending.
