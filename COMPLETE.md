# COMPLETE.md — post-loop completion reports

**One section per completed loop, newest first.** `HANDOFF.md` is the live
scratchpad of a session; this is the closing record of a loop — what it did and
did not close.

**Same rule as `HANDOFF.md`: replaced whole by default, appended only when the
owner asks** — as here, because the next work continues directly off loop L1 and
both reports need to be readable at once. Every prior report is
`grid.py payload build:COMPLETE.md --version N`, which is what makes replacing
safe and accumulating unnecessary.

Shape and rules: `goal:g1.13`. What it must contain:
`mvp:complete-md-the-post-loop-completion-report`. Why it is written by a
director today and by a small model later: `goal:g14`.

**Every per-goal claim is grounded in a commit, a node diff or a parent report.
A claim that cannot be grounded says so. A decision banked to the owner is a
completion failure** — not the model's, the harness's, for not giving the
director enough to decide with.

---

# Loop L2 — 2026-09-06 — season ladder, morals, daisy-chain (prime director `agi-master`, remote-control)

Appended newest-first at the owner's standing instruction (keep both). Closed at commit `be1607487`; opened at `4235ab1b6`.

## 1. What ran

Ten rounds (iter L2.01–L2.10), three pi parents per round on OpenRouter (`qwen/qwen3.8-27b` parents, `deepseek/deepseek-v4-flash` kids), one kid per target file, each target a `hypothesis:l2*` brief minted by the director. 31 commits on master. Director: one Claude session (`claude remote-control --name agi-master`), context meter 0.31 of the assumed 1.0M at close, no rotation needed before L2 closed. Spend: about $3 OpenRouter for rounds 1–6 ($27 of the $30 top-up remained at that check); subscription untouched. Crons off for rounds 1–2, on from round 2 (grid master-guard landed).

## 2. Scoreboard

| | start | end |
|---|---|---|
| active / deprecated nodes | 1099 / 191 | 1186 / 191 (never dropped) |
| tests | 1487 passed | 1627 passed, 9 skipped (also green under the kid environment) |
| `outcome_coverage` | 0.190 | 0.172 (25 new hypothesis briefs in the denominator; no mvp was the point of this loop) |
| `evidence_fraction` | 0.375 | 0.376; `unevidenced_decisive_verdicts` 0 |
| broken links | 0 | 0 (1356 resolved) |
| disk | 96% | 79% (six pushed repos deleted, 17G) |

## 3. Per active goal

- **goal:g12 (morals parentless → vision → goal), active this loop.** `[moral].md`, `[shape].md` parentless_types=[moral] + season/provenance edge fields, five moral nodes minted by hand as owner from the brief verbatim (commit "The constitution"), write.py refuses moral edits without `--actor owner` (iter-L2.08). Grounded: `.agi/nodes/moral/*`, `hypothesis:l2w1-moral-schema`, `l2w1-shape-parentless-moral`, `l2w2-write-owner-and-payload-types`.
- **goal:g12.3 (ladder, seasons, season.py), minted and closed in substance.** Ladder node + schema (L2.01); report-node floors to 1 + judgment record (L2.02); vision on morals with season edge (L2.03); gate validates season_parents (L2.05); metrics exclude the season edge (L2.05); `season.py status|judge|rollover --dry-run` (L2.07); `send.py` (L2.07); brief heads by read order for all four tiers (L2.07–08); **season-1 pairing done**: 23/23 outcomes, 19/19 bigger_outcomes judged against real goals, 17 visions closed season 1, 17 overviews (L2.09–10); SKILL.md Seasons + Constitution (L2.10). Open: rollover cap counts closed visions (`hypothesis:l2w3-season-py` note); real rollover waits on the owner's vision text (banked).
- **goal:g15 (bugfix and optimization), minted L2.01, always active.** 35 S goals reparented. In-loop fixes: grid master-guard, non-blocking `dispatch.py --detach`, `cli.py done` doubled frontmatter + missing DONE line, agent git-commit guard (belt) + pi-autoresearch `log_experiment` patch off-repo (suspenders), guard scoped to the project repo, bin `--help` smoke test. Open: `hypothesis:l2-graph-hygiene` (round 11).
- **goal:g16 (telemetry), minted L2.01, active from wave 2.** Writer stamps season/loop/model/profile (L2.06); telemetry stamps at done with a real source or `telemetry_source: unavailable` (L2.06, lean 70). Open: session roll-up, cost per aligned outcome.
- **goal:g13.1 (one way in).** Owner's ask delivered: `write_guard.py check` warns on any node changed outside the logged writers; both writers log; smoke path runs it; hook lines in QUICKSTART. After a round it reports 0 warnings. Grounded: `hypothesis:l2w15-write-guard`, iter-L2.03, L2.09.

