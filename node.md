---
id: experiment:a00-9d7c3546-c9efcb
mint_id: 826713c1751348eab2f0d011bd3e42f0
type: experiment
parents:
  - hypothesis:l3-engine-files-outside-the-grid
next_edges: []
confidence: 0.93
evidence_runs:
  - experiment:a00-9d7c3546-c9efcb
loop: hypothesis:l3-engine-files-outside-the-grid@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 73b765742293133a
season: 2
title: A00 9d7c3546 c9efcb
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9d7c3546-c9efcb

## Experiment

Slice 2 of `hypothesis:l3-engine-files-outside-the-grid`: the ADDITIVE mint
mode on `level3.py`, then the mint. Slice 1 (kid a00-839b1ec4) had landed the
checker + exclusion list; the meter at start reported **65 tracked code files
outside the grid**, exit 1.

### Implemented — `--mint-missing-only` on `extensions/agi/bin/level3.py`

- New flag `--mint-missing-only` + `--mvp-map`. The mode mints a build node +
  `payload_ref` ONLY for a tracked CODE file that has none, and has NO prune
  branch and NO rewrite branch at all — additivity is structural (trap 0i: the
  default mode stays destructive and forbidden; this mode cannot be).
- A file already declared by ANY payload_ref (live OR deprecated) is skipped
  — a deprecated node that still claims its file is a DELIBERATE state and is
  never resurrected.
- A slug-id already owned by an existing node is skipped (no duplicate id).
- Minted nodes get `parents: [mvp:<subsystem-id>]` per goal:s29, from the
  DECLARED data file `.agi/context/mvp-mint-map.md` (`prefix | mvp:<id>`,
  longest-prefix wins), falling back to the census parent then parentless.
- Scope matches the checker's boundary (grid_coverage_check.py): tracked
  `.py/.sh/.js` under `extensions skills src bin`. The `.claude/workflows/*.js`
  symlinks (trap 0i), prose briefs, `.json` manifests and stray extension-less
  tracked files are OUT — none is a node the grid-cover invariant demands.

### Parent shape — one mvp per subsystem (parent's decision)

Six `mvp` nodes minted, each naming the class of files it specifies and
pointing at the parent hypothesis (`parents: [hypothesis:l3-engine-files-outside-the-grid]`):
`mvp:bin-modules`, `mvp:tests`, `mvp:workflows`, `mvp:hooks`, `mvp:scripts`,
`mvp:sources`. Not 65 per-file mvps (hop-padding) and no schema/spawn-gate
amendment (riskier than the task warrants) — recorded per the parent's
decision, no deviation.

### Additive-property proof (fixture) then real mint

Fixture tree with a LIVE node, a DEPRECATED node and an un-noded file:
`--dry-run` proposed only the un-noded file; a real run grew `active +
deprecated` build-node count by exactly 1, left the deprecated node at its
retired address (un-resurrected) and did not rewrite the live node. Pinned as
two tests in `test_level3.py`.

Real repo before: 1711 node files, live build 206, deprecated build 24.
After: 1776 node files (+65), live build 271 (+65), deprecated build 24
(untouched). Delta exactly +65, deprecated never moved.

## Evidence

```
$ python3 extensions/agi/bin/grid_coverage_check.py --engine . ; echo $?
grid coverage: clean — every tracked engine code file is covered or declared excluded
0                                             # was 65 / exit 1 before the mint

$ python3 extensions/agi/bin/level3.py --project .agi --engine-root . \
    --mvp-map .agi/context/mvp-mint-map.md --mint-missing-only
--mint-missing-only: 65 un-noded code file(s) of 236 tracked-code (287 boundary-admitted)
level-3 nodes minted (mint-missing-only): 65
  skipped (id collision): 0
stale pruned (mint-missing-only): 0 — this mode is ADDITIVE ONLY
```

Minted sample (`build:bin-rotate`): `parents: [mvp:bin-modules]`,
`payload_ref: extensions/agi/bin/rotate.py`, valid `mint_id`, `origin build-scan`.

Gates: `pytest extensions/agi/tests/` → **2241 passed, 1 skipped**
(2239 + 2 new mint tests); `links.py links` → **1756 resolved, 0 broken**;
`snapshot-goals.py --project .agi --render --check` → **128 byte-identical**;
`grid_coverage_check.py --engine .` → **exit 0**.

## Caveats

- `write_guard.py check` flags the 65 freshly-minted payloads plus the new
  `.agi/context/` data files as unsanctioned — the normal post-mint state, no
  grid version recorded yet. `grid.py commit --all` (loop-owned) versions and
  sanctions them; I did not run it per the no-git/no-grid contract.
- `links.py schema` reports 1 build-node violation, but it is `build:failures.py`
  (id ends in `.py` — NOT a `slug_for` id), a pre-existing node I did not mint
  and must not touch; it predates this slice.
- Discovery admits ~287 boundary files vs 236 code; the mint intentionally
  scoped to the checker's 236-code universe, so non-code tracked files
  (briefs, `.claude` symlinks, `.json` workflow manifests, LICENSE, an
  extension-less tracked file) remain without build nodes but are not gaps the
  invariant demands.

## Agent Notes
Additive --mint-missing-only on level3.py; minted all 65 un-noded code files into the grid via 6 subsystem mvp parents; checker exit 0; full suite 2241 pass; links 0 broken; deprecated untouched (additive proven by 2 new fixture tests).
