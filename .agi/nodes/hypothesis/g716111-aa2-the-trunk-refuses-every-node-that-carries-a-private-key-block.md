---
id: hypothesis:g716111-aa2-the-trunk-refuses-every-node-that-carries-a-private-key-block
mint_id: c95fafe9752e4332a8c503acfc80f745
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) a commit that ADDS or CHANGES ANY path (a node, a script, a payload, a binary; a merge commit included) whose bytes hold a private key block (a line matching BEGIN, any label of capitals, digits and spaces, then PRIVATE KEY, in five dashes: OPENSSH, RSA, EC, DSA, PKCS8, ENCRYPTED, bare) is refused by grow-gate, whatever the ring says; (b) the refusal names the file and never prints the key; (c) no key is parsed (no ssh-keygen), so a passphrase-encrypted block REFUSES inside a timeout and never hangs the gate; (d) a node with no such armour, or one that names a PUBLIC key, an SSH signature block, or the words private key without the dashed BEGIN line, lands exactly as today."
title: "AA2: the trunk refuses every commit that carries a private key block in any path it adds or changes (alive's pattern pinned per commit by all-is-one, 283 B in grow-gate; a publication lives only on refs/revoked)"
town: core
---
# hypothesis:g716111-aa2-the-trunk-refuses-every-node-that-carries-a-private-key-block

