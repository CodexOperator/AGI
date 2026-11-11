---
id: goal:g7.16.1.11.46.19
mint_id: 5a3a9adce1414b9f98621180e7263f11
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.19
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - V1
season: 3
status: horizon
title: "G7.16.1.11.46.19: V1 -- refs/id/<mint> per post and kid: a piece tree and a continuity signature chain to a pinned root signer, `id check`, a mint column on config:posts; the M6 store moves to the mint path in the same land"
town: local-maxxing
---
# goal:g7.16.1.11.46.19

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §9, §27. K5: the doc names the genesis (§9: 'v1 is signed by the spawner'; check (3): the birth link is signed by the parent post), so the top of the spawn tree is ONE root signer pinned on the trunk (sp 3). Dependency from goal:g7.16.1.11.46.13's THOUGHT: the M6 store key is ${AGI_MINT:-$AGI_POST}, so the leaf that adds the mint cell moves the store IN THE SAME LAND. Box reading: refs/id/* = 0 today.

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.19 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 2.3 | "identity = composable key over signed pieces, re-hashed on swap, continuity = the history" | target:§9 · decision:§21 #1 |
| 3.5 | "mint id per post and kid; inherit director's slot; different login" | target:§27 |
| 2.2 | rest: the capsule in refs/id + slot (from goal:g7.16.1.11.46.20's close 11-09) | target line 1 (the piece set: slot); V1b |
| 2.25 | the cred piece; the second subscription is an owner act (from goal:g7.16.1.11.46.20's close 11-09) | target line 1 (the piece set: cred, riding its piece tree, never a config:posts column); V1b |

## Target end-state
- Every post and kid has refs/id/<mint>: a commit per identity version whose tree is the piece set (key.pub role harness model brief card perms slot cred), signed by the previous link's key; the birth link is signed by the spawner; the top of the spawn tree is ONE root signer in the trunk's allowed-signers with valid-after.
- `id check` (~20 lines, ckpt's walker) walks a chain and names the first bad link.
- config:posts carries a `mint` column; a rename is a one-line address change.
- The M6 store lives at ~/.mem/<mint>.git (moved, same tip), in the same land as the mint column.

## Invariants
- A post is alive iff its chain is unbroken to its birth and its tip's piece set passes the row's allowed piece types (§9).
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/id-chain.t.sh` exits 0: a swap of every piece but slot passes; a link signed by a foreign key fails by name; a self-signed birth link (unlisted key) fails by name.
2. After the land, per post: ~/.mem/<post>.git is absent, ~/.mem/<mint>.git has the SAME tip sha as the old store, and `mem: tapped k/m` is unchanged; mutant: a store left at the post path reads RED.
3. Negative: `git for-each-ref refs/id/` lists one chain per config:posts row with boot true; a row without a mint prints its name, rc 1.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 11-11 (HORIZON, SM's placement 11:22Z on my V1 read): status active -> horizon = PARKED, not abandoned; unpark = belam's word (one line to SM; silence keeps the park). Read on the trunk b1827471c5: F1 MET (sh extensions/agi/tests/id-chain.t.sh = 'id-chain: 0 FAIL', rc 0: V1a, the id walker and its rows and mutants). F2 NOT MET: no M6 store has moved to ~/.mem/<mint>.git. F3 NOT MET: git for-each-ref refs/id/ lists 0 chains and config:posts has no mint column. The remainder is V1b, whole: the mint column, AGI_MINT exported to the units, the ~/.mem store moves (all three in ONE land, council 3/3 21:44:14Z 10-31), a live chain per boot-true row, and the root key pinned in .geometry/id-root (a RULES path), each behind belam's host act. The OWNER atoms table gains 2.2 (rest) and 2.25 from .46.20's close (sp 12:41Z + 12:44Z 11-09); 2.25's cell rides the cred piece's tree, not a config:posts column. The text below is the earlier versions, kept as written.
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
director-general-2 10-31 (V1a, the no-live-key half, per my [proposal] 14:1xZ 10-31 C, AMENDED by my [note] 21:39:08Z 10-31): V1a = the `id` piece (engine-grow.md, beside ckpt: `id check refs/id/<mint> [allowed-signers]`, the walker of target line 2) + id-chain.t.sh = F1 as worded (a swap of every piece but slot passes; a foreign-key link fails by name; a self-signed birth with an unlisted key fails by name), sharpened with rows the target implies: a slot change is a new identity (target: 'the piece set ... slot'), a path that is no piece, no key.pub, a birth before the root's valid-after, an unread ref or root file (`id: unread`, rc 1, the invariant), a three-link chain and its grandparent-key forgery; mutants m1-m4. NOT in V1a: the mint column, AGI_MINT exported to the units, and the store move. Reason (this node's 'Why'): the M6 store key is ${AGI_MINT:-$AGI_POST}, so an AGI_MINT exported before each ~/.mem store moves would point every post's tap and brief at an empty ~/.mem/<mint>.git; the leaf already says the mint cell moves the store IN THE SAME LAND. So F2 + F3 + the live chains + the root key pinned in .geometry/id-root are V1b, behind belam's host act. The root signer file the piece reads by default (.geometry/id-root) does not exist on the trunk until V1b: `id check` without a root argument prints `id: unread root signers ...`, rc 1, today (fails closed). The council AGREED the narrowing 3/3 (alive [decision] 21:44:14Z 10-31), with two reads named here (words only): (a) the reach of an early AGI_MINT is ONE post today: one config:posts row carries a mem cell (belam, full), and agi-mem's gate exits 0 for every other row on every verb but cite; AGI_MINT has one reader (agi-mem's store key S), and agi-project composes AGI_<KEY> from the engine cell's keys, so a mint engine cell IS the export; (b) aio's add: cite is that exception, and verify-land.sh runs `agi-mem cite` on the LAND tree with AGI_POST=belam and holds the land on its rc, so an AGI_MINT that reached that call would key the land's owner-cite on the same empty store: tap, at, view AND cite would all read ~/.mem/<mint>.git. UNMEASURED: whether an exported AGI_MINT reaches verify-land's environment; the narrowing removes the case either way. RE-CUT 1 (alive [decision] 22:02:20Z 10-31, terms (1)-(4) pre-approved): (1) every tree entry of a link must be a PLAIN FILE (git ls-tree mode 100644, type blob; a tree, symlink, submodule or executable entry is BAD by name), and key.pub must be a blob; (2) the signature backend is PINNED to ssh: the commit HEADER (to the first blank line) must hold EXACTLY ONE line starting 'gpgsig', equal to 'gpgsig -----BEGIN SSH SIGNATURE-----', before verify-commit runs (RE-CUT 2, alive [decision] 22:18:14Z: a whole-object grep passed a PGP link whose MESSAGE held the SSH line, k2c; an any-line header grep passed a PGP link with a SECOND gpgsig header line, k2d), so an OpenPGP link fails by name whatever keyring the verifier holds; that header is SHA-1's: a SHA-256 repo writes 'gpgsig-sha256', which this check reads as BAD (the check assumes the SHA-1 object format the trunk uses); (3) the piece is NAMED agi-id, not id, against this leaf's words 'id check': /usr/bin/id is on every PATH and agi-gate's root drop calls 'id -u', so a piece installed as id would shadow it (sp measured id -u rc 2 under the shadow); the leaf's 'id check' reads 'agi-id check'; (4) an EMPTY root file reads 'id: unread root signers', rc 1, never a BAD birth. Rows k0, k5b, k6b, k2b, k8c with mutants m5-m7 and the k0 name check. RE-CUT 2 also: (5) a name must equal EXACTLY ONE word of AGI_ID_PIECES, read untrimmed from ls-tree's tab (a substring test passed 'brief card'; 'role ' with its space is bad), rows k5c + k5d, mutant m10; (1) k6b's own mutant m5b (the mode test cut AND key.pub back to cat-file -e reads the directory key.pub ok).
<!-- THOUGHT:END -->
