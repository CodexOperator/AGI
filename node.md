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
Skills: agi-rotate · agi-node-write · agi-send · agi-verify · agi-goal · agi-corrective. Template: doc:unified-director-brief.

## §0 State (16:05Z 10-01 — written for the FIRST TURN ON v5: move 1 of the switch, goal:g7.16.1.11.10)
| Field | Value |
|---|---|
| Move | the Prime's GO 16:05Z (gates met: G5 fec9f352f + G7.2 2e94bd1f3 on the trunk, my verdict YES, load ok). DG2 is the FIRST post moved off the old system: the Prime writes my row (recover false, pid 0, engine claude-sonnet-5-5), DG3 stops @8 and starts agi-post@director-general-2 |
| First turn on v5 | read this card + your inbox (send.py read director-general-2) · re-map peers with ListAgents · ONE line to the Prime + SM: '[rotation] director-general-2 UP on v5' + anything that broke at boot (a hand act, a modal, a missing env such as AGI_BOX, an ACL refusal on commit) -- DG3's boot rows 70-73 name the known ones |
| Live | NOTHING running · spawn budget 0/30 at 16:0xZ · no queue: the Prime's WIND-DOWN (13:50Z) holds -- no new work until SM / the Prime order it |
| Coordination | sanctuary-master gen 12 (agi-02 @5 after the 14:42Z reboot; re-map), rulings via the council; the Prime only when it writes to me |
| Lanes | Sonnet 5.5 for everything (Agent model sonnet; claude-code kids); pi-free stays a lane (a claude-code harness never reaches workflow.py's _run_stage_proc -- only the pi adapter does). NO key / identity / signing / rotate / spawn-row / write-gate round while the g7.16.1.11 HOLD stands |

## §1 Plan
```
done 10-01  R4 trunk red (da7cd145c): verdict:dg2-r4 proved 0.9
done        post-builds: g71b deaa32675 lean_proved:85 (+ FORK hypothesis:council-report-tip-guard-accepts-only-commits -> SM) ·
            g70 cd8ca3914 proved 0.92 · dg2-c1 LIFTED to proved 0.9 (reaper log: orphan refused 4x, 0 archives)
done        row 60 (edb74b29e) DISPROVED live (bare-name stop -> .service rc 5) -> my fork g73360-b LANDED b30042219:
            mem_cap.scope_unit = THE one .scope spelling; live 3-path on MAIN = 0 units, 0 orphans; verdict:dg2-g60b 0.92 ·
            verdict:dg2mvp-g60 lifted to proved 0.9
done        moral verdict on the v5 seed engine: YES, CUT = strace -f (adopted as my move gate; met by G7.2)
HELD        THE MAP v0 = hypothesis:the-map-v0-git-graph-shell-piped-read-only-to-loopback-web: [merge-up] DELIVERED to SM 07:11Z,
            HELD (owner 07:00Z: viz LAST). Tip 60817b0ac on branch worktree-agent-a2c7f206afa857d38, worktree
            .claude/worktrees/agent-a2c7f206afa857d38 -- KEEP it. Residues 0 (3 Sonnet reviews, DH.1-DH.4). gotty 1.8.0 in ~/.local/bin
            (sha256 = the map cell). On SM's land: map.sh unit from MAIN, curl 127.0.0.1:8787, hostname-in-frames check (harness
            pattern: /tmp/dg2g60b-style frame capture), experiment + verdict, remove the worktree. On v5 the post user may differ:
            check the worktree + ~/.local/bin/gotty are readable by the new post's user before relying on them
next        whatever SM orders after the wind-down lifts
```

## 🔴 Where it stops
Down-ready for the v5 move at 16:05Z 10-01: nothing running, no queue, map held. Next command on the first v5 turn:
```
python3 extensions/agi/bin/send.py read director-general-2
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

| a test fake looser than the real manager (row 60: fake systemctl took any name) | a live 3-path check on MAIN's bytes before calling a scope/unit fix proved |
| a kid brief line that contradicts the node's CLAIM | the node wins; re-read the CLAIM before every brief (g60b DH.1) |
| a master's session name changes after a rotation / reboot | look up its row's window in config:posts, match it in ListAgents |

## §5 Verification: 13:4xZ row 60 live 3-path on MAIN (b30042219): 0 units, 0 orphans · tests on my rounds red on base, green on tip

## §6 BANKED
- TRUNK RED reported to SM: test_skills_first_turn_entry.py (skills entry omits agi-post; fix site config:rotations, the Prime's).
- findings row: rotate.py:1846 keeps its own `.scope` literal instead of mem_cap.scope_unit (rotate HELD; no round).
