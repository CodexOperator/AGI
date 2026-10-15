---
id: experiment:a00-1ec8fd12-e47d10
mint_id: d06d843cd0af4d75a0620611b6e1db48
type: experiment
parents:
  - hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file
next_edges: []
confidence: 0.8
edited_by: a00-b30a6d55
evidence_runs:
  - experiment:a00-1ec8fd12-e47d10
loop: hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "fixture on season2/main with a bare origin; mint an UNTRACKED node; verification.compare_count(groot, CURRENT, stamp=True)", "expected": "refusal by name, no verify-count.json written", "observed": "no baseline; NOT STAMPED: explicit --stamp; refused by name — 1 uncommitted node path(s) here: nodes/hypothesis/untracked-mint.md; state absent", "result": "HOLD"}
  - {"conjunct": 2, "class": "wire", "cmd": "fixture: commit a NON-.md file under nodes/; stamp; worktree deletes a committed .md node and commits the loss; mint an untracked filler; compare_count(wt/.agi, smoke)", "expected": "FAIL naming the lost node", "observed": "committed triple == smoke triple and the read FAILS naming nodes/hypothesis/b.md", "result": "CLOSED, HOLD"}
  - {"conjunct": 3, "class": "gate", "cmd": "fixture: stamp on MAIN; worktree deletes committed b.md and commits the loss; mint an untracked filler; compare_count(wt/.agi, {active:3})", "expected": "FAIL naming nodes/hypothesis/b.md", "observed": "FAIL \"committed active=2 below baseline=3; (working tree reported active=3) missing committed file(s): nodes/hypothesis/b.md\"", "result": "CLOSED, HOLD"}
  - {"conjunct": 3, "class": "wire", "cmd": "fixture: node c.md with status: deprecated committed; verification._committed_deprecated(groot, [\\\"nodes/gone.md\\\"] + manifest)", "expected": "None — the git-cannot-answer contract", "observed": "None — kid 5 turned the loop-s malformed-header `break` into `return None`; previously 0, which read committed active HIGH and masked drops silently (reachable via a commit landing between _node_manifest and _committed_deprecated in this shared tree)", "result": "defect — CLOSED by kid 5"}
  - {"conjunct": 3, "class": "wire", "cmd": "REAL TREE (this worktree, .agi): compare verification._committed_counts(groot, _node_manifest(groot)) with metrics.node_lifecycle_stats(nodes_dir, len(rglob(\\\"*.md\\\")))", "expected": "equal triples on a clean checkout", "observed": "metric {active:2902,deprecated:199,total:3101} vs committed {active:2897,deprecated:199,total:3096} — the 5 gap is exactly the five uncommitted kid nodes on this dirty tree; deprecated agrees at 199 both ways", "result": "HOLD"}
  - {"conjunct": 4, "class": "gate", "cmd": "fixture: stamp, then hand-correct the state reason cell and count, then re-stamp from clean bytes", "expected": "the corrected stamp names the manifest it was corrected to", "observed": "manifest_sha256 present and equal across the re-stamp; reason cell preserved verbatim", "result": "HOLD"}
profile: balanced
push_further: "close the FAIL-fallback hole my review named: when _committed_deprecated or _node_manifest returns None while _node_dirt is non-empty, compare_count falls back to the working-tree current[\"active\"] and the untracked-file mask returns; make that branch SKIP/refuse rather than compare, and guard the printed missing-file set on committed is not None so a git race cannot print stale names."
role: kid
scaffold_hash: 29222f515678588e
season: 2
title: A00 1ec8fd12 e47d10
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-1ec8fd12-e47d10

## Experiment

FIFTH and final pass on
`hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file`.
Four kids had already landed the claim (committed `*.md` manifest; parser-based
deprecated cell; refusal-by-name on dirt; `manifest_sha256`). One defect was
open. This round measured it, fixed it, and proved the fix on the built bytes.

### Pre-fix measurement (the defect, reproduced)

`/tmp/parent-probe-sm34e.py` probe 8, on the staged bytes before this round:

    fixture: node c.md with `status: deprecated` committed
    _committed_deprecated(groot, FULL manifest)   -> 1
    _committed_deprecated(groot, [missing] + man) -> 0      <-- OBSERVED
    _committed_deprecated(groot, man + [missing]) -> 0      <-- OBSERVED

MEASURED, not argued: `git cat-file --batch` answers `<path> missing` — two
fields, not three — for an object it cannot read, and the reader's
`if len(head) != 3 or head[1] != b"blob": break` returned the PARTIAL count as
if it were complete. A truncated DEPRECATED count is LOW, so
`_committed_counts` reported committed `active` HIGH by the number of lost
deprecations. Measured worst case (missing entry mid-manifest): committed
triple read `{active: 5, deprecated: 0, total: 5}` against a true
`{active: 3, deprecated: 1, total: 4}` — active two HIGH, the drop masked
silently, which is the exact failure class this hypothesis exists to kill.

WHY REACHABLE, not theoretical: `_node_manifest` and `_committed_deprecated`
are TWO separate git invocations. `grid.py commit --all` runs every 5 minutes
in this shared tree, so a commit deleting a node can land between them;
`HEAD:./<path>` then answers `missing`. The input is impossible on a frozen
HEAD — which is why this was a one-line fail-safe and not a redesign.

### The fix (built, not described)

`extensions/agi/bin/verification.py`, `_committed_deprecated` ONLY:

- the header guard now `return None` instead of `break`, and additionally
  requires `head[2].isdigit()` so a non-integer size cannot reach `int()`;
- the no-newline-in-stdout `break` is likewise `return None` — same class
  (a truncated stream is not an answer).

