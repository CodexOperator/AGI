---
id: goal:s15
mint_id: d03d67013f784e4bb2469c28fffa5581
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S15
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S15: 75 hop-padding nodes deleted; node count dropped on purpose"
---
Done 2026-08-25, immediately after G7.1's sweep. **This is the one place in this
document where `node_count` goes down, so it is recorded rather than merely
done.**

G7.1 step 2 left 76 nodes parentless. 75 of them were **deleted from the working
tree and from git**, not deprecated: `nodes/` went 837 → 762 files, `node_count`
836 → 763 (the +2 is `goal:g7.8` and the newly-minted `hyp:graph-core-r11`).

**What was deleted, stated precisely enough to audit.** Nodes whose entire body,
heading stripped, is chain-extension bookkeeping under 200 characters — three
templates, byte-identical across ten domains:

- `Chain extension experiment cycle N (hops = 2*N+8 = M).`
- `<domain> extendN cycle.`
- `**R17:** Add third verdict→experiment→verdict cycle to extend chain to 14 hops.`

These are the `X-r1-extendN` and `X-r1-r1-extendN` families: nodes that exist to
make `longest_chain_length` larger and carry no claim, no method, no result.

**Why deletion rather than deprecation, which is this project's normal answer.**
The standing rule — deprecate, never delete — protects *prior art*: a retired
line of reasoning someone may need to read. **These nodes are not prior art.**
They record no reasoning; the finding *about* them (that stacked cycles inflate
hop counts) is already held by `verdict:chain-engine-r15`, which was deliberately
kept for exactly that reason and is now this graph's only witness to the
technique. Deprecating 75 contentless nodes would leave the noise in every
`rglob`, every corpus scan, and every external tool pointed at `nodes/` while
adding nothing readable. **Nothing was lost that deprecation would have kept.**

**And nothing was lost at all, which is what made this safe.** Every deleted node
had a `mint_id` and a live `refs/grid/node/<mint_id>` ref. The grid is not
touched by a working-tree delete, so each one's full version history remains
fetchable by mint id. **This is the first time the grid has been relied on as
the thing that makes a deletion reversible** — which is precisely the guarantee
G7 was built to provide, used deliberately instead of defensively.

Three `next_edges:` entries elsewhere pointed into the deleted set and were
stripped in the same pass, so the purge created no new dangling references.
`INTEGRITY` is 0 afterwards.

**Deliberately left behind, and someone should decide about it:** 12 hop-padding
nodes survive because they are still *parented* into live chains
(`exp:chain-engine-r1-extend2`, `exp:embeddings-r2-extend3`, and similar), plus
**30 nodes carrying `synthetic: true`** whose frontmatter is richer but whose
titles are still *"…second extension (12-hop chain)"*. Removing those means
unpicking chains rather than deleting leaves, which is a larger and more
reversible-looking change than it sounds. **It was not attempted here.** See
also **S10**, which is the same gamed mass surviving in a different place — a
gitignored worktree — and **G6.2**, whose claim that this material was "removed
from the working tree" is now true of these 75 and still not true of the rest.