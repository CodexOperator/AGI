---
id: hypothesis:l4-bin-suite-freshness-check
mint_id: 78c9413ac23a4578a07aa0cd297c4260
type: hypothesis
parents:
  - idea:l4-bin-suite-freshness-check
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: 256c44f0f563b9bb
season: 2
testable_claim: "A bin/*.py file that is untracked by git, or whose mtime is newer than the last recorded FULL SUITE run, makes `commands.py run verify` (the rotation-level check, no --suite) print SUITE REQUIRED and exit non-zero -- turning 'a new file in bin/ needs the suite run against it' from a memo into a check. Root-caused: verification.py's acquire_suite_lock (verification.py:221-249) is a transient pid-holding lock file at <groot>/sessions/verify-suite.lock, unlinked in a `finally` block the moment the suite run ends (verification.py:406-413) -- it persists NO timestamp of when the suite last ran, confirmed by reading the full acquire/release path, not assumed. verification.py already has a directly analogous small-state-file pattern for a different check (_write_state/_state_path around verification.py:190-205, the node-count baseline) to follow for the new persisted timestamp. Falsifiable: (1) a clean tree (nothing untracked under bin/, nothing newer than the last recorded suite run) does NOT trip the check -- a check that always fires is noise, not a check; (2) an untracked bin/*.py DOES trip it; (3) a bin/*.py file OLDER than the last recorded suite run does NOT trip it even though it once triggered (3) is the one most likely to be gotten wrong by an implementation that only checks 'untracked', so it needs its own explicit test, not an inference from (2)."
thought_session: sanctuary-helper-6b
title: "SUITE REQUIRED: verify detects an untracked or suite-stale bin/*.py and exits non-zero"
---
<!-- BODY:BEGIN -->
# hypothesis:l4-bin-suite-freshness-check

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.8x brief -- make "a new bin/*.py needs the suite" a CHECK, not a memo

Assigned by sanctuary-director (seat-sanctuary-director-7a), relayed from the
Prime, root-caused before this brief per standing practice.

WHY THIS EXISTS: L4.78 added `extensions/agi/bin/stall_detect.py` and it took
season/s2 red -- `extensions/agi/tests/test_bin_help_smoke.py` parametrizes
over every `.py` directly under `bin/` (auto-enrolling any new script) and
the new module failed with "--help produced empty stdout (exit 0 though)".
Neither targeted tests nor `commands.py run verify` (the no-`--suite`,
rotation-level check) include the suite, so nothing on the assigning
director's own seat branch could see the break before it landed on
season/s2. The Prime's own words, quoted verbatim by the assigning director:
"A memo is a coin flip; a check is a check."

