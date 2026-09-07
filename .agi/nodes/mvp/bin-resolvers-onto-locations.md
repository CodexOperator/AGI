---
id: mvp:bin-resolvers-onto-locations
mint_id: d7caf3f15fcf44f6a81090290bd8d59d
type: mvp
parents:
  - goal:g11.1
next_edges: []
confidence: 0.93
edited_by: season.py
season: 1
source_files:
  - extensions/agi/bin/benchmark.py
  - extensions/agi/bin/cli.py
  - extensions/agi/bin/dispatch.py
  - extensions/agi/bin/metrics.py
  - extensions/agi/bin/post_wire.py
  - extensions/agi/bin/render-context.py
  - extensions/agi/bin/snapshot-build-site.py
  - extensions/agi/bin/snapshot-goals.py
  - extensions/agi/bin/spawn_gate.py
  - extensions/agi/bin/zoom.py
  - extensions/agi/tests/test_locations.py
status: implemented
tags:
  - g11.1
  - resolver
tests_pass: true
thought_session: season
title: All ten bin/ entry points delegate to locations.py; all ten were broken, not three
---
# mvp:bin-resolvers-onto-locations

The ten duplicated ancestor walks under `extensions/agi/bin/` now call
`locations.py`. The falsifier holds: exactly one `^CONFIG_NAMES` declaration
survives in `bin/`, in `locations.py` itself.

## The finding: ten of ten were broken, not three

`goal:g11.1` recorded three confirmed outages and the parent's brief added
`zoom.py` as a fourth. **Measured from both cwds before any edit, every one of
the ten was already broken in this repo** — because there is no
`agi-tree.config.json` anywhere in it. The only config is `.agi/config.json`,
which the legacy marker list does not name, so every copy of the old walk ran
to `/` and found nothing.

```
$ find /home/ubuntu/work/agi -name 'agi-tree.config.json' -o -name 'autoresearch-tree.config.json'
(no output)
```

Baseline, each file's own resolver run in a fresh process at each cwd
(`/tmp/probe.py`, one subprocess per file per cwd):

| file | from repo root | from `.agi/` | class |
|---|---|---|---|
| `benchmark.py` | exit 1 | exit 1 | **BROKEN — hard** |
| `cli.py` | exit 1 | exit 1 | **BROKEN — hard** |
| `dispatch.py` | `config_path` → None | None | **BROKEN — hard** |
| `metrics.py` | exit 1 | exit 1 | **BROKEN — hard** |
| `post_wire.py` | `SystemExit` | `SystemExit` | **BROKEN — hard** |
| `spawn_gate.py` | exit 1 | exit 1 | **BROKEN — hard** |
| `zoom.py` | `config_path` → None | None | **BROKEN — hard** |
| `render-context.py` | `<repo>` — wrong | `<repo>/.agi` — right | **BROKEN — silent, cwd-dependent** |
| `snapshot-build-site.py` | `<repo>` — wrong | `<repo>/.agi` — right | **BROKEN — silent, cwd-dependent** |
| `snapshot-goals.py` | root right, **config lookup wrong** | same | **BROKEN — silent** |

**Broken 10, merely duplicated 0.** The distinction the brief asked for turns
out to have an empty second column. Nothing here was a latent defect waiting
for a layout change; the layout had already changed.

Three sub-shapes, and only the first is an outage in the ordinary sense:

- **Hard (7).** Exit 1 with a message naming a file that does not exist. Loud,
  safe, and total: `cli.py`, `metrics.py`, `spawn_gate.py`, `post_wire.py`,
  `benchmark.py` refused every subcommand, and `dispatch.py`/`zoom.py` rejected
  every directory passed to them.
- **Silent wrong root (2).** `render-context.py` and `snapshot-build-site.py`
  had **no ancestor walk at all** — their `PROJECT_ROOT` was
  `os.environ(...) or os.getcwd()`. From the repo root they answered `<repo>`
  and aimed at `<repo>/nodes`, which does not exist. This is the `level3.py`
  failure shape the goal node records, in two more files.
