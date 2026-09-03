---
id: experiment:a00-5b72095d-2c70c0
mint_id: a4347868c5ea4995803592d05e6e64d6
type: experiment
parents:
  - hypothesis:a00-dbd82e32-0b294f
next_edges: []
scaffold_hash: d33a6b8f00f829e1
title: A00 5b72095d 2c70c0
---

# experiment:a00-5b72095d-2c70c0

## Hypothesis Under Test

"`grid.py commit --all` already produces the same version structure for every node regardless of body strategy — same `refs/grid/node/<mint-id>` namespace, same `blob sha` domains (git objects), same tree mechanics (one `mktree` per version, one `commit-tree` per version, one `update-ref` per version), same `grid.py log`/`diff`/`versions` contract. The only structural difference is tree entry count — one entry (`node.md`) for a body-rich node, two entries (`node.md` + `payload`) for a payload-rich node — and `build_tree`/`read_tree`/`tree_entries` already handle both identically."

## Experiment Design

Five probes into the grid structure and tool behaviour, comparing a body-rich population (e.g. `command:commands`, `cron:crons`, `config:secrets`) against a payload-rich population (e.g. `build:.env.example`, `build:.gitignore`, `build:AGENTS.md`, `build:GOALS.md`):

1. **Ref namespace**: enumerate refs for both populations using `git for-each-ref` and `git ls-tree` on the mint-id ref.
2. **Tree shape**: inspect tree contents for both — every entry name, mode, and blob sha domain.
3. **Tool contract**: run `grid.py log`, `grid.py diff`, `grid.py versions`, `grid.py status` for both populations and compare output shape.
4. **`commit_file` code path**: read the source (`commit_file` → `build_tree` → `tree_entries`) to confirm there is no branch on body strategy — only a single `if payload is not None: entries.append(...)` for the extra tree entry.
5. **`node_writer.update_node` code path**: confirm it writes `node.md` always, never the payload file, regardless of `payload_ref`.

## Results

### 1. Same ref namespace

All nodes — body-rich and payload-rich — live under `refs/grid/node/<32-hex-char-mint-id>`. No divergent namespace or naming convention.

```
# Body-rich examples (via mint_id):
refs/grid/node/b7e4f0a91c2d4e8fa63b5d7c8e1f2a04  # command:commands
refs/grid/node/dc4da698f3f94dbc83a0c2233b2a8b94  # cron:crons
refs/grid/node/eba3708aa2ce4642a394a3646f6e2a26  # config:secrets

# Payload-rich examples (via mint_id):
refs/grid/node/d1826fa76ffd463f86b416351197facf  # build:.env.example
refs/grid/node/aae1893604ff4ef0888dd954909d1b1c  # build:.gitignore
refs/grid/node/f831dd7ca9df44048061087936cf4acd  # build:AGENTS.md
refs/grid/node/16fd4c7f953c40298fc1a486e8a2a4c8  # build:GOALS.md
```

### 2. Same tree shape, payload is an extra entry not a fork

Body-rich: tree has ONE entry `node.md` (`100644 blob <sha>`).
Payload-rich: tree has TWO entries — `node.md` (`100644 blob <sha>`) + `payload` (`<mode> blob <sha>`).

The `node.md` entry uses the same mode (`100644`), the same blob hash algorithm, and lives at the same tree-root path. The payload entry is the ONLY addition — no structural fork.

Notably, `build:AGENTS.md` has `120000` (symlink) mode for its payload, confirming the mode-preserving round-trip (goal:s9) works correctly for both regular files and symlinks.

