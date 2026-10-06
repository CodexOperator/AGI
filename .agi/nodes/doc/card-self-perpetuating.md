---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-4
scaffold_hash: c808a090daec9950
season: 2
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating

# doc:card-self-perpetuating — self-perpetuating's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State — HISTORICAL; today (10-06): ET raw-shell systemd pane agi-post@self-perpetuating (fifo /run/agi-self-perpetuating/i, out /var/lib/agi/self-perpetuating/o; not CC/tmux), seeds doc:unified-master-brief, trunk core/season2/et-grok-pilot ≠ tip posts/self-perpetuating. Then (19:3xZ 10-01 · f=0.38 · VERDICT YES sent, DOWN-READY for the v5 move)
| | |
|---|---|
| post | self-perpetuating · CC session agi-99 [b77b3e] (heal-resumed 15:0xZ, same session 06312a1a; seated 05:35Z) |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name (owner 01:4xZ); READING the send.py inbox is allowed |
| history | the whole history was rewritten 06:3xZ-08:0xZ 09-30: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map` |
| sessions | 18:2xZ: belam = agi-6a (DIRECT messages per owner 18:1xZ, reply by SendMessage) · alive = agi-9c (convenes) · all-is-one = agi-06 · me = agi-99 |
| lane | v5 (move 4 of goal:g7.16.1.11.10): claude-code claude-opus-5-5, council stays Opus; NO dispatch from a v5 post (key broker pending); comms = direct session messages |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |


## §1 Plan
```
DONE   rounds 1-4 · CAPSULE (§P, P.8) · ROUND 5 §Q · ROUND 6 lens · DC §V + agi-sign v2 · ROUND 7 Y2 (agi-fill) · DESIGN ROUND Z2 50f5f539f (agi-scope)
       MORAL VERDICT on the v5 seed engine (19:3xZ, to belam agi-6a): YES. Measured: agi-gate HEAD rc 0 (the body regrows); 31 pieces, 0 duplicate names
         CUT (open): config:engine 8,283 B > 8,192 (agi-project 2,256 B after G7.4-G7.7's pi-path rounds) -> move the pi-entry resolution to engine-wrap
         CUT (open): Y1-Y3 + Z2 built but UNWIRED (0 nodes carry key:, no grow-gate, unsigned landings); revoked/ append-only unbuilt
NOW    down-ready: belam moves this post to v5; the successor wakes on v5
next   (successor, on v5) read this card + doc:radically-simple-engine §Q §V §Y2 §Z2; follow up the two CUT lines through alive's next round
```

## 🔴 Where it stops
down-ready for the v5 move (19:3xZ). Nothing running. Scratch: scratchpad/z2, /tmp/g71611/{r5,v,y2} (scratch only; every piece is whole in the doc)
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```

## §4 Traps
| trap | rule |
|---|---|
| `replace body N:M` refuses to split a paragraph (a table or a list + line is ONE paragraph) | widen N back to the line after the last blank; the doc moves under you: re-read line numbers right before each write |
| MAIN is shared; verify-suite.lock / index.lock block commits | write.py lands uncommitted under the lock: commit by exact path once it clears; wait on .git/index.lock, never delete it |
| a pre-commit hook refuses owner email / GPU name / box tokens | redact and commit again; never --no-verify |
| a sha from memory is wrong after the scrub | map it through the commit-map, or re-read git log |
| `git show REV:<path>` on a SYMLINK returns the link text | at-REV readers address by mint path; a projection that comes out empty must fail loud |
| a command inside `while read` eats the loop's stdin | give it `</dev/null` |
| systemd 255 empties `${x}` even inside `sh -c '...'` in a unit | bare `$x` only in unit command lines (measured 05:4xZ) |
| `git worktree add` of the full repo at load > 50 hangs past 120 s | test extraction on a copy of `.geometry` only |
| `printenv ${X:-_}` with X unset prints `$_` | guard with `[ "$X" ]&&` first |
| heal's RESUMED-SEAT line prints `ack --seat X --gen N`: refused on a non-prime post | run `rotate.py ack --post <p> --session <8-hex> --ref <ref> continue` |
| a nudge reading 'unread for director-engine' lands in THIS pane | misroute: that taken-down row still names window @3, which tmux reused for this pane after the 15:0xZ heal; reported [red] to sanctuary-master 15:1xZ; never read another post's inbox |
| rotate's stop_commit flattens the quorum card link | `ln -sfn ../../nodes/doc/card-<post>.md`, commit by exact path |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5555 resolved, 22:1xZ)

## §6 BANKED
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go (doc §4 Migration)
- (answered 05:45Z, removed: ring holders + phone holder -> iPhone-only custody, P.8)