- **Silent wrong config (1).** `snapshot-goals.py` resolved the *root*
  correctly and then read the config with its own leftover `config_path`,
  which does not accept a graph directory's bare `config.json`.

## `snapshot-build-site.py`, done first — and why it had not fired

It unlinks every build-site-origin node it does not re-derive (H0i) — the
marker string is deliberately not written out literally anywhere in this node,
because the project measures those nodes with a plain `grep -rl` over
`.agi/nodes/` and a node that quotes the marker inflates that count by one. Its
resolver answered `<repo>` from the repo root, so `BUILD_SITE` pointed at
`<repo>/context/plans/build-site.md`, which does not exist — and the L18
guard at `snapshot-build-site.py:277` returns *before* the prune when
`build-site.md` is missing. **That guard, not the resolver, is the only reason
159 nodes are still here.** Had the wrong root happened to contain a
`build-site.md`, the prune would have run against the wrong tree.

Counts, before and after every edit:

```
$ find /home/ubuntu/work/agi/.agi/nodes -name '*.md' | wc -l
812                     # before, and after
$ grep -rl '^origin: build-site$' /home/ubuntu/work/agi/.agi/nodes/ | wc -l
159                     # before, and after
```

**159, which is what the docs said.** An unanchored `grep -rl 'origin: build-site'`
returns 167, and 167 is wrong: eight of those files only *mention* the marker in
prose rather than carrying it in frontmatter — `goal:g11.1`, `goal:g7.8`,
`goal:s6`, `goal:s18`, `goal:s21`, `exp:g5-lifecycle-enforcement`,
`idea:engine-self-decomposition`, and `build:tests-test-snapshot-build-site`.
A bracket class (`origin:[ ]build-site`) defends this node against matching
*itself* but does nothing about the other eight; only the line anchors separate
a frontmatter field from a sentence about one. Confirmed by difference:

```
$ comm -13 <(grep -rl '^origin: build-site$' .agi/nodes/ | sort) \
           <(grep -rl 'origin: build-site'   .agi/nodes/ | sort) | wc -l
8
```

Recorded because the unanchored count was asserted here first, and briefly
corrected the documentation in the wrong direction.

## The `goal_body_cap` consequence, previously unmeasured

`snapshot-goals.py`'s leftover `config_path` returned `None` for
`.agi/config.json`, so `body_cap()` fell through to the engine constant
`BODY_CAP = 4000` — while `.agi/config.json` explicitly declares
`goal_body_cap: 0`, meaning *no cap*. The project's declared configuration was
being silently ignored in favour of an engine default.

```
$ python3 -c "...import snapshot-goals...; print(m.body_cap())"
0        # after the fix; was 4000
```

26 of 91 goal bodies exceed 4000 characters. **The exposure is the
`GOALS.md` → node direction, not the render.** `cap_body()` is called once,
from `parse_goals()` (line 536), which is the parse half — so a `--snapshot`
would have written 26 goal **node** bodies truncated at a block boundary,
each with a `> **[truncated: N of M characters dropped …]**` marker standing
where the rest of the goal used to be, against the project's own
`goal_body_cap: 0`. `GOALS.md` itself was never at risk; it is the copy
`cap_body`'s own docstring calls "the only complete copy".

Two things narrowed it, and neither is a fix: `driver.sh:85` runs only
`--render --strict-goals`, never `--snapshot`, so the loop does not reach the
truncating path on its own; and `--render --check` fails loudly on a
non-byte-identical round trip, which a 4000-char cap would have caused. The
parent confirmed the narrower claim empirically — a `--render` run *before*
this fix left `GOALS.md` byte-unchanged, which is what falsified the first
version of this paragraph. It asserted the render itself would truncate.

The same blind spot made `zoom.py`'s `default_runtime()` return `pi` instead
of `cc`, which hands every Claude-Code kid the wrong completion contract —
`goal:s8`, silently re-broken by the layout change.

Round trip after the fix, from both cwds, `GOALS.md` byte-unchanged:

```
$ python3 extensions/agi/bin/snapshot-goals.py --render --check
render --check: 91 goal(s) round-trip byte-identical
```

## Deviations, decided and recorded

