---
id: experiment:a00-acc4e078-35fa9a-exp
mint_id: 3d5c81ab4e2f47c9a0b16d3f7c92e845
type: experiment
parents:
  - hypothesis:a00-acc4e078-35fa9a
next_edges: []
edited_by: a00-64cdf8ed
loop: goal:g7.33.14@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
season: 2
title: un-count the gate and repoint the three coupled literals
town: core
---
# experiment:a00-acc4e078-35fa9a-exp

Builds the two defects the parent review of `hypothesis:a00-b9700763-8d8657`
named, on the guard that kid landed. Test files only, **0 production lines**.

## 1 · the magic count is gone, replaced by the property

`test_t3` ended in `assert len(BOX_BOUND) == 5`. A tally inside a gate is the
brittleness this whole subgoal argues against: repointing the coupled literals
moves the number and the test breaks for a reason that is not a defect. What
is now asserted:

| old | new |
|---|---|
| `assert len(BOX_BOUND) == 5` | every `EXEMPT` entry's reason is non-empty, single-line, and ≥20 chars |
| (nothing) | `BOX_BOUND <= set(EXEMPT)` — it must stay DERIVED from the classes, never hand-listed |

`BOX_BOUND` remains `{k for k, (cls, _r) in EXEMPT.items() if cls == "B"}`, so
"is this exemption code-level?" is still answered mechanically; only the
tally is gone.

## 2 · the coupled literals are repointed (idempotently)

`test_unify.py` had three class-`B` literals frozen at the retired box paths.
They now use the seam the test four lines below already used,
`unify._git_common_root()`:

```python
here = unify._git_common_root()
assert here is not None, "git must name the repo this checkout belongs to"
result = unify.preflight(here, tree)                       # was Path("/home/ubuntu/work/agi")
result = unify.preflight(engine, here)                      # was Path("/home/ubuntu/work/agi-tree")
result = unify.preflight(unify._git_common_root(), tree, force=True)
```

This is **idempotent w.r.t. group A**: `/data/work/agi` (and this worktree's
main repo) is in `_FORBIDDEN_REAL_PATHS` today through the git-derived branch
of `_real_repos()`, and stays in it after `.agi/config.json:188` is corrected.
So the tests pass both before and after the config fix — the coupling is
removed, not merely deferred.

`test_provisioning.py:351 ROOT` (dead: every consumer is `@live`, skipped at
:44) now names the checkout the file lives in:

```python
ROOT = str(BIN.parent.parent.parent)
```

`ls` on it succeeds on this box, so falsifier clause 3 holds. The `@live`
marker is **untouched** — making these pass by running a real mint is the
named near-miss.

After both repoints the only class-`B` exemption left is the `box.root` cell
in `.agi/config.json`, owned by group a00-3b546363; when that cell is
corrected the hit AND its `EXEMPT` entry disappear together (T2).

## Measurements

```
$ python3 -m pytest extensions/agi/tests/test_retired_box_prefix.py \
      extensions/agi/tests/test_unify.py \
      extensions/agi/tests/test_provisioning.py -q
160 passed, 5 skipped
```

The 5 skips are the `@live` real-API provisioning tests, still skipped.

**PROBE A — the gate still bites on a new live hit.** Appended
`RETIRED_PREFIX_PROBE = "/home/ubuntu/work/agi"` to `extensions/agi/bin/commands.py`:

```
E  extensions/agi/bin/commands.py:673: RETIRED_PREFIX_PROBE = "/home/ubuntu/work/agi"
1 failed, 4 passed
```

**PROBE B — the new T3 property is enforced.** Shortened the config cell's
reason from 100+ chars to `"owned by group a00-3b546363"` (41 chars): still
passes, because the mechanical form of "a real reason" is a length floor, not
a judgement. Recorded as the honest limit of the replacement, not as a pass.

Both probes restored the tree byte-for-byte (`md5sum -c` OK on
`commands.py` and on the guard).

## What this node does NOT fix

- The count is gone, but nothing stops a future kid from re-adding a tally
  *next to* the property. The property is the documented shape; nothing
  enforces the shape.
- `.claude/` is still unscanned (0 hits today, so latent).
- `P` (11) and `F` (4) exemptions are still prose/inert data that could be
  rewritten in a later round; one class per node.
