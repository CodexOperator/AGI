---
id: experiment:a00-e123028f-3825f1
mint_id: e404f57b1823451cbe2e555b74b06ed1
type: experiment
parents:
  - hypothesis:a01-721930d9-d34989
next_edges: []
confidence: 0.75
scaffold_hash: 588fe3f1d3c30641
title: A00 e123028f 3825f1
verdict: inconclusive_lean_proved:75
---
# experiment:a00-e123028f-3825f1

## Experiment

Tested conditions 1 and 2 of the read/write join hypothesis (`hypothesis:a01-721930d9-d34989`) on the 112-goal-node corpus at `.agi/nodes/goal/`.

**Script:** `/tmp/g13-join-experiment-2.py`

### C1 — Read-side agreement

Compared `graph_core.persistence.frontmatter.load_node_file` (canonical reader) against snapshot-goals' ad-hoc read path (`text.split("---").yaml.safe_load`) on 112 goal nodes. Both frontmatter and body compared.

**Result:**
- Frontmatter: 112/112 identical ✅
- Body: 111/112 identical. One node (`g4.3`) has a body starting with `\n> **⚠ SUPERSEDED...` — canonical reader preserves leading blank because `>` is body content, not a blank separator; SG reader strips all leading blank lines.

### C2 — Write-side equivalence (write_frontmatter vs update_node)

For each goal node: copied to two temp dirs. Dir A: wrote through replica of snapshot-goals' `write_frontmatter` with `preserve=` keys merge. Dir B: wrote through `node_writer.update_node` with `set_fm=` containing same derived keys (`goal_id`, `goal_kind`, `heading_level`, `origin`). Re-read both through canonical reader; compared parsed frontmatter and body (trailing newlines normalized — 2 nodes had trailing `\n` from originals that write_frontmatter drops, a non-semantic artifact of the canonical reader's `splitlines` join).

**Result:**
- Parsed fm + normalized body: 112/112 equivalent ✅
- THOUGHT preserved: all 40 nodes with THOUGHT blocks ✅
- `update_node`: 1 updated, 111 unchanged (existing keys already matched)

### Key insight

The hypothesis claims "the write path must first grow a preserve-keys mechanism it does not yet have." This experiment shows `update_node` already provides preserve semantics: it starts from the existing frontmatter and merges `set_fm` into it. `write_frontmatter` needs explicit `preserve=` because it *reconstructs* the file from scratch; `update_node` applies a delta. No new mechanism needed — the required semantics are inherent.

## Evidence

```
=== Condition 1: Canonical reader vs snapshot-goals reader ===
  Corpus: 112 goal nodes

  [OK] C1: frontmatter agreement: 112/112 nodes identical frontmatter
  [FAIL] C1: body agreement: 111/112 nodes identical body

  Body discord (1):
    g4.3-finish-the-runtime-split-pi-and.md: canonical starts '\n> **⚠ SUPERSEDED...'
             SG starts      '> **⚠ SUPERSEDED...'

=== Condition 2: write_frontmatter vs update_node ===
  Compare parsed frontmatter+body (normalized)

  [OK] C2: write-path equivalence: 112/112 nodes produce equivalent
          parsed output via both paths
  [OK] C2: THOUGHT preserved: all 40 nodes with THOUGHT blocks

  update_node: 1 updated, 111 unchanged

=== SUMMARY ===
Tests: 4 | 3 passed | 1 failed
  [OK] C1 frontmatter agreement: 112/112
  [FAIL] C1 body agreement: 111/112
  [OK] C2 write-path equivalence: 112/112
  [OK] C2 THOUGHT preserved: 40/40
```

### Discrepant node details

**C1 body discord (1 of 112):** `g4.3` body opens with blockquote `>` preceded by `\n`. Canonical reader's `_parse_md` strips only ONE leading blank line (`if body_lines and body_lines[0] == "": body_lines = body_lines[1:]`), so `\n>` survives as `\n>` — this is correct behavior (the `\n` is part of the body content, not a blank separator). SG reader strips ALL leading blank lines via `while body_lines and body_lines[0] == "": body_lines = body_lines[1:]`, consuming the `\n` before `>`. Two different conventions for body boundary stripping. The canonical reader's single-blank strip matches the common node file convention.

**C2 trailing newlines (2 of 112):** `g6.8` and `s11` have original files ending with `\n\n` after the body. write_frontmatter writes the body without a trailing `\n`; update_node (UNCHANGED) preserves the original. When re-read, the canonical reader's `splitlines`/`join` chain preserves trailing blank lines from `splitlines` as trailing `\n`. After normalizing trailing `\n` both are equivalent.


## Agent Notes
Tested C1 (read-side agreement) and C2 (write-side equivalence) of the join hypothesis on 112 goal nodes. C1: frontmatter 112/112 identical, body 111/112 (1 body-boundary edge case in g4.3). C2: write_frontmatter vs update_node produce equivalent parsed frontmatter+body for 112/112 nodes after trailing newline normalization. Key finding: update_node already provides preserve semantics via set_fm merge — no new preserve= mechanism needed, contradicting the hypothesis's stated precondition. THOUGHT preserved for all 40 nodes with thoughts.
