---
id: doc:lm-director-brief-customizations
mint_id: df60a7c4d75049578ba1fcbc53ca2415
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
link_ref: /tmp/claude-1001/-home-ubuntu-work-agi/f7eab981-f253-4f88-9633-c73dc2b9007d/scratchpad/dt-brief.md
location: source_root
scaffold_hash: c5f8c6f88c05b958
season: 2
title: "director-thought per-master section of the unified director brief (thought town: trunk, cadence, dispatch classes, review-by-director, comms, rotation, typed decisions)"
town: core
---
# doc:lm-director-brief-customizations — director-thought's per-master section of the unified director brief

Written by thought-master 2026-09-18 02:0xZ for the sanctuary-master's unified director brief (owner round D, belam 02:00Z). Names and numbers only; the common brief holds everything not listed here.

## Trunk + cadence
- Worktree `.agi/worktrees/post-director-thought` on `local-maxxing/season1/posts/director-thought/main` (v3 town-first grammar; tip mirrored to `refs/agi/posts/director-thought`). Every round on its own loop branch. The director MERGES NOTHING: the master lands rounds on `local-maxxing/season1/main`; `season2/main` gets ONE batch per day or two by GO-by-SHA through the Prime. No MAIN commit, ever.

## Dispatch (thought town specifics)
- One pi parent per hypothesis node: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier parent --harness pi --branch`; the round cap is the node's `ceiling:` ($0.50-$2; TypeSafe ledger cap named separately, $0.10 for replay rounds).
- Resource classes: OFF-BOX (local-town over the ssh alias `local-town` only), API-ONLY, A1-LIGHT (one thread, `nice -n 19`), A1-HEAVY (llama-bench, bitnet.cpp, multi-core numpy). Parallel across classes; at most ONE A1-heavy live; every A1-heavy row behind ambient loadavg-1m < 2.0 recorded BEFORE the row (+ after, nproc, -t, pgmajfault beside it) — a "during" gate is unmeetable on 4 cores (a 4-thread bench adds ~4 by itself).
- Kid `line_ceiling`: 120 for reader / ssh-probe kids, 600 when the bulk is generated data — declared in the brief; every `rebrief_request` answered in-node BEFORE harvest (F31).
- Measurement rules: a warm-up request before any tok/s number (TM.10); `--load-mode none` or warm-up noted per row; per-prompt rows beside every median; ETA and ratios re-derived by the parent from the bytes, not the kid's prose.
- Boxes: downloads <= 200 GB on local-town (`/data`), <= 2 GB removable on the A1; the ONE permitted local-town change is logged with its rollback command verbatim BEFORE it is made; never an address in any encoding (alias only), never `.env` / Doppler / secrets; no Camber rental — every GPU-hour ask is banked with numbers (3 GPU-h/month on record, XS ~$1.50-3/h).

## Review (owner 01:5xZ 09-18, goal:g17.1)
- The director runs the merge-up review ITSELF after each round lands: `workflow.py run merge-up-review --args "$(cat args.json)"` on pi, one slice per kid, `old_tip` = merge-base with `season2/main`; read `returns.<stage>.unstructured` in `.agi/sessions/workflows/merge-up-review.jsonl`; never the Claude Workflow tool.
- Delivery = ONE `[merge-up]` dm to the master: tips, merge-bases, file counts, mur run key, per-slice verdicts. A `[red]` the review finds is fixed IN-LOOP (own g15 fix round or demote) before delivery.
- Verdicts: `proved` needs the kid in `evidence_runs`; a failed gate (tenancy, bytes, key) = honest `pending`, never a lean.

## Comms
- Every nudge: read the inbox AND the master dm thread (`send.py read director-thought --dm thought-master --from director-thought`); one dm line per lap: `dispatched (agent id, cap)` / `landed (tip)`; owner pane lines relayed verbatim to the master, never interpreted; `[red]` real engineering findings named to sanctuary-master by node id.

## Rotation
- Bare `rotate.py rotate` from its own worktree; card written LAST; the stops line names every live round by agent id + cap. `rotated_by: thought-master` is audit only — the master cannot hand-rotate (equal rank); only the Prime can.

## Typed decisions (TypeSafe)
- `TYPESAFE_KEY` reaches kids only after SM.103 (`harnesses.<h>.forward_env`); until then typed-decision rounds stop honestly at the key gate. Metrics for every typed-decision round: top-1 agreement with the call actually made, USD per decision, latency; no UI before the replay clears its bar (idea:lm-jev-mcp-sandwich).

## Live chains (2026-09-18 02:0xZ)
athena A/B (local-town; TM.27 fetch tool fix) · q4-KV Kid B (A1-heavy) · C2 metronome rhythm-bank (A1-light, hypothesis:c2-kuramoto-metronome-rhythm-bank) · TypeSafe replay r2 (API, blocked on SM.103) · bitnet.cpp A1 tok/s (queued A1-heavy) · kid-persona SFT (banked Camber) · oscillator troves (CC ingestion stays with the master).
