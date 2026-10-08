---
id: hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
mint_id: 6db191401e5343408032ae40083eb70d
type: hypothesis
parents:
  - goal:g1.14.1
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 3431e4aa9043efad
season: 2
tags:
  - config-maxxing
  - workflow-router
  - template-chaining
testable_claim: "workflow.py run round-mur with target = a hypothesis dispatches ONE parent (--tier parent --role parent --ladder-tier 0 --branch --detach), waits on the parent's own status until the loop branch carries its done commit, and feeds {key, hypothesis, experiments, files, old_tip = merge-base, new_tip = loop tip, verdict} into the unchanged merge-up-review stages (round-research-review: the research-review stages); a refused dispatch, a dead parent, a missing done commit or a timeout fails the round stage by name and no review stage runs."
title: "A round stage spawns the parent and chains its review in one workflow (assigned: director-engine; homed under goal:g1.14.1)"
town: core
---
# hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow

# hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow

# A round stage spawns the parent and chains its review in one workflow (assigned: director-engine)

assigned: director-engine -- home is goal:g1.14.1 (config-maxxing / workflow router); one pi-free parent per round (doc:unified-director-brief §1).

```
round stage ─► review ─► verify                                 round-mur: the merge-up-review stages, unchanged
            └► review ─► verify ─► why ─► brainstorm ─► refute round-research-review (director-thought): the research-review stages, unchanged
```

**Measured (Prime, 09-24 21:4xZ)**
- every stage in extensions/agi/workflows/merge-up-review.json (2) and research-review.json (5) is an LLM stage (label · role · prompt · schema · repeat · chained_from); no stage runs a command
- chaining exists: chained_from hands a stage the prior stage's structured return (workflow.py:1320, 2116, 2315); a failed dependency skips its dependents by name (_failed_dependency)
- the wait is the gap: cli.py wait sees tier:kid rows only (cli.py:2387 "no tier:kid row exists") -- blind to a parent round (director-thought's wait3)
- the harvest args (merge-base, loop tip, files, experiment nodes, verdict) are computed by hand today (the director's HARVEST step; the Prime's PASS build.py)

**Build (config first; code only for the missing trigger)**
1. workflow.py: ONE stage kind "round" -- runs the director's dispatch line on {target}, waits on the parent's OWN status/pid (never cli.py wait), requires the loop branch's done commit, emits {key, hypothesis, experiments, files, old_tip = merge-base, new_tip = loop tip, verdict} from git
2. manifest composition: "extends": "<workflow>" + "prelude": [<round stage>] -- the review prompts stay ONE source
3. two manifests (config): round-mur, round-research-review, registered in config:workflows on pi-free
4. optional: cli.py wait learns tier:parent rows (fixes wait3 for every director)

**FALSIFIERS** a review stage runs on a round with no done commit · the loop branch name is guessed instead of read from dispatch's own output · a dispatch refusal (rc 3) retries in a loop · a review prompt is copied into the new manifests
**TESTS** fake dispatch exits 3 / parent dies / parent times out / parent finishes -> only the last reaches review; both manifests load and chain; existing merge-up-review and research-review runs unchanged
**FILE SCOPE** extensions/agi/bin/workflow.py · extensions/agi/workflows/ (2 new manifests) · .agi/nodes/.geometry/workflows.md · (optional) extensions/agi/bin/cli.py · tests
**CEILING** ~150 lines of code + tests; the director still merges only what cleared and writes the [merge-up] line

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.301 (kid a00-b7f6dcf9-0a130e): re-verified the Measured line citations against current bytes -- they had drifted (now _load_manifest:791, _expand_stages:802, _run_stage_pi:1779, _failed_dependency:2111, run_workflow:2149, pi loop 2280-2373; the original 1320/2116/2315 no longer point at this mechanism). Concluded the claim does not fit the default 40-production-line ceiling without omitting a required fail-closed gate, and requested a 220-line ceiling split into three seams: (1) round execution (~120 lines: dispatch once, parse branch/run identity, wait on parent status, distinguish refusal rc3/death/timeout/missing-done-commit, emit the round payload), (2) manifest composition (~60: resolve extends+prelude once, preserve child type/harness, reject cycles/unknown base), (3) harvest/config (~40: derive the review payload from committed parent data, register two thin manifests via the prime-owned geometry node). The parent answered the rebrief with cut rather than granting the larger ceiling (verdict=pending, production_lines=0) -- correctly honest: not forcing an unsafe partial implementation. Next round should dispatch against this 3-seam plan directly with an explicit raised ceiling, rather than re-deriving it from scratch.
<!-- THOUGHT:END -->
