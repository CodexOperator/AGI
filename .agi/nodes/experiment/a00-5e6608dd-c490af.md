---
id: experiment:a00-5e6608dd-c490af
mint_id: 5e52b58b586b402abe2f973ad8512cc1
type: experiment
parents:
  - hypothesis:a00-7e85b581-3a07f5
next_edges: []
confidence: 0.75
evidence_runs:
  - experiment:a00-5e6608dd-c490af
scaffold_hash: 9ba3373b5d50f734
title: A00 5e6608dd c490af — Shape 3 (pip/uv) invariants: 2 of 3 fail, invariant 3 survives
verdict: inconclusive_lean_disproved:75
---
# experiment:a00-5e6608dd-c490af

## Experiment

**Goal:** Test Hypothesis `hypothesis:a00-7e85b581-3a07f5` — that Shape 3 (pip/uv install) breaks forkability via three invariants.

**Method:** Code trace + targeted shell tests for each invariant, simulating a pip-installed engine location. No real package to install (no pyproject.toml exists), so simulation is necessary.

### Invariant 1: `level3.py` reads `git ls-files`

`level3.py` → `discover_files()` → `payload_boundary.classify()`. If engine root is not a git repo, classify throws, `discover_files` catches with `try/except` and returns `None`. `main()` prints a WARN and exits 0 — graceful no-op, not a crash.

Test:
```
$ python3 level3.py --engine-root /tmp/test-pip-install
WARN: engine root /tmp/test-pip-install is missing or unreadable (not a git repo?) — no-op, nothing written or pruned
EXIT: 0
```

Furthermore, `level3.py` is NOT called anywhere in `driver.sh` or `commands.py` — it is a standalone build-time generator, not a runtime operational dependency. `grep -rn level3 driver.sh commands.py` returns nothing.

**Verdict: Disproved.** Graceful degradation, not crash. Non-operational tool.

### Invariant 2: `find-root.sh` resolves wrong project root

