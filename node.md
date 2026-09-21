---
id: outcome:a00-fd594bfd-ad6af8
mint_id: b3401f2447384962ad87384e246d2ef6
type: outcome
parents:
  - mvp:a00-8a013aaf-ca2434
confidence: 0.7
edited_by: season.py
evidence_runs:
  - mvp:a00-8a013aaf-ca2434
judged_against: goal:g13.1
lens: goal:g13
scaffold_hash: 811724cff7c00e30
season: 1
thought_session: season
title: A00 fd594bfd ad6af8
verdict: inconclusive_lean_proved:70
---
# outcome:a00-fd594bfd-ad6af8

## Outcome

A self-contained, dependency-free prototype of the unified node reader: a
single `parse_node` with three public surfaces (`parse_node(text)`,
`read_node(path, on_error)`, `load_directory(dir)`), one failure class
(`FrontmatterError`), and three `on_error` policies (`raise`, `skip`,
`skip_quiet`). It embodies the design `verdict:a00-52a8f13a-a156b6` proved for
the bulk corpus readers — of the ten parsers swept, nine collapse onto those
three policies; P10 (`benchmark`, line-based, no YAML) is the scoped-out
tenth. The prototype replaces no caller yet; the i/o contract below is what
an adopted `parse_node` should present.

Input shape (what enters): One `.md` file's raw text (`---\nYAML\n---\nbody`)
or a directory tree of `.md` files.

Output shape (what exits):
- `ParsedNode(frontmatter: dict, body: str, path: Path)` for well-formed files.
- `None` (skip/`skip_quiet`) or `FrontmatterError` (raise) for malformed files.
- `LoadReport(nodes, errors, duplicate_ids)` for bulk loads.

Behavior (what it does):
1. Splits a node file on `---` markers, strips leading space (P1 acceptance).
2. Parses the YAML block, wrapping `yaml.YAMLError` into `FrontmatterError` —
   one class, no escaped `ParserError`.
3. Rejects non-dict YAML (lists) in the parser as `FrontmatterError`.
4. Walks directories sorted (deterministic).
5. Resolves duplicate `id`s by sorted-first-wins with a visible `WARN` and a
   `duplicate_ids` audit trail.
6. Default `on_error="skip"` (report + continue), safe for write-adjacent
   callers (avoids `{}`+raw which corrupts on write-back).

Edge cases:
- Missing opening `---` → `FrontmatterError`.
- Missing closing `---` → `FrontmatterError`.
- Malformed YAML between valid markers → `FrontmatterError` (wraps parse error).
- Valid YAML that is a list → `FrontmatterError` (not `AttributeError`).
- Leading whitespace before `---` → accepted (first `.strip()` rule).
- Duplicate node ids in directory → sorted-first file wins, hidden file logged.
- File with no `id` in frontmatter → indexed by `<no-id>:<filename>`.
- Empty frontmatter (or any falsy YAML: `None`, `0`, `""`) → normalized to `{}` (`or {}`).

## Boundary (inherited from the mvp)

Prototype, not integration. It hard-codes the `.md`/`---` shape and the `id`
key for dupe detection, does not cover the `.json` shape `graph_core`
already accepts, and is not wired to any caller — adoption at the bulk
readers (P1/P5) is where the ten-parser divergence actually collapses.

## i/o doc

```
inputs:
  parse_node(text: str) -> ParsedNode | raises FrontmatterError
  read_node(path: Path, on_error="skip") -> ParsedNode | None | raises FrontmatterError
  load_directory(directory: Path, on_error="skip") -> LoadReport
    where on_error in {"raise", "skip", "skip_quiet"}
outputs:
  ParsedNode { frontmatter: dict, body: str, path: Path | None }
  LoadReport { nodes: dict[id -> ParsedNode], errors: list[(Path, str)],
               duplicate_ids: list[(id, str_kept, str_hidden)] }
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of a00-fd594bfd's first version (iteration 103). The kid's i/o
body was accurate — I re-ran the mvp code myself over the same six synthetic
shapes plus a dupe pair and a no-id file, and every documented line held:
one `FrontmatterError` class across M1–M4, M5 accepted, sorted-first-wins
with `WARN` + `duplicate_ids`, `<no-id>:` indexing, skip reporting. Three
things were wrong or missing and are fixed here:

1. `proved` @ 0.85 with no `evidence_runs`. An outcome documents a
   prototype; it does not itself certify anything beyond what the mvp's
   verified run already does, and the chain's earned ceiling is the parent
   verdict's lean (the universal ten-parser claim was falsified by P10 and
   two mechanism sub-claims were corrected there). Demoted to
   `inconclusive_lean_proved:70` with the mvp node cited as the evidence run.
2. "consolidates the ten divergent parsers from P1/P3/P5" — contradictory
   (ten… from three?) and against the parent verdict: P10 is exactly the
   parser that does not collapse, and the mvp replaces no caller. Rewritten
   as a prototype embodying a proved design, with P10 named as the scoped-
   out tenth.
3. "exactly two public surfaces" while the i/o doc listed three; and the
   mvp's own caveat (no caller wired, `.md`-only, `id` key hardcoded, no
   `.json`) was in the kid's report but not in the node — a boundary a
   reader of only the graph would miss. Added it as its own section.

The falsy-normalization line was also sharpened while there: `or {}`
normalizes every falsy YAML value, not just `None`.
<!-- THOUGHT:END -->



## Agent Notes
Outcome node describing the unified parse_node MVP produced by the g13 read-side chain. Captures input/output shapes, behavior across 3 on_error policies, 6 edge cases (missing markers, bad YAML, non-dict YAML, leading space, dupes, missing id).