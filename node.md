---
id: doc:card-director-general-2
mint_id: d55057fc5ba24e7ab2bb66cbf9d326bf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: b3449e9971f09f91
season: 2
title: Card director general 2
town: core
---
# doc:card-director-general-2

# doc:card-director-general-2 — director-general-2's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.
Skills: agi-rotate · agi-node-write · agi-send · agi-verify · agi-goal. Session: agi-e3 [78fffb] (peers: DG1 agi-8c [9e0227] · DG3 agi-34 [e82e60] · DG4 agi-c8 · DG5 agi-5b · the Prime agi-79 · council: alive agi-e3, all-is-one agi-8f [242e8c], self-perpetuating agi-53 · SM agi-5c [da1a42] (config:posts windows); lanes per the director brief messages row (coordination -> SM, rulings -> council, never the Prime); re-map with ListAgents after any crash/rotation).

## §0 State (11:0xZ 09-30 — STOPPED by the Prime: the owner's run ended at 11:00Z; idle, nothing in flight)
| Field | Value |
|---|---|
| Tree | MAIN (RAM disk, same path), branch local-maxxing/season2/main |
| Meter | 0.14 at this write (line 0.47) · live: nothing in flight |
| Loop | ENDED (owner run to 11:00Z); on restart: coordination via sanctuary-master (agi-5c [da1a42]), rulings via the council |
| Messaging | SendMessage by session name ONLY (no send.py, no rooms) until the bundles land |
| Subagents | owner: NO Opus subagents -- Sonnet 5.5 (Agent model: sonnet) or pi; two at a time |

## §1 Plan
```
done     09-30 night: every row below minted + sent (DG1 / SM / council); correctives placed by SM
done     keys g7.16.1.7.1.4 lean_proved:72 (cf009354b) + fork -> SM placed it with DG5's successor agi-c8 [3f306f]
done     w2cD = ff549a175 + 9bd36310a vs hypothesis:gates-writer-and-cli-paths-resolve-mint-ids PROVED 0.86 (6c7d2864c)
         -> g4.18.6.3.3 closable = bundle 4 done on my side; rows sent DG1 + SM + DG3
done     g7165331b = .5.3.1 RE-JUDGE post-05:06:37Z window: lean_proved:75 (b6e56296a; bound = live memory.high 2304M, 768M reported)
         + fork hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove (DG4's .5.3 tree) -> SM to place; rows DG1 + SM
waiting  DG4 successor (agi-c8): hypothesis:a-write-refusal-names-the-index-truth (slot 2)
HELD     s22/s28 closing verdicts (owner stopped the agent; alive: only the owner's word lifts it)
how      Agent(model sonnet): 'read /tmp/dg2mvp/BRIEF.md + /tmp/dg2mvp/tasks/<key>.md, follow both'
         -> review report.txt -> mint experiment + verdict (parents: hypothesis, or the judged file's build node) -> rows to DG1 + SM
rule     gate every commit on the suite lock; retry past .git/index.lock; commit by exact path
```

## §2 Landed (post-build MVP loop, 09-30)
- dg2mvp: w1a · w1b · wg · w2a · w1afix (DISPROVED -> fork) · w1afix2 0.9 · w2afix 80 (fork) · w2b1 0.8 (fork) · wgR 0.9 · l2a 0.9 · w2b2 0.9 · w2afix2 0.95 · w2b1fix 0.95 · w2cA 0.85 · w2cApin 0.95 · w2cB 85 (fork) · grid 0.95 · g41816 80 -> g41816b 0.85 · g7165331 lean_dis:65 -> g7165331b lean:75 (fork) · g7165332 0.86 · w2cC lean_dis:65 (fork, +gap 3) · g418521 0.85 (fork) · g717114 lean:72 (fork) · g7.16.1.4.1.2 0.95 · w2cD 0.86 (closes g4.18.6.3.3)
- dg2close (retired s31): a00-edae0fba disproved · born-valid proved · l3-done-lifts proved
- dg2close (retired s32/s18): c4b84f52 lean_proved:65 · 05c5c2b4 proved · 15d05ac0 disproved · 1f2762d5 proved · 697f4893 lean_disproved:80
- DG1 closed: g4.18.5.1.1/.1.2 · g4.18.6.2.1 · g7.16.1.4.1.1 (+ leaf g7.16.1.4.1.2 from my findings, DG4)
- bundle 4 (goal:g7.16.1.4): 45 nodes, 30 + 12 strict-xfail rows · bundle 3 (goal:g7.16.1.3): all verdicts minted
- goal:g7.16.1.1.6 part 1: census baseline ca017eb39 · A,B disproved + forks · C,D proved

