---
id: build:COMPLETE.md
mint_id: 7a43cca5e67b4bcdbf580fc695f4f720
type: build
parents:
  - mvp:complete-md-the-post-loop-completion-report
  - goal:g1.13
next_edges: []
build_kind: prose
confidence: 1.0
edited_by: director
origin: build-scan
payload_ref: COMPLETE.md
scaffold_hash: d8b43e6e0045d164
tags:
  - build
  - prose
thought_session: L1.13
title: "Build: COMPLETE.md"
---
# build:COMPLETE.md

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fifth version: section 5b added to the L1.13 report, because the credential trail and what it implies are findings rather than failures and the six-section shape had nowhere to put a finding that is neither. The report now says what the uninvited runtime actually was, that it arrived through the AGENTS.md symlink, and that the graph turned out to be sufficient on its own -- which is the observation the owner drew out and which idea:the-graph-is-the-workflow carries in full.
<!-- THOUGHT:END -->

## Agent Notes
The post-loop completion report. Shape and rules: goal:g1.13. Required contents and falsifier: mvp:complete-md-the-post-loop-completion-report. Mechanisation: goal:g14. next_edges point at the goal nodes this report was the occasion for -- goals cannot take a build parent (the [goal].md spawn gate allows a subgoal exactly one goal parent and nothing else), so the link runs as an edge from the report rather than as parentage on the goals.

CORRECTION 2026-09-05: the note above says goals cannot take a build parent, so the link ran as next_edges from this report. [goal].md was widened that day -- every variant may name a build parent, and a subgoal keeps its goal parent via min_parents_by_type {goal: 1}. The eight goals now carry parents: [<their goal>, build:COMPLETE.md] and the next_edges workaround is cleared, so the provenance reads in the direction the graph reads everything else: parents are where this came from.