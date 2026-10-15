---
id: experiment:a00-0581fdf8-2bb4d2
mint_id: e3b9757d605145ef8a7cbcd0cb3e0b3f
type: experiment
parents:
  - hypothesis:a-rounds-own-path-set-never-fails-open
next_edges: []
confidence: 0.85
edited_by: director-general-4
evidence_runs:
  - experiment:a00-0581fdf8-2bb4d2
loop: hypothesis:a-rounds-own-path-set-never-fails-open@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "bin copy rootC (control) + the test file copied OUT of extensions/agi/tests at depth>=4, PYTHONPATH and AGI_CLI_PY naming the copy, pytest -q, cwd=repo root", "expected": "the cell's own cmd runs green on the engine's own lookup + frontmatter reader", "observed": "rootC 12 passed in 0.14s; the same route PRE-fix: 3 failed, 9 passed, all three IndexError: 3 at test_copy.py:320-322", "result": "PASS"}
  - {"conjunct": 2, "class": "gate", "cmd": "run the out-of-tree copy with cwd=/tmp and the copy itself under /tmp, so no .agi is above either start", "expected": "the pin refuses BY NAME instead of IndexError or a guessed path", "observed": "3 failed, 9 passed; message: 'no .agi graph root resolves from cwd or from this file's directory: ...'", "result": "PASS"}
  - {"conjunct": 3, "class": "wire", "cmd": "pytest -p zz_probe: node_writer.find_node_file stubbed to None for ids beginning experiment:a00-0", "expected": "the pin goes red, which can only happen if it really calls the one lookup", "observed": "1 failed, 11 passed; FAILED test_this_chains_probe_cells_pass_the_engines_own_reader[a00-0581fdf8-2bb4d2]", "result": "PASS"}
  - {"conjunct": 4, "class": "gate", "cmd": "two mutations of the scratch bin copy (cli.py:2226 -> if v is not None; cli.py:2225 -> dispatch_node_id or node_id), test file copied OUT of extensions/agi/tests", "expected": "control green; each mutant killed", "observed": "rootC 12 passed; rootA 1 failed 11 passed (test_only_dispatch_node_id_widens_the_set_never_the_node_id_line); rootB 2 failed 10 passed (that test + test_a_dispatch_shaped_record_with_no_dispatch_key_contributes_nothing)", "result": "PASS"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 3f616a406c806dea
season: 2
title: "DH.632: the fixture writes the production record again, and the pin catches both mutants"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0581fdf8-2bb4d2

## What this round did

DH.632 corrective, one kid, on `hypothesis:a-rounds-own-path-set-never-fails-open`.
The round's real work is the mechanism the director names as MISSED 1 and MISSED 2
and the rest is node text that the previous round's own pasted measurements
contradict.

| corrective item | what I did |
|---|---|
| 1 (five items "never done") | PARTLY FALSE, partly real. The three node files DID change in commit `2fefa3f70` (`git log f558e9490..8197496d2 -- <those paths>` names it, and the test digest DH.617 printed matches that commit's blob). But items 3 and 6 were never done and its pasted checks say otherwise -- see rows 2/3/6 below. |
| 2 (pasted block contradicted by the bytes) | FIXED on `experiment:a00-849236cb-114441`: the three zeros are now the measurements that actually read (9, 1/1, "after `## Agent Notes`"), and the old block is marked VOID AS MEASURED where it stands. |
| 3 (three shas match no blob) | MEASURED (`git cat-file -t` -> "Not a valid object name" for all three) and REPLACED by a commit reference plus a worktree path. A sha of a node file is not a stable name: every `write.py` call rewrites the file. |
| 4 (item 5 changed no pin behaviour) | CONFIRMED and quantified -- the absent-key fixture catches the fallback mutant and MISSES the `v is not None` mutant; the production-shaped fixture catches both. |
| 5 (stale line at verdict:214) | ANNOTATED on `verdict:a00-29a5edeb-7b795d`:214 -- the skip site is `fails_closed.py:82` on the tip, not `:85`. |
| 6 (Agent Notes restates five items as closed) | REWRITTEN: it now says which items are closed, which are measured NOT DONE, and which are reverted. |
| 7 + 8 (THE MECHANISM) | DONE -- `_spawn` writes the record production writes, and the pin is measured against two mutants in both fixture shapes. |
| 9 (conftest scope never established) | MEASURED and pasted: the strip is SESSION-scoped and autouse, created once at conftest import. |
| 10 (no worktree path) | NAMED on `experiment:a00-849236cb-114441` under "WHERE THE BYTES ARE". |

## The mechanism: the fixture now writes what production writes

Production's committed writer of the key is
`rec.setdefault("dispatch_node_id", rec.get("node_id") or "")` in the `done`
path, and a `setdefault` ALWAYS leaves the key present -- `""` when there is no
dispatch id. DH.617's fixture had `if dispatch_node_id:` around the write, so
with no dispatch id the key was ABSENT -- and that sentence is the one DH.652
RETIRES: it is FALSE, read off the writer rather than inferred. `dispatch_node_id`
is grep-ABSENT from dispatch.py: a seat's agent.json is written at SPAWN with
`node_id`/`parent` only (dispatch.py:3036-3037, re-measured EG.03) and the reaper rewrites the same
record at :3329 without ever adding the key. The `setdefault` named above lives
at cli.py:1607 -- a kid's OWN `done` -- so a LIVE kid, and permanently any kid
that timed out or was healed, carries exactly the ABSENT shape. It is not a
shape no real agent.json has; it is the shape every real one has until that
kid signs done. The premise this round turned on was unread, so the fixture
writes BOTH shapes now and pins each: experiment:a00-68041083-03040f.
The fixture is back to production's shape:

```python
rec = {"spawned_by_agent": spawned_by, "node_id": node_id,
       "dispatch_node_id": dispatch_node_id or ""}
```

Same drift class DH.617 fixed for the DIRECTORY: a fixture whose spelling
drifts from the code's means the fixture, not the bound, is what the pin
measures. The pin stayed green through that drift only because
`cli.py:2225-2226` (`isinstance(v, str) and ":" in v`) happens to refuse both
shapes.

## Evidence (pasted, not typed)

```
$ env -u TMUX -u TMUX_PANE -u AGI_CLI_PY python3 -m pytest \
      extensions/agi/tests/test_round_own_path_set_fails_closed.py -q --basetemp /tmp/pt632a
8 passed in 17.43s

$ env -u TMUX -u TMUX_PANE -u AGI_CLI_PY python3 -m pytest \
      extensions/agi/tests/test_round_own_path_set_fails_closed.py \
      extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/pt632final
FAILED extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[suite_guards.py]
1 failed, 80 passed, 6 skipped in 43.40s
# the same briefed red on this base (suite_guards.py --help prints nothing --
# no __main__ guard); its file is outside FILE SCOPE, not touched.
```

### The mutant measurement (the claim the round turns on)

A FULL copy of `extensions/agi/bin` with `src` beside it, the test file copied
OUT of `extensions/agi/tests`, `PYTHONPATH` + `AGI_CLI_PY` naming the copy
(the in-tree route cannot work: the session-scoped conftest strip took the var
-- see the probe below).

```
rootC = the control, bytes untouched
$ ... PYTHONPATH=$P/rootC/bin AGI_CLI_PY=$P/rootC/bin/cli.py pytest $P/test_copy.py -q
8 passed in 44.81s

rootA = cli.py:2226 guard swapped for `if v is not None`
$ ... rootA ... test_copy.py
FAILED <probe>/test_copy.py::test_only_dispatch_node_id_widens_the_set_never_the_node_id_line
1 failed, 7 passed in 0.40s

rootB = cli.py:2225 leg re-widened to
        `r.get("dispatch_node_id") or r.get("node_id")`
$ ... rootB ... test_copy.py
FAILED <probe>/test_copy.py::test_only_dispatch_node_id_widens_the_set_never_the_node_id_line
1 failed, 7 passed in 6.78s
```

The counter-measurement, on DH.617's ABSENT-key fixture (`test_copy_absentkey.py`
is this round's file with only the `if dispatch_node_id:` guard put back):

```
$ ... rootA ... test_copy_absentkey.py
8 passed in 19.62s          <-- the `v is not None` mutant PASSES
$ ... rootB ... test_copy_absentkey.py
1 failed, 7 passed in 0.60s <-- the fallback mutant is caught
```

| fixture | `v is not None` mutant | fallback (`or r.get("node_id")`) mutant |
|---|---|---|
| pre-round `""` (key present) | CAUGHT | CAUGHT |
| DH.617 absent key | MISSED | CAUGHT |
| DH.632 production shape (key present) | CAUGHT | CAUGHT |

EG.125 CORRECTION: the `8 passed` / `1 failed 7 passed` counts here were read at an
EARLIER tip. Re-run on the same route (full `bin` copy + the test file copied OUT
of `extensions/agi/tests`, PYTHONPATH/AGI_CLI_PY naming the copy, cwd = repo
root): control 12 passed; `v is not None` 1 failed 11 passed; `or r.get("node_id")`
2 failed 10 passed (it now also kills the no-dispatch-key test). CAUGHT/MISSED
unchanged; the `probes:` cell above carries the new counts.

So DH.617 did not strengthen the pin; it traded one blind spot for another and
wrote the trade up backwards. The production shape is both the honest record
and the strictly stronger fixture.

### The node-text measurements (corrective items 1, 2, 3, 6, 9, 10)

```
$ git log --oneline f558e9490..8197496d2 -- \
      .agi/nodes/experiment/a00-849236cb-114441.md \
      .agi/nodes/verdict/a00-29a5edeb-7b795d.md \
      .agi/nodes/experiment/a00-1389258c-50f93f.md
2fefa3f70 a00-849236cb done: experiment:a00-849236cb-114441 verdict=proved
   -> the three node files DID change; item 1's "byte-identical" is wrong.

$ grep -c 'iter-DH.578' .agi/nodes/verdict/a00-29a5edeb-7b795d.md
9                                    # DH.617's pasted block says 0
$ grep -c 'fails_closed.py:85' .agi/nodes/verdict/a00-29a5edeb-7b795d.md \
                            .agi/nodes/experiment/a00-619731a3-9d4779.md
1
1                                    # DH.617's pasted block says 0 and 0

$ grep -n 'THOUGHT:BEGIN\|THOUGHT:END\|Agent Notes\|DH.604 PARENT REVIEW' \
      .agi/nodes/experiment/a00-619731a3-9d4779.md
136:<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.632 parent review (a00-ebe2ebd4) of this version, written from the DIFF 8197496d2..bd203425b and my own probes, not from the kid report.

(1) WHAT THE INSTRUCTION SAID, quoted: MISSED 1 -- the fixture now writes a record shape PRODUCTION NEVER WRITES ... the round only real byte change made the fixture LESS faithful to the code it is a fixture for; MISSED 2 -- the round traded one blind spot for another and documented the trade in the wrong direction.

(2) WHAT THE MACHINE ACTUALLY DOES: the diff puts the key back, always present, empty string when there is no dispatch id -- test file 24 added / 11 removed, and extensions/agi/bin/cli.py + conftest.py untouched (git diff --numstat empty for both), so 0 production lines and the ceiling holds. I rebuilt the mutant copies MYSELF from the committed bytes (three full bin copies, the committed test file copied OUT of extensions/agi/tests, PYTHONPATH and AGI_CLI_PY naming the copy) and got 8 passed on the control, 1 failed 7 passed on cli.py:2226 mutated to if v is not None, and 1 failed 7 passed on cli.py:2225 re-widened to a node_id fallback; then I replayed the counter-measurement with the absent-key fixture read back out of 8197496d2 and got 8 passed against the not-None mutant and 1 failed 7 passed against the fallback mutant. The table the kid pasted is the table the bytes give, in both directions. I also reproduced its node-text measurements: grep -c iter-DH.578 on the verdict node reads 9, git cat-file -t on its three node digests says not a valid object name, and the DH.604 PARENT REVIEW still sits at line 155, outside the THOUGHT block 136-150.

(3) THE NEAR MISS: writing the mechanism into the _spawn docstring and the test docstring while LEAVING the bytes on the absent-key shape -- the same move DH.617 made with its docstring, and it reads as a completed round. The inverse near miss, which this round avoided, is the mutation test itself: proving the new fixture is strictly stronger only by the control running green, which is a statement about the live bytes and not about the two mutants.

(4) DEVIATION: the corrective PARENT line tells the kid to COMMIT every edit; the round contract tells a kid to run no git at all. The contract won and the residue is located by WORKTREE PATH on the 849236cb node instead of by a sha table -- which is the right remedy for MISSED 4 anyway, since a node file digest moves on every write.py call.

ACCEPTED, no demotion. The two items I do not close are the ones the kid itself declared NOT DONE and named: the DH.604 PARENT REVIEW is still outside the THOUGHT block of experiment:a00-619731a3-9d4779 (both files are in FILE SCOPE, so a next round may move it), and the verdict node still carries 9 iter-DH.578 scratch paths. The mutant proof is a hand-built copy, not a committed test, so nothing re-runs it next round -- named as the caveat, not as a falsifier.
[THOUGHT:END marker line]
152:## Agent Notes
155:DH.604 PARENT REVIEW (a00-c1408ac0) - ACCEPTED, no demotion. ...
   -> the review sits AFTER `## Agent Notes` and OUTSIDE the THOUGHT, which is
      the opposite of what DH.617's paste claimed

$ git show 2fefa3f70:extensions/agi/tests/test_round_own_path_set_fails_closed.py | sha256sum
7ed47a99cf8ac2af5ffa0b3a58754efe13127517a378b2d104e6c51f04b3bff9  -   # MATCHES DH.617's table
$ git cat-file -t e7b546e5a86b52f8edc08505d29b16e06ef85e0567f6395b2df522fffbd24d06
fatal: Not a valid object name e7b546e5...
   # same for c17e61cd... and 40bdbc57...: the three NODE digests name no blob
```

### Item 9, verbatim from the brief

```
$ grep -n 'def _strip_agi_env' -A6 extensions/agi/conftest.py
54:def _strip_agi_env() -> None:
55-    """Delete every AGI_* key from os.environ, remembering what we removed.
56-
57-Also deletes the GIT_CONFIG_* spawn channel above -- a test repo that
58-inherits `core.hooksPath` runs the commit guard, so the suite would be
59-green or red depending on who spawned it.
60-

$ grep -n '_agi_env_stripped' -A3 extensions/agi/conftest.py
80:_agi_env_stripped = suite_guards.make_agi_env_stripped_fixture(
81-    GIT_CONFIG_SPAWN_VARS)
$ grep -n 'scope=' extensions/agi/bin/suite_guards.py
82:    @pytest.fixture(scope="session", autouse=True)
149-    @pytest.fixture(scope="session", autouse=True)
$ grep -n 'def make_agi_env_stripped_fixture' -A11 extensions/agi/bin/suite_guards.py
139:def make_agi_env_stripped_fixture(extra_keys=()):
...
149-    @pytest.fixture(scope="session", autouse=True)
150-    def agi_env_stripped():
151-        stripped = strip_dispatch_env(extra_keys)
152-        yield
153-        restore_dispatch_env(stripped)
```

ANSWER to the question the round left open: the strip is SESSION-scoped and
autouse, one instance built at conftest IMPORT time (`conftest.py:80-81`), torn
down at session end. It is not function-scoped and nothing else writes those
keys, so a test cannot re-set what it took -- the test file's comment that
module import is the only moment `AGI_CLI_PY` is readable is true, and the
`AGI_CLI_PY` seam is structural rather than a policy choice one test can undo.

## What I did NOT do, and why

- `experiment:a00-619731a3-9d4779` -- the DH.604 PARENT REVIEW is still outside
  its THOUGHT block (measured, above). Fixing it is a whole-block THOUGHT
  rewrite of another node; named on `experiment:a00-849236cb-114441` instead.
- The verdict's 9 `iter-DH.578` scratch paths (corrective item 3) -- another
  node's body block. Named, not edited.
- `extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[suite_guards.py]`
  -- briefed red on this base, file outside FILE SCOPE.
- No production line moved: `git diff --numstat -- extensions/agi/bin/cli.py
  extensions/agi/conftest.py` is empty. The test file is `24 11`.

## Struggles recorded for the next reader

- `write.py`'s `replace body N:M` consumed the `<!-- BODY:BEGIN -->` marker
  (coordinate 1 of the body region IS the marker) and its end index behaved
  exclusive, so several single-line replaces inserted a line and left the old
  one. `sub <old> => <new>` takes NO shell quoting and is the safe verb for a
  one-line node edit; `body_patch` refused my difflib hunk headers
  ("context mismatch"). Both are defects someone else will hit.
- One frontmatter of `experiment:a00-849236cb-114441` was lost and restored
  from `git show HEAD:` while repairing the above; the node now parses and
  carries its full frontmatter plus a new title.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.632, about THIS node alone.

(1) WHAT THE INSTRUCTION SAID, quoted: items 7 and 8 -- "the fixture now writes
a record shape PRODUCTION NEVER WRITES ... the round's only real byte change
made the fixture LESS faithful to the code it is a fixture for"; "the round
traded one blind spot for another and documented the trade in the wrong
direction".

(2) WHAT THE MACHINE ACTUALLY DOES: `cli.py`'s `done` path writes
`dispatch_node_id` through `setdefault(..., rec.get("node_id") or "")`, so the
key is present on a real seat's record and `""` when there is no dispatch id;
the reader refuses anything that is not a `str` containing `":"`. The pin's job
is to hold the READER to that, and it can only do that against a record the
reader could plausibly be handed. Measured both ways: the production shape
catches a `v is not None` mutant and a fallback mutant; the absent-key shape
catches only the second.

(3) THE NEAR MISS: annotating the absent-key fixture with a comment explaining
that it is deliberately a record production never writes. That is a second
sentence about the fixture where the bytes wanted a different fixture, and it
is the same move DH.617 made with the docstring -- it makes the pin honest
about what it measures and leaves it measuring the wrong thing. Also near-miss:
an assertion that production's writer does `setdefault` -- it pins a copy of a
fact `cli.py` owns instead of routing the fixture through the code.

(4) DEVIATION: the corrective's PARENT line says COMMIT every kid and node edit
before exiting; the round contract says a kid runs no git and `cli.py done` is
the only versioning step. The contract wins, and the residue is located by
WORKTREE PATH, not by a sha table (a node file's digest moves on every
`write.py` call -- that is why three of DH.617's four digests name no blob).
`git diff --numstat`, `git log`, `git show`, `git cat-file -t` were read-only.

CEVEAT not closed: the mutant proof is a hand-built copy of `bin` rather than a
committed test, so nothing re-runs it next round; and the leg-1 pin still
proves the one-sided thing DH.617 named -- a record carrying a real dispatch id
lands is covered by the same test's second assertion, not by new bytes.
<!-- THOUGHT:END -->

## Agent Notes
Fixture reverted to the PRODUCTION record shape (dispatch_node_id key present, empty string when no dispatch id); both mutants the pin used to miss now fail it, measured against a full bin copy in both fixture shapes; 0 production lines, 8 passed

PARENT REVIEW DH.632 (a00-ebe2ebd4): ACCEPTED 1 / demoted 0 / failed 0. Kid experiment:a00-0581fdf8-2bb4d2 on hypothesis:a-rounds-own-path-set-never-fails-open, branch tip bd203425b off 8197496d2, diff read as 24/11 in the test file and 0 production lines. One parent probe class run by me and pasted into probes: (wire) three full bin copies, control 8 passed, guard mutant if v is not None 1 failed 7 passed, fallback mutant 1 failed 7 passed, and the DH.617 absent-key fixture replayed from 8197496d2 gives 8 passed against the not-None mutant. Open: the DH.604 PARENT REVIEW is still outside the THOUGHT block of experiment:a00-619731a3-9d4779 and the verdict node still carries 9 iter-DH.578 scratch paths -- both named by the kid as NOT DONE, both in FILE SCOPE, neither falsified.
