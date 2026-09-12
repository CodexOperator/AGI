---
id: experiment:a00-5e1a3534-d342eb
mint_id: 2b44a8c02392413880add0dce2b59745
type: experiment
parents:
  - hypothesis:l4-a-join-matches-the-delimited-window-token-and-keep-both-is-tested
next_edges: []
confidence: 0.9
edited_by: a00-3cf95563
evidence_runs:
  - experiment:a00-5e1a3534-d342eb
loop: hypothesis:l4-a-join-matches-the-delimited-window-token-and-keep-both-is-tested@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 55c4fd8f7ef3fc6a
season: 2
title: A00 5e1a3534 d342eb
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5e1a3534-d342eb

## Experiment

L4.302 FIX-ONLY (mur-42 P1 line (2); Prime verbatim: "test_rotate_handover
Clause A regression test is green on the PRE-fix substring code — make it red
on pre-fix bytes").

**Defect:** the landed Clause A test
`test_join_matches_window_id_as_delimited_token` was GREEN on the pre-fix
substring code. Its fixture wrote pid 10001 with `@30` and pid 10002 with
`@302`; sorted glob is filename order (10001.json then 10002.json), and with
the pre-fix `if token not in raw` the first file (`@30`) matched `@30` BY
ACCIDENT of ordering. The test never falsified the substring bug.

**Fix (test only, `extensions/agi/tests/test_rotate_handover.py`):** re-seeded
the Clause A fixture so the join for `@30` MUST fail on pre-fix bytes. Now TWO
raw files BOTH contain the substring `@30`, and the `@302` file sorts FIRST:

    _reg_file(reg, 10001, "sid-threeoh-two", "/home/u/two", "@302")  # raw ...view:@302.%0
    _reg_file(reg, 10002, "sid-thirty",     "/home/u/one", "@30")   # raw ...view:@30.%0

- 10001.json raw = `{"session_id":"sid-threeoh-two","cwd":"/home/u/two","tmux":"view:@302.%0"}`
  (contains substring `@30`, sorts first)
- 10002.json raw = `{"session_id":"sid-thirty","cwd":"/home/u/one","tmux":"view:@30.%0"}`
  (the plain @30 file, sorts second)

Assertions kept: `@30` → pid 10002 (the @30 file) NOT 10001; `@302` → pid
10001; named miss `@999`. No `rotate.py` change was needed — the landed
`_registry_matches_window_id` delimited fix is complete.

**Proved it is a real falsifier** on a scratch copy in `/tmp/rotfix/` (never
mutating the live worktree): reverted the one clause-A match line to the
pre-fix substring form and ran the test → RED. Restored live tree (post-fix) →
GREEN. Paste both outputs + the `joined by @...` lines below.

## Evidence

**RED — pre-fix bytes (scratch copy `/tmp/rotfix/rotate.py`):
`if token not in raw: continue`**

```
E       assert 10001 == 10002
test_rotate_handover.py:765: AssertionError
FAILED test_rotate_handover.py::test_join_matches_window_id_as_delimited_token
1 failed in 0.20s
```

Pre-fix `@30` joins the WRONG file (pid 10001, the @302 file that sorts first):

```
PRE-FIX @30 -> 10001 | joined by @30 in registry file 10001.json
```

**GREEN — post-fix bytes (live worktree, `_registry_matches_window_id`):**

```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotate_handover.py -q
.............................   [100%]
29 passed in 9.79s
```

Post-fix joins land on the right file:

```
POST-FIX @30  -> 10002 | joined by @30  in registry file 10002.json
POST-FIX @302 -> 10001 | joined by @302 in registry file 10001.json
POST-FIX @999 -> None  | registry file for @999 not found ... (named miss)
```

The clause-A regression test is now a genuine falsifier: it turns RED when the
delimited-token guard is reverted to a bare-substring match, and GREEN on the
landed fix.

## Agent Notes
Re-seeded Clause A fixture so @30 MUST fail on pre-fix substring form: @302 file (pid 10001) sorts first and also carries substring @30; test now RED on reverted pre-fix, GREEN on landed delimited fix. No rotate.py change needed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-3cf95563, L4.302) -- ACCEPTED proved, confidence 0.9.

WHAT THE INSTRUCTION SAID: the target node L4.302 clause says verbatim: "test_rotate_handover Clause A regression test is green on the PRE-fix substring code -- make it red on pre-fix bytes ... prove it in the experiment node by reverting the one line on a scratch copy and running the test: red; restore: green. CEILING: 1 kid. FILE SCOPE: test_rotate_handover.py only".

WHAT THE MACHINE ACTUALLY DOES (I BUILT AND RAN it, not read it): I copied extensions/agi to /tmp/agi302verify, reverted the one call line in the COPY (bin/rotate.py:5891 `_registry_matches_window_id(data, token)` -> `if token not in raw: continue`), and ran the test there: RED, `assert 10001 == 10002` at tests/test_rotate_handover.py:765 -- the pre-fix substring matcher joins @30 onto the @302 file that sorts first, which is exactly the defect. On the landed tree the suite is 29 passed. The fixture now seeds @302 at pid 10001 (sorts first AND its raw text contains the substring @30) and @30 at pid 10002, so ordering can no longer mask the bug. The git diff is confined to test_rotate_handover.py plus this node.

THE NEAR MISS (the plausible implementation that satisfies the words and loses the mechanism): a fixture that merely ADDS a @302 file while leaving the @30 file first in glob order satisfies "seeds two registry files whose raw JSON both CONTAIN @30" and still loses the clause -- the pre-fix matcher hits the @30 file first and the test passes green on broken bytes, i.e. the same non-falsifier the fix was cut to eliminate. The ordering is the whole test; the kid got it right by giving @302 the LOWER numeric pid.

CAVEATS, none blocking: (1) the assertions cover pid/path/session_id; the pin cell that the original clause B names as an identity cell is still unasserted in the ref-equal branch (owed from L4.295). (2) the fixture writes tmux shape view:@302.%0 rather than the claim illustrative @302.%302 -- equivalent for a substring test, since both raws contain @30. (3) no rotate.py change was needed; the landed _registry_matches_window_id delimited match is complete.
<!-- THOUGHT:END -->

PARENT REVIEW L4.302 (a00-3cf95563): ACCEPTED proved at 0.9. Independently reproduced the falsifier -- reverted the clause-A match line on a scratch copy of extensions/agi and the test goes RED (assert 10001 == 10002), landed tree 29 passed. Fixture now has @302 sorting first, so the test is a genuine falsifier of the pre-fix substring join. Evidence: experiment:a00-5e1a3534-d342eb. Owed small fix-only, not blocking: pin-cell assertion in the ref-equal branch.
