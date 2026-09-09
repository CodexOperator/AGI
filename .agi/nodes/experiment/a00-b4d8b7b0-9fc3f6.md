---
id: experiment:a00-b4d8b7b0-9fc3f6
mint_id: 339bc26e39b34148a0f63ef6e38c32a1
type: experiment
parents:
  - hypothesis:l3-partial-write-adoption
next_edges: []
confidence: 0.8
edited_by: a00-6c4ee18a
evidence_runs:
  - experiment:a00-b4d8b7b0-9fc3f6
loop: hypothesis:l3-partial-write-adoption@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4d54e1520675671b
season: 2
title: A00 b4d8b7b0 9fc3f6
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-b4d8b7b0-9fc3f6

## Experiment

ADOPTED the partial-write verbs (hyp:l3-partial-write-adoption). The mechanism
(patch / body_patch / read in write.py) already existed but had zero adoption:
`read` was broken and WROTE (it fell through the write path, restamped
`edited_by`, stripped the trailing newline, printed `updated:` rather than
content), no test covered it, brief.py never named the verbs, and SKILL.md
declared the gap open.

WHAT I DID, in the director's order:

**1. Fixed the read verb, red-first.** Added 5 tests to test_write.py asserting
a ranged read prints the requested lines to stdout AND leaves the node file
BYTE-IDENTICAL on disk (no edited_by restamp, no body mutation, no trailing-
newline loss). Confirmed red: 4 failed against pre-change code (the bad-range
test already passed, since verb_read's `_parse_range` refuses at parse time).
Then added the missing terminal branch in write.py `main()`: when
`edit.read_target` is set, it renders the range to stdout and returns BEFORE
`submit()` is reached — it can never be mistaken for an edit. Added
`_slice_range` (body) and `_read_payload_text` (payload, streams only the
requested lines) helpers. Read is terminal: it refuses a line shared with any
write verb, mirroring `adopt`. Greened: 5/5.

**2. Measured the read.** Whole write.py (build:bin-write) = 48,004 bytes /
1080 lines (~12,001 tokens at ~4 chars/token). Ranged `read payload 290:300`
= 639 bytes / 11 lines (~160 tokens) — ~75x less than reading whole. A ranged
read materialises only the requested lines.

**3. Taught the template.** Added the partial verbs to brief.py's WRITE.PY
SYNTAX block (in `_kid`, the engine-work tier): `read payload|body START:END`,
`patch -`, `body_patch -`, plus the stdin rule (diff bytes by path or `-`, never
inline — a diff can contain the doubled ampersand that splits the script form).
Verified: `brief.assemble(tier='kid')` now carries all three; parent/director
briefs, which do not do engine file surgery, unchanged.

**4. Corrected SKILL.md.** Replaced the stale lines 281-283 "Known gap: payload
writes are whole-file only..." with what actually exists: the three verbs,
the stdin rule, and the fail-closed guarantee (a hunk that does not apply
refuses the whole write and changes nothing).

**5. Proved adoption live.** Landed a REAL engine change to write.py (build:bin-
write) THROUGH the patch verb with a unified diff on stdin: extended `main()`'s
usage docstring with the read/patch forms. The patch applied, replaced the
payload, and stamped provenance on the node.

## Evidence

Defect confirmed live before the fix (read body 1:3 of a real node):
```
$ write.py hypothesis:l3-write-partial-diffs-as-writes 'read body 1:3'
updated: hypothesis:l3-write-partial-diffs-as-writes
$ git diff  # node modified: edited_by restamped, trailing newline stripped
```
Reverted; tree clean before starting.

Red test run (pre-fix): `test_read_body_prints_range...` FAILED, 4 failed /
1 passed. Post-fix: 5 passed. Full write suite: 50 passed.

Read measurement:
```
whole write.py: 48004 bytes / 1080 lines  (~12001 tokens @4ch/token)
read payload 290:300: 639 bytes / 11 lines (~160 tokens)  ~75x less
```

Live adoption command and output:
```
$ python3 extensions/agi/bin/write.py build:bin-write 'patch -' \
      --actor a00-b4d8b7b0 --session SD.14-live-adoption < /tmp/adopt.diff
updated: build:bin-write
payload: .../extensions/agi/bin/write.py replaced
```
Provenance stamped on the node after the write:
```
edited_by: a00-b4d8b7b0
thought_session: SD.14-live-adoption
```
The payload now carries the new doc line (`read payload 10:20`); confirmed
with `read payload 855:859`.

One necessary test refinement: the no-file-WRITE invariant guard
(`test_edit_py_contains_no_file_write`) banned ANY `open()` and tripped on my
streaming READ. Refined it to flag only a provably write-mode open (and any
open whose mode cannot be proven read-only), plus a guard test proving
`open('w')` / `open('a')` / `open('r+')` / non-literal mode still trip.
`open('r')` / `open('rb')` / default (read) are allowed. Intent preserved:
write.py still performs no file WRITE.

Grid versioning: per the shared-worktree rule I did NOT run `grid.py
commit --all` (parallel agents and the loop's uncommitted work share this
tree; running it would sweep those into one version). The provenance and the
payload byte change are shown by command output above; the build:bin-write
grid version is cut by the loop's own commit on accept.

Suite: 2247 passed, 1 skipped (was 2241 passed 1 skipped; +6 new tests: 5
read + 1 open-guard). links.py links: 1758 resolved, 0 broken.
grid_coverage_check: clean. write_guard check: silent. Full
`python3 -m pytest extensions/agi/tests/ -q` green.

## Agent Notes
PARTIAL-WRITE ADOPTION — red-first read test names: `test_read_body_prints_range_and_leaves_node_byte_identical`, `test_read_payload_prints_the_range_and_writes_nothing`, `test_read_supports_open_ended_ranges`, `test_read_refuses_a_bad_range`, `test_read_is_terminal_and_cannot_share_a_line_with_write_verbs`. Ranged read: 48,004 B / ~12,001 tokens whole vs 639 B / ~160 tokens for 11 lines — ~75x less. Live patch: `write.py build:bin-write 'patch -' --actor a00-b4d8b7b0 --session SD.14-live-adoption < adopt.diff` -> `updated: build:bin-write`, payload replaced, node stamped edited_by=a00-b4d8b7b0 / thought_session=SD.14-live-adoption. brief.py: added read/patch/body_patch plus stdin rule to kid WRITE.PY SYNTAX block. SKILL.md: replaced stale "Known gap: payload writes are whole-file only" paragraph with the three verbs + stdin + fail-closed guarantee. Suite 2247 passed 1 skipped; links 0 broken; grid_coverage clean; write_guard silent. OpenRouter account: no new spend by me (7.87 remaining at start; Omit = I ran local tests only). Grid version of build:bin-write deferred to the loop's commit (shared-worktree rule forbids me running grid.py commit).

## Agent Notes
Fixed the broken read verb red-first (+5 tests, byte-identical on read), measured ranged read at ~75x less than whole-file, taught brief.py kid tier the three partial verbs + stdin rule, corrected stale SKILL.md known-gap paragraph, and proved adoption live by landing a real write.py change through the patch verb on stdin (edited_by/thought_session stamped, payload replaced, grid version deferred to the loop's commit per shared-worktree rule).

PARENT REVIEW a00-6c4ee18a SD.14: ACCEPTED. Independently verified against the tree: terminal read branch present in main (write.py L954, refuses a line shared with any write verb); live `read payload` prints content and no updated stamp; SKILL.md gap paragraph replaced with the three verbs plus stdin rule plus fail-closed guarantee; brief.py kid tier carries all three verbs; test_write.py 50 passed, full suite 2247 passed 1 skipped; git diff shows only intended files (write.py, test_write.py, brief.py, SKILL.md). The read-measurement and the live patch adoption command with provenance (edited_by a00-b4d8b7b0, thought_session SD.14-live-adoption) both satisfy the brief items 2 and 5. The open-guard refinement preserves intent: no write-mode open in write.py, guard tested against write modes. Verdict lean_proved 80 agreed.
