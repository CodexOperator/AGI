---
name: agi-town
description: >
  Bring the whole agi town up on a box, or take it down, with ONE script: `agi.sh start` / `agi.sh stop`
  (goal:g7.16.1.11.44.8). Use on a fresh box with a fresh Claude install, after a stop, or to find where an
  interrupted start stopped. The traps are code; this skill only runs the loop.
---
Run as root from the repo: `sudo sh extensions/agi/bin/agi.sh start` (down: `... stop`; where it stands: `... status`).
Repeat until rc 0, by the rc:
- rc 20 `[ask] KEY: question` → ask the owner that one question, then `sudo sh extensions/agi/bin/agi.sh answer KEY VALUE`, run start again.
- rc 21 `[owner-do] command` → show the owner the command to type with `!` (a login URL, an apt line, `gh auth login`), run start again.
- rc 1 → the line says what and why; nothing is half-done, a re-run resumes at the first unmet step.
- `host: not met; run agi.sh host` → the one root act, once per box and pin: `sudo PIN=<40-hex> sh extensions/agi/bin/agi.sh host`, then start again.
The step order is the `town start` row of the engine matrix (main host posts crons units blast); a second start changes nothing. `a start is in progress since <UTC>` → finish it with start, never stop it. Boot unlock (tang / passphrase) comes before agi.sh exists: out of scope.
- `[ring] no ring at <pin>` → ring: unverified (the old gate): no agi-out ring commit exists yet, so start verifies no post key and goes on.
- By design start enables agi-boot even when town.state recorded `boot disabled`: a stopped town's boot is brought back by start, not by hand.
