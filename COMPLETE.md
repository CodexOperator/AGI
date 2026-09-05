# COMPLETE.md — post-loop completion reports

**One section per completed loop, newest first. This file is never replaced.**
`HANDOFF.md` is the live scratchpad and the next director deletes it; this is its
opposite — the closing record of what a loop did and did not close, appended to
and versioned by the grid (`build:COMPLETE.md`).

Shape and rules: `goal:g1.13`. What it must contain:
`mvp:complete-md-the-post-loop-completion-report`. Why it is written by a
director today and by a small model later: `goal:g14`.

**Every per-goal claim is grounded in a commit, a node diff or a parent report.
A claim that cannot be grounded says so. A decision banked to the owner is a
completion failure** — not the model's, the harness's, for not giving the
director enough to decide with.

---

## Loop L1 — waves L1.08 → L1.12 — 2026-09-03 → 2026-09-04

Reported 2026-09-04 by the L1.13 director, from `HANDOFF.md` (unmodified), the
commit log, and goal-node status history.

### 1. What ran

~35 commits. Three phases:

1. **L1.08 – L1.08h.** The parent tier ran live on pi/OpenRouter for the first
   time: 44 parents, cap **25/25 reached and held**, budget refused overflow
   cleanly, parent-spawns-kid observed on both harnesses. The wave then died at
   a **$10/week OpenRouter workspace budget that nothing in the engine reads**.
   Pivot to four CC subagents on disjoint domains: removal guard, evidence gate
   on the commit path, an mvp audit, and the s18 mining survey. All four landed.
2. **L1.09 – L1.11d.** The build-site cohort retired in **one atomic pass** (159
   nodes deprecated with per-node dispositions, 29 verdicts by citation, kits and
   plan deleted in the same commit). Loop-scoped iteration ids landed end to end.
   Waves 6–10 on pi. **A second, uninvited director ran this graph 21:21–23:20
   EDT on 09-03** (commits `L1.10b`…`L1.10f`); `openclaw`/`hermes` crons paused
   and services stopped, reactive daemon named as prime suspect.
3. **L1.12.** Three owner goals minted (`g4.9`, `s33`, `s34`) plus one practice
   iteration: 14 parents, kids editing `provisioning.py`, `dispatch.py` and both
   adapters in-loop as the new skill rule asks.

### 2. Scoreboard

| | start | end |
|---|---|---|
| active nodes | 940 | 1094 (+181 deprecated) |
| `outcome_coverage` (primary) | 0.271 | **0.187** ⬇ honest — guard withholding ≈ −0.1 |
| `evidence_fraction` | 0.317 | 0.375 ⬆ |
| `unevidenced_decisive_verdicts` | 6 | 0 at every grid commit |
| `mvp_count` | 39 | 50 (48 scoring, 2 backward) |
| tests | 1371 | 1482 |
| broken links | 0 | 0 |

The primary fell and that is the guard working: deprecated hypotheses stay in
the denominator by design, and eight waves added hypotheses faster than mvps
closed.

### 3. Per active goal, how far it got

*"nodes touched" = node files referencing the goal that changed during the loop;
a rough activity proxy, not a progress measure.*

| Goal | Touched | Where it got to |
|---|---|---|
| **g3** scoring that motion cannot move | 1 | **Code landed.** Removal guard (`deprecation_score_delta`) plus backward-mvp exclusion, held live twice. Open: detection is a body-language regex, brittle by construction. |
| **g7** nothing silently lost | 2 | **Code landed.** Evidence gate moved onto the commit path (`grid.py commit`); corpus 11 → 0. Open: six prior-director experiments sit demoted, banked. |
| **g4.8** many loops at once | 5 | **Mostly proved.** Cap held, overflow refused cleanly, parent-spawns-kid observed. Clause 2 (a parent demoting unaided) never separately observed — made moot at acceptance rather than tested. |
| **g4.1** parallel kids collide | 8 | **Thesis observed live, not fixed.** Two director-minted nodes vanished uncommitted mid-wave. Mitigation is a human rule ("commit at mint"), not an engine guard. |
| **g13 / g13.1** one read/write path | 5 / 1 | `write.py` used in anger all loop; scalar-type bug found and fixed. **91 deprecated nodes still schema-invalid** on `tier` from the L1.09 pass. |
| **g1.10** commands declared, not memorised | 5 | The runner became the only trusted verify path — it caught a `commands.py` breakage that direct `pytest` missed. Open: `verify` runs `smoke` before `grid-commit`, so the metric lags one gate pass. |
| **g1.11** a fresh capped key per spawn | 3 | Kids edited `provisioning.py` in-loop. Core defect stands: it knows the per-key cap, not the workspace weekly budget, so a whole wave 403s *after* minting. |
| **g4.7 / g4.9** healing, hung processes | 1 / 4 | `g4.9` only existed from 12:30 on the final day. Wave-6 parents sat at 25/25 for 34 min; `iter-1075` outlived a 20-minute timeout by over an hour. Nothing enforces `agent_timeout_mins` under bare `dispatch.py`. |
| **g5** goals are a lifecycle | 6 | Structural only: status semantics, and the focus cap raised 15 → 18 to fit three new goals (banked, reversible). |
| **g9.7** one render, two readers | 1 | Briefing data contract verified byte-identical across window sizes. `briefing.py` still re-reads idea status from disk. |
| **s31** a scaffold ships schema-invalid | 1 | Barely touched, and the loop *created* new instances: 91 invalid `tier` values, two nodes with a second appended THOUGHT block. |
| **s33** the docs say what the tree does now | 4 | Minted 12:30, one practice iteration. `QUICKSTART.md` still stale. |
| **s34** close every carried hazard in-loop | 12 | Most active goal at close: four hypotheses, kids editing three engine files. **Of 16 carried hazards, roughly 2 verifiably closed.** |
| **g9.4** the live viewport | 4 | Shipped, and rejected on review — see §5, category 1. |

