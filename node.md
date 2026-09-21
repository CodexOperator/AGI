---
id: experiment:a00-9a208c13-dc42b3
mint_id: 0089a6a32c484383b21f0c83fcfc833c
type: experiment
parents:
  - hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file
next_edges: []
confidence: 0.7
edited_by: a00-b30a6d55
evidence_runs:
  - experiment:a00-9a208c13-dc42b3
loop: hypothesis:l4-the-never-lower-baseline-counts-committed-node-files-and-records-the-manifest-so-a-drop-names-the-file@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "fixture on season2/main with a bare origin; mint an UNTRACKED node; verification.compare_count(groot, CURRENT, stamp=True)", "expected": "refusal by name, no verify-count.json written", "observed": "no baseline; NOT STAMPED: explicit --stamp; refused by name — 1 uncommitted node path(s) here: nodes/hypothesis/untracked-mint.md", "result": "HOLD — SM.33 fix kept across all four kids"}
  - {"conjunct": 2, "class": "wire", "cmd": "fixture: commit a NON-.md file under nodes/; stamp; worktree deletes a committed .md node and commits the loss; mint an untracked filler; compare_count(wt/.agi, smoke)", "expected": "FAIL naming the lost node", "observed": "committed triple == smoke triple and the read FAILS naming nodes/hypothesis/b.md", "result": "defect — CLOSED by kid 3, still HOLD"}
  - {"conjunct": 3, "class": "gate", "cmd": "fixture: stamp on MAIN; worktree deletes committed b.md and commits the loss; mint an untracked filler; compare_count(wt/.agi, {active:3})", "expected": "FAIL naming nodes/hypothesis/b.md", "observed": "FAIL \"committed active=2 below baseline=3; (working tree reported active=3) missing committed file(s): nodes/hypothesis/b.md\"", "result": "defect — CLOSED by kid 2, still HOLD"}
  - {"conjunct": 3, "class": "wire", "cmd": "fixture: commit nodes/hypothesis/c.md with frontmatter status: \\\"deprecated\\\"; compare _committed_counts with metrics.node_lifecycle_stats", "expected": "the committed triple EQUALS the metric triple for every spelling the parser accepts", "observed": "both {active:3,deprecated:1,total:4} — kid 4 reads the HEAD blobs through frontmatter.read_frontmatter, so the quoted spelling no longer diverges; CRLF frontmatter also agrees", "result": "defect — CLOSED by kid 4"}
  - {"conjunct": 3, "class": "wire", "cmd": "fixture: node c.md with status: deprecated committed; verification._committed_deprecated(groot, [\\\"nodes/gone.md\\\"] + manifest)", "expected": "None — the function-s own git-cannot-answer contract", "observed": "0 — a `git cat-file --batch` MISSING header hits the loop-s `break` and returns a PARTIAL count; a LOW deprecated count makes committed active read HIGH and masks that many drops, silently. Reachable because _node_manifest and _committed_deprecated are two git calls and grid.py commit --all runs every 5 min in this shared tree", "result": "defect — OPEN, kid 5 dispatched to make it a one-line return None"}
  - {"conjunct": 4, "class": "gate", "cmd": "fixture: stamp, then hand-correct the state reason cell and count, then re-stamp from clean bytes", "expected": "the corrected stamp names the manifest it was corrected to", "observed": "manifest_sha256 present and equal across the re-stamp; reason cell preserved verbatim", "result": "HOLD"}
profile: balanced
role: kid
scaffold_hash: 08a303d863046afe
season: 2
title: A00 9a208c13 dc42b3
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-9a208c13-dc42b3

## Experiment

SM.34 kid 4, BUILD ORDER (last pass). Built the fix for the one open defect the
parent reproduced: `_committed_counts` read the deprecated cell with a LINE
ANCHOR (`git grep -l "^status: deprecated" HEAD -- nodes`) while the metric it
must agree with, `metrics.node_lifecycle_stats`, PARSES YAML FRONTMATTER. The
two disagree in BOTH directions.

PRE-FIX (reproduced on a fixture of committed nodes):

    nodes/hypothesis/q.md  frontmatter `status: "deprecated"`
    metric     {active: 4, deprecated: 1, total: 5}
    committed  {active: 5, deprecated: 0, total: 5}   <- active HIGH by 1, masks

WHAT LANDED — `extensions/agi/bin/verification.py`:

