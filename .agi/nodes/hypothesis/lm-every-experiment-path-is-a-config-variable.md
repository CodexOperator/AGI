---
id: hypothesis:lm-every-experiment-path-is-a-config-variable
mint_id: 5c50528c87d246508da85bc012de8785
type: hypothesis
parents:
  - goal:g14
next_edges: []
confidence: 0.6
edited_by: director-thought
scaffold_hash: 9122847394ca5548
season: 2
tags:
  - local-maxxing
  - config-max
testable_claim: Every filesystem path the local-maxxing experiment chains rely on (scripts under datasets/ and .agi/context/local-maxxing/, and the commands their nodes cite) resolves at runtime from paths in .agi/config.json through one shared reader, each variable resolving to the exact literal it replaced; falsified by any literal left in a converted script, any changed resolved value, any converted script that no longer runs, or any file under extensions/ touched
title: "CONFIG-MAX PASS (owner 09-23): every path in the local-maxxing experiment chains is a named variable under paths in .agi/config.json, read through one shared reader, values unchanged"
town: local-maxxing
---
# hypothesis:lm-every-experiment-path-is-a-config-variable

# hypothesis:lm-every-experiment-path-is-a-config-variable

## Hypothesis
**Owner (2026-09-23 ~08:4xZ, director-thought pane, verbatim on goal:g14):** "We need to template max and config max everything. Add new standing order to parent and kid docs that paths are always stored in variables that are stored in a config. Then do a pass doing that for any paths in the experiment chains in this town goal bundle."

**Claim.** Every filesystem path the local-maxxing experiment chains rely on -- in their scripts (under `datasets/` and `.agi/context/local-maxxing/`) and in the commands their nodes cite -- resolves at runtime from ONE config section, `paths` in `.agi/config.json`, through ONE shared reader, with behavior unchanged.

```
inventory   2026-09-23: 51 tracked .py/.sh scripts scanned · 19 carry path literals · 40 literals (15 files .agi/context/local-maxxing · 3 datasets/switch-rule · 1 datasets/kid-sft)
config      .agi/config.json -> paths.<key> (a relative value resolves from the repo root) · one reader shared by .py and .sh
behavior    every variable resolves to the exact literal it replaced · every converted script still runs its smallest honest check
nodes       node commands in these chains cite paths.<key> -- corrections in place via write.py, results never rewritten
```

**Falsifiers.** Any path literal left in a converted script · any variable resolving to a value different from the literal it replaced · any converted script that no longer runs · any file under `extensions/` touched.

**Standing order behind it.** `extensions/agi/lib/agent-prompt.md` Rules item 13 (commit 23663947a), appended to every parent and kid.

## Agent Notes
CARRIED RESIDUE (TMM.44, thought-master 09:06Z 09-23): three of the seven paths.local_maxxing keys point into OTHER rounds' worktrees (worktree_a00_2f819956, worktree_a00_48ed5e56_nodes, worktree_a00_d511add6 and the two keys under it) -- ephemeral dirs a reaper can remove; kept byte-identical to the literals they replaced, by the pass's own rule. Routed to the Prime, not this pass: box.root and the other box.* / locations.* cells are stale on this box (they name /home/ubuntu/work/agi; the repo lives elsewhere), and cli.py done's scoped commit drops .agi/config.json edits (the round's 7 keys were committed by director-thought's review pass, 7b0053ac5). Audit: repo-wide 10,086 -> 10,077, no new hit.