### 4. Goals closed — and one closure the record cannot substantiate

**Zero.** No goal node's `status` changed to `complete` in any commit from
2026-09-03 onward. Sixteen goals were `active` for the whole loop.

**One pre-existing `complete` is not substantiated by the code that existed at
the time:** `goal:g4.6` (one spawn path; a harness is an adapter named in
config) was set `complete` on **2026-09-01** (`80eb607df`), while the
`claude-code` adapter was found *unimplemented* during L1.08 and only written in
`L1.08h`. The goal was right; the closure was two days early and nothing checked.

### 5. Completion failures, by category

Every one of these is a harness gap — the director had no mechanism to see the
thing in time. Failure here includes decisions correctly banked to the owner.

1. **Saturation — the goal was too big to aim at.** `g9.4`, `g13`, `g5`. One goal
   carrying five independent deliverables and one mvp. `g9.4` came back as a
   list view: correct against the words, nowhere near the intent. A model can
   satisfy a saturated goal and miss it entirely with no signal that anything
   went wrong. `goal:g5.1` names this; nothing detected it, so `goal:g5.2` was
   minted to detect it mechanically and `g9.4` was split three ways.
2. **Ceiling discovered by dying, not by reading.** `g1.11`. A third spend limit
   nothing in the engine reads killed 44 parents' work at 403 mid-flight. The
   constraint was learned from failure logs — the most expensive channel there is.
3. **Late minting.** `g4.9`, `s33`, `s34` all minted at 12:30 EDT on the last day
   and got one practice iteration. The work had been visible for two sessions —
   in handoff prose, where nothing schedules it.
4. **Hazard carry-over.** 16 bugs found in-loop were written into a handoff table
   instead of fixed in-loop. A handoff table has no owner, no falsifier and no
   metric. `goal:s34` exists to end this and itself closed ~2 of 16.
5. **Banked to owner.** Two: raising the OpenRouter workspace budget (a provider
   spend setting, outside director authority) and whether to restore six demoted
   experiments. Both correctly banked. The failure is that the first silently
   gated roughly half the loop's throughput with no way to know until it hit.
6. **Verification blindness.** `driver.sh` is not under pytest, so the suite was
   green while the entry point was dead (`L1.10d` → fixed in `L1.10e`). A
   non-hermetic test fails whenever real keys are outstanding. Guards that had
   never failed on purpose passed while not measuring the thing that broke.
7. **Attribution void.** An uninvited second director ran the graph for two hours
   and it took forensics to establish it was not the owner. Had `goal:g10.1`
   existed, the `build:HANDOFF.md` version would name the session that wrote it.

### 6. What was minted in response

All `horizon` — declared, not in flight.

- **`goal:g9.4`** returned to `horizon` with the owner's review, and split:
  **`goal:g9.8`** (one hook layer, one frame stream, player avatar, `f` to dock
  into a node's versions and chats, LOD-on-approach, `z`/`x` zoom anywhere,
  recursive in both directions), **`goal:g9.9`** (the spider skin — every node on
  a living web, ASCII spiders crawling edges and messing with the nodes they work
  on), **`goal:g9.10`** (the space skin — systems, bodies, ships sized by tier,
  modular station/terraformer/colony tiers, a player ship that docks the same way).
- **`goal:g1.12`** — loop flavor is a tag: `research`, `exploration`,
  `development`, `implementation`; nested so a research loop collapses to one
  node at one zoom and resolves into its chains at the next.
- **`goal:g5.2`** — splitting a goal is mechanical: classifiers and encoders
  score saturation, propose sub-goals and assign each one's loop flavor, with the
  classifier output as in-node evidence.
- **`goal:g1.13`** — this file: a loop ends with a completion report, generated
  rather than remembered. Chain: `hypothesis:a-loop-that-does-not-report-its-own-completion-repeats-its-gaps`
  → `mvp:complete-md-the-post-loop-completion-report` → `build:COMPLETE.md`.
- **`goal:g14` — local-maxxing** (new long-term): the smallest competent model
  everywhere, mechanistic tagging at mint, tags routing the model for the next
  node in a chain, specialists sharpening into a lattice of hyper-narrow tuned
  models. Its addendum names the first slot worth filling — **a classifier that
  spots exactly the gaps in this report from a parent's own report** — and frames
  the lattice as the middle ground between a deterministic decision tree and
  prompt-maxxing, where an instruction that should be harness code is handed to a
  model as text and becomes a Markov chain.