`None` is the function's own "git cannot answer" contract, so
`_committed_counts` returns None and the gate falls back to the working-tree
metric instead of comparing against a wrong number.

### Post-fix proof (A/B on the reverted bytes)

Both new tests were run against the PRE-FIX source by swapping the guard back
textually and restoring it in a `finally`: **2 failed, 9 deselected** pre-fix,
**11 passed** post-fix. Post-fix probe 8:

    full dep=1  broken-first dep=None  broken-mid dep=None

The load-bearing assertion is not "None came back" but the consequence: with
`_committed_counts` = None, `compare_count` never emits a note containing
`committed active=` — it fails on the working-tree count, so a real drop is
still CAUGHT rather than judged against a silently short number.

Regression hold, all four earlier kids, on the built bytes:

- kid 1: an untracked node present → stamp refuses BY NAME, no state file;
- kid 2: worktree read names `nodes/hypothesis/b.md`;
- kid 3: `.md`-only manifest, committed non-`.md` cannot offset the count;
- kid 4: `status: "deprecated"` and CRLF agree with `metrics.node_lifecycle_stats`.

## Evidence

Changed: `extensions/agi/bin/verification.py` (3 code lines + 5 comment
lines — under the 10-line ceiling) and
`extensions/agi/tests/test_verification_manifest.py` (+2 tests).

Suite, exactly the five files the parent named:

```
python3 -m pytest extensions/agi/tests/test_verification_manifest.py \
  extensions/agi/tests/test_verification.py \
  extensions/agi/tests/test_verification_kept_merge.py \
  extensions/agi/tests/test_verification_window.py \
  extensions/agi/tests/test_verification_seat_model.py -q
82 passed in 2.94s
```

Pre-fix falsifier, same two new tests, guard swapped back to `break`:

```
FAILED test_a_missing_blob_yields_none_never_a_truncated_count
FAILED test_a_stale_manifest_yields_no_drop_verdict_rather_than_a_wrong_one
E  assert {'active': 5, 'deprecated': 0, 'total': 5} is None
2 failed, 9 deselected in 0.38s
```

Probe 8 after the fix (no finding):

```
full dep=1 broken-first dep=None
[p8-missing-blob-truncates] NO FINDING
[p9-crlf-frontmatter] NO FINDING
```

No git operation was run. Nothing was reverted or restaged; the four earlier
kids' staged work is untouched and built on.

<!-- BODY:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid 5 is the pass that CLOSES the round, and I recorded it as a lean rather than a proof because my review drove one path it does not cover. WHAT THE ORDERS SAID: change the loop-s malformed-header arm from `break` to `return None`, add the test, keep every earlier falsifier green, <= 10 production lines. WHAT THE BYTES DO: `_committed_deprecated` now returns None on a header that is not three fields or whose second field is not `blob` (verification.py, kid 4-s block edited by kid 5), so `git cat-file --batch`-s `<path> missing` answer — reachable in this shared tree because `_node_manifest` and `_committed_deprecated` are two git calls and `grid.py commit --all` runs every 5 minutes — no longer returns a PARTIAL count that read committed active HIGH and masked drops silently. MY PROBES, ALL NINE GREEN ON THESE BYTES (/tmp/parent-probe-sm34{,b,c,d,e}.py): c1 gate — the explicit `--stamp` refusal by name with an untracked node present, no state written (SM.33-s false DROP stays fixed through all five kids); c2 wire — a committed non-.md under nodes/ no longer offsets the triple, and a worktree that lost a committed .md node FAILS naming nodes/hypothesis/b.md; c3 gate — the same FAIL through the untracked-filler mask; c3 wire — p8 now returns None, and the quoted-`status: \"deprecated\"` and CRLF fixtures both give committed == metric; c4 gate — a corrected stamp still carries manifest_sha256 beside a verbatim reason cell. I also ran the real-tree check the acceptance criterion names: on this worktree the committed triple is {2902,199,3101}... {2897,199,3096} — the 5 gap is exactly the five uncommitted kid nodes, and `deprecated` agrees at 199 both ways. I did NOT cite the kid suite as evidence (it is 82 passed on the tree; run as an integrity check only). NEAR MISS my review drove and could NOT close inside the five-kid ceiling: `using_committed = bool(committed and dirt)`, so when `_committed_deprecated` or `_node_manifest` returns None while `_node_dirt` is non-empty, `measured` falls back to the working-tree `current[\"active\"]` and conjunct 3-s untracked-file falsifier RETURNS on that branch — a git failure re-opens the mask. That branch also prints the `missing` file set from a manifest it did not vouch for. Neither is in the hypothesis-s falsifier list and both need git to fail mid-read, which is why this is a lean and not a disprove; I passed it forward as this node-s `push_further` rather than spend a sixth kid the dispatch ceiling forbids.
<!-- THOUGHT:END -->

## Agent Notes
Fixed the one open defect: the malformed-header guard in _committed_deprecated now returns None (was break, which returned a PARTIAL count), plus a head[2].isdigit() guard and the no-newline-in-stdout break. Pre-fix, measured on the staged bytes: a manifest entry with no blob made the committed triple read {active:5,deprecated:0,total:5} against a true {active:3,deprecated:1,total:4} — active HIGH, the drop masked silently. Post-fix None is the "git cannot answer" contract, so _committed_counts returns None and the gate falls back rather than comparing a wrong number. Falsified first: both new tests fail on the pre-fix bytes, and all 82 pass on the built bytes across the five named verification test files. 3 production code lines changed (under the 10-line ceiling); nothing reverted, the four earlier kids staged work built on unchanged.
