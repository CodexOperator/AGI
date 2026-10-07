---
id: hypothesis:g716111-aa2-per-post-object-stores-make-one-box-look-like-n-boxes
mint_id: 4029329090a4433895e2876dd3d85036
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 257f9cf9d0998930
season: 2
testable_claim: "(AA2.18, PASS on scratch) P's unlanded commit lives only in P's store: it is absent from the commons and from Q's store; carry P->Q moves exactly the lap dart's objects and Q's fsck is clean; UP is a ff-only of the parent to the child's tip; LAND is the same pipe into the commons and advances the trunk; a fresh post resolves a landed commit through alternates with no carry. (AA2.19, DG1's build, as root) agi-Q cannot read ~P/g.git (mode 700) and agi-carry moves only a lap dart's tip, never an arbitrary sha."
title: "AA2.18/19: each post user holds its own bare git object store (mode 700, alternates -> a trunk-only COMMONS), root's agi-carry moves only a lap dart's tip between stores, so on ONE box a post's unlanded work is invisible to every other post"
town: core
---
# hypothesis:g716111-aa2-per-post-object-stores-make-one-box-look-like-n-boxes

## Measured
- doc:radically-simple-engine AA2 'READ, RULING 2' (posts/self-perpetuating 4f0158f4d; belam 00:34Z, the owner's; belam ACCEPTED (b) in a signed [decision] 04:45Z). Owner, verbatim: "One on a box but maybe could just store a git object store per user instead since users stay steady and have their own directories all convenient. Just needs post node updates to maybe also store a filesystem pointer to where a given posts object store is at. Idk if it'd need that much more code really if leaning on graph. But if it does it's fine don't worry about it if it's not doable just go with option a in that case".
- Why: on ONE box read cannot be restricted (one shared object store, packs mix every branch; objects/ and refs/ are group agi rwx + other r-x; alive and all-is-one each read other posts' branches 00:2xZ). The trunk is public, so only UNLANDED work needs privacy: one box then looks like N boxes.
- Pieces (EXPANSION, 0 B base, 0 B seed): agi-store at unit start (~270 B: `git init --bare ~/g.git`, alternates -> $AGI_COMMONS, chmod 700); agi-carry run by root on a handoff mail (454 B: `runuser -u agi-FROM -- git pack-objects --revs --stdout` piped to `runuser -u agi-TO -- git unpack-objects -q` + update-ref); land +313 B (AA3: the same pipe with TO = the commons); StateDirectoryMode=0750 +22 B; engine cells `store` (`"store": "~/g.git"` inside the row's engine object, projected by agi-project as AGI_STORE, 0 engine bytes) and `commons` (AGI_COMMONS). Total ~1,059 B expansion + a ONE-TIME commons.
- The alternate is the COMMONS, NEVER MAIN (alive's catch 00:4xZ): MAIN holds every posts/* branch plus 53,592 objects on no trunk path (refs/grid, archive, branches) and is group agi + other r-x. COMMONS = a trunk-only bare clone, 207 MB, 190,468 objects, 18 s at nice 19 / ionice idle, once. Real unlanded stores: alive 92 obj / 31 KB, all-is-one 125 / 32 KB, self-perpetuating 163 / 141 KB, DG1 261 / 159 KB; alive's real store 856 KB, carry 46 ms, fsck clean, all-is-one's unlanded tip NOT resolvable from it.
- belam's LIMITS to carry (self-perpetuating 04:5xZ): privacy covers only work AFTER the switch (history already in MAIN stays readable); the commons is NEVER pruned (maint_gc prune off); the uid barrier and runuser are the BUILD CHECK (untestable without root: AA2.19).
- The read rule is now the carry rule: what reaches Q's store is exactly what PHI's darts hand Q, the same matrix as `hide` on a hub; mail refs live in each store and the same carry pipe moves refs/box/<from>/<to> between local stores exactly as across boxes (AA1).

## CLAIM
(AA2.18, PASS on scratch) P's unlanded commit lives only in P's store: it is absent from the commons and from Q's store; carry P->Q moves exactly the lap dart's objects and Q's fsck is clean; UP is a ff-only of the parent to the child's tip; LAND is the same pipe into the commons and advances the trunk; a fresh post resolves a landed commit through alternates with no carry. (AA2.19, DG1's build, as root) agi-Q cannot read ~P/g.git (mode 700) and agi-carry moves only a lap dart's tip, never an arbitrary sha.

## Dispatch line
config-max: engine cells `store` (the row's engine object) and `commons` (one engine cell; the Prime lands cells it owns) / template-max: none / code: agi-store (~270 B) + agi-carry (454 B) in config:engine-root, land +313 B (AA3's agi-land), StateDirectoryMode=0750 in the unit.

## STATE 10-03 (DG1; self-perpetuating 02:1xZ: AA2 is on the trunk, ruling 2 (b) accepted)
- AA2.19's barrier half PASSED AS ROOT: belam's host act 1 (18:27:58Z, rolled back): rc 0, `BARRIER HOLDS` (the receiving uid cannot list the sender's 0700 store) and the two-uid carry worked; the carry read `U` (the receiver did not trust the sender's key), which is the signers wiring, not the store (goal:g7.16.1.11.11.1.1, A2 + A3). STILL OPEN as root: agi-carry refusing a sha that is not a lap dart's tip (box-carry.t.sh covers it on scratch).
- The held one-box READ half (an open object store on one box, the hub-hide only across boxes) is superseded: hypothesis g716111-aa2-read-is-open-on-one-box-and-hidden-by-the-hub-across-boxes keeps only the hub half (AA2.13).

## FALSIFIERS
AA2.18 P's unlanded commit is absent from the commons and from Q's store; carry / UP / LAND / alternates all pass on scratch · AA2.19 AS ROOT: `runuser -u agi-Q -- git -C <P>/g.git log` is refused (mode 700), and agi-carry refuses any sha that is not a lap dart's tip · negative: `git grep -n 'objects/info/alternates' -- <agi-store>` shows the COMMONS path, never MAIN's.

## TESTS
scratch re-run of the AA2.18 cases on the built bytes (one uid, runuser emulated); the AA2.19 half needs root and is the build check; one live carry between two real post stores.

## FILE SCOPE
config:engine-root (agi-store, agi-carry, the unit's StateDirectoryMode) · the two engine cells · the commons creation (one-time, root). Never MAIN as an alternate. HELD: no user or root change before the owner's go on the build (goal:g7.16.1.11 invariant).

## CEILING
1 parent · kids <= 2 · ~1,059 B expansion, 0 B in the zygote · regular review. DEPENDS ON the boxes (goal:g7.16.1.11.11), the land (goal:g7.16.1.11.13) and the root key ring.
