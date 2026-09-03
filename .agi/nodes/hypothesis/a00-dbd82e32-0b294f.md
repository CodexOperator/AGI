---
id: hypothesis:a00-dbd82e32-0b294f
mint_id: 4e3b7d8b55f44039a4946a0d2952eec0
type: hypothesis
parents:
  - goal:g13
next_edges: []
confidence: 0.8
scaffold_hash: 74b964a5da96094e
title: A00 dbd82e32 0b294f
verdict: pending
---
# hypothesis:a00-dbd82e32-0b294f

## Hypothesis

**Claim.** `grid.py commit --all` already produces the same version structure for every node regardless of body strategy — same `refs/grid/node/<mint-id>` namespace, same `blob sha` domains (git objects), same tree mechanics (one `mktree` per version, one `commit-tree` per version, one `update-ref` per version), same `grid.py log`/`diff`/`versions` contract. The only structural difference is tree entry count — one entry (`node.md`) for a body-rich node, two entries (`node.md` + `payload`) for a payload-rich node — and `build_tree`/`read_tree`/`tree_entries` already handle both identically.

This means the grid layer imposes no constraint on the write path's ability to produce uniform versions for both body strategies. **The gap `goal:g13` names — "how payload-backed and node-backed bodies produce the same grid version" — is on the write side, not the grid side.** `node_writer.update_node` writes the body into `node.md` regardless of whether the node has a `link_ref` pointing elsewhere; a build node whose body was edited through the write path would change only `node.md` in the grid tree, while the payload file (and its grid entry) stay unchanged until the next `grid.py commit --all` picks up the external edit. The two strategies are versioned identically by the grid; they are produced identically only when the write path respects the storage decision.

**What would prove it.**

1. **Same ref namespace.** Every node — body-rich or payload-rich — lives under `refs/grid/node/<mint-id>`. Verified by enumerating both populations' refs through `git for-each-ref refs/grid/node/`.
2. **Same tree shape for non-payload entries.** `git ls-tree <tip>` for a body-rich node shows `node.md`; for a payload-rich node `node.md` is the first entry with the same mode (`100644`), same hash domain (git blob). The payload entry is a second entry alongside `node.md`, not a structural fork.
3. **Same grid.py tools work identically.** `grid.py log`, `grid.py diff`, `grid.py versions` produce the same output shape for both populations — only the content differs, never the format or the presence of a version.
4. **`commit_file` has no branch on body strategy.** `grid.py cmd_commit` resolves `payload_ref` and passes a `Path | None` to `build_tree`, which adds exactly one extra tree entry when the path is non-None. No grid-level branch on "is this a body-rich or payload-rich node."
5. **A write-path change to a build node's body would produce a grid tree that differs only in `node.md`, not in tree structure.** The grid would version it identically to a body-rich node's body edit — the asymmetry is in the PAYLOAD entry staying stale, not in the grid structure diverging.

**What would disprove it.**

- A body-rich node whose grid ref uses a different namespace or naming scheme than a payload-rich node's — e.g., `refs/grid/node/goal/g13` vs `refs/grid/node/build/grid.py` with different formatting.
- A body-rich node whose `grid.py log` output has a different column count, heading, or behaviour (e.g. `diff --back 1` works for payload-rich but errors for body-rich).
- A payload-rich node that cannot have its body versioned via `update_node` → `grid.py commit --all` producing a version with the body change — i.e., the grid treats `node.md`+`payload` as an inseparable unit that cannot be partially updated.
- A grid reader that branches on tree entry count to decide whether a version is "a real version" — which would mean the two strategies produce different KINDS of version.
- `node_writer.update_node` on a payload-rich node producing a version that includes neither the body change (in `node.md`) NOR the payload change — because the writer silently wrote to the wrong file.

**Scope.** Grid structure only, not the write-path behaviour. The write path's treatment of payload-backed bodies (`update_node` always editing `node.md` rather than the payload file) is the goal's real seam, and this hypothesis exists to separate the grid claim from the writer claim — so a reader knows which half of the unification is already standing.


## Agent Notes
Grid already versions payload-backed and node-backed nodes identically — same ref namespace, same hash domains, same tree mechanics. The gap goal:g13 names is on the write side (update_node edits node.md always, never the payload file), not the grid side.
