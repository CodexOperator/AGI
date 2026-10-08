---
id: hyp:payload-in-node
mint_id: f2b6e00657e94e01814df19b704d1f5e
type: hypothesis
parents:
  - goal:g6.3
confidence: 0.65
edited_by: season.py
season: 1
subgraph: false
tags:
  - g6.3
  - level3
  - stitch
thought_session: season
title: "G6.3's payload model: resolve against the node's own grid ref, not a disk path"
---
**Hypothesis:** G6.3's falsifier becomes passable if `payload_ref` resolution
changes from "a repo-relative path into the live engine tree" to "the payload
blob recorded at the current tip of `refs/grid/node/<id>`" — the node's own D2
version ref, which `grid.py` already writes on every `grid commit` via plumbing
(`hash-object` → `mktree` → `commit-tree` → `update-ref`,
`extensions/agi/bin/grid.py:1-33`). Concretely: a `grid commit` against a
level-3 node's ref folds the payload's bytes into that ref's tree alongside the
node's frontmatter/contract, so the ref's own commit history *is* v1 → v2 → v3
of the file, and `stitch.py --out` gains a second resolution mode that reads
`git cat-file -p refs/grid/node/<id>:<payload-path>` instead of reading
`extensions/agi/<payload_ref>` off disk. Editing a node then means: commit new
payload bytes to its grid ref. Stitching a chosen version then means: point
`--out` at a specific commit in that ref's history, not "whichever is current"
— which is the exact language G6.3 uses (`GOALS.md:569-571`) to describe the
untested case.

