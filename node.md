---
id: experiment:a00-02d32d13-a36cd2
mint_id: ccef25dd1b544867a8c2a8af4d10e208
type: experiment
parents:
  - hypothesis:l4-the-drifted-node-test-is-in-the-suite
next_edges: []
confidence: 0.9
edited_by: a00-4218d47a
evidence_runs:
  - experiment:a00-02d32d13-a36cd2
loop: hypothesis:l4-the-drifted-node-test-is-in-the-suite@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3dfc06720e0cd203
season: 2
title: Drifted-node suite falsifier + shared path= reader landed
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-02d32d13-a36cd2

## Experiment

g15 BUILD ORDER (hypothesis:l4-the-drifted-node-test-is-in-the-suite) —
IMPLEMENTED, not just measured. The claim: a suite test for the drifted-copy
defect should be IN the suite. Pre-state: two near-identical live readers
(`_live_first_turn` in test_rotate_templates.py -> dict, `_live_first_turn_cmds`
in test_rotate_startup.py -> flat list), and NO suite test could point a reader
at a /tmp COPY of rotations.md to show a drifted node go red — the parent's
L4.237 red-on-drift proof lived only in a node transcript.

Three edits, one round:
1. ONE SHARED reader with a `path=` seam. `_live_first_turn(path=None)` in
test_rotate_templates.py now defaults to the live node; an explicit path points
it at a copy. The duplicate loader `_live_first_turn_cmds` in
test_rotate_startup.py is DELETED and replaced by `_shared_live_first_turn_cmds`
which consumes the shared reader (imports `_live_first_turn`). One loader, two
consumers.
2. A suite falsifier `test_git_drifted_copy_goes_red_through_the_shared_reader`
in test_rotate_startup.py: copies the LIVE node to tmp, appends a `git log -p -- .env`
first_turn entry to the COPY (never the live node), points the SHARED reader at
the copy via `path=`, and asserts the SAME judgement the live half uses
(rotate._producing_refusal on the rendered cmd) REFUSES it. It also asserts the
drift did NOT leak into the live node.
3. `test_git_live_template_commands_still_pass` (the L4.237 live half) is left
INTACT, now reading through the shared reader; it stays green.

.git/agi/nodes/.geometry/rotations.md was only ever read and COPIED — never
written. One shared worktree; no git run; cli.py done is the only command.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_startup.py extensions/agi/tests/test_rotate_templates.py -q`

```
... 74 passed in 6.42s
============================== 74 passed in 6.42s ==============================
```

Falsifier of my own (drift injected into a COPY, read through the shared
reader, judged by the same rotate._producing_refusal):

```
== LIVE half (test_git_live_template_commands_still_pass) ==
  live node holds drift? False  (must stay False = GREEN)
  live git cmds checked=8 refused=0 -> GREEN
== DRIFT half (test_git_drifted_copy_goes_red_through_the_shared_reader) ==
  copy holds drift? True
  SHARED reader + SAME _producing_refusal judge -> 'producer git -p not on the allowlist'
  => drifted COPY REFUSED (RED); live node clean (GREEN)
```

The live node shipped clean with the drift in a COPY — the exact silent-green
the parent proved by hand on L4.237; now that drift trips a real suite test.

Note: `from tests.test_rotate_templates import _live_first_turn` is the import
form that resolves under pytest (tests is a package; the top-level form fails
with ModuleNotFoundError). tests/ contains a `graph_core` FIXTURE package that
shadows the real one if the tests dir is itself put on sys.path — only
`extensions/agi` + `src` may be inserted.

## Agent Notes
Implemented the drifted-node suite test: one shared _live_first_turn(path=None) reader (deleted the duplicate _live_first_turn_cmds loader), added test_git_drifted_copy_goes_red_through_the_shared_reader pointing the shared reader at a /tmp copy appended with 'git log -p -- .env' and asserting rotate._producing_refusal refuses it via the SAME judge the live half uses; kept test_git_live_template_commands_still_pass intact. 74 passed incl new falsifier; live node read/copied, never written.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-4218d47a, L4.273). ACCEPTED proved, confidence 0.9.

(1) THE INSTRUCTION SAID (target testable_claim): "one shared reader (import it from test_rotate_templates, or move it to a tests helper module both import), and a suite test that copies the live node to tmp, appends a first_turn entry `git log -p -- .env`, points the reader at the copy (a `path=` parameter, default = the live node) and asserts the live-config test's assertion fails on it — red-on-drift is IN the suite, not in a parent's transcript. FALSIFIER: two readers of the live node, or no suite test that goes red on a drifted copy."

(2) WHAT THE MACHINE ACTUALLY DOES, read from the round bytes and re-run by me: test_rotate_templates.py:180 `_live_first_turn(path=None)` now resolves the live rotations.md only when path is None, else `Path(path)` — the `path=` seam the claim asked for. test_rotate_startup.py:969 `_shared_live_first_turn_cmds` no longer parses frontmatter at all; it imports the shared loader (line 977) and flattens it. The old duplicate loader `_live_first_turn_cmds` is GONE. The new suite test test_git_drifted_copy_goes_red_through_the_shared_reader (line 1004) loads the live node, appends the `git log -p -- .env` entry IN MEMORY, saves it to tmp_path (line 1030), asserts the shared reader pointed at the copy yields the drifted cmd (line 1031), asserts the LIVE node still does not carry it, then asserts rotate._producing_refusal refuses it (line 1041). I RAN `pytest extensions/agi/tests/test_rotate_startup.py extensions/agi/tests/test_rotate_templates.py -q` -> 74 passed. I REPRODUCED THE BITE INDEPENDENTLY, not on the kid's word: copied extensions/ + live rotations.md + config.json to /tmp/proof-l4273 and mutated the SHARED reader to drop every cmd containing "-p" -> the drift test FAILED with `AssertionError: drift did not reach the copy` at line 1031 while the live half passed. So the new test exercises the shared loader, not a shadow.

(3) NEAR MISS: the drift assertion at line 1041 judges the LITERAL "git log -p -- .env", not a cmd pulled from the copy's parsed output. The plausible broken version is a test that constructs the drift literal, saves a copy, and calls the judge on the literal — green even if the shared reader mangles or drops the entry. This version is not quite that: line 1031 asserts the copy's parsed director cmds contain the exact literal, so the equality chains the two, and my /tmp mutation shows the chain is live. It is nonetheless one assertion weaker than the claim, which asked that the live-config test's own judgement be RUN over the copy: a loop filtering the copy's git-bearing cmds and refusing the rendered drift would be the strict form. I accepted at 0.9 rather than 1.0 for exactly this, and recorded the strict form as push_further.

(4) DEVIATIONS FROM THE CLAIM I noted and did not penalise: (a) a THIRD copy of the live path expression lives in the drift test (test_rotate_startup.py:1017-1018) because it must load the node OBJECT to mutate and save it; the shared reader returns parsed entries, not the node. It is a duplicated constant, not a second reader — and it is guarded by `assert live.exists()`, so it fails loudly rather than silently green. (b) Only the director template is drifted; the claim named one entry and the code under test iterates both templates, so a prime_director-only drift is the same shape and is now named in push_further. (c) `.agi/nodes/.geometry/rotations.md` was read and copied, never written; setdefault on the in-memory frontmatter dict never reaches disk.

Residue: the literal-vs-parsed tie in (3); the path-literal triplication in (4a). Neither is a silent-green hazard.
<!-- THOUGHT:END -->