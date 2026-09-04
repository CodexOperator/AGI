---
id: mvp:a01-f1a34371-eeec0b
mint_id: 76b1177f6f0444c0a07a5debe3bc8128
type: mvp
parents:
  - verdict:a00-4c4fbb51-0f3630
next_edges: []
scaffold_hash: 8b8c9dd1104b7e34
title: A01 f1a34371 eeec0b
---

# mvp:a01-f1a34371-eeec0b

## MVP

**Worktree isolation in `dispatch.py`: each parallel kid gets its own `git worktree add --detach` before work begins, and the parent harvests results from the main tree after the kid completes.**

`verdict:a00-4c4fbb51-0f3630` proved `git worktree add --detach` overhead is negligible: 0.094s warm, 0.80s cold, 0.19s for 2 kids — well within iteration bounds by 15-158×. The goal:g4.1 collision record (three incidents) shows every collision came from a whole-tree command (`git commit -A`, `git checkout .`), never from two agents editing the same file. Worktree isolation eliminates the root cause: kids in separate worktrees cannot collide on whole-tree commands because each kid's working tree is a detached branch.

### What it must satisfy

1. **`dispatch.py` creates a detached worktree per kid before spawning the agent.** Each kid's `spawn_args` has `cwd` set to its private worktree path, not the main checkout.
2. **The worktree is cleaned up when the kid finishes or the reaper declares it dead.** No orphan worktrees survive the iteration (verified by `git worktree list` after each iteration).
3. **The parent (or `post_wire`) reads kids' produced files from the main checkout — the kid writes into a scratch `.claude/worktrees/` tree, and its node file lands in `.agi/nodes/` of the main tree via a path the kid can see.** This is the load-bearing interface: the kid must be able to write its node file to a location the parent can read, without crossing a worktree boundary that `git` manages implicitly.
4. **`git worktree prune` runs after all worktrees are removed**, to keep `.git/worktrees/` clean.
5. **The kid's environment includes `GIT_WORKTREE_DIR` so it knows where it is running.** The kid never runs `git` commands against the main tree.
6. **Existing contracts stay unchanged:** `"Do not run git"` in every agent prompt is already the safe default and is effective when kids cannot reach each other's files. With worktree isolation the guard is structural rather than contractual.
7. **Integration tests:** for each spawned kid, verify the worktree exists under `.claude/worktrees/<agent_id>/` and resolves to the correct commit. After the kid finishes (or is reaped), verify the worktree is gone.

### What it explicitly is NOT

- **Not a solution for nested tiers.** `goal:g4.1`'s open questions (whose worktree under a parent, where review happens, iteration commit across N branches) are deliberately unresolved here. This MVP covers exactly the current architecture: **one main tree, N peer kids, no parent loop.** A parent hierarchy will need its own MVP when the hierarchy is built.
- **Not a merge step.** Kids produce node files only (not engine code edits), so the main-tree harvest reads a node file from the kid's session directory or a designated path, not a git merge. Engine-code work is rare enough (goal:g6 exceptions) that it can stay serialised or be handled by a later MVP.
- **Not a change to `post_wire`.** Post-wire processing reads nodes from the graph; those nodes are written by `cli.py done` into the kid's session output, and the parent harvests them from there. The connectivity is orthogonal to the worktree.

### Falsifier

A later reader knows the MVP is discharged when:
- Two kids spawned in the same iteration each get a `git worktree list` entry pointing to a detached HEAD under `.claude/worktrees/<agent_id>/`
- Both kids can write `cli.py done` reports and node files that the parent can read (no permission errors, no "this is a git-controlled directory" errors)
- After reaper completes, `git worktree list` shows no orphan entries for that iteration
- `python3 -m pytest extensions/agi/tests/ -q` stays green (no regressions in the dispatch layer)

## Inputs

- `dispatch.py` reads `config.json` which may gain `worktree: { enabled: bool, base_path: str }` under `spawn`, or defaults to `enabled=True` with worktrees at `<root>/.claude/worktrees/<agent_id>/`
- Per-agent: the agent id, the ref to check out (currently `HEAD`, the checked-out branch)
- The main checkout path for cross-boundary node file reads

## Outputs

- Per spawned kid: `git worktree list` shows `<root>/.claude/worktrees/<agent_id>/ <hash> (detached HEAD)`
- After cleanup: no entries for that agent id in `git worktree list`
- `refs/grid/*` is unchanged — grid versions a node independently of which worktree it was committed from

## Implementation sketch (not the code — this is the design contract `build` nodes must satisfy)

```
def prepare_worktree(root, agent_id, ref="HEAD"):
    path = root / ".claude" / "worktrees" / agent_id
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "worktree", "add", "--detach", str(path), ref],
                   cwd=str(root), check=True, capture_output=True)
    return path

def cleanup_worktree(root, agent_id):
    path = root / ".claude" / "worktrees" / agent_id
    subprocess.run(["git", "worktree", "remove", "--force", str(path)],
                   cwd=str(root), check=False, capture_output=True)
    subprocess.run(["git", "worktree", "prune"],
                   cwd=str(root), check=True, capture_output=True)
```

The actual `build` node must implement these in `dispatch.py`'s spawn path, between the zoom context generation and the `Popen` call.

