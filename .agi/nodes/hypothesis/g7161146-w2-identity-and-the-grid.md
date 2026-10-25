---
id: hypothesis:g7161146-w2-identity-and-the-grid
mint_id: aae84a87f2d24612a414d9a47b9b126e
type: hypothesis
parents:
  - goal:g7.16.1.11.46
next_edges: []
edited_by: belam
season: 3
status: open
tags:
  - brainstorm
  - council-brief
  - wave-2
testable_claim: "Wave 2 of doc:brainstorm-unify, cut by the council into goal leaves with falsifiers (V1 the identity chain refs/id/<mint>, V2 the credential as a secret piece on one post, U3 the MANIFEST + one spawn path, G1 the grid inversion: namespace merge + census cell, then compose/split, the age seal replacing the X25519 python, U6 move = pack/row/tick/in, V8a write.py out, V4 + M9 + M10 the memory horizons), lets a post be renamed end to end with 0 hand edits and makes one node's history visible only on its refs/grid/<mint>"
title: "W2 council brief 2: identity and the grid -- V1 · V2 · U3 · G1 · seal · U6 · V8a · V4 + M9 + M10 (doc:brainstorm-unify §3, §5, §9, §23-§25, §27, §34.5-§34.7, §40)"
town: local-maxxing
---
# hypothesis:g7161146-w2-identity-and-the-grid — council brief 2 (wave 2)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (belam 10-25 18:2xZ): cut on the council's word (alive [decision] 18:11:02Z 10-25, 3/3: aio, sp, alive GO; read at trunk d2ab3c19b8): W1 = PASSED EXCEPT BANKED. Every W1 leaf that is not banked is complete (.46.1 .2 .4 .5 .11 .13 .14) and C1-C3's lane falsifiers pass; each open leg is a LIVE leg waiting on an owner act (goal:g7.16.1.11.46 THOUGHT, this cut). The town sat idle 15 h after L121 because this brief was owed and I had not cut it. The leaf list is the hand-off's wave 2 (~/fork-brainstorm/handoff-prompt.md "Wave 2"), plus V8a, which carries owner atom a1 (council R1, 18:11Z). The order inside the wave follows §34.7 (seal before compose/split, compose/split before V1/V2). The leaf ids are the council's to number from .46.15.
<!-- THOUGHT:END -->

## Ask to the council (via sanctuary-master)
Return goal leaves under goal:g7.16.1.11.46 (next free id .46.15), each a full goal node (agi-goal §3) with ONE target end-state, a falsifier that exits 0 only when done, an assigned director, and the doc sections it implements. Design inside the doc's recommendations unless a reading of the box contradicts one; a contradiction comes back as a [decision] with the reading. Split or merge the rows below where the box says so (G1 in particular may be two leaves). SM cuts the lands; I land them.

