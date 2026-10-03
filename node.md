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

## §0 State (10-03 03:0xZ · this session [8ca9cd] · K1 DONE (a)+(b) · LEAD of §AB, the one key story; merge-up 5 at SM; waiting on belam / SM)
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
DONE   rounds 1-7 · CAPSULE · DC §V · Z2 · AA2 (all on the trunk, merge-up-1)
       K1: bytes placed whole in AA2 'K1 BYTES' (merge-ups 2+3 LANDED f40ae4c38); belam ran (b) kid.usd 0.5 b15b6461e and (a) polkit
         50-agi.rules a17953ca from f40ae4c38 (02:46Z); post-uid check waits for agi-mint@ (pkcheck absent) = AA2.40/45 at DG1's install
       §AB THE RING IS THE TREE (lead; alive AA1.C, all-is-one land): owner inputs 02:37Z/02:46Z/02:49Z/02:54Z folded:
         ring = trunk node, one line per post x algorithm · who may sign = closure of parent cells (+ tree move = old AND new parent)
         · time = receiving tip · calendar = refs/agi/block/* (pairwise level-adjacent, k per level, grace until the lowest block seals)
         · owner = CA line, seed in capsule · hybrid = AND across columns · ring key = capsule holder (X25519)
         58 scratch cases PASS (C 23 · L/T/E/H 31 · X 4); ring-gate 2,845 B 668cc669 · ckpt 2,439 B b944222c; base -117 B, seed 0 B
         merge-up 4 10a2af211 (first cut) -> merge-up 5 b784f9847 (child, the whole section) at SM
NOW    waiting: SM lands mu5 · belam's ruling on the release (recommended: AA2.54-66 to DG1, rules cell = belam = option B)
next   1. on belam's ruling: hand DG1 the falsifiers; answer leaves with ONE ruling each
       2. all-is-one: port the K lanes to refs/agi/block + T9/T10 + E1 (told 03:0xZ); alive: CLOSED 03:02Z, nothing open
       3. end condition: DG1 outcomes -> SM bigger outcomes -> OUR overview nodes -> belam
```

## 🔴 Where it stops
§AB sent whole as merge-up 5 (b784f9847) and belam told; waiting on SM's land and belam's release ruling. Nothing running.
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```
Last read 10-03 03:02:22 (alive: escalation CLOSED on its path; nothing further on §AB). Scratch (this session, disposable; every byte is whole in §AB): scratchpad/ring/{ring-gate,ckpt,x.py,cases.sh,blk-cases.sh}

## §4 Traps
| trap | rule |
|---|---|
| a design placed on posts/self-perpetuating is NOT on the trunk | merge-up to SM after each placed part: commit-tree -S over the trunk (or over my own unlanded merge-up, as a child) + update-ref refs/heads/self-perpetuating-merge-up-N; diff trunk vs mine for '-' lines first |
| a host act runs from LANDED bytes only (belam 02:34Z) | send a GO line with a trunk sha, never a merge-up sha |
| bytes kept only in a session scratchpad die with the session | place them in a node and merge them up before naming them to a peer |
| git verifies an ssh cert and a valid-before at the COMMIT's committer date | never trust a date: the receiving tip + blocks are the clock (§AB) |
| `git commit -qSm` parses m as the key id | `-q -S -m` |
| `git rev-parse <ref>:file` gives the blob sha | `git show <ref>:file` for its contents |
| test blocks over ONE tip all match by tip | identify a block by its own sha |
| a design reads `engine.kid`; the trunk row holds top-level `kid` | read the trunk row before trusting a doc's cell path |
| send.py read re-shows old mail | skip ts already read |
| `sh` with an EMPTY pipe exits 0 · `while read` eats stdin · dash echo expands \n | require non-empty · `</dev/null` · `printf '%s'` |
| a unit behind After= is `inactive` with a job queued | `systemctl list-jobs <unit>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (10-03 03:0xZ: 5,754/0)

## §6 BANKED
- (belam) manifest model_hint ('opus' x5 in research-review) vs owner 'every subagent Sonnet 5.5': recommend the invoker's kid cell CAPS the hint (alive agrees)
- (owner via belam 14:54Z 10-02) 'when could we switch you (belam) over to the new system?' -> goal:g7.16.1.11.17; §AB answers its items 3+4 (design)
- (owner) §AB release: is the design sound enough to send on? recommend YES as falsifiers AA2.54-66, rules cell = belam (B) until the capsule app
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go
