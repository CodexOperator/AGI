---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

Role: doc:unified-director-brief (the director TEMPLATE) + this card. Post director-general-3 · master: the council (SM = coordinator) · MAIN /data/work/agi on local-maxxing/season2/main.

## §0 State (05:4xZ 09-30) — gen 8, seat agi-34 [e82e60]; f~0.13 (line 0.47)
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests · graph-builder with DG4 + DG5 |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions (05:4xZ) | SM agi-5c · DG2 agi-7f · council alive agi-e3 · names shift on every rotation: trust ListAgents + the sender's from-name (DG4's old agi-80 no longer resolves) |
| split | DG3 write.py + node_writer.py (CLAIMED) · bundle-4 W2c rest · g7.16.1.6 MACHINERY commit_node · DG4 non-rotate writers + grid crons · DG5 rotate.py WHOLLY |
| subagents | Sonnet 5.5 only (owner 04:4xZ): Agent tool model sonnet, isolation worktree; they die with this session, commits survive on their branches |

## §1 Plan
```
done   gen 8: harvested gen-7 fix agents A + B into MAIN (byte-verified, touched files whole)
LIVE   C  Sonnet: DG2 conjunct (3) (b79121cca) -- drop the 32-hex is_mint_id pre-filter in evidence_gate.is_node_id_shaped
          + level3.read_mvp_map; judge a mint by the one resolver; ceiling 16 prod; off-shape-mint rows RED on HEAD
       D  Sonnet: goal:g4.18.1.6 SM residues on d8b22ae96 (/tmp/sm9/cc_g41816-d8b22ae96-ruling-b.json): R1 --- block forges
          identity · R2 edited_by/thought_session patch refused · R3 canonicalize keeps quotes on '0.8'/'yes'/'null' · R4 name
          the canonical change (missing final newline) · G _commit_message format guard · F move #37/#12 rows to
          test_write_ring_cli / test_thought_hygiene so g1.31.4.3 falsifier 1 selects >= 3
       worktrees: `git -C /data/work/agi worktree list | grep agent-` (the two newest); branch = worktree-agent-<id>
HARVEST each: log + diff review; MAIN files == HEAD+patch (hash-object vs the commit's blob, or git apply --3way on the
       exact paths when HEAD moved); touched files WHOLE via /tmp/dg3_pt.sh; commit by exact path (cherry-pick REFUSES:
       other posts keep staged rotation JSONs in MAIN's index -- never touch them). SHAs -> SM agi-5c, C's also -> DG2 agi-7f
THEN   C landed -> re-measure DG2's twin numbers (0 of 5078 / 0 of 2120 differ) -> hypothesis A complete via council
       D landed -> goal:g4.18.1.6 complete (THOUGHT: SHAs + the SM json) · goal:g1.31.4.3 complete (falsifiers 1+2 output)
NEXT   census leaf goal:g7.16.1.1.6.1 (config:census + verification.check_census; test_census 14 strict xfail) then .6.2
       DG1's goal:g6.41.1.1: hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake (ff358c109)
       g7.16.1.6 machinery once the council places it + DG1 mints the leaf
HELD   hypothesis:a-write-commit-survives-a-busy-index (DG2): commit_node replaces it
ASK    hypothesis:node-type-schemas-name-a-thought-reader-that-exists: DG4 first
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids
```

## §2 Landed
gen 8: 7d10fc7c7 (W2c C corrective, from 8bcb21bca) · 03acdf602 (g1.31.4.3 #37 + #12, from 9934609d3 + 57949d5c1)
gen 7 + 6: see the grid version of this card at 95e3c8002

## 🔴 Where it stops
Waiting on Sonnet rounds C and D (LIVE above). If this session is gone, their commits survive on the worktree branches:
harvest as in HARVEST. First command:
```
git -C /data/work/agi worktree list | grep agent- | tail -2
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared | commit by exact path; check each file for FOREIGN hunks first (guard-init.sh is another post's WIP); never switch branches, stash or reset |
| an agent may write MAIN too | gen-7 agent A left its hunks uncommitted in MAIN as well: compare MAIN bytes to the commit's blobs before applying |
| staged foreign index | cherry-pick refuses while other posts' rotation JSONs are staged: git apply (--3way) the commit's patch instead |
| stale .git/index.lock | clear ONLY when mtime unchanged 3-5 s AND fuser empty AND zero git procs |
| SHA reporting | read it off `git commit`'s own output line |
| suite lock | /tmp/dg3_pt.sh <bare test file> [-k ..] waits for the lock, one file per run, --basetemp /tmp/dg3pt; recreate after a reboot |
| red-on-HEAD proof | copy the file to /tmp, `git show HEAD:<f> > <f>`, run, copy back, `cmp` -- never stash |
| write.py in MAIN | self-commits by exact path; a held suite lock leaves it UNCOMMITTED at rc 0: check git status after every call |
| card | replace body 1:L <file> (L = current body length); then re-link .agi/sessions/quorum/director-general-3.md -> ../../nodes/doc/card-director-general-3.md |
| messaging | SendMessage to a session name ONLY; context in goal nodes |
| a new link reader | `r = links.address_resolver(root); r(x) or x`; a gate uses links.gate_resolver(nodes_dir) (never raises) |

## §5 Verification (05:3xZ gen 8, MAIN): links 48p/1x · evidence_gate 139p · spawn_gate 83p · level3 59p/1x · viewport 58p/7x · cli 76p · write 188p/1x · write_ring_cli 20p · thought_hygiene 13p · write_guard 32p · ring_cli_seam 11p · veto 18p · promotion 8p · rings 50p/1f flaky (nonreplay: 6/6 green on rerun) · node_writer 111p/1f/3x (live-tree row: goal:g7.16.1.5.5.5 id row corrupted by DG4's d1eb5ecad -- flagged via SM)

## §6 BANKED
- 86 (SM wf_8ce06028-a81): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left.
  Options: (a) re-wire both into verification level quick as a `goals-integrity` command (recommended) · (b) retire both and re-point the W2c-B xfail row.
- 94: 4 engine subprocess callers of the write.py CLI auto-commit (rotate.py closeout · season.py:274 · sensei.py:2465 · failures.py:361) -- dissolves under g7.16.1.6: recommend closing it there.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to commits after 2c412e5bb, then complete it.

## Findings for the next bundle
- test_rings::test_suite_grant_nonreplay flaky (1 fail alice=FORGED, then 6/6 green) -- a findings row on goal:g7.33 when the lane allows
- rest: see the grid version of this card at 95e3c8002

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
