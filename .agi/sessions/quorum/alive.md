---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (23:0xZ 09-30) -- goal:g7.16.1.11 ROUND 3 opened (belam 23:0xZ); alive gen 4 rotates at a clean seam (0.43 of 0.47); the successor writes alive's part 3
| | |
|---|---|
| post | alive gen 4 · session agi-e3 [761106] · rotate at f >= 0.47 (0.23 at STOP) |
| state | waiting: nothing in flight of mine; §1 next = watch lines |
| spend | subagents on Sonnet 5.5 only (owner 06:1xZ via the Prime: "ease off expensive subagents"); workflow.py pi-free |
| role | the council IS prime to the directors (owner 02:5xZ): a director [decision] -> ONE lens round (10 min, silence = agree) -> ONE consolidated ruling from the convener |
| messaging | SendMessage by session name, "name [ref]" where names collide; NO send.py, NO rooms; town nodes are Prime-gated |
| peers (13:4xZ) | alive agi-e3 [761106] · Prime agi-23 [ecd665] · SM agi-5c [da1a42] · all-is-one agi-8f [242e8c] · SP uds 2078668.sock · DG1 agi-8c [9e0227] · DG2 agi-e3 [78fffb] · DG3 agi-b4 [a470d3] (@26) · DG4 agi-1c [c38ba9] (@25) · stood down: DG5, DG6 · RE-MAP at wake: ListAgents + tmux list-windows -t agi-rc |
| lens | vision:alive = the system reports its own TRUE state · doc:council-loop "The council's lens" |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   gen 4 (details in git + the grid): belam resume items 1-3 · rulings (boxkit home · meter fallback · g7.16.1.10.7 -> DG3) · bundle-4 review
       -> limit (4) -> 3 leaves (g4.18.5.5 · .5.6 · g7.16.1.6.1) · findings: provenance (g7.33.20.2 LANDED) · names collide · future stamps
done   goal:g7.16.1.11 ROUND 1 (45282a4661: 1,432 B wrap, a post 34 B, pre-receive tested 6/6, track local) · ROUND 2 (c9800a4537 -> 9d4076f96a:
       the living whole 4,253 B; §A fixed point project==observe, 794 B tested; §E = all 17 files whole, regrow byte-exact) -- belam ACCEPTED both
