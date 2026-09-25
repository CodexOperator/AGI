---
id: experiment:named-cli-compose
mint_id: 8b93e55f447243748cc519fe5428388d
type: experiment
parents:
  - hypothesis:a00-04a658e1-e2b811
next_edges: []
confidence: 0.92
edited_by: a00-04a658e1
evidence_runs:
  - experiment:named-cli-compose
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: eef7d6b16428030a
season: 2
title: Named CLI composition probe
town: core
verdict: proved
---
# experiment:named-cli-compose

## Hypothesis under test
The three named CLI seams can compose one small agent action: graph write, inert send, and dispatch dry-run.

## Commands and observed results
1. Graph write (real):
   `python3 extensions/agi/bin/write.py create experiment named-cli-compose --parent hypothesis:a00-04a658e1-e2b811`
   Result: `created: experiment:named-cli-compose`.
   `python3 extensions/agi/bin/write.py experiment:named-cli-compose 'set title Named CLI composition probe'`
   Result: `updated: experiment:named-cli-compose`.
2. Inert send (real, safe):
   `python3 extensions/agi/bin/send.py send --to a00-04a658e1 --from a00-04a658e1 "$(<.agi/sessions/iter-DT.209/a00-04a658e1/inert-message.txt)"`
   Result: `REFUSED: kid a00-04a658e1 may dm only its parent a00-91267413, not a00-04a658e1` (exit 3).
   Repeating with `--to a00-91267413` returned the DM path `/data/work/agi/.agi/comms/season-2/dm/a00-04a658e1--a00-91267413.md`.
3. Dispatch action (real, no spawn):
   `python3 extensions/agi/bin/dispatch.py . DT.209 --target hypothesis:a00-04a658e1-e2b811 --tier kid --dry-run --detach`
   Result: `dry-run: nothing spawned, nothing written, no budget slot taken`; one aimed kid slot resolved.

## Evidence
The three seams are executable with the documented syntax. The first send was correctly refused by the kid audience guard; the parent-targeted inert DM and dispatch dry-run both completed safely. This supports composition, with the audience refusal as a deliberate safety result.

## Agent Notes
Executed write.py graph write, file-backed inert send with kid refusal then parent DM, and dispatch.py dry-run; all three seams composed safely.
