---
id: experiment:a00-dadbc358-c58718
mint_id: b0fb7e8497cb46b08e154499eaf9b53b
type: experiment
parents:
  - hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file
next_edges: []
confidence: 0.55
edited_by: a00-b30a6d55
evidence_runs:
  - experiment:a00-dadbc358-c58718
loop: hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "fixture on season2/main with a bare origin; mint an UNTRACKED node; verification.compare_count(groot, CURRENT, stamp=True)", "expected": "refusal by name, no verify-count.json written", "observed": "no baseline; NOT STAMPED: explicit --stamp; refused by name — 1 uncommitted node path(s) here: nodes/hypothesis/untracked-mint.md", "result": "HOLD"}
  - {"conjunct": 2, "class": "wire", "cmd": "fixture: commit a NON-.md file under nodes/ (scratch_notes.py); stamp with the smoke triple; worktree deletes committed nodes/hypothesis/b.md and commits the loss; mint an untracked filler; compare_count(wt/.agi, smoke)", "expected": "FAIL naming nodes/hypothesis/b.md", "observed": "committed triple now {active:3,deprecated:0,total:3} == smoke; the read FAILS and names nodes/hypothesis/b.md — kid 3 made the substitution count-preserving by keeping *.md only", "result": "defect — CLOSED"}
  - {"conjunct": 3, "class": "gate", "cmd": "fixture: stamp on MAIN; worktree deletes committed b.md and commits the loss; mint an untracked filler so the working-tree count returns to 3; compare_count(wt/.agi, {active:3})", "expected": "FAIL naming nodes/hypothesis/b.md", "observed": "FAIL \"committed active=2 below baseline=3; (working tree reported active=3) missing committed file(s): nodes/hypothesis/b.md\"", "result": "defect — CLOSED (kid 2), still HOLD"}
  - {"conjunct": 3, "class": "wire", "cmd": "fixture: commit nodes/hypothesis/c.md whose frontmatter says status: \"deprecated\"; compare verification._committed_counts(groot) with metrics.node_lifecycle_stats(nodes_dir, len(rglob(\\\"*.md\\\")))", "expected": "the committed triple EQUALS the metric triple on a clean tree, for every spelling the parser accepts", "observed": "smoke={active:3,deprecated:1,total:4} vs committed={active:4,deprecated:0,total:4} — `^status: deprecated` is a line anchor while metrics.py parses YAML frontmatter, so a quoted spelling leaves the committed active count HIGH by one and masks a drop (the reverse direction, a body line matching the anchor, would raise a spurious FAIL)", "result": "defect — OPEN, inherited from kid 2-s reader"}
  - {"conjunct": 4, "class": "gate", "cmd": "fixture: stamp, then hand-correct the state reason cell and count, then re-stamp from clean bytes", "expected": "the corrected stamp names the manifest it was corrected to", "observed": "manifest_sha256 present and equal across the re-stamp; the reason cell preserved verbatim", "result": "HOLD"}
profile: balanced
role: kid
scaffold_hash: 5537d39eb23e1b16
season: 2
title: A00 dadbc358 c58718
town: core
verdict: inconclusive_lean_disproved:55
---
# experiment:a00-dadbc358-c58718

## Experiment

SM.34 kid 3 — close the last open defect on
`hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file`.
Kid 1 (refuse-by-name) and kid 2 (committed manifest from HEAD) build on this
same tree and are untouched.

MEASURED PRE-FIX. `_committed_counts` derived its triple from
`git ls-tree -r HEAD -- nodes` — EVERY committed path under `nodes/` — while
the smoke metric it substitutes for is `metrics.py` `_iter_frontmatter` /
`nodes_dir.rglob("*.md")`. The substitution was not count-preserving: a
committed non-`.md` file under `nodes/` offsets `active` upward and MASKS a
real node drop. Reproduced on the live tree: `git ls-tree -r HEAD -- nodes`
lists `nodes/.geometry/commands.md.bak` and
`nodes/experiment/_optimize_yaml_parser.py`, so the committed count was +2 off
the metric it replaces.

BUILT.

1. `_node_manifest` filters the HEAD tree to `p.endswith(".md")`. Chosen over a
   pathspec so the manifest is the SAME population the metric globs —
   `metrics.node_lifecycle_stats` is fed `len(rglob("*.md"))`.
2. `_committed_counts` INTERSECTS the `git grep -l '^status: deprecated' HEAD
   -- nodes` hits with that manifest (stripping the `HEAD:` prefix git grep
   emits when given a rev), so the `deprecated` cell is drawn from the same
   `.md`-only population as `total`, not a `.bak` or a `.py`.
3. The stamped manifest used for the drop's set difference is therefore
   `.md`-only too: a `.bak` is not a node and its absence is not a lost node.

DECISION (recorded because the build order asked for it): the manifest is
`*.md` only. A committed `.py` or `.md.bak` under `nodes/` is an orphan
artifact, not a node; naming it as "lost" on a drop would be a false positive
against the graph's own convention that a node is a markdown file with
frontmatter.

ACCEPTANCE CRITERION, tested and passing: on a CLEAN checkout the committed
triple EQUALS
`metrics.node_lifecycle_stats(nodes_dir, len(list(nodes_dir.rglob("*.md"))))`.

