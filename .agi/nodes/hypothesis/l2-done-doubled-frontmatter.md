---
id: hypothesis:l2-done-doubled-frontmatter
mint_id: d3ee741e7f2f44a8b697ade1d8195244
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director
scaffold_hash: 6268cbf53652f2ce
testable_claim: cli.py done writes the verdict into a kid's node without leaving a second frontmatter block in the body, and a kid brief that ends without the DONE contract line is detected and named in the manifest
thought_session: agi-master-2026-09-06
title: "L2 g15: l2-done-doubled-frontmatter"
---
# hypothesis:l2-done-doubled-frontmatter

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Observed L2.01: experiment:a00-e65beccc-ac5309 arrived with a duplicate scaffold frontmatter block left in the body after cli.py done wrote the verdict into the first block (the parent merged them by hand, see .agi/sessions/iter-L2.01/a00-a9fddc13/output.log); and kid a00-fc43bb62 never emitted the DONE line at all (parent a00-0338943a noted it as a process defect). Reproduce the doubling first with a scaffolded node plus a kid-style rewrite that keeps the scaffold's frontmatter in the body, then fix in the one writer both paths share (cli.py done routes through post_wire.py or node_writer.py; find it, fix it once): a body that begins with a second --- frontmatter block is merged into the real frontmatter, later keys winning, and the duplicate is removed; log one line saying it happened. For the missing DONE line: post_wire.py or the reaper marks the manifest entry done_line: missing when the kid's output.log has no line starting with DONE, so a parent can see it without reading the log; do not fail the kid for it. FILES: the shared writer module, extensions/agi/bin/cli.py or post_wire.py as needed, tests. VERIFY: red-first tests for both, suite green. REPORT: one experiment node under this hypothesis with a verdict on the testable claim, evidence_runs as a list of node ids, every verify command with its actual output in the body. Engine files are edited in place; suite via python3 extensions/agi/bin/commands.py run tests, green before you report; each new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them.

ADDENDUM 2026-09-06 after L2.04: write_guard.py check now warns on every kid experiment node after a round, because a kid writes its node file with its editor (the sanctioned kid contract) and a parent's review edit is often a hand edit too. Make the sanctioned paths log: cli.py done must route the final node bytes through the logged writer (node_writer.write_node or the same log call) so a kid node that reached done is clean; and the parent brief (brief.py _parent) must say review edits go through write.py thought or note, never an editor, so a parent hand edit is the only thing left that warns. Verify on a fake kid node: after done the guard is silent; after a hand edit it warns.
