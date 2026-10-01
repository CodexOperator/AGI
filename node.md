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

## §0 State (04:11Z 10-01) -- goal:g7.16.1.11 ROUND 4 DONE: doc @bfc04e8588, [decision] sent to belam agi-a3; waiting on its reply
| | |
|---|---|
| post | alive · session agi-a8 [1e3de5] · rotate at f >= 0.47 (0.12 at 04:1xZ) |
| state | idle on the council lane: belam relays round 4 to the owner; DG3 builds after (goal sequence step 3) |
| spend | FREE LANE (the F17 exception is spent: $0.2829); no root act without a new owner go |
| messaging | SendMessage by session name, "name [ref]" where names collide; NO send.py sends; town nodes are Prime-gated |
| peers (04:1xZ) | belam agi-a3 [446ae8] (window @30) · s-p agi-5b [1edcee] · all-is-one agi-15 [c6276e] · DG3 builds config:engine v2 on DG5 (stage 2.5): never block it |
| lens | vision:alive = the system reports its own TRUE state |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   round 3: config:engine v2 @f37e25ced2 (§I + §K); belam re-minted v2 (50eda68b1f)
       round 4: §L s-p a3b98158d9 · §M all-is-one 48aed6ac6d · §N alive a658452cd9 + whole-doc pass (M.1 reworded on s-p's note,
       §0 round-4 line, THOUGHT) -> tip bfc04e8588 · [decision] to belam 04:1xZ (incl. the N.5 red for DG3)
NEXT   answer belam / the owner on §N if asked · on the owner's go, DG3 builds: N3 (a live TUI in the pane) and N4 (the post's
       cgroup under a capped agi.slice) are proved at stage 2.5 on DG5, not by alive
HELD   key/identity/rotate work until DG3's build lands (belam 03:48Z) · NO root, NO paid run without a new owner go
```

## §2 Landed
- 547f237df4 card re-link · a658452cd9 §N · b278b510a2 M.1 · 2fa28c053b §0 · 214d4dea0a + bfc04e8588 THOUGHT
- gen 5: e7bf243872 r3 part 3 · 44619712d9 v1 · c9c66b2f4b §J spike · f37e25ced2 §I v2 + §K

## 🔴 Where it stops
alive sent round 4's [decision] (doc @bfc04e8588) to belam and waits for its reply; nothing in flight, no unit, no round
```
next: on a reply from belam: read it (SendMessage arrives in the pane; also send.py read alive + tail the inbox file)
  -> a question on §N = answer from the doc's bytes (scratch /tmp/g71611/r4-alive: post.v3 inbox.v3 sectionN.md notes.md)
  -> a change to §N = write.py replace body on §N, re-run the whole-doc check (cmp §I vs f37e25ced2, links.py links 0 broken)
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
| a check run as yourself over root-owned paths | "Permission denied" is not "absent": re-check as root before calling a collision |

## §5 Verification: links 5,561 resolved, 0 broken (00:4xZ) · §I == v2 tested (cmp) · F19 22/22 · box clean after both root runs

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| row R live cutover (restart drops every post) | the Prime gen 17: dummy proof GO; live step = owner's word after PASS B3 (doc:card-belam §6) | as before (doc:card-belam §6); superseded if config:engine replaces the rotation machinery |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 5, 03:5xZ 10-01 (date -u): whole rewrite to rotate. Round 4 cannot finish before the line (0.36 of 0.47), so per agi-rotate §1 it is handed on whole: the split went to s-p and all-is-one, alive's part 3 is the successor's. Gen 5 landed round 3 part 3, v1, the owner-approved spike (F17 + root-once), and config:engine v2 (re-minted by belam).
<!-- THOUGHT:END -->
