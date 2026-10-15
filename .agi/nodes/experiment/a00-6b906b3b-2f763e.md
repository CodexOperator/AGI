---
id: experiment:a00-6b906b3b-2f763e
mint_id: b51c897793424438aa5fdd4d2f7facca
type: experiment
parents:
  - hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert
next_edges: []
confidence: 0.9
edited_by: a00-b1d92d36
evidence_runs:
  - experiment:a00-6b906b3b-2f763e
loop: hypothesis:l4-the-reshuffle-plans-the-final-town-first-tree-from-the-town-tuples-and-the-mirror-line-lands-inert@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 11220447eacfe160
season: 2
title: A00 6b906b3b 2f763e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6b906b3b-2f763e

## Experiment

Region C (item 2 of the Prime XVII order) of the I-3a-2 round: build the hidden
MIRROR line so it LANDS INERT. Three deliverables, all landed and fixture-proved:

**1. `crons.md` declares the mirror (ONE key).** Added `mirror_towns: true`
under `cadences.grid_sync` in `.agi/nodes/.geometry/crons.md`
(`.agi/nodes/.geometry/crons.md`, the `cadences.grid_sync` block, line 8).
`load_crons_node` parses it without breaking any existing key — verified on
the live node: `grid_sync: {enabled: True, every_mins: 5, schedule: None,
mirror_towns: True}`, `branch_push`/`publish_engine`/`engine_push` untouched,
`crons_live: true` intact. A non-bool value is refused BY NAME
(`extensions/agi/bin/crons.py`, `load_crons_node`, the `if name == "grid_sync"`
block).

**2. `crons.py` renders a GUARDED push per town.**
- `_mirror_towns(root)` (`extensions/agi/bin/crons.py`, added near the render
  region) resolves the town set EXACTLY as `cli.py::_rs_town_set` does —
  `towns.town_tuples(root)` when a `town:*` node exists, else the ladder.md
  `towns:` fallback (lazily `import cli`, single source of truth with the
  planning region; never a hardcoded app town). Returns [] when the set is
  undeclared or unresolvable, so a corrupt geometry never bricks the crontab
  apply and a town-less graph renders no mirror lines.
- `_mirror_push_line(town, root, repo_root, log, sched)`
  (`extensions/agi/bin/crons.py`) renders each line to the pinned shape:
  `{sched} cd {root} && if git -C {repo_root} for-each-ref
  --format='%(refname)' refs/heads/{town}/ | grep -q .; then git -C
  {repo_root} push -q origin 'refs/heads/{town}/*:refs/agi/{town}/*' >>
  {log} 2>&1; fi` — pushes ONLY to `refs/agi/<town>/*`, NEVER to
  `refs/heads/...`.
- `render_managed_lines` (the `grid_sync` block, after its own line) appends
  one mirror line per declared town when `jobs["grid_sync"].get("mirror_towns")`
  is true, on the same `*/5 * * * *` grid_sync schedule.
- The guard makes it a NO-OP (rc 0, no push, no log write) while no
  `refs/heads/<town>/` ref exists — proven in the fixture.

Rendered against the REAL tree (from this worktree, resolution-only; no live
apply): three guarded lines, one per ladder town (`core`,
`streaming-suite`, `web-app-suite`), e.g.
`*/5 * * * * cd .agi && if git -C <repo> for-each-ref --format='%(refname)' refs/heads/core/ | grep -q .; then git -C <repo> push -q origin 'refs/heads/core/*:refs/agi/core/*' >> <log> 2>&1; fi`.

**3. Restore command** (written into the node body / runbook note):

```
git config --add remote.origin.fetch '+refs/agi/*:refs/agi/*'
```

This is the ONE command that restores the hidden `refs/agi/*` refs on a fresh
box after a clone (without it the mirror's pushes land on the origin but are
never fetched locally).

**4. Tests — `extensions/agi/tests/test_crons_mirror.py` (new).** A fixture
`git` repo (root IS the graph dir + repo, the make_project shape) with a fake
BARE origin, `HOME` sandboxed into `tmp_path` so rendered `>> <log>` appends
stay in the test. Every guard test runs the REAL rendered line through
`bash -c` and asserts by `git ls-remote` on the fake origin:
- no `refs/heads/<town>/*` -> the guard does NOTHING: rc 0, the fake origin's
  ref list stays empty, and `refs/heads/*` on the origin is untouched.