**What would prove it:** Take one real level-3 node (e.g. `build:bin-grid`,
`payload_ref: extensions/agi/bin/grid.py`). Change only its payload content,
`grid.py commit` that change against `refs/grid/node/build:bin-grid` (minting
v(n+1) the normal D2 way — no new command). Run a grid-resolving `stitch.py
--out DIR` that reads the payload from that ref's tip instead of the engine
repo path, then `sha256sum DIR/extensions/agi/bin/grid.py` and compare against
the sha256 of the same file produced by editing it directly in the engine repo
the old way. Byte-identical (matching sha256) across >=2 real files and >=3
version bumps each (v1→v2→v3, per G6.3's own bar) passes. Do this for a second
file whose payload includes something a plain path-copy would not need to
reconstruct correctly (e.g. a file containing non-ASCII bytes or an executable
bit) to check the model isn't silently lossy on the cases `cp -r` handles for
free today.

**What would disprove it:** Any case where the grid-resolving `--out` still has
to fall back to reading the engine-repo disk path to reconstruct the file
correctly (permission bits, symlinks, anything `mktree`/`cat-file` can't carry
that a plain copy can) — that would mean the node is decorative, not
authoritative, exactly the gap this hypothesis claims to close. Also
disproved if two level-3 nodes must ever produce byte-identical payloads (the
`duplicate_payload_ref` case `stitch.py` already flags, `stitch.py:39-44`) and
the grid encoding has no way to assert "these two refs' payload blobs are the
same object" — that would let the graph and the tree drift silently in exactly
the way `stale_contracts` already worries about for contracts.

---

**Three models, weighed:**

**1. Inline body.** Node body carries the file's content verbatim, inside a
fenced block next to the contract. Loses outright: `hyp:level3-node-anatomy`
and both `stitch.py`'s and `level3.py`'s module docstrings say, in three
independent places, that source "lives on disk exactly once — never inlined
into the node" (`level3.py:12-13`, `stitch.py:18-19`). Inlining isn't a
refinement of that design, it's the thing it was written to rule out. Concrete
costs beyond re-litigating the anatomy node: a `bin/*.py` file's content sitting
inside a markdown fence needs escaping (a source file that itself contains a
` ``` ` fence, or the harness-owned `BUILD-CONTRACT` markers, breaks the
node's own parser); every code edit now diffs twice — once as the real file
change, once as an unrelated-looking prose diff in a `.md` file — which is
worse for review than the status quo, not better, and directly works against
G6's invariant that "an engine change is reviewable as node → verdict →
commit." It also silently reintroduces the frontmatter-growth problem the
anatomy node fought to keep at zero, just moved into the body instead of the
frontmatter keys.

**2. Content-addressed blob ref.** Frontmatter carries a git blob sha
(`payload_blob: <sha>`); the object lives once in the shared store, same as
grid already deduplicates by construction (`grid.py:14-16`: "a node version
whose content is also committed on D1 is the same blob... costs almost
nothing"). This is closer to right than inlining, but it loses to model 3 on
authoring mechanics, not on storage: nothing today lets an agent "edit
frontmatter to point at a new blob" as a single act. The blob has to exist
*before* the sha can be written, which means the actual edit is a two-step,
out-of-band sequence — write the new content somewhere, `git hash-object -w`
it, then hand-edit the sha string into the node file — none of which is
expressible as "here is my node edit" the way every other node write in this
graph is. It also throws away reviewability: a frontmatter diff of
`payload_blob: a3f9e2c... -> 7b1d40f...` shows that something changed and
nothing about what, whereas `grid.py diff NODE_ID` already renders a real
diff for D2 today (`grid.py` usage block) — model 2 would need to reimplement
that machinery a second time under a different field name instead of reusing
what `grid commit`/`grid diff` already do.

**3. Grid-ref payload — picked.** The payload is whatever
`refs/grid/node/<id>` currently points at; `payload_ref` stays a pointer, but
what it points at is a *version* (a commit in that ref's own history), not a
path in the engine repo. This wins for three concrete reasons, not by
default:

- **Zero new frontmatter.** `hyp:level3-node-anatomy`'s hard constraint —
  "I add zero new frontmatter keys" — holds exactly. `payload_ref` keeps its
  existing shape (a path string); only its *resolution rule* changes, from
  "read this path off `--engine-root` disk" to "read this path from
  `refs/grid/node/<id>`'s tree." No sha field, no new markers.
- **Versioning and reviewability come for free from infrastructure that
  already exists and is already exercised.** `grid commit`, `grid log`,
  `grid diff`, `grid status` are real, working D2 machinery
  (`grid.py:1-33`); this model asks them to carry payload bytes in the same
  tree they already carry the node file in, not a parallel system. v1 → v2 →
  v3 is literally `grid log NODE_ID`'s output — the exact accumulation G6.3
  says has never been tested (`GOALS.md:568-571`).
- **It composes directly with G6.7's D4 without a translation step.** G6.7
  describes a release ref built by `mktree`-ing "each build node's payload"
  directly (`GOALS.md:671-672`), and says outright that the fork is "whether
  a node holds its payload or points at it" and that this is G6.3
  (`GOALS.md:683-684`). If the payload already lives as a blob inside
  `refs/grid/node/<id>`'s tree, D4 is a tree-merge over existing refs — no
  markdown to parse (unlike model 1) and no per-node sha lookups to resolve
  first (unlike model 2). If G6.3 picks model 1 or 2, G6.7 has to invent its
  own extraction step before it can even start; model 3 is the only one of
  the three that hands G6.7 exactly the input it says it wants.

It is also **not** a re-litigation of `hyp:level3-node-anatomy` by fiat: the
anatomy node's real claim is that source should not live *inlined in the node
body / working tree, duplicated and driftable*. A grid ref is never checked
out and never appears in `git branch` (`grid.py:12`) — it is not a second
copy of the working tree, it is a second *name* into the same
content-addressable object store the engine repo's own D1 history already
uses. When the bytes match, git's own hashing guarantees they are the *same*
object, not a copy that merely ought to match — which is a strictly stronger
non-drift guarantee than "never inlined" was reaching for, not a violation of
it. So this hypothesis extends the anatomy node's mechanism (content-addressed
storage) into the one place it hadn't yet been applied (the payload) rather
than overturning its stated design.

**Where I'm not confident (why 0.65, not higher):** `stitch.py --verify`'s
`missing_payload`/`orphan_files`/`duplicate_payload_ref` checks are all
written against a disk-path world (`shutil`, `Path.exists()`,
`stitch.py:120`-area imports); making them grid-aware is real, unwritten work,
not a formality — and until someone writes the grid-resolving `--out` this
falsifier calls for, this is a design choice, not a verified result. The
disproof conditions above (permission bits, symlinks, cross-node payload
identity) are the concrete edges I'd expect to break first.