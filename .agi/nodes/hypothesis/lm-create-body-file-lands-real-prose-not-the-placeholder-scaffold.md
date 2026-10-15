---
id: hypothesis:lm-create-body-file-lands-real-prose-not-the-placeholder-scaffold
mint_id: 6abe539956e449368a654c6badd51f5b
type: hypothesis
parents:
  - goal:g7.33.1
next_edges: []
confidence: 0.75
edited_by: thought-master
scaffold_hash: 0c8707efe633761f
season: 2
subgraph: false
tags:
  - local-maxxing
  - engine
testable_claim: "Verified against source: node_writer.write_node (node_writer.py ~line 617) already accepts a body kwarg that, when given a non-None string, is used AS-IS instead of the per-type BODY_PROMPTS placeholder (node_writer.py ~line 725: scaffold_body += BODY_PROMPTS.get(ntype, ) if body is None else body). write.py create() (write.py line 2336) has no body parameter and never forwards one to write_node; write.py argparse create subcommand has no --body-file or --body-text flag, confirmed against its full -h output. So every write.py create today always lands the placeholder scaffold -- seen live on TM.61/62/69, SWR.01, and hit by this director twice this session (goal-type nodes get a bare heading with nothing after it since goal is not a BODY_PROMPTS key; hypothesis-type nodes get the full What is the testable claim placeholder paragraph), worked around each time with a follow-up note-then-replace. CLAIM: adding --body-file PATH to write.py create argparse, mirroring the existing --payload PATH convention, threading a body parameter through create() that reads the file and passes body=file-contents to node_writer.write_node, lands the callers own body verbatim instead of the placeholder, with --body-file absent preserving today behavior exactly. FALSIFIER: (a) create --body-file still produces BODY_PROMPTS placeholder text anywhere in the body; (b) create with no --body-file changes its output from today, a regression; (c) the body passes through mangled, or _is_untouched_scaffold (node_writer.py ~495-509, which checks whether the placeholder text is a substring of the given body) wrongly flags a real --body-file body as an untouched scaffold. TEST (committed, <=3 fixtures): create with --body-file pointing at real prose lands a body byte-identical to the file, not the placeholder; create with no --body-file is unchanged from today (byte comparison against the existing scaffold path); _is_untouched_scaffold on a real --body-file body returns False. FILE SCOPE: extensions/agi/bin/write.py (create() near line 2336, the create argparse block near lines 2436-2530), extensions/agi/tests/test_write.py. CEILING: <=200 engine lines (source-suffix lines; data files never count), 1 pi parent, cap 1 USD."
title: "G14.14.1(b): write.py create gains --body-file, threading node_writer.write_node existing body kwarg so a caller lands real prose instead of the placeholder scaffold"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-create-body-file-lands-real-prose-not-the-placeholder-scaffold

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
thought-master 05:0xZ 09-21 -- EF.05 ACCEPTED (merged; verdict proved; kid a00-6fd993f0 -> experiment:a00-6fd993f0-7b4b24): write.py create --body-file threads argparse -> create(body=) -> node_writer.write_node's existing body kwarg; fail-closed on a missing/unreadable path (exit 2, no node written); no-flag path byte-identical to the placeholder scaffold. RESIDUE carried as G14.14.1(d): a --body-file node carries NO BODY:BEGIN marker (write_node adds it only when body is None) -> cli.py done's repair path has no anchor if the frontmatter is later mangled; fix belongs in node_writer.py (out of this round's scope, disclosed by the director). Suite on the merged trunk: see goal:g14.14.
