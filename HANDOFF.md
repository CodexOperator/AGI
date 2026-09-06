# SESSION HANDOFF — 2026-09-06: LIVE SCRATCHPAD — loop L2 opened (prime director `agi-master`, remote-control, session in progress)

**Owner's instruction 2026-09-06: this handoff is carried forward, not replaced** — the 2026-09-05 plan below stays and the live session diffs it in place. Successors: read before touching.

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale. Prior sessions are in
the grid: `grid.py payload build:HANDOFF.md --version N` (the L1.13 director
session is the version before this one).

**Closed loops are recorded in [COMPLETE.md](COMPLETE.md)** — untouched this
session, by the owner's instruction; no loop ran. It holds L1 and L1.13. Loop
L2, planned below, appends to it when it closes (owner asked to keep both).

**The design this plan implements is in
[`.agi/context/season-ladder-and-morals-brief.md`](.agi/context/season-ladder-and-morals-brief.md).**
Read that first, whole. It is the record of a long owner/director brainstorm —
the tier ladder, the morals as a constitution, the prayers and reference texts,
telemetry, comms — and every wave below mints nodes from it. Do not re-derive it.

## §0 State block

| | value |
|---|---|
| active nodes / deprecated | **1186** / 191 after L2.10 (1099 at session start; never dropped) |
| goals | 124 (16 active) |
| `outcome_coverage` (primary) | 0.190 |
| `evidence_fraction` | 0.375 |
| tests | **1627** passed, 9 skipped after L2.10, also green under `AGI_TIER=kid` + hooks env (was 1487 at session start) |
| broken links | 0 (1270 resolved, 2026-09-06) |
| crons | **ON** since round 1 landed the grid master-guard: `grid_sync` every 5 min, `branch_push` hourly at :07. Kill switch: `write.py cron:crons "set crons_live false"` then `crons.py apply`. |
| branch | `master`, clean, worktree branch merged. Prime director works on master (brief §2). |
| agents live | round 6 parents + kids (see §0.5 checklist); director meter 0.296 of 1.0M at L2.10 dispatch — rotation expected right after round 10 or 11 review; OpenRouter $27 remaining of the $30 top-up after six rounds, rotates at 0.35 via `rotate.py spawn --name agi-master-2` |
| spend this session | OpenRouter balance $5 at start; owner topping to $30 (the binding cap). Fallback if it runs dry: `--harness claude-code`, opus parents / sonnet kids, until the subscription taps out. |
| disk | 79% (was 96%); 17G freed 2026-09-06 — see §0.5 item 4 |
| this session | prime director, `claude remote-control --name agi-master --permission-mode bypassPermissions` in tmux `agi-rc`, log `.agi/sessions/remote-control.log` (carries `usage` lines = context meter for rotation) |

## §0.5 Session 2026-09-06 — L2 opened. Owner answers, settled (do not re-ask)

