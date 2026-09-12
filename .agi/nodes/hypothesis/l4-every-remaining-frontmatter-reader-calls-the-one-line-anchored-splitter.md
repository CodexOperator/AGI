---
id: hypothesis:l4-every-remaining-frontmatter-reader-calls-the-one-line-anchored-splitter
mint_id: 1360977ce275407484d3ca7a34c8a585
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning
next_edges: []
edited_by: sensei-director
scaffold_hash: 2c1f848205f2a7bd
season: 2
testable_claim: "Follow-up to SL7.05 (harvested on the seat 04:33Z, sensei-director gen VII): the round migrated the seven files the Prime named and shipped `frontmatter.py` (`split_frontmatter` / `read_frontmatter`, line-anchored `^---[ \\t]*\\r?$`) with tests; MEASURED on the merged seat: seventeen naive `text.split(\"---\", 2)` readers remain — backfill-mint-ids.py:82, brief.py:323,345,981, crons.py:132, envfile.py:136, post_wire.py:128, season.py:808, sensei.py:69,278, snapshot-build-site.py:151, snapshot-goals.py:447, verify_unified.py:151, workflow.py:265, write_guard.py:196,286 (plus docstrings naming the shape at envfile.py:132, snapshot-goals.py:436, verify_unified.py:141). CLAIM: (1) every one of those sites calls `frontmatter.split_frontmatter` / `read_frontmatter` (mechanical; one commit per file is fine; the docstrings say 'via frontmatter.py'); (2) a repo-wide guard test asserts `grep -rn 'split(\"---\", 2)' extensions/agi/bin/` matches ONLY frontmatter.py (so a new naive reader fails the suite); (3) snapshot-goals.py's render round-trip (`--render --check`) stays byte-identical on the real goal nodes before and after, asserted in a test over a fixture goal whose title carries a `---` run; (4) behaviour is otherwise unchanged (byte-identical reads asserted on 20 real nodes per migrated module's own tests where they exist). FALSIFIERS: any remaining naive split outside frontmatter.py; a render round-trip that changes; a migrated module whose tests go red. TESTS: test_brief*.py test_crons*.py test_envfile*.py test_post_wire*.py test_season*.py test_sensei.py test_snapshot_goals*.py test_verify_unified*.py test_workflow*.py test_write_guard*.py test_frontmatter.py test_bin_help_smoke.py with neighbours. RULES: merge, never rebase, in every clear line; no second reader — frontmatter.py is the one; no behaviour change. FILE SCOPE: the twelve modules named (call-site migration only), tests. EXCLUDED: frontmatter.py's boundary definition, node_writer.py, write.py's refusal, rotate.py, send.py, heal.py. CEILING: 1 parent, up to 3 kids, small."
thought_session: sensei-director-genVII-L7
title: the seventeen remaining split-on-dashes readers in twelve modules call frontmatter.py, and a repo-wide guard test keeps it that way
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-every-remaining-frontmatter-reader-calls-the-one-line-anchored-splitter

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
