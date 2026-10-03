---
id: hypothesis:g716111-aa2-a-node-carrying-a-private-key-block-lands-only-if-its-public-halfs-ring-line-is-closed
mint_id: c95fafe9752e4332a8c503acfc80f745
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) a commit that ADDS or CHANGES a node under .agi/nodes whose bytes hold a private key block (any -----BEGIN ... PRIVATE KEY----- armour: OPENSSH, RSA, EC, DSA, PKCS8, ENCRYPTED, bare) is refused by grow-gate unless EVERY block in it, checked one at a time, derives a public half (ssh-keygen -y -P '' with no tty) that sits on a CLOSED ring line (valid-before set) in the receiving allowed-signers; (b) with today's ring no line is closed, so EVERY private key block is refused, a live key included; (c) a block ssh-keygen cannot read (RSA, EC, PEM, encrypted, truncated) is refused, fail closed, and a passphrase-encrypted block REFUSES within the timeout, never hangs the gate; (d) a node with no such armour lands exactly as today; (e) the refusal names the file and never prints the key."
title: "AA2: grow-gate refuses a node that carries a private key block unless its public half's ring line is CLOSED (alive's corrected 630 B line, AA1.K; today it refuses every private key block)"
town: core
---
# hypothesis:g716111-aa2-a-node-carrying-a-private-key-block-lands-only-if-its-public-halfs-ring-line-is-closed

## Measured
- alive 03:13Z (read-only): NO landing gate looks for private keys in node bytes today. anonymize's classes are hostname, ip, mac, board, secret, home, email, hardware; its secret class reads .env values, not key blocks. A published retired key passes, and so does an ACCIDENTAL leak of a live one.
- belam 03:2xZ, counts only: 0 private key blocks in the tree, 0 on origin/local-maxxing/season2/main, 0 commits on any origin/* ref ever adding one.
- alive's FIRST line (490 B, belam accepted it 03:2xZ) was WRONG on three fixtures, measured by alive 03:2xZ: it passed an RSA PEM block (matched OPENSSH only), passed a live key placed AFTER a retired one (checked the first block only), and HUNG on a passphrase-encrypted OpenSSH key (`ssh-keygen -y` waits for a passphrase, so one such block stalls every land). BUILD FROM the corrected line, section AA1.K of doc:rse-aa1-boxes (alive merge-up alive/aa1k 385dff5d2): 630 B, any `BEGIN ... PRIVATE KEY` label, one block at a time into per-block files, `ssh-keygen -y -P '' </dev/null`, fail closed; 12/12 on alive's fixtures. NEVER from the 03:13Z text.
- alive 03:1xZ (GitHub API, no token): origin is PUBLIC-READABLE, so a key pushed there is world-public at the push.
- belam [decision] 03:2xZ (1): accepted; it goes NOW as its own round, NOT held behind §AB. Under §AB the rule becomes "closed at or below the latest block"; that wording lands with AA2.54-66, not here.

## CLAIM
(a) a commit that ADDS or CHANGES a node under .agi/nodes whose bytes hold a private key block (any `-----BEGIN ... PRIVATE KEY-----` armour: OPENSSH, RSA, EC, DSA, ENCRYPTED, bare) is refused by grow-gate unless the block is an OPENSSH key whose public half (`ssh-keygen -y`) has a CLOSED ring line (valid-before set) in the receiving allowed-signers; (b) with today's ring no line is closed, so EVERY private key block is refused, a live key included; (c) a block ssh-keygen cannot read (RSA, EC, PEM, encrypted, truncated) is refused, fail closed, and a passphrase-encrypted block REFUSES within the timeout, never hangs the gate; (d) a node with no such armour lands exactly as today; (e) the refusal names the file and never prints the key.

## Dispatch line
config-max: none / template-max: none / code: ONE line group in the grow-gate piece of engine-grow.md (<= +630 B, AA1.K's line; 1465 B today), no new piece.

## FALSIFIERS
1. A live OpenSSH key (its public half on an OPEN ring line) in a new node: push refused, exit non-zero, output names the file. The same bytes after the ring line is closed: admitted.
2. An OpenSSH key whose public half is on NO ring line: refused (unknown key).
3. A non-OpenSSH block (RSA PEM, EC PEM, PKCS8 RSA, PKCS8 ed25519, ENCRYPTED PKCS8, a truncated OpenSSH block) in a new node: refused; none is admitted by any ring state. A passphrase-encrypted OpenSSH key: refused, and the gate returns inside a timeout (a HANG is the failure; run with `timeout 20`).
3b. A retired key AND a live key in ONE node: refused (the live one is checked, not just the first). Two copies of the retired key: admitted.
4. The same key block added to an EXISTING node (CHANGED, not ADDED): refused; a CHANGED node that already carried a closed-line key and is edited elsewhere still lands.
5. A node with no armour, and a node whose prose merely mentions the words PRIVATE KEY without the dashed BEGIN line: lands as today.
6. The refusal text contains no base64 of the key (grep the output for a 16-char slice of the body = 0 hits).
7. Existing gate behaviour unchanged: the engine suite and the grow-gate tests have the same count of ok as before; `wc -c` of the grow-gate piece <= 2095 B and config:engine stays <= 8192 B (AA2.63 gate).

## TESTS
Shell, scratch repo and a scratch ring only (the agi-fresh.t.sh pattern: ssh-keygen into a temp dir, no live key, no network): the cases above plus a mutation per rule (check dropped = falsifier 1 RED; closed test inverted = 1 and 2 RED; fail-open on an unreadable block = 3 RED; first-block-only = 3b RED; OPENSSH-only match = 3 RED; `-P ''` and `</dev/null` dropped = the encrypted case hangs).

## FILE SCOPE
`.agi/nodes/.geometry/engine-grow.md` (the grow-gate piece) and its measure line in `engine.md`; one test file under extensions/agi/tests/. Nothing else. The line's text is alive's AA1.K; the builder takes it byte for byte and wires it into the existing per-node loop (`$t/n` = the node file, `$A` = the ring).

## LIMITS (named, not fixed here)
- The gate reads node files under `.agi/nodes` only: a key in a payload outside it (extensions/, skills/) passes. Naming the wider scope is the council's, with §AB.
- The public hub's own push protection on a private key block is UNMEASURED (an outward fact); nothing is published until the owner names that act.
- A key stored base64-wrapped or split across lines is not seen; the claim is the armoured block.

## CEILING
1 parent · kids <= 1 · <= +630 B in grow-gate · 1 new test file · 0 USD · regular review + security mur on root code.
