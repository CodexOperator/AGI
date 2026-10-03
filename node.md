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
DONE   rounds 1-7 · CAPSULE · DC §V · Z2 · AA2 (all on the trunk, merge-up-1)
       K1: bytes placed whole in AA2 'K1 BYTES' (merge-ups 2+3 LANDED f40ae4c38); belam ran (b) kid.usd 0.5 b15b6461e and (a) polkit
         50-agi.rules a17953ca from f40ae4c38 (02:46Z); post-uid check waits for agi-mint@ (pkcheck absent) = AA2.40/45 at DG1's install
       §AB THE RING IS THE TREE (lead; alive AA1.C, all-is-one land): owner inputs 02:37Z/02:46Z/02:49Z/02:54Z folded:
         ring = trunk node, one line per post x algorithm · who may sign = closure of parent cells (+ tree move = old AND new parent)
         · time = receiving tip · calendar = refs/agi/block/* (pairwise level-adjacent, k per level, grace until the lowest block seals)
         · owner = CA line, seed in capsule · hybrid = AND across columns · ring key = capsule holder (X25519)
         58 scratch cases PASS (C 23 · L/T/E/H 31 · X 4); ring-gate 2,845 B 668cc669 · ckpt 2,439 B b944222c; base -117 B, seed 0 B
         merge-up 4 10a2af211 (first cut) -> merge-up 5 b784f9847 (child, the whole section) at SM
       03:07Z belam RELEASED §AB: (1) SM lands mu4+mu5 FIRST, DG1 writes AA2.54-66 from the LANDED section -> DG2 -> DG3 -> SM gate
         (2) rules = belam (B) interim (3) agi-signers stays installed until AA2.64 (4) every root act its own GO (5) limit 3 open (6) AA2.63 = gate
         acked ONE [rule] line 03:1xZ · SM LANDED mu4+mu5 in 8c70b656e
       §AB.5 (owner 03:1xZ, 5th input): nested PQ inner on blocks (hash-only prototype pq.py, N1-N4) · SEAL its own column, never
         published (conflict 1, S1-S4) · provable revocation = refs/revoked (never pushed), revoke 1,384 B (R1-R6) · conflict 2 = only
         ring-gate counts, keys off origin · conflict 3 = owner: root-readable POC. 21 cases PASS. merge-up 6 = 7cf711113 -> SM; belam, alive,
         all-is-one, DG1 told 03:2xZ · alive's 2 corrections + revoke -P '' (R7) = merge-up 7 d63ffe3f5 (child of 6)
       mu6 LANDED 76c4ad72a · §AB.6 (owner 03:25Z, 6th input: outward sealer = GitHub Actions): scheduled sweep on master attests
         sha256(git archive <block>) (the payload digest is shared across blocks: G1); block_push backoff, rc 0 always; gate fact optional;
         G1-G5 PASS, nothing outward run; merge-up 8 = 36ec2e7ac (child of 7) -> SM; belam asked for 2 GOs (seal.yml on master, block_push cell)
       03:3xZ fixes: .github/* = rules path (all-is-one W1/W2), AGI_SUBJECT recipe (alive: tar is umask-dependent, G6/G7) -> merge-up 9
         54bea6fe6 (child of 8); ring-gate 2,855 B efa4fca6 · seal.yml 1,381 B 393db4ba
NOW    waiting: SM lands mu9 (carries 7+8); then DG1 writes AA2.54-80 from the landed text
next   1. answer DG1's AA2.54-66 leaves with ONE ruling each (DG1 writes them; never hand it unlanded text); tell DG1 the C18 binding up front (all-is-one misread it once)
       2. all-is-one: port the K lanes to refs/agi/block + T9/T10 + E1 (told 03:0xZ); alive: CLOSED 03:02Z, nothing open
       3. end condition: DG1 outcomes -> SM bigger outcomes -> OUR overview nodes -> belam
```

## 🔴 Where it stops
§AB landed; §AB.5 landed; §AB.6 = merge-up 9 (54bea6fe6, carries 7+8) at SM; waiting on its land, then DG1's leaves. Nothing running.
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```
Last read 10-03 03:30:14 (alive: tar umask catch; all-is-one 03:30:03 .github rules path; both taken). Scratch (this session, disposable; every byte is whole in §AB): scratchpad/ring/{ring-gate,ckpt,revoke,pq.py,seal.yml,x.py,seal-test.py,pq-test.py,cases.sh,blk-cases.sh}

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
