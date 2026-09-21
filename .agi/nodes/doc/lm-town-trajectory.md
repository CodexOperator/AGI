---
id: doc:lm-town-trajectory
mint_id: 55dc3a3e4dba43fcb83b3be6a25433a1
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: 7c61cb59727a97bd
season: 2
status: active
title: "The local-maxxing town trajectory board — the ONE shared update space for the master and both directors (owner 01:2xZ 09-21): live rounds, queue per track, last merges, the engine batch; every post appends one line per landing, the master trims the body"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# doc:lm-town-trajectory
## Agent Notes
**What this is (owner 01:2xZ 09-21: "use the trajectory node as the shared update space"):** the ONE board the thought-master and both directors write to — one `note` per landing (round dispatched / merge-up sent / merged / demoted / blocked), stamped and one line long. Cards shrink to identity + stops + a pointer here. The master trims this body (a `replace body`) whenever it passes ~40 lines; history lives in the grid.
**Formation (01:2xZ 09-21):** thought-master (Opus max, MAIN = the trunk `local-maxxing/season2/main`) · director-thought (Sonnet max; research rounds, worktree `.agi/worktrees/post-director-thought`) · director-engine (Sonnet max; engine-fix rounds under goal:g14.14 — seat requested, row is the owner's/Prime's) · pi parents + kids on OpenRouter carry the graph growth. One [merge-up] per batch; the master merges and gates.
**Memory (measured 01:20Z 09-21):** 15 GB total, 12 GB available with the 9B resident; `memory_max` 6G per kid (ceiling); at most ONE model-loading kid on the host at a time, engine kids 2-3 in parallel; GPU = one research round at a time.
**Board:**
| track | live | queue | last landed |
|---|---|---|---|
| G14.11 switch | SWR.01 chunk 1 (a00-9db255d9, API-only, v4.1-flash reference row on HumanEval + IFEval, gap table) | SWR.02 IFEval on local arms, one GPU round per arm | — |
| G14.8 jev + magic pane | — (side track, owner 01:2xZ: jev + openjev research allowed alongside) | MP.01 detector; openjev = the open-source jev line (trycua/cua) | jev chain CLOSED 09-20 |
| G14.9 abliteration | — | H1' hidden-state-mean direction (minted, no spend) | ABL.01 DISPROVED structurally (c0d8c356c) |
| G14.6 / G14.7 tracks I-II | — | OSC.01 → FT.00 | — |
| G14.10 corpus | — | DS.01 kid-sft re-scrub + scrub.py tests | humaneval-abc + trajectories ABC.01/02/ABL.01 landed |
| G14.14 engine fixes | — (director-engine pending) | G14.14.1-4 (write.py · comms · dispatch/runtime · the two workflows) | — |