- with a real `refs/heads/core/main` present (pushed to origin once so the
  origin already carries it) -> running the guard pushes it under
  `refs/agi/core/main` ONLY: `refs/heads/core/main` STILL exists and remains
  the only `refs/heads/*`, and exactly one new `refs/agi/*` ref appears.
- the rendered line shape is pinned: single line, `*/5` prefix, `cd {root} &&`,
  the `for-each-ref` guard strictly BEFORE `push -q origin`, the town-scoped
  refspec `'refs/heads/core/*:refs/agi/core/*'`, and never `:refs/heads/`.
- parser tests: `mirror_towns: true` parses, absent defaults to false, a
  non-bool `mirror_towns` is refused by name.

## Evidence

Command (both crons files):

```
python3 -m pytest extensions/agi/tests/test_crons_mirror.py extensions/agi/tests/test_crons.py -q
```

Result: **77 passed** (6 new mirror tests + 71 existing crons tests, all
green — no regression to the parse/render/apply/marker/unit surfaces).

Live-node parse check on the edited `crons.md`:

```
node["jobs"]["grid_sync"]  == {enabled: True, every_mins: 5, mirror_towns: True}
node["crons_live"]         == True
```

Real-tree render (worktree, resolution only — NO live `crons.py apply`, NO
crontab touched, NO push; the live apply is the Prime's): three guarded mirror
lines, one per ladder town, shape matching the spec byte-for-byte.

Verdict: **proved** — the mirror is declared by graph content, rendered by
`crons.py` as guarded per-town pushes to `refs/agi/<town>/*` only, and
fixture-proven to land inert (no-op when no town refs exist) and to mirror
exactly when they appear. No live crontab, ref, or push changed: the live tree
is untouched by this round.

## Agent Notes
Region C: crons.md mirror_towns:true declares the grid_sync town mirror; crons.py renders one GUARDED per-town push to refs/agi/<town>/* only (inert no-op until town refs exist, fixture-proven by ls-remote); restore cmd written. 77 crons tests green, live tree untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (L4.334): accepted proved. (1) WHAT THE BRIEF SAID: region C -- crons.md declares the mirror by ONE key, crons.py renders a GUARDED per-town push to refs/agi/<town>/* only, inert until refs exist, the town set = towns.town_tuples with the ladder fallback, plus fixture tests and the restore refspec line. (2) WHAT THE MACHINE ACTUALLY DOES: .agi/nodes/.geometry/crons.md adds mirror_towns:true under cadences.grid_sync; crons.py load_crons_node refuses a non-bool by name and defaults absent to false; _mirror_towns lazily imports cli._rs_town_set (single resolution with the planning region) and returns [] on an undeclared set; _mirror_push_line renders a single shell line whose for-each-ref guard runs BEFORE the push and whose refspec is refs/heads/<town>/*:refs/agi/<town>/*; render_managed_lines appends one line per town inside the grid_sync block. The parent re-ran the crons suite: 77 passed in 4.08s, and read test_crons_mirror.py -- both guard tests run the REAL rendered line through bash against a fake bare origin and assert by ls-remote: with no town refs the line is a no-op with an unchanged origin; with refs/heads/core/main present exactly one refs/agi/core/main appears and refs/heads/core/main stays the only refs/heads ref. (3) THE NEAR MISS: a render that emitted the push unconditionally would still work when refs exist and would log noise or push a nonexistent wildcard when they do not; the fixture no-op test is what proves the guard is real. A line that published a second refs/heads name would pass a naive did-it-push check while publishing the wrong namespace; the pinned-shape test asserts the string :refs/heads/ never appears. (4) DEVIATION ACCEPTED AND RECORDED: _mirror_towns catches broad Exception and returns [] so a corrupt geometry cannot brick the 5-minute crontab apply; defensible because the mirror lines are guarded no-ops anyway and the live crontab is the higher-order invariant. (5) LIVE INVARIANT HELD: crons.py apply ran only on fixtures; the parent did not run a live apply; render on the live tree resolves the three ladder towns because locations.find_project_root returns the graph dir that _rs_town_set expects. Proved is per-experiment (region C), not a claim that the whole hypothesis is finished -- region B and the full real-tree proof remain.
<!-- THOUGHT:END -->
