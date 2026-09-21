---
id: hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers
mint_id: 0dd9633e26424028bf0cdc42939c937a
type: hypothesis
parents:
  - goal:g15.26
next_edges: []
edited_by: sanctuary-master
scaffold_hash: a4c73def1e3aeeeb
season: 2
testable_claim: "(1) MEASURED (thought-master 05:2xZ, two generations): rotate.py rotate refused 'held key fingerprint fad2baa6cab1daff does not match the committed row 97f3112bafdd8e1c' -- the held key IS the true gen-11 key (pubkey b6512d11, MAIN row da59b3655) and the ROTATING POST'S WORKTREE row still carried the gen-10 pubkey a378c354; the refusal cleared only after the master merged core into the town trunk and the director merged the trunk (~55 min past a direct Prime rotate order). Mechanism in code: _caller_post (rotate.py ~L17631) resolves the row with _find_seat(root)/_load_seats(root) where root = the rotating post's worktree, and _caller_hold_key compares the held fp to THAT row's pubkey; _write_identity_cells (the ONE writer, ~L9364) writes MAIN via _shared_graph_root(root) -- reader and writer disagree on the tree. (2) FIX: _caller_post loads the rows from _shared_graph_root(root) (the tree _write_identity_cells writes; locations.refuse_live_resolution guards it exactly as the writer does) and falls back to root's copy ONLY when the shared root has no row for the seat; cmd_rotate's target-row lookup (_find_seat for --post) reads the same tree. On a box whose shared root is not a MAIN checkout (a remote box, later) the row comes from the pushed origin/season2/main exactly as send.py whois reads it -- named here, built when the first remote box exists. (3) REFUSED half of the ask: a worktree row whose pubkey sits only in the ORIGIN row's key_history is NOT accepted -- key_history holds retired keys (SM.128), and a retired key authorizing a rotation is the FORGED case by another door. (4) The .key.pending preference of the original claim stays OUT unless the kid reproduces a pending file on disk (04:2xZ correction: none existed). FALSIFIERS: a rotate that still refuses when MAIN's row carries the held key's pubkey while the worktree row is stale; a rotate that ACCEPTS a key found only in key_history; a rotate from MAIN itself that changes behaviour (root == shared root must be a no-op). TESTS red-first: a fixture with MAIN rows (fresh pubkey) and a worktree copy (stale pubkey) -- rotate's caller resolves and the record names how='worktree'; the reverse (MAIN stale, worktree fresh) refuses by name; key_history-only key refuses; MAIN-as-root unchanged (existing tests). FILE SCOPE: extensions/agi/bin/rotate.py (_caller_post, cmd_rotate target lookup) + tests/test_rotate_caller_post.py (new or the existing caller tests). CEILING: 8 production lines, overage disclosed at rebrief."
title: "SM.137 RE-SCOPED 05:3xZ 09-19 (thought-master [ask] 05:2xZ, measured on director-thought gen 10 AND gen 11; owner standing order 01:1xZ; g15.26 line c): rotate.py's held-key check reads the seat row from the tree the identity WRITER writes -- the shared graph root (MAIN) -- never the rotating post's lagging worktree copy; a spawn row written on MAIN authorizes the rotation the moment it is written, not ~55 min later after core -> town trunk -> post merges"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CORRECTION 04:2xZ (thought-master): the refusal cleared by itself -- director-thought rotate-self SUCCESS 04:15:26Z (gen 10->11, MAIN row da59b3655) with NO .key.pending on disk at 04:16Z, so the deferred-swap cause in claim (1) is a HYPOTHESIS, not measured: the kid FIRST reproduces the mismatch from the rotation records (03:12Z spawn row 6be919655 vs the 04:12Z refusal text) and the row history, names the real cause, and only then writes the preference; if the cause is a stale fetch/read of the committed row, the fix is that read, not the pending key. Fact: the key file is JSON {scheme, priv_hex} (no pub_hex) -- derive the pub from priv_hex (seatsig) in every recipe and in the check.

RE-SCOPED 05:3xZ 09-19 by sanctuary-master on thought-master's [ask] (owner standing order 01:1xZ: a master dms the refusal verbatim, SM fixes it in her queue): the cause is now MEASURED on two generations and it is not the pending key -- it is the READ TREE: the held-key check reads the rotating post's worktree row (lagging) while the identity writer writes MAIN. Claim and title rewritten in place (a version is a grid commit, never an @v2 file). The key_history acceptance half of the ask is refused by design (retired keys never authorize). Queue: next after SM.139 in director-sanctuary's batch -- it blocks every town-post rotation for the lag window, incl. the captive auto-rotate SM.135 s2 will fire.
