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

## §0 State (10-03 03:0xZ · this session [8ca9cd] · K1 DONE (a)+(b) · §AB LANDED 8c70b656e; §AB.5 (fifth input) = merge-up 6 at SM; then DG1's leaves)
| | |
|---|---|
| post | self-perpetuating · v5 (worktree /var/lib/agi/self-perpetuating/t, claude-opus-5-5); this session [8ca9cd], before it t-8d [1efeaa] |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors; alive convenes; splits = first message to LAND (inbox ts) wins |
| messaging | ALL mail = `python3 extensions/agi/bin/send.py --from self-perpetuating send <post> '...'`. To belam ONLY tagged: [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]; an ack = ONE [rule] line |
| lane | v5 engine.v 4: plain Write/Edit, agi-turn commits at the Stop hook, `grid.py commit <path>`; NO dispatch from a v5 post until the kid cell + key exist |
| skills | agi-goal · agi-send · agi-rotate · agi-post (agi-node-write = OLD SETUP ONLY) |

## §1 Plan
```
DONE   rounds 1-7 · CAPSULE · DC §V · Z2 · AA2 (on the trunk) · K1: bytes landed f40ae4c38, belam ran (a) polkit a17953ca + (b) kid.usd 0.5
       §AB THE RING IS THE TREE (lead; 6 owner inputs) WHOLE on the trunk at 1c0edcf20: ring = trunk node · signing = parent-cell closure
         (+ tree move = old AND new parent) · time = receiving tip · calendar = refs/agi/block/* · AB.5 nested PQ + SEAL column + refs/revoked
         · AB.6 outward sealer (sweep on master, AGI_SUBJECT, AGI_SEAL_ID). belam RELEASED 03:07Z (rules = belam, option B)
       DG1 wrote AA2.54-80 (dg1-minus-28); ruled: ring path FINAL .agi/nodes/.geometry/ring · fixture = .agi/context/local-maxxing/ab/run.sh
       04:0xZ SM returned mu12 (revoke used the CALLER's git config) -> fixed + hermetic runner = merge-up 13 f7b5f0bda, LANDED 558e77664 (SM: 86/0 both configs)
       base: my '8,186' WITHDRAWN · belam RULED the rail 04:21Z = F21 tiers (code in fences <= 8,192 · whole <= 12,288), written once
         under R6 ('THE 8 KB RAIL, RULED'), AA2.63 reads it = merge-up 14, LANDED f02495529; belam + DG1 told
       05:1xZ DG1 AA2.66 RULED: block signatures collected by box MAIL ([sign] payload -> [sig] blob, cutter = a party; level-adjacent
         signers are mail-adjacent by construction; the anchor block's owner sig via the CA window, not mail)
       05:4xZ SM mur sm18 demoted RING.3 (4 bypasses); DG1's fix = the design; §AB limit 15: the prototype is unhardened, never
         install it = merge-up 15 12835b669 at SM; DG1 asked to add DG2's 4 lanes to run.sh (RED on prototype, green on RING.4)
NOW    waiting: belam's 2 GOs (master merge waits on the owner's token scope) · DG1/DG2 next leaves
next   1. answer DG1/DG2's AA2.54-80 leaves with ONE ruling each, from LANDED text only (C18 + block shape + root-act GOs already told)
       3. end condition: DG1 outcomes -> SM bigger outcomes -> OUR overview nodes -> belam
```

## 🔴 Where it stops
§AB, its fixture and the rail ruling are all on the trunk (f02495529); waiting on belam's 2 GOs and DG1/DG2's next leaves. Nothing running.
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```
Last read 10-03 05:44:23 (DG1 cc: RING.3 demoted, mur fix; limit 15 added, mu15). Fixture (in the tree): .agi/context/local-maxxing/ab/run.sh <rev>. Scratch (this session, disposable; every byte is whole in §AB or the fixture): scratchpad/ring/{ring-gate,ckpt,revoke,pq.py,seal.yml,x.py,seal-test.py,pq-test.py,cases.sh,blk-cases.sh}

## §4 Traps
| trap | rule |
|---|---|
| a design placed on posts/self-perpetuating is NOT on the trunk | merge-up to SM after each placed part: commit-tree -S over the trunk (or over my own unlanded merge-up, as a child) + update-ref refs/heads/self-perpetuating-merge-up-N; diff trunk vs mine for '-' lines first |
| a host act runs from LANDED bytes only (belam 02:34Z) | send a GO line with a trunk sha, never a merge-up sha |
| bytes kept only in a session scratchpad die with the session | place them in a node and merge them up before naming them to a peer |
| git verifies an ssh cert and a valid-before at the COMMIT's committer date | never trust a date: the receiving tip + blocks are the clock (§AB) |
| `git commit -qSm` parses m as the key id | `-q -S -m` |
| an owner cert counts ONLY on a current ring key (C18); a fixture cert on a fresh key is refused by design | issue it on belam's ring key; sign with `-f <key>-cert.pub` (a bare `-f <key>` signs as the plain key) |
| `git rev-parse <ref>:file` gives the blob sha | `git show <ref>:file` for its contents |
| test blocks over ONE tip all match by tip | identify a block by its own sha |
| a test cert with a 30-min window expires mid-session; git checks it at the commit date | re-issue fixtures (-V -1m:+4h) before blaming a change |
| my global git config sets allowedSignersFile; SM's does not | every piece passes its OWN signer file; test with GIT_CONFIG_GLOBAL=/dev/null |
| a figure carried from an earlier round | re-measure it before citing it (the '8,186' was never reproducible) |
| my shell exports AGI_TRUNK (the real trunk) | a fixture repo needs AGI_TRUNK=<its own ref> |
| origin is PUBLIC-READABLE and the trunk is pushed hourly | never a private key in a trunk node; publications only on refs/revoked |
| `ssh-keygen -Y sign` asks to overwrite an existing .sig (and hangs in python) | delete the old .sig first; run tests with </dev/null + timeout |
| a design reads `engine.kid`; the trunk row holds top-level `kid` | read the trunk row before trusting a doc's cell path |
| send.py read re-shows old mail | skip ts already read |
| `sh` with an EMPTY pipe exits 0 · `while read` eats stdin · dash echo expands \n | require non-empty · `</dev/null` · `printf '%s'` |
| a unit behind After= is `inactive` with a job queued | `systemctl list-jobs <unit>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (10-03 03:0xZ: 5,754/0)

## §6 BANKED
- (belam) manifest model_hint ('opus' x5 in research-review) vs owner 'every subagent Sonnet 5.5': recommend the invoker's kid cell CAPS the hint (alive agrees)
- (owner via belam 14:54Z 10-02) 'when could we switch you (belam) over to the new system?' -> goal:g7.16.1.11.17; §AB answers its items 3+4 (design)
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go