```
$ git ls-tree refs/grid/node/b7e4f0a91c2d4e8fa63b5d7c8e1f2a04  # body-rich
100644 blob e148d0176d8ec021c804acb843e7d98fe1d7cb03	node.md

$ git ls-tree refs/grid/node/d1826fa76ffd463f86b416351197facf  # payload-rich
100644 blob 96ffc32941888375aceef21fa14782383f57b5ac	node.md
100644 blob d9c9ecb06a06245bb713da9991fb46476226e0db	payload

$ git ls-tree refs/grid/node/f831dd7ca9df44048061087936cf4acd  # payload-rich with symlink
100644 blob edff047db9fe27fc767fc2d0b85544ff2d9dde97	node.md
120000 blob 681311eb9cf453d0faddf3aacaec7357e97ba8e9	payload
```

### 3. Same grid.py tools produce identical output shape

`grid.py log` produces the same column format for both populations:

```
$ grid.py log command:commands -n 3
b5004657b 2026-09-03 v4 command:commands
e3f2735ce 2026-09-03 v3 command:commands
a961a18ef 2026-09-03 v2 command:commands

$ grid.py log build:.gitignore -n 3
22a48b10e 2026-09-02 v14 build:.gitignore
90c3d52a3 2026-09-02 v13 build:.gitignore
423be3ec3 2026-09-02 v12 build:.gitignore

$ grid.py log build:GOALS.md -n 3
0c7dafd17 2026-09-03 v39 build:GOALS.md
7f396046d 2026-09-02 v38 build:GOALS.md
e6c4a464b 2026-09-02 v37 build:GOALS.md
```

`grid.py versions` works for both — different counts per node but same output format.
`grid.py diff` works for both — `command:commands --back 1` produced a real diff; `build:.env.example --back 1` produced an empty diff (correct: v1→v2 no node.md change), demonstrating the tool does not break on either strategy.
`grid.py status` enumerates all types uniformly as `NEW`, `CHANGED`, or `CLEAN`.

### 4. `commit_file` has no branch on body strategy (source code)

From `grid.py` `commit_file` (line 640):

```python
def commit_file(root, path, ref, msg_prefix, *, trailer=None, payload=None):
    tree = build_tree(root, path, payload)
    ...
    n = int(git(root, "rev-list", "--count", tip)) + 1 if tip else 1
    ...
    commit = git(root, "commit-tree", tree, *parent, "-m", message)
    git(root, "update-ref", ref, commit)
    return f"v{n}"
```

There is NO conditional on "is this body-rich or payload-rich". The `payload` parameter is None for body-rich, a Path for payload-rich. Inside `tree_entries` (line 490):

```python
def tree_entries(root, path, payload, *, write):
    entries = [(NODE_ENTRY, *hash_path(root, path, write=write))]
    if payload is not None:
        entries.append((PAYLOAD_ENTRY, *hash_path(root, payload, write=write)))
    return sorted(entries)
```

This `if payload is not None` is the ONLY difference — it adds one additional tree entry `("payload", mode, blob)`. The same `mktree`, same `commit-tree`, same `update-ref`, same reference namespace (mint-id ref via `write_ref_for`) for every node. `ref_tip` comparison also compares the whole tree (payload included), which is correct — a payload-only edit produces a real version.

### 5. `node_writer.update_node` writes `node.md` always

From `node_writer.py` line 598: `update_node` has zero logic branching on `payload_ref`. It reads the node file, merges frontmatter, writes the edited body to `node.md` — always. A write-path edit to a payload-rich node changes only `node.md` in the next grid version, leaving the `payload` tree entry pointing at the same blob as the previous version (until the next `grid.py commit --all` picks up external payload edits too). This is the seam `goal:g13` identifies — the asymmetry is in the writer behaviour, not the grid structure.

## Verdict

`inconclusive_lean_proved:90` — The grid layer itself is proven to version both body strategies identically across all five probes. The only remaining uncertainty is whether a scenario exists where the write path's asymmetric treatment (always editing `node.md`, never the payload file) creates a functional problem for a specific class of nodes. The hypothesis explicitly narrows scope to "grid structure only, not the write-path behaviour," and within that scope the evidence is overwhelming.

## Evidence

All commands run from `/home/ubuntu/work/agi` against the live repo. Raw output archived above in ## Results.