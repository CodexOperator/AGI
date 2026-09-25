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
Re-minted 2026-09-25 by director-engine. Original (eee1800559, minted by the Prime under goal:g15 -- a generic
bucket, not a properly-scoped home) was deleted the same session on the owner's word ("There's no need for a
hypothesis for the round-mur no? It's just a workflow" / "Just delete it if not pushed") after being routed to
director-engine by dm instead. The owner then clarified the deletion was a misunderstanding: the intent was to
re-home this under the appropriate subgoal, not drop it -- this is config-maxxing (a template/manifest-chaining
capability: workflow.py gains one stage kind + extends/prelude composition so two hand-authored workflows become
one config), which is what goal:g1.14 ("ONE workflow router") already exists to hold, not the generic g15 bucket.
Minted goal:g1.14.1 as the properly-scoped leaf and re-parented here. Technical content (Measured/Build/
FALSIFIERS/TESTS/FILE SCOPE/CEILING) is unchanged from eee1800559 -- it was already Prime-verified against real
line numbers in workflow.py and cli.py; only the parent goal moved. Not yet dispatched: this session verified the
node's new home, not workflow.py's current bytes against the Measured claims above -- re-verify those line numbers
before dispatch, since the tree has moved since 09-24 21:4xZ.
<!-- THOUGHT:END -->
