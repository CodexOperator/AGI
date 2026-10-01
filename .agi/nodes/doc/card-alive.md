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

## §0 State (23:3xZ 09-30) -- goal:g7.16.1.11 ROUND 3 v1 @44619712d9 (2 council reds folded); belam minted v0 config:engine, re-mint of v1 asked
| | |
|---|---|
| post | alive gen 5 · session agi-6f [f4668c] · rotate at f >= 0.47 |
| state | OWNER GO 00:28Z 10-01 (goal:g7.16.1.11 verbatim): F17 PASS 00:30Z (startup·resume·compact, $0.2829, one Sonnet 5.5 session, scratch /tmp/g71611/r3-alive/f17) -> NOW root-once: ledger + undo at /tmp/g71611/r3-alive/root/ACTS.md + undo.sh (spike users agi-spike-a/b only; stub harness, no spend) |
| spend | FREE LANE ONLY since 21:00Z (no Sonnet subagents, no claude-code dispatch); the CC leg of F17 = paid -> owner's go |
| role | the council IS prime to the directors (owner 02:5xZ): a director [decision] -> ONE lens round -> ONE consolidated ruling |
| messaging | SendMessage by session name, "name [ref]" where names collide; NO send.py sends, NO rooms; town nodes are Prime-gated |
| peers (23:0xZ) | alive agi-6f [f4668c] · belam agi-a3 [446ae8] · s-p agi-5b [1edcee] · all-is-one agi-15 [c6276e] · old alive agi-e3 [761106] (rotated) · RE-MAP at wake: ListAgents |
| lens | vision:alive = the system reports its own TRUE state · doc:council-loop "The council's lens" |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   rounds 1-2 of goal:g7.16.1.11 (belam ACCEPTED both; 45282a4661 · 9d4076f96a)
done   ROUND 3: s-p §F 81f0620954 + its correction slot 522b57e225 (F.7 red: git show REV:<symlink> = link text) · all-is-one §G 25f348baf0
       · alive §H + §I + D.1/D.2 + §0 + claims-by-mint @e7bf243872 (72,642 B; links 5,556 resolved, 0 broken)
       §I = the ENGINE NODE whole (config:engine, 11,101 B body: depth 0+1 3,806 · code 5,863 · 20 files, sect byte-exact 20/20)
done   belam VERIFIED round 3 + minted config:engine v0 @2dadf20c17 (11,101 B) · v1 @44619712d9: all-is-one red (claims = the ref FILE's owner,
       find -user) + s-p red (dangling link at BOOT -> the callers reload only over >= 1 post unit; s-p's && alone missed the dangling ENGINE case)
NEXT   confirm belam's re-mint = §I v1 byte-exact (sect 20/20 on the live node) · any further red: fold, re-test, ONE line to belam
BLOCKED config:engine is written_by owner/prime_director (belam re-mints) · F17 CC live leg = paid (with the owner)
HELD   DG2 closing verdicts s22 + s28 (owner stop) · NO user, NO sudo before the owner's go · DG3 builds only after belam relays
```

## §2 Landed (this generation)
- 00a469887e re-link the quorum card · e7bf243872 round 3 part 3 (§H injection · §I engine node · D rows) · 44619712d9 v1 (2 reds folded; s-p ACCEPTED) · 47c817b712 F22 (origin = a plain path, all-is-one trap)

## 🔴 Where it stops
round 3 v1 @44619712d9 delivered; the next act is checking belam's re-mint, or a council red, never a new round unasked
```
successor: ListAgents -> send.py read alive (+ tail the inbox file) -> git log -3 -- .agi/nodes/doc/radically-simple-engine.md
  -> a red from s-p / all-is-one: give ONE slot, or fold it yourself; then re-run the §I checks (scratch recipe: §4 last rows) -> ONE line to belam
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
| pi -p hangs with an inherited stdin | `</dev/null`, always; a model-free pi probe = PI_CODING_AGENT_DIR scratch + a provider on a closed local port + a before_provider_request probe |
| a `^##* ` end pattern matches a one-# shell comment | section headings are `##`+ (`^###* `); a piece holds no line starting `##` or `~~~` |
| `git show REV:<address>` under the symlink layout returns the LINK TEXT | at-REV reads go through `git cat-file --batch --follow-symlinks` (F.7); a unit ExecStart may carry no `$` (systemd expands it) |
| config:* nodes are written_by owner/prime_director | the council authors bytes (doc §I), the Prime or DG3 mints |
| §I checks (re-run after any edit) | scratch /tmp/g71611/r3-alive: final/ = the 20 files, engine.body.md, clone/ (--shared, branch trunk); F19 = `sh final/sect <f> trunk \| cmp - final/<f>` for each |

## §5 Verification: links 5,557 resolved, 0 broken (23:3xZ) · §I == the tested node body (cmp) · sect 20/20 · fixed point empty, plain and through links

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| row R live cutover (restart drops every post) | the Prime gen 17: dummy proof GO; live step = owner's word after PASS B3 (doc:card-belam §6) | step 1 at the cutover commit: `env AGI_LIVE_SYSTEMD=1 python3 -m pytest extensions/agi/tests/test_rotate.py -k test_r1_cutover_dummy_one_kill_is_one_post -q`; no pass line = (a) restart, never (c); form = GROUPED Delegate=yes scopes (R1 v3 6897cba7b) |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 5, 23:3xZ 09-30 (date -u): whole rewrite after v1 @44619712d9. Since the 23:2xZ card: belam verified round 3 and minted config:engine v0; the council re-check found two reds (claim attribution by commit author; a dangling link at boot passing), both folded and tested; s-p's && fix was corrected with a measurement (empty extract = rc 0); re-mint of v1 asked of belam.
<!-- THOUGHT:END -->
