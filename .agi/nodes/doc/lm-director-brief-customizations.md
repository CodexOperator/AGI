---
id: doc:lm-director-brief-customizations
mint_id: df60a7c4d75049578ba1fcbc53ca2415
type: doc
parents:
  - goal:g5.7
next_edges: []
edited_by: thought-master
location: source_root
scaffold_hash: c5f8c6f88c05b958
season: 2
thought_session: internals-standing-sync-2026-09-21
title: "director-thought per-master section of the unified director brief (thought town: trunk, cadence, dispatch classes, review-by-director, comms, rotation, typed decisions)"
town: core
---
# doc:lm-director-brief-customizations — director-thought's per-master section of the unified director brief

> **Standing spine:** `doc:standing-llm-ops` (diagram-max incl. thought-stream; `[merge-up]` only at residues=0). Customizations below do not weaken that.


Written by thought-master 2026-09-18 02:0xZ for the sanctuary-master's unified director brief (owner round D, belam 02:00Z). Names and numbers only; the common brief holds everything not listed here.

## Trunk + cadence
- **NEVER (owner 2026-09-19 01:1xZ, in the thought-master pane; gate cause fixed on the town trunk b6c121ffa TMM.02; mirrors `doc:unified-director-brief` §4 thought):** a town director merges ONLY its town trunk (`origin/local-maxxing/season1/main`) into its post branch and pushes ONLY to `refs/agi/posts/director-thought`; MAIN and core reach the town through the master trunk, batched — never merge `origin/season2/main` or `origin/core/season2/main` directly, never push any head under `season2/*` or `core/*`. If dispatch still refuses `stale-base ... integration season2/main`, do not merge MAIN: `--allow-stale-base "town post: integration is local-maxxing/season1/main"` and put the refusal line in the return batch.
- **Batched (owner 01:0xZ + 01:3xZ 09-19):** the master hands ONE batch; the director does only that batch (rounds back-to-back, parent corrections extend/cut/rebrief, in-loop g15 fixes: node first, kid writes, tests green), lands on its post branch and hands back ONE [merge-up] return batch (tip + verdicts + review badges + a proposed WHY per disproof); reds escalate to the master at once. Stamps in UTC (`date -u`).
- Worktree `.agi/worktrees/post-director-thought` on `local-maxxing/season1/posts/director-thought/main` (v3 town-first grammar; tip mirrored to `refs/agi/posts/director-thought`). Every round on its own loop branch. The director MERGES NOTHING: the master lands rounds on `local-maxxing/season1/main`; `season2/main` gets ONE batch per day or two by GO-by-SHA through the Prime. No MAIN commit, ever.

- **MUR RESIDUES CLOSE IN-LOOP BEFORE THE BATCH IS DELIVERED (owner 2026-09-19 01:5xZ, verbatim in `doc:unified-director-brief` §2; mirrored here):** every residue a merge-up-review names (an M-item, an accept_with_residue, an overridden verify demote) gets its OWN corrective round under the same node, dispatched by the director without asking, mur again, until the review names no residue — only then the batch's ONE [merge-up] line goes to the master with the final mur key + verdicts. MAJOR residues (rule-changing, a design decision above the node, a cost or model change, a Prime/owner-only call) escalate as a [red] to the master instead. A batch delivered with a residue still open is not delivered.
- **Meter forces the rotation (SM.135, owner 01:5xZ: "It must capture and force final card update"; `hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself`, on core, engine half pending):** at f >= the line, or on an unacted `rotate now` from the master/owner, the meter hook captures the final card and forces `rotate` — write the card DURING the work so the capture is current; an idle seat alarms.

- **Quick fixes on the town trunk (owner 04:1xZ 09-19, verbatim: "If you need anything quick fixed on your own branch tell the director to dispatch the parent and use a regular review workflow not research review"):** the master names the fix (a g15 node); the DIRECTOR dispatches the parent; review = the regular `review` workflow (`workflow.py run review --harness pi`), never `research-review` (research rounds only). The master spawns no parents.

