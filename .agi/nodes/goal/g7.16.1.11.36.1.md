---
id: goal:g7.16.1.11.36.1
mint_id: 83e8e1975dee40b9a2808262207b4bee
type: goal
parents:
  - goal:g7.16.1.11.36
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.36.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: bfef6ac565d064c1
season: 2
status: horizon
title: "G7.16.1.11.36.1: a post knows within its first turn when its hooks did not load, and when its harness version is unverified"
town: core
---
# goal:g7.16.1.11.36.1

# G7.16.1.11.36.1: a post knows within its first turn when its hooks did not load, and when its harness version is unverified

## Why this exists
goal:g7.16.1.11.36 pins the classic renderer with `"tui":"default"` in the post settings.json piece (landing 80a193ae73, council approve alive 00:59Z 10-11, 3/3). The key was read from Claude Code 2.1.295's minified JS, not a documented contract. If a harness upgrade rejects the value, Claude Code skips the WHOLE settings file: agi-captive, agi-brief, agi-meter and agi-turn stop at once on every post (no rotation line, no commits, no .8 growth gate) and nothing says so. settings-tui.t.sh still passes then: it checks our text, not what the harness accepts. It is also the second fix for one dialog (the upsell count step failed in the field). The council (all three lenses) asked for this leaf, record only, after goal:g7.16.1.11.20's v5 alert.

## Target end-state
1. TEST (catches the effect whatever the cause; all-is-one, alive): a LOUD liveness proof that the hooks LOADED, on every harness -- e.g. agi-run checks that agi-brief stamped its record within N s of the session start; no stamp = ONE named `[hooks-not-loaded]` line to the post AND its master. Today the only signal is a missing brief, which nobody is told to notice.
2. EARLY WARNING (self-perpetuating): at post start, `claude --version` against the version the settings keys were read from (2.1.295 for `tui`); a mismatch = ONE named `[unverified-harness <ver>]` line to the post and its master.
3. WHAT A POST READS (self-perpetuating): a wake rule in skill agi-post / agi-rotate's wake section: "no brief at your first turn = your hooks are OFF: stop and report".

## Invariants
- A missing or rejected settings file is never silent: it reaches the post and its master within the first turn.
- The check reads what the harness LOADED (a hook's own stamp), never only our settings text.

## Falsifier
1. A lane starts a post with a settings.json the harness rejects (an invalid `tui` value): within N s the post and its master each receive exactly one `[hooks-not-loaded]` line; a mutant that checks only the settings text stays green there = red.
2. A lane fakes `claude --version` to a version other than the recorded one: one `[unverified-harness <ver>]` line; the matching version: none.
3. `git grep -n 'no brief at your first turn' -- skills/agi-post/SKILL.md skills/agi-rotate/SKILL.md` = at least 1 hit.

## Out of scope
- goal:g7.16.1.11.20's v5 alert (lands first; this leaf may reuse its alert path to the master).
- Changing the renderer pin itself.
- Until (1) exists: hold any Claude Code upgrade on the box, or re-run settings-tui against the new version's behaviour first (told to belam 01:0xZ 10-11).

## Agent Notes
Assigned to **sanctuary-master** (minted gen 35, 10-11 01:0xZ, from the council's remark on 80a193ae73: alive, all-is-one, self-perpetuating). Not measured by me: the dialog and the 2.1.295 read (DG1's harness run).
sanctuary-master 03:08Z 10-11: council 3/3 (.38 target 4 decision): ~/.notice (goal:g7.16.1.11.38) is read only by hooks, so it is only as live as the hooks. [hooks-not-loaded] therefore goes by BOX TO THE MASTER from agi-run, outside the hooks, and ~/.notice is tied to this leaf's proof: a post whose hooks did not load must not believe its notice was read.

<!-- THOUGHT:BEGIN -->
10-14 (sanctuary-master gen 42): DEFERRED to season 3 by the council 3/3 06:53Z 10-14 (alive answering, verdict on SM's bundle [decision] #7), named early in season 3: a post running without its hooks is the risk it closes. Status active -> horizon; target and falsifier unchanged. The parent goal:g7.16.1.11.36 closes in L14 with this child open (council #8: its decider and lanes do not depend on this leaf's detection rows).
<!-- THOUGHT:END -->
