---
id: goal:g7.33.3
mint_id: e719282b8045465a999a4a8e98abab57
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G7.33.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: b7ba842beff4c05a
season: 2
seeds:
  - hypothesis:lm-ceiling-engine-units-source-suffix-measured-beside-recorded
  - hypothesis:lm-dispatch-memory-override-feeds-agi-batch-scheduling
  - hypothesis:lm-dispatch-where-locates-kid-session-dir
  - hypothesis:lm-rotate-status-uses-canonical-season-branch
status: retired
tags:
  - local-maxxing
  - engine
title: "G14.14.3: DISPATCH/RUNTIME -- five measured engine gaps in the dispatch, session-locator, schema-check and startup path (owner 2026-09-21 01:1xZ-01:2xZ on goal:g14, relayed via goal:g7.33)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.14.3

## Agent Notes
Source. This sub-sub-goal carries the DISPATCH/RUNTIME group, five lettered items (a) through (e), transcribed from the goal g14.14 body (owner 2026-09-21 01:1xZ-01:2xZ on goal g14). Minted before any round runs under it, per the commitment stated on g14.14.

Commits to. (a) the CEILING clause: brief.py CEILING line and the hypothesis schema wording say source-suffix lines, data files never count, and cli.py session-complete prints the measured number beside the recorded one -- verify the two agree and fix whichever drifts. (b) a kid session-dir locator, dispatch.py where KID-ID: a kid dispatched by a parent nests under the parent worktree at .agi/worktrees/PARENT/.agi/sessions/iter-X/KID/, not the top-level iter dir a director would guess first. (c) memory per round: add dispatch.py --memory GB, overriding the config-only spawn.memory_max (mem_cap.py lines 17 to 25, one call site at dispatch.py line 2649) for that single dispatch, so the future agi-batch workflow (G14.14.4) can schedule each round under its own measured GB instead of one fixed global value. (d) links.py schema currently exceeds 120 seconds on this graph; bring it under 60. (e) startup noise: rotate.py status prints a deprecated-alias warning on every call (season/s2 -> season2/main); the caller should pass the current name.

Invariants. Kids write the fix, parents review, the director batches and orders -- never engine code hand-written above kid tier. Every fix is pinned by the engine suite before and after, python3 -m pytest extensions/agi/tests -q, one announce line to belam first per the suite-lock rule. Item (c) specifically: the override is request-scoped, it changes the resolved cap for that one dispatch call only, never the config file on disk.

Falsifiers. Each lettered item is falsified on its own hypothesis: its committed test failing to reproduce the gap it names means the gap was misdiagnosed, and the WHY names the real mechanism for a re-mint; its fix breaking the engine suite means demote, never merge.

Done when. All five lettered items have a landed round, proved or disproved with its WHY, in the stated order: item (c) first because the future agi-batch workflow depends on it, then the rest batched two to three at a time.

First chunk, minted next: hypothesis:lm-dispatch-memory-override-feeds-agi-batch-scheduling, for item (c), ordered first per the g14.14 Order of work line.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
renumber g14.14.3 -> g7.33.3 to align the town with core's 09-21 goal re-arrangement (owner GO on core; owner 09-23 asked the two teams be aligned): the parent g14.14 became g7.33 on core; mint_id preserved; Prime core-sync 09-23
<!-- THOUGHT:END -->

Belam NO-PI 2026-09-28: item (c) residue re-landed — mem_cap.resolve_memory_cap(cfg, override=) restored on tip (was TypeError vs dispatch --memory); test_mem_cap_override 8/8; hyp confidence 0.95. Items (a)(b)(d)(e) still open — goal stays active.

Belam NO-PI 2026-09-28: items (b)+(e) landed — dispatch.py where <kid-id> nested locator; rotate.season_branch canonical-first (no status alias warn). Focused tests 5/5. Items (a)(d) still open — goal stays active.

Belam NO-PI 2026-09-28: item (a) landed — CEILING engine-units wording (brief + schema) + measured↔recorded print. Item (d) links.py schema still ≫3min wall (~6min+ prior measure) — left as note; switching to g7.33.7 hottest alternate. Goal stays active (d open).

Belam NO-PI 2026-09-29: item (d) PARKED — links.py schema alone timed out at 180s wall (timeout exit 124; no output); still much greater than 3min; no under-3min slice exists to bring under 60s. Goal stays active (d open). No pi.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
