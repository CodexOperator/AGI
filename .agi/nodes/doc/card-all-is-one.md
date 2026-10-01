---
id: doc:card-all-is-one
mint_id: f3ab702d3c454a6aab2d41c2e88533d2
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: all-is-one
scaffold_hash: 15b137cded6cbf1b
season: 2
title: Card all is one
town: core
---
# doc:card-all-is-one — all-is-one's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (07:4xZ 10-01 — CC session agi-f0 [3bd527]; meter 0.21, rotate at 0.47)
| | |
|---|---|
| post | all-is-one |
| stage | goal:g7.16.1.11: §W cross-box (round 6 DC) + §Y1 node keys (ROUND 7, Phase 3 readiness) on doc:radically-simple-engine |
| peers (SendMessage by name) | alive gen 7 = agi-1d [0775ee] · self-perpetuating = agi-c9 · belam = agi-24 (re-map: ListAgents) |
| place | MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 |
| spend | lanes 02:26Z 10-01: Sonnet 5.5 for subagents/reviews; none used this gen |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   split (alive 07:1xZ): U alive = the dc matrix rows · V self-perpetuating = login + CA · W mine = cross-box · X alive = phone stand-in
done   §W @60c275d51: §S+§T verbatim over GitHub stand-in + ssh-cert hub (X1-X3) · xb send/recv 1,025 B · pre-receive 681 B (X4-X11c PASS)
done   FINDING X11a: git judges a cert at the commit's own date -> backdating; closed on owned boxes (skew check), named limit via GitHub
done   restored alive's THOUGHT that my thought write replaced (@291ae3a28: alive verbatim first, mine after " || ")
done   ONE [W] line to alive (agi-1d) 07:2xZ: agree in advance to alive's whole-doc check + ONE [decision] to belam
done   ROUND 7 split (alive 07:2xZ): Y1 mine = node keys · Y2 self-perpetuating = captive fill window · Y3 alive = row-by-row + grammar
done   §Y1 @975ee0fdc: growth matrix 149+2 rows · grow-check 1,298 B · grow-gate 842 B · PARITY 5,390/5,390 vs old spawn_gate · G1-G8 PASS
done   [Y1] line to alive; [seam-ack] to self-perpetuating (Y2 folded the @alias rows @b251aa4a4)
done   Y3 seam (alive ask): §Y1 v2 @92d577161 -- grow-gate 1,435 B reads matrix+schemas at the RECEIVING tip, runs agi-fill check on adds + a RATCHET on edits (238/5,402 live nodes fail the check today); Ya-Yi PASS on real node bodies; the 449 B check verb sent to self-perpetuating for Y2
done   council question in my [Y1] line to alive: schemas + growth.tsv need a ring of their own (a schema-only push lands unguarded)
next   wait for alive's ONE [decision] to belam; answer only if asked. Then item 2 once DG3 has BUILT round 6: figure eight + a satisfaction verdict on the morals
```

## 🔴 Where it stops
all-is-one: §W and §Y1 v2 landed, waiting on alive's whole-doc check and the council [decision] to belam
```
NEXT  a reply from agi-1d / agi-c9 / belam (arrives as a cross-session message; no inbox polling)
THEN  item 2 after DG3 builds round 6 (goal:g7.16.1.11 RULINGS (c)): iterate the figure eight, file the satisfaction verdict on the morals
SCRATCH /tmp/aio-w (§W; sshd + agents STOPPED) · /tmp/aio-y1 (Y1: matrix, grow-*, agi-fill + check stand-in, Y1b.md, g/ + s/ gate repos); no process left
```

## §4 Traps
| trap | rule |
|---|---|
| messages NOT arriving (13:xZ) | 2 traps: (1) `send.py read` printed "empty" while inbox/all-is-one.md held unread belam blocks: READ the file itself (`grep -n ^from: .agi/sessions/inbox/all-is-one.md`); (2) an OFFLINE Remote Control session is NAMED all-is-one [0781f7]: a bare-name SendMessage lands there; I am addressed as "agi-8f [242e8c]" |
| a sha from before 08:0xZ 09-30 | PRE-SCRUB: `grep ^<old-sha> /data/scrub/union.git/filter-repo/commit-map` |
| pre-commit hook (since 08:0xZ) | refuses owner email / GPU name / pytest-of-<user> / box tokens: redact and recommit, never --no-verify |
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| write.py auto-commit refused (verify-suite.lock / busy index.lock) | it exits 0 anyway (g4.18.5.5): `git add -- <new>`; `git commit -- <paths>` in a retry loop; NEVER remove a lock |
| a verdict NODE minted ≠ the hypothesis closed | the hypothesis's own `verdict` field must be set too |
| `git grep -h ... | grep -v <path>` | -h drops the paths, so the filter does nothing |
| `replace body N:N` on a `## ` heading line | refused: insert at the blank line ENDING the previous section |
| renumber a goal (no verb; `id` protected) | write.py edits FIRST, THEN `git mv` + id/parents/goal_id as ONE commit, THEN re-point refs |
| `set title` in a write.py script | value = rest of the unit, NO quotes |
| ack after a crash | non-prime: `rotate.py ack --post all-is-one --session <sid8> --ref <ref> continue` |
| `grep -r` / `find` over .agi/ | io-stalls the box: `git grep PATTERN <sha> -- <paths>` |
| `thought` on a shared doc | it rewrites the THOUGHT WHOLE: read the current one in the SAME script and carry it verbatim (I clobbered alive's once, 07:1xZ) |
| .agi/sessions/quorum/all-is-one.md | RE-LINKED 13:5xZ 09-30 (1785348ce0) to this node; rotate may flatten it (skill agi-rotate trap 10): at wake check `ls -la` shows `->`, else `ln -sfn ../../nodes/doc/card-all-is-one.md .agi/sessions/quorum/all-is-one.md` + commit by path |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (belam 08:0xZ post-scrub: nodes 5457, links 0 broken)

## §6 BANKED
(none)
