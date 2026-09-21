---
id: goal:g14.13
mint_id: 9d7fd57351ce4e89ad00a1df16c86fda
type: goal
parents:
  - goal:g14
next_edges: []
confidence: 0.9
edited_by: thought-master
goal_id: G14.13
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: ba1ab6c021159cbe
season: 2
seeds:
  - doc:arxiv-2510-05421
  - doc:arxiv-2603-12201
  - doc:arxiv-2607-24653
  - doc:baseten-eagle3-heads
  - doc:baseten-live-draft
  - doc:dead-head
  - doc:deepseek-v4-1-flash
  - doc:glm-5-3-flash
  - doc:lm-trove-2026-09-18-owner-links
  - doc:osd-2310-07177
  - doc:recurrent-looped-transformer
  - doc:tiktok-videos-4b
status: active
tags:
  - local-maxxing
  - treasury
  - digests
title: "G14.13: THE RESEARCH TREASURY — every owner-named paper, repo and model card digested by name (trove-survey / paper-digest on pi), kept as doc: nodes here, its falsifiable rows minted under the track they serve, never as loose chains under g14 (charter 09-13; owner links 09-14 / 09-18 / 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.13

## Agent Notes
**Owner source (2026-09-13 23:32Z, verbatim in doc:l4-owner-decisions; goal:g14 charter):** the thought-master owns "goal:g14 … and its research treasury"; "a very slow, gentle research loop". Owner links arrive as lines in the pane (09-18: turboquant_plus / OrcaBonsai / bonsai2-small-gpu; 09-14: dead-head, tiktok-videos-4b, the looped transformer) and are ingested by the trove-survey and paper-digest workflows.

**Commits to.** Every paper, repo or model card the owner names is digested once (reader → critic → panel → judge, by name, on pi), its digest is a `doc:` node here, its structured stage outputs land in `datasets/workflow-runs/`, and the judge's ranked, falsifiable rows are minted as chunks under the track they serve (G14.6–G14.12) — never as free-floating chains under g14. A digest that produces no falsifiable row is still kept (a treasury entry), but mints nothing.

**Invariants.** One survey per owner link set, never re-run blind (the run dir is the record); every digest quotes file paths and dates and marks MEASURED vs ESTIMATE; a critique stage that times out is recorded as missing on the goal (the 09-20 bonsai2-small-gpu critique); cost per survey stated (≤ 1 USD unless the owner names more).

**Falsifiers.** A treasury row that is minted as a hypothesis without a falsifier, or under g14 directly instead of its track, is a rule violation counted here; the workflow is re-authored if two surveys in a row produce judge rows that cannot be minted as written.

**Done when.** Never — perpetual; reviewed when a track closes (every digest it cites resolves).

**Seeds:** the paper/repo digests re-homed here on 2026-09-20 (cleanliness pass), plus the 09-20 trove-survey run (`datasets/workflow-runs/trove-survey-2026-09-20/`).
