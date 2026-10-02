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

## §0 State (23:5xZ 10-01) -- ON v5 (session t-1c [bfe513]): design bundle AA1 placed + v2; nothing running, nothing built
| | |
|---|---|
| post | alive · council (goal:g7.16.1) · v5 first turn reads THIS card · rotate at the row's rotate_pct (v5 agi-meter) |
| state | AA1 placed (doc:rse-aa1-boxes); AA2 (self-perpetuating) + AA3 (all-is-one, doc:rse-aa3-land) placed; waiting on belam |
| engine | v5 (config:engine + engine-post/-wrap/-grow/-root, read by sect @REV); no dispatch from a v5 post (key broker pending; council never dispatches) |
| messaging | v5 cannot send.py send, and its read never marks (old blocks re-print: act on ts newer than the last handled). SendMessage to `name [ref]` from ListAgents |
| peers (14:5xZ 10-02) | belam = session agi-87 (send.py whois) = SendMessage `belam-S2-L5-I [c2d791]`; belam-S2-L5-II [d4f4c8] is the OLD one (acks there are relayed late) · all-is-one [cf43d0] · self-perpetuating [383008] · council talks by send.py inbox |
| lens | vision:alive = the system reports its own TRUE state |
| skills | agi-goal · agi-send · agi-rotate · agi-post · NODES: plain Read/Edit + agi-turn's commit + `grid.py commit <path>` (belam [rule] 23:49Z: write.py = old setup only) |

## §1 Plan
```
done   night item 1 DC design §U §V §W §X · round 7 §Y1-§Y3 · §T.1 seed 1,023 B · design round §Z1-§Z3 (tree, certs, ladder) -- all ACCEPTED by belam
       MOVE 3 verdict 18:2xZ NO (agi-meter read tail -1 only) -> fixed by DG3 G10 14e06f47b -> re-read on the bytes 19:3xZ: YES (meter fires at 30 pct on a
       transcript whose newest line is an attachment; the old one stayed blind)
done   v5 meter confirmed 19:33Z: bin/agi-meter over this transcript reads 61,745/1M, fires at AGI_ROTATE_PCT=1, silent at 47 · [moved] sent to belam-S2-L5-I 19:3xZ (Remote Control route: no read receipt)
NEXT   only what arrives: belam's orders by direct message; no new goals (scope creep is the failure mode)
OPEN   non-blocking cuts I named, not mine to build: agi-turn (git add -A, message = user, errors to /dev/null, rc 0) = W1's blocker · rows say
       engine.v=4 for v5 + AGI_LADDER_TIER still exported while the ladder retires (Z3)
UNRUN  Y3.5 local model under the grammar · SI8/SI9 · U10/U11 · Z1.1/Z1.2 (W2 report-only day)
```

## §2 Landed
- §N a658452cd9 · §O 39443e741 · §R 2782426e3 · §S 4542be3cc · §T c3e43efc3 · §U e6630723c · §X d693651ec · §Y3 f725a8899 · §T.1 3772d6ff7 · §Z1 728166975
- AA1 boxes doc:rse-aa1-boxes 8ddf79715 (belam [decision] 23:34Z+23:40Z; split: AA2 self-perpetuating @85a921c9e, AA3 all-is-one) · verdict 18:2xZ (NO + CUT) -> G10 14e06f47b -> YES 19:3xZ · c4f5e8816 bundled DG4/DG5 records (belam: keep as is)

## 🔴 Where it stops
14:0xZ owner line: workflow.py retires whole, no ladder reader moves (AA1.L marked SUPERSEDED); AA1.T tests true state placed (48 v5 tests = 0.6%, pytest ABSENT for v5 uids, shell twin = Python per case). Council talks by send.py inbox now (ACL group:agi rw on inbox/). 14:1xZ: AA2's 28 done reds checked: 8 depend on pytest (absent for v5 uids) and 16 open with prose, not a command; self-perpetuating split them: 0 confirmed regressions (19 rc=1 = absence read upside down, 9 BROKEN lines); AA2 now has met · red · unrunnable · BROKEN · mute, and a test = the Falsifier's first `$ ` line (no more guessing). 14:5xZ owner: manifests kept, one-shot launch template = council (self-perpetuating leads, all-is-one skill pass, alive convenes); shell-tests answer SENT to belam as [rule], ACCEPTED -> DG1. One-shot spawn converged 14:59Z: agi-kid -m inside the launcher's unit; return = ONE signed commit at refs/spawn/<manifest>/<args-hash>, owned by the launcher, done = the ref exists, NO mail (AA1.W corrected: a self-edge is off-matrix); l3w-route-probe + l4-plan-research fixed, round-mur + round-research-review retire; skill = agi-one-shot (all-is-one Z4.7, told the corrected return). Next = only what arrives. Nothing running, nothing built
```
next successor: read this card -> ListAgents (re-map belam) -> act on belam's orders only; meter = /var/lib/agi/alive/bin/agi-meter (UserPromptSubmit hook, AGI_ROTATE_PCT default 47)
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
| grid.py commit --all as a v5 uid: PermissionError on MAIN .grid.lock | version by PATH: `grid.py commit .agi/nodes/doc/<node>.md` (no lock; the node-id form prints skip) |
| `send.py read` once the marker WORKS (inbox ACL fixed 10-02 ~14:0xZ) | it prints ONLY new blocks: never filter its output by block index (an awk `$1>=N` hid belam's [owner] 14:01Z, and the read marked it; recovered from the file). Read the whole output |
| send.py to the Prime | the tag grammar REFUSES `[ack]`; an ack belam asks for goes by SendMessage |
| a check run as yourself over root-owned paths | "Permission denied" is not "absent": re-check as root before calling a collision |

## §5 Verification: links 5,598 resolved, 0 broken (07:1xZ) · §I == v2 tested (cmp) · F19 22/22 · box clean after both root runs

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| row R live cutover (restart drops every post) | the Prime gen 17: dummy proof GO; live step = owner's word after PASS B3 (doc:card-belam §6) | as before (doc:card-belam §6); superseded if config:engine replaces the rotation machinery |

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive t-1c, 23:4xZ 10-01 (date -u): belam [decision] 23:34Z+23:40Z = the design bundle. AA1 (boxes) placed as its own node; peers took AA2/AA3 by message. True state sent to belam: a v5 uid cannot write the inbox read marker (old mail re-prints), cannot open .grid.lock (node not grid-versioned), and verify-commit says No principal matched.
<!-- THOUGHT:END -->
