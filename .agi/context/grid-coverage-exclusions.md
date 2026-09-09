# grid-coverage-exclusions.md — DECLARED exclusion list for grid_coverage_check.py
#
# DATA, not code. One excluded path per line, a reason after `|` on the same
# line. Blank lines and `#` comments are ignored. This file is read by
# grid_coverage_check.py: a tracked engine CODE file (.py/.sh/.js) with no
# `payload_ref` and no line here is a REAL gap and makes the checker exit 1.
#
# Hard rule (hypothesis:l3-engine-files-outside-the-grid): NEVER widen this
# list to make the count pass. Add a line ONLY for a file that legitimately
# has no node — data, test fixtures, docs — never for a missing mint. If the
# checker reports a remainder, that remainder is the mint backlog and must be
# reported, not excluded away.
#
# NOTE on scope: the checker enumerates CODE files only (.py/.sh/.js under
# extensions/ skills/ src/ bin/). Everything below is data/non-code, so it
# never appears in the enumeration today — it is declared so the boundary is
# an explicit decision a reader can see, not an accidental calm.

# ---- Test fixtures: synthetic data consumed by the test harness, not source.
# ---- level3.py's own boundary classifies these "out" (test-fixture-directory)
# ---- and the parent's measurement listed them as the clean exclusion.
extensions/agi/tests/fixtures/nested/level_a/level_b/level_c/leaf.md | test fixture data, not source
extensions/agi/tests/fixtures/nested/level_a/level_b/middle.md | test fixture data, not source
extensions/agi/tests/fixtures/nested/level_a/outer.md | test fixture data, not source
extensions/agi/tests/fixtures/nested/top.md | test fixture data, not source
extensions/agi/tests/fixtures/nodes/sample.json | test fixture data, not source
extensions/agi/tests/fixtures/nodes/sample.md | test fixture data, not source
extensions/agi/tests/fixtures/schemas/[hypothesis].md | test fixture data, not source
extensions/agi/tests/fixtures/schemas/example.json | test fixture data, not source
extensions/agi/tests/fixtures/schemas/example.md | test fixture data, not source
extensions/agi/tests/fixtures/walk_test/a/file_a.md | test fixture data, not source
extensions/agi/tests/fixtures/walk_test/b/file_b.md | test fixture data, not source
extensions/agi/tests/fixtures/walk_test/b/file_c.md | test fixture data, not source
extensions/agi/tests/fixtures/walk_test/file_top.md | test fixture data, not source

# ---- Briefs: prose that rides alongside the engine, authored in the graph's
# ---- own brief channel, not a payload a build node links. No code, no mint.
extensions/agi/briefs/master-sensei-duties.md | brief prose, not a grid payload
extensions/agi/briefs/prime-director-successor.md | brief prose, not a grid payload
extensions/agi/briefs/sensei-director-duties.md | brief prose, not a grid payload