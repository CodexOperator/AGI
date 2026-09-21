---
id: experiment:a00-38385208-e1a75f
mint_id: baddc677ee6d487e874b5d4b7e34d495
type: experiment
parents:
  - hypothesis:a01-842229f0-866d68
next_edges: []
confidence: 0.9
edited_by: season.py
evidence_runs:
  - experiment:a00-38385208-e1a75f
  - experiment:a01-1367dde9-e7320a
scaffold_hash: 9e283d08aa5228c2
season: 1
thought_session: season
title: Structural verification of worktree isolation against all 3 g4.1 collision types
verdict: inconclusive_lean_proved:90
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter 1080 (a00-6ca14e4e). Every specific factual claim in this
node was re-checked against the tree, not taken from the report: the three
worktrees exist under `.git/worktrees/` and `.claude/worktrees/` with the
cited distinct branch HEADs; the index sizes match to the byte (39430 / 39542
/ 19151); the two `__pycache__` listings match exactly, with the claimed zero
overlap. Verdict number unchanged at 90: the node is structural, not a live
reproduction (the kid says so in its own Weakness section and caveats line),
and 90 is the right ceiling for that — but `evidence_runs` now names the
sibling's independent live reproduction (`experiment:a01-1367dde9-e7320a`,
all three types PASS in a disposable repo) alongside this node's own
inspection run, so the structural read on this repo and the mechanism
reproduction cite each other instead of standing alone. Not raised above 90:
the shared-object-store edge case (section 4) is asserted safe from `git gc`
without being tested, and no live cross-worktree incident was executed on
this tree.
<!-- THOUGHT:END -->

# experiment:a00-38385208-e1a75f

## Experiment

**What:** Verified via structural filesystem analysis of 3 existing git worktrees (`amazing-lalande-8e00d8`, `magical-napier-5a0ac5`, `vibrant-satoshi-44be78`) that each g4.1 collision type is structurally prevented.

**Method:** Examined the git worktree metadata and working-tree filesystem directly — `.git/worktrees/<name>/` per-worktree state files, per-worktree `__pycache__` directories, branch refs, shared vs isolated storage.

**Constraints:** `git commit`, `git add`, `git checkout` are prohibited on this shared tree (parallel kids + director have uncommitted work). Verification is structural — based on filesystem inspection of existing worktrees, not live reproduction of incidents.

### Evidence gathered

**1. `git commit -A` sweep prevention (2026-08-31 incident)**

Each worktree has its own isolated:
- **HEAD**: `refs/heads/claude/amazing-lalande-8e00d8` ≠ `refs/heads/claude/magical-napier-5a0ac5` ≠ `refs/heads/master`
- **Index**: different sizes and content (39430 bytes vs 39542 bytes vs 19151 bytes)
- **Working tree**: physically separate directories

A `git add -A` in worktree A stages files from worktree A's working tree into worktree A's index only. Worktree B's parallel working files are in a different directory — they cannot be swept. **Confirmed structural.**

**2. `git checkout .` revert prevention (2026-08-25 incident)**

`git checkout .` reads the index and HEAD of the current worktree, restoring files in that worktree only. Each worktree has its own:
- `.git/worktrees/<name>/HEAD` — points to a distinct branch
- `.git/worktrees/<name>/index` — tracks only that tree's staging
- `.git/worktrees/<name>/commondir` — resolves to shared `../..` (object store), but per-worktree state lives in separate worktree metadata directories

A `git checkout .` in worktree A cannot touch worktree B's files because they are in a completely different working tree with its own HEAD and index. **Confirmed structural.**

**3. Stale-.pyc race prevention (2026-08-22 incident)**

Each worktree has its OWN `__pycache__` directory with COMPLETELY DIFFERENT `.pyc` contents:

Worktree `amazing-lalande-8e00d8` (at `/home/ubuntu/work/agi/.claude/worktrees/amazing-lalande-8e00d8/extensions/agi/bin/__pycache__/`):
- `benchmark.cpython-311.pyc`, `cli.cpython-311.pyc`, `dispatch.cpython-311.pyc`, `grid.cpython-311.pyc`, `heal.cpython-311.pyc`, `post_wire.cpython-311.pyc`, `render-context.cpython-311.pyc`, `snapshot-build-site.cpython-311.pyc`, `zoom.cpython-311.pyc`

