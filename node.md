---
id: goal:g1.14.1
mint_id: 4fb13d4f30df43ec96f38513065242e9
type: goal
parents:
  - goal:g1.14
next_edges: []
confidence: 0.75
edited_by: director-engine
goal_id: G1.14.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 55a0cfd36d1d52ef
season: 2
seeds:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
status: active
tags:
  - config-maxxing
  - workflow-router
  - template-chaining
  - leaf
title: "G1.14.1: A WORKFLOW \"ROUND\" STAGE CHAINS A PARENT DISPATCH STRAIGHT INTO ITS OWN REVIEW -- one manifest extends/prelude mechanism so round-mur and round-research-review need no hand-authored glue (re-homed from goal:g15 09-25; assigned director-engine)"
town: core
---
# goal:g1.14.1

# goal:g1.14.1

# goal:g1.14.1 — A WORKFLOW "ROUND" STAGE CHAINS A PARENT DISPATCH STRAIGHT INTO ITS OWN REVIEW

```
leaf      one workflow.py stage kind ("round") dispatches ONE parent, waits on its own status (never cli.py wait, which is
          blind to tier:parent rows), and harvests {key, hypothesis, experiments, files, old_tip, new_tip, verdict} from git
          on its done commit -- so a manifest can chain straight into the existing, unchanged review stages (round-mur ->
          merge-up-review; round-research-review -> research-review) instead of the director computing harvest args by hand
          and running the two halves as separate operations
source    the owner 2026-09-24 21:4xZ (verbatim, via the Prime): "Can we include the parent spawn on a specific goal/
          hypothesis node as part of our mur workflow in our configs? So that both the parent spawn and the subsequent mur
          for their result is in one workflow? ... Is it possible to implement with very little code likes but still do it
          robustly?" -- minted by the Prime as hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-
          workflow (eee1800559) under the generic goal:g15 bucket, deleted the same session on the owner's word ("There's
          no need for a hypothesis for the round-mur no? It's just a workflow" / "Just delete it if not pushed"), then
          re-authorized 09-25 00:2xZ once the owner clarified the intent was to re-home it under a properly-scoped goal
          rather than drop it -- config-maxxing (this is a template/manifest-chaining capability, not a bare code change)
home      the G1.14 "ONE workflow router" umbrella -- workflow.py's own architecture goal, empty until now; the CLI-grammar
          tree (goal:g1.25.*) is a different surface (commands.md/jev), not this
rule      KEEP SPLITTING (goal:g5's standing convention): one leaf, one small round
round     hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow (re-minted here, content
          unchanged from eee1800559 -- only the parent goal moved)
writer    director-engine
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Owner verbatim (in-pane, director-engine session e3bf5bfa, 2026-09-25T00:37:38Z; relayed by thought-master as TMM.146/TMM.147, full text confirmed here directly against the session transcript): "Oh woops sorry i misunderstood what prime was saying. Let's re-mint the hypothesis but under the appropriate subgoal or sub-subgoal instead. Somewhere in config maxxing likely as it'll involve another custom template or chaining existing ones in a fresh template." This is why hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow was re-homed here under goal:g1.14 (config-maxxing) as this leaf, goal:g1.14.1, rather than left deleted or re-minted under the generic goal:g15 bucket.
<!-- THOUGHT:END -->
