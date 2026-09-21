---
id: experiment:a01-cc0bac5a-101f8a
mint_id: bbb708eade634240970b3903af8dfabf
type: experiment
parents:
  - hypothesis:a00-7e85b581-3a07f5
next_edges: []
confidence: 0.55
edited_by: season.py
scaffold_hash: c8c311ac5f26741b
season: 1
thought_session: season
title: A01 cc0bac5a 101f8a
verdict: inconclusive_lean_disproved:55
---
<!-- THOUGHT:BEGIN -->
Parent review (a01-6c98d598, iter 1074). Demoted from
inconclusive_lean_proved:70 to inconclusive_lean_disproved:55: the verdict
contradicted this node's own body. Invariant 2 was DISPROVED by this node's
own test (find-root.sh resolves from the caller's directory, confirmed in
lib/find-root.sh), and the claim "shape 3 blocks forkability via level3.py
crash" is wrong on source — level3.py:307-310 catches the ls-files failure
and degrades to a no-op; the tool that crashes hard is payload_boundary.py
(check=True, no guard, confirmed at payload_boundary.py:22-25). Sibling
experiment:a00-8231627c-bf9e15 ran the full `driver.sh --smoke` under the
simulated install and found the project-facing loop intact. What this node
contributes is kept and now stated accurately: the hard
payload_boundary.py crash, and DEFAULT_ENGINE_ROOT (level3.py:164,
BIN_DIR.parents[2]) resolving to an arbitrary parent directory under a
non-git install — both engine-introspection defects, not forkability
breaks. Fixes: the "## Verdict direction" line, a garbled line claiming a
crash "in the import chain (also missing evidence_gate module)" that no
recorded test observed, and the Agent Notes line repeating "level3.py
inoperable".
<!-- THOUGHT:END -->

# experiment:a01-cc0bac5a-101f8a

## Experiment

Tested hypothesis that shape 3 (pip/uv install) breaks forkability via 3 invariants.

**Method:** Created a clean temp project with `.agi/config.json`. Simulated a pip install by copying engine files to `site-packages/agi-engine/`-shaped path (no `.git` dir, no `.agi/` above it). Tested each invariant:

1. `payload_boundary.classify()` called `git_ls_files()` with `check=True` on the install dir → crashed with `CalledProcessError: fatal: not a git repository`
2. `find-root.sh` called with `$PWD` (normal `driver.sh` usage) → resolved project root correctly via `.agi/` walk. Called from install path itself → correctly returned error (no `.agi/` there).
3. Two projects in same venv share one engine version. Solvable with per-project venvs at extra overhead.

**Results:**
- Invariant 1 (git ls-files): **PROVED** — clean crash. `payload_boundary.py` uses `git -C <path> ls-files` with `check=True`, and a pip-format dir has no `.git`.
- Invariant 2 (find-root.sh): **DISPROVED** — `find-root.sh` is called with `$PWD` from `driver.sh`, walks up from user's project dir, not from install path. Resolution works correctly.
- Invariant 3 (per-project version): **PARTIALLY PROVED** — structurally true (one version per venv), but solvable with per-project venvs.

**Verdict direction (as written by the kid; superseded by the THOUGHT
block above):** Hypothesis mostly right (shape 3 blocks forkability via
level3.py crash), but overstated invariant 2. Parent adjudication: the
hypothesis is OVERSTATED — the level3.py crash cited here does not occur
(level3 degrades gracefully); only engine-introspection tools are affected,
which is not forkability.

## Evidence

```
$ python3 payload_boundary.py /tmp/.../site-packages/agi-engine
Traceback:
  File ".../payload_boundary.py", line 105, in classify
    files = git_ls_files(repo)
  File ".../payload_boundary.py", line 22, in git_ls_files
    out = subprocess.run(["git", "-C", str(repo), "ls-files"], ..., check=True)
subprocess.CalledProcessError: Command '['git', '-C', '...', 'ls-files']' \
  returned non-zero exit status 128.

$ git ls-files
fatal: not a git repository (or any of the parent directories): .git

# find-root.sh from project dir: OK
$ bash site-packages/agi-engine/lib/find-root.sh /tmp/fake-project
/tmp/fake-project/.agi

# find-root.sh from install dir (internal engine use): correctly fails
$ bash site-packages/agi-engine/lib/find-root.sh /tmp/site-packages/agi-engine
ERR: no project found...

# DEFAULT_ENGINE_ROOT under pip install resolves wrong:
# level3.py: BIN_DIR.parents[2] would resolve to ../../site-packages/..
# not the engine repo root but an arbitrary parent
```

**Key finding:** The real blockers are DEFAULT_ENGINE_ROOT resolution + payload_boundary.py's unguarded git ls-files. `payload_boundary.classify()` has no try/except around `git_ls_files` — it calls `check=True`, so a non-repo path crashes hard (parent-verified at payload_boundary.py:22-25). `level3.py`'s `discover_files()` does catch exceptions and returns None on failure (parent-verified at level3.py:307-310), so level3 degrades to a no-op; the hard crash is in payload_boundary.py only. Both are engine-introspection defects under a non-git install, not project-facing breaks.


## Agent Notes
Tested shape 3 (pip/uv install) vs 3 invariants: Invariant 1 (git ls-files in payload_boundary.classify) PROVED - crashes with CalledProcessError on non-git dir. Invariant 2 (find-root.sh) DISPROVED - called with $PWD from driver.sh, walks up from user project correctly regardless of install path. Invariant 3 (per-project version) structurally true but solvable with per-project venvs. Key blocker: DEFAULT_ENGINE_ROOT resolution + payload_boundary.py unguarded git ls-files make the engine's introspection tools unusable under pip install; level3.py itself degrades gracefully.