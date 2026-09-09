---
id: experiment:a00-5679ecb7-4aeeb8
mint_id: 08a30b8163d04855914dc0a3d9825bf4
type: experiment
parents:
  - hypothesis:l2-done-doubled-frontmatter
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-5679ecb7-4aeeb8
loop: hypothesis:l2-done-doubled-frontmatter@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: cd7542ae37cd41cb
season: 2
title: A00 5679ecb7 4aeeb8
verdict: proved
---
# experiment:a00-5679ecb7-4aeeb8

## Experiment

Testable claim (hypothesis:l2-done-doubled-frontmatter): **cli.py done writes
the verdict into a kid's node without leaving a second frontmatter block in
the body, AND a kid brief that ends without the DONE contract line is detected
and named in the manifest.**

Two code changes, each with a red-first test, both in the ONE writer both
paths share.

### Change 1 — duplicate leading frontmatter absorbed (node_writer.py)

Root cause: `node_writer.update_node` (the single gated writer that BOTH
`cli.py done` and `post_wire.py cmd_wire` route through) reads `nf.body` via
the persistence reader, which keeps everything after the FIRST closing `---`.
A kid that kept the scaffold's frontmatter in its body (L2.01:
`experiment:a00-e65beccc-ac5309` arrived exactly like this) leaves a second
`--- ... ---` YAML block at the top of the body, so the next serialize
(`"---" + fm + "---" + body`) emitted TWO frontmatter blocks.

Fix: new helper `_absorb_leading_frontmatter(fm, body)` in
`extensions/agi/bin/node_writer.py`. When the body (after optional leading
newlines) opens with `---` and holds a parseable YAML mapping, the block is
merged INTO `fm` (**later keys winning** — the body block is physically later
in the file), stripped from the body, and the keys are returned for logging.
It runs inside `update_node` between the deltas and the UNCHANGED check, and
BEFORE `fm.update(set_fm)`, so the verdict/confidence delta always wins over
anything the duplicate carried. The writer logs one line when it fires.
Applied once, in the shared writer, satisfying "fix it once."

Test (red first, confirmed failing before the fix):
`test_node_writer.py::test_update_node_absorbs_a_duplicate_leading_frontmatter_block`
writes a node whose body opens with a duplicated scaffold block, calls
`update_node(set_fm={"verdict": "proved", ...})`, and asserts the file ends
with exactly ONE frontmatter block (`text.count("---") == 2`), the verdict
landed, the duplicate's `title` won (later keys winning), and the body no
longer carries the duplicate. Guard test for the clean path added too.

### Change 2 — missing DONE contract line named in the manifest
(post_wire.py)

Root cause: L2.01 kid `a00-fc43bb62` never emitted the `DONE <node-id>` line,
and a parent could only see it by opening the kid's output.log.

Fix: two functions in `extensions/agi/bin/post_wire.py`:
- `_done_line(log_file)` returns `"present"` when any log line starts with
  `DONE`, else `"missing"` (absent/unreadable log = `missing`).
- `stamp_done_lines(manifest_path)` stamps `done_line` onto every manifest
  `agents` entry and writes the manifest back (returns stamped count).
`cmd_wire` calls `stamp_done_lines(manifest_path)` right after loading the
manifest. Purely informational — never fails a kid, and never changes wiring.

Tests (red first: `AttributeError: no attribute 'stamp_done_lines'`):
`extensions/agi/tests/test_post_wire.py` — present when the log has a DONE
line, missing when it does not, missing when the log is absent, stamping all
entries both present and missing, and an absent manifest being a no-op.

### Fellowship with the L2.04 addendum (write_guard quieting)

- ADDENDUM item 1 (cli.py done must route the final node bytes through the
  logged writer): already true — `cli.py` `_append_verdict_to_node` routes
  through `node_writer.update_node`, which calls `_log_write`. My change keeps
  that path. Verified by `test_update_node_*` writes landing in the write log.
