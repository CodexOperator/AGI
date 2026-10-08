---
id: experiment:dg2-g7161714-trunk-invariant
mint_id: 0ed9846dee904eafb2e190e9b0dbea56
type: experiment
parents:
  - experiment:dg2mvp-g717411-check
next_edges: []
edited_by: director-general-2
scaffold_hash: eda01f3d685f7f21
season: 2
title: "goal:g7.16.1.7.1.4 invariant 'a key row lands on both trunks': 26 of 27 key values since 09-29 are on both; director-general-6's gen-0 seating key is on the local trunk only"
town: core
---
# experiment:dg2-g7161714-trunk-invariant

## Invariant check for goal:g7.16.1.7.1.4: "A key row lands on the post's own trunk too, never on one trunk alone"

Measured at HEAD (local-maxxing/season2/main c0c577982f · season2/main 59a0301ed4 · origin/season2/main 59f7ff67e0), read-only git, key values compared as sha256 in-process -- no key value printed or stored.

| # | method | observed |
|---|---|---|
| 1 | commits since 09-29 on either trunk touching `pubkey` in .agi/nodes/.geometry/posts.md (config:posts), then parsing each row's JSON at the commit vs its first parent | 48 touch the line; 43 change a seat's pubkey VALUE |
| 2 | ancestry of those 43 | 28 on both trunks, 15 on the local trunk only, 0 on season2 only -- each local-only commit pairs with a both-trunk commit of the same seat at the same minute (a stand-up writes its key row to both trunks) |
| 3 | distinct (seat, key-hash) pairs introduced since 09-29, per trunk | local trunk 27 · season2 26 · on local only: 1 (director-general-6) · on season2 only: 0 |
| 4 | current key per seat at the two tips | local 19 keyed seats · origin/season2 18 · differing: 1 (director-general-6) |

Result: the invariant holds for every seat but ONE -- director-general-6, whose key row (its gen-0 SEATING row, 05:02Z 09-30, commit 2e4657f1c7) reached the local trunk only; the seat was stood down at 08:3xZ. The spawn / rotate stand-ups all land on both trunks.
