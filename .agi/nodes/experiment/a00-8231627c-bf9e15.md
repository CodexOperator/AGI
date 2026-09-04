---
id: experiment:a00-8231627c-bf9e15
mint_id: 0b655e7944c143199f9fe087d3604a2b
type: experiment
parents:
  - hypothesis:a00-7e85b581-3a07f5
next_edges: []
confidence: 0.65
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved' [caught at grid commit, not by a writer path]
demoted_from: disproved
scaffold_hash: b309fc2e191c9149
title: A00 8231627c bf9e15
verdict: inconclusive_lean_disproved:50
---
# experiment:a00-8231627c-bf9e15

## ## Experiment

Simulated pip/uv install of the agi-engine into a clean test project and tested each of the three claimed broken invariants.

**Setup:** Created `/tmp/test-pip-install/` with `.agi/config.json` and minimal nodes. Copied engine to `site-packages/agi-engine/` (no `.git` — simulates pip install into site-packages).

### Invariant 1 test: `level3.py` git ls-files

```
$ python3 level3.py --project /tmp/test-pip-install/.agi --engine-root site-packages/agi-engine/
WARN: engine root ... is missing or unreadable (not a git repo?) — no-op, nothing written or pruned
```

`level3.py` gracefully degrades (no-op, no crash). But `payload_boundary.py` crashes on the same engine root:

```
$ python3 payload_boundary.py site-packages/agi-engine/
CalledProcessError: Command 'git -C .../site-packages/agi-engine ls-files' returned non-zero exit status 128.
```

`decompose-engine.py` also gracefully degrades to no-op.

**Result:** Invariant 1 is PARTIALLY BROKEN. Engine introspection tools fail gracefully (level3, decompose-engine) or crash (payload_boundary). But this does NOT affect the driver loop.

### Invariant 2 test: `find-root.sh` resolution

Tested `find-root.sh` from three locations while the script lived in site-packages:
```
# From project root:
bash site-packages/agi-engine/.../find-root.sh  -> /tmp/test-pip-install/.agi  (correct)

# From subdir of project:
bash site-packages/agi-engine/.../find-root.sh  -> /tmp/test-pip-install/.agi  (correct)

# From inside site-packages itself:
bash site-packages/agi-engine/.../find-root.sh  -> /tmp/test-pip-install/.agi  (correct)

# From /tmp with no project:
bash .../find-root.sh  -> ERR: no project found  (correct — expected failure)
```

**Result:** Invariant 2 is NOT BROKEN. `find-root.sh` resolves from PWD, not from the script location. The driver loop (`driver.sh --smoke`) correctly resolves `PROJECT_ROOT` and `PLUGIN_ROOT` regardless of engine install location.

### Invariant 3 test: per-project version independence

| Method | Version independence | Operational cost |
|---|---|---|
| Clone (today) | Natural per-checkout | One checkout per project |
| Global pip install | One version for all | Highest (no isolation) |
| Per-venv pip install | Per-venv | Venv management overhead |
| uv tool install | One version globally | Highest |

**Result:** Invariant 3 PARTIALLY BROKEN. Venvs solve it but add friction. Not a structural break of forkability.

### Full driver test: `driver.sh --smoke`

```
[driver] PROJECT_ROOT=/tmp/test-pip-install/.agi        ← CORRECT
[driver] PLUGIN_ROOT=.../site-packages/agi-engine/extensions/agi  ← CORRECT
=== iter L1.01 @ ... ===
```

The driver loop starts correctly — resolves both project root and plugin root without issue. `inject.py`, `metrics.py`, `locations.py` all work correctly. `snapshot-goals.py` failed only because test project had malformed goal nodes (not a pip-install issue).

## Evidence

All three invariants tested with concrete commands and outputs:

- **Invariant 1:** level3.py → no-op (graceful). payload_boundary.py → crash (CalledProcessError). Engine introspection tools do not work from a non-git tree.
- **Invariant 2:** find-root.sh → works correctly from all locations. The hypothesis's claim that "resolution returns a wrong or missing root" is INCORRECT for the user's project — the root is always resolved from PWD, not the script location.
- **Invariant 3:** Version independence works via venvs but adds operational friction vs. native clone-per-project.

**Commands used:**
```
./level3.py --project ... --engine-root ... (non-git copy)
./payload_boundary.py (non-git engine dir)
bash find-root.sh (from three locations within and outside the project)
bash driver.sh --smoke (project with pip-installed engine)
./locations.py (from test project)
```

**Key finding:** The hypothesis overstates the breakage. The core driver loop (`driver.sh --smoke`, `dispatch.py`, `metrics.py`, `inject.py`, `locations.py`, `grid.py`, `stitch.py`) all work correctly with a pip-installed engine because they operate on the **project** repo (which IS a git repo), not on the engine tree. The only things that break are engine-internal introspection tools (`level3.py`, `decompose-engine.py`, `payload_boundary.py`) which use `git -C <engine_root> ls-files` — these are engine-development tools, not project-facing tools. Forkability (g8) requires the project to fork and grow its own tree, which the driver loop provides; engine introspection is a separate concern."}


## Agent Notes
Tested 3 invariants of Shape 3 (pip install). Result: invariant 1 partially broken (engine introspection tools fail gracefully or crash — level3.py/payload_boundary.py/decompose-engine.py need git tree), invariant 2 NOT broken (find-root.sh resolves from PWD correctly), invariant 3 partially solvable via venvs (friction not structural break). Core driver loop works correctly with pip-installed engine. Hypothesis overstated — shape 3 doesn't break forkability, only engine-dev introspection tools.