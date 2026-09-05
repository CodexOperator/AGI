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
Fourth version: the header now states the real rule, which the owner corrected -- replaced whole by default like HANDOFF.md, appended only on request, as in this instance where the next work continues directly off loop L1. Calling the file append-only made accumulation the default and would have grown the one document a cold reader opens for a verdict on the last loop, which is the mistake the handoff already paid for at 1,723 lines.
<!-- THOUGHT:END -->

## Agent Notes
The post-loop completion report. Shape and rules: goal:g1.13. Required contents and falsifier: mvp:complete-md-the-post-loop-completion-report. Mechanisation: goal:g14. next_edges point at the goal nodes this report was the occasion for -- goals cannot take a build parent (the [goal].md spawn gate allows a subgoal exactly one goal parent and nothing else), so the link runs as an edge from the report rather than as parentage on the goals.

CORRECTION 2026-09-05: the note above says goals cannot take a build parent, so the link ran as next_edges from this report. [goal].md was widened that day -- every variant may name a build parent, and a subgoal keeps its goal parent via min_parents_by_type {goal: 1}. The eight goals now carry parents: [<their goal>, build:COMPLETE.md] and the next_edges workaround is cleared, so the provenance reads in the direction the graph reads everything else: parents are where this came from.