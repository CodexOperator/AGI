---
id: outcome:a00-5510b3ee-67fb62
mint_id: 5d4a730773974adaa7b67b54c647aa82
type: outcome
parents:
  - mvp:a00-8a013aaf-ca2434
confidence: 0.7
edited_by: season.py
judged_against: goal:g13.1
lens: goal:g13
scaffold_hash: 4d1ad36c24dd8644
season: 1
thought_session: season
title: A00 5510b3ee 67fb62
verdict: inconclusive_lean_proved:70
---
# outcome:a00-5510b3ee-67fb62

## Outcome

Adoption path for the unified `parse_node` MVP — the exact delta between each
major caller's current reader and the unified design. Verified by running P1's
real `_parse_md` side by side with the MVP's `parse_node` over all six
synthetic shapes from `experiment:a00-00cde6d0-57851d` (W well-formed, M1
one-marker, M2 no-marker, M3 bad-YAML, M4 YAML-list, M5 leading-space).

**P1 (`_parse_md` in `graph_core.persistence.frontmatter`):**
- Adoption delta = **1 wrap**: `yaml.safe_load` → `try/except yaml.YAMLError` → `raise FrontmatterError`.
- P1 already has: `isinstance(fm, dict)` non-dict check (M4 caught), `.strip()` acceptance (M5 accepted), three-policy surface (`raise` in `_parse_md`, error isolation in `load_node_dir`).
- Verified: 5/6 shapes MATCH between P1 and MVP; M3 is the only diff (bare `ParserError` vs `FrontmatterError`). With the wrap added, all 6 match.

**P5 (`load_existing_nodes` in `snapshot-goals.py`):**
- Adoption delta = **5 changes**: replace `split("---",2)` with line-by-line marker scan; wrap `yaml.safe_load`; add `isinstance(fm, dict)` check; change last-wins→first-wins + WARN + `duplicate_ids` trail; remove bare `except Exception: pass`.
- Currently silent on all errors (swallowed by bare `except Exception`). P5 has no `dup` detection, no non-dict guard, no YAML wrap.

**P3 (`_read_frontmatter` in `post_wire.py`):**
- Adoption delta = **4 changes**: replace `"---\n" in text` heuristic with line-by-line scan; wrap `yaml.safe_load`; add non-dict check; change `{}`+raw → `skip`-with-report (avoids write-back corruption verdict discovered).

Input shape (what enters): P1's real `_parse_md(path, suffix=".md", want_body=True)`
and the MVP's `parse_node(text)` applied to six synthetic `.md` shapes.

Output shape (what exits): A delta table showing which shapes match and which
differ between P1 and MVP, and the exact code changes that close each gap.

Behavior (what it does):
1. Runs P1's `_parse_md` and MVP `parse_node` over each synthetic shape.
2. Compares result/error class for each.
3. Documents which adoption deltas are needed per caller (P1, P3, P5).
4. Confirms P1 already matches the MVP except the YAML wrap — the adoption
   is a 2-line change for P1, a rewrite for P5 and P3.

Edge cases:
- P1 already handles all six shapes correctly for the `raise` policy; the only
  gap is bare `ParserError` on M3 escaping `except FrontmatterError`.
- P1's `load_node_dir` already has error isolation (`try/except FrontmatterError`,
  `try/except Exception`) — the adoptable read path is two lines shorter than
  the MVP's equivalent surface.
- The `.json` shape is not tested here; P1 supports it, the MVP does not yet.

## i/o doc

```
inputs:
  python3 /tmp/g13-adoption-delta.py   # side-by-side P1 vs MVP over 6 shapes
    Six synthetic .md shapes (W, M1-M5) from the experiment corpus.
outputs:
  Delta per shape: MATCH (same result/error class) or MISMATCH.
  Adoption delta per caller:
    P1: 1 wrap (yaml.YAMLError → FrontmatterError)
    P5: 5 changes (marker scan, yaml wrap, isinstance check, dupe rule, rm bare except)
    P3: 4 changes (marker scan, yaml wrap, isinstance check, {}+raw→skip)
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Second outcome under the same MVP, documenting the adoption path rather than
the prototype itself. The sibling outcome (a00-fd594bfd-ad6af8) describes the
MVP's internal behavior; this one describes what changes when you wire it into
each caller. Verified experimentally by running P1's real code against the
MVP's code over the same corpus the experiment used — the adoption delta for
P1 is exactly one try/except wrap, a much smaller gap than the MVP's boundary
section suggested. P5 and P3 need deeper rewrites.
<!-- THOUGHT:END -->

## Agent Notes
Adoption-path outcome: verified P1 _parse_md vs MVP parse_node over 6 synthetic shapes — delta = exactly 1 try/except yaml.YAMLError wrap (5/6 shapes already MATCH). Documented P5 (5 changes) and P3 (4 changes) adoption paths from code analysis.