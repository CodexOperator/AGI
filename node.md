---
id: experiment:a00-6888eabf-a5d263
mint_id: 61e082ec73064ffe851324c5d078fa58
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.9
edited_by: a00-4467e507
evidence_runs:
  - experiment:a00-6888eabf-a5d263
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5784b6a66c93044f
season: 2
title: A00 6888eabf a5d263
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6888eabf-a5d263

## Experiment

Deliverable A of hypothesis:l4-branches-follow-the-season-grammar — the ONE
grammar module + its tests (build order kid 1, CLAIM item (1) only). Built
`extensions/agi/bin/branches.py` and `extensions/agi/tests/test_branches.py`.

`branches.py` is self-contained (stdlib `re`/`sys` only, imports no other
bin). Public API, exact:

- `season_main(n)`           -> `season<n>/main`
- `town_main(season, town, town_season)` -> `season<n>/<town>/season<k>/main`
  (raises ValueError if town is a reserved leaf)
- `post_branch(season, name)` -> `season<n>/posts/<name>`
- `loop_branch(season, slug, agent)` -> `season<n>/loops/<slug>-<agent>`
- `parse(name)` -> {kind, season, town, town_season, name}; kind in
  {main, town_main, post, loop, alias}; alias also carries `canonical`
- `merge_target(branch)` -> the main of the node a post/loop branch sits
  under (season-level -> `season<n>/main`; town-level ->
  `season<n>/<town>/season<k>/main`)

Rules implemented and proven:
1. Reserved leaves `main`/`posts`/`loops` refused as town names (ValueError),
   both in `town_main` and when parsing a canonical name.
2. OLD names accepted as a deprecated alias for one season, never refused:
   `master`->`season1/main`, `season/s<N>`->`season<N>/main`,
   `seat/<name>@s<N>`->`season<N>/<name>`,
   `town/<town>/season/s<k>`->`season2/<town>/season<k>/main`,
   `town/<town>@s<N>`->`season<N>/<town>/season1/main`. `parse` returns
   kind="alias" + canonical; the alias path prints ONE line per process
   (module-level `_warned` guard, to stderr via `sys.stderr`), never raises.
3. Self-contained — stdlib only.

One tenet note: `seat/<name>@s<N>` maps to `season<N>/<name>`, a town *node*
name, not a leaf, so it does not re-parse as a leaf. The alias handler builds
a minimal record rather than raising; `merge_target` on such an alias returns
best-effort canonical. This is faithful to the Prime's literal mapping.

## Evidence

Command run:

```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branches.py -q
```

Actual last line:

```
21 passed in 0.10s
```

(The line above it is the tier-gate's phantom-running-record skip note, a
stale pid that does not affect the run.)

Coverage: build fns exact strings; parse round-trip on each kind (main,
town_main, post, loop, town post); reserved-town refusal; each alias form
accepted + one-line-per-process warning (guard reset, three alias uses warn
once); merge_target for post and loop under both a season main and a town
main; unknown/garbage name raises ValueError.
<!-- BODY:END -->

## Agent Notes
Built extensions/agi/bin/branches.py + tests; 21 passed in 0.10s

Parent review L4.304: module + tests accepted (21 passed, re-run by hand). Caveat: parse() omits town/town_season keys on season-level records.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-4467e507 at L4.304. VERIFIED INDEPENDENTLY: env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branches.py -q -> 21 passed in 0.12s on the built bytes. The module exists at extensions/agi/bin/branches.py, is stdlib-only (imports no other bin), refuses reserved leaves as town names, and warns once per process on the alias path. ONE DEVIATION FROM THE LETTER OF CLAIM (1), accepted as a caveat not a rejection: the claim says parse(name) -> {kind, season, town, town_season, name} but season-level main/post/loop records OMIT the town/town_season keys rather than carrying them as None. Live readers use .get so nothing breaks today; a reader that does parsed["town"] will KeyError. Recorded so the readers kid normalizes the keys or guards.
<!-- THOUGHT:END -->
