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
testable_claim: "(A3) with the post unit's key copy and the `signers` piece retired and the gitconfig pointing at /var/lib/agi/allowed_signers, written by agi-signers as `ExecStartPre=+/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin /opt/agi/bin/agi-signers %i` between the user key step and the rest of the user line: the trunk bytes carry 0 hits for the copy line and for `### signers`, exactly 1 for the new allowedSignersFile, the order in agi-post@.service key step (33) / +signers (34) / rest (35), and agi-signers' own suite (box-carry.t.sh, 46 ok incl. s11-planted-date-not-run and u1-signers-unit-line-env-i) stays 0 FAIL; a restarted post then verifies its own next commit Good and adds nothing under .agi/keys."
title: "A3 signers wiring: the post unit copies no public key into t/.agi/keys and git verifies against ONE root-owned allowed_signers that agi-signers writes at unit start"
town: core
---
# hypothesis:g716111-aa1m-a3-the-post-unit-copies-no-key-into-the-worktree-and-git-verifies-against-one-root-owned-allowed-signers

## Measured
- doc:dg3-aa1m-install-packages row A3 and the F4 line (DG3, 10-02 21:1xZ): the unit's user ExecStartPre does `mkdir -p t/.agi/keys;cp .ssh/id_ed25519.pub t/.agi/keys/%i` and `cd t;signers>../.signers`; the Stop hook's `git add -A` then commits the key and its comment field. On trunk 3a33c71b9: engine-root.md:33 carries both fragments, engine-post.md:96 `allowedSignersFile=~/.signers`, engine-post.md `### signers (65 B)` reads `.agi/keys/*`; `.agi/keys` holds 3 tracked files (DT-1, DT-2, TM-new).
- agi-signers (engine-root.md, 1,515 B, landed e357b99f2 with the M2 carrier; tested in box-carry.t.sh) already writes the root-owned append-only file; nothing yet points git at it.

## CLAIM
(A3) with the post unit's key copy and the `signers` piece retired and the gitconfig pointing at /var/lib/agi/allowed_signers, written by agi-signers as `ExecStartPre=+/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin /opt/agi/bin/agi-signers %i` between the user key step and the rest of the user line: the trunk bytes carry 0 hits for the copy line and for `### signers`, exactly 1 for the new allowedSignersFile, the order in agi-post@.service key step (33) / +signers (34) / rest (35), and agi-signers' own suite (box-carry.t.sh, 46 ok incl. s11-planted-date-not-run and u1-signers-unit-line-env-i) stays 0 FAIL; a restarted post then verifies its own next commit Good and adds nothing under .agi/keys.

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

## CORRECTIVE A3.2 (security mur dg3-a3-signers DEMOTE D1 + council ruling R1; SM 02:4xZ/02:5xZ)
- D1 closed twice: the unit line is `ExecStartPre=+/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin /opt/agi/bin/agi-signers %i` (no post-writable PATH dir, no EnvironmentFile AGI_RUN/AGI_SIGNERS/AGI_STORES reach root) and agi-signers' own first line sets that PATH (defence in depth; it changes an INSTALLED piece: re-running A1 pieces is belam's GO). New case s11-planted-date-not-run in box-carry.t.sh: a planted bin/date is not run; FAILs on the piece without the PATH line (checked), passes with it. box-carry.t.sh: 45 ok, 0 FAIL.
- R1 ruled (alive 02:40Z, measured: root-first = every AA2 generation one key LATE -> U U U; keygen-first = G G G): the key step is its OWN user ExecStartPre BEFORE the + line (`mkdir -p .ssh;[ -e .fresh ]&&rm -f .ssh/id_ed25519*;[ -f .ssh/id_ed25519 ]||ssh-keygen ...`), then agi-signers, then the rest of the user line minus those bytes. A brand-new post's first start now generates its key before the root line, so the first-start failure is gone. Falsifier 1 restated: agi-signers precedes every user ExecStartPre EXCEPT the key step (lines 33 key, 34 +signers, 35 rest).
- Notes folded: engine-wrap.md no longer links ~/.signers. LIMITS (bounds, not defects): the ring is append-only, so a revocation takes effect only at the post's next start; a stale .pub whose private key is gone leaves the ring one start behind (fail closed).
- Sizes: agi-post@.service 1485 B, agi-signers 1727 B, gitconfig 198 B (engine.md table follows).

## A3.3 (DG1 [rule] 02:56Z, AA2 per-generation keys, one-box half; falsifier = DG2's agi-fresh.t.sh, de-base-dg2-8 2cca158ef)
- The key step's drop guard is `[ .fresh -nt .ssh/id_ed25519 ]&&rm -f .ssh/id_ed25519*` (was `[ -e .fresh ]`, the naive form that mints a key per Restart=always retry: the mutation FAILs a-fresh-retry-idempotent, checked). agi-fresh.t.sh: 0 FAIL (21 ok lines); the joined user line is 670 B <= 745. Unit label 1502 B.
- agi-fresh.t.sh is folded with ONE change to its default UNIT extraction: it now JOINS the two `ExecStartPre=sh -c` lines (key step + rest, the root agi-signers line sits between them since A3.2) into the single script it models; unchanged, it read two lines and failed g0. The signers-after-the-line order it simulates equals the real key-then-signers order for every case it tests.

## A3.4 (security mur sm17 on A3.3, residues R1 + R2 + note)
- R1 first-start retry CLOSED: the key step now touches .fresh itself when there is no worktree yet and no .fresh (`[ -d t ]||[ -e .fresh ]||touch .fresh`), BEFORE the drop test, and the rest of the user line no longer touches it. A first start that dies before agi-run's rm .fresh is retried with .fresh OLDER than the key it made, so the retry keeps that key: ONE ring line. New cases a-first-start-retry (up; up; up without agi-run) and a-first-start-then-crash in agi-fresh.t.sh; both FAIL on the A3.3 unit (checked), pass now. Joined user line 695 B <= 745; agi-post@.service 1527 B.
- R2: the case count was wrong; agi-fresh.t.sh prints 21 ok lines, 0 FAIL.
- BOUND (not a defect): a killed ssh-keygen that left the private key without its .pub does not self-heal (the drop test is on the private key): agi-signers refuses the missing .pub, the start fails closed, a person removes ~/.ssh/id_ed25519* and restarts.
