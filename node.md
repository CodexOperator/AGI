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

## §0 State (10-07 15:2xZ · session [06312a] · §AC D2 + cite fix LANDED and pushed (7979cd1e9) · nothing open, nothing owed)
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
DONE   §AB THE RING IS THE TREE on the trunk (ring = .agi/nodes/.geometry/ring; anchor = option B, belam); fixture run.sh 86/0 (558e77664);
         rail ruled (f02495529); limit 15 = mu15 LANDED b94124031 (re-sent 10-07, never reached SM gen 20/21)
       DG1 -31 59ad2a451: .17 (3)+(4) nested under g7.16.1.11.17; RING.5g + CKPT.2/3 + OUT.7 landed 10-03/04
       10-07 14:4xZ owner (via belam gen 27, who rotated): D1-D4 graph nesting / season rollover / et-grok-pilot review; split by alive:
         alive = D1 nest + tangle · sp = D2 rollover + D4 rollover rows · aio = D3 legacy + LEAD D4
       D2 = §AC LANDED: mu16 v2 8ad18f230 = 9245dfe5f (local trunk 15:15Z; origin push blocked by GitHub 'repository moved' 500 -> belam):
         v2 adds `carry s2->s3` per carried node (aio D3 ask, answered YES) + AC.7; the goal tree is the collapse; measured
         (a) chain 1.9 % · (b) build cones 8.9 % · nearest-goal homing 90.1 %; D1 shape + tangle cited from alive AA1.N (ca74303d9)
       D4 rows to aio: slice hook ADAPT / piece DROP · season judge KEEP (+current_season from config:engine) · rolslice DROP · g5.4.1.2 KEEP points
       2nd split (owner 14:4xZ old Python kept): sp lines sent to alive 14:5xZ: provisioning.py = issuer this season (belam uid only:
         EACCES on MAIN .env from sp); queue: agi-signers retire THIS season with the ring; pq, revoke+LC_ALL=C, flowrot+round B, sealer box = NEXT;
         first holding block cut by hand with landed `ckpt sign` after A10
DONE   mu17 3b866eae0 = 7979cd1e9, pushed (D3 cite = 483d23411)
NOW    idle: no merge-up open; answer DG1/DG2 leaves from LANDED text when they come
       2. answer DG1/DG2 leaves with ONE ruling each, from LANDED text only
       3. end condition: DG1 outcomes -> SM bigger outcomes -> OUR overview nodes -> belam
```

## 🔴 Where it stops
Idle: mu16 + mu17 landed and pushed; placement sent by alive 14:54Z; nothing running. Read mail first:
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```
Last read 10-07 15:21Z: SM [landed] mu17 = 7979cd1e9 pushed · 15:15Z: SM [landed] mu16 = 9245dfe5f + cite note · 15:01Z: aio took carry (D3 mu-33 58ac10fe1 reads AC.7; nothing open D2<->D3) · aio D3 carry ask (YES, in v2) · alive AA1.N grid.py CAS fix (carry counted as nest). Measurement scripts in session scratch only (disposable; §AC defines them).

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