NOW    ROUND 3 (belam brief in the inbox 23:0xZ; owner verbatim on goal:g7.16.1.11 "round 3" section). Base = round 2 @ 9d4076f96a. Split SENT 23:0xZ:
       1 self-perpetuating agi-5b [1edcee]: the SHAPE TEST (every engine piece = ONE .geometry node; 18 .geometry files 327 KB, 293 build nodes)
       2 all-is-one agi-15 [c6276e]: links = SYMLINKS (the mint id = the real file, addresses = symlinks, find -xtype l = the broken-link check)
         + the vector brief A^k e_post read off the filesystem (its ppr.py)
       3 ALIVE (the successor): INJECTION guaranteed -- the harness SessionStart hook returns the brief on startup / resume / compact (today
         extensions/agi/hooks/cc-session-start.sh, 8.9 KB: measure what it does, shrink it to the brief call); NAME the pi equivalent (its
         extension events: session_start / before_agent_start -- core's magic_pane_inject maps them) · TRANSPARENCY: agents use plain paths,
         observe/project + the flush keep the graph current · update the §0 one-screen diagram · falsifiers: find -xtype l = 0; the brief
         injected on a fresh session AND on a resume (+ compact) · then the whole-doc check · ONE [decision] to belam agi-a3 [446ae8] with the sha
       serialized: SP -> all-is-one -> alive; each sends "[done] <sha>" before the next writes
HELD   DG2 closing verdicts s22 + s28 (owner stop) · NO user, NO sudo before the owner's go
```

## §2 Landed (this generation)
- c24f021ef 6bce4aafd df7e2d655 670c893d3 3bb0a37e6 96ac80e95 eee4e5951 85063f1a3 7a857e140 fc70d6b5b 2ee4d0180 5dca1fc47 a1ef46951 11b2f1e95 3c2e83db3 bc3bb8700 d57507672 df64e98c6 4a83b52eb

## 🔴 Where it stops
alive gen 4 ROTATED at 0.43 after sending the round-3 split; nothing in flight; the successor waits for all-is-one's "[done] <sha>", then writes part 3
```
successor: ListAgents (names collide: "name [ref]") -> send.py read alive (belam's round-3 brief) -> read goal:g7.16.1.11 "round 3" verbatim
  -> read doc:radically-simple-engine by id (round 2 base) -> wait for SP + all-is-one [done] -> write part 3 -> whole-doc check -> [decision] to belam
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset; filter a dirty posts.md to YOUR hunk (git apply --cached) |
| write.py commits each write itself, EXCEPT while .agi/sessions/verify-suite.lock is held | it prints "commit refused" and the write lands uncommitted: wait for the lock, THEN commit by exact path; never commit MAIN under the lock |
| my timestamps were guessed TWICE, then a THIRD time as a "fix" (round 2: SP's 22:4xZ -> 22:3xZ from the clock at check time; the commit was 22:28Z) | a time you write = date -u in the same step; a PAST event's time = git log -1 --format=%cI <sha>, never the clock now |
| `send.py read` shows only new blocks; a [red] sat in the inbox FILE alone | after any wake, tail the inbox file too |
| `send.py status belam` marker stuck after an inbox send | SendMessage the Prime directly as well |
| `sub` has no newline: `\n` lands LITERALLY | build a multi-line change in python and `replace body` the WHOLE paragraph or section |
| `thought` rewrites the THOUGHT whole | read the old one first; carry owner verbatim forward word for word |
| a relay says "the owner said X" | verify on the bytes (a node section, a signed inbox block) before spending; a STOP needs no proof |
| the captive capture chain tried rotate-self at 0.4035 and FAILED rc=1 (23:4xZ) | rotate yourself (agi-rotate §2); read the ladder's capture_chain_log if it repeats |
| grep -r / find over .agi/ or the repo root stalls the box | `git grep PATTERN -- <paths>` |
| hypothesis verdict | set `evidence_runs [experiment:...]` WITH `verdict`, or the grid evidence gate demotes it (s31 x3, fixed a1ef46951) |
| write.py `set` | `set key value` (a space, never key=value); a dotted value like G7.x breaks key=value |
| replace body guard | a range must start/end on a heading or blank; to keep a THOUGHT, replace up to the line before it or carry it in the file |
| after_join `[reap-proof] exit 1` | = nothing to reap by design (rotate.py 14399-14421: the named non-matching value); true-state finding for the bundle-4 review: an exit 1 that means clean reads as a failure |
| a send to an idle .prev session (agi-79, 06:1xZ) reached only the rotated-out Prime, which relayed it | re-map before every send to a post that may have rotated: ListAgents + tmux window NAME |
| a SendMessage that returns Failed may still DELIVER (the overview to agi-79, 06:1xZ: the retry was dropped as a duplicate) | never retry blind: wait for the reply or a delivery notice |
| .agi/sessions/quorum/alive.md | a SYMLINK to this node (re-link at wake if rotate flattens it: agi-rotate §3) |

## §5 Verification: links 5355 resolved, 0 broken (06:0xZ) · post-scrub (belam 08:0xZ): nodes 5457, links 0 broken · S goals: complete 22 · retired 10

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| row R live cutover (restart drops every post) | the Prime gen 17: dummy proof GO; live step = owner's word after PASS B3 (doc:card-belam §6) | step 1 at the cutover commit: `env AGI_LIVE_SYSTEMD=1 python3 -m pytest extensions/agi/tests/test_rotate.py -k test_r1_cutover_dummy_one_kill_is_one_post -q`; no pass line = (a) restart, never (c); form = GROUPED Delegate=yes scopes (R1 v3 6897cba7b) |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole rewrite at the STOP (belam [rule] 11:0xZ 09-30; the owner's run ended 11:00Z, owner 04:58Z: "until 7am"). Since the 04:4xZ whole write: gen 4 seated on a stale card (the captive rotation fired before gen 3's last write), rebuilt from gen 3's final version; the council ran belam's resume items 1-3, two rulings, and the bundle-4 vision:alive review, which caught a false claim (exit 0 = committed fails under the suite lock) and minted 3 leaves; a 2-hour freeze for the owner-ordered history scrub (every sha remapped via the commit-map); DG5 + DG6 stood down (owner 06:1xZ), so their leaves re-laned to DG3/DG4.
<!-- THOUGHT:END -->
