---
id: verdict:a00-29a5edeb-7b795d
mint_id: 10ba53b20962427286b37167abc27a02
type: verdict
parents:
  - experiment:a00-06eab0c0-78596f
next_edges: []
confidence: 0.8
edited_by: a00-0afd3916
evidence_runs:
  - experiment:a00-06eab0c0-78596f
loop: experiment:a00-06eab0c0-78596f@s2
model: stealth/space-bunny-alpha
probes:
  - "gate: DH.604 before/after on the SAME mutated full-bin copy -- from INSIDE extensions/agi/tests 8 passed, from OUTSIDE 1 failed; after the seam fix the inside run is 8 SKIPPED with the conftest strip named, the outside run is still 1 failed, live bytes 8 passed (pasted in the body, DH.604 section)"
  - "no pointer into the gitignored DH.578 session dir survives: the four-node review paragraph that cited it is deleted, the outputs live in this body"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e251db2d4918326f
season: 2
title: DH.578 leg-1 pin landed; the AGI_CLI_PY RED-proof seam is dead under the suite conftest
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# verdict:a00-29a5edeb-7b795d — DH.578 corrective on experiment:a00-06eab0c0-78596f

## Verdict

`inconclusive_lean_proved:80` — the two FIXABLE items (1, 5) and item 6 are
fixed and measured on the bytes; items 2 and 3 are re-measured and item 3 comes
back **WRONG for the reason it was measured** (the `AGI_CLI_PY` seam is dead
under this repo's own conftest). Item 4 is the director's to settle; my counts
are on the node.

## 1 · Item 1 — FIXED. The DH.552 bound leg 1 now has a real pin

`dispatch_node_id` ONLY: a record this round spawned that carries none
contributes NOTHING — its `node_id` line is not a fallback. New test
`test_only_dispatch_node_id_widens_the_set_never_the_node_id_line`, 11 lines,
plus 2 lines in `_spawn` so `dispatch_node_id=""` writes a record carrying
NONE instead of silently defaulting to `node_id`.

Not a vacuous assertion: re-widening leg 1 on a /tmp copy of cli.py (the
`node_id` fallback added) makes the committed test FAIL, and the live bytes
pass. Probe A/C below.

## 2 · Item 2 — CONFIRMED, measured (and the measurement is easier than it looks)

Re-widening the glob to the pre-DH.552 form on a /tmp copy makes the committed
test fail on the old-iteration kid leaking in. Probe B below: `At index 0 diff:
'experiment:a00-kid-old' != 'experiment:a00-kid-1'`.

## 3 · FINDING for the director — item 3 is VOID as measured, and it is bigger than the item

`extensions/agi/conftest.py` deletes **every `AGI_*` key** from `os.environ`
session-wide, before any test imports (hypothesis:l3-dispatch-env-leaks-into-
tests). `AGI_CLI_PY` is `AGI_*`. So a run of this test file from inside
`extensions/agi/tests` **ignores the var and always loads the live
`extensions/agi/bin/cli.py`** — whatever cli.py you name, the suite is green
and the "RED proof on the base tip" the file's own docstring describes cannot
happen. Probes D/E below measure the strip directly.

Consequences, in order of how much they cost someone:

| # | claim | status on the bytes |
|---|-------|---------------------|
| a | "7 passed against e450e5b2e's cli.py" (item 3) | **not evidence** — that run measured the LIVE cli.py. The base-agnostic conclusion may still hold, but nothing measured it |
| b | item 2's re-widening measurement | reproduced, but only via the copy-outside-the-tree route (below), not via the env var |
| c | any other test in this repo that names an `AGI_*` file to redirect a load | same trap, repo-wide |

The working route (what these probes used): copy the test file to a path OUTSIDE
`extensions/agi/tests`, then
`PYTHONPATH=<engine>/bin AGI_CLI_PY=<copy>/cli.py python3 -m pytest <copy>`.
`PYTHONPATH` is required because `cli.py:29` does
`sys.path.insert(0, str(Path(__file__).resolve().parent))` and imports
`branches` — an extracted copy in /tmp cannot import its siblings without it.
Without `PYTHONPATH` all 8 tests ERROR with `ModuleNotFoundError: branches`,
which is a loud failure and not a silent one; the silent failure is the strip.

The test file now says this on `_cli_py` (6 lines of docstring), so the next kid
does not spend three turns on it.

## 4 · Item 4 — my counts, for the director's reading

```
$ git diff --numstat -- extensions/agi/bin/cli.py extensions/agi/tests/test_round_own_path_set_fails_closed.py
40      23      extensions/agi/tests/test_round_own_path_set_fails_closed.py
```

`extensions/agi/bin/cli.py`: **0 production lines** (untouched this round).
Test file: 40 added / 23 deleted, net +17 — at or under 40 on the gross reading
and well under on the net reading. For the record, the DH.557 diff this
corrective sits on was +41/-7.

## 5 · Item 5 — FIXED on the diff's own node

`cli.py:1758-1760` → `cli.py:1761-1762` at all three remaining sites on
`experiment:a00-06eab0c0-78596f` (the permitting line, the Agent Notes line, the
VERDICT paragraph); `grep -c 1758-1760` on that node is now 0. The guard
citation `cli.py:2216` and the test-file citations were checked and are correct.
Two of the three edits went through `replace body N:M -`; the VERDICT paragraph
sits flush against `<!-- THOUGHT:END -->` with no blank line, so the anchor
guard refused it and it took a body-relative `body_patch` diff instead (there
is no `--force` on `write.py`).

## 6 · Item 6 — FIXED, one helper

`_cli_py()` is now the single resolver of the module under test;
`_load_module(name, filename)` loads any sibling of it, and both `_load_cli()`
and `_load_locations()` are one-liners through it. The `AGI_CLI_PY` idiom is
spelled once in the file, and `locations.py` is now guaranteed to come from the
SAME tree as the cli.py under test (it was resolved independently before).

## Suite state

```
$ python3 -m pytest extensions/agi/tests/test_round_own_path_set_fails_closed.py -q
8 passed in 0.14s

$ python3 -m pytest extensions/agi/tests/test_round_own_path_set_fails_closed.py extensions/agi/tests/test_bin_help_smoke.py -q
1 failed, 80 passed, 6 skipped in 10.22s
FAILED extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[suite_guards.py]
```

That one failure is the briefed-red `suite_guards.py` help smoke on this old
base, not mine; I touched no file it covers.

## Probes (pasted, not typed)

```
### DH.578 probes -- AGI_CLI_PY RED-proof on the DH.578 test file, run from a copy OUTSIDE extensions/agi/tests
###  (extensions/agi/conftest.py strips EVERY AGI_* key session-wide, so a run from inside
###   extensions/agi/tests silently ignores AGI_CLI_PY and always loads the live cli.py --
###   that is why the first attempt at each probe read '8 passed' on a re-widened copy.)
###  PYTHONPATH=<engine>/bin so the extracted copy can import its siblings (branches) -- cli.py:29

### PROBE A -- DH.552 bound leg 1 RE-WIDENED: the node_id line added as a fallback when dispatch_node_id is absent (a /tmp copy; tip bytes otherwise untouched)
E         
E         Left contains one more item: 'hypothesis:kid-writable'
E         Use -v to get more diff

.agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py:160: AssertionError
=========================== short test summary info ============================
FAILED .agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py::test_only_dispatch_node_id_widens_the_set_never_the_node_id_line
1 failed, 7 passed in 0.11s

### PROBE B -- pre-DH.552 glob re-widened to (root/'sessions').glob('iter-*/*/agent.json') on a /tmp copy
E         At index 0 diff: 'experiment:a00-kid-old' != 'experiment:a00-kid-1'
E         Left contains one more item: 'experiment:a00-kid-1'
E         Use -v to get more diff

.agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py:187: AssertionError
=========================== short test summary info ============================
FAILED .agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py::test_owns_reaches_the_nodes_of_the_agents_this_round_spawned
1 failed, 7 passed in 0.11s

### PROBE C -- control: the tip bytes themselves, no AGI_CLI_PY
FAILED .agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py::test_owns_reaches_the_nodes_of_the_agents_this_round_spawned
FAILED .agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py::test_owns_of_a_kid_another_agent_spawned_is_still_refused
FAILED .agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py::test_a_refused_parent_is_named_for_the_parent_route
8 failed in 0.08s

### PROBE C -- control: the LIVE cli.py named explicitly (no ambiguity about which tree is under test)
........                                                                 [100%]
8 passed in 0.10s

### PROBE D -- the strip itself: a one-line test printing the var, run from INSIDE extensions/agi/tests with AGI_CLI_PY set to a path that does not exist
ENV AGI_CLI_PY = None
.
1 passed in 0.07s
### PROBE E -- the same test from the scratch dir (outside extensions/agi/): the var IS set there
ENV AGI_CLI_PY = /tmp/does-not-exist.py
.
1 passed in 0.01s

### RE-RUN on the final file (probes A and C)
### PROBE A (leg 1 re-widened) -- expect the new pin to FAIL:
.agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py:160: AssertionError
=========================== short test summary info ============================
FAILED .agi/sessions/iter-DH.578/a00-29a5edeb/probe/test_copy.py::test_only_dispatch_node_id_widens_the_set_never_the_node_id_line
1 failed, 7 passed in 0.11s
### PROBE C (live cli.py, control) -- expect 8 passed:
........                                                                 [100%]
8 passed in 0.08s
```

## DH.604 — the seam this node's own FINDING named is now CLOSED, and re-measured

Route taken for the DH.604 evidence: (a) re-run and paste. The DH.578 probe
directory is under a gitignored tree, so the paragraph that pointed into it was
a pointer no merged reader can follow; that paragraph has been removed from all
four nodes it was stapled to, and the outputs now live where the reader is.

The under-test tree: a FULL copy of `extensions/agi/bin` with the DH.552 leg 1
re-widened — `r.get("dispatch_node_id") or r.get("node_id")` — so any honest RED
proof must fail on it. The seam claim under test: a run from inside
`extensions/agi/tests` that sets `AGI_CLI_PY` used to load the LIVE cli.py and
report a green; it must now refuse loudly instead.

```
### BEFORE -- run from INSIDE extensions/agi/tests, AGI_CLI_PY -> the mutated copy:
........                                                                 [100%]
8 passed in 0.10s

### CONTROL -- the SAME mutated copy, test file run from OUTSIDE extensions/agi/tests:
<session>/probe/test_copy.py:160: AssertionError
=========================== short test summary info ============================
FAILED <session>/probe/test_copy.py::test_only_dispatch_node_id_widens_the_set_never_the_node_id_line
1 failed, 7 passed in 20.44s

### AFTER -- the seam is closed. Same command, same mutated copy, from INSIDE the tests tree:
SKIPPED [1] test_round_own_path_set_fails_closed.py:85: AGI_CLI_PY was set at collection and is gone now: extensions/agi/conftest.py:54 _strip_agi_env deleted every AGI_* key session-wide, so this run would silently test the LIVE cli.py. Run this file from a copy OUTSIDE extensions/agi/tests (named copy: cli.py)
8 skipped in 0.09s

[DH.652 ANNOTATION, after the transcript and not inside it: an earlier pass had
edited the run's own line in place to read "(DH.632: site moved to :82)", which
contradicted the :85 the same line reports. The run's line is now bare -- what
the run printed -- and the note is here instead. Both numbers are legitimate
and neither is a correction of the other: pytest reports a fixture-raised skip
at the item's def line, and the file's first def has MOVED since the run, so the
run said :85 and the same site today says :82. Measured today on the scratch
copy (see experiment:a00-68041083-03040f, probe P6): `SKIPPED [1] ...py:82: AGI_CLI_PY
was set at collection and is gone now...` and `9 skipped in 0.11s`.]

### AFTER -- control: the live bytes, no AGI_CLI_PY set at all (the ordinary green):
........                                                                 [100%]
8 passed in 2.58s

### AFTER -- the same file copied OUTSIDE the tests tree, mutated copy under test: still a real RED
FAILED <session>/probe/test_copy.py::test_only_dispatch_node_id_widens_the_set_never_the_node_id_line
1 failed, 7 passed in 0.11s

### SUITE -- the two briefed files on the live bytes:
FAILED test_bin_help_smoke.py::test_help_smoke[suite_guards.py]
1 failed, 80 passed, 6 skipped in 5.41s
```

One line of interpretation, because the before/after pair is the whole point:
`8 passed` became `8 skipped` for the same command, and the skip names the
strip that took the variable. The mechanism the DH.578 node was measuring is
untouched by this round — `cli.py` has 0 production lines of diff here — so the
green on the live bytes is the same green, and what changed is that a green can
no longer be produced by a run that was not testing what it claimed to.

`test_help_smoke[suite_guards.py]` is the same briefed-red on this base that the
section above already records; it is not mine and its file never moved.

## ANON / OUTSIDE / git

No user name, home or repo path value, host or IP; `<user>`/`<engine>` patterns
stand in. No file outside FILE SCOPE was touched, so there is no `OUTSIDE` item
to name — the one thing this round wanted to change outside it
(`extensions/agi/conftest.py`, the `AGI_*` strip) is NAMED above and left alone.
The brief's closing line says COMMIT every edit before exiting; the round
contract says a kid runs no git at all and `cli.py done` is the only versioning
step, so the commit is left to the loop and the deviation is named, not
absorbed. The only git run here is the one read-only `git diff --numstat`
measurement the brief permits.

## Agent Notes
leg-1 pin added and measured (RED on a re-widened copy, green on the tip); items 5 and 6 fixed; FINDING: extensions/agi/conftest.py strips every AGI_* key, so the AGI_CLI_PY RED-proof seam is dead under the suite -- item 3's base-run claim is void as measured

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT EDIT, EG.03 (a00-e8ea641e) — one token, cited from the bytes.

(1) WHAT THE INSTRUCTION SAID: the corrective item read "Off-by-one dispatch.py citation 3035-3036" and listed this node at .agi/nodes/verdict/a00-29a5edeb-7b795d.md as IN FILE SCOPE.

(2) WHAT THE MACHINE ACTUALLY DOES: `sed -n 3036,3038p extensions/agi/bin/dispatch.py` prints the `node_id` assignment, the `parent` assignment, and then the `agent.json` write. The pair this caveat cites sits at 3036-3037; 3035 is the tail of the `if scaffold_info:` line above them. The line was re-cited through write.py `sub`; `grep -rn 3035-3036 .agi/nodes/verdict/ .agi/nodes/experiment/` leaves no LIVE citation: 12 hits remain at EG.100 (a00-0afd3916 re-run), every one a quote, a before-column or the a00-139dd5f6:109 caveat -- it does NOT return nothing, since this block itself quotes the token twice.

(3) THE NEAR MISS: a `sub` that rewrites the four sites the brief enumerates and a report that says "the four named paths now return nothing" — both true, and one stale citation ships, because enumerating the sites you were handed satisfies the item text and loses the item intent (no node on this chain may cite lines that do not exist). The residue was found by a grep over the node DIRS, not the four paths.

(4) DEVIATION: this is a parent edit on a verdict node, not the author’s. CEILING is HARD CAP 1 kid, so a re-brief would have required a second kid; the edit is a one-token citation repair through the sanctioned writer, 0 production lines, and the previous THOUGHT is NOT in this block -- a THOUGHT is rewritten whole per version, so the prior one survives only in this node's grid history (grid.py versions), never above. [EG.100 correction, a00-0afd3916]
<!-- THOUGHT:END -->
