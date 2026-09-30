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

## §0 State (13:5xZ 09-30 — RESUMED to 18:00Z (owner ~12:4xZ: "continue now until 2pm EST"); STOP comes 18:00Z; meter 0.44, rotate at 0.47)
| | |
|---|---|
| post | all-is-one |
| stage | council — embody vision:all-is-one ONLY ("everyone uses a unified set of tools ... same UI/UX by any role"); TOP-DOWN, generations, never the nitty gritty (doc:council-loop "The council's lens") |
| role (owner 02:5xZ 09-30) | "directors should reach out to council for rulings who discuss it among themselves using the lenses to keep you free. Remember the council IS prime to everyone else." alive convenes: ONE lens line to alive; alive sends ONE ruling; silence = agree |
| place | local-town · MAIN /data/work/agi (RAM disk, same path) on local-maxxing/season2/main · claude-code Opus 5.5 high · CC session agi-8f [242e8c] |
| messaging (owner, until bundles land) | SendMessage by "name [ref]" ONLY (short names collide); NO send.py, NO rooms |
| spend | subagents + reviews on Sonnet 5.5 (owner 04:5xZ); workflow.py pi-free |
| history | REWRITTEN 06:3x-08:0xZ 09-30 (owner: redact email / hardware name / pytest-of path): every sha before 08:0xZ changed -> commit-map below |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1-3 reviewed · bigger_outcome 1-3 v2 accepted (home-path false green named, residue 128)
done   goals rewritten from OWNER lines: mine g7.32.6 (one conversation node; push_on_write; wake = adapter verb) + g4.18.5 (write = one commit on its own ref; era cell write.commit_target)
done   12 S goals closed: mine s7 (leaf g4.18.6.6) · s35 -> g4.18.8 · s18 · s32 (leaf g2.4.1 = cache + storage + apply_umap_coords bridge); retire IN PLACE
done   rulings for directors: DG5 keys (C) own-box remint (box = AGI_BOX; rule = key_template row) · DG3 replace payload not extended · DG1 body refs -> g4.18.6.4
       · DG3 residue 154 fail closed · DG6 meter fallback + one finding · bundle 4: write rc under the suite lock (g4.18.5.5 stopgap) + suite on a tip snapshot (g7.16.1.6.1: the lock retires)
done   g7.16.1.5 placement check -> belam: .5.5.3 restates .5.5 · two session-dir movers (.5.2 vs .5.3.2) -> one mover
done   goal:g1.31 (PASS B3 residues): DG6 first assignment (SM agreed); 47 upheld triaged INTO its Target LANES: DG3 3 · DG5 8 · DG6 17 · NODE 19 (#22 #25 closed)
open   horizon leaves g4.18.6.6 + g2.4.1 wait for their lines · no OVERVIEW until .6, .7 and bundle 4 close (all 3 council posts agreed)
```
Lens questions for every ask: two paths for one act? · a role-only verb or flag? · a copy of a rule (one source)? · an overbuilt branch?

## 🔴 Where it stops
13:5xZ 09-30 resumed to 18:00Z; bundle-4 bigger_outcome reviewed (ACCEPT, W3 first); rotating at 0.47
```
on wake: re-read this card + git log (never a sha from memory) · ListAgents (use "name [ref]") · answer any director ask with ONE lens line to alive
check: git log --since='2 hours ago' --format='%h %an %s' -- .agi/nodes/goal/g1.31.md '.agi/nodes/goal/g7.16.1.*' .agi/nodes/bigger_outcome
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
| .agi/sessions/quorum/all-is-one.md | RE-LINKED 13:5xZ 09-30 (1785348ce0) to this node; rotate may flatten it (skill agi-rotate trap 10): at wake check `ls -la` shows `->`, else `ln -sfn ../../nodes/doc/card-all-is-one.md .agi/sessions/quorum/all-is-one.md` + commit by path |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (belam 08:0xZ post-scrub: nodes 5457, links 0 broken)

## §6 BANKED
(none)
