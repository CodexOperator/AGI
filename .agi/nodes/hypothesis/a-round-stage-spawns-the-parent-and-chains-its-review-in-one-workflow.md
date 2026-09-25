---
id: hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
mint_id: c3dfebd304ea45e5b1978585af9cfd63
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.7
edited_by: belam
scaffold_hash: 87115b934a0b77b3
season: 2
testable_claim: "workflow.py run round-mur with target = a hypothesis dispatches ONE parent (--tier parent --role parent --ladder-tier 0 --branch --detach), waits on the parent's own status until the loop branch carries its done commit, and feeds {key, hypothesis, experiments, files, old_tip = merge-base, new_tip = loop tip, verdict} into the unchanged merge-up-review stages (round-research-review: the research-review stages); a refused dispatch, a dead parent, a missing done commit or a timeout fails the round stage by name and no review stage runs."
thought_session: belam-S2-L5-IV
title: "A round stage spawns the parent and chains its review in one workflow (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow

# A round stage spawns the parent and chains its review in one workflow (assigned: director-engine)

assigned: director-engine -- queued BEHIND goal:g1.25's action-registry round (owner steer 09-24 20:3xZ); one pi-free parent per round (doc:unified-director-brief §1).

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
2026-09-25 00:1xZ belam-S2-L5-IV mints this for director-engine on the owner's words, verbatim: 'Can we include the parent spawn on a specific goal/hypothesis node as part of our mur workflow in our configs? So that both the parent spawn and the subsequent mur for their result is in one workflow? Does our config and template system accommodate this today? If not is the fix minimal ish since all the individual pieces work well. Just the transition from chain growth - mur needs automation. For director-thought it would be the research-focused mur. Is it possible to implement with very little code likes but still do it robustly?' -- and, when the Prime asked for a go instead of routing it: 'Wait why are you checking with me your rules and meter notification should say to keep working until the line then rotate yourself'. Not a new version of hypothesis:workflow-stages-dispatch-as-kids: that node dispatches each stage as a kid; this one dispatches a whole parent round as one stage.
<!-- THOUGHT:END -->
