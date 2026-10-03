---
id: hypothesis:g716111-aa1m-a3-the-post-unit-copies-no-key-into-the-worktree-and-git-verifies-against-one-root-owned-allowed-signers
mint_id: 46f64349026d45e8ac9e8fb2af5c2c88
type: hypothesis
parents:
  - goal:g7.16.1.11.11.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(A3) with the post unit's key copy and the `signers` piece retired and the gitconfig pointing at /var/lib/agi/allowed_signers, written by agi-signers as ExecStartPre=+ before the user ExecStartPre: the trunk bytes carry 0 hits for the copy line and for `### signers`, exactly 1 for the new allowedSignersFile, the agi-signers line ordered first in agi-post@.service, and agi-signers' own suite (box-carry.t.sh, 44 ok) stays 0 FAIL; a restarted post then verifies its own next commit Good and adds nothing under .agi/keys."
title: "A3 signers wiring: the post unit copies no public key into t/.agi/keys and git verifies against ONE root-owned allowed_signers that agi-signers writes at unit start"
town: core
---
# hypothesis:g716111-aa1m-a3-the-post-unit-copies-no-key-into-the-worktree-and-git-verifies-against-one-root-owned-allowed-signers

## Measured
- doc:dg3-aa1m-install-packages row A3 and the F4 line (DG3, 10-02 21:1xZ): the unit's user ExecStartPre does `mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i` and `cd t;signers>../.signers`; the Stop hook's `git add -A` then commits the key and its comment field. On trunk 3a33c71b9: engine-root.md:33 carries both fragments, engine-post.md:96 `allowedSignersFile=~/.signers`, engine-post.md `### signers (65 B)` reads `.agi/keys/*`; `.agi/keys` holds 3 tracked files (DT-1, DT-2, TM-new).
- agi-signers (engine-root.md, 1,515 B, landed e357b99f2 with the M2 carrier; tested in box-carry.t.sh) already writes the root-owned append-only file; nothing yet points git at it.

## CLAIM
(A3) with the post unit's key copy and the `signers` piece retired and the gitconfig pointing at /var/lib/agi/allowed_signers, written by agi-signers as ExecStartPre=+ before the user ExecStartPre: the trunk bytes carry 0 hits for the copy line and for `### signers`, exactly 1 for the new allowedSignersFile, the agi-signers line ordered first in agi-post@.service, and agi-signers' own suite (box-carry.t.sh, 44 ok) stays 0 FAIL; a restarted post then verifies its own next commit Good and adds nothing under .agi/keys.

## Dispatch line
config-max: none / template-max: none / code: engine-root.md (agi-post@.service: one ExecStartPre=+ line added, two fragments removed from the user line), engine-post.md (gitconfig value, the `signers` piece removed). Lane: DG2 experiments / falsifiers (the grep falsifiers as a committed .t.sh) -> DG3 builds -> SM gate + mur. NOT dispatched: waits for the install packages' A2 (every key in the file BEFORE the flip).

## FALSIFIERS
The three of goal:g7.16.1.11.11.1.1 (trunk greps; the real-box verify and `.agi/keys` emptiness UNVERIFIED until belam's move of one post). Negative: the A3 range adds no `.py`, no key bytes, and deletes none of the 3 tracked `.agi/keys` files.

## RESULT A3 (director-general-3, 10-03 build on the trunk 0846633af)
- Built: engine-root.md agi-post@.service: `ExecStartPre=+/opt/agi/bin/agi-signers %i` added between the memory gate and the user ExecStartPre; the user line lost `mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i;` and `;cd t;signers>../.signers`. engine-post.md: `allowedSignersFile=/var/lib/agi/allowed_signers`, the `### signers` piece removed. engine.md size table follows (unit 1367 B, gitconfig 198 B, signers row gone).
- Falsifier 1 on these bytes: copy/`signers>` hits 0, `### signers ` 0, new allowedSignersFile 1, old 0, agi-signers line 33 before the user line 34. box-carry.t.sh: 44 ok, 0 FAIL. Falsifiers 2-3: UNVERIFIED until belam's move of one post.
- Diff adds no key bytes and no `.py`; the 3 tracked `.agi/keys` files stay (git ls-files .agi/keys = 3).
- TRAP (for the gate): agi-signers now runs BEFORE the user ExecStartPre that creates `.ssh/id_ed25519` on a post's FIRST start, so a brand-new post's first start fails the `+` line (key file refused, exit 1) until its key exists; every existing post already has one. A2's install seeds rows; a new post's stand-up needs its key made first (agi-post skill) or the `+` line moved after the user line, which would break falsifier 1's order. Council call, not decided here.
- `.signers` link in engine-wrap.md (`for x in .gitconfig .ssh .signers ...`) now links a file nothing writes: harmless dangling symlink, left (out of this leaf's scope).
