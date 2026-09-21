---
id: goal:g2.8
mint_id: 28dcc9c1236e491e983b34b9dba07506
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.8
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G2.8: LOD is a second axis: detail dials independently of position"
---
**Zoom says where you are; LOD says how much is drawn there.** They are
orthogonal, and every zoom position carries its own detail range. Standing far
out, low LOD is a supernode's name and high LOD is its members' titles and
counts. Standing on a build node, low LOD is a one-line summary and high LOD is
the raw file — and past that, **G2.9**.

**Summaries are stored, not generated on demand.** Each node carries *several*
summary-level bodies baked in, one per LOD step, so dialling detail is a read
rather than a model call. That is the whole reason this is worth building: a
summary computed live costs motion on every view and varies between views; a
summary written once is stable, citable and free to render. For code build
nodes the summary can live in the file's own comments, so the payload and its
summaries travel together and `stitch` keeps carrying exactly one artifact.

What has to be true:
- A node declares its LOD bodies explicitly; a missing level renders as the
  next-coarser one rather than as nothing.
- Summaries are **written**, never fabricated at render time — the same rule
  G2.2 already applies to `why`/`perf`/`security`, for the same reason.
- The renderer picks an LOD; the graph does not decide for it.

Open: whether LOD bodies are frontmatter fields, body sections under known
headings, or comment blocks in the payload. Decide it against the injected-map
budget — LOD exists to *control* context weight, so a scheme that ships every
level on every read defeats it.