## Measured
- alive 03:13Z (read-only): NO landing gate looks for private keys in node bytes today. anonymize's classes are hostname, ip, mac, board, secret, home, email, hardware; its secret class reads .env values, not key blocks. An ACCIDENTAL leak of a live key passes.
- belam 03:2xZ, counts only: 0 private key blocks in the tree, 0 on origin/local-maxxing/season2/main, 0 commits on any origin/* ref ever adding one.
- alive 03:1xZ (GitHub API, no token): origin is PUBLIC-READABLE, and the trunk is pushed hourly to it, so a key on the trunk is world-public at the push.
- THE LINE HAS CHANGED THREE TIMES; BUILD FROM THE LAST. (1) 03:13Z 490 B ring-lookup line (belam accepted it) was WRONG on three fixtures: it passed an RSA PEM block, passed a live key placed after a retired one, and HUNG on a passphrase-encrypted OpenSSH key (`ssh-keygen -y` waits for a passphrase). (2) 03:20Z 630 B per-block ring lookup, 12/12 on alive's fixtures: SUPERSEDED. (3) 03:22Z, alive, after section AB.5 (self-perpetuating 03:21Z: the trunk is public, so it refuses EVERY private key block; a publication lives only on refs/revoked, ruled by `revoke`): the 176 B pattern line of section AA1.K of doc:rse-aa1-boxes, alive merge-up alive/aa1k 1c9ecc2ca, 12/12, no ssh-keygen, no hang. The ring is NOT consulted by the trunk gate: a closed ring line does not admit a block.
- (4) FINAL, alive 03:27Z (after my question): the SOURCE is all-is-one's PER-COMMIT line (every path a commit adds or changes, binaries and merges included), same pattern as AA1.K, carried VERBATIM in section AA1.K of doc:rse-aa1-boxes on branch alive/aa1k @1335d96ef (one node, at SM's gate; it is not yet in AA3.15 of doc:rse-aa3-land, aio will copy it there). PIECE = GROW-GATE, one line per commit beside the signer read: 1,465 -> about 1,746 B, 281 B measured. Built by all-is-one through the built agi-land 9/9 + the 17 AA3 lanes, re-run by alive 8/8: refused = key in extensions/, in a deprecated node, in a .geometry .tsv, inside a binary, in a path with spaces, an EVIL merge; pass = a public key, SSH signature prose, a CLEAN merge. AA1.K's node-loop placement is NOT used (it misses 4). The builder takes the line byte for byte from 1335d96ef.

## CLAIM
(a) a commit that ADDS or CHANGES ANY path (a node, a script, a payload, a binary; a merge commit included) whose bytes hold a private key block (a line matching BEGIN, any label of capitals, digits and spaces, then PRIVATE KEY, in five dashes: OPENSSH, RSA, EC, DSA, PKCS8, ENCRYPTED, bare) is refused by grow-gate, whatever the ring says; (b) the refusal names the file and never prints the key; (c) no key is parsed (no ssh-keygen), so a passphrase-encrypted block REFUSES inside a timeout and never hangs the gate; (d) a node with no such armour, or one that names a PUBLIC key, an SSH signature block, or the words private key without the dashed BEGIN line, lands exactly as today.

## Dispatch line
config-max: none / template-max: none / code: ONE per-commit line (<= +283 B, byte for byte from AA1.K at alive/aa1k 1335d96ef) in the grow-gate piece of engine-grow.md, beside the signer read in its commit loop, no new piece.

## FALSIFIERS
1. A live OpenSSH key, a retired one (its ring line closed), and an unknown one, each in a new node: all three refused, exit non-zero, the output names the file.
2. RSA PEM, EC PEM, PKCS8 RSA, PKCS8 ed25519, ENCRYPTED PKCS8: each refused.
3. A passphrase-encrypted OpenSSH key: refused, and the gate returns inside `timeout 20` (a HANG is the failure).
4. A retired key AND a live key in ONE node: refused. The same block added to an EXISTING node (CHANGED, not ADDED): refused.
4b. The same block in a NON-node path (extensions/x.sh), in a deprecated node, in a .geometry .tsv, inside a binary file, in a path with spaces, and in an EVIL merge (a key file in neither parent): each refused (the four-plus the node loop misses). A CLEAN merge, a public key, SSH signature prose: pass.
4c. FIXTURE RULE: no test file may hold a literal armoured block (it would trip the gate on its own landing); the falsifier generates its keys at run time with ssh-keygen into a scratch dir.
5. Prose that QUOTES the armour with dots in place of the label (the form in this node's own testable_claim and title, SM's heads-up 03:3xZ) and no key body: lands. Prose that quotes the header EXACTLY (five dashes, BEGIN, a label, PRIVATE KEY, five dashes on one line) is refused, by design: a node quotes the phrase with dots, never exactly; this lane pins both.
5b. A node with no armour; a node naming a PUBLIC key (ssh-ed25519 line); a node holding an SSH signature block; a node whose prose says PRIVATE KEY without the dashed BEGIN line: all land as today. This hypothesis node itself lands (its text carries the pattern only with dots, never as a matching line).
6. The refusal output contains no slice of the key body (grep a 16-char slice = 0 hits).
7. Existing gate behaviour unchanged: the grow-gate and engine suite keep the same ok count; `wc -c` of the grow-gate piece grows by <= 283 B (1,465 -> 1,748: DG1 [rule] 03:34Z set the bar at 1,748, the line is 281 B + its separator and newline) and config:engine stays <= 8,192 B (AA2.63 gate).

## TESTS
Shell, scratch repo and a scratch ring only (the agi-fresh.t.sh pattern: ssh-keygen into a temp dir, no live key, no network), one mutation per rule: check dropped = 1 RED; OPENSSH-only match = 2 RED; a ssh-keygen -y step added without -P and a tty-less stdin = 3 hangs (timeout); first-block-only = 4 RED; the ring consulted (closed line admits) = 1 RED on the retired key.

## FILE SCOPE
engine-grow.md (the grow-gate piece) and its measure line in `engine.md`; one test file under extensions/agi/tests/. Nothing else.

## LIMITS (named, not fixed here)
- A key that is base64-wrapped, split across lines, or stored without the BEGIN line is not seen; the claim is the armoured block.
- The pattern needs `PRIVATE KEY` just before the closing dashes: a PGP block (`BEGIN PGP PRIVATE KEY BLOCK`) is NOT matched (mur sm17 R3). Named, not fixed: widening it is a new byte decision.
- OPEN (mur sm17, returned for correction): R1 a path holding a NEWLINE splits under `tr '\0' '\n'` and passes unscanned; R2 a type change (file -> symlink) is dropped by `--diff-filter=AM`, and a `git show` error passes as empty. The fix needs DG2's R1/R2 lanes first and a DG1 byte rule; candidates measured by DG3: see the DG3 message of 04:0xZ.
- The public hub's own push protection on a private key block is UNMEASURED (an outward fact); nothing is published until the owner names that act, and a publication lives only on refs/revoked (AB.5).

## CEILING
1 parent · kids <= 1 · <= +283 B in grow-gate · 1 new test file · 0 USD · regular review + security mur on root code.
