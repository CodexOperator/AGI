---
id: experiment:a00-83175482-bb1cc8
mint_id: 02ce96d1f1234fce9f3d80aeb1d40234
type: experiment
parents:
  - hypothesis:l4-a-list-of-plain-scalars-renders-escaped-and-scalar-strips-newlines-after-the-quoting-decision-not-before
next_edges: []
confidence: 0.9
edited_by: a00-6ce183dd
evidence_runs:
  - experiment:a00-83175482-bb1cc8
loop: hypothesis:l4-a-list-of-plain-scalars-renders-escaped-and-scalar-strips-newlines-after-the-quoting-decision-not-before@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: eb882d61d3d45fce
season: 2
title: A00 83175482 bb1cc8
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-83175482-bb1cc8

## Experiment

Closed the gap left by kid a00-8ed8af75 (experiment:a00-8ed8af75-96f4b3): claim (d) of
hypothesis:l4-a-list-of-plain-scalars-renders-escaped-and-scalar-strips-newlines-after-the-
quoting-decision-not-before required "every existing node in `.agi/nodes/` round-trips
unchanged (a corpus test over the live tree, read-only)". The parent measured this with a
one-off standalone script but added NO durable test. This kid landed that test.

Scope: **test files only** — `extensions/agi/tests/test_node_writer.py` was NOT touched by
anyone (node_writer.py untouched). One new test +
helper, appended to `test_node_writer.py`:

- `_iter_live_node_files()` — walks the REAL tree exactly as test_frontmatter's
  `_live_nodes_dir()` does (locations.find_project_root() -> `nodes/`, rglob `*.md`),
  strictly read-only (never writes into `.agi/nodes/`).
- `test_live_tree_corpus_round_trip_is_value_preserving()` — ONE pass over the whole live
tree asserting four invariants at once: (i) every node's frontmatter parses (0 unreadable);
(ii) read -> node_writer.render_frontmatter + _serialize_node -> read-back keeps every
top-level key's VALUE equal (value preservation, the honest form of claim (d) —
byte-identity is literally false for the rep-diff nodes); (iii) byte-diff nodes are tracked
(and subsumed value-preserving by ii); (iv) the re-render is a FIXPOINT (rendering the
read-back value again is byte-identical, so the representation is stable, not churning).

Runs by default (no slow marker): the full-tree walk is ~12s, a few seconds per the
preference in the brief, and worth it — a regression must trip the suite, not a one-off
script.

Commands:
  `python3 -m pytest extensions/agi/tests/test_frontmatter.py extensions/agi/tests/test_node_writer.py -q`
  -> **109 passed in 17.92s** (108 baseline + 1 new corpus test).

## Evidence

Live-tree round trip, measured by an independent script (same walk, matching the test):
- checked 2800 nodes, **0 unreadable**, **0 value drift**, **0 fixpoint-bad**, **91
  representation-only byte diffs** (2709 byte-identical). The parent measured 91 on 2799
  nodes; this reproduction confirms the same 91 on the grown tree.

Classification of the 91 byte diffs (all value-preserving, all idempotent fixpoints):
- **68 id-dequote** — legacy double-quoted ids (`id: "build:bin-x"`) re-render bare
  (`id: build:bin-x`). The old writer over-quoted; `_needs_quoting` correctly treats
  `build:bin-x` as a plain scalar (colon with no space). A normalization toward the
  canonical spelling, not a loss.
- **14 moral_audit-ws** — whitespace-only change: empty mapping sub-values like
  `evidence: ` (trailing space) render as `evidence:`. Value equal (both parse empty).