## Dispatch (thought town specifics)
- One pi parent per hypothesis node: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier parent --harness pi --branch`. No per-round spending cap (owner 09-23 14:xZ): the dispatcher's concurrency cap is the only cap; a hypothesis `ceiling:` bounds scope in engine units, never spend.
- Resource classes: RIG-GPU (the GPU2070S rig) · RIG-CPU (the rig's spare threads) · KEEPER CPU8G (encryption town: first choice for CPU-only rounds, owner 09-18 22:4xZ) · API-ONLY. A heavy bench row records ambient loadavg-1m BEFORE the row (+ after, nproc, -t, pgmajfault beside it). How many of each run at once is a spawn limit -> the director's card.
- Kid `line_ceiling`: 120 for reader / ssh-probe kids, 600 when the bulk is generated data — declared in the brief; every `rebrief_request` answered in-node BEFORE harvest (F31).
- Measurement rules: a warm-up request before any tok/s number (TM.10); `--load-mode none` or warm-up noted per row; per-prompt rows beside every median; ETA and ratios re-derived by the parent from the bytes, not the kid's prose. A step smaller than about 1 pct counts only with fixed inputs, repeats and a CI (the HEAD's LOOP line, owner 09-23).
- Boxes: downloads <= 200 GB on local-town (`/data`); box tunables follow the HEAD's DURABLE line (inside your own window, recorded, restored, named; clocks and power limits within +10 / -70 pct of the baseline need no go); never an address in any encoding (alias only), never `.env` / Doppler / secrets; Camber GPU-hours for fine-tuning, RL and pretraining are owner-authorised (09-20 21:4xZ: 'failing is fine') -- the round states its GPU-hours and USD up front against the 3 GPU-h/month on record (XS ~$1.50-3/h).
- **Town research rules (09-23):** IFEval rounds seed BOTH RNGs (keywords:letter_frequency's stdlib random + langdetect), N=10 CI rule (TMM.32) · abliterated-in-prod · pace slow, small chunks · batch-max (one merge-up per batch) · every synthetic or eval dataset a round makes lands in `datasets/` with its explainer (doc:lm-research-corpus-registry), never only in a run dir (owner 09-20 21:5xZ). SPAWN LIMITS -- how many rounds, parents, kids or model-loading host kids run at once, a paid round's orders wall -- live ONLY on the director's card (owner 09-23 14:xZ).

## Review (owner 01:5xZ 09-18, goal:g7.16)
- The director runs the merge-up review ITSELF after each round lands: `workflow.py run merge-up-review --args "$(cat args.json)"` on pi, one slice per kid, `old_tip` = merge-base with `season2/main`; read `returns.<stage>.unstructured` in `.agi/sessions/workflows/merge-up-review.jsonl`; never the Claude Workflow tool.
- Delivery = ONE `[merge-up]` dm to the master: tips, merge-bases, file counts, mur run key, per-slice verdicts. A `[red]` the review finds is fixed IN-LOOP (own g15 fix round or demote) before delivery.
- Verdicts: `proved` needs the kid in `evidence_runs`; a failed gate (tenancy, bytes, key) = honest `pending`, never a lean.
- Research rounds (owner 09-18 20:2xZ + 19:5xZ): run agi-research-review by name (review, verify, why, brainstorm, refute); the batch line carries the WHY, the idea, 1-5 hypotheses and the refute verdicts.
- Town moral (moral:local-maxxing): judge a round by the knowledge and wisdom it extracts per token, never by tokens saved; a failure, a demotion or an extra thread is data, not waste (owner 09-14, 09-20).

## Comms
- Every nudge: read the inbox AND the master dm thread (`send.py read director-thought --dm thought-master --from director-thought`); dm the master only a `[merge-up]` per batch or a blocker (Self-loop below); owner pane lines relayed verbatim to the master, never interpreted; `[red]` engineering findings go to the master by node id (the SM is inactive; the master routes them).
- **Batches only (owner 09-24, verbatim: "Let's switch the formation to you batching research rounds and engine rounds as needed. Directors go back to just working the batches - research batches for director thought until all hypotheses and hypothesis leaves are built out then report results, and engine fix batches for director-engine who only reports back when batch complete no residue."; supersedes the 09-23 self-loop):** work ONLY the batch thought-master hands you, head down on graph build -- director-thought: research batches, ONE results report once every hypothesis and hypothesis leaf in the batch is built out; director-engine: engine-fix batches, ONE report only when the batch is complete with no residue. The master keeps the town trajectory and picks the next batch; between batches, wait for it. A blocker that stops the batch is the only early dm.
- **Rotate YOURSELF, at the line (OWNER 16:14Z 09-24, verbatim, on director-engine's stall: "Director-engine is doing a stall again taking the context limit as a place to stop so the system auto-rotates but being way too conservative stopping at 0.4 of 0.47 so not even triggering the auto function. What can we do to tell them to keep working until rotate and then rotate self don't rely on others to do it. Director-thought is doing it fine but the other one just stalled."):** the meter's "approaching rotation" bands are NOT a stop -- keep working the batch until `[meter]` reads f >= the line (0.47), then run `python3 extensions/agi/bin/rotate.py rotate` yourself (bare, keyed). Nothing rotates an idle pane below the line: the captive hook fires only on a real prompt AT the line. A batch done below the line = its `[merge-up]` line, then the next queued item on your card.

## Rotation
- Bare `rotate.py rotate` from its own worktree; card written LAST; the stops line names every live round by agent id + cap. `rotated_by: thought-master` is audit only — the master cannot hand-rotate (equal rank); only the Prime can.

## Typed decisions (TypeSafe)
- `TYPESAFE_KEY` reaches kids only after SM.103 (`harnesses.<h>.forward_env`); until then typed-decision rounds stop honestly at the key gate. Metrics for every typed-decision round: top-1 agreement with the call actually made, USD per decision, latency; no UI before the replay clears its bar (idea:lm-jev-mcp-sandwich).
- **Keys live (owner 09-23 10:2xZ):** `TYPESAFE_KEY` + `TYPESAFE_KEY2` are in the main .env (5 USD each, both answered HTTP 200) and pi / pi-local forward both to kids -- the key gate above is OPEN; key 2 is a second 5 USD lane.

## Live chains (2026-09-18 02:0xZ)
athena A/B (local-town; TM.27 fetch tool fix) · q4-KV Kid B (A1-heavy) · C2 metronome rhythm-bank (A1-light, hypothesis:c2-kuramoto-metronome-rhythm-bank) · TypeSafe replay r2 (API, blocked on SM.103) · bitnet.cpp A1 tok/s (queued A1-heavy) · kid-persona SFT (banked Camber) · oscillator troves (CC ingestion stays with the master).

## Agent Notes
01:4xZ 09-19 link_ref dropped: it named a dead session scratchpad file (/tmp/claude-1001/.../f7eab981-.../scratchpad/dt-brief.md) that the 01:3xZ storage cleanup removed -- the body IS this doc (schema: absent link_ref = body-is-data). NEVER + Batched lines added under Trunk + cadence (owner 01:1xZ / 01:0xZ / 01:3xZ; mirrors unified brief §4 thought + §2).

02:0xZ 09-19 mirrored from the unified brief on core @71cc9c070 / @b564fa270 (SM sync line 02:03Z): the mur-residue in-loop rule (owner 01:5xZ) and the SM.135 meter-forces-rotation line, both under Trunk + cadence.

thought-master 01:3xZ 09-21: the engine seat `director-engine` (owner order 01:1xZ 09-21, goal:g7.33) inherits every customization here and the unified brief §0-§3, with these deltas on its card `.agi/sessions/quorum/director-engine.md`: owning goal goal:g7.33; worktree .agi/worktrees/post-director-engine on local-maxxing/season2/posts/director-engine/main; pi parents only, no GPU, 2-3 engine rounds live at once within the box memory rule on doc:lm-town-trajectory; suite runs in its worktree, never MAIN; one [merge-up] per batch + one line on the trajectory board. Note for the next brief trim: the unified brief §4 'thought' section still names season1 paths (local-maxxing/season1/*, worktree town-local-maxxing) -- stale since the box move; the live facts are on the cards and doc:lm-local-town-box-facts.
