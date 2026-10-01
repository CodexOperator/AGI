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

## §0 State (13:5xZ 10-01, WIND-DOWN at 14:00Z, belam) -- item 1 + round 7 DESIGNED and sent; §T.1 folded DG3's holes; satisfaction verdict DEFERRED to the owner's morning (round 6 not live)
| | |
|---|---|
| post | alive (agi-9c [10fb62] since heal 15:0xZ; was agi-1d) · rotate at f >= 0.47 (0.24 at 07:4xZ) |
| state | nothing running; scratch /tmp/g71611/{u-alive (§U/§X sshd tests), y3-alive (Y3 probes, js/), t2-alive (§T.1 seed + harness t.sh)} |
| spend | Sonnet 5.5 for MURs/subagents (owner 06:5xZ); no root act without a go |
| messaging | SendMessage by session name; re-map first (ListAgents + tmux window name) |
| peers (18:1xZ) | belam agi-6a (window @10, belam-S2-L5-I; agi-d4 = the old Prime) · all-is-one agi-06 (@2) · self-perpetuating agi-99 (@3) · alive agi-9c (@4) |
| lens | vision:alive = the system reports its own TRUE state |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   item 1 DC design: §U e6630723c · §V (SP) · §W (AIO) 60c275d51 · §X d693651ec (+SI rename 3a46f35ce) -> [decision] to belam 07:2xZ
       round 7: Y1 (AIO) 975ee0fdc/92d577161 · Y2 (SP) 2536d7ff3/a280bdfba · Y3 f725a8899 -> [decision] 07:3xZ + addendum 07:4xZ
       §T.1 3772d6ff7: DG3's H1 H2 H4 T7c closed at 1,023 B, H7 = --ff-only; DG3 told to build from §T.1
RULED  belam 07:4xZ: OPTION A (schema/growth.tsv pushes need an anchor-signed commit), folded by all-is-one @d00f70e0f (Y1 complete); round 7 closed to belam 07:4xZ; DG3 acked §T.1
NEXT   item 2 ONLY once round 6 is BUILT live (DG3, after Phase C): figure eight on the seed engine -> alive's SATISFACTION VERDICT on the morals
then   item 3 VIZ LAST (boot math, matrix-op shell renderer, spider viz first)
UNRUN  Y3.5 (a local model under the grammar: the model slot is held by a local-maxxing run since 05:11Z) · SI8/SI9 · U10/U11
```

## §2 Landed
- §N a658452cd9 · round 4 bfc04e8588 · §O 39443e741 · O.5/O.6 df64fa6ea · O.7 e93499fc1 · O.8 1daf2888a · §R 2782426e3 · §S 4542be3cc · §T c3e43efc3
- gen 7: card re-link 554a94423 · §U e6630723c · §X d693651ec · §Y3 f725a8899 · §T.1 3772d6ff7 · THOUGHT 5f2b94556
- 18:1xZ design round (belam agi-6a): §Z1 728166975 (post tree + scope + wiring W1-W4; grow-scope 510 B) · Z2 SP 50f5f539f · Z3 AIO baca24bfb · THOUGHT 40b24d7b5 · [decision] sent 18:2xZ -> ACCEPTED by belam (tree shape to the owner; Z3 build + agi-turn W1 = director rounds; council: nothing more)

## 🔴 Where it stops
alive wound down at 14:00Z (belam), resumed by heal 15:0xZ as agi-9c [10fb62] (ack: continue, already answered); the morning's first act is item 2 once DG3's round 6 is live; nothing claimed or running
```
successor: ListAgents -> send.py read alive -> git log -5 -- .agi/nodes/doc/g716111-round6-build.md (DG3: round 6 live?)
  -> built: run the figure eight on the seed engine, then ONE satisfaction verdict on the morals to belam
  -> not built: stay idle (no new goals); answer only what arrives
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
| a heredoc for python with backticks or $ | ALWAYS quoted (<<'EOF'), pass values by env; an unquoted one ate the backticks once |
| replace body guard | the range must start/end on a blank or heading; mid-table = refused: widen to the block, carry it whole |
| a scratch ssh login whose row has no forced command | it opens a SHELL and the test hangs: every scratch ssh = timeout 10 + </dev/null |
| committing ONE path in MAIN when its index may hold others' staged files | `git diff --cached --name-only` must list ONLY your path, else stop; a bare `git commit` takes the whole index (c4f5e8816 bundled DG4/DG5 records, 15:0xZ 10-01) |
| a check run as yourself over root-owned paths | "Permission denied" is not "absent": re-check as root before calling a collision |

## §5 Verification: links 5,598 resolved, 0 broken (07:1xZ) · §I == v2 tested (cmp) · F19 22/22 · box clean after both root runs

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| row R live cutover (restart drops every post) | the Prime gen 17: dummy proof GO; live step = owner's word after PASS B3 (doc:card-belam §6) | as before (doc:card-belam §6); superseded if config:engine replaces the rotation machinery |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 7, 07:1xZ 10-01 (date -u): whole rewrite DURING item 1 -- §U/§X landed, §V acked from self-perpetuating, §W landed by all-is-one 60c275d51; the 🔴 = the whole-doc check then ONE [decision] to belam. One trap added (a scratch ssh row without a forced command opens a shell and hangs the test).
<!-- THOUGHT:END -->
