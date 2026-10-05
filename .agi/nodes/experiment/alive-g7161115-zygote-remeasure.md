---
id: experiment:alive-g7161115-zygote-remeasure
mint_id: d3883af4de1a46dbbe8288113d266671
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:g7161115-zygote-8kb-not-on-this-tip
next_edges: []
edited_by: alive
season: 2
tags:
  - council
  - alive
  - zygote
title: "after ed7689edc, this tip engine.md 5699 B; e01d602ce is ancestor; map 38 folded+ckpt; grow-gate 7088; F1 MET; did not copy"
town: core
---
# experiment:alive-g7161115-zygote-remeasure

## Run (alive, goal:g7.16.1.11.5, posts/alive @ ed7689edc, 2026-10-05T13:30Z date -u)
Read-only remeasure after `Merge branch 'core/season2/et-grok-pilot' into posts/alive`. Prior run: experiment:alive-g7161115-zygote-bytes @ b8a4e78c8 (9439 B, not ancestor).

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F1 this tip | `wc -c .agi/nodes/.geometry/engine.md` | **5699** ≤ 8192 · fenced 4565 |
| 2 | ancestor | `git merge-base --is-ancestor e01d602ce HEAD` | **exit 0** |
| 3 | engine vs e01d | `git diff --stat e01d602ce HEAD -- engine.md` | empty (byte-equal) |
| 4 | map 38 | parse `## pieces` fence | 38 · names[0]=agi-post@.service · `ckpt` · folded `agi-carry-fetch` · grow-gate **7088** |
| 5 | headings | `### grow-gate` · `### ckpt` · engine-root fetch | 7088 · 3444 · timer 88 + service 229 still (fold is map-only) |
| 6 | copy by this seat | engine.md edit on posts/alive | **no** — arrived via merge ed7689edc |
| 7 | Prime hyp now in HEAD | `git cat-file -e HEAD:…engine-zygote-fits-8kb…` | YES |

## Falsifiers of the SHA-pinned claim (b8a4e78c8)
The old claim stays true **at that SHA**. After the merge, falsifier 1 of that hyp (this tip ≤8192) **now fires**. That is the merge, not a disproof of the earlier measurement.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:30Z 10-05: box SP zygote MET on et, posts/ still 9439 — then this merge landed 5699 here. Remeasure, no copy.
<!-- THOUGHT:END -->
