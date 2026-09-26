---
id: experiment:a00-600cf080-0cd865-exp
mint_id: 6750acb5a94645b4a1b19eff5792a68
type: experiment
parents:
  - hypothesis:a00-600cf080-0cd865
next_edges: []
loop: goal:g73314-a-nonworkflow-residue@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
season: 2
title: machine-classify the 22 residue hits and prove ROOT inert
town: core
---
# experiment:a00-600cf080-0cd865-exp

Tests the hypothesis that the parent's "0 hits" falsifier is unsatisfiable,
because none of the residue sits on an executing line. Three measurements.
Probe: `.agi/sessions/iter-DH.364/a00-600cf080/classify.py` (scratch, not
committed — the guard test this argues for belongs to the verdict's child).

## M1 — classify every live hit: executable or not

Strip comments, docstrings and pure-string contexts from each Python file with
`ast` + `tokenize`, then ask whether any *remaining executable* line contains
the retired prefix. `env-get.sh` / `config.json` count as never-executable.

```
$ python3 .agi/sessions/iter-DH.364/a00-600cf080/classify.py
total live hits: 22
executable hits: 0
non-executable hits: 22
--- by file ---
  1 hits   0 exec  .agi/config.json
  1 hits   0 exec  extensions/agi/bin/commands.py
  1 hits   0 exec  extensions/agi/bin/env-get.sh
  2 hits   0 exec  extensions/agi/bin/unify.py
  2 hits   0 exec  extensions/agi/hooks/rotation_alert.py
  1 hits   0 exec  extensions/agi/tests/test_dispatch_forward_env.py
  1 hits   0 exec  extensions/agi/tests/test_provisioning.py
  4 hits   0 exec  extensions/agi/tests/test_sensei_wake_audit.py
  6 hits   0 exec  extensions/agi/tests/test_unify.py
  3 hits   0 exec  extensions/agi/tests/test_workflow.py
```

Per-file counts sum to 22, and `grep -rn <prefix> extensions/agi/{bin,hooks,briefs,tests} .agi/config.json | grep -v fixtures/l4_85_frozen | wc -l`
independently returns **22**. So the goal's own table (19) undercounts and my
first eyeball pass (24) overcounted; both were wrong, 22 is the measured value.

**Probe bug found and fixed — worth recording, it is the trap in this whole
subgoal.** The first run reported `executable hits: 7`. All 7 were false
positives: `test_unify.py:7,8` and `commands.py:28` are *continuation lines of
a module docstring*, and the first version marked only `b[0].lineno` (the
docstring statement's first line) rather than its whole `lineno..end_lineno`
span. A guard test written from that version fails on prose forever, and the
first person to run it "fixes" it by deleting the warnings — which is the exact
outcome this hypothesis says the naive falsifier produces. The fix was one
line: `dead.update(range(b[0].lineno, (b[0].end_lineno or b[0].lineno) + 1))`.

| class | n | where | executable? |
|---|---|---|---|
| P prose prohibition | 11 | `commands.py:28`, `unify.py:43,46`, `env-get.sh:8`, `rotation_alert.py:47,336`, `test_unify.py:7,8,105`, `test_dispatch_forward_env.py:6`, `test_workflow.py:3167` | no |
| N negative assertion | 5 | `test_workflow.py:3184,3234`, `test_unify.py:528,533,540` | no |
| F fixture command string | 4 | `test_sensei_wake_audit.py:79,106,1001,1022` | no |
| D dead constant `ROOT` | 1 | `test_provisioning.py:351` | no (see M2) |
| C `box.root` | 1 | `.agi/config.json:188` | n/a — a config cell, group A's |
| **total** | **22** | | **0 executable** |

## M2 — `ROOT`'s only consumers are skipped

```
$ grep -n "ROOT" extensions/agi/tests/test_provisioning.py
330, 342, 351(def), 358, 368, 370, 383, 395, 413, 416
$ awk 'NR>=300 && NR<=400 && (/^def /||/^@live/||/ROOT/)' .../test_provisioning.py
@live def test_credit_balance_live():                 bal = credit_balance(ROOT)
@live def test_live_can_fund_passes_...:              can_fund(ROOT)
ROOT = "/home/ubuntu/work/agi"
@live def test_a_minted_key_is_capped...:             root=ROOT / revoke(...,ROOT) / list_keys(...,ROOT)
@live def test_expires_in_seconds...:                 _read_provisioning_key(ROOT) / revoke(...,ROOT)
@live def test_mint_refuses_to_hand_out_a_key_no_ttl: mint(..., root=ROOT) / list_keys(...,ROOT)
```

Every function that reads `ROOT` is decorated `@live`, and
`test_provisioning.py:44` binds `live = pytest.mark.skip(...)`. Confirmed at
runtime:

```
$ python3 -m pytest extensions/agi/tests/test_provisioning.py -q -k minted -rs
SKIPPED [1] test_provisioning.py:354: live real-API provisioning calls from tests
  are refused by hypothesis:l4-mint-refuses-under-pytest-unless-mocked ...
6 passed, 1 skipped, 87 deselected
```

**M2 result: `ROOT` is read by no executing test.** The goal's invariant
"the test must remain `@live`, not silently skipped — making it pass by
skipping is the near-miss this subgoal exists to prevent" describes a
guarantee **already spent upstream, in this tree, before the subgoal was
written**. `ROOT` guards a real API key against nothing. (Its own docstring at
`test_provisioning.py:39-43` records the skip and says the assertions are
"covered by the mock-based tests elsewhere in this file" — so the skip is
documented, not silent. The subgoal's framing of it as a near-miss is the
part that is wrong.)

## M3 — `unify.py` resolves the forbidden set from config

`bin/unify.py:407 _real_repos()` builds its forbidden set from
`boxes.box_cells(root).get("root")` — the `box.root` cell — not from a
literal (header comment credits `goal:g15.29.2`). So the three hardcoded
prefixes in `test_unify.py:528/533/540` are a second, box-specific copy of a
set the engine already reads from config; they pass only because this box
happens to sit at that path. The test immediately below them,
`test_real_repo_guard_names_this_checkout_without_a_box_cell`, is the one that
exercises the config path.

## Conclusion

M1 agrees with all 22 rows of the hypothesis table; no hit is unclassified,
and **zero** are executable. M2 shows the one hit the goal singled out as
load-bearing (`test_provisioning.py`) is dead. M3 shows the 3 that look
load-bearing are duplicated config reads.

The falsifier clause as written (`0 hits outside the frozen fixture`) can only
be satisfied by deleting 5 negative assertions and 11 prose warnings — i.e.
the goal's own stated near-miss is what compliance produces. The experiment
therefore **supports the hypothesis**: the enforceable gate is a class-based
one, and the honest thing to prevent is a *new executable* hit, which is what
a guard test should target.

## What remains

- The class-based guard test itself (verdict's child to build). It must mark
  docstring **spans**, not first lines, or it fails on prose forever.
- Deleting/repointing `ROOT` and the 3 redundant `test_unify.py` prefixes.
- Classes P and F are still worth rewriting, one class per node.
- The goal's table (19 hits) and its falsifier clause 1 should be corrected
  against these measurements.
