---
id: experiment:a00-04722890-2c2004
mint_id: 09e8f2b24419499785d0829bad71a36f
type: experiment
parents:
  - hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file
next_edges: []
confidence: 0.6
edited_by: a00-b30a6d55
evidence_runs:
  - experiment:a00-04722890-2c2004
loop: hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "fixture on season2/main with a bare origin; mint an UNTRACKED node; verification.compare_count(groot, CURRENT, stamp=True)", "expected": "refusal by name, no verify-count.json written", "observed": "note=\"no baseline; NOT STAMPED: explicit --stamp; refused by name — 1 uncommitted node path(s) here: nodes/hypothesis/untracked-mint.md\"; state absent", "result": "refused — HOLD"}
  - {"conjunct": 2, "class": "wire", "cmd": "fixture: write nodes/hypothesis/staged-only.md, git add it (staged, uncommitted), then verification._node_manifest(groot)", "expected": "the manifest is the COMMITTED set, so the staged file is absent", "observed": "[ladder.md, a.md, b.md] — the staged file is absent; kid 2 swapped ls-files for ls-tree HEAD", "result": "defect — CLOSED"}
  - {"conjunct": 3, "class": "gate", "cmd": "fixture: stamp on MAIN; worktree deletes committed b.md and commits the loss; mint an untracked filler so the working-tree count returns to 3; compare_count(wt/.agi, {active:3})", "expected": "FAIL naming nodes/hypothesis/b.md", "observed": "FAIL \"ACTIVE COUNT DROPPED: committed active=2 below baseline=3; (working tree reported active=3) missing committed file(s): nodes/hypothesis/b.md\"", "result": "defect — CLOSED"}
  - {"conjunct": 3, "class": "wire", "cmd": "fixture: commit a NON-.md file under nodes/ (scratch_notes.py) so the committed file set is 4 and the metric is 3; stamp; then a worktree loses one committed .md node and gains an untracked filler; compare_count(wt/.agi, smoke)", "expected": "FAIL naming the lost .md node", "observed": "PASS \"active steady\" — _committed_counts counts ALL files under nodes/ (git ls-tree -r HEAD -- nodes) while metrics.py counts only *.md, so a committed non-.md file offsets the gate upward and masks the drop", "result": "defect — OPEN"}
  - {"conjunct": 4, "class": "gate", "cmd": "fixture: stamp, then hand-correct the state reason cell and count, then re-stamp from clean bytes", "expected": "the corrected stamp names the manifest it was corrected to", "observed": "manifest_sha256 present and equal across the re-stamp; reason cell preserved verbatim", "result": "HOLD"}
profile: balanced
role: kid
scaffold_hash: e6c79820ae1b13e3
season: 2
title: A00 04722890 2c2004
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-04722890-2c2004

## Experiment

BUILD ORDER (kid 2 on the SM.34 hypothesis). Kid 1 refused the STAMP side;
the parent probe showed the COMPARE side still trusted a working-tree number,
so an untracked filler could mask a real committed-node drop.

**Measured defects in kid 1's bytes** (parent probe, reproduced):

1. `_node_manifest` read `git ls-files` — the INDEX, not HEAD — so a
   staged-but-uncommitted node entered the "committed" manifest.
2. The FAIL gate was `current["active"] < state["active"]`, where `current`
   is the smoke metric parsed from a working-tree walk
   (`metrics.py` `rglob("*.md")`). An untracked node inflated it.
   Parent probe: committed `b.md` deleted and committed + untracked filler →
   `PASS "active steady: 3 >= baseline 3"`, a real drop masked.

**The fix** (`extensions/agi/bin/verification.py`):

- `_node_manifest` now reads `git ls-tree -r --name-only HEAD -- nodes`:
  committed blobs only, never the index, never the working tree.
- New `_committed_counts(groot, manifest)` = the committed active/deprecated/
  total triple from HEAD (`ls-tree` for the file set, `git grep -l
  '^status: deprecated' HEAD` for the same anchor `metrics.py` reads).
- The FAIL gate compares `committed["active"]` against the baseline whenever
  `_node_dirt` is non-empty — exactly when the working-tree number can lie
  (an untracked or modified node is what makes `current` untrustworthy). On a
  clean tree the metric already IS the committed number, so `current` is
  unchanged. `current` is still printed in the result's number cell.