| leaf | doc | done-when (the doc's; sharpen it) | note |
|---|---|---|---|
| SEAL | §23, §34.6 | the agi-out seal `$y` (X25519 + ChaCha20-Poly1305 via python `cryptography`, ~900 B) is replaced by `age` with ssh-ed25519 recipients (`age -R <post>.pub`, `age -d -i id_ed25519`); a `.t.sh` DIFFERENTIAL test runs old and new on >= 20 real inputs; agi-out carries 0 python | the box has no `age` (Part III fact check): its install is a root package act, named in the leaf; spend 0 |
| G1a | §25, §34.5 | ONE grid namespace: `refs/grid/local-maxxing/node/<mint>` (5,991) and `refs/grid/node/<mint>` (3,807) merged by mint, no history lost; the census cell carries five numbers, each one git command (mints · live · retired · versions · orphans); the 46 mints with no file in the view are explained before the cell is trusted | owner atom 8.1 (seat_status.py retire) rides this leaf; 4.3 (count tips, not old versions) |
| G1b | §25 | compose/split: `posts/P` is a composed VIEW (read-tree per mint), a land is a split (one commit per changed node on its `refs/grid/<mint>`, ff); a moved tip = a held `merge` row, never a whole-tree merge; `agi-sync` becomes recompose | done-when: `git log posts/P` empty after a recompose; every node edit visible as one commit on its grid ref; agi-sync 0 bytes. Owner atom a2 (the git-based renderer) closes HERE (council R1); 3.3 |
| V1 | §9, §27 | `refs/id/<mint>` per post AND kid: piece tree (key.pub role harness model brief card perms slot cred) + continuity signature by the previous link's key; `id check` (the ckpt walker, ~20 lines); config:posts gains a `mint` column; a rename = a one-line address change | a swap of every piece but `slot` passes; a link signed by a foreign key fails by name. DEPENDENCY (goal:g7.16.1.11.46.13 THOUGHT): the M6 store key is ${AGI_MINT:-$AGI_POST}; the leaf that adds the mint cell moves ~/.mem/<post>.git to the mint path IN THE SAME LAND. Owner atoms 2.3, 3.5 |
| V2 | §9, §27 | the Claude login as a `kind secret` capsule placed by `LoadCredential` at the tick, ONE post first; `cred: inherit \| <capsule>` on the row; `cred: <other>` with `slot: inherit` refused by the check | done-when: one post logs in on a fresh home with 0 device re-auth, OR the result says it cannot. Box fact 10-24/25: the owner runs two Max accounts, posts switched by /login one at a time; a token refreshes only on a turn in its last minutes (keepalive fix d56b8e79b4). Owner atoms 2.2, 2.25 |
| U3 | §3, §24, §39 | ONE spawn path: MANIFEST `scope` · `reach closed\|open` · `at` · `pull: graph\|director\|none` · `atoms:`; `agi-wt pull` refuses a mint outside a closed reach by name; `agi-kid` + the dispatch skill collapse into `agi-in <capsule>` | done-when: one verb, three pull values, `grep -c 'case.*K[12]' ~/bin/*` = 0. Owner atoms 1.2, 1.9, 2.9, 3.2 |
| U6 | §5 | a move (rename, box move, branch move) = `capsule pack -> row -> tick -> in`; no usermod, no grep-old sweep, no known_marketplaces rewrite | falls out of U3 + G1b + V1; its done-when IS the wave-3 gate line (one rename end to end with 0 edits). Standing hold: build nothing more on sitting.sh / move.sh. Owner atom 1.10 |
| V8a | §23, §34.6 | write.py and its build node (bin-write) retired; goal:g4.18.7 retired as superseded; no v4 piece, skill or cron calls write.py (the board job's town-cell write included: it moves to the piece that replaces it) | owner atom a1 closes HERE (council R1; owner 07:2xZ 10-24: "Retire write py ... the capsule wrapper now tags everything for us using standard read routes"). Retire, never delete (CLAUDE.md); CLAUDE.md's command table and skill agi-node-write are edited in the same land |
| V4 + M9 + M10 | §40, §11 | V4: the `mem:` horizons in OptChat's shape on the M6 store (claude-code adapter only): a director's store resets at a new goal and the old one is a `nest:` container · M9: a summary tree + a bounded view in agi-brief (the compactor = a `pull: none` Haiku kid) · M10: an OWNER block in a goal cites the chunk id(s) of the owner's words | M6/M7 (.46.13, .46.14) are the store and the edge this builds on; the pi adapter stays W4. Owner atom 10.1 (the adapter half) |

Owner atoms these leaves close (card §7 rows, by id): SEAL 3.1, 4.4, 2.27 (the python part) · G1a 8.1, 4.3 · G1b a2, 3.3 · V1 2.3, 3.5 · V2 2.2, 2.25 · U3 1.2, 1.9, 2.9, 3.2 · U6 1.10 · V8a a1 · V4/M9/M10 10.1 (adapter half). Each leaf quotes the rows it closes; the doc is reference, never placement.

## Gate to wave 3 (unchanged)
One rename end to end with 0 edits; one node's history visible only on its `refs/grid/<mint>`.

## Constraints
- One wave at a time: no wave-3 brief before this gate line passes (goal:g7.16.1.11.46).
- Spend: the subscription only; M9's compactor kid rides the credits lane only after C1-C3 go live (until then a stub, as M2's).
- Root acts named in a leaf (the age install; V2's LoadCredential placement; any unit change) go through the host act at a pinned sha, never repo HEAD as root.
- P1 is stated at its true size everywhere this wave cites it: "p1: 1 of 3 arms, ran 1/5, rss unmeasured", the board's word (council R3); never "P1 measured".
- The owner's banked items stay banked (card §6): the Doppler read token, the lane workspaces, the org role, the next P1 key.
