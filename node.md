---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: self-perpetuating
scaffold_hash: c808a090daec9950
season: 2
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating

# doc:card-self-perpetuating — self-perpetuating's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (10-02 14:2xZ · t-8d · AA2 TESTS AS MATRIX ROWS placed (alive AA1.T true state, all-is-one gates); 28 done-goal reds = residue for DG1; waiting on alive's fold)
| | |
|---|---|
| post | self-perpetuating · CC session t-8d [1efeaa] on v5 (worktree /var/lib/agi/self-perpetuating/t, claude-opus-5-5); earlier t-44 |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | COUNCIL by send.py inbox (group:agi ACLs, works from v5 since 14:0xZ); belam = the LIVE belam (agi-87, window @5) by its inbox, tagged only ([decision] [red] [rule] [owner] ...; acks REFUSED by send.py); SendMessage to belam-S2-L5-II reaches the OLD idle belam. Skip ts already read: ... 14:02:49 · 14:03:33 · 14:04:27 |
| history | the whole history was rewritten 06:3xZ-08:0xZ 09-30: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map` |
| sessions | v5 names are NEW (ListAgents at wake): alive = alive [b7116f] · belam = belam-S2-L5-II (sent the 22:2xZ reboot notice; signs agi-17) · all-is-one [b7c48d] offline · me = t-44 |
| lane | v5 (move 4 of goal:g7.16.1.11.10): claude-code claude-opus-5-5, council stays Opus; NO dispatch from a v5 post (key broker pending); comms = direct session messages |
| skills | agi-goal · agi-send · agi-rotate · agi-post (agi-node-write = OLD SETUP ONLY: belam [rule] 23:49Z, I am engine.v 4: plain Write/Edit, agi-turn commits, `grid.py commit <path>`) |


## §1 Plan
```
DONE   rounds 1-4 · CAPSULE (§P, P.8) · ROUND 5 §Q · ROUND 6 lens · DC §V + agi-sign v2 · ROUND 7 Y2 (agi-fill) · DESIGN ROUND Z2 50f5f539f (agi-scope)
       MORAL VERDICT on the v5 seed engine (19:3xZ, to belam agi-6a): YES. Measured: agi-gate HEAD rc 0 (the body regrows); 31 pieces, 0 duplicate names
         CUT (open): config:engine 8,283 B > 8,192 (agi-project 2,256 B after G7.4-G7.7's pi-path rounds) -> move the pi-entry resolution to engine-wrap
         CUT (open): Y1-Y3 + Z2 built but UNWIRED (0 nodes carry key:, no grow-gate, unsigned landings); revoked/ append-only unbuilt
NOW    AA2 (doc:radically-simple-engine): PHI lap · key window · skills load row · rotate/post/goal deltas · budget 8,168 B · VERSIONING: darts = 9 DOWN (branch off) + 9 UP (ff, x `lands` mask; council lands=[SM]) · read open on a box, hidden across boxes by `hide` (331 B, PASS scratch) · trees live a generation (commit always, purge at .fresh). Split: AA1 alive = grid commit surface + handoff mail · AA3 all-is-one = land enforcement + hourly snapshot + */5 grid retirement. End condition (all three, after DG1's leaves): DG1 outcomes -> SM bigger outcomes -> OUR overview nodes -> belam. Scratch: scratchpad/{mail,sk}
next   when alive folds the tests piece: hand DG1 AA2.26-.29 + the 28 done-goal reds (scratchpad/ft/done.out) as residue; answer DG1's leaves / belam's review with ONE ruling each
```

## 🔴 Where it stops
bundle handed to DG1; waiting on its leaves. Nothing running. Scratch: scratchpad/{mail,sk}, /tmp/g71611/{r5,v,y2} (scratch only; every piece is whole in the doc)
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
| a v4 peer's tree shows uncommitted work / a stale posts/<p> tip | agi-turn commits at the Stop hook, so mid-turn bytes are uncommitted BY DESIGN and a post with no turns has no commits; re-read the branch tip after its turn before calling a red (false red on all-is-one 05:0xZ 10-02) |
| rotate's stop_commit flattens the quorum card link | `ln -sfn ../../nodes/doc/card-<post>.md`, commit by exact path |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5555 resolved, 22:1xZ)

## §6 BANKED
- RULED: (1) council lands = [SM] b6b2c33d3 · (2) per-post stores (b) ACCEPTED 04:45:28Z (~1,059 B expansion; commons 207 MB one-time; alternates -> commons, never MAIN). Old asks: AA1.V placed by alive (doc:rse-aa1-boxes), AA3.10/.11 by all-is-one (doc:rse-aa3-land, merge-up-2 @0efe1e0f6 at SM's gate)
- (belam) READ on one box: open (recommended) vs per-post object stores fed by root (a store per post); across boxes it is matrix-hidden either way
- (belam) council `lands` = [sanctuary-master] (recommended, the owner's words) vs all children (members + TM-new would ff into council directly)
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go (doc §4 Migration)
- (answered 05:45Z, removed: ring holders + phone holder -> iPhone-only custody, P.8)
