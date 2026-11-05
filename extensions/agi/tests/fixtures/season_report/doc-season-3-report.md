---
id: doc:season-3-report
type: doc
title: Season 3 rollover report (test fixture)
status: active
---

# Season 3 report

## narr.lede
The season {{facts.prev_season}} line was folded into the archive refs and season {{facts.season}} opened at {{facts.cells.opened|hms}}. The graph holds {{facts.counts.engine_active|n}} active nodes by the engine's own rule.

## narr.day_intro
The run, in the order it happened. Each time comes from a box fact read by a named command.

## narr.timeline
{"cls": "", "when": "{{facts.box.events.last_landing.value|hms}}", "title": "Last landing before the freeze (L22).", "text": "All towns aligned; the lands of the season number {{facts.ledger.lands_total|n}}, of which {{facts.ledger.names_count|n}} carry a stack number."}
{"cls": "", "when": "{{facts.box.events.freeze_on.value|hms}}", "title": "Freeze on.", "text": "One node write turned off the jobs that move the trunk."}
{"cls": "warn", "when": "{{facts.box.events.dry_run.value|hms}}", "title": "Dry run refused.", "text": "The dry run stopped on a stale pin."}
{"cls": "warn", "when": "{{facts.box.events.first_run.value|hms}}", "title": "First real run stopped at its first push.", "text": "One seat signs and another pushes, so the run moved to the Prime's seat."}
{"cls": "", "when": "{{facts.box.events.run_start.value|hms}}–{{facts.box.events.run_end.value|hms}}", "title": "The rollover run, rc {{facts.box.run_rc.value}}.", "text": "Season {{facts.prev_season}} folded into the archive refs; {{facts.cells.town_count}} towns now read season {{facts.season}}."}
{"cls": "", "when": "{{facts.box.events.run_end.value|hms}}–{{facts.box.events.pushed_end.value|hms}}", "title": "Pushed, merged, switched.", "text": "The trunk cell of {{facts.trunk_cells}} of {{facts.posts_named}} post rows names {{facts.lines.trunk}}."}
{"cls": "", "when": "{{facts.box.events.freeze_off.value|hms}}", "title": "Freeze off.", "text": "The jobs were turned back on."}
{"cls": "", "when": "{{facts.box.events.trunks_moved.value|hms}}", "title": "Every post's trunk moved, then the engine pin.", "text": "The pin now reads {{facts.box.pin.value}}."}
{"cls": "", "when": "{{facts.box.events.restarts_start.value|hms}}–{{facts.box.events.restarts_end.value|hms}}", "title": "Twelve restarts, one at a time.", "text": "Directors first, the Prime last: {{facts.box.restarts.value}} restarts in all."}
{"cls": "", "when": "{{facts.box.events.mains_moved.value|hms}}", "title": "Four mains moved to the season line.", "text": "Overwrites happen only at a rollover, with an archive ref first."}

## narr.map_intro
One station per distinct branch tip. {{facts.grid.map.drawn|n}} of {{facts.grid.heads_total|n}} heads are drawn.

## roles
{
 "archive/core-season3-main-pre-20261014": "kept as the pre-rollover snapshot of the core line",
 "codex-town/main": "the town's integration line",
 "codex-town/season@PREV@/main": "the closed season's line, kept",
 "core/main": "the town's integration line",
 "core/season@PREV@/et-grok-pilot": "the closed season's line, kept",
 "core/season@PREV@/main": "the closed season's line, kept",
 "core/season3/main": "the town's integration line",
 "encryption-town/main": "the town's integration line",
 "encryption-town/season@PREV@/main": "the closed season's line, kept",
 "local-maxxing/main": "the town's integration line",
 "local-maxxing/season3/main": "the town's integration line",
 "master": "the default branch; only the outward sealer reads it",
 "posts/belam": "the Prime's post branch",
 "sanctuary/main": "the town's integration line",
 "sanctuary/season3/main": "the town's integration line",
 "season3/main": "the town's integration line",
 "streaming-suite/main": "the town's integration line",
 "streaming-suite/season3/main": "the town's integration line",
 "web-app-suite/main": "the town's integration line",
 "web-app-suite/season3/main": "the town's integration line"
}

## narr.graph_note
Counts are read from the commit {{facts.at_short}}; the type bars are relative to the widest row.

## narr.engine_note
Run rc {{facts.box.run_rc.value}}, complete {{facts.box.complete_time.value|hms}}.

## narr.open
{"text": "Nodes whose status and directory disagree wait for a move into deprecated/."}
{"text": "Season {{facts.season}} reports its own report: goal:g5.4 holds the design."}
{"text": "The close ({{facts.close.value|hms}}) is read from the ladder cell commit and verified by git, not by its header."}

## media
{"src": "song-fixture.mp3", "title": "Fixture song", "credit": "a test fixture", "first_line": "First line", "lines": [[0, "First line"], [4, "Second line"]]}

<!-- FACTS:BEGIN at=0000000000000000000000000000000000000000 -->
```json
{}
```
<!-- FACTS:END -->
