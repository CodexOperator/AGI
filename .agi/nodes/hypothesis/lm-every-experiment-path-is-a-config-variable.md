---
id: hypothesis:lm-every-experiment-path-is-a-config-variable
mint_id: 5c50528c87d246508da85bc012de8785
type: hypothesis
parents:
  - goal:g5
next_edges: []
confidence: 0.6
edited_by: director-thought
scaffold_hash: 9122847394ca5548
season: 2
tags:
  - local-maxxing
  - config-max
testable_claim: Every repo-relative filesystem path the local-maxxing experiment chains rely on (scripts under datasets/ and .agi/context/local-maxxing/, and the commands their nodes cite) resolves at runtime from paths.local_maxxing in .agi/config.json through one shared reader, each variable resolving to the exact literal it replaced; absolute box roots are deliberately left as literals, proposed as separate box.* cells, not converted by this pass; falsified by any literal left in a converted script, any changed resolved value, any converted script that no longer runs, or any file under extensions/ touched
thought_session: belam-S2-L5-I
title: "CONFIG-MAX PASS (owner 09-23): every path in the local-maxxing experiment chains is a named variable under paths in .agi/config.json, read through one shared reader, values unchanged"
town: local-maxxing
---
# hypothesis:lm-every-experiment-path-is-a-config-variable

# hypothesis:lm-every-experiment-path-is-a-config-variable

## Hypothesis
**Owner (2026-09-23 ~08:4xZ, director-thought pane, verbatim on goal:g14):** "We need to template max and config max everything. Add new standing order to parent and kid docs that paths are always stored in variables that are stored in a config. Then do a pass doing that for any paths in the experiment chains in this town goal bundle."

**Claim.** Every filesystem path the local-maxxing experiment chains rely on -- in their scripts (under `datasets/` and `.agi/context/local-maxxing/`) and in the commands their nodes cite -- resolves at runtime from ONE config section, `paths.local_maxxing` in `.agi/config.json`, through ONE shared reader, with behavior unchanged; absolute box roots (single-machine paths such as `/data/ml/models`) are deliberately left as literals, proposed as separate `box.*` cells, not converted by this pass.

```
inventory   2026-09-23: 51 tracked .py/.sh scripts scanned · 19 carry path literals · 40 literals (15 files .agi/context/local-maxxing · 3 datasets/switch-rule · 1 datasets/kid-sft)
config      .agi/config.json -> paths.<key> (a relative value resolves from the repo root) · one reader shared by .py and .sh
behavior    every variable resolves to the exact literal it replaced · every converted script still runs its smallest honest check
nodes       node commands in these chains cite paths.<key> -- corrections in place via write.py, results never rewritten
```

**Falsifiers.** Any path literal left in a converted script · any variable resolving to a value different from the literal it replaced · any converted script that no longer runs · any file under `extensions/` touched.

**Standing order behind it.** `extensions/agi/lib/agent-prompt.md` Rules item 13 (commit 23663947a), appended to every parent and kid.

## Agent Notes
CARRIED RESIDUE (TMM.44, thought-master 09:06Z 09-23): three of the seven paths.local_maxxing keys point into OTHER rounds' worktrees (worktree_a00_2f819956, worktree_a00_48ed5e56_nodes, worktree_a00_d511add6 and the two keys under it) -- ephemeral dirs a reaper can remove; kept byte-identical to the literals they replaced, by the pass's own rule. Routed to the Prime, not this pass: box.root and the other box.* / locations.* cells are stale on this box (they name the old {root} value; the repo lives elsewhere), and cli.py done's scoped commit drops .agi/config.json edits (the round's 7 keys were committed by director-thought's review pass, 7b0053ac5). Audit: repo-wide 10,086 -> 10,077, no new hit.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 3 residue correction (hypothesis:pass3-0924-residue-batch, demote reason: Universal path claim is contradicted by accepted conversion) -- CORRECTED IN PLACE per thought-master TMM.118 owed 1. The accepted design (experiment:a00-3f66ba67-f5c25c, the CFG.01 rebrief correction, inconclusive_lean_proved:80) deliberately leaves absolute box roots as literals, proposed as separate box.* cells -- and its own parent review already named the gap directly: the hypothesis text quantifies over every path while the rebrief (TMM.42) intentionally leaves absolute box roots outside paths, so the hypothesis text was stricter than the design it was scored against. The testable_claim and the body Claim paragraph are narrowed in this version to REPO-RELATIVE paths through paths.local_maxxing, matching what was actually proved (the earlier experiment:a00-1b4d6db0-04de8a tried the literal universal reading before the rebrief and was itself demoted for it, inconclusive_lean_disproved:60). FALSIFIERS, the Dispatch line and the three experiment children are otherwise unchanged; no result is rewritten, only the claim's own wording is brought into agreement with the design it was already scored against.
<!-- THOUGHT:END -->

RESIDUE (TMM.46, from mur-director-thought-3): the inventory figures above (51 tracked .py/.sh scripts scanned, 19 carrying path literals, 40 literals) were not reproduced by the review -- they came from director-thought's pre-dispatch scan with its own regex, not a committed tool; treat them as an estimate.
