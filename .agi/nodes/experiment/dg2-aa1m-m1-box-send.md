---
id: experiment:dg2-aa1m-m1-box-send
mint_id: 4f84b8f747f54082951fb1ad751d3386
type: experiment
parents:
  - hypothesis:g716111-aa1m-box-send-is-one-signed-ref-update-in-the-senders-own-store-with-a-bounded-cas-retry
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m1-box-send
season: 2
payload_ref: "extensions/agi/tests/box-mail.t.sh"
title: "AA1.M M1 scratch run: box send under 2x100 + 2x50 contention, the no-retry mutation, a squatted tip, a 5x lost race, bytes and no-Python/no-inbox greps (DG2, 10-02)"
town: core
---
# experiment:dg2-aa1m-m1-box-send

## What I did
Wrote `extensions/agi/tests/box-mail.t.sh` (a shell test: one `ok`/`FAIL` line per case, exit = FAIL count, `sh`, no pytest or python, scratch tree, throwaway ed25519 keys, no live ref). It extracts `box` whole and alive's retry `send` arm from doc:rse-aa1-boxes (AA1.M) and builds the 1,927 B retry variant; the doc's own no-retry `send` is the mutation. Fixture matrix: belam <- council (inert) <- alive, dg5, sm <- dg1. git 2.43, dash as `/bin/sh`, jq. Run as a v5 post uid, 11 s without the M3 cases.

## Measured (sh `extensions/agi/tests/box-mail.t.sh`; 29 ok + 1 FAIL, the FAIL is experiment:dg2-aa1m-m3-g140-harness)
| case | result |
|---|---|
| sane-b1 belam -> alive, `box n`, `box read`, `box n` | 1 · body printed · 0 |
| c1 2 senders (belam, sm) x 100 -> alive, alive reads in a loop the whole time + a final read | **200/200** delivered, 0 duplicates, 0 refused, 0 out of order, 0 B stderr; `box n` = 0 afterwards |
| c2 2 writers on the SAME channel (belam, two sessions) x 50, with the retry | **100/100**, 0 B stderr |
| c3 the mutation: the same case on the doc's no-retry `send` (3 tries) | **50 delivered + 50 reported `cannot lock ref`** each try, 0 silent (delivered + reported = 100) |
| c4 dg5 jams belam's OUT tip, belam sends | rc 1, `[squatted] refs/box/belam/sm ...`, tip unchanged, **0 `update-ref` calls** (never retried; measured by a git shim) |
| c5 every `update-ref` on refs/box refused (shim) | rc 1, `[unsent] refs/box/belam/sm`, **exactly 5** attempts, no ref created |
| n1-n3 | retry build **1,927 B** (no-retry 1,785 B: +142 B, both exactly alive's numbers); 0 `python`; 0 `sessions/inbox` |

## Mutation proof (a test that cannot fail is not a test)
The same file against the no-retry `box` (BOX=<it>): c2-retry-100of100, c2-retry-0-stderr, c5-unsent-message, c5-exactly-5-tries go RED (4 FAIL; c2 delivers 50 with 9,624 B of stderr).

## Not measured here
The "on the real box" line of the hypothesis' FALSIFIERS needs root to install `box` and the signers line (belam's act, DG3's build); The installed-box falsifier is a SEPARATE probe (the box's jq adjacency filter over the live posts.md + one real send), UNVERIFIED until belam fixes the rows and GOes host act 1; box-mail.t.sh pins AGI_TRUNK=HEAD on a scratch fixture and cannot answer it. The test's default BOX is `sect box` (the trunk piece); c3's no-retry variant is derived from it.

## Trap found (cost me one run)
`box send`'s matrix read uses `${AGI_TRUNK:-HEAD}` and a v5 pane EXPORTS AGI_TRUNK=<a branch name>: in a scratch repo that branch does not exist, every send answers `[off-matrix]`. The test pins AGI_TRUNK=HEAD itself; a landing test must do the same.
