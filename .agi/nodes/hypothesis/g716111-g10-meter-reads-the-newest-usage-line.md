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

## RESULT G10 (kid b483adc00, director record)
agi-meter: `xargs tac | jq -nR 'first(inputs|fromjson?|select(.message.usage)|...)'`, null fields 0, .tokens still wins. NUMSTAT bd3495bea..b483adc00: engine-post.md 2/2 (line + size header) · test_agi_meter.py 45/0. Rows (a) + (e) red on the old bytes; 6 passed. Director live check: on its own transcript the piece reads the correct total and fires at a lowered line. mur-de-base-g10: review accept_with_residue (verify stage unstructured/empty).

## CORRECTIVE G10.2 -- closes mur-de-base-g10 g10-code (D2 D3; D1 = findings row 70; D4 = the record above)
BASE      CUT FROM de-base-G10 tip (b483adc00 + this node write). No merge. Never rebase.
1. (D2) a line whose .message.usage is a string / array / number raises a jq runtime error outside fromjson?, t goes empty, the out-line is silent again. TRUE WHEN the select requires .message.usage to be an OBJECT (type=="object") so such a line is skipped like any other; a row puts a non-object usage line newest and an over-the-line object line earlier -> out-line printed.
2. (D3) a row pins the bounded scan: a large fake transcript (>= 200k lines) with the over-the-line usage line LAST, run under a wall-time bound well below a full parse -- or, deterministically, a transcript whose EARLY lines are invalid JSON-breaking bytes that fromjson? must never reach because first() stopped.
FILE SCOPE engine-post.md (agi-meter line) · extensions/agi/tests/test_agi_meter.py.  CEILING production net 0 · tests +25 · Sonnet 5.5 subagent · 0 USD.

## RESULT G10.2 (kid 00782dc30, director record)
select((.message.usage)?|type=="object"); a deterministic bounded-scan row. NUMSTAT 3fec41a65..00782dc30: engine-post.md 2/2 · test_agi_meter.py 11/0. 8 passed (5 consecutive runs). mur-de-base-g10b: review + verify accept_with_residue (review D1 refuted: the bounded row is the regression guard the node asked for; D2 confirmed; D3 = findings row 70).

## CORRECTIVE G10.3 -- closes mur-de-base-g10b g10b-code (verify missed a + D2)
BASE      CUT FROM de-base-G10 tip (00782dc30 + this node write). No merge. Never rebase.
1. (missed a) an OBJECT usage with a non-numeric field (input_tokens "a") still raises inside the arithmetic -> jq exits 5 -> t empty -> silent: the same harm this node closes. TRUE WHEN the select admits only lines whose .message.usage.input_tokens is a NUMBER, and the cache fields sum as (numbers // 0); a row puts such a poison object newest and an over-the-line valid line earlier -> out-line printed.
2. (D2) the bounded-scan row's comment claims only what it shows (the scan stops at the first VALID usage line from the end); after item 1 a poison line reached first is skipped, not fatal -- extend the row or its sibling to show that.
FILE SCOPE engine-post.md (agi-meter line + its size header) · extensions/agi/tests/test_agi_meter.py.  CEILING production net 0 · tests +15 · Sonnet 5.5 subagent · 0 USD.
