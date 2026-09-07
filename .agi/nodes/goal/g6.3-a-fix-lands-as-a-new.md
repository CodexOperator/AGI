---
id: goal:g6.3
mint_id: 6634587e21fc4173911d4024abb7d858
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
goal_id: G6.3
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - hyp:payload-in-node
  - build:bin-stitch@v2
status: complete
tags:
  - goal
  - subgoal
thought_session: season
title: "G6.3: A fix lands as a new version of a build node"
---
**The mechanism to test, and the reason to test it on real work.** Today an
engine fix is edited in the engine repo, and `level3.py` re-derives the build
node afterwards — the node trails the code. The target is the reverse: a fix is
applied *as a version update to the build node*, and the engine file follows
from it via `stitch.py`.

This is also how the grid's version dimension gets exercised for the first time
on content that matters. `refs/grid/node/<id>` already records one version per
change and the grid held 535 refs after its first full pass; what has never been
tested is a build node accumulating **meaningful** versions — v1 → v2 → v3 as a
real fix evolves — and `stitch.py` materialising a chosen version rather than
whichever is current.

Falsifier: take one real fix from this session, apply it as a build-node version
update, stitch it out, and confirm the engine file is byte-identical to what the
direct edit produced. If it is not, the version layer is not yet a source of
truth and should not be described as one.

**Payload model decided 2026-08-23 (iter-9006 → 9008), and the falsifier is now
known to be passable.** The chain is `hyp:payload-in-node` →
`exp:grid-payload-roundtrip` → `verdict:payload-in-node` (proved, conf 0.75,
evidence resolves).

- **The pick: grid-ref payload.** `payload_ref` keeps its shape; only its
  *resolution rule* changes, from "read this path off the engine tree" to "read
  this path from `refs/grid/node/<id>`'s tree". Inline body lost — three
  independent docstrings rule it out and a source file containing a fence breaks
  the node's own parser. Blob-sha lost on authoring mechanics, not storage: the
  blob must exist before the sha can be written, so the edit is never expressible
  as one node write, and a sha-to-sha diff says *that* something changed and
  nothing about *what*.
- **Proved at the mechanism level, with bytes.** Git's tree format carries
  content, exec bit and symlink-ness losslessly across real version history — 4
  files × 3 bumps, sha256-matched against a non-git baseline.
- **Blocked on S9, and this is the operative sentence:** "payload lives in the
  node's grid ref" is a proved **design**, not a proved **deployment**. Wiring
  resolution to `commit_file()` as it ships today reproduces the failing variant.
  S9 first.

**Correction 2026-08-25: a version is a grid commit, not a second file.** On
2026-08-24 this was implemented as separate `@v2` node *files* — `level3:x` plus
`level3:x@v2`, both pointing at one `payload_ref`, with `supersedes:` linking
them. That was a misreading of this goal. "A fix lands as a new version of a
build node" means the node is **updated in place** and the grid records the
version; it does not mean a new file per version. The file convention duplicated
what `refs/grid/node/<id>` already does, inflated the on-disk graph with one node
per revision, and forced `stitch.py` to grow a whole version-chain concept
(`build:bin-stitch@v2`) to tell a legitimate pair apart from a genuine
duplicate `payload_ref`.

**The convention going forward:** edit the node, let the grid be the history.
Version history is not flat structure on disk — it is depth you zoom into
(**G2.7**). Grid commit messages should name the parent nodes by **mint id**
(**G2.5**) so a renderer can traverse disk nodes and grid commits as one
hypergraph.

The four `@v2` nodes already minted (`bin-stitch`, `lib-find-root.sh`,
`skills-agi-SKILL.md`, `bin-grid`, plus `src-graph-core-identity`) stay for now
and are folded back in a later pass — deliberately not rushed, since collapsing
them touches `stitch.py`'s chain logic and the grid refs that already carry their
history. `stitch.py`'s version-chain support is not wasted either way: it is what
keeps a transitional corpus from reading as drift.

**Built and falsified 2026-08-25. Both halves of the untested case now run.**

The payload lives in the node's own ref: `refs/grid/node/<mint-id>` holds a
two-entry tree, `node.md` plus `payload`, with the payload's **real** mode read
from `os.lstat()`. `payload_ref` kept its shape exactly as the hypothesis
predicted; only its resolution rule changed. The unchanged-check compares the
whole tree rather than `node.md` alone, which is what makes a payload-only edit
a real version — comparing the node file alone would have made every payload
edit invisible to the history this goal exists to accumulate.

**Falsifier, run on the live corpus, not a sandbox:** materialise all 185 build
nodes twice — once from the engine tree, once from the grid — and compare.
**180/180 files byte-identical** (5 nodes are `@v2` chain members resolving to
the same 180 payloads). Modes checked against the engine's own git index:
**180/180 match, including all 16 executables.** The pre-S9 code would have
published every one of those 16 as `100644`. The engine has no symlinks, so
`120000` is covered by the regression tests rather than by the corpus — stated
plainly rather than counted as live evidence.

**The other half — "materialising a chosen version rather than whichever is
current" — is `--grid-version N`**, which reads version N out of the ref's
history instead of its tip and *reports* a node with no such version rather
than quietly serving the tip.

**And it was exercised on content that matters, which is what this goal
actually asked for.** S12's fix and `--grid-version` itself both landed as
payload versions and were published to the engine; the engine repo was never
edited by hand for either. See **G6.1**.

Residual, deliberately not claimed as done: the `@v2` collapse above, and
`stitch.py --verify`, which still compares contracts against the engine tree
rather than against the payload in the ref. Both are named in **G6.1**.

This also settles that the anatomy decision was not overturned by fiat. A grid
ref is never checked out, so it is not a second copy of the tree — it is a second
*name* into the same object store. When bytes match, git's hashing makes them the
same object, which is a stronger non-drift guarantee than "never inlined" was
reaching for.