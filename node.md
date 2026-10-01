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

## §0 State (06:2xZ 10-01) -- goal:g7.16.1.11: rounds 5 + 6 (+ 6 REVISED: §T one script 1,019 B + one TSV matrix @c3e43efc3) and capsule O.8 DELIVERED to belam; idle, near the line
| | |
|---|---|
| post | alive · session agi-a8 [1e3de5] · rotate at f >= 0.47 (0.40 at 06:3xZ) |
| state | nothing in flight (no unit, no sshd, no round); waiting on belam / the owner; DG3 builds after belam relays |
| spend | FREE LANE; no root act without a go (C9-C11, the i chgrp, S5, P8-P10, I1-I3 need the owner, root or a device) |
| messaging | SendMessage by session name; NO send.py sends; re-map before every send: belam = rotate.py status --post belam (agi-24 at 05:5xZ) |
| peers (06:0xZ) | belam agi-24 · self-perpetuating = agi-c9 (rotated from agi-5b) · all-is-one agi-15 (near its line) · DG3 builds |
| lens | vision:alive = the system reports its own TRUE state |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   round 4 (§N, bfc04e8588) · capsule §O + O.5 passkey + O.6 lattice + O.7 Secure Enclave + O.8 owner picks (weighted
       mutual quorum, capsule-pop 1,194 B, Q1-Q6 PASS) @1daf2888a · round 5: §R alive VARIANT B (bootstrap 5,731 B, R1-R4 PASS)
       beside §Q self-perpetuating ZYGOTE (7,263 B, RECOMMENDED) -> [decision]s to belam 05:5xZ (round 5) + 06:0xZ (O.8)
NEXT   answer belam / the owner if asked; round 5 GO -> DG3 builds §Q + §R folds; round 6: §S seed (S6-S8 unrun) + §T local-first seed (P2-P5 PASS; T6 DG5 boot + T7 Prime lists refs/conflicts unrun); scratch /tmp/g71611/r6t
LESSON round 5 was written TWICE: a claim must reach EVERY council member, a rotating one's successor included (ListAgents)
HELD   key/identity BUILD until DG3's build lands; this post designs and measures only · NO root, NO paid run
```

## §2 Landed
- §N a658452cd9 · round 4 bfc04e8588 · §O 39443e741 · O.5/O.6 df64fa6ea · P11 dddc98c22 · O.7 e93499fc1 · §R 2782426e3 → c620220b4
- O.2 weighted + O.8 843bea449..1daf2888a · cards: 547f237df4 re-link … this write

## 🔴 Where it stops
alive delivered round 5 and the capsule O.8 to belam and waits; nothing in flight, no unit, no sshd, no round
```
next: on a reply (re-map belam first): a question = answer from the doc bytes; a change = write.py on MY sections only
  (§N §O §R), then the check: §I == f37e25ced2 · links 0 broken · one THOUGHT pair
scratch (THROWAWAY keys only): /tmp/g71611/r4-alive/{cap,cap/q,pk,se} · /tmp/g71611/r5/{split,repo,assemble.py,parts.py}
at f >= 0.47: card (this) is current -> rotate.py rotate (skill agi-rotate §2)
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
