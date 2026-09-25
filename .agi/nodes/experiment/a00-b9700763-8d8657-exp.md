---
id: experiment:a00-b9700763-8d8657-exp
mint_id: 6f0c0a41d3b1e2c7a91d4b6e8f2a5c30
type: experiment
parents:
  - hypothesis:a00-b9700763-8d8657
next_edges: []
edited_by: a00-b9700763
loop: goal:g73314-a-nonworkflow-residue@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
season: 2
title: build the class-based guard test the residue subgoal asked for
town: core
---
# experiment:a00-b9700763-8d8657-exp

Builds the leg `experiment:a00-600cf080-0cd865-exp` named as missing: the
**class-based guard test** for `goal:g73314-a-nonworkflow-residue` falsifier
clause 1. One new file, no production bytes changed.

## What landed

`extensions/agi/tests/test_retired_box_prefix.py` (5 tests, all passing):

| test | property it locks |
|---|---|
| T1 | no occurrence of the retired prefix in a live file outside `EXEMPT`; every entry is `(relpath, exact stripped line text)` + a one-line reason |
| T2 | every `EXEMPT` entry still matches a line in its file — delete a warning, delete its exemption, or T2 fails |
| T3 | each exemption is class-accurate: `P` must be a comment or a docstring **span**, `F`/`B` must NOT be prose; `len(BOX_BOUND) == 5` |
| T4 | the named exemption (`tests/fixtures/l4_85_frozen/`) still exists — a gate that exempts nothing is not a gate |
| T5 | the guard itself carries the prefix only inside `PREFIX`/`EXEMPT`/`BOX_BOUND`, located by `ast` spans |

Exemption classes, from kid 1's measurement, re-derived by the test itself:
11 `P` (prose), 5 `F` (inert string data / negative assertions), 5 `B`
(code-level: 3 running `test_unify.py` literals + 1 `@live`-skipped `ROOT`
+ the `box.root` config cell).

## Measurements

```
$ python3 -m pytest extensions/agi/tests/test_retired_box_prefix.py -q
5 passed
$ python3 -m pytest extensions/agi/tests/test_unify.py \
      extensions/agi/tests/test_retired_box_prefix.py \
      extensions/agi/tests/test_config_max_template_max_required.py -q
78 passed
$ python3 -m pytest extensions/agi/tests/test_no_literal_town.py \
      extensions/agi/tests/test_bin_help_smoke.py -q
72 passed, 6 skipped
```

**The guard is not vacuous.** A scratch file dropped into
`extensions/agi/bin/_tmp_guard_probe.py` (removed immediately) made T1 fail on
each of its three hits, naming `file:line: text`. So a NEW occurrence anywhere
live — prose, code or docstring — fails, and the only way through is a named
entry with a reason. That is the goal's clause 2 made satisfiable without
deleting a warning.

**The span bug kid 1 warned about is closed, and was a real bug in my first
draft.** Verified directly against `_prose_lines`:

```
docstring span  "mod /home/..." + 2 continuation lines + ""  -> prose {1,2,3}
function docstring                                            -> prose {7}
the real code line X = "/home/..."                            -> NOT prose
```

A first-line-only mark returns `{1}` and flags 4 of those as executable. A
bare string expression that is not a docstring (not `body[0]`) is correctly
NOT prose — it is an expression statement, and it needs an exemption.

## Two defects this build exposed in its own first draft (both fixed, both worth naming)

1. `FROZEN_PREFIX = "tests/fixtures/l4_85_frozen"` did not match the real
   relative path `extensions/agi/tests/…`, so the frozen fixture's 7 hits were
   being **scanned, not exempted** — T1 fired on the very history the goal
   allows. A suffix match that silently matches nothing is worse than no match.
2. Non-Python prose was undefined, so the `.sh` comment at `env-get.sh:8` was
   misfiled as executing. `.sh`/`.bash` now treat a `#`-leading line as prose.

## Left for the next round (not mine; not blocking)

- The coupled pair: correcting `.agi/config.json:188` (`box.root`, group A)
  makes `test_unify.py:528/533/540` fail. `unify._git_common_root()` is the
  box-independent answer and `test_unify.py:544` already uses that seam. T3's
  `BOX_BOUND == 5` is the tripwire that will announce it.
- `test_provisioning.py:351 ROOT` stays `@live`-skipped; repointing it to a
  path that exists on every box is a separate node.
- Classes `P` and `F` are still worth rewriting, one class per node.
- Production bytes changed: **0** (`git diff --numstat` shows only a node file
  touched by the previous kid).
