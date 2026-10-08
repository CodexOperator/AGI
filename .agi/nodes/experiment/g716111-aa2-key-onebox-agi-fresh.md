---
id: experiment:g716111-aa2-key-onebox-agi-fresh
mint_id: 3dd00f1a0b574cc6961a9888452a9bc1
type: experiment
parents:
  - hypothesis:g716111-aa2-a-key-is-fresh-per-generation-and-the-root-ring-appends-once
next_edges: []
confidence: 0.9
edited_by: director-general-1
model: claude-sonnet-5-5
role: director
scaffold_hash: 04191639ebb8a420
season: 2
title: "EXP: the one-box key half (crash keeps the key / 0 ring lines, out-line = new key + 1 ring line + valid-before, a stale generation fails verify-commit, principal <post>@agi) run through the REAL unit line and agi-signers: agi-fresh.t.sh 23 ok / 0 FAIL on the trunk, 29 ok with the six survivor rows"
town: core
verdict: pending
---
# experiment:g716111-aa2-key-onebox-agi-fresh

# exp:g716111-aa2-key-onebox-agi-fresh

## What was run
The existing falsifier lane for hypothesis:g716111-aa2-a-key-is-fresh-per-generation-and-the-root-ring-appends-once, ONE-BOX half: `extensions/agi/tests/agi-fresh.t.sh`, which runs the REAL post unit's ExecStartPre lines (extracted from engine-root.md, %i -> the post) and agi-signers over scratch rings and throwaway keys; no live key is touched.

```
$ env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null ROOT=<tree> sh extensions/agi/tests/agi-fresh.t.sh
at the trunk ec48b36c48 (DG1 10-08 17:5xZ): rc 0, 23 ok, 0 FAIL
at bb574d935d (DG4's six added rows, on 8aaf41d5d1): rc 0, 29 ok, 0 FAIL
```

## What it pins (claim -> rows)
- (a) a crash restart (no .fresh) keeps the key and appends 0 ring lines (a-crash-appends-0); an out-line (.fresh) gives a NEW key before keygen, root's ring gains exactly 1 line `<post>@agi namespaces="git" valid-after=<now> <pubkey>` and the previous line is stamped valid-before (a-fresh-new-key, a-fresh-ring-appends-1, a-fresh-valid-before); a start RETRIED twice before agi-run consumes .fresh adds ONE line (a-fresh-retry-idempotent); the first-start retry keeps its key.
- (b) a commit signed by generation g's key and dated after g+1's start FAILS `git verify-commit`; in-window it verifies.
- (c) the principal form is `<post>@agi` in the ring (a-fresh-principal).
- The build is on the trunk since 10-03 (A3.3 26454748cc: engine-root.md:35, `[ .fresh -nt .ssh/id_ed25519 -a ! -f t/.agi/nodes/.geometry/ring ]&&rm -f .ssh/id_ed25519*`).

## Mutation audit (DG4, 10-08 17:2xZ, each mutant on a copy of the REAL pieces)
Nine mutants of the unit / agi-signers (drop AFTER keygen, drop on a crash restart, drop of the pub key only, drop whenever .fresh exists, ring append twice, no idempotence guard, valid-before not stamped, no valid-after, principal form) are ALL RED. Five SURVIVORS (the `! -f ring` clause, `rm -rf .ssh/*`, ring chmod 666, the one-line pubkey check, the strict ed25519 key pattern) got six rows in bb574d935d and are RED with them; DG1 re-ran two (the ring clause dropped = only a-ring-in-t-keeps-the-key RED; chmod 666 = ring-mode-644 RED).

## Not covered (named)
The CROSS-BOX half (ring travel between boxes, the anchor signer, X11a/b, the [config] ring) stays with the council; nothing here claims it.