1. **Authority is open-ended**: loop until L2 closes; minimise owner decisions, combine several into one, morals as the tie-breaker.
2. **Wave order changed**: wave 1 → **wave 1.5 (daisy-chain path)** → wave 2 → 3 → 4 → 5. Wave 1.5 = ladder node with `director_rotate_at: 0.35`, rotation script (write handoff live, launch successor `claude remote-control --name agi-master-N` in tmux `agi-rc`, successor reads handoff before replacing), **plus an unsanctioned-write check** (owner's ask): the repo mechanically detects a node or payload edit that did not go through `write.py` and warns to redo it properly.
3. **Rotation 0.35 and council quorum (§7) confirmed as written.**
4. **Disk**: owner granted deletion of every other repo whose remote is up to date. Done this session: pushed the one unpushed ML branch, christenArts main (+9), two hermes stashes as `stash/*` branches, belam's dirty canvas json as `wip/2026-09-06-canvas-progress`; then deleted `machinelearning` (14G), `machinelearning-hermes`, `belam-codex`, `christenArts`, `agi-tree`, `fencePros`, `/tmp/pytest-of-ubuntu` (2.5G). **Left**: `machinelearning-modularnn-spike-viz` (787M, not a git repo, no remote to verify — banked), `fantasia` (worked example, dirty), tiny repos. Grid storage: git already delta+zlib packs the grid; `git gc` took `.git` 63M → 23M. Zips would not beat pack deltas — no grid compression work needed.
5. **Spend**: $30 OpenRouter is the cap once topped. Subscription was exhausted 2026-09-04 by stress-testing; the fallback ladder is opus parents / sonnet kids at max.
6. **Successor first prompt — TESTED, works hands-off** (2026-09-06 02:47): `claude --remote-control <name> --permission-mode bypassPermissions "<prompt>"` run in a tmux window **with a TTY (no pipe to tee — piping makes it print-mode and exit)** takes the prompt, answers, and stays live under Remote Control with a claude.ai/code URL. No owner tap needed. This is the rotation transport.

**Live checklist (this session)**
- [x] smoke 1099 active / 1290 total, tests 1487, disk freed, handoff carried
- [x] wave 1 mint: `goal:g15`, `goal:g12.3`, `goal:g16`, `g12`→active, 35 S goals → `g15` (commit after this line)
- [~] wave 1 dispatch, 2 parents at a time, one kid per schema file. Briefs = `hypothesis:l2w1-*` (7). `spawn.parallel` set to 1 so one dispatch call = one parent. Iter id `L2.01`. **Round 1 landed** (iter L2.01, commit after this line): `[shape].md` parentless_types=[moral] + 3 edge fields (kid also set goal/idea min_parents 1 — accepted, brief for round 3 amended); `[ladder].md` + `.geometry/ladder.md` (proved); grid master-guard in `grid.py` (proved, 8 tests). Tests 1497. **Round 2** (iter L2.02) kids done, two parents still reviewing at 04:30: `[moral].md` (parent accepted; gate demoted to lean-proved:50 because the kid omitted `--evidence-runs`), report floors (same demotion), `rotate.py` + `briefs/prime-director-successor.md` + `test_rotate.py` (kid says 1501 tests). **A kid ran `git commit`** (`9b28e958a`, swept all three kids' work into one commit on master — kept, merge-not-rebase; guard brief `hypothesis:l2-agent-git-commit-guard` minted under g15). Tests on the tree: 1501 passed. **Round 3 landed** (iter L2.03): `[vision].md` (moral parents, season_parents, moral_adherence), `[goal].md` + `[idea].md` (vision parents, authors), `write_guard.py` + logging in `node_writer.py` + smoke step in `driver.sh` + hook lines in QUICKSTART — **the owner's unsanctioned-write check works live**: its first run caught a kid's hand edit. Parent re-graded to 60 because `snapshot-goals.py write_frontmatter` is still unlogged (follow-up noted on the hypothesis). **Round 4 landed** (iter L2.04): `[experiment].md` payload_ref + location (proved); `dispatch.py --detach` + parent brief polls `cli.py status` (lean 80); commit guard `hooks/agent-git/{pre-commit,pre-push}` exported via `GIT_CONFIG_*` by dispatch — **verified live: a kid commit is refused, a plain commit passes** (lean 80). **Round 5 landed** (iter L2.05): gate validates `season_parents` by type + grandfathers earlier seasons (proved; parent caught a crash in a `post_wire.py` caller the kid's report claimed was updated — fixed in review); metrics read traversable edge fields from `[shape].md` (parent verified byte-identical output; `outcome_coverage` 0.19→0.176 is the 21 new L2 hypothesis briefs in the denominator, not the code); `cli.py done` merges a doubled frontmatter, marks `done_line: missing`, logs final bytes (lean 60; guard warnings 3→2). **Round 6 landed** (iter L2.06): writer stamps season/loop/model/profile from dispatch env (lean 75); telemetry stamps at done with a real source or `telemetry_source: unavailable` (lean 70; read the experiment for which source pi exposes); **write.py owner-only moral guard NOT built** — the kid tested the old write.py and reported disproved; re-run note on the hypothesis, goes in round 8. Guard warnings now 0 after a round. **Round 7 landed = wave 3** (iter L2.07): `send.py` inbox verb (proved, live round trip ok); `season.py status|judge|rollover --dry-run` (lean 55; **season-1 baseline measured**: tier 0 plans 12 active/106, reports 16/23, ratio 0.22, 83 plans without reports, 23 reports with no judged_against; tier 1 plans 8/21); brief heads for director + prime_director only (lean 55) — kid/parent heads, `--evidence-runs` in the done template and `set FIELD VALUE` syntax are the re-run note on `hypothesis:l2w3-brief-heads`. **Round 8 landed** (iter L2.08): write.py refuses moral edits without `--actor owner` (proved, verified live); kid + parent constitution heads (lean 50: kid head has the prayers and the `set FIELD VALUE` line, parent has prayers + words of Jesus; check the done template carries `--evidence-runs`); `test_bin_help_smoke.py` runs `--help` on 40 bin scripts, 34 pass, 6 explicit skips (lean-disproved 60 on the word *every* — the guard is in the suite). **Round 9 landed = wave 4 pairing** (iter L2.09): all 23 outcomes carry `judged_against` (tier 0 reports without a judgment: 23 → 0); 17 visions retagged season 1 + closed; second-writer log landed (lean 85); **tier-1 pairing blocked** (chain bigger_outcome→outcome→mvp reaches no goal) — re-run note derives it via the outcomes' new `judged_against`. Briefs were: `l2w4-outcomes-judged` (tier 0, every outcome gets judged_against via `season.py judge`, no fabricated outcomes) + `l2w4-tier1-and-visions` (bigger_outcomes for active LT goals, 17 visions → season 1 closed, overviews only where a bigger_outcome exists) + second-writer log follow-up on `l2w15-write-guard`. **Round 10 landed** (iter L2.10): commit guard scoped to the project repo (suite 1627 green normally **and** under the kid env); tier-1 pairing 19/19 bigger_outcomes + 17 overviews (parent verified; verdict flipped only on the three-part wording); SKILL.md Seasons + Constitution. **Round 11 live** (iter L2.11, window `p-hygiene`): `l2-graph-hygiene` only. **L2 report appended to COMPLETE.md** (newest first). L2 closes when round 11 lands; the real rollover waits on the banked season-2 decision (§6 item 9). Round 11 = wave 5 close: `season.py rollover` dry then real (≤3 season-2 visions on the morals), SKILL.md **Seasons** + **Constitution** sections, `COMPLETE.md` **appended** (owner asked to keep both) with the L2 report, seven sections. Round 5 = `l2-done-doubled-frontmatter` + wave 2 starts: briefs `hypothesis:l2w2-*` minted (gate season_parents, writer stamps, write.py owner-only morals + payload types, metrics season edge, telemetry stamps under `goal:g16`, now active). Three parents per round.
- [x] five moral nodes by hand, `--actor owner`, text sliced verbatim from the brief (ESSENCE / QUESTION / IN PRACTICE / VIOLATED WHEN / REFERENCE; faith carries §4 whole, 183 lines). Gate approved `parents: []` for all five — `[shape].md` change proven live.
- [~] wave 1.5 (rotate.py + write_guard.py + grid guard landed; follow-ups: second writer log, non-blocking spawn, commit guard): briefs minted `hypothesis:l2w15-rotate` (rotate.py meter/spawn/status + successor prompt), `l2w15-write-guard` (owner's unsanctioned-write check, under goal:g13.1), `l2w15-grid-master-guard` (crons come back on after it lands). grid-guard parent dispatched alongside round 1 (window `p-gridguard`); rotate + write-guard dispatch when round-1 slots free. RC successor test: done, see §0.5 item 6.
- [ ] waves 2–5 per §3

## §1 What the 2026-09-05 session did

- [x] Whiteboard photo → `.agi/context/images/season-cycle-whiteboard-2026-09-05.webp` (1200×900, 80 KB).
- [x] Read `HANDOFF.md` and `COMPLETE.md` at owner's request; neither erased until this replacement.
- [x] Found the graph already holds most of the design: `goal:g12`, `g12.1`, `g12.2` (morals, caps, season edge — all `horizon` since 2026-08-29), `[vision]`/`[overview]`/`[bigger_outcome]` with `season:` fields, 0 overviews ever minted, 17 visions none meeting their schema.
- [x] Brainstormed the ladder, roles, seams, morals, questions, reference texts, prayers, telemetry, comms with the owner over six correction rounds. **All owner-approved.** Written to the brief.
- [x] Measured the season-1 data point: subgoal 71 / outcome 23; long-term 18 / bigger_outcome 19; vision 17 / overview 0; short-term 35 unplaced; outcomes have 0 goal parents.
- [x] **Doc pass, 2026-09-06 (director by hand, owner's ask):** `GOALS.md` preamble no longer says `agi-tree`; 10 pre-agi build nodes retired (`autoresearch.*`, `run-loop.sh`, `start.sh`, `schema.sql`, `context/impl/*`) and their files removed, plus file-only leftovers (`_benchmark.py`, `context/kits/`, `context/plans/`); census rows pruned; driver, find-root and agent-prompt headers rewritten for the `.agi/` layout. `context/refs/` kept (31 nodes cite it); `TODO.md` kept as the retired archive.
- [x] **Director tier declared:** `harnesses.claude-code.models.director = claude-fable-5-1`, `effort: {director: max}`; the adapter accepts a per-tier effort map (one test, verified red). **`brief.py` has no director brief yet** — `--tier director` fails there until L2 wave 3.
- [ ] **No schema touched, no ladder code.** That is loop L2.

## §2 🔴 Where it stops, and the next command

```bash
cd /home/ubuntu/work/agi
git status --short && git branch --show-current          # merge the worktree branch first if still separate
bash extensions/agi/driver.sh --smoke --max-iters 1       # 1109 active, must NOT drop
python3 extensions/agi/bin/commands.py run tests          # 1493
```

Then **open loop L2, wave 1**, below. Every wave is pi parents on OpenRouter via
`dispatch.py <root> <iter> --tier parent --target <node>`; the director never
does kid work (moral: faith). Mint the hypothesis/goal node for each target
first, commit, then aim parents at it.

## §3 Loop L2 — five iterations, dependency-ordered

Owner's budget: **about five iterations**, $30/week OpenRouter, kids at the
DeepSeek V4 Flash price point, parents `qwen/qwen3.8-27b` (config as is).
Assign **one kid per file** — several schema files change and two kids on
`[shape].md` will collide.

### Wave 1 — geometry and schema (all parallel, 6–7 kids; no engine code)

Mint first, by hand through `write.py`, so the wave has parents:
- `goal:g15` **Bugfix and optimization** — long-term, `active`, always active, exempt from `max_goals_active`. Parent of all 35 S goals (reparent in this wave: `write.py goal:sNN "link parents goal:g15"` ×35 — script it).
- `goal:g12.3` **The tier ladder, seasons, and `season.py`** — under `g12`. Carries §1 of the brief.
- `goal:g16` **Telemetry per node, propagated up the ladder** — long-term, `horizon` until wave 2.
- Flip `goal:g12` → `active`.

Kids (one file each):
1. `context/schemas/[moral].md` — shape in brief §3; `spawn: allowed_parents: [], min_parents: 0`; body regions ESSENCE/QUESTION/IN PRACTICE/VIOLATED WHEN/REFERENCE; `grounded_in`, `axis`, `edited_by: owner`.
2. `context/schemas/[ladder].md` + `.agi/nodes/.geometry/ladder.md` — tiers table, `current_season: 1`, caps (5 morals, 3 visions), `budget_usd_week: 30`, spawn profiles, read-order-by-role, zoom numeric. Parented on `goal:g12.3` (same move as `.geometry/crons.md`).
3. `context/schemas/[shape].md` — `parentless_types: [moral]` (creation-time, grandfather note); `edge_fields` add `season_parents: {role: season, traversable: false}`, `grounded_in: {role: provenance, traversable: false}`, `authors: {role: provenance, traversable: false}`.
4. `[outcome].md`, `[bigger_outcome].md`, `[overview].md` — **drop floors to `min_parents: 1`**; add `judged_against`, `lens`, `alignment`, `adjust`, `season`, telemetry fields; overview adds `moral_audit`. Three files, may be one kid or three.
5. `[vision].md` — `allowed_parents: [moral]`, `min_parents_by_type: {moral: 1}`, `season_parents: [overview]`, `moral_adherence`, cap 3 from season 2.
6. `[goal].md` + `[idea].md` — long-term may name a vision parent (grandfathered); S goals take `goal:g15`; idea gains `authors`, `allowed_parents: [goal, vision]` (`g12.2`).
7. `[experiment].md` — `payload_ref` + `location` allowed (experiments are build nodes in practice).

Then, **director by hand, owner text verbatim from the brief**: mint the five
moral nodes (`write.py create moral faith --actor owner …`), `moral:faith`
carrying the full REFERENCE (§4 of the brief). Needs kids 1 and 3 landed.

Gate for the wave: smoke count does not drop; `links.py schema` shows no new
violations; `spawn_gate` accepts a `moral` with `parents: []` and rejects a
new parentless `idea`.

### Wave 2 — gate, writer, stamps (depends on wave 1; parallel by module)

- `spawn_gate.py` — reads `[ladder]`; validates `season_parents` by type; grandfather flag for pre-season-2 nodes.
- `node_writer.py` — stamps `season`, `loop`, `model`, `profile` on every mint.
- `write.py` — refuses `moral:*` unless `--actor owner`; experiment payload verbs work.
- `metrics.py` — excludes `season_parents` from chain depth and coverage.
- `cli.py done` / `post_wire.py` — stamp `tokens_in/out`, `cost_usd` (OpenRouter generation lookup via the per-spawn key — **investigate first**, may be its own hypothesis), accepted diff bytes.
- Tests **verified red** for every rule; run through `commands.py run tests`.

### Wave 3 — `season.py`, comms, briefs (depends on wave 1; parallel with wave 2)

- `season.py status` — the count table + ratios + mismatches (plan without report, report without plan) + cost per tier. `judge <report>` scaffolds the judgment fields and derives `lens`. `rollover --dry-run`.
- `send` — one verb, looks like a session send; kid→parent, parent→director, director→director-above, council; inbox file under `sessions/` for pi, direct for CC.
- Brief templates ×4 (kid / parent / director / prime director) with the prayer heads in the brief's read order. `dispatch.py` picks the template by tier and role.

### Wave 4 — pair season 1 (depends on 2 and 3; the expensive wave)

- Every active-goal outcome gets its subgoal as `judged_against`; mint missing outcomes for the 8 active subgoals only.
- Mint `bigger_outcome` for the 4 active LT goals; overviews for the visions that actually directed work.
- Retag all 17 visions `season: 1`, `status: closed`. Legacy build-site outcomes stay, labelled season 1.
- `season.py status` becomes the season-1 baseline. Most alignments will be `unknown` — that is the honest first data point, not a failure.

### Wave 5 — rollover and report (depends on 4)

- `season.py rollover` (dry-run first, then real) → ≤3 season-2 visions with `parents=[morals]`, `season_parents=[overviews]`, `moral_adherence`, `proposes_goals`; `current_season: 2`.
- `SKILL.md` gains **Seasons** and **Constitution** sections (read order by role, the one comms verb, death per role).
- `COMPLETE.md` **appended** (owner asked to keep both) with the L2 report, seven sections.

## §4 Traps to carry

0. **Found in L2.01, bank to `goal:g15` (mint a hypothesis when a slot frees):** (a) a pi parent's blocking `dispatch.py --tier kid` call was killed by the 20-min tool timeout while the kid kept running; the parent recovered from the manifest but should not have had to — spawn must be non-blocking or the timeout must not apply to a spawn call. (b) `cli.py done` left a doubled frontmatter block in a kid's node (parent merged it by hand). (c) one kid never emitted the DONE contract line. (d) Monitoring parents: the dispatch log ends with `reaper: finished` **before the parent exits** — wait on the parent pid from `spawn_budget.py status`, not the log. (e) Kids omit `--evidence-runs` on `cli.py done` and get gate-demoted to 50 even when the parent accepts — fold into `hypothesis:l2-done-doubled-frontmatter` (kid done template). (f) A kid committed on master (`9b28e958a`) — an autoresearch `log_experiment` auto-commit; `hypothesis:l2-agent-git-commit-guard`. (h) The rogue-commit root cause is **outside the repo**: `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/pi-autoresearch/index.ts` `log_experiment` auto-commits; patched on this box to skip when `AGI_TIER` is kid/parent (L2.04). A fresh box needs the patch again or the hooks-path guard alone (which is enough). (i) `write_guard.py check` warns on every kid node after a round until `cli.py done` logs the final bytes — addendum on `hypothesis:l2-done-doubled-frontmatter`. (k) **The commit guard breaks kid test suites**: under `AGI_TIER=kid` + hooks env, 99 tests fail / 71 error (`tier kid may not commit`) because tests commit in temp repos; parents strip `AGI_*` to verify. Fix = scope the hooks to the project repo — `hypothesis:l2-commit-guard-scope`, round 10, **first**. (l) The outcomes kid wrote 5 nodes for one sweep (an empty scaffold, `experiment/season:l2w4.md`, two verdicts) — harmless, links resolve; deprecate-and-move is a g15 cleanup item. (j) **L2.07 first launch died**: `dispatch.py` called `spawn_gate.read_ladder_season` with no import (L2.06 stamps kid); suite green because nothing calls `main()`. Director added the import by hand (thought on the build node) and minted `hypothesis:l2-bin-help-smoke` under g15. Re-launched. (g) `.agi/bin/analyze-chat-structure.py` exists (L1.11c stray, referenced by `experiment:a01-c6a5fb12-52f818`); S1 says no `.agi/bin/`. `driver.sh` **still prefers** `$PROJECT_ROOT/bin/{snapshot-build-site,inject,render-context}.py` (lines 222, 240, 241) — the stray has a different name so nothing is shadowed today, but the directory existing is the hazard S1 names. Clean-up is a g15 item: retarget the experiment's payload and remove the directory.

1. **Prose verbs cannot contain `&&`** (`write.py` splits on it). The Slavonic and the verbatim essence contain none, but check before a `payload_text`; use `payload <file>` for the moral bodies.
2. **`write.py create --payload` stamps `link_ref`, not `payload_ref`** — set `payload_ref` by hand after.
3. **Payload writes are whole-file.** Engine surgery is ordinary tools plus a `thought` afterwards.
4. **Attribution is load-bearing in the constitution.** Jeremiah 31:33 and Ephesians 6 are not Jesus; the brief labels them. Keep the labels.
5. **This branch is a worktree branch, not master.** Merge before dispatching, or every parent commits off master.
6. **Worktree sessions cannot run git inside loops, heredocs or with computed arguments** — the harness refuses. Batch `write.py` calls in a script file; run moves and removals as plain single commands.

## §5 Known-good verification sequence

```bash
bash extensions/agi/driver.sh --smoke --max-iters 1 && echo SMOKE_OK   # 1109 active
python3 extensions/agi/bin/commands.py run tests                        # 1493
python3 extensions/agi/bin/snapshot-goals.py --render --check
python3 extensions/agi/bin/links.py links                               # 0 broken
python3 extensions/agi/bin/links.py schema
python3 extensions/agi/bin/grid.py commit --all
git push origin <branch>
```

## §6 Owner decisions, 2026-09-06 — settled, do not re-ask

1. **Merged.** The doc-pass branch went to master with owner permission; the director merged it under that grant only.
2. **Church Slavonic** — unpointed text stands for now; pointed text or an Ostromir passage later, by hand.
3. **`goal:s35` still waits.**
4. **A parent's `adjust` rewords only.** Splitting a subgoal is a director's call through the lens.
5. **Cost lookup** is the first hypothesis of wave 2, not an assumption; pi usage logs are the fallback.
6. **Camber Cloud waits** for `g16` data — but may be tried sooner on **low-level kids fine-tuned to the read/write paths**, once every path is behind an action word. The gate is **saturation**: do not spend GPU hours until the task set saturates the untuned model.
7. **Branching, decided** — see the brief §2 "Branches mirror the ladder": one branch per parent loop, one long-lived branch per director, master owned by the prime director; kids never branch. **Grid node refs are branch-blind** (one linear ref per mint id, parent = current tip), so `grid.py commit --all` runs **only on master, after a merge**; session refs may be written from anywhere. Wave 2 adds a guard to `grid.py` that refuses `commit --all` off master.

8. **Merge, not rebase**, when a director takes a parent branch (owner, 2026-09-06). Rebase rewrites hashes the grid may cite.

9. **BANKED 2026-09-06 (L2 close) — season-2 visions, one decision.** `season.py rollover` is ready except for the owner-tier input: up to 3 season-2 visions, each `parents: [the five morals]`, `season_parents: [season-1 overviews]`. A vision is owner text; the director does not invent one. **Recommendation** (grouping the 7 active top-level LT goals): (1) *The ladder runs itself* — G12 seasons + G16 telemetry + G5 lifecycle; (2) *One hand, one path* — G13 write.py as the only hand + G7 nothing silently lost; (3) *Antifragile by default* — G15 bugfix in-loop + G3 scoring motion cannot move. Reply with three lines of vision text (or "use the recommendation") and the successor runs `season.py rollover` for real (after the cap-count fix on `hypothesis:l2w3-season-py`). Until then season 1 stays open and the loop keeps working g15/g16 items.

## §7 Proposed, owner to confirm — none blocking wave 1

- **Council quorum and record** — brief §6 "Council": convened one tier up only, quorum = convener + affected directors, one-seam time box, co-authored idea node as the record.
- **Director rotation** — brief §6 "Director rotation": `director_rotate_at: 0.35` on the ladder node; the parent above respawns a rotating director on the same branch and worktree; the prime self-rotates and daisy-chains; rotation writes the handoff only, and a successor reads before replacing. Wave 3 builds the trigger and the respawn; wave 1 declares the field.
