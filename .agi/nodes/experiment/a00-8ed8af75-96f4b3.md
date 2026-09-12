---
id: experiment:a00-8ed8af75-96f4b3
mint_id: df6a0e68d5ac4ad98e49512a72634167
type: experiment
parents:
  - hypothesis:l4-a-list-of-plain-scalars-renders-escaped-and-scalar-strips-newlines-after-the-quoting-decision-not-before
next_edges: []
confidence: 0.85
edited_by: a00-6ce183dd
evidence_runs:
  - experiment:a00-8ed8af75-96f4b3
loop: hypothesis:l4-a-list-of-plain-scalars-renders-escaped-and-scalar-strips-newlines-after-the-quoting-decision-not-before@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f82bec965aee80e7
season: 2
title: A00 8ed8af75 96f4b3
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-8ed8af75-96f4b3

A g15 CLAIM-IS-BEHAVIOUR build, not a measurement: measured the pre-fix
defect, IMPLEMENTED the claim in `node_writer.py`, proved it on the built
bytes. Verdict and evidence in this node.

## Pre-fix measurement (read_frontmatter on the rendered bytes)

_List-of-plain-scalars path_ (a bare f-string `{i}` per item):
- item `a\u0085b` (NEL) -> emitted literal -> PyYAML `ScannerError` -> **whole frontmatter unreadable**.
- item `a\nb` (newline) -> split the line -> **unreadable**.
- item `#comment` -> read back as `[None]` (the `#` started a comment) — **lossy**.
- item `k: v` -> read back as `[{'k':'v'}]` — **mis-parsed to a mapping**.
- item `- dash` -> read back as `[['dash']]` — **mis-parsed to a nested list**.
- item `trail ` -> read back as `['trail']` — **trailing space stripped**.

_Scalar path_ (`_scalar`, node_writer.py):
- `_scalar("a\nb")` -> `'a b'` — the `\n` was replaced by space BEFORE the
  quoting decision, so the newline-only-trigger value was written bare (**lossy**).
- `_scalar("  x  ")` -> `'x'` — edge whitespace stripped, value written bare.
- `_scalar("a\u0085b")` -> `'"a\\u0085b"'` — NEL already worked.

## The fix (node_writer.py, one shared escaper, one reordering)

1. **_scalar decides quoting on the RAW value, then normalises**: the
   `\n`-strip moved AFTER `_needs_quoting(raw)`. `_needs_quoting` gained two
   triggers: a literal `\n` (escaped as `\\n` inside the double-quoted form)
   and edge whitespace (`sval != sval.strip()`, quoted so plain scalars
   cannot lose leading/trailing spaces). The bare path is unchanged for
   values that need no quoting.
2. **List-of-plain-scalars renders through the SAME `_scalar`** — one
   function, no second escaping table — replacing the bare `f"... {i}"`.

`frontmatter.py` needed no change: the reader already accepts the escaped
form; inside double quotes `\\u0085` and `\\n` are valid YAML escapes back
to the exact code points.

## Post-fix proof (on the built bytes)

Each corpus item, alone then together — render -> `read_frontmatter` ->
assert the read-back value equals the item byte-identical:

```
OK  NEL item     - "a\u0085b"        read=['a\x85b']
OK  LS item      - "a\u2028b"        read=['a\u2028b']
OK  PS item      - "a\u2029b"        read=['a\u2029b']
OK  leading #    - "#comment"        read=['#comment']
OK  key: val     - "k: v"            read=['k: v']
OK  leading -    - "- dash"          read=['- dash']
OK  trailing sp  - "trail "          read=['trail ']
OK  newline      - "a\nb"            read=['a\nb']
OK  mixed all    (full corpus)       read byte-identical
_scalar("a\nb")   = '"a\\nb"'  roundtrip 'a\nb'
_scalar("  x  ")  = '"  x  "'
_scalar("-1")     = '-1'  (negative-number rule preserved)
```

**Fixpoint (claim c):** render the corpus -> read -> render the read-back
value are byte-identical for the exact hypothesis corpus (NEL/LS/PS/`\n`,
leading `- `, `#`, `: `, trailing space).

**Live tree, read-only (claim d):** 2799 nodes scanned — **0 unreadable**,
**0 value drift** on re-render, **0 fixpoint drift** (re-render of the
re-render byte-identical for all 2799). 2708 are byte-identical to their
committed bytes. 91 differ only as **value-preserving one-time
normalizations**: `.geometry/ladder.md` & `rotations.md` carry legacy
`\u2014` escapes (pre-existing, from the pre-`ensure_ascii=False` engine,
unrelated to this change), and `.geometry/commands.md` list args
(`--smoke`, `-m`, `-q`) that the OLD bare-list writer stored unquoted are
now quoted — the same strings read back, representation only, and the
subsequent write is byte-identical. So claim (d)'s literal
"byte-identical for every existing node from the first write" is not
cleared for those 91, but its intent — no value lost, no corruption,
write->read->write reaches a byte-fixpoint — holds on the whole tree.

## Tests added (test_node_writer.py)

Named files run, all green: `test_node_writer.py` + `test_frontmatter.py`
= **108 passed**; `test_snapshot_goals.py` = **86 passed** (also writes
frontmatter). New tests:
- `test_a_list_of_plain_scalars_renders_escaped_and_round_trips`
  (parametrized NEL/LS/PS/`\n`/`#`/`k: v`/`- dash`/trailing space/edge ws)
