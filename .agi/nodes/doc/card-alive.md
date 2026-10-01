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

## §0 State (05:0xZ 10-01) -- goal:g7.16.1.11 CAPSULE DONE: doc @59cbe58c6, [decision] sent to belam agi-24; waiting on its reply
| | |
|---|---|
| post | alive · session agi-a8 [1e3de5] · rotate at f >= 0.47 (0.23 at 05:0xZ) |
| state | idle on the council lane: belam relays the capsule to the owner; the owner picks the notification carrier (BANKED) |
| spend | FREE LANE; no root act without a new owner go (C9-C11, the i chgrp, P8-P10 need the owner or a go) |
| messaging | SendMessage by session name; NO send.py sends; belam ROTATED: gen 23 = agi-24 [1675318 sock] (rotate.py status --post belam) |
| peers (05:0xZ) | belam agi-24 · s-p agi-5b (near its line, 0.38) · all-is-one agi-15 · DG3 builds v2 on DG5 (stage 2.5): never block it |
| lens | vision:alive = the system reports its own TRUE state |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   round 4 -> bfc04e8588, [decision] sent 04:1xZ · capsule §O 39443e741 (capsule-pop 1,102 B, T1-T8 PASS) · §P s-p 7ebb6c384
       O.5 passkey route + O.6 vector seal df64fa6ea: capsule-login 639 B, P1-P7 PASS (scratch sshd, user-level, all stopped);
       council merged form (ask-id, issued/used refs, projected authorized_keys); code straight to pane i, never the inbox
done+  P.7 s-p df95a721f · whole-doc check PASS · THOUGHT 59cbe58c6 (owner 04:49Z, 04:5xZ x2, 04:59Z verbatim) · [decision] to belam 05:0xZ
NEXT   answer belam / the owner on §O if asked; root/package steps (C9-C11, P8-P10, V-L1) only on a go
HELD   key/identity BUILD until DG3's build lands; this is design only · NO root, NO paid run
```

## §2 Landed
- 547f237df4 re-link · a658452cd9 §N · bfc04e8588 round 4 · 39443e741 §O · df64fa6ea O.5 + O.6 · 59cbe58c6 THOUGHT (capsule)
- gen 5: e7bf243872 r3 part 3 · 44619712d9 v1 · c9c66b2f4b §J spike · f37e25ced2 §I v2 + §K

## 🔴 Where it stops
alive sent the capsule [decision] (doc @59cbe58c6) to belam agi-24 and waits; nothing in flight, no unit, no sshd, no round
```
next: on a reply from belam (re-map first: rotate.py status --post belam): a question = answer from the doc bytes; a change to §O =
  write.py on §O, then the whole-doc check (§I == f37e25ced2, all above §O == bfc04e8588 but edited_by, links 0 broken)
scratch: /tmp/g71611/r4-alive/{cap,pk} (THROWAWAY keys only) · sectionO.md · sectionO56.md
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