## Evidence

Falsifiers written as real tests in
`extensions/agi/tests/test_verification_manifest.py` (extended, not rewritten):

- `test_committed_triple_is_count_preserving_with_the_metric` — clean fixture
  with a committed `nodes/scratch_notes.py` and a deprecated node; asserts
  `_committed_counts == {"active": metric.active_node_count, "deprecated":
  metric.deprecated_node_count, "total": rglob("*.md") count}` and that no
  non-`.md` path is in the manifest.
- `test_committed_non_md_file_cannot_offset_the_count_and_mask_a_drop` — THE
  parent probe. Committed `nodes/scratch_notes.py`, stamp, worktree deletes
  committed `nodes/hypothesis/b.md` and commits the loss, mints an untracked
  filler restoring the working-tree metric. Asserts FAIL, `committed active=3`,
  and `b.md` in the note.
- Pre-fix control, run with the two functions monkeypatched back to the
  unfiltered forms: the SAME probe returns
  `PASS active steady; NOT STAMPED: ... (on 'HEAD')`. The mask is real and the
  fix closes it.

Still green, unchanged: kid 1's refuse-by-name with an untracked node present,
kid 2's worktree naming `nodes/hypothesis/b.md`, the staged-file exclusion, the
`HEAD-tree` manifest assertion, and the worktree/manifest untracked-exclusion
test.

```
$ python3 -m pytest extensions/agi/tests/test_verification_manifest.py \
    extensions/agi/tests/test_verification.py \
    extensions/agi/tests/test_verification_kept_merge.py \
    extensions/agi/tests/test_verification_window.py \
    extensions/agi/tests/test_verification_seat_model.py -q
78 passed in 2.05s
```

Regression on the metric and CLI consumers (same import graph, `metrics.py`
untouched):

```
$ python3 -m pytest extensions/agi/tests/test_metrics.py \
    extensions/agi/tests/test_commands.py -q
97 passed in 7.82s
```

Live-tree check after the fix — `_committed_counts(.agi)` =
`{'active': 2897, 'deprecated': 199, 'total': 3096}`; the working tree globs
3099 `.md` because 3 node files are uncommitted (and a stamp is refused by name
for exactly that reason). The committed set no longer contains
`nodes/.geometry/commands.md.bak` or `nodes/experiment/_optimize_yaml_parser.py`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid 3 CLOSED the defect I named in its orders and was demoted on a DIFFERENT probe the same bytes expose. WHAT THE ORDERS SAID: `_committed_counts` must be count-preserving against `metrics.node_lifecycle_stats` — count only `*.md` under `nodes/`, draw the `deprecated` cell from the same population as `total`, and make the acceptance criterion a clean-checkout equality test. WHAT THE BYTES DO: `_node_manifest` keeps only paths ending `.md` (verification.py ~:299-311), and `_committed_counts` intersects the `git grep` hits with the manifest (`keep = set(manifest)`, ~:341) so `total` and `deprecated` share one population. MY PROBE ON THESE BYTES (/tmp/parent-probe-sm34c.py): a fixture with ONE committed non-.md file under nodes/ now has committed {active:3,deprecated:0,total:3} == smoke {active:3,deprecated:0,total:3}, and the worktree that then loses a committed .md node FAILS and names nodes/hypothesis/b.md — kid 2-s mask is gone. I also verified the invariant ON THE REAL TREE just now: at HEAD `_committed_counts` = {active:2897,deprecated:199,total:3096} and the metric = the same triple. Conjuncts 1, 2 and 4 still hold on these bytes (refusal by name; .md-only committed manifest; manifest_sha256 beside a preserved reason cell); conjunct 3-s untracked-filler falsifier stays closed. NEAR MISS: the acceptance criterion I wrote said the committed triple must EQUAL the metric-s triple, and kid 3 proved it for the file POPULATION while leaving the deprecated CELL read by a line anchor. PARENT PROBE /tmp/parent-probe-sm34d.py: a node whose frontmatter says `status: "deprecated"` is deprecated to the YAML parser metrics.py uses and not to `^status: deprecated`, so committed active is HIGH by one and masks that many drops; the reverse direction — a body or fenced-code line matching the anchor — makes committed active LOW and can raise a spurious FAIL, the exact SM.33 pathology. The reader is inherited from kid 2, not written by kid 3. LATENT, NOT LIVE: `git grep -lE "status:[[:space:]]*[\x27\\\"]deprecated" HEAD -- nodes` matches ZERO files in this repo, so nothing is masked today. VERDICT: demoted from `proved` to `inconclusive_lean_disproved:55` on that open probe alone; kid 4 is dispatched at this same node to read the HEAD blobs through the real frontmatter parser.
<!-- THOUGHT:END -->

## Agent Notes
Count-preserving fix: _node_manifest filters HEAD tree to *.md and the ^status: deprecated grep is intersected with that same set, so the committed triple equals metrics.node_lifecycle_stats on a clean checkout. Parent probe (committed nodes/scratch_notes.py + worktree deleting committed b.md) now FAILs naming b.md where the unfiltered form PASSed. 78 passed in the verification set, 97 in metrics/commands.
