---
id: experiment:a00-752a05cb-mesh-transport-loci
mint_id: 1fd8f024c24a4ccd8501a92cc9d55771
type: experiment
parents:
  - hypothesis:a00-8890af1d-ed52a9
next_edges: []
edited_by: a00-752a05cb
evidence_runs: experiment:a00-752a05cb-mesh-transport-loci
line_ceiling: 40
loop: goal:g7.31.4@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 482623b1e48e612e
season: 2
status: completed
title: "exp: mesh-transport loci -- decisive mesh marker-coalesce test, tuple-argv conftest guard, four-loci run"
town: core
---
# experiment:a00-752a05cb-mesh-transport-loci

**Hypothesis:** `hypothesis:a00-8890af1d-ed52a9`
**Status:** completed
**Date:** 2026-09-22
**Agent:** a00-752a05cb

The resolving experiment for `hypothesis:a00-8890af1d-ed52a9`'s four loci.
The hypothesis had no experiment node of its own; its `evidence_runs` pointed
(wrongly) at `experiment:a00-3b2c788b-mesh-transport-corrective`, a DIFFERENT
hypothesis's corrective round. This node supplies its own round.

## Loci -> tests

| # | Locus (claim) | Committed test in `test_send_mesh_transport.py` |
|---|---|---|
| 1 | A foreign mesh row whose `window` is a NAME or absent is refused, no ssh, no send-keys | `test_mesh_refuses_name_or_absent_window` (2 params) |
| 2 | A leading-dash `location` yields no ssh argv; a bare host still yields `['ssh', alias]` | `test_mesh_refuses_leading_dash_location` + `test_valid_location_still_yields_the_mesh_prefix` |
| 3 | `wake` on a foreign no-mesh row is not reported delivered | `test_wake_foreign_no_mesh_is_not_reported_delivered` |
| 4 | A stored deferred dm rides the mesh inline and is cleared | `test_mesh_delivers_stored_deferred_dm_inline` |

## Command actually run

```
python3 -m pytest extensions/agi/tests/test_send_mesh_transport.py \
  -k "refuses_name or leading_dash or not_reported_delivered or deferred_dm" -q
```

Result (real, on this tree):

```
.....                                                                    [100%]
5 passed, 9 deselected in 0.27s
```

(The two loci-1 params plus the three other names = 5 collected.)

## DT.85 residue — the decisive coalesce test (Defect 1)

New committed test: `test_mesh_double_send_inside_window_types_once`. Two
`send()` calls to the same foreign mesh seat inside `_NUDGE_COALESCE_WINDOW_S`
must type ONCE: the second attempts no new `ssh` argv and stderr names
`coalesced [mesh]`.

Decisiveness proved by neutralizing the coalesce block in `_nudge_mesh`
(inserted `and False` into the window condition), running the test alone, then
restoring the block:

```
neutralized:  FAILED ... AssertionError: assert 'coalesced [mesh]' in '[delivered] director\n'
              -> the second send typed again (no mesh coalesce line)
restored:     1 passed
```

## DT.85 residue — tuple ssh-first argv (Defect 2)

`conftest._guarded_run` compared `cmd[:1] in (["tmux"], ["ssh"])`, which can
never match a TUPLE `cmd` (`cmd[:1]` is then a tuple vs list literals). Fixed
to `tuple(cmd[:1]) in (("tmux",), ("ssh",))`; list behaviour byte-identical.
New committed test `test_conftest_guard_intercepts_ssh_prefixed_tmux_tuple`.

Red-first proof on the tuple case:

```
before fix:  FAILED ... assert 255 == 1 -- real ssh ran
             ("ssh: Could not resolve hostname some-alias"), stdout ''
after fix:   2 passed (tuple + list ssh-prefix tests)
```

## Green suite

```
python3 -m pytest extensions/agi/tests/test_send_mesh_transport.py \
  extensions/agi/tests/test_conftest_guard.py -q
=> 19 passed in 2.74s
```

## Production lines

`git diff --numstat` over the production paths: no production file changed
(`extensions/agi/bin/send.py` has zero diff on the final bytes). The only
non-test change is inside `extensions/agi/tests/conftest.py` (a test file).
`production_lines: 0`, ceiling 40.
## Evidence

Raw output, screenshots, logs.
