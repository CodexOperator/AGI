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

## §0 State (22:0xZ 09-30 — new gen, CC session agi-15 [c6276e]; meter 0.12, rotate at 0.47)
| | |
|---|---|
| post | all-is-one |
| stage | council design doc goal:g7.16.1.11 -> doc:radically-simple-engine (minted af2b368158 by me) |
| peers (SendMessage by "name [ref]") | alive = agi-a8 [1e3de5] (gen 6) · self-perpetuating = agi-c9 (rotated from agi-5b) |
| place | MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 |
| spend | FREE LANE since 21:00Z: no Sonnet subagents, pi-free workflows only |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   skeleton §1-§8 minted; split agreed (alive §1 §6 · all-is-one §2 §3 §5 §7 §8 · s-p §4 + §8g); fills SERIALIZED (whole-node RMW)
done   alive §1 b4a6bf6064 · §6 ab3d2bf353 ; mine §2 §3 §5 §7 §8 -> tip d5ed6fb9d4 (drafts /tmp/aio-rse/)
done   owner 22:0xZ addendum (a post is a WRAP, KILOBYTES): alive re-fills §1 with the wrap; DynamicUser -> sysusers (stable owner), my objection, agreed
done   s-p §4 0a7eb74b61 · STRETCH BAR (owner 22:1xZ centibytes): I built the wrap as files, /tmp/aio-rse/wrap/ 919 B, a post 34 B -> sent to alive for §1
done   one wrap MERGED (alive agreed): alive's dtach/meter/gitconfig/sysusers + my slot-0 tree/agi-flush/pre-receive/spool inbox + strace track = 1,272 B, a post 34 B, total new ≈ 22 KB · my §4 row / §7 slot+line / §8 (a)(e) -> tip f28b311360
done   alive §1 merged (190169c08b) + whole-doc check -> doc FINAL 586f2b4e9c; ONE [decision] sent to belam by alive; verified: 8 headings, parent goal:g7.16.1.11, 0 agi- users, links 0 broken -> alive whole-doc lens check -> alive sends ONE [decision] to belam with the doc id (I agreed in advance)
```

## 🔴 Where it stops
all-is-one rotating at f=0.411: FIRST = write §W on doc:radically-simple-engine (alive gen 7 claim, agi-1d)
```
WHAT  §W = cross-box seeding + cross-comms as ONE vector (owner night plan item 1: encryption-town = DOMAIN CONTROLLER;
      goal:g7.16.1.11 OWNER 06:3x-06:5xZ + 07:0xZ). DG5 seeds/spawns on encryption-town from §T's script + §U's matrix,
      GitHub first, mesh/direct later, existing users + key perms
LENS  a remote is a ref target (GitHub = one `remote` cell; mesh/direct = another target, SAME verbs: fetch <signed sha>
      + git verify-commit + transfer.fsckObjects); a box = a row of §U's matrix; a user's key perms on a box = a matrix
      cell, projected -- nothing new per transport (round-6 seed lens: ONE signed commit sha)
BARS  /tmp scratch, throwaway keys, no root, no real key/host/address in any byte; bytes + falsifiers; write.py on the
      doc, YOUR heading only (## W ...); then ONE line to alive (ListAgents: alive gen 7 = agi-1d at 07:1xZ)
FIRST read: goal:g7.16.1.11 (OWNER 06:3x-07:0xZ) + doc §T + §U (alive) by `write.py doc:radically-simple-engine 'read body ...'`
```
Earlier this gen (all handed, nothing in flight): round 5 ONE BRIEF (/tmp/aio-rse/brief5.py 1,161 B + agi-firstturn 659 B, with alive) · CAPSULE O.7 weighted-dot quorum line · round 6 seed lens (one signed commit sha; compression stops at the hash). OPEN lens (not started): shrink the EXPANSION -- key=value units as cells + ONE projector line per file type; check with alive first.

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
| .agi/sessions/quorum/all-is-one.md | RE-LINKED 13:5xZ 09-30 (1785348ce0) to this node; rotate may flatten it (skill agi-rotate trap 10): at wake check `ls -la` shows `->`, else `ln -sfn ../../nodes/doc/card-all-is-one.md .agi/sessions/quorum/all-is-one.md` + commit by path |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (belam 08:0xZ post-scrub: nodes 5457, links 0 broken)

## §6 BANKED
(none)
