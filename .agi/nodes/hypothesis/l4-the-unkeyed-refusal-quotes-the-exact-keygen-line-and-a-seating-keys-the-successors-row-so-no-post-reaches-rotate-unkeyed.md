---
id: hypothesis:l4-the-unkeyed-refusal-quotes-the-exact-keygen-line-and-a-seating-keys-the-successors-row-so-no-post-reaches-rotate-unkeyed
mint_id: d17aef66fc7046659b83e624c2740756
type: hypothesis
parents:
  - goal:g6.47
next_edges: []
edited_by: sensei-director
scaffold_hash: 135b98f473cb3174
season: 2
testable_claim: "goal:g6.47 SM.27 (intake: master-sensei 19:15Z, measured on stream-master first rotation 19:13Z at 0.4691: 3 calls paid to the refusal string). MEASURED on season2/main @c40cf5969: rotate.py _caller_post refusal prints `post X is unkeyed: send.py keygen X first` (the site near :15462 / the resolver at :14297+) — `send.py keygen X` is not the grammar (keygen takes --post <seat> / --all-live); my own SM review 00:1xZ printed the same wrong line from this post; seating row writes (SL5.01) already commit session_id/generation/window/pid in one pathspec commit but never a pubkey, so every first seating is unkeyed until the Prime runs keygen --all-live (mine still is, asked 00:1xZ). CLAIM: (1) every refusal that names keygen quotes the exact runnable line `python3 extensions/agi/bin/send.py keygen --post <seat>` — ONE constant used by every site (grep: no other spelling); (2) at seating (cmd_spawn + rotate-self successor row write), when the successor row has no pubkey, the seating mints the key with send.keygen semantics (key file seats/<seat>.key mode 0600 + the row cells pubkey/sig_scheme/enc_scheme) INSIDE the same row write/commit the seating already makes — one write, visible in the same +/- cells; a row that already has a pubkey is untouched (a re-seat never rotates a key; key rotation stays keygen --all-live / the Prime); (3) --dry-run prints `would key <seat>`; (4) the record carries keyed_at_seating: true|false. FALSIFIERS: any keygen refusal spelling that argparse rejects; a seating that rotates an existing key; a second row commit for the key; a key file left mode != 0600. TESTS (test_rotate.py / test_send.py <= 4): refusal string == the constant and parses under send.py argparse (assert parse_args on the quoted tail); spawn on an unkeyed fixture row -> key file 0600 + row pubkey in the seating commit; keyed row -> untouched; dry-run line. FILE SCOPE: rotate.py (refusal constant, seating row write), send.py (expose keygen as a function if not already), the two test files. CEILING: <= 40 production lines, <= 4 tests. Order: after SM.25 (before 20)."
title: the unkeyed refusal quotes the EXACT line (`send.py keygen --post <seat> first`; today it names a grammar argparse rejects — 3 calls on stream-master first rotation), and a seating keys the successor row inside rotate/spawn (the same row write that already carries session_id/window/pid) so no post ever reaches rotate unkeyed (master-sensei 19:15Z)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-unkeyed-refusal-quotes-the-exact-keygen-line-and-a-seating-keys-the-successors-row-so-no-post-reaches-rotate-unkeyed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
second live instance 2026-09-16 10:04Z (master-sensei on director-thought gen1): the post typed send.py keygen director-thought, then keygen --seat, before landing - same class as stream-master 09-13 (3 tries). Priority raised: dispatch right after the Prime-ordered rounds; the refusal prints the exact working line send.py keygen --post <post>.

SM.39 harvest reviewed by sanctuary-master 11:0xZ: ACCEPT bytes (merge to the post branch, 1b976bc33), round verdict inconclusive_lean_proved:80 - mechanism proved by the parent own three probes (auth/gate/wire) and 729 green, parent caught the kid inaccurate self-report (the kid wrote the prod code it claimed pre-existed); demoted because ~90 net lines in rotate.py against a 40-line ceiling (~2.25x) with no re-brief on record. By-name review rides its merge-up.
