---
id: goal:g14.5
mint_id: 6311a8358b364f54b01cc4302be5d75c
type: goal
parents:
  - goal:g14
next_edges: []
confidence: 0.6
edited_by: thought-master
goal_id: G14.5
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: b107818aa40fe941
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - side-track
  - bend2
  - hvm
title: "Map the Bend2 / HVM source tree into the graph at the source level: one hypothesis per code file (\"I think this file does X\"), experiment until the hypothesis is right, link it to the build node that IS the file -- a long-term, slow-moving effort chased independently by a dedicated director (the first test of a goal-attached director), NOT stood up yet (owner: preserve resources); the proper mapping waits on the IOMap system"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.5

## Agent Notes
OWNER 2026-09-18 17:4xZ (thought-master pane), verbatim: "We need to map bend2 into the graph properly, but that needs IOMap system from SM so dont worry about that or telling her. Just letting you know thats a part of the solution. But some way to at least explain what each code file in bend2 does in and of itself at the source level. Thatll take a while, can be a long-term slow moving ongoing effort. The hypothesis could be I think this file does this and experiment until you have the right hypothesis and it links up to the existing build mode that is the code file. This can be a second director job you spawn, a test run of having a director attached to a specific goal that they keep chasing independently. You can communicate this to sanctuary master but dont stand up the post yet we need to preserve resources." APPLY (thought-master): (1) this goal holds the field; (2) SHAPE of the work: the Bend2 + HVM source (HigherOrderCO, the compiler, the C and CUDA runtimes) enters the tree under .agi/context/local-maxxing/bend2-src/ (a pinned shallow checkout, commit recorded) so level3 mints a build node per file -- the build node IS the file; per file one hypothesis "this file does X" with a falsifier (a probe: a call, a test, a trace) and one experiment; a verdict links hypothesis -> build node; a per-directory doc summarizes what proved; (3) ORDER: start where the why-idea points (the HVM CUDA runtime + the Bend to HVM lowering), not alphabetically; (4) the dedicated director (second town director, goal-attached, chases this alone at a gentle cadence, 1 USD/round) is NOT seated until the owner lifts the resource hold; until then the why-idea experiment (kernel-launch count) is the only Bend work and runs under director-thought; (5) the proper cross-file mapping (calls, imports, contracts) waits on the IOMap system -- not a thing to ask for. Communicated to the sanctuary-master 17:5xZ as a status line (a post to plan, not to stand up).

thought-master 22:3xZ 09-20 (cleanliness pass, owner 22:1xZ): required goal fields were missing (status, origin, seeds, tags, confidence) so this subgoal never rendered into GOALS.md -- set now, no other change; it is the source-mapping sibling of the G14.12 spiking side track.
