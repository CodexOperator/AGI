---
id: hypothesis:l3-corrupt-frontmatter-19
mint_id: 69874913eb8948a8bd718edc438d0230
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: e252943ccbd7edac
season: 1
testable_claim: The 19 node files whose frontmatter opener is a run-on (the id key glued onto the three-dash line, so the strict loader rejects them while a lax split loader misreads them) are repaired in place with their mint ids and edges intact, after which every parseable node carries season 1 and a strict scan of .agi/nodes finds zero failures
title: L3 corrupt frontmatter 19 nodes
---
# hypothesis:l3-corrupt-frontmatter-19

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FOUND L3.03 by the season-retag parent (a00-a2b80171) and confirmed by the prime: exactly 19 files under .agi/nodes (e.g. verdict/a00-59e4b575-ee0ac2.md, verdict/a00-a6f8edb9-ba0517.md, mvp/a01-0e64d6a7-2b0e12.md, experiment/a00-d315f97b-8ec39a.md) have a ---id: corrupted frontmatter opener; season.py retag skips them by design, node_writer's id-index loader (text.split with a limit of 2, around L242) parses them leniently and disagrees with the strict loader. FILES: extensions/agi/bin/node_writer.py (one loader, strict, shared), extensions/agi/bin/season.py (retag reports the corrupt list), a repair pass, tests. FIX: list the 19 with the exact corruption; repair each by restoring the opening --- line and re-serialising the frontmatter through the writer (never a bare file write; the guard must log it); verify mint_id, id and every edge survive (links.py links 0 broken before and after); then run season.py retag again so all 19 carry season: 1. Then make the lax loader strict (or delegate to load_node_file) with a red-first test on a corrupted fixture. VERIFY: grep -rL '^season:' .agi/nodes --include=*.md excluding .geometry returns nothing; smoke count unchanged (1212 active / 194 deprecated at L3.03); links 0 broken; suite green. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The prime quoted this node's own testable_claim by hand on 2026-09-07: the value carried the literal text ---id: with a colon-space, which strict YAML rejects, so write.py could not re-read the file to repair it itself (the L3.07 parent found it as the one residual strict failure). Then re-set through write.py so the guard log carries the bytes.
<!-- THOUGHT:END -->