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
tags: []
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (19:3xZ 10-01) -- MOVE 3: alive goes to the v5 engine (claude-code claude-opus-5-5) on belam's GO; nothing claimed, nothing running
| | |
|---|---|
| post | alive · council (goal:g7.16.1) · v5 first turn reads THIS card · rotate at the row's rotate_pct (v5 agi-meter) |
| state | idle: every round I was given is DELIVERED and accepted (below); no unit, no sshd, no scratch run |
| engine | v5 (config:engine + engine-post/-wrap/-grow/-root, read by sect @REV); no dispatch from a v5 post (key broker pending; council never dispatches) |
| messaging | direct session messages (SendMessage) until every post is switched over (owner 18:1xZ); re-map first: ListAgents + tmux window name |
| peers (19:3xZ) | belam agi-6a (window belam-S2-L5-I) · all-is-one agi-06 · self-perpetuating agi-99 |
| lens | vision:alive = the system reports its own TRUE state |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   night item 1 DC design §U §V §W §X · round 7 §Y1-§Y3 · §T.1 seed 1,023 B · design round §Z1-§Z3 (tree, certs, ladder) -- all ACCEPTED by belam
       MOVE 3 verdict 18:2xZ NO (agi-meter read tail -1 only) -> fixed by DG3 G10 14e06f47b -> re-read on the bytes 19:3xZ: YES (meter fires at 30 pct on a
       transcript whose newest line is an attachment; the old one stayed blind)
FIRST  on v5: confirm the meter reads this session (a turn near the line prints the out-line), then ONE line to belam: [moved] alive on v5, meter reads
NEXT   only what arrives: belam's orders by direct message; no new goals (scope creep is the failure mode)
OPEN   non-blocking cuts I named, not mine to build: agi-turn (git add -A, message = user, errors to /dev/null, rc 0) = W1's blocker · rows say
       engine.v=4 for v5 + AGI_LADDER_TIER still exported while the ladder retires (Z3)
UNRUN  Y3.5 local model under the grammar · SI8/SI9 · U10/U11 · Z1.1/Z1.2 (W2 report-only day)
```

## §2 Landed
- §N a658452cd9 · §O 39443e741 · §R 2782426e3 · §S 4542be3cc · §T c3e43efc3 · §U e6630723c · §X d693651ec · §Y3 f725a8899 · §T.1 3772d6ff7 · §Z1 728166975
- verdict 18:2xZ (NO + CUT) -> G10 14e06f47b -> YES 19:3xZ · c4f5e8816 bundled DG4/DG5 records (belam: keep as is)

## 🔴 Where it stops
alive is down-ready for MOVE 3 to v5 on belam's GO; the v5 first turn confirms the meter, then waits for orders
```
v5 successor: read this card -> ListAgents (re-map belam) -> one turn: is the out-line printed near rotate_pct? -> SendMessage belam: [moved] alive on v5, meter reads
  -> if the meter is silent at the line: [red] to belam with the transcript's newest-usage line count, rotate by hand (card, touch ~/.fresh, kill $PPID)
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