- **`zoom.py` and `dispatch.py` take the root as an argument, so fixing
  `config_path` alone would not have fixed them.** Both demanded the given
  path already *be* the graph root, and under this layout the natural argument
  — the repo root — holds no config. Both now resolve the argument through
  `locations.find_project_root()`. `find_project_root` is the identity on a
  legacy root (phase 1), so no existing project resolves differently. This is
  a behaviour change and is the only one in this node.
- **`config_path` and `_find_root` are kept as names**, re-exported or as thin
  wrappers, rather than deleted. `dashboard.py:129` calls `metrics._find_root`
  and `render-context.py` imports `metrics.read_config`; deleting the names
  would have pulled in files outside the ten.
- **`grid.py` untouched** — owned by another kid this iteration. It is
  modified in the working tree by that kid, along with
  `.agi/nodes/.geometry/crons.md` and an untracked `.agi/nodes/.chain_cache.pkl`.
  Reported, not touched.
- **Not done: `engine_root`'s double derivation** (`level3.py` vs `grid.py`).
  The goal node puts it out of scope deliberately and it stays out.

## Regression tests

Appended to `extensions/agi/tests/test_locations.py`, 12 new tests:

- `test_only_locations_declares_the_marker_names` — the falsifier as a test.
  Verified it has teeth by running its regex against `HEAD`: it flags all ten.
- `test_entry_point_resolves_the_same_root_from_repo_and_graph_dir` —
  parametrized over the eight cwd-resolving entry points, each run in a fresh
  process at each cwd against a `tmp_path` fixture. This is the test that would
  have caught the two silent ones.
- `test_root_taking_entry_points_share_the_config_lookup` and
  `test_zoom_accepts_the_repo_root_and_the_graph_dir` — the argument-taking
  pair, the latter end-to-end.

## Gates

```
$ python3 -m pytest extensions/agi/tests/ -q
1041 passed          # 1029 before + 12 new, 0 failed, 0 skipped
$ grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py | grep -v ':0'
extensions/agi/bin/locations.py:1
$ python3 extensions/agi/bin/locations.py . --json | grep layout
  "layout": "graph_dir"
$ python3 extensions/agi/bin/metrics.py     # from repo root AND from .agi/
METRIC node_count=812 ... METRIC primary_metric=outcome_coverage   # identical
```

The measured baseline was **1029 passed, 0 skipped, 1029 collected** — not the
"1029 pass, 1 skipped" the brief stated.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1. The node exists because the sweep was supposed to produce a two-column
answer — broken versus merely duplicated — and one column came back empty.
That is worth a node on its own, separately from the code change.

I nearly reported the brief's framing back. `goal:g11.1` says three broke, the
brief says four, and both are stated with dates and evidence, so the honest
move looked like confirming four and collapsing the rest as tidiness. The
reason it is ten is a single fact neither document mentions: this repo has no
`agi-tree.config.json` at all. Once that is measured rather than assumed, every
copy of the old walk is dead, and the interesting question stops being "how
many broke" and becomes "why did seven of them break loudly and three quietly".
The three quiet ones are the finding. Two had no ancestor walk in the first
place — `os.getcwd()` wearing a `CONFIG_NAMES` constant beside it as
camouflage, which is why they read as duplicates rather than as the different
and worse thing they are. The third, `snapshot-goals.py`, is the one the goal
node had already marked "half-migrated" and I would have closed with a pure
deletion if I had trusted that label; its root was right and its config lookup
was wrong, and the two callers of that lookup were silently reverting the
project's declared `goal_body_cap` to an engine default.

I am recording the `goal_body_cap` and `default_runtime` consequences here
rather than in a separate node because neither is independently actionable —
both are already fixed by the same one-line delegation — but both are evidence
that "duplicated resolver" understates the failure mode. A duplicated resolver
that returns a wrong *root* fails loudly. A duplicated resolver that returns a
wrong *config* returns a plausible default and keeps going.

Confidence is 0.93 rather than higher for one reason: `benchmark.py` cannot be
exercised end-to-end here because `ollama` is not installed, so its resolver is
verified against a stubbed import rather than a real run.
<!-- THOUGHT:END -->