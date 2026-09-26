---
id: goal:g7.33.14
mint_id: 867c26fcafa941ca887b09d96ddf6506
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G7.33.14
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 5b913738aea99943
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - engine
title: "G7.33.14: NO WORKFLOW-AUTHORED TEMPLATE HARDCODES A BOX PATH SEPARATE FROM CONFIG.JSON'S ROOT -- ~15 review/investigation templates carried a stale /home/ubuntu/work/agi literal; kid/parent dispatch was never affected"
town: core
---
# goal:g7.33.14

## Why this exists
**Parent `goal:g7.33`.** director-engine gen 20 (2026-09-25), while checking whether DH.360's
merge-up-review could safely be re-dispatched, found `.agi/config.json` declares
`root: "/home/ubuntu/work/agi"` and that exact literal (not a `{template}` var) is hardcoded
into the prompt text of ~15 workflow.py-authored review/investigation templates. MEASURED on
this box: `ls /home/ubuntu/work/agi` -> No such file or directory; `whoami` -> belam; `$HOME` ->
/home/belam; the real repo root is /data/work/agi (confirmed via `ps -ef` showing real
launch-wrapper processes running from /data/work/agi). thought-master independently verified
the same absence (TMM.183, 2026-09-25 23:0xZ) and named this the right home for the fix.

## Target end-state
- Every `workflow.py run <name>` dispatch, on the box it actually runs on, sends its dispatched
  model a working directory / cd target that exists and is the real repo root.
- `.agi/config.json`'s `root` field (and `paths.local_maxxing.pi_home`, `claude_home`,
  `logs_dir`, which carry the same `/home/ubuntu/...` assumption) match the box.
- A single seam retires: no workflow-authored `.json`/`.js` template carries an
  independently-hardcoded absolute repo path that can drift from config.json's own `root`.

## Invariants
- Kid/parent agent dispatch (`dispatch.py`/`cli.py`) must stay unaffected -- it already resolves
  the root dynamically (`bin/locations.py`, nearest `.agi/` wins) and every existing round
  (hundreds of `iter-*` dirs) depends on that continuing to work exactly as it does today.
- A fix must not require every template to be hand-edited forever after: if `workflow.py author`
  can regenerate the `.js` siblings from their `.json` source, the fix belongs at the source
  (config.json's `root`, or the `.json` templates it feeds), not scattered N times.

## Falsifier
1. `grep -rn '/home/ubuntu/work/agi' extensions/ .claude/ .agi/config.json` returns 0 hits (or
   only hits inside a historical comment/changelog explicitly marked as such).
2. A fresh `workflow.py run <any review/investigate workflow> --dry-run` on THIS box resolves a
   root that `ls` confirms exists, for every stage.
3. `python3 -m pytest extensions/agi/tests/ -q` still passes in full after the fix (no template
   or config change should touch dispatch.py's own root resolution).

## Out of scope
- Actually re-running either DH.360's or DH.362's merge-up-review mur -- owed after this lands,
  not part of it.
- Any change to `dispatch.py`/`cli.py`/`bin/locations.py`'s own (already-correct) dynamic root
  resolution.
- goal:g6.41's reseat-bug hypotheses (heal.py) -- a different, only possibly-related mechanism
  (both are "the box changed, something didn't know" incidents, but distinct code paths).

## Agent Notes
Assigned to **director-engine**. Minted as the parent goal for the owner-directed parent
mini-swarm trial (hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis,
goal:g7.16) -- 3 parents split this goal's remaining work into 3 disjoint file groups and each
mints its own sub-subgoal before proceeding to hypothesis -> kids as normal.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fixes three schema defects thought-master's gate caught at tip 019242b32d (TMM.196), independently
reproduced here first (`snapshot-goals.py --render --check` -> rc 1, identical error) rather than
taken on the report's word: missing `heading_level` (every g7.33.N sibling uses 4), a placeholder
`title` instead of the "G7.33.N: ONE CAPS SENTENCE" siblings use, and a duplicated
`# goal:g7.33.14` heading left by the create step running against a --body-file that already
opened with its own heading. No content change beyond the three named defects.
<!-- THOUGHT:END -->