## 4. Goals closed

None marked `complete`. `goal:g12.3` is closed in substance but its rollover conjunct is banked; marking it complete before the first real rollover would repeat L1's `goal:g4.6` mistake. No `complete` claim in the record lacks a commit.

## 5. Completion-failure categories

- `banked-to-owner`: season-2 visions (the rollover's owner-tier input); pointed Church Slavonic; `goal:s35`.
- `hazard-carry-over`: rollover cap bug; `.agi/bin` stray + L2.09 node sprawl (round 11 in flight); `l2-parent-spawn-nonblocking` landed but pi parents still report ~9-minute silent kids (no live progress signal).
- `verification-blindness`: L2.06 left `dispatch.py` with an unimported name and 1539 tests stayed green (fixed by hand, `test_bin_help_smoke.py` now guards the class); the commit guard broke every kid's test sandbox for one round before it was scoped.
- `late-minting`: none — every brief was minted before its round and committed at mint.
- `attribution-void`: one — commit `9b28e958a` came from a kid's tool auto-commit, not any agent's decision.

## 6. Findings that are not failures

- The daisy-chain transport works hands-off: `claude --remote-control NAME "prompt"` in a tmux window with a TTY answers and stays live; piped, it exits. `rotate.py meter` reads the real transcript; 0.31 at close of ten rounds.
- The constitution gate is real: the first parentless `moral` was approved by the live gate, and the same gate refuses a new parentless idea.
- Three pi parents per round on cheap models did the whole loop for about $3; the director's context, not money, was the budget that moved.
- Parents' `struggles:` lines found every engine defect this loop before the director did.

## 7. Minted or changed in response

`goal:g15`, `goal:g12.3`, `goal:g16` (new); `goal:g12`, `goal:g16` → active; 25 `hypothesis:l2*` briefs with their experiments; five `moral:*`; `.geometry/ladder.md`; 17 `overview:*`; schemas `[moral]`, `[ladder]`, and edits to `[shape]`, `[vision]`, `[goal]`, `[idea]`, `[outcome]`, `[bigger_outcome]`, `[overview]`, `[experiment]`; engine: `rotate.py`, `season.py`, `send.py`, `write_guard.py`, `hooks/agent-git/`, `briefs/prime-director-successor.md`, `test_bin_help_smoke.py`, plus edits to `dispatch.py`, `brief.py`, `cli.py`, `post_wire.py`, `node_writer.py`, `spawn_gate.py`, `metrics.py`, `grid.py`, `write.py`, `snapshot-goals.py`, `driver.sh`, `SKILL.md`, `QUICKSTART.md`.

---

## Session L1.13 — 2026-09-04 → 09-05 — director session, no waves

Not a loop: no dispatch, no kids, no parents. A director session working the
owner's asks directly. Recorded here because it closed things and left things
open, which is what this file is for.

### 1. What ran

Eight commits, all direct director work. No agents spawned, no provider spend.

### 2. Scoreboard

| | start | end |
|---|---|---|
| active nodes | 1094 | 1108 |
| goals | 115 | 124 |
| `outcome_coverage` | 0.187 | 0.190 |
| tests | 1482 | **1493** |
| broken links | 0 | 0 |

### 3. Per goal, how far it got

| Goal | Where it got to |
|---|---|
| **g13.1** edit mode | **Real code, twice.** `write.py` gained `payload <path>`, `payload_text <inline>` and `payload -` (stdin), so editing the file behind a build node is finally a named operation instead of the one node operation with no command. Then payload resolution moved off a hardcoded `source_root()` onto a named `location:` on the node. 10 tests, all verified red. |
| **g1.13** completion report | Minted, chained (`hypothesis` → `mvp` → `build:COMPLETE.md`), and this section is its second use. |
| **g2.12** the FEELING block | Minted and specified in `SKILL.md`; not yet implemented in any writer. |
| **s35** schemas are nodes | Minted `active` with a five-step migration and a count falsifier. **Not started** — see §5. |
| **g9.4 / g9.8 / g9.9 / g9.10** live view | Split from one saturated goal into an umbrella plus three subgoals, each with its own mvp to chase. All `horizon`. |
| **g1.12, g5.2, g14** | Minted `horizon`: loop-flavor tags, mechanical goal splitting, local-maxxing. |
| **g5** goal lifecycle | `[goal].md` widened so a goal may name the build node that produced it; ingest fixed to preserve it. |

### 4. Goals closed

**Zero.** Every goal touched is `horizon` or `active`. Nothing became
`complete`, and nothing was claimed to be.

### 5. Completion failures

- **`banked-to-owner`** — `goal:s35` (schemas are nodes). The owner decided it;
  the director minted the plan and stopped, because every reader globs
  `nodes/<type>/*.md` and a move-first migration breaks three readers against
  files with no `id:` and no `mint_id:`. Correctly banked, but it is banked.
- **`verification-blindness`, twice, and both were the graph not seeing itself.**
  `write.py`, `test_write.py` and `links.py` — the write path and the link
  resolver — **had no build nodes at all**. Both were found by trying to record
  a thought against them and getting "no node file". Nothing checks that every
  tracked source file has a node; `level3.py` mints them on a scan nobody ran.
- **`hazard-carry-over`, avoided once.** Three goals from L1.12 (`g4.9`, `s33`,
  `s34`) were schema-invalid on `confidence`/`seeds`/`tags` and were fixed in
  this session rather than written into a table.
- **Two gaps found and documented rather than fixed:** no prose verb can contain
  `&&` (the script form splits on it — it broke a `thought` in this session),
  and payload writes are whole-file only, with no anchored edit. Both are now
  🔴 in `SKILL.md`, because a rule that cannot be followed for real work is how
  the write path got skipped in the first place.

### 6. Findings that are not failures

**The credential trail on the uninvited director resolves, and it changes the
guard.** The `openclaw`/`hermes` stack runs on a **ChatGPT/Codex OAuth session**
— `auth: oauth` against `api.openai.com`, all five agents on `openai/gpt-5.4`,
plus a second `openai-codex` session in `~/.hermes/auth.json` with
`auth_mode: chatgpt`. There is **no Anthropic credential in that stack at all**,
so the uninvited director was almost certainly a **Codex agent, not a Claude
one** — and it arrived through **`AGENTS.md`, which is a symlink to
`CLAUDE.md`**. It was handed the full director contract by a route nobody
designed. A guard that names one vendor's CLI would guard the wrong thing: what
needs gating is *acting as director*, not which binary does it.

**The larger observation, recorded as `idea:the-graph-is-the-workflow`:** an
agent on a different runtime and a different vendor read one instruction file
and *continued the work correctly for two hours*, with no skill invoked and
nothing scheduling it. The graph was sufficient. A graph with missing pieces is
a structure that states what is absent — a hypothesis with no experiment, a goal
with no mvp, a `payload_ref` with no node — each a hole with a typed edge already
pointing at it, so the set of legal next moves is computable from the structure
rather than argued for in prose. The owner's framing: **the graph is DNA, the
models are ribosomes, the code is protein**, and growth is cross-assembly —
completion happens wherever a reader binds, with the gates as proof-reading.
`goal:g14` reaches the same picture from the efficiency end; this is the
observation that the substrate already behaves that way.

### 7. What was minted or changed

`goal:g9.8`, `g9.9`, `g9.10`, `g1.12`, `g1.13`, `g2.12`, `g5.2`, `g14`, `s35`;
`build:COMPLETE.md`, `build:bin-write`, `build:tests-test-write`,
`build:bin-links`. `[goal].md` and `[build].md` both widened, each with the
shape that stays forbidden stated as plainly as the ones added. `SKILL.md`
reached v32 with three new sections: the write path, `COMPLETE.md`, and the
`FEELING` block.

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

### 6. Findings that are not failures

*(none recorded — this report predates the section, added 2026-09-05)*

### 7. What was minted in response

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
