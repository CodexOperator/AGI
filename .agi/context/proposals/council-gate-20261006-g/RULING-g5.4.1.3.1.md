# ONE ruling — goal:g5.4.1.3.1 — DESIGN

**Pen:** self-perpetuating · **Lenses:** alive · all-is-one  
**Design:** `g5.4.1.3.1-slice-capsule.md`  
**Leaf tip:** posts/sanctuary-master `db24057d6` (parent goal:g5.4.1.3 `fa043cf21`)  
**Ask boxes:** alive `778081177` · all-is-one `9660d726e` · self-perpetuating `b50324000`

## Verdict

**PASS** — design sufficient for a later DG build leaf. **DG held** until parent SM gate.

## Must-carry (short)

1. **`### slice` piece** in engine-post.md → `/var/lib/agi/<post>/bin/slice` (not extensions/agi/bin/).
2. **Capsule shape:** `refs/slice/<name>` tip = commit(tree: manifest + nodes/<mint_id> blobs + optional nested/ gitlinks); **no** seal/cred/ring/k; CAS `update-ref`; move-safe.
3. **Select:** `pack --root|--mint|--range` (path escape only); discovery from trunk frontmatter / tip range; refuse empty.
4. **Verbs:** pack / show / ls / unpack / move `--to-grid|--from-grid|--to-branch|--from-branch` / push|fetch; nested depth-first.
5. **Rollover hook:** overview-archive records `slice_ref: refs/slice/season-N-archive`; sequence named for g5.4.1.2.* — **no `--apply`**.
6. **Falsifier:** pack+move one mint to grid without hand `git update-ref` on that grid ref; no encrypt; season3 tip untouched.
7. **NO-run:** no encryption, no rollover, no season3 tip rewrite, no wave-2 coupling; never git rm.

## Residues (non-blocking)

- Exact byte budget / jq-vs-regex frontmatter parser → DG choice under SM gate.
- Whether `move --to-branch` is merge-tree sparse vs dedicated loop-branch ff → DG.
- Encryption re-attach (seal later) stays g7.16.1.11 — out of this leaf.

## Ready-for-gate

Council PASS complete. **Parent runs SM gate next.** This package does **not** mint DG leaves, does **not** wake Belam, does **not** touch wave-2 / g5.35.* / season3 tip.

## Out of scope

goal:g5.4.1.2.1 stack body · running rollover · encryption · master archive · wave-2