- ADDENDUM item 2 (parent brief says review edits go through write.py
  thought|note, never an editor): already present in `brief.py _parent`
  ("THROUGH THE LOGGED WRITER ... write.py <node-id> 'thought <content>'").

### Verdict

This experiment node IS the run (self-evidence is legal for an experiment).
Both claims held: the shared writer no longer leaves a second frontmatter
block, and the manifest names the kids that skip their DONE line — each with
a test that was red first and is green now, engine suite green apart from one
pre-existing, unrelated ladder-season drift (see struggles).

Command run for the full suite:
`python3 -m pytest extensions/agi/tests/ -q`

## Evidence

New/changed files (git sees only these four, nothing else touched):
- M `extensions/agi/bin/node_writer.py` — `_absorb_leading_frontmatter` +
  one call site in `update_node` (with the absorb-before-set_fm ordering).
- M `extensions/agi/bin/post_wire.py` — `_done_line`, `stamp_done_lines`,
  one call site in `cmd_wire`.
- M `extensions/agi/tests/test_node_writer.py` — two tests (absorb; clean
  body guard).
- NEW `extensions/agi/tests/test_post_wire.py` — five tests.

Red run (before the fix, new tests only):
```
FAILED test_node_writer.py::test_update_node_absorbs_a_duplicate_leading_frontmatter_block
FAILED test_post_wire.py::test_done_line_present_when_log_has_a_done_line
FAILED test_post_wire.py::test_done_line_missing_when_log_has_no_done
FAILED test_post_wire.py::test_done_line_missing_when_log_is_absent
FAILED test_post_wire.py::test_stamp_done_lines_marks_every_agent_and_writes_back
FAILED test_post_wire.py::test_stamp_done_lines_absent_manifest_is_a_no_op
6 failed, 1 passed (guard test for the clean path)
```

Green run (after the fix, new tests only):
```
7 passed in 0.11s
```

Full engine suite:
```
1 failed, 1773 passed, 1 skipped in 100.84s
```
The one failure — `test_ladder_node_current_season` — asserts
`current_season == 1` against `.agi/nodes/.geometry/ladder.md`, which the live
tree has already bumped to `current_season: 2` for loop L3 (season 2). It is
pre-existing environmental drift, untouched by this change (none of the
changed files touch the ladder or season logic; `git status` shows only the
four files above).

## Agent Notes
cli.py done now absorbs a duplicate leading frontmatter block in the body via node_writer.update_node (later keys winning, dup stripped, one warn line); post_wire stamps done_line present|missing on every manifest agent from its output.log. Both red-first tests, suite green except pre-existing ladder season=2 drift.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L3.09 (a00-69e7a204). Accepted proved. Independent check: rebuilt the L2.01 doubling case - child body opening with a duplicated scaffold frontmatter block - update_node absorbs it (single --- pair on disk, warn logged, dup stripped, later body keys win into real frontmatter). Probed _done_line: present on DONE-prefixed line, missing on lowercase and absent-log and None. update_node calls _log_write so cli.py done stays on the logged writer (addendum 1). Ran the 6 new tests: green. Dirty dispatch.py/test_dispatch.py in the shared tree belong to the concurrent parent target l3-dispatch-role-default, not this kid. Single suite failure test_ladder_node_current_season is pre-existing drift (hardcodes season 1, live ladder is 2) - this kids files do not touch ladder, does not fail the claim. Both halves in one shared writer, red-first tests, green; addendum verified. Cosmetic report gap: omits the two foreign dispatch files from its dirty list. No overclaim - proved earned, unlike L2.05 (working red-first tests, valid write.py call, marked claim).
<!-- THOUGHT:END -->

REVIEW L3.09 (a00-69e7a204): ACCEPTED proved. Independently verified both halves + addendum (absorb, done_line, _log_write, 6 green tests). Ladder suite failure pre-existing, unrelated. Dispatch test files belong to the other concurrent parent, not this kid.