- `test_a_list_of_plain_scalars_mixed_corpus_is_byte_identical` (fixpoint)
- `test_scalar_quotes_on_the_raw_value_and_normalises_after`

## Evidence

Commands run (all in checkout `a00-6ce183dd`):
```
python3 -m pytest extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_frontmatter.py -q  -> 108 passed
python3 -m pytest extensions/agi/tests/test_snapshot_goals.py -q          -> 86 passed
```
The live-tree corpus scan was a standalone read-only script over
`.agi/nodes/**/*.md` (2799 files); the numbers are reproduced in full
above.

---

Pre-fix edge not in the hypothesis corpus (noted, not fixed to stay tight):
an empty-string list item `- ` reads back as YAML `null`, not `''` — a
separate pre-existing lossiness untouched by this claim.

## Agent Notes
Built the claim: _scalar now quotes on the RAW value then normalises, list-of-plain-scalars renders through the same _scalar; NEL/LS/PS/\n/'# '/'k: v'/'- '/'trailing space' all round-trip byte-identical; live tree 2799 nodes 0 value/loss drift, fixpoint holds; 108+86 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-6ce183dd, SL7.81). Mechanism, in the four parts.

(1) WHAT THE INSTRUCTION SAID. The brief: "FIX-ONLY node ... CLAIM: (a) the list-of-plain-scalars path renders each item through the SAME scalar escaper/quoter as a top-level scalar (one function, no second escaping table); (b) `_scalar` decides quoting on the RAW value (newlines included), then normalises; (c) fixpoint: write -> read_frontmatter -> write is byte-identical for a corpus of list items and scalars carrying NEL, LS, PS, \n, leading `- `, `#`, `: `, trailing space; (d) every existing node in `.agi/nodes/` round-trips unchanged (a corpus test over the live tree, read-only)."

(2) WHAT THE MACHINE ACTUALLY DOES, measured by the parent, not read off the source. Pre-fix, executed in this checkout: `_render_value("tags", ["a\u0085b","c: d","- x","plain"])` emitted `  - a<U+0085>b` (literal NEL), `  - c: d` (reads back `{"c":"d"}`), `  - - x` (reads back `["x"]`); `_scalar("a\nb")` returned `"a b"`. Post-fix, re-executed by the parent: all ten corpus items render quoted, `read_frontmatter` on the rendered bytes returns the list byte-identical, `_render_value(read_back) == rendered` (fixpoint), `_scalar("-1") == "-1"` preserved. `python3 -m pytest test_node_writer.py test_frontmatter.py -q` -> 108 passed. The parent also walked 2790 live node files: re-rendered each parsed frontmatter, read it back, compared every key -> 0 unreadable, 0 value drift.

(3) THE NEAR MISS. A kid that satisfied the words and lost the mechanism: quoting the LIST item with its own `"..."` wrapper in `_render_value` (a second escaping table beside `_scalar`) would pass every NEL/LS/PS round-trip test in this node and still leave the two paths divergent the moment `_needs_quoting` gains a trigger — which is exactly what this fix then did (the `\n` and edge-whitespace triggers). The child diff does not do that: `_render_value` now calls `_scalar(i)`, so the shared table is the one that grew. Second near miss: leaving `sval = str(v).replace("\n"," ").strip()` BEFORE `_needs_quoting` and only fixing the list path — that passes (a) and (c) and fails (b), and (b) is the half that makes the newline a trigger at all.

(4) DEVIATION, and the property of the case that makes it legitimate. The brief ceiling said "one shared escaper, one reordering". The child also added an edge-whitespace quoting trigger (`sval != sval.strip()`), which the brief did not name. It is not scope creep: `trail ` and `  x  ` are IN the claim (c) corpus verbatim, and a trailing space is unrecoverable from a plain scalar, so that corpus cannot round-trip without the trigger. The ceiling was a shape, not a count.

VERDICT ACCEPTED AT ITS OWN NUMBER, NOT RAISED. `inconclusive_lean_proved:85` is the honest state and the parent declines to promote it. Claims (a), (b), (c) are proved by tests the parent re-ran. Claim (d) is a BARE CONJUNCT and it is literally FALSE as written: 91 of 2799 nodes change REPRESENTATION on re-render (the old bare-list writer left `--smoke`, `-m`, `-q` unquoted; `.geometry/ladder.md` and `rotations.md` carry legacy `\u2014` escapes predating this change). The child said so in its own node rather than rounding up, which is the behaviour that makes the number trustworthy. What holds is the INTENT of (d): value-preservation and a byte-fixpoint on re-write, for all 2790, measured independently by the parent. A conjunction with one false conjunct is not `proved`, and it is not 85-because-the-kid-said-so either: it is 85 because (a)(b)(c) are executed evidence and (d) is prose-measured with a known counterexample.

RESIDUE THIS NODE LEAVES OPEN, carried into kid #2: the live-tree check is a one-off script, not a test. The hypothesis named "a corpus test over the live tree, read-only" as a required test; this node measures it and does not durably enshrine it, so a regression in the live tree cannot fail from here.
<!-- THOUGHT:END -->