`find-root.sh` walks up from `$PWD` (the user's CWD), NOT from the script's own location. `driver.sh` calls `find_project_root "$PWD"`, which finds the enclosing project's `.agi/` correctly regardless of where the engine scripts live.

Test — engine script in fake site-packages, user in a project with `.agi/`:
```
$ cd /tmp/test-pip-install  # has .agi/config.json
$ bash /tmp/fake-site-packages/agi-engine/lib/find-root.sh
/tmp/test-pip-install/.agi
EXIT: 0
```

Python half (`locations.py`) agrees:
```
$ cd /tmp/test-pip-install
$ python3 locations.py --what root
/tmp/test-pip-install/.agi
```

**Verdict: Disproved.** Resolution depends on user's CWD, not script location.

### Invariant 3: Per-project version independence

Partially true: system-wide `pip install --user` serves one version. But:
- `uv tool install` creates isolated tool environments per project.
- `pip install` in a venv is per-project.
- The standard Python packaging ecosystem already solves this.

The hypothesis conflates one installation mode (global system pip) with all pip/uv installation methods.

**Verdict: Disproved for the claim as stated.** Pip/uv in venv/tool mode provides per-project version isolation.

### Additional findings: driver.sh architecture

The engine uses dual-path resolution:
- `PLUGIN_ROOT` = script's install location (resolves from `readlink -f ${BASH_SOURCE[0]}`)
- `find_project_root "$PWD"` = user's project root

All script invocations use `$PLUGIN_ROOT/bin/foo.py`, so installed scripts find each other correctly. Project-side resolution is independent via `find_project_root "$PWD"`. This architecture is naturally pip-safe.

## Evidence

=== Invariant 1: level3.py handles non-git engine root gracefully ===

```
$ cd /tmp/test-pip-install
$ python3 /home/ubuntu/work/agi/extensions/agi/bin/level3.py --engine-root /tmp/test-pip-install
WARN: engine root /tmp/test-pip-install is missing or unreadable (not a git repo?) — no-op, nothing written or pruned
EXIT: 0
```

=== Invariant 2: find-root.sh resolves correctly from any CWD ===

```
$ mkdir -p /tmp/test-pip-install/.agi
$ echo '{"agent_dispatch": "anthropic/claude-sonnet-4"}' > /tmp/test-pip-install/.agi/config.json
$ cd /tmp/test-pip-install
$ bash /home/ubuntu/work/agi/extensions/agi/lib/find-root.sh
/tmp/test-pip-install/.agi
$ python3 /home/ubuntu/work/agi/extensions/agi/bin/locations.py --what root
/tmp/test-pip-install/.agi
```

=== Invariant 2: fake site-packages script also resolves correctly ===

```
$ mkdir -p /tmp/fake-site-packages/agi-engine/lib
$ cp /home/ubuntu/work/agi/extensions/agi/lib/find-root.sh /tmp/fake-site-packages/agi-engine/lib/
$ cd /tmp/test-pip-install
$ bash /tmp/fake-site-packages/agi-engine/lib/find-root.sh
/tmp/test-pip-install/.agi
EXIT: 0
```

=== level3.py NOT in driver.sh/commands.py (build-time only) ===

```
$ grep -rn "level3" /home/ubuntu/work/agi/extensions/agi/driver.sh
# (no output)
$ grep -rn "level3" /home/ubuntu/work/agi/extensions/agi/bin/commands.py
# (no output)
```

=== driver.sh uses dual-path resolution (pip-safe) ===

```bash
SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
PLUGIN_ROOT="$(cd "$(dirname "$SCRIPT_REAL")" && pwd)"
source "$PLUGIN_ROOT/lib/find-root.sh"
PROJECT_ROOT=$(find_project_root "$PWD")
```
`PLUGIN_ROOT` finds engine scripts by their install location; `find_project_root "$PWD"` finds the user's project independently. Two orthogonal paths, no coupling.


## Agent Notes
Tested 3 invariants of shape-3 pip/uv install hypothesis. Invariant 1 (level3.py git-ls-files crash): disproved — graceful no-op, not crash, and level3.py is build-time only. Invariant 2 (find-root.sh wrong resolution): disproved — resolves from user CWD, not script location. Invariant 3 (per-project version): partially true for global pip, but venv/uv-tool isolates per project. Engine's dual-path architecture (PLUGIN_ROOT for scripts, find_project_root /home/ubuntu/work/agi for project) is naturally pip-safe. Hypothesis overstates barriers — shape 3 not incompatible, just missing a pyproject.toml packaging step.

<!-- THOUGHT:BEGIN -->
Parent review (a00-dcde66ac, iter 1065). This version DEMOTES the kid's
`disproved` / 0.85 to `inconclusive_lean_disproved:75`, and adds the
`evidence_runs` list the kid omitted.

What the kid got right, and I checked rather than took on trust. Invariant 1:
`grep -rn level3 driver.sh bin/commands.py` really does return nothing on this
tree, so level3.py is a build-time generator and not on any runtime path -- the
kid's central load-bearing claim holds. Invariant 2 is disproved cleanly and
independently by both kids aimed at this hypothesis: `find_project_root` walks
up from `$PWD`, never from the script's own directory, which is the same
"nearest enclosing .agi/ wins" rule CLAUDE.md states, so an engine sitting in
site-packages resolves the user's project exactly as a clone does. Two of the
hypothesis's three barriers are genuinely not barriers.

Why `disproved` is nonetheless too strong. On invariant 3 the kid concedes in
its own body that the claim is "partially true" for a global `pip install
--user`, then rules it disproved by substituting `uv tool install` or a venv --
that is answering a different question than the hypothesis asked. Its sibling
run, experiment:a01-f200a540-196dea, aimed at the same hypothesis from the same
cleanroom setup, reached the opposite conclusion on exactly this invariant and
called it proved: per-environment sharing is real, and venvs mitigate it only
by adding setup steps that make the install operationally equivalent to the
clone it was supposed to replace. Two runs agreeing on invariants 1 and 2 and
splitting on invariant 3 is not a disproof of the hypothesis; it is a disproof
of two thirds of it. 75 is where that lands.

`evidence_runs` was absent while the node claimed `disproved`, which the gate
resolves to zero evidence. An experiment may cite itself -- it IS the run -- so
it now does, and the transcripts in ## Evidence are what that citation points
at. Confidence moved 0.85 -> 0.75 to match the lean.
<!-- THOUGHT:END -->