- new `_committed_deprecated(groot, manifest)`: reads HEAD's blobs with `git
  cat-file --batch` (ONE subprocess; a malformed header — `<path> missing` —
  ends the parse rather than desyncing it), feeds each blob through
  `frontmatter.read_frontmatter`, and counts `isinstance(st, str) and
  st.strip().lower() == "deprecated"` — the exact predicate `metrics.py` uses.
  A `b"deprecated" not in blob` pre-filter skips the yaml load for the ~95% of
  nodes that cannot hold the value.
- `_committed_counts` now calls it instead of `git grep`; kid 3's `.md`-only
  manifest is still the single population both cells are drawn from.

WALL TIME, measured on the REAL tree (`.agi/nodes`, 3096 committed `.md`):

    _node_manifest         0.01 s  (git ls-tree)
    _committed_deprecated  1.8 s   (was 6.1 s before the substring pre-filter;
                                    the cost is yaml.safe_load on 3096 files)
    committed triple       {active: 2897, deprecated: 199, total: 3096}

The same triple arrives from the metric over HEAD's EXTRACTED tree
(`git archive HEAD .agi/nodes` -> `{active: 2897, deprecated: 199, total:
3096}`): EQUAL. The live working tree reads 3099 because three other kids'
experiment nodes are staged in this shared checkout — expected, and the
`_node_dirt` guard is why that state can never be stamped.

FALSIFIERS, all four fail as required (fixture repo, bare origin, HEAD pushed):

1. quoted `status: "deprecated"` -> committed == metric `(4, 1, 5)`, and the
   drop it used to mask is caught: `FAIL ... committed active=3 below
   baseline=4; (working tree reported active=4) missing committed file(s):
   nodes/hypothesis/b.md`;
2. `status: deprecated` inside a BODY with an active frontmatter -> committed ==
   metric (`deprecated: 0`) and a clean tree stamps, then compares steady — no
   spurious FAIL;
3. kid 1's refusal by name; 4. kid 2's `.md`-only worktree read and kid 3's
   committed non-`.md` offset guard all stay green.

## Evidence

    python3 -m pytest extensions/agi/tests/test_verification_manifest.py \
      extensions/agi/tests/test_verification.py \
      extensions/agi/tests/test_verification_kept_merge.py \
      extensions/agi/tests/test_verification_window.py \
      extensions/agi/tests/test_verification_seat_model.py -q
    80 passed

Two tests added to `test_verification_manifest.py`:
`test_quoted_deprecated_spelling_agrees_with_the_metric` and
`test_a_body_line_is_not_a_deprecation_and_raises_no_spurious_fail`.

DEVIATION: the parent's ceiling was <= 35 changed production lines. This delta
is 18 removed / 43 added = **net +25 production lines** (61 changed lines as
`git diff -U0` counts them, because the two docstrings carrying the WHY are
lines). No new file, no new module-scope import, `metrics.py` untouched.
Recorded rather than silently exceeded.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid 4 CLOSED the deprecated-cell divergence and the bytes expose one more silent-mask path. WHAT THE ORDERS SAID: read the deprecated cell from the HEAD BLOBS with the SAME parser metrics.py uses instead of grepping a line anchor, and make the acceptance criterion a clean-checkout equality of the committed triple against metrics.node_lifecycle_stats for EVERY spelling the parser accepts. WHAT THE BYTES DO: new `_committed_deprecated(groot, manifest)` (verification.py ~:314-352) feeds `HEAD:./<path>` for every manifest entry to ONE `git cat-file --batch`, slices each blob by the announced size, skips blobs without the substring `deprecated`, and parses the rest with `frontmatter.read_frontmatter` + `str.strip().lower() == "deprecated"` — the same comparison metrics.py makes. MY PROBES ON THESE BYTES: /tmp/parent-probe-sm34d.py — a node whose frontmatter says `status: "deprecated"` now yields committed {active:3,deprecated:1,total:4} == the metric triple (kid 3 read {active:4,deprecated:0,total:4} and masked a drop); /tmp/parent-probe-sm34e.py probe 9 — CRLF frontmatter agrees; probes p1 (refusal by name), p2/p6 (the worktree read still FAILS and names nodes/hypothesis/b.md), p4 (staged file excluded from the .md-only manifest), p5 (manifest_sha256 beside a preserved reason cell) all still hold. NEAR MISS in kid 4-s own reader: the loop-s malformed-header arm is `break`, not `return None`, and `git cat-file --batch` answers a MISSING object with a 2-field `<path> missing` header — so the function RETURNS A PARTIAL COUNT rather than the None its own contract promises, and a low deprecated count makes committed active read HIGH and masks that many drops silently. PARENT PROBE 8 (/tmp/parent-probe-sm34e.py): `_committed_deprecated(groot, ["nodes/gone.md"] + manifest)` returned 0 against a full count of 1. REACHABLE, not theoretical: `_node_manifest` and `_committed_deprecated` are two separate git invocations and `grid.py commit --all` runs every 5 minutes in this shared tree, so a node deleted by a commit landing between them yields exactly that missing header. VERDICT: recorded as `inconclusive_lean_proved:70`, not proved, because a silent-mask path in the very number this node substituted is a defect in its bytes; kid 5 carries a one-line order to make the malformed-header arm return None.
<!-- THOUGHT:END -->

## Agent Notes
BUILT the parser fix: _committed_deprecated parses HEAD blobs through frontmatter.read_frontmatter (same strip().lower() predicate as metrics.py) instead of the ^status: deprecated line anchor; committed triple now EQUALS metrics.node_lifecycle_stats on a clean tree for quoted and body-literal spellings, on the real tree (2897/199/3096) and on the fixture. 1.8s on 3096 blobs. 80 tests pass, 2 new falsifiers.