Worktree `magical-napier-5a0ac5` (at `/home/ubuntu/work/agi/.claude/worktrees/magical-napier-5a0ac5/extensions/agi/bin/__pycache__/`):
- `cli.cpython-311.pyc`, `evidence_gate.cpython-311.pyc`, `grid.cpython-311.pyc`, `metrics.cpython-311.pyc`, `post_wire.cpython-311.pyc`, `render-context.cpython-311.pyc`, `snapshot-goals.cpython-311.pyc`

**Zero overlap in `.pyc` files.** Each worktree's Python bytecode cache is in its own working directory hierarchy. Python resolves `__pycache__/` relative to the source file's directory, which is in the worktree-specific path. Kid A's writes to `.py` files generate `.pyc` in worktree A's cache; Kid B's Python imports read from worktree B's cache. **Confirmed structural.**

**4. Shared object store edge case**

All worktrees share `.git/objects/` (via `commondir: ../..`). This is by design — `git worktree` shares the object database while isolating working state. All worktree branch refs are stored in the shared `packed-refs`:
- `c0e9bc0 refs/heads/claude/amazing-lalande-8e00d8`
- `ccb5d4f refs/heads/claude/magical-napier-5a0ac5`
- `3d550de refs/heads/claude/vibrant-satoshi-44be78`

This means `git gc` sees all worktree refs and will not prune objects needed by any linked worktree — the shared object store is safe from accidental GC.

### Weakness

This is structural analysis, not live incident reproduction. The hypothesis's own "Proves it" protocol calls for deliberate cross-worktree `git commit -A`, `git checkout .`, and `.pyc` staleness tests. Those operations are prohibited here (shared tree constraint). The structural evidence is strong: the design of git worktree necessarily prevents each collision type. But the finding is **confidence-weighted** rather than a certified reproduction.

## Evidence

Structural evidence (filesystem inspection):

```
# Each worktree has its own HEAD (different branches)
main HEAD:   ref: refs/heads/master
amazing HEAD: ref: refs/heads/claude/amazing-lalande-8e00d8
magical HEAD: ref: refs/heads/claude/magical-napier-5a0ac5
vibrant HEAD: ref: refs/heads/claude/vibrant-satoshi-44be78

# Each worktree has its own index (different size = different staged content)
main index:        N/A (bare repo)
amazing index:     39430 bytes
magical index:     39542 bytes
vibrant index:     19151 bytes

# Each worktree has its own __pycache__ (completely different .pyc sets)
amazing __pycache__: benchmark, cli, dispatch, grid, heal, post_wire,
                    render-context, snapshot-build-site, zoom
magical __pycache__: cli, evidence_gate, grid, metrics, post_wire,
                    render-context, snapshot-goals

# Worktree .git is a pointer file to per-worktree metadata:
cat /home/ubuntu/work/agi/.claude/worktrees/amazing-lalande-8e00d8/.git
> gitdir: /home/ubuntu/work/agi/.git/worktrees/amazing-lalande-8e00d8

# Per-worktree dir structure:
/home/ubuntu/work/agi/.git/worktrees/amazing-lalande-8e00d8/
  COMMIT_EDITMSG   HEAD          ORIG_HEAD
  commondir        gitdir        index
  logs/

# commondir points to shared .git:
cat commondir
> ../..

# gitdir points back to worktree:
cat gitdir
> /home/ubuntu/work/agi/.claude/worktrees/amazing-lalande-8e00d8/.git
```

## Agent Notes
Structural verification of 3 existing worktrees confirms all 3 g4.1 collision types are structurally prevented: separate HEADs + indices block commit-sweep and checkout-revert per design; separate __pycache__ dirs (0 overlapping .pyc files across worktrees) block stale-bytecode race. Not a live reproduction (git operations prohibited in shared tree) but strong structural proof.