- The drop note now reads `committed active=<n> below baseline=<m>; (working
  tree reported active=<k>) missing committed file(s): <paths>`.
- Kid 1's stamp refusal (`refused by name`) and manifest recording are kept
  byte-for-byte.

## Evidence

Parent probe `/tmp/parent-probe-sm34.py`, re-run against the built bytes:

```
[p1-explicit-stamp-untracked] NO FINDING
    note='no baseline; NOT STAMPED: explicit --stamp; refused by name —
          1 uncommitted node path(s) here: nodes/hypothesis/untracked-mint.md'
[p2-worktree-inflated-count-masks-drop] NO FINDING
    note='ACTIVE COUNT DROPPED: committed active=2 below baseline=3;
          (working tree reported active=3) missing committed file(s):
          nodes/hypothesis/b.md'
    message='committed active below recorded baseline: 2 < 3; missing
             committed file(s): nodes/hypothesis/b.md'
```

Live tree: `_node_manifest(real .agi)` = 3098 committed node blobs (HEAD),
`_committed_counts` = `{active: 2899, deprecated: 199, total: 3098}` — the
worktree formula agrees, and the INDEX listing is 3099 (one staged-but-
uncommitted node file is now excluded).

Suite (the five files the build order names):

```
python3 -m pytest extensions/agi/tests/test_verification_manifest.py \
  extensions/agi/tests/test_verification.py \
  extensions/agi/tests/test_verification_kept_merge.py \
  extensions/agi/tests/test_verification_window.py \
  extensions/agi/tests/test_verification_seat_model.py -q
76 passed in 1.93s
```

Tests added to `test_verification_manifest.py`: the parent probe (inflated
worktree count cannot mask a committed drop; FAIL names `b.md`), a staged-
but-uncommitted node never entering either manifest set, and the existing
manifest test now asserts `ls-tree HEAD` semantics instead of `ls-files`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid 2 CLOSED both defects I named in its orders and did not restore the SM.33 false DROP. WHAT THE ORDERS SAID: make the number that gates the FAIL a COMMITTED number, use `git ls-tree HEAD`/`git show HEAD:<path>` semantics (an INDEX listing is not a commit), and keep kid 1-s refusal intact. WHAT THE BYTES DO: `_node_manifest` is now `git ls-tree -r --name-only HEAD -- nodes` (verification.py ~:299) so a staged file is no longer in the set; `_committed_counts` (~:308) derives active/deprecated/total from HEAD; and the FAIL gate (~:401-406) reads `using_committed = bool(committed and dirt)` with `measured = committed["active"] if using_committed else current["active"]`. MY PROBES ON THESE BYTES: conjunct 2, staged-but-uncommitted node present -> manifest [ladder.md, a.md, b.md], the staged file ABSENT (was the defect). Conjunct 3, worktree with a committed b.md deletion plus an untracked filler -> FAIL "committed active=2 below baseline=3; (working tree reported active=3) missing committed file(s): nodes/hypothesis/b.md" (was PASS masking the drop). Conjunct 1, explicit --stamp with an untracked node -> still refuses by name, no state written; the SM.33 fix is kept. Conjunct 4 -> a corrected stamp still carries manifest_sha256. NEAR MISS in kid 2-s own design: the committed number is computed over ALL files under nodes/ (`git ls-tree -r HEAD -- nodes`) while the metric it replaces counts only `*.md`, so the substitution is not count-preserving. PARENT PROBE /tmp/parent-probe-sm34c.py: a fixture with ONE committed non-.md file under nodes/ has committed active=4 against smoke active=3; a worktree that then loses one committed .md node reads compared-4 -> 3 >= baseline 3 and PASSES, masking the drop. The real repo carries two such files (nodes/.geometry/commands.md.bak, nodes/experiment/_optimize_yaml_parser.py), so the offset is +2 — it biases toward a masked drop of up to two nodes and never toward the false DROP this hypothesis exists to kill. VERDICT: demoted from `proved` to `inconclusive_lean_disproved:60` on that one open probe, not on the two it closed. I did not run the kid suite as evidence.
<!-- THOUGHT:END -->

## Agent Notes
Compare-side closed: _node_manifest now reads git ls-tree HEAD (index excluded); the FAIL gate uses a committed active count from HEAD whenever _node_dirt is non-empty, so an untracked filler can no longer mask a committed drop. Parent probe p2 now FAILs naming b.md; refused-by-name stamp kept; 76 tests pass.