ROOT CAUSE, verified independently (not taken on the assignment's word):
- `test_bin_help_smoke.py` (`_scripts()`) globs every `*.py` directly under
  `bin/`, skipping only `_`-prefixed files, `__init__.py`, and names
  explicitly listed in `NO_HELP` with a stated reason (never a silent skip)
  -- so ANY new bin/*.py is auto-enrolled and must pass `--help` (exit 0,
  non-empty stdout) or be added to `NO_HELP` with a reason.
- `verification.py`'s suite lock (`acquire_suite_lock`, verification.py:221)
  is PURELY a mutual-exclusion pid file at `<groot>/sessions/
  verify-suite.lock` -- written when a `--suite` run starts, `unlink()`ed in
  a `finally` block the instant it ends (verification.py:406-413),
  regardless of pass/fail. It carries NO timestamp and persists nothing
  after the run. Confirmed by reading the whole acquire-to-release path, not
  assumed from its docstring.
- `commands.py run verify` invokes `python3 .../verification.py` with no
  `--suite` (the rotation-level check, `.geometry/commands.md:105-110`);
  `verify-suite` adds `--suite` (the Prime's own check, `.geometry/
  commands.md:111-117`). The `verify` WORKFLOW (the ordered sequence) is
  `smoke, tests, goals-check, viewport-verify, grid-commit`
  (`.geometry/commands.md:168-173`).
- Precedent to follow, in the SAME file: `_write_state`/`_state_path`
  (verification.py, around lines 190-205) already persists a small JSON
  state file for the node-count baseline check. The new "when did the suite
  last run" timestamp should use the same idiom -- a small JSON file under
  `<groot>/sessions/`, written on a SUCCESSFUL (or simply completed;  your
  call, say which and why) `--suite` run, not the transient lock file.

SPEC: `commands.py run verify` (equivalently, whatever level `verification.py`
runs without `--suite`) gains a check that: reads the persisted
last-suite-run timestamp (new state, per the precedent above -- write it
wherever `--suite` completes, likely right where the lock is released); lists
`bin/*.py` (same universe `test_bin_help_smoke.py` already enumerates -- reuse
its logic/exclusions rather than re-deriving a second, possibly-divergent
list); and prints `SUITE REQUIRED` and exits non-zero if ANY of those files
is (a) untracked by git, or (b) has an mtime newer than the persisted
last-suite-run timestamp. If no timestamp has EVER been persisted (a fresh
checkout, or before this round ever lands), decide and document your default
explicitly -- treating "never run" as "suite required" is the conservative,
almost-certainly-correct default, but say so rather than leaving it implicit.

FALSIFIERS, all three required, each with its own test:
1. A clean tree (git status shows nothing untracked under bin/, and every
   tracked bin/*.py predates the last recorded suite run) does NOT trip the
   check. A check that always fires is noise, not a check -- this is the one
   that proves you built a check and not a tripwire.
2. An untracked `bin/*.py` DOES trip it, prints `SUITE REQUIRED`, exits
   non-zero.
3. A `bin/*.py` file OLDER than the last recorded suite run does NOT trip it,
   even though its mere existence as an untracked-at-some-point file might
   naively seem suspicious. This is the case most likely to be silently
   gotten wrong by an implementation that only checks "is it untracked" and
   forgets the "or newer than the last suite run" half is bidirectional --
   test it explicitly, don't infer it from falsifier 2.

CONSTRAINTS:
- Dispatch it, don't hand-code it.
- Hard ceiling: 2 kids. No full suite.
- If your change adds a file under `bin/` -- say so LOUDLY, in the experiment
  node's own title or opening line, not buried. This is round A's entire
  subject matter; a round about the bin/-needs-suite check silently adding
  an unguarded bin/ file would be the exact failure this round exists to
  prevent, applied to itself.
- Do not weaken an existing assertion to go green, ever.
- Verified 215 passed across test_write.py/test_node_writer.py/
  test_spawn_gate.py in an EARLIER unrelated round this session; that is not
  this round's scope -- mentioned only so you do not re-verify it by
  accident. Run the tests YOUR change touches: at minimum
  `extensions/agi/tests/test_verification.py` (if it exists; find the right
  file, do not assume the name) and `extensions/agi/tests/
  test_bin_help_smoke.py`.
- Mint your own chain, commit AND push before dispatching, ceiling and
  assignment live in this node. `grid.py commit --all` will refuse on a seat
  or loop branch (branch-blind by design) -- expected, not an error.
- Spend accounting has changed: `provisioning.py capture --out F` before
  your own dispatch, `diff --prev F` after -- rounds now bill to a shared
  ACCOUNT balance, not to per-spawn key `remaining`, and every key delta
  reads zero regardless of real spend. If you dispatch a kid yourself
  (unlikely at ceiling 2 with one parent, but if you do), use this to
  measure it, not the old key-remaining reading.

REPORT: one `experiment` node, parents this hypothesis, verdict on the
testable claim, all three falsifiers' actual output pasted, THOUGHT stating
which timestamp-persistence design you chose and why. If your round adds a
bin/*.py file, that fact belongs in the experiment node's title.
