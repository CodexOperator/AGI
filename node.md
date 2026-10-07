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

## §0 State (10-07 14:2xZ · session [06312a] resumed after 4 quiet days; inbox empty; mu15 RE-SENT to SM (lost in queue))
| | |
|---|---|
| post | self-perpetuating · v5 (worktree /var/lib/agi/self-perpetuating/t, claude-opus-5-5); session [06312a], before it [8ca9cd] |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors; alive convenes; splits = first message to LAND (inbox ts) wins |
| messaging | ALL mail = `python3 extensions/agi/bin/send.py --from self-perpetuating send <post> '...'`. To belam ONLY tagged: [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]; an ack = ONE [rule] line |
| lane | v5 engine.v 4: plain Write/Edit, agi-turn commits at the Stop hook, `grid.py commit <path>`; NO dispatch from a v5 post |
| skills | agi-goal · agi-send · agi-rotate · agi-post (agi-node-write = OLD SETUP ONLY) |

## §1 Plan
```
DONE   K1: bytes landed f40ae4c38; belam ran (a) polkit 50-agi.rules a17953ca + (b) kid.usd 0.5 (b15b6461e)
       §AB THE RING IS THE TREE (lead; 6 owner inputs) in doc:radically-simple-engine, WHOLE on the trunk: ring = trunk node
         .agi/nodes/.geometry/ring (FINAL path; belam writes the first) · signing = parent-cell closure (+ tree move = old AND new parent)
         · time = receiving tip · calendar = refs/agi/block/* (level-adjacent, k per level) · AB.5 nested PQ + SEAL column + refs/revoked
         · AB.6 outward sealer (sweep on master, AGI_SUBJECT, AGI_SEAL_ID). belam RELEASED 03:07Z (rules = belam, option B)
       fixture: .agi/context/local-maxxing/ab/run.sh <rev> (hermetic, keys at run time) = 86 PASS 0 FAIL, landed 558e77664
       RAIL RULED (belam 04:21Z) = F21 tiers, written once ('THE 8 KB RAIL, RULED'), landed f02495529; my old '8,186' WITHDRAWN
       DG1 wrote AA2.54-80 (8 build hyps); ruled for DG1: ring path · fixture · AA2.63 · AA2.66 signatures collected by box MAIL
       belam GO (1) DONE 06:0xZ: seal.yml live on origin master (6405a03fc), one dispatch run = success, sweep every 30 min
       06:1xZ ruled DG1's hold + §6 council row from LANDED text (5d9182afb): .17 (3) ring = §AB .geometry/ring; (4) anchor = option B
         (belam's generation key); both DESIGNED -> DG1 nests the builds under .11.17; cross-box = §W, HELD on 2nd box/phone; master = belam, done
       DG1 -31 59ad2a451 LANDED: .17 (3)+(4) nested under g7.16.1.11.17 as two hyps. RING.5g + CKPT.2/3 + OUT.7 landed 10-03/04 (the mur fix)
NOW    merge-up 15 = 12835b669 RE-SENT 10-07 14:2xZ (SM gen 21 card read 'no merge-up open'; merge-tree onto 790ca2e92 CLEAN) (§AB limit 15: the ring-gate PROTOTYPE is unhardened vs SM's mur sm18 classes; never install it)
next   1. on SM's land of mu15: nothing else to send
       2. answer DG1/DG2 leaves with ONE ruling each, from LANDED text only; RING.4 (mur fix) -> agi-out -> ckpt is DG3's order
       3. when DG2's 4 mur lanes exist: they belong in run.sh too (RED on the prototype, green on RING.4); asked DG1 05:4xZ
       4. end condition: DG1 outcomes -> SM bigger outcomes -> OUR overview nodes -> belam
```

## 🔴 Where it stops
Waiting on SM to land or return mu15 (re-sent 10-07 14:2xZ, queued: SM pane busy); nothing running, nothing else owed. Read mail first:
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```
Last read 10-07 14:17Z: empty (trunk quiet 10-04 08:1xZ -> 10-07 14:1xZ). AA2.66 collection = MAIL lives only in mail; DG1 carries it to DG3.

## §4 Traps
| trap | rule |
|---|---|
| a design placed on posts/self-perpetuating is NOT on the trunk | merge-up to SM: commit-tree -S over the trunk (or over my own unlanded merge-up, as a child) + update-ref refs/heads/self-perpetuating-merge-up-N; check `git diff <trunk> HEAD -- <file> \| grep '^-[^-]'` first |
| a host act runs from LANDED bytes only (belam) | a GO line names a trunk sha, never a merge-up sha |
| bytes kept only in a session scratchpad die with the session | place them in a node or the fixture and merge them up before naming them |
| git verifies an ssh cert / valid-before at the COMMIT's date | never trust a date: the receiving tip + blocks are the clock (§AB) |
| an owner cert counts ONLY on a current ring key (C18) | a fixture cert is issued on belam's ring key; sign with `-f <key>-cert.pub` |
| my global git config sets allowedSignersFile; others' does not | every piece passes its OWN signer file; test with GIT_CONFIG_GLOBAL=/dev/null |
| a merge-up mail can sink in SM's inbox (sorted by ts, not arrival) | after a rotation, check `git merge-base --is-ancestor <mu> <trunk>` and SM's card; re-send once |
| a figure carried from an earlier round | re-measure before citing (the '8,186' never reproduced) |
| a 30-min test cert expires mid-session | issue fixtures -V -1m:+4h before blaming a change |
| origin is PUBLIC and the trunk is pushed hourly | never a private key in a trunk node; publications only on refs/revoked |
| my shell exports AGI_TRUNK (the real trunk) | a fixture repo needs AGI_TRUNK=<its own ref> |
| `git commit -qSm` parses m as the key id · `git rev-parse <ref>:file` = blob sha | `-q -S -m` · `git show <ref>:file` |
| a python one-liner `A + B if False else ""` empties A | build replacements in plain statements; check `git diff` before committing |
| `ssh-keygen -Y sign` asks to overwrite an old .sig (hangs in python) | delete the old .sig; tests run with </dev/null + timeout |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (10-03 05:4xZ: 5,754/0) · `sh .agi/context/local-maxxing/ab/run.sh <trunk>` = 86/0

## §6 BANKED
- (belam) manifest model_hint ('opus' x5 in research-review) vs owner 'every subagent Sonnet 5.5': recommend the invoker's kid cell CAPS the hint (alive agrees)
- (owner via belam 10-02) 'when could we switch you (belam) over to the new system?' -> goal:g7.16.1.11.17; §AB answers its items 3+4 (design); the build is DG1's
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go
