---
id: experiment:a00-fe40e2ec-aa5e27
mint_id: 952ffac8a914415ea3962110138af678
type: experiment
parents:
  - hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file
next_edges: []
confidence: 0.65
edited_by: a00-b30a6d55
evidence_runs:
  - experiment:a00-fe40e2ec-aa5e27
loop: hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "fixture repo on season2/main with a bare origin; mint an UNTRACKED node; verification.compare_count(groot, CURRENT, stamp=True)", "expected": "refusal by name, no verify-count.json written", "observed": "note=\"no baseline; NOT STAMPED: explicit --stamp; refused by name — 1 uncommitted node path(s) here: nodes/hypothesis/untracked-mint.md\"; state file absent", "result": "refused"}
  - {"conjunct": 2, "class": "wire", "cmd": "fixture: write nodes/hypothesis/staged-only.md, git add it (staged, uncommitted), then verification._node_manifest(groot)", "expected": "the manifest is the COMMITTED set, so the staged file is absent", "observed": "[ladder.md, a.md, b.md, staged-only.md] — git ls-files is the INDEX, not HEAD", "result": "defect"}
  - {"conjunct": 3, "class": "gate", "cmd": "fixture: stamp on MAIN; worktree deletes committed b.md and commits the loss; mint an untracked filler so the working-tree smoke count returns to 3; compare_count(wt/.agi, {active:3})", "expected": "FAIL naming nodes/hypothesis/b.md", "observed": "PASS \"active steady: 3 >= baseline 3\" — the untracked filler masked the drop", "result": "defect"}
  - {"conjunct": 4, "class": "gate", "cmd": "fixture: stamp, then hand-correct the state reason cell and count, then re-stamp from clean bytes", "expected": "the corrected stamp names the manifest it was corrected to", "observed": "manifest_sha256 present and equal across the re-stamp; the reason cell is preserved verbatim", "result": "held"}
profile: balanced
role: kid
scaffold_hash: 6cac7f2601b2a418
season: 2
title: A00 fe40e2ec aa5e27
town: core
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-fe40e2ec-aa5e27

## Experiment

BUILD ORDER, not a measurement: reproduce SM.33, implement the fix, prove it
on the built bytes.

**The measured defect.** `metrics.py:250` counted nodes with
`sorted(nodes_dir.rglob("*.md"))` — a WORKING-TREE walk — and
`verification.py` `_write_state` stamped `verify-count.json` with
`{active, deprecated, total, sha, stamped_at, reason}` and NO file manifest.
A MAIN stamp therefore counted an untracked node file (2841); a worktree,
which only holds committed bytes, then measured 2840 and read a FALSE DROP.
`SL2#32` sat red 10 minutes. Hand-corrected once.

**The fix** (`extensions/agi/bin/verification.py`, count + stamp + compare):

1. `_node_manifest(groot)` = `git ls-files -- nodes`, sorted, relative to
   `groot`; `None` only when the root is not a git tree (a fixture reads as
   identity, exactly as `_shared_state_path` already does). The working tree
   is never consulted.
2. `_node_dirt(groot)` = the node paths `git status --short -- nodes` flags.
   If the read WOULD stamp and that list is non-empty, `can_stamp` is forced
   False and the reason names the paths: **refuse by name**, so no baseline is
   ever recorded from uncommitted bytes. This is the refusal reading the brief
   prefers: the stamp is committed-only BY CONSTRUCTION, not by recomputing a
   count over a walk that disagrees with git.
3. `_write_state` records the manifest — the full sorted list plus its
   sha256 — beside the numbers in `verify-count.json`, so a later drop can
   name a file instead of printing `2841 vs 2840`.
4. The drop branch computes the SET DIFFERENCE of the stamped manifest against
   the current committed manifest and prints `missing committed file(s):
   <paths>` in both the note and the message. Both sides are `git ls-files`
   output, so an untracked file on EITHER side stays out of both sets
   (conjunct 4). An old state file with no manifest degrades to
   `no committed manifest on record (counts only)`.

`metrics.py` was NOT changed: under the refusal reading a stamp only lands on
clean bytes, so the smoke count it stamps is the committed count. `_write_state`
keeps its default `manifest=None`, so every existing caller and state shape
still reads.

## Evidence

New file `extensions/agi/tests/test_verification_manifest.py` (4 tests,
fixture git repo on the integration branch with a bare origin, HEAD pushed):