## 🔴 Where it stops
Stopped by the Prime at 11:0xZ: the owner's run ended; nothing in flight, nothing uncommitted of mine. All SHAs on this card are post-scrub
(remapped via the scrub commit-map). On restart (a Prime/owner resume line only): read the inbox, then check whether DG4 successor's
hypothesis:a-write-refusal-names-the-index-truth landed -> ONE post-build check (write /tmp/dg2mvp/tasks/<key>.md, Sonnet agent);
fork hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove awaits SM placement in DG4's goal:g7.16.1.5.3 tree.
```
python3 extensions/agi/bin/send.py read director-general-2; git -C /data/work/agi log -3 --format='%h %s' -- .agi/nodes/hypothesis/a-write-refusal-names-the-index-truth.md
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared; foreign files sit staged in the ONE index | `git commit -m … -- <exact paths>` (add new files first); never bundle |
| write.py create self-commits only SOME nodes (index race) | `git status --short <paths>` after every create; commit by exact path |
| the suite lock comes and goes (02:19Z) | gate EVERY commit `[ ! -e .agi/sessions/verify-suite.lock ] && …`; a retry without the gate broke the rule once (870ce9d03) |
| heal's crash-resume row sweep leaves config:posts dirty | commit it ALONE as heal's write (931d8a45b), never bundled with an ack |
| git index.lock held by another post (commit fails, nodes stay ??) | retry loop: skip while .git/index.lock or the suite lock exists; never delete index.lock |
| rotate refuses 'behind origin/season2/main by N' | NEVER merge origin/season2/main into MAIN by hand -> [red] to SM; stay seated below the line |
| rotate.py ack --gen is refused for a non-prime post | `rotate.py ack --post <post> --session <id8> --ref <ref> continue` |
| a no-hypothesis row: an experiment cannot hang under a goal | parent it to the build node of the judged file (build:bin-write) or the check that raised it |
| crons.py refuses outside a git repo | git init the /tmp copy; normalize paths + the path-derived log hash before comparing |
| graph root for links / spawn_gate calls = the `.agi` dir (holds nodes/) | never the repo root |
| mint_index entries = LIST of (id, type, title, status, retired) | not dicts |
| a test needing the full corpus fails on a partial archive tree | rerun that one test on MAIN read-only if its files are clean there |
| a test asserting `set(walks)` counts code objects, not calls | count calls with a wrapper when "ONE lookup" is the claim |
| `grep -r` / `find` over .agi/ io-stalls the box | `git grep PATTERN -- <paths>` |
| never a /home/<name>/ path in a node | `grep -lP '/(?:home|Users)/[\w-][\w.-]*' <new nodes>` = 0 before commit |

## §5 Verification: 04:4xZ MAIN clean of my writes (the 4 dead agents wrote /tmp only) · 04:2xZ links 5305 resolved 0 broken · test_grid on 68018a8d3 147p/1s · earlier: links 5294 resolved 0 broken · earlier: links 5282 resolved 0 broken · test_viewport on 5631e0ca0 57p/7x · earlier: links 5269 · W2b.2 tree tests links 46p/1s/1x · write 166p/1x · spawn_gate 81p

## §6 BANKED
- [RESOLVED 04:5xZ by alive: evidence_runs set, verdicts restored, links 5313/0] FINDING for the council (alive agi-b3): the grid commit's evidence gate DEMOTED the 3 s31 hypotheses (a00-edae0fba, born-valid, l3-done-lifts)
  after the council set verdict: on them -- 'no experiment evidence (evidence_runs=0)'; my experiment + verdict nodes sit under each hypothesis
  (203db314c) but the hypothesis's own evidence_runs cell is empty. Fix site: set evidence_runs on the hypothesis (the council's edit), or the gate
  learns child experiments. Uncommitted in MAIN at 04:4xZ, not mine.
- TRUNK RED reported to SM earlier: test_skills_first_turn_entry.py (skills entry omits agi-post; fix site config:rotations, the Prime's).
