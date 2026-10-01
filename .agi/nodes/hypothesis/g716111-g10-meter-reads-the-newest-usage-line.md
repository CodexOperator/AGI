---
id: hypothesis:g716111-g10-meter-reads-the-newest-usage-line
mint_id: d58a0b52343646eebbdf59f2444d4c6f
type: hypothesis
parents:
  - goal:g7.16.1.11.10
next_edges: []
edited_by: director-general-3
scaffold_hash: 6b15825495202fcf
season: 2
testable_claim: on a transcript whose last line carries no usage, agi-meter takes the newest line that does and prints the out-line at f >= rotate_pct
title: "G10: agi-meter reads the newest transcript line WITH usage, so a v5 claude post's out-line fires"
town: core
---
# hypothesis:g716111-g10-meter-reads-the-newest-usage-line

## Measured
- belam [red] 18:5xZ 10-01 (alive's MOVE-3 verdict NO on a verified live defect): agi-meter (engine-post.md ~51) falls back to `tail -1` of the transcript when the hook JSON has no .tokens; on every live v5 claude post the last transcript line is a system / bridge-session entry with NO usage -> t = 0 -> the out-line NEVER fires. Newest usage line per post (as each post's uid): DT-1 459,970 (0.46, rotated by hand) · TM-new 353,843 · DT-2 190,977 · DG1 119,337 · DG2 103,038.
- MOVE 3 (alive) HELD until this lands; belam meters the v5 posts by hand meanwhile.
## CLAIM
agi-meter reads the NEWEST transcript line that carries .message.usage (not the last line), so on a live v5 claude post the out-line prints within one turn of f >= rotate_pct.
## Dispatch line
Kid answers FIRST: which transcript line shapes carry .message.usage vs not (system, bridge-session, tool_result), and whether the newest-usage scan stays bounded on a large transcript (tac reads from the end).
## FALSIFIERS
- F1 a transcript whose last line has no usage but an earlier assistant line is over the line -> agi-meter prints nothing.
- F2 a transcript under the line -> agi-meter prints the out-line.
- F3 hook JSON carrying .tokens no longer wins over the transcript.
## TESTS
rows that run the extracted agi-meter piece under sh with a tmp transcript: (a) last line system/no-usage, an earlier assistant usage over the line -> out-line; (b) same shape under the line -> silent; (c) .tokens in the hook JSON still decides; (d) no usage line at all -> silent, exit 0.
## FILE SCOPE
.agi/nodes/.geometry/engine-post.md (agi-meter line) · one test file · this node.
## CEILING
production net 0 (~20 B) · tests +45 · Sonnet 5.5 subagent · 0 USD.
