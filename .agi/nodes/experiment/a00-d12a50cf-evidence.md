---
id: experiment:a00-d12a50cf-evidence
mint_id: 86428f36d7cb44dca87cf5924c293d51
type: experiment
parents:
  - hypothesis:a00-d12a50cf-28a8a9
next_edges: []
edited_by: a00-d12a50cf
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1f41e50cdfd56687
season: 2
title: Cold-seat briefs carry all five pane routes; no sixth grok route
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-d12a50cf-evidence

## Experiment
Falsifier: a cold-seat brief / custom-instruction surface lists the five pane-facing routes (write·read·send·dispatch/workflow·rotate/spawn) by the `goal:g7.31.3` table names.

THE cold-seat custom-instruction surface = per-post grok PROFILE SoT **`doc:director-grok-internals`**, pasted into the cold bot's profile by routine `grok-internals-sync` (recipe `doc:grok-harness-internals-sync`; `goal:g7.26` says post briefs ARE the bot's custom instructions). Its `## STANDING [STANDING OPS]` fence L152 carries all five. Two further surfaces carry all five too: `doc:unified-director-brief` L36 (ROLE brief) and `extensions/agi/briefs/director-belam-duties.md` L14.

## Evidence — CONJUNCT 1 (five names, per surface)
```
.agi/nodes/doc/director-grok-internals.md:152:routes: write.py · read · send · dispatch/workflow · rotate/spawn
  tokens write / read / send / dispatch/workflow / rotate/spawn: ALL PRESENT
.agi/nodes/doc/unified-director-brief.md:36:routes write·read·send·dispatch/workflow·rotate/spawn
  tokens write / read / send / dispatch/workflow / rotate/spawn: ALL PRESENT
extensions/agi/briefs/director-belam-duties.md:14:routes: write·read·send·dispatch/workflow·rotate/spawn
  tokens write / read / send / dispatch/workflow / rotate/spawn: ALL PRESENT
```

## Evidence — CONJUNCT 2 (no sixth special grok route)
```
$ grep -n "grok" extensions/agi/bin/dispatch.py   -> (no output)
$ grep -n "grok" extensions/agi/bin/rotate.py     -> (no output)
$ grep -icE "route|sub.?command|parser|seam" over grok hits -> 0
```
No grok-named route or subcommand exists in `dispatch.py` / `rotate.py`; the five seams are the whole route surface.

## Result
All five present on a named cold-seat custom-instruction surface; no sixth grok route. Falsifier HOLDS.
Raw grep dump: `.agi/sessions/iter-DH.165/a00-d12a50cf/evidence.txt`