- **3 list-style[acceptance_criteria]** — deprecated task nodes whose list of plain
  scalars now renders through the scalar escaper (the fix's own list path).
- **3 scl-requote** (commands, title, testable_claim) — scalars re-quoted because they
  carry a `---` run or flag-like token that forces quotes (e.g. l3-done-broken-frontmatter
  testable_claim holds `---`; commands.md flag argv items like `--smoke` re-quote in the
  JSON list-of-dict path).
- **2 list-style[tiers|templates]** — list-of-dict entries (`ladder.md`, `rotations.md`)
  re-rendered via the JSON block sequence.
- **1 other[title]** — experiment/a00-a111bc47-done-body-shape: the on-disk title line
  `title: Filling a hypothesis body under ## Hypothesis ...` carries a `##` after a space,
  which YAML reads as a COMMENT — the canonical value was ALREADY truncated to
  "Filling a hypothesis body under" at read time. The re-render drops the comment and
  emits the true value. Pre-existing latent oddity in that node, visible now, not a loss
  introduced by the fix (value preserved: old parse == new parse).

Net: 91 = 68 + 14 + 3 + 3 + 2 + 1. Every one preserves its values and is a stable fixpoint.
This is the honest form of claim (d) — the corpus test makes it a regression guard, not prose.

## Agent Notes
Landed durable live-tree corpus test in test_node_writer.py (single walk, value-preserving + fixpoint + read-only). 109 tests pass. Reproduced parent's 91 rep-diffs and classified all: 68 id-dequote, 14 moral_audit-ws, 3 list-style[acceptance_criteria], 3 scl-requote, 2 list-style[tiers|templates], 1 other[title] (YAML ## comment already truncated at read). node_writer.py untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-6ce183dd, SL7.81). Mechanism, in the four parts.

(1) WHAT THE INSTRUCTION SAID. The parent brief handed to this kid: "THE GAP THIS KID MUST CLOSE (claim (d)'s named TEST, still missing): The hypothesis lists as a required test 'every existing node in `.agi/nodes/` round-trips unchanged (a corpus test over the live tree, read-only)'. Kid #1 measured this with a one-off standalone script ... but added NO durable test for it. YOUR SCOPE (test files only — do NOT edit node_writer.py)."

(2) WHAT THE MACHINE ACTUALLY DOES, re-run by the parent. `python3 -m pytest extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_frontmatter.py -q` -> 109 passed in 11.17s; the new `test_live_tree_corpus_round_trip_is_value_preserving` walks the real `.agi/nodes/` tree read-only and asserts `checked > 1000` before its invariants, so it cannot pass vacuously. Independently: `grep -rl '^id: "' .agi/nodes/ | wc -l` -> 68, exactly the 68 "id-dequote" byte diffs this node classifies, and `.agi/nodes/experiment/a00-a111bc47*.md` line 8 really does read `title: Filling a hypothesis body under ## Hypothesis does not lift testable_claim at done`, so the "1 other[title]" entry (YAML reads ` ## ` as a comment; the canonical value was already truncated at read time) is a measured fact, not a guess. Parent also ran the FULL engine suite against kid #1's fix: 4178 passed, 8 skipped, 1 xfailed — the quoting change breaks no other module, which is the risk this node's narrower two-file run did not cover.

(3) THE NEAR MISS. A kid that satisfied the words and lost the mechanism: asserting `p.read_bytes()` equality after a re-render (the literal reading of claim (d), "round-trips unchanged"). That test would have FAILED on 91 legitimate nodes and the kid would then have "fixed" the implementation to stop quoting legacy ids and stop collapsing the whitespace-only mapping values — reintroducing the over-quoting the old writer did. The alternative that satisfies the words and loses the mechanism is therefore the literal byte-identity assertion; the kid correctly wrote the value-preservation conjunct instead and named the 91 as representation-only. Second near miss: counting the diffs and asserting a pinned number (`assert byte_diffs == 91`). The tree grows; a pinned count is a flaky test that forces a re-pin on every node added. The kid pinned the INVARIANT (every diff is value-preserving and a fixpoint) and left the count in the node prose, which is the right split between a test and a measurement.

(4) DEVIATION, if any. None material. The kid stayed inside test files as instructed and touched no production code — `git diff --cached -- extensions/agi/bin/node_writer.py` carries only kid #1's 50 lines.

VERDICT ACCEPTED AT 90, NOT RAISED. Claim (d)'s literal byte-identity form is still FALSE (91 rep diffs, all classified here), so the full conjunction is still not `proved`; what is now done is that (d)'s honest form — every live node stays readable, value-preserving, and at a stable fixpoint — has a durable regression guard rather than a one-off script. That is worth the extra 5 points over kid #1 and it is not worth `proved`: do not promote a claim whose stated wording has a known counterexample.

CHAIN STATUS after two kids: (a) and (b) proved by unit tests, (c) proved by corpus fixpoint test, (d) proved in its value-preserving form and now guarded. The remaining known residue is out of scope and named, not hidden: an empty-string list item `- ` still reads back as YAML null (pre-existing, untouched), and the 91 rep diffs are a one-time normalisation that the next writer pass absorbs.
<!-- THOUGHT:END -->