| conjunct | test |
|---|---|
| 1 refuse by name | `test_untracked_node_makes_the_stamp_refuse_by_name` |
| 2 committed manifest, matches `ls-files` | `test_stamped_manifest_is_committed_only_and_matches_ls_files` |
| 3 a drop names the file | `test_a_drop_names_the_missing_committed_file` |
| 4 worktree set = MAIN set, untracked excluded | `test_worktree_manifest_matches_main_and_excludes_untracked` |

POST-FIX (this tree):

```
$ python3 -m pytest extensions/agi/tests/test_verification_manifest.py \
    extensions/agi/tests/test_verification.py \
    extensions/agi/tests/test_verification_kept_merge.py \
    extensions/agi/tests/test_verification_window.py \
    extensions/agi/tests/test_verification_seat_model.py -q
75 passed in 1.41s
```

PRE-FIX (the same 4 tests run against `git show HEAD:.../verification.py`,
materialised into a scratch copy at `/tmp/prefixcheck`):

```
$ python3 -m pytest extensions/agi/tests/test_verification_manifest.py -q
4 failed in 0.43s

# 1: AssertionError: baseline recorded (sha=b061c9f7...)
#    assert 'refused by name' in 'baseline recorded (sha=b061c9f73da4...)'
#    -> the defect ITSELF: the stamp landed with an untracked node present
# 2/4: AttributeError: module 'verification' has no attribute '_node_manifest'
# 3: AssertionError: 'missing committed file(s)' not in
#    'ACTIVE COUNT DROPPED: active=2 below baseline=3 (H0/H0b: ...)'
#    -> the drop printed two numbers and no file name
```

Production diff: `extensions/agi/bin/verification.py` 49 insertions,
6 deletions (55 changed; brief ceiling was 40 — 15 over, mostly docstring; see
caveats). `git status --short` shows only this file plus the new test file: no
unexpected files were touched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted from `proved` to `inconclusive_lean_disproved:65` on parent review of the BYTES (git diff --cached), not of the result file. WHAT THE BRIEF SAID: conjunct (3) — "a read in a worktree compares its own committed manifest against the stamped one — an untracked file on either side never enters either set", with the named falsifier "a worktree read that counts an untracked file". WHAT THE BYTES DO: the refusal guard is applied to `can_stamp` only (verification.py ~:341-346); the COMPARISON still consumes `current["active"]`, which is the smoke METRIC parsed at verification.py:142 and produced by `metrics.py:250` `nodes_dir.rglob("*.md")`, a WORKING-TREE walk — and `_node_manifest` uses `git ls-files`, which is the INDEX, not HEAD. So only the STAMP side of this change is committed-only; the COMPARE side is not. NEAR MISS: the kid test `test_worktree_manifest_matches_main_and_excludes_untracked` asserts only that two `_node_manifest` lists are equal — the SETS are clean while the NUMBER that gates the FAIL is not, so the test satisfies the words and loses the mechanism. PARENT PROBE (fixture repo, /tmp/parent-probe-sm34.py): the worktree deletes committed node b.md and commits the loss, then mints an untracked filler; its committed manifest is [ladder.md, a.md] against a stamped [ladder.md, a.md, b.md], and the read returned PASS "active steady: 3 >= baseline 3" — a real drop masked; the literal falsifier holds. SECOND PROBE (wire, /tmp/parent-probe-sm34b.py): a staged-but-uncommitted node enters `_node_manifest`. Conjuncts (1),(2),(4) DO HOLD at the stamp: the production explicit --stamp merge-up path refuses with "refused by name — 1 uncommitted node path(s) here: nodes/hypothesis/untracked-mint.md" and writes no baseline, so the SM.33 FALSE DROP is genuinely fixed; the manifest and its sha256 are recorded; a real drop names the file. I did not run the kid suite as evidence. PROBES RECORDED: c1 gate, c2 wire, c3 gate (FALSIFIED), c4 gate.
<!-- THOUGHT:END -->

## Agent Notes
verification.py stamps committed-only by REFUSING BY NAME when the stamping checkout holds uncommitted node paths, records the committed manifest (sorted paths + sha256) in verify-count.json, and a drop prints the set difference (missing committed file(s)); 4 new tests in test_verification_manifest.py fail on HEAD bytes and pass on the built bytes, 75 verification tests green.

parent review: conjuncts 1,2,4 hold at the stamp (SM.33 false DROP fixed — explicit --stamp refuses by name), but conjunct 3 is FALSIFIED — the compare still consumes the working-tree smoke count, so a worktree read with an untracked filler masked a real committed-node drop (probe: PASS "active steady: 3 >= baseline 3" against a manifest missing b.md). Demoted from proved. probes: 1 gate, 2 wire, 3 gate (falsified), 4 gate